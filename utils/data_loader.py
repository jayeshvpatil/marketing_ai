import streamlit as st
import pandas as pd
from typing import List, Tuple

#unused for now
def get_data():
    # File uploader for data file
    file_types = ["csv", "xlsx", "xls"]
    data_upload = st.file_uploader("Upload a data file", type=file_types)
    
    if data_upload:
        # Check the type of file uploaded and read accordingly
        if data_upload.name.endswith('.csv'):
            df = pd.read_csv(data_upload)
        elif data_upload.name.endswith('.xlsx') or data_upload.name.endswith('.xls'):
            df = pd.read_excel(data_upload)
        else:
            df = None
        return df
    return None


@st.cache_data
def load() -> pd.DataFrame:
    data = pd.read_csv('data/generated_analytics_data.csv')
    data['date'] = pd.to_datetime(data['date'])
    return data


def filter(data: pd.DataFrame, column: str, values: List[str]) -> pd.DataFrame:
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