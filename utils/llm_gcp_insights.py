import streamlit as st
import pandas as pd
import re
import vertexai
from vertexai.preview.generative_models import GenerativeModel, Part

MODEL_NAME = "gemini-pro"
model = GenerativeModel(MODEL_NAME)

def generation_config():
    return  {
        "max_output_tokens": 1024,
        "temperature": 0.2,
        "top_p": 0.95,
        "top_k": 40
    }


# Generate LLM response
def generate_insights(df):
    column_names = ",".join(df.columns)
    messages= prepare_prompt(df,column_names)
    responses = model.generate_content(messages,generation_config=generation_config(), stream=False)
    st.markdown(responses.text)
   
    
def prepare_prompt(df,column_names):
    prompt_content = f"""
            You are a marketing analyst and you are required to create advanced summarized the key insights of given dataframe.
           {df}
            Please list important, but no more than five, highlights in the given table. Use calculated metrics to justify the higlights.
            Include all essential information.
            Please write in a professional and business-neutral tone.
            Strictly base your notes on the provided information, without adding any external information. The output should be in markdown format.
            """
    return prompt_content    