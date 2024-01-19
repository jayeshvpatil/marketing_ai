from typing import List, Tuple

import pandas as pd
import plotly.express as px
import streamlit as st
from utils import  llm_gcp_q_a_chat,llm_gcp_insights
import streamlit_shadcn_ui as ui

# Set page config

def set_page_config():
    st.set_page_config(
        page_title="Campaign Dashboard",
        page_icon=":bar_chart:",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    st.markdown("<style> footer {visibility: hidden;} </style>", unsafe_allow_html=True)


@st.cache_data
def load_data() -> pd.DataFrame:
    data = pd.read_csv('generated_analytics_data.csv')
    data['date'] = pd.to_datetime(data['date'])
    return data


def filter_data(data: pd.DataFrame, column: str, values: List[str]) -> pd.DataFrame:
    if not values:
        return data
    # Check if the column is a date type, then filter a range
    if pd.api.types.is_datetime64_any_dtype(data[column]):
        # Convert values to datetime objects
        start_date, end_date = pd.to_datetime(values, errors='coerce')
        # Filter data within the date range
        filtered_data = data[data[column].between(start_date, end_date, inclusive='both')]
    else:
        # For non-date columns, use isin
        filtered_data = data[data[column].isin(values)]
    return filtered_data


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
    set_page_config()
    st.title("Marketing Campaign AI")
    data = load_data()
    start_date, end_date,selected_source, selected_medium, selected_campaign = display_sidebar(data)
    
    filtered_data = data.copy()
    filtered_data = filter_data(filtered_data, 'date', [start_date, end_date])
    filtered_data = filter_data(filtered_data, 'source', selected_source)
    filtered_data = filter_data(filtered_data, 'medium', selected_medium)
    filtered_data = filter_data(filtered_data, 'campaign', selected_campaign)

    # Create tabs
    tab_titles = ['Data', 'Insights', 'Q&A', 'Detect','Analyze']
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
    
    # Add content to the Model Evaluation tab
    llm_gcp_q_a_chat.start_chat(filtered_data)
    
    # Add content to the Results Visualization tab
    with tabs[3]:
        st.write('This is where you can detect anamolies')

if __name__ == '__main__':
    main()