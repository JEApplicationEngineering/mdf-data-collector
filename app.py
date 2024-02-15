# import streamlit, pandas, and numpy
import streamlit as st
import plotly.express as px

from utils.dashboard import *
from utils.tabs import *

#########################################

# main layout
st.set_page_config(
    page_title="eZTR Data Collection",
    layout="wide",
    initial_sidebar_state="auto",
    page_icon=":chart_with_upwards_trend:"
)

#########################################

# set up session state so app interactions don't reset the app.
if "converted" not in st.session_state:
    st.session_state["converted"] = False
else:
    st.session_state["converted"] = True if st.session_state["converted"] else False

if "downloaded" not in st.session_state:
    st.session_state["downloaded"] = False
else:
    st.session_state["downloaded"] = True if st.session_state["downloaded"] else False

if "dbc_file_upload" not in st.session_state:
    files_uploaded = False
else:
    files_uploaded = True if st.session_state["dbc_file_upload"] else False

if "mdf_file_upload" not in st.session_state:
    files_uploaded = False
else:
    files_uploaded = True if st.session_state["mdf_file_upload"] else False

if "groups" not in st.session_state:
    groups = None
else:
    groups = st.session_state['groups']

#########################################

# initialize headers
st.title("eZTR Data Collection")
st.sidebar.header("File Uploader")

tab1, tab2, tab3 = st.tabs(['Metadata', 'Graphs', 'Tables'])

tab1.subheader("Metadata")
tab2.subheader("Graphs")
tab3.subheader("Tables")

#########################################

# display file uploaders in sidebar
with st.sidebar:
    upload_conainter = st.expander('Upload', expanded=True)

    dbc_files = upload_conainter.file_uploader(
        "Upload your .DBC files", 
        type=['dbc'], 
        accept_multiple_files=True,
        key="dbc_file_upload",
        help="Import your .DBC files",
        on_change=reset_page
    )
    mdf_files = upload_conainter.file_uploader(
        "Upload your .MF4 files", 
        type=['mf4', 'mdf'], 
        accept_multiple_files=True,
        key="mdf_file_upload",
        help="Import your MDF files",
        on_change=reset_page
    )
    convert_button = upload_conainter.button(
        label="Convert", 
        on_click=process_convert,
        args=(dbc_files, mdf_files),
        use_container_width=True
    )

#########################################
    
dbc_path = [f'./DBC Files/{dbc.name}' for dbc in dbc_files]
mdf_file_names = [file.name for file in mdf_files]

#########################################

# display each tab
if st.session_state["converted"] and files_uploaded:
    metadata_tab(tab1)
    charts_tab(tab2, mdf_file_names, groups)
    tables_tab(tab3, mdf_file_names, groups)

#########################################

# display download button
if st.session_state["converted"] and not st.session_state['downloaded']:
    with open("tmp/temp_output.zip", "rb") as fp:
        st.sidebar.download_button(
            label="Download Data",
            data=fp,
            file_name="output.zip",
            mime="application/zip",
            on_click=delete_zip,
            type="primary",
            use_container_width=True
        )

if __name__ == "__main__":
    st.caption("")