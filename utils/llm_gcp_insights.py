import streamlit as st
import pandas as pd
import re
from utils import vertexai


# Generate LLM response
def generate_insights(df):
    column_names = ",".join(df.columns)
    messages= prepare_prompt(df,column_names)
    responses = vertexai.generate_text(messages, stream=False)
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