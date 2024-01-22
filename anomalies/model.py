import pandas as pd
from sklearn.ensemble import IsolationForest
import streamlit as st
import time

def train_model():
    run = st.button("Run model training")
    if run:
        with st.expander("Training Output :"):
            total_steps = 6  # Total number of steps in your process
            with st.spinner("Model training in progress..."):
                progress_bar = st.progress(0)

                # Load your marketing data (replace 'your_data.csv' with your actual data file)
                df = pd.read_csv('data/generated_analytics_data.csv')
                st.success("Data loaded successfully.")
                progress_bar.progress(1 / total_steps)

                # Preprocess 'conversion_rate' column to remove percentage signs and convert to numeric
                df['conversion_rate'] = df['conversion_rate'].replace('%', '', regex=True).astype(float)
                st.success("Data pre-processed.")
                progress_bar.progress(2 / total_steps)

                # Select relevant features for anomaly detection (e.g., cost, CTR, etc.)
                features = df[['cost', 'conversion_rate', 'feedback_score', 'impressions']]
                time.sleep(2)
                st.success("Features selected.")
                progress_bar.progress(3 / total_steps)

                st.write("Training model...")
                # Train Isolation Forest model
                model = IsolationForest(contamination=0.05)  # Adjust contamination based on your data
                model.fit(features)
                time.sleep(4)
                st.success("Model trained.")
                progress_bar.progress(4 / total_steps)

                st.write("Predicting Anomalies...")
                # Predict anomalies (1 for normal, -1 for anomaly)
                df['scores'] = model.decision_function(features)
                df['anomaly'] = model.predict(features)
                time.sleep(3)
                st.success("Anomalies predicted.")
                progress_bar.progress(5 / total_steps)

                df.to_csv('anomalies/updated_anomalies.csv')
                st.write(df.head())
                st.success("Process completed.")
                progress_bar.progress(6 / total_steps)

