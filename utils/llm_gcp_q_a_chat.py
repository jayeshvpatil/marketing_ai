import streamlit as st
import pandas as pd
import re
import ast
import sys
from utils import vertexai
from io import StringIO
from datetime import datetime
import markdown
import PIL

#st.title("Go Further AI chat")
def prepare_simple_prompt(query, df):
    column_names = ",".join(df.columns)
    today = datetime.today()
    df_string = df.head(10).to_string()
    prompt_content = f"""
            You are a marketing analyst and you are required to answer business questions and summarize the key insights of given numerical tables. 
            The dataframe has following columns :
            {column_names}  

            Please answer the following business question based on the data in the table : {query}

            Please write in a professional and business-neutral tone. Note that Today's date is {today}
            The answer should only be based on the information presented in the table.
            {df_string}   
            
            """
    #st.write(prompt_content)
    return prompt_content    

def prepare_prompt(query, df):
    column_names = ",".join(df.columns)
    today = datetime.today()
    prompt_content = f"""
  You are Marketing analyst who answers to CMO's business questions by using Python code from preloaded 'df' DataFrame.
    Follow these steps:
    1. Import pandas.
    2. No need to reload 'df'.
    3. Answer this query: {query}.
    4. Generate code for accurate extraction.
    5. Execute for results.
    6. Present professionally.
    
    Key Points:
    - Ensure numeric column recognition.
    - Handle NaN with mean or median.
    - Attend to dates within desired time.
    - Fix non-numeric values.
    - Convert time formats to datetime.
    - Avoid duplicate variable names.
    - Use .2f for numeric output.
    - Maintain proper indentation.
    - DataFrame columns: {column_names}.
    - 'time_on_site' is numeric and is in seconds; 'satisfaction_score' and 'feedback_score' range from 1 to 5.
    - Output using st.write.
    - Include try-except for errors.

    Today's date: {today}.
              """
    return prompt_content

def ask_follow_up(df,answer):
    column_names = ",".join(df.columns)
    prompt_content = f"""
    Always generate a array with list of business questions, 
    the Chief Marketing Officer (CMO) could ask based on the following response:
    "{answer}"
    The questions should be short and precise. Only create 3 questions. 
    Ask questions that only use the information that following columns could provide : {column_names}. 
    Don't suggest the same questions again and again. Remove any unterminated string literal.
    Strictly follow the below shown example output format :
      ['What are my top revenue generating sources',
    'Which campaign  received highest customer satisfaction score last quarter?',
    'What is the averate time user spend on site for direct campaigns?']. 
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
            original_stdout = sys.stdout
            sys.stdout = StringIO()
            exec(code)
            output = sys.stdout.getvalue()
            return markdown.markdown(output)
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
    avatar_img = PIL.Image.open('assets/logo_avatar.png')
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
        avatar = avatar_img if role=='ai' else None
        with st.chat_message(role, avatar=avatar):
            st.markdown(content)
    # Chat input
    (user_input := st.chat_input("Ask anything:")) or (user_input_from_session := st.session_state.get("follow_up_clicked_q"))
    prompt = user_input or user_input_from_session
    if prompt:
        st.session_state['messages'].append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
            #final_prompt = prepare_prompt(prompt, df)
            #st.write(final_prompt)
        #response = vertexai.generate_text(final_prompt,stream=False)
        response = vertexai.generate_chat_agent_response(prompt, df)
        output = response['output']
        st.markdown(output)
        #st.markdown(output)
        st.session_state['messages'].append({"role": "ai", "content": output})
        followup_prompt = ask_follow_up(df,output)
        followup_q = vertexai.generate_text(followup_prompt,stream=False)
        with st.chat_message("ai", avatar=avatar_img):
            try:
                followup_q_list = ast.literal_eval(followup_q)
                #st.write(followup_q)
                if followup_q_list and len(followup_q_list) > 0:
                    for q in (followup_q_list):
                        st.button(q, on_click=click_follow_up_button, args=[q])
            except (SyntaxError, ValueError) as e:
                print(f"Error: {e}")

         

