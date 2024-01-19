import streamlit as st
import pandas as pd
import re

from vertexai.preview.generative_models import GenerativeModel, ChatSession

MODEL_NAME = "gemini-pro"
model = GenerativeModel(MODEL_NAME)

# Generate LLM response
def generate_response(df, input_query):
    chat = model.start_chat()
    column_names = ",".join(df.columns)
    messages= prepare_prompt(input_query,column_names)
    response =  chat.send_message(messages)
    st.write(response.text)
   
    
def prepare_prompt(input_query, column_names):
    prompt_content = f"""
            The dataset is ALREADY loaded into a DataFrame named 'df'. DO NOT load the data again.
            
            The DataFrame has the following columns: {column_names}
            
            Before executing, ensure the data is ready:
            1. Check if columns that are supposed to be numeric are recognized as such. If not, attempt to convert them.
            2. Handle NaN values by filling with mean or median.
            
            Use package Pandas and Matplotlib ONLY. Make sure you import the packages.
            Provide final answer to user's question based on the data using the above library packages. If possible, provide a chart or plot explaining the final answer.
            Here's the question:
            {input_query}

            - Do NOT EXPLAIN the code 
            - Make sure you reply in a business neutral tone based on the available data
            """
    return prompt_content