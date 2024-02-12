import vertexai
from google.oauth2 import service_account
import streamlit as st
from vertexai.preview.generative_models import GenerativeModel
from langchain.chat_models.vertexai import ChatVertexAI
from langchain_experimental.agents import create_pandas_dataframe_agent
from langchain.callbacks import StreamlitCallbackHandler
from datetime import datetime
from langchain.prompts import PromptTemplate

PROJECT_ID = 'dce-gcp-training' # @param {type:"string"}
LOCATION = 'us-central1'  # @param {type:"string"}
MODEL_NAME = "gemini-pro"


def init_vertex():
    credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcs_connections"]
    )
    vertexai.init(project=PROJECT_ID, location=LOCATION, credentials=credentials)

def get_model_config():
    return  {
        "max_output_tokens": 2048,
        "temperature": 0.2,
        "top_p": 0.95,
        "top_k": 40
    }

@st.cache_resource
def get_model():
     init_vertex()
     model = GenerativeModel(MODEL_NAME)
     return model

def get_chat_model():
    chat_model = ChatVertexAI(
    model_name=MODEL_NAME, max_output_tokens=1048, temperature=0.2
) 
    return chat_model

def get_chat_agent(chat_model, df, max_iterations=6):
    pd_agent = create_pandas_dataframe_agent(chat_model, 
                         df, 
                         verbose=True, 
                         handle_parse_errors= True,
                         #return_intermediate_steps=True,
                         max_iterations=max_iterations)
    return pd_agent

def generate_text(prompt, stream=False):
    model = get_model()
    responses = model.generate_content(
            prompt,
            generation_config=get_model_config(),
            stream=stream
    )
    if stream:
        final_response = []
        for response in responses:
            try:
                final_response.append(response.candidates[0].content.parts[0].text)
            except IndexError:
                final_response.append("")
                continue
        return " ".join(final_response)
    else:
        return responses.text
    
def generate_chat_agent_response(query, df):
    chat_model = get_chat_model()
    st_cb = StreamlitCallbackHandler(st.container(),expand_new_thoughts=False)
    today = datetime.today()
    PROMPT = """
            You are working with a pandas dataframe in Python.
            The name of the dataframe is `df`. 
            Remember today's date is {today} for any date relative calculations.
            Answer final answer in a business neutral professional tone in a complete sentence. 
            Do not make up the final answer. If you don't know, simply reply back that you are not able find the final answer and need more details.
            Here's the query : {query}
            """
    try:
        prompt = PromptTemplate(template=PROMPT, input_variables=["query", "today"])
        pd_agent = get_chat_agent(chat_model,df)
        response= pd_agent(prompt.format(query=query, today=today))
        output = response['output']
    except Exception as e:
        response = str(e)
        print(response)
        if response.startswith("Could not parse LLM output: `"):
            response = response.removeprefix("Could not parse LLM output: `").removesuffix("`")
            print(response)
        output = 'I am not able to find the final answer and need more details. Please provide more context and ask precise questions'
    return output