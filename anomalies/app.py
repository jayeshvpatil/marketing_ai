import streamlit as st
import pandas as pd
import time
from utils import vertexai


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
        prompt = f"""Explain the anomaly in campaign '{row['campaign']}'. 
        Look at the severity score and other features to explain your finding. 
        Make sure your response is accurate, concise and in one line. 
        Include all the relevant features and make final answer in professional and business tone.
        Here's the data: '{row}'
        """
        explanation = vertexai.generate_text(prompt, stream=False)
        #explanation = response.candidates[0].content.parts[0].text
        #st.toast(explanation)
        anomalies.at[index,'explanation']=explanation
        time.sleep(2)
    st.dataframe(anomalies)

def display_anomalies():
        # Streamlit app
    st.title('Marketing Anomaly Detection')
    # Add a radio button for severity level selection
    severity_level = st.radio("Select Severity Level", ('Low', 'Medium', 'High'), index=2)
    # Show anomalies
    st.subheader('Top 5 Detected Anomalies')
    anomalies = init_anamolies()
    if severity_level:
        filtered_anomalies = filter_anomalies(anomalies,severity_level)
    explain_anomalies(filtered_anomalies)
