import streamlit as st
import pandas as pd
import re
import vertexai
from vertexai.preview.generative_models import GenerativeModel
import ast
import sys

MODEL_NAME = "gemini-pro"
model = GenerativeModel(MODEL_NAME)

st.title("Go Further AI chat")

def generation_config():
    return  {
        "max_output_tokens": 2048,
        "temperature": 0,
        "top_p": 0.95,
        "top_k": 40
    }

def prepare_prompt(query, df):
    column_names = ",".join(df.columns)
    prompt_content = f"""
    You are a marketing analyst assisting the CMO in analyzing a pandas DataFrame named df. 
    Your goal is to answer business questions using Python. 
    The question asked by the CMO : {query}.
    The dataset is ALREADY loaded into a DataFrame named 'df'. DO NOT load the data again.
    Complete the following tasks:
    1. Check if numeric columns are recognized as such; convert them if necessary.
    2. Handle NaN values by filling with mean or median. Pay special attention to dates and retrieve dates within the desired time.
    3. Convert all time formats to datetime format; dates should not support sum operations.
    4. Avoid naming variables with duplicate names and use the format string .2f to output numbers.
    5. Ensure the Python code is properly indented.
    6. Use a single code block for the solution. Don't add unnecessary spaces.
    7. Do not explain or comment the code. Wrap up the code in a single code block. 
    8.The DataFrame has columns: {column_names} . Use only these columns for analysis.
                """
    st.write(prompt_content)
    return prompt_content

def generate_response(prompt):
    responses = model.generate_content(
            prompt,
            generation_config=generation_config(),
            stream=True
        )
    final_response = []
    for response in responses:
        try:
            final_response.append(response.candidates[0].content.parts[0].text)
        except IndexError:
            final_response.append("")
            continue
    return " ".join(final_response)

def ask_follow_up(answer):
    prompt_content = f"""
    Generate a array with list of business questions, 
    the Chief Marketing Officer (CMO) could ask based on the provided response:
    {answer}
    The questions should be short and precise. Only create 3 questions. 
    Don't suggest the same questions again and again.
    Final output format should be ["q1","q2","q3]
    """
    return prompt_content

def click_follow_up_button(q):
    st.session_state.follow_up_clicked_q= q

def extract_code(code_text):
    code_blocks = re.findall(r"```(python)?(.*?)```", code_text, re.DOTALL)
    # Strip leading and trailing whitespace and join the code blocks
    code = "\n".join([block[1].strip() for block in code_blocks])
    return code

def exec_code(df, code_response):
    code = extract_code(code_response)
    if code:
        try:
            exec(code)
            output = sys.stdout.getvalue()
            st.write(output)
        except Exception as e:
            error_message = str(e)
            st.error(
                f"📟 Apologies, failed to execute the code due to the error: {error_message}"
            )
            st.warning(
                """
                📟 Check the error message and the code executed above to investigate further.
                Pro tips:
                - Tweak your prompts to overcome the error 
                - Use simpler, concise words
                - Remember, I'm specialized in conveying information about the dataset. Give me context of your question and I can answer better.
            """
            )
    else:
        st.write(code_response) 

def start_chat(df):
    # Initialise session state variables
    if 'messages' not in st.session_state:
        st.session_state['messages'] = []
    clear_button = st.sidebar.button("Clear Conversation", key="clear")

    # Reset conversation
    if clear_button:
        st.session_state.follow_up_clicked_q = ''
        st.session_state['messages'] = []

    if 'follow_up_clicked_q' not in st.session_state:
        st.session_state.follow_up_clicked_q = ''


    # Display previous messages
    for message in st.session_state['messages']:
        role = message["role"]
        content = message["content"]
        with st.chat_message(role):
            st.markdown(content)
    # Chat input
    (user_input := st.chat_input("Ask anything:")) or (user_input_from_session := st.session_state.get("follow_up_clicked_q"))
    prompt = user_input or user_input_from_session
    if prompt:
        st.session_state['messages'].append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
            final_prompt = prepare_prompt(prompt, df)
        response = generate_response(final_prompt)
        exec_code(df, response)
        followup_prompt = ask_follow_up(response)
        followup_q = generate_response(followup_prompt)
        followup_q_list = ast.literal_eval(followup_q)
        st.session_state['messages'].append({"role": "assistant", "content": response})
        with st.chat_message("assistant"):
            st.markdown(response)
            for q in (followup_q_list):
                st.button(q, on_click=click_follow_up_button, args=[q])
         

