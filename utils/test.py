import pandas as pd
import numpy as np
import streamlit as st

df = pd.read_csv('data/generated_analytics_data.csv')
import pandas as pd

try:
    # Convert numeric columns to numeric
    df[['cost', 'impressions', 'clicks', 'users', 'revenue', 'conversion_rate', 'bounce_rate', 'time_on_site', 'satisfaction_score', 'feedback_score']] = df[['cost', 'impressions', 'clicks', 'users', 'revenue', 'conversion_rate', 'bounce_rate', 'time_on_site', 'satisfaction_score', 'feedback_score']].apply(pd.to_numeric, errors='coerce')

    # Convert date to datetime
    df['date'] = pd.to_datetime(df['date'])

    # Filter data for last week
    last_week_data = df[df['date'].between('2024-01-15', '2024-01-21')]

    # Calculate metrics for last week
    total_cost = last_week_data['cost'].sum()
    total_impressions = last_week_data['impressions'].sum()
    total_clicks = last_week_data['clicks'].sum()
    total_users = last_week_data['users'].sum()
    total_revenue = last_week_data['revenue'].sum()
    avg_conversion_rate = last_week_data['conversion_rate'].mean()
    avg_bounce_rate = last_week_data['bounce_rate'].mean()
    avg_time_on_site = last_week_data['time_on_site'].mean()
    avg_satisfaction_score = last_week_data['satisfaction_score'].mean()
    avg_feedback_score = last_week_data['feedback_score'].mean()

    # Identify the best campaign
    best_campaign = last_week_data.groupby('campaign')['revenue'].sum().idxmax()

    # Output results
    st.write(f"Total Cost: ${total_cost:.2f}")
    st.write(f"Total Impressions: {total_impressions}")
    st.write(f"Total Clicks: {total_clicks}")
    st.write(f"Total Users: {total_users}")
    st.write(f"Total Revenue: ${total_revenue:.2f}")
    st.write(f"Average Conversion Rate: {avg_conversion_rate:.2%}")
    st.write(f"Average Bounce Rate: {avg_bounce_rate:.2%}")
    st.write(f"Average Time on Site: {avg_time_on_site:.2f} seconds")
    st.write(f"Average Satisfaction Score: {avg_satisfaction_score:.2f}")
    st.write(f"Average Feedback Score: {avg_feedback_score:.2f}")
    st.write(f"Best Campaign Last Week: {best_campaign}")

except Exception as e:
    st.write("An error occurred while processing the data. Please check the input data and try again.")