import vertexai
from google.oauth2 import service_account
import streamlit as st
from vertexai.preview.generative_models import GenerativeModel
from langchain_experimental.agents import create_csv_agent
from langchain.chat_models.vertexai import ChatVertexAI
from langchain.agents.agent_types import AgentType

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
    