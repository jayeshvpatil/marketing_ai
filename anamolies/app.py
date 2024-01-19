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

# Load the data with anomalies
df_with_anomalies = pd.read_csv('anamolies/updated_anamolies.csv')

# Streamlit app
st.title('Marketing Anomaly Detection')
# Add a radio button for severity level selection
severity_level = st.radio("Select Severity Level", ('Low', 'Medium', 'High'), index=2)

# Show anomalies
st.subheader('Detected Anomalies')
anomalies = df_with_anomalies[df_with_anomalies['anomaly'] == -1]

# Define a function to calculate severity based on your criteria
def calculate_severity(row):
    # Example: Use some criteria as filters on the app or may be in logic to get explaination only for top anamolies
    return row['cost'] + 0.5 * row['clicks']

# Apply the function to create the severity column
anomalies['severity'] = anomalies.apply(calculate_severity, axis=1)


# Define a function to classify anomalies based on quantiles
def classify_anomalies(row, quantiles):
    severity = row['severity']

    if severity <= quantiles[0.25]:
        return 'Low'
    elif quantiles[0.25] < severity <= quantiles[0.75]:
        return 'Medium'
    else:
        return 'High'

# Apply the severity classification function
anomalies['severity_level'] = anomalies.apply(classify_anomalies, axis=1, quantiles=anomalies['severity'].quantile([0.25, 0.75]))

# Sort anomalies by severity (you may need to adjust the sorting criteria based on your data)
#top_anomalies = anomalies.sort_values(by=['severity'], ascending=False).head(10)
high_severity_anomalies = anomalies[anomalies['severity_level'] == severity_level].head(5)

# Explain anomalies (provide additional insights or context)

for index, row in high_severity_anomalies.iterrows():
    prompt = f"Explain the anomaly in campaign '{row['campaign']}' with high cost, low CTR, and other features. Make sure your response is accurate, concise and in one line"
    response = model.generate_content(prompt,generation_config=generation_config(), stream=False)
    explanation = response
    st.toast(explanation)
    anomalies['explanation']=explanation
    time.sleep(2)

st.dataframe(anomalies)