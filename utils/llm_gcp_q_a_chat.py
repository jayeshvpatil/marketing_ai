import streamlit as st
import pandas as pd
import re
import vertexai
from vertexai.preview.generative_models import GenerativeModel, Part
import ast

MODEL_NAME = "gemini-pro"
model = GenerativeModel(MODEL_NAME)


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
            You are a marketing analyst helping CMO answer business questions using the dataframe.
            The dataset is ALREADY loaded into a DataFrame named 'df'. DO NOT load the data again. 
            The DataFrame has the following columns: {column_names}
            Use pandas library to come to conclusion. Don't use any deprecated code.Do not explain the code.
            Make sure you reply in a business neutral tone and in a professional manner based on the available data.  Generate the code and execute it to get the final answer.
            Here's the question:
            {query}
            Here's the data:
            {df}
            """
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
            # st.write(response.text)
            final_response.append(response.text)
        except IndexError:
            # st.write(response)
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
        st.write(final_prompt)
        response = generate_response(final_prompt)
        followup_prompt = ask_follow_up(response)
        followup_q = generate_response(followup_prompt)
        followup_q_list = ast.literal_eval(followup_q)
        st.session_state['messages'].append({"role": "assistant", "content": response})
        with st.chat_message("assistant"):
            st.markdown(response)
            for q in (followup_q_list):
                st.button(q, on_click=click_follow_up_button, args=[q])
         

