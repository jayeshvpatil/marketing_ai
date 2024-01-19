import pandas as pd
import streamlit as st

df= pd.read_csv('generated_analytics_data.csv')
st.write(df.head())
# Calculate key metrics for each campaign
campaign_metrics = df .groupby('campaign').agg({
    'cost': 'sum',
     'impressions': 'sum',
    'clicks': 'sum',
    'users': 'sum',
    'revenue': 'sum', 
    'conversion_rate': 'mean',
    'bounce_rate': 'mean',
    'time_on_site': 'mean' 
})

# Sort the campaigns by revenue in descending order
campaign_metrics = campaign_metrics.sort_values('revenue', ascending=False)

# Print the top 10 campaigns
st.write(campaign_metrics.head(10))