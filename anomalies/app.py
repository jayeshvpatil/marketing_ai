import streamlit as st
import pandas as pd
import re
import vertexai
from vertexai.preview.generative_models import GenerativeModel, Part
import time

MODEL_NAME = "gemini-pro"
model = GenerativeModel(MODEL_NAME)

def generation_config():
    return  {
        "max_output_tokens": 1024,
        "temperature": 0.2,
        "top_p": 0.95,
        "top_k": 40
    }



def init_anamolies():
    # Load the data with anomalies
    df_with_anomalies = pd.read_csv('anomalies/updated_anomalies.csv')
    anomalies = df_with_anomalies[df_with_anomalies['anomaly'] == -1]
    # Apply the function to create the severity column
    anomalies['severity'] = anomalies.apply(calculate_severity, axis=1)
    # Apply the severity classification function
    anomalies['severity_level'] = anomalies.apply(classify_anomalies, axis=1, quantiles=anomalies['severity'].quantile([0.25, 0.75]))
    return anomalies

# Define a function to calculate severity based on your criteria
def calculate_severity(row):
    # Example: Use some criteria as filters on the app or may be in logic to get explaination only for top anamolies
    return row['cost'] + 0.5 * row['clicks']

# Define a function to classify anomalies based on quantiles
def classify_anomalies(row, quantiles):
    severity = row['severity']
    if severity <= quantiles[0.25]:
        return 'Low'
    elif quantiles[0.25] < severity <= quantiles[0.75]:
        return 'Medium'
    else:
        return 'High'

def filter_anomalies(anomalies, severity_level):
#top_anomalies = anomalies.sort_values(by=['severity'], ascending=False).head(10)
    return  anomalies[anomalies['severity_level'] == severity_level].head(5)

def explain_anomalies(anomalies):
# Explain anomalies (provide additional insights or context)
    for index, row in anomalies.iterrows():
        prompt = f"Explain the anomaly in campaign '{row['campaign']}'. Look at the severity score and other features to explain your finding. Make sure your response is accurate, concise and in one line. Include all the relevant features and make final answer in professional and business tone"
        response = model.generate_content(prompt,generation_config=generation_config(), stream=False)
        explanation = response.candidates[0].content.parts[0].text
        #st.toast(explanation)
        anomalies['explanation']=explanation
        time.sleep(2)
    st.dataframe(anomalies)

def display_anomalies():
        # Streamlit app
    st.title('Marketing Anomaly Detection')
    # Add a radio button for severity level selection
    severity_level = st.radio("Select Severity Level", ('Low', 'Medium', 'High'), index=2)
    # Show anomalies
    st.subheader('Detected Anomalies')
    anomalies = init_anamolies()
    if severity_level:
        filtered_anomalies = filter_anomalies(anomalies,severity_level)
    explain_anomalies(filtered_anomalies)
