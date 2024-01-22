import pandas as pd
import numpy as np
import streamlit as st

df = pd.read_csv('data/generated_analytics_data.csv')
import pandas as pd
from datetime import datetime

# Convert numeric columns to numeric
df[['cost', 'impressions', 'clicks', 'users', 'revenue', 'conversion_rate', 'bounce_rate', 'time_on_site']] = df[['cost', 'impressions', 'clicks', 'users', 'revenue', 'conversion_rate', 'bounce_rate', 'time_on_site']].apply(pd.to_numeric, errors='coerce')

# Handle NaN values
df['date'] = pd.to_datetime(df['date'], errors='coerce')
df['time_on_site'] = df['time_on_site'].fillna(df['time_on_site'].mean())

# Convert time formats to datetime format
df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d')

# Calculate average time spent on site by users with high satisfaction scores
high_satisfaction_users = df[df['satisfaction_score'] >= 4]
avg_time_on_site = high_satisfaction_users['time_on_site'].mean()

# Output the result
st.write(f"The average time spent on site by users with high satisfaction scores is {avg_time_on_site:.2f} seconds.")