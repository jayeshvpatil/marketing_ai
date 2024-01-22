import pandas as pd
import plotly.express as px
import streamlit as st
from utils import data_loader,llm_gcp_insights
import streamlit_shadcn_ui as ui
import PIL
from google.oauth2 import service_account
import vertexai

PROJECT_ID = 'dce-gcp-training' # @param {type:"string"}
LOCATION = 'us-central1'  # @param {type:"string"}
# Set page config
def init_vertex():
    credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcs_connections"]
    )
    vertexai.init(project=PROJECT_ID, location=LOCATION, credentials=credentials)

def set_page_config():
    img = PIL.Image.open('assets/genai.png')
    st.set_page_config(
        page_title="Campaign Dashboard",
        page_icon=img,
        layout="wide",
        initial_sidebar_state="expanded",
    )
    st.markdown("<style> footer {visibility: hidden;} </style>", unsafe_allow_html=True)

init_vertex()
set_page_config()

st.image("assets/further-logo.png",width=350)   
st.title('Marketing AI wizard') 


# Sidebar
st.sidebar.header("About")
st.sidebar.markdown(
    "Marketing AI wizard helps you deep dive into your campaigns, detect anamolies, generate insights and chat with your data to answer your business questions"
)

st.sidebar.header("Resources")
st.sidebar.markdown("""
- [Go Further AI Solutions](https://www.gofurther.com/solutions/ai)
- [Financial Services](https://www.gofurther.com/industries/financial-services)
- [Customer Success story](https://www.gofurther.com/customer-stories/increasing-revenue-200-over-three-years-for-b2b-financial-payments-client)                    
"""
)
                 

with open(f"README.md", "r") as f:
    st.markdown(f.read())