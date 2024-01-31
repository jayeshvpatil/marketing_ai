import pandas as pd
import numpy as np
import streamlit as st

df = pd.read_csv('data/generated_analytics_data.csv')
import pandas as pd

try:
    df_last_week = df[df['date'].between('2024-01-23', '2024-01-29')]
    top_campaign = df_last_week.groupby('campaign')['revenue'].sum().reset_index().sort_values('revenue', ascending=False).head(1)
    st.write(top_campaign)
except Exception as e:
    st.write("An error occurred while processing the data. Please check the input data and try again.")