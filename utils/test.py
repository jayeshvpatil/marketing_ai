import pandas as pd
import streamlit as st

df= pd.read_csv('generated_analytics_data.csv')
st.write(df.head())
import pandas as pd

# Convert numeric columns to numeric data type 
df[['cost', 'impressions', 'clicks', 'users', ' revenue', 'conversion_rate', 'bounce_rate', 'time_on_site']] = df[['cost', 'impressions', 'clicks', ' users', 'revenue', 'conversion_rate', 'bounce_rate', 'time_on_site']].apply(pd.to_numeric, errors ='coerce')

# Fill NaN values with mean or median
df['cost'].fillna(df['cost'].mean(), inplace=True)
df['impressions'].fillna(df['impressions'].mean(), inplace=True )
df['clicks'].fillna(df['clicks'].mean(), inplace=True)
df['users'].fillna(df['users'].mean(), inplace=True)
df['revenue'].fillna(df['revenue'].mean(),  inplace=True)
df['conversion_rate'].fillna(df['conversion_rate'].mean(), inplace=True)
df['bounce_rate'].fillna(df['bounce_rate'].mean(), inplace=True)
df['time_on_site'].fillna(df['time_on_site '].median(), inplace=True)

# Convert time formats to datetime format
df['date'] = pd.to_datetime(df['date'])

# Calculate total cost and revenue for each campaign
total_cost = df.groupby('campaign')['cost'].sum().reset_index()
total_revenue  = df.groupby('campaign')['revenue'].sum().reset_index()

# Calculate ROI for each campaign
roi = pd.merge(total_revenue, total_cost, on='campaign')
roi['roi'] = (roi['revenue'] - roi['cost']) / roi['cost']

#  Output the results
output_data = {
    "answer": "The campaign with the highest ROI is {} with a ROI of {:.2f}".format(roi.loc[roi['roi'].idxmax(), 'campaign'], roi.loc[roi['roi'].idxmax(), 'roi'])
}

print(output_data)