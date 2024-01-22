import pandas as pd
import plotly.express as px
import streamlit as st
from utils import data_loader,llm_gcp_insights
import streamlit_shadcn_ui as ui
from typing import List, Tuple
from anomalies import model, app

@st.cache_data
def calculate_kpis(data: pd.DataFrame) -> List[float]:
    total_revenue = data['revenue'].replace('[\$,]', '', regex=True).astype(float).sum()
    total_cost = data['cost'].replace('[\$,]', '', regex=True).astype(float).sum()
    total_clicks = data['clicks'].sum()
    total_impressions = data['impressions'].sum()
    total_users = data['users'].sum()
    cost_per_clicks = f"${total_cost / total_clicks:.2f}"
    clicks_through_rate = f"{total_clicks / total_impressions * 100:.2f}%"
    conversion_rate = f"{total_users / total_clicks * 100:.2f}%"
    cost_per_conversion = f"${total_cost / total_users:.2f}"
    return_on_investment = f"{(total_clicks - total_cost) / total_cost * 100:.2f}%"
    return [ cost_per_clicks, clicks_through_rate,
            conversion_rate, cost_per_conversion]



def display_kpi_metrics(kpis: List[float], kpi_names: List[str]):
    st.header("KPI Metrics")
    kpi_counts = len(kpi_names)
    cols = st.columns(kpi_counts)
    for i, (col, (kpi_name, kpi_value)) in enumerate(zip(cols, zip(kpi_names, kpis))):
        #col.metric(label=kpi_name, value=kpi_value)
        with cols[i]:
            ui.metric_card(title=kpi_name, content=kpi_value)




def display_sidebar(data: pd.DataFrame) -> Tuple[List[str], List[str], List[str]]:
    st.sidebar.image('assets/further-logo.png')
    st.sidebar.header("Filters")
    start_date = pd.Timestamp(st.sidebar.date_input("Start Date", data['date'].min().date()))
    end_date = pd.Timestamp(st.sidebar.date_input("End Date", data['date'].max().date()))
    source = sorted(data['source'].unique())
    selected_source = st.sidebar.multiselect("Select Source", source)
    medium = sorted(data['medium'].unique())
    selected_medium = st.sidebar.multiselect("Select Medium", medium)
    campaign = sorted(data['campaign'].unique())
    selected_campaign = st.sidebar.multiselect("Select Campaign", campaign)

    return start_date, end_date,selected_source, selected_medium, selected_campaign

def main():
    st.title("GoFurther.AI")
    data = data_loader.load()
    start_date, end_date,selected_source, selected_medium, selected_campaign = display_sidebar(data)
    
    filtered_data = data.copy()
    filtered_data = data_loader.filter(filtered_data, 'date', [start_date, end_date])
    filtered_data = data_loader.filter(filtered_data, 'source', selected_source)
    filtered_data = data_loader.filter(filtered_data, 'medium', selected_medium)
    filtered_data = data_loader.filter(filtered_data, 'campaign', selected_campaign)

    # Create tabs
    tab_titles = ['Data', 'Insights', 'Detect']
    tabs = st.tabs(tab_titles)
    
    # Add content to the Data Preprocessing tab
    with tabs[0]:
        kpis = calculate_kpis(filtered_data)
        kpi_names = ["Cost Per Clicks", "Clicks Through Rate", "Conversion Rate", "Cost Per Conversion"]
        display_kpi_metrics(kpis, kpi_names)
        st.dataframe(filtered_data)
    
    # Add content to the Model Training tab
    with tabs[1]:
        llm_gcp_insights.generate_insights(filtered_data)
    
    # Add content to the Results Visualization tab
    with tabs[2]:
        model.train_model()
        app.display_anomalies()

if __name__ == '__main__':
    main()