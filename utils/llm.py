import streamlit as st
import pandas as pd
from openai import OpenAI
import re

client = OpenAI()
MODEL_NAME = "gpt-4"

# Generate LLM response
def generate_insights(df):
    column_names = ",".join(df.columns)
    messages= prepare_prompt(df,column_names)
    response = client.chat.completions.create(temperature= 0.2,
model=MODEL_NAME, messages=messages, stream=False
    )
    st.write(response.choices[0].message.content)
   
    
def prepare_prompt(df,column_names):
    prompt_content = f"""
            You are a marketing analyst and you are required to summarize the key insights of given numerical tables.
           {df}
            Please list important, but no more than five, highlights in the given table. Use calculated metrics to justify the higlights.
            Please write in a professional and business-neutral tone.
            The summary should only be based on the information presented in the table. 
            """
    messages = [
                {
                    "role": "system",
                    "content": "You are a marketing analyst and you are required to summarize the key insights of given dataframe.",
                },
                {"role": "user", "content": prompt_content},
            ]
    return messages    