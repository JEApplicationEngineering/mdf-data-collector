# import streamlit, pandas, and numpy
import streamlit as st
import pandas as pd
import numpy as np

from io import BytesIO

from DataCollector import DataCollector
from utils.dashboard import *

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

#########################################

# initialize headers
st.title("eZTR Data Collection")
st.sidebar.header("File Uploader")

#########################################

# display file uploaders in sidebar
with st.sidebar:
    st.subheader("Upload")

    dbc_files = st.file_uploader(
        "Upload your .DBC files", 
        type=['dbc'], 
        accept_multiple_files=True,
        on_change=reset_page
    )
    mdf_files = st.file_uploader(
        "Upload your .MF4 files", 
        type=['mf4', 'mdf'], 
        accept_multiple_files=True,
        on_change=reset_page
    )
    convert_button = st.button(
        label="Convert", 
        type="primary", 
        use_container_width=True,
        on_click=save_files,
        args=(dbc_files, mdf_files)
    )

#########################################

# initialize data collector object
dbc_path = [f'./DBC Files/{dbc.name}' for dbc in dbc_files]
dc = DataCollector(dbc_path)

#########################################

# display selectbox with DBC groups
if convert_button or st.session_state["converted"]:
    groups = convert(mdf_files, dc) if mdf_files else {}

    mdf_file_names = [file.name for file in mdf_files]

    selected_file = st.selectbox(
        label="Select .MF4 to View",
        options=mdf_file_names,
        key="selected_file",
        placeholder="Select File..."
    )
    selected_group = st.selectbox(
        label="Select Group to Graph", 
        options=groups[selected_file].keys(),
        key="selected_groups",
        placeholder="Select group...",
    )

    if selected_group:
        print("displaying graphs...")
        st.subheader("Graphs")

        # selected = st.session_state['selected_groups']
        group = groups[selected_file][selected_group]
        
        for name in group.columns:
            st.write(name)
            st.line_chart(group[name])

#########################################

# display download button
if st.session_state["converted"]:
    st.sidebar.markdown("---")

    st.sidebar.subheader("Download")
    
    # selected_files = st.sidebar.multiselect(label="Column Types", options=mdf_file_names)

    # df_xlsx = "test"
    # check_disable = False
    # if not selected_files:
    df_xlsx = dc.to_excel(groups["00000001.MF4"])
        # df_xlsx = dc.to_excel(groups, selected_files)
        # check_disable = True

    st.sidebar.download_button(
        label="Download Data",
        data=df_xlsx,
        file_name="output.xlsx",
        mime="application/vnd.ms-excel",
        type="primary",
        use_container_width=True
    )

if __name__ == "__main__":
    st.caption("")