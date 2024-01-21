import pandas as pd
from sklearn.ensemble import IsolationForest
import streamlit as st
import time

def train_model():
    run = st.button("Run model training")

    if run:
        with st.status("Downloading data..."):
            # Load your marketing data (replace 'your_data.csv' with your actual data file)
            df = pd.read_csv('data/generated_analytics_data.csv')
            st.write("Pre-processing  data...")
            # Preprocess'conversion_rate' columns to remove percentage signs and convert to numeric
            df['conversion_rate'] = df['conversion_rate'].replace('%', '', regex=True).astype(float)
            # Select relevant features for anomaly detection (e.g., cost, CTR, etc.)
            features = df[['cost', 'conversion_rate', 'feedback_score', 'impressions']]
            time.sleep(2) 
            st.write("Training model...")
            # Train Isolation Forest model
            model = IsolationForest(contamination=0.05)  # Adjust contamination based on your data
            model.fit(features)
            time.sleep(4)
            st.write("Predicting Anamolies..")
            # Predict anomalies (1 for normal, -1 for anomaly)
            df['scores']=model.decision_function(features)
            df['anomaly'] = model.predict(features)
            time.sleep(3)
            df.to_csv('anomalies/updated_anomalies.csv')
            print(df.head())
