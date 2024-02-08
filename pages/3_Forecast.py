import streamlit as st
from google.oauth2 import service_account
from google.cloud import bigquery
import pandas as pd
import random
import string
random.seed(1236)

# Create API client.
credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcs_connections"]
)
client = bigquery.Client(credentials=credentials)


tab1, tab2, tab3 = st.tabs(["Dataset", "Model", "Results"])

with tab1:
    # Perform query.
    # Uses st.cache_data to only rerun when the query changes or after 10 min.
    @st.cache_data(ttl=600)
    def run_query(query):
        query_job = client.query(query)
        rows_raw = query_job.result()
        # Convert to list of dicts. Required for st.cache_data to hash the return value.
        rows = [dict(row) for row in rows_raw]
        return rows
    rows = run_query("SELECT * FROM `bigquery-public-data.iowa_liquor_sales.sales` LIMIT 10")
    # Print results.
    st.write("Sales Dataset")
    df = pd.DataFrame(rows)

    st.dataframe(df)

with tab2:
    
# Assuming these are your dataset columns for selection
    column_options = df.columns
    frequency_options = ["daily", "weekly", "monthly", "yearly", "PER_MINUTE"]

    # Target Column
    target_column = st.selectbox("Target Column", options=column_options, help="Name of the column that the Model is to predict values for.")

    # Time Column
    time_column = st.selectbox("Time Column", options=column_options, help="Name of the column that identifies time order in the time series.")

    # Time-series Identifier Column
    identifier_column = st.selectbox("Time-series Identifier Column", options=column_options, help="Name of the column that identifies the time series.")

    # Data Frequency
    data_frequency = st.selectbox("Data Frequency", options=frequency_options, help="The data frequency of the input time series. The finest supported granularity is 'PER_MINUTE'. When forecasting multiple time-series at once, this argument applies to all individual time series.")

    # Forecast Horizon
    forecast_horizon = st.slider("Forecast Horizon", min_value=1, max_value=365, value=30, step=1, help="Number of periods to forecast into the future. Adjust the slider to set the forecast horizon.")
    model_params = {
        'targetColumn': target_column,
        'timeColumn': time_column,
        'timeSeriesIdentifierColumn': identifier_column,
        'dataFrequency': data_frequency
    }
    st.session_state.model_params = model_params
    forecast_params = {
        'forecastHorizon': forecast_horizon,
    }
    st.session_state.prediction_params = forecast_params

    col1, col2 = st.columns(2)

    with col1:
        markdown_table = f"""
        ### Model Parameters
        
        | Name                         | Value             |
        | ---------------------------- | ----------------- |
        | **Target Column**            | `{model_params['targetColumn']}`           |
        | **Time Column**              | `{model_params['timeColumn']}`            |
        | **Time-Series Identifier Column** | `{model_params['timeSeriesIdentifierColumn']}` |
        | **Data Frequency**           | `{model_params['dataFrequency']}`           |
        """
        st.markdown(markdown_table)
    with col2:
        markdown_table = f"""
        ### Prediction Parameters
        
        | Name                         | Value             |
        | ---------------------------- | ----------------- |
        | **Forecast Horizon**            | `{forecast_params['forecastHorizon']}`           |
        """
        st.markdown(markdown_table)
    

with tab3:
    train_button= st.button('Train Model')
    if train_button:
        query_job = train(model_params,forecast_params)
        # Wait for result
        _ = query_job.result()
        df.write(str(query_job.destination))



# Generate a uuid of a specifed length(default=8)
def generate_uuid(length: int = 8) -> str:
    return "".join(random.choices(string.ascii_lowercase + string.digits, k=length))

def train(model_params,forecast_params):
        project_id = client.project
        dataset_id = generate_uuid()

        # Create training dataset in default region
        bq_dataset = bigquery.Dataset(f"{project_id}.jp_test_gen_ai.{dataset_id}")
        bq_dataset = client.create_dataset(bq_dataset, exists_ok=True)

        bigquery_uri = get_bigquery_table_id(time_column=time_column)

        query = f"""
            CREATE OR REPLACE MODEL `{project_id}.jp_test_gen_ai.{dataset_id}.bqml_arima`
            OPTIONS
            (MODEL_TYPE = 'ARIMA_PLUS',
            TIME_SERIES_TIMESTAMP_COL = '{model_params['timeColumn']}',
            TIME_SERIES_DATA_COL = '{model_params['targetColumn']}',
            TIME_SERIES_ID_COL = '{model_params['timeSeriesIdentifierColumn']}',
            DATA_FREQUENCY = '{model_params['dataFrequency']}',
            HORIZON = {forecast_horizon}
            ) AS
            SELECT
            {model_params['timeColumn']},
            {model_params['targetColumn']},
            {model_params['timeSeriesIdentifierColumn']}}
            FROM
            `{bigquery_uri}`
            """

        # Start the query job
        return client.query(query)

def get_bigquery_table_id(time_column) -> str:
        dataset_id = generate_uuid()
        table_id = generate_uuid()
        project_id = client.project

        bq_dataset = bigquery.Dataset(f"{project_id}.{dataset_id}")
        bq_dataset = client.create_dataset(bq_dataset, exists_ok=True)

        job_config = bigquery.LoadJobConfig(
            # Specify a (partial) schema. All columns are always written to the
            # table. The schema is used to assist in data type definitions.
            schema=[
                bigquery.SchemaField(time_column, bigquery.enums.SqlTypeNames.DATE),
            ],
            # Optionally, set the write disposition. BigQuery appends loaded rows
            # to an existing table by default, but with WRITE_TRUNCATE write
            # disposition it replaces the table with the loaded data.
            write_disposition="WRITE_TRUNCATE",
        )

        # Reference: https://cloud.google.com/bigquery/docs/samples/bigquery-load-table-dataframe
        df = pd.DataFrame()
        job = client.load_table_from_dataframe(
            dataframe=df,
            destination=f"{project_id}.{dataset_id}.{table_id}",
            job_config=job_config,
        )  # Make an API request.
        _ = job.result()  # Wait for the job to complete.

        return str(job.destination)