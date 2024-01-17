from typing import List, Tuple

import pandas as pd
import plotly.express as px
import streamlit as st
from utils import llm2, llm
import streamlit_shadcn_ui as ui
import pygwalker as pyg
import streamlit.components.v1 as components
from pygwalker.api.streamlit import init_streamlit_comm, get_streamlit_html
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
    data = pd.read_csv('data/ga_source_medium_campaign.csv')
    data['date'] = pd.to_datetime(data['date'], format='%m/%d/%Y')
    return data


def filter_data(data: pd.DataFrame, column: str, values: List[str]) -> pd.DataFrame:
    return data[data[column].isin(values)] if values else data


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
    return_on_investment = f"{(total_revenue - total_cost) / total_cost * 100:.2f}%"
    return [ cost_per_clicks, clicks_through_rate,
            conversion_rate, cost_per_conversion, return_on_investment]



def display_kpi_metrics(kpis: List[float], kpi_names: List[str]):
    st.header("KPI Metrics")
    kpi_counts = len(kpi_names)
    cols = st.columns(kpi_counts)
    for i, (col, (kpi_name, kpi_value)) in enumerate(zip(cols, zip(kpi_names, kpis))):
        #col.metric(label=kpi_name, value=kpi_value)
        with cols[i]:
            ui.metric_card(title=kpi_name, content=kpi_value, description="+20.1% from last month")




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

@st.cache_resource
def get_pyg_html(df: pd.DataFrame) -> str:
    # When you need to publish your application, you need set `debug=False`,prevent other users to write your config file.
    html = get_streamlit_html(df, use_kernel_calc=True, debug=False)
    return html

def main():
    set_page_config()
    st.title("Campaign Dashboard")
    data = load_data()
    start_date, end_date,selected_source, selected_medium, selected_campaign = display_sidebar(data)
    
    filtered_data = data.copy()
    filtered_data = filter_data(filtered_data, 'date', [start_date, end_date])
    filtered_data = filter_data(filtered_data, 'source', selected_source)
    filtered_data = filter_data(filtered_data, 'medium', selected_medium)
    filtered_data = filter_data(filtered_data, 'campaign', selected_campaign)

    # Create tabs
    tab_titles = ['Dashboard', 'Insights', 'Q&A', 'Detect','Analyze']
    tabs = st.tabs(tab_titles)
    
    # Add content to the Data Preprocessing tab
    with tabs[0]:
        kpis = calculate_kpis(filtered_data)
        kpi_names = ["Cost Per Clicks", "Clicks Through Rate", "Conversion Rate", "Cost Per Conversion", "Return On Investment"]
        display_kpi_metrics(kpis, kpi_names)
        st.dataframe(filtered_data)
    
    # Add content to the Model Training tab
    with tabs[1]:
        llm.generate_insights(filtered_data)
    
    # Add content to the Model Evaluation tab
    with tabs[2]:
        question_list = [
        'Which campaign had the highest Click-Through Rate (CTR)? Why might that be the case?',
        'Which campaign achieved the highest Conversion Rate? What factors could contribute to this?',
        'What is the Cost per Conversion for each campaign? How efficient are the campaigns in terms of cost?',
        'Which campaign generated the highest Return on Investment (ROI)? What elements of that campaign contributed to its success?',
        'How do the Cost per Click (CPC) metrics differ between the campaigns? What insights can be drawn from these differences?',
        'What is the overall revenue generated by each campaign? Which campaign contributed the most to the total revenue?',
        'Were there any noticeable trends or patterns in user behavior across the campaigns, considering factors like source and medium?How many rows are there?',
        'How do the Cost per Click (CPC) metrics differ between the campaigns? What insights can be drawn from these differences?',
        'Other']
        q = st.selectbox('Select an example query:', question_list)

        # App logic
        if q == 'Other':
            q = st.text_input('Enter your query:', placeholder = 'Enter query here ...')
        llm2.generate_response(filtered_data, q)
    
    # Add content to the Results Visualization tab
    with tabs[3]:
        st.write('This is where you can detect anamolies')
    with tabs[4]:
        # Initialize pygwalker communication
        init_streamlit_comm()
        components.html(get_pyg_html(filtered_data), width=1000, height=1000, scrolling=True)

if __name__ == '__main__':
    main()