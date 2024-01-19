import streamlit as st
import pandas as pd
from openai import OpenAI
import re

client = OpenAI()
MODEL_NAME = "gpt-4"

# Generate LLM response
def generate_response(df, input_query):
    column_names = ",".join(df.columns)
    messages= prepare_prompt(input_query,column_names)
    response = client.chat.completions.create(
model=MODEL_NAME, messages=messages, stream=False
    )
    with st.expander("Code Block", expanded=False):
        st.write(response.choices[0].message.content)
    code_blocks = re.findall(r"```(python)?(.*?)```", response.choices[0].message.content, re.DOTALL)
    # Strip leading and trailing whitespace and join the code blocks
    code = "\n".join([block[1].strip() for block in code_blocks])
    if code:
        try:
            exec(code)
            st.set_option('deprecation.showPyplotGlobalUse', False)
            st.pyplot()
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
        st.success("Done")
    
def prepare_prompt(input_query, column_names):
    prompt_content = f"""
            The dataset is ALREADY loaded into a DataFrame named 'df'. DO NOT load the data again.
            
            The DataFrame has the following columns: {column_names}
            
            Before executing, ensure the data is ready:
            1. Check if columns that are supposed to be numeric are recognized as such. If not, attempt to convert them.
            2. Handle NaN values by filling with mean or median.
            
            Use package Pandas and Matplotlib ONLY. Make sure you import the packages.
            Provide SINGLE CODE BLOCK with a solution using Pandas and Matplotlib plots in a single figure to address the following query:
            
            {input_query}

            - USE SINGLE CODE BLOCK with a solution. 
            - Do NOT EXPLAIN the code 
            - DO NOT COMMENT the code. 
            - ALWAYS WRAP UP THE CODE IN A SINGLE CODE BLOCK.
            - The code block must start and end with ```
            
            - Example code format ```code```
        
            - If the user asks to create plot, Colors to use for background and axes of the figure : #F0F0F6
            - Try to use the following color palette for coloring the plots : #8f63ee #ced5ce #a27bf6 #3d3b41
            
            """
    messages = [
                {
                    "role": "system",
                    "content": "You are a helpful Data analysis assistant who gives a single block without explaining or commenting the code to plot. IF ANYTHING NOT ABOUT THE DATA, JUST politely respond that you don't know.",
                },
                {"role": "user", "content": prompt_content},
            ]
    return messages