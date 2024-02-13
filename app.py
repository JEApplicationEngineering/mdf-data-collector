# import streamlit, pandas, and numpy
import streamlit as st

from DataCollector import DataCollector
from utils.dashboard import *

# TODO: add form to save to metadata.csv (cut height, ambient temp, etc.)

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

#########################################

# initialize headers
st.title("eZTR Data Collection")
st.sidebar.header("File Uploader")

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
        # type="primary",
        on_click=save_files,
        args=(dbc_files, mdf_files),
        use_container_width=True
    )

#########################################

# initialize data collector object
dbc_path = [f'./DBC Files/{dbc.name}' for dbc in dbc_files]
dc = DataCollector(dbc_path)

#########################################

# display selectbox with DBC groups
if (convert_button or st.session_state["converted"]) and files_uploaded:
    groups = convert(mdf_files, dbc_path)
    st.session_state["converted"] = True

    mdf_file_names = [file.name for file in mdf_files]

    selected_file = st.selectbox(
        label="Select .MF4 to View",
        options=mdf_file_names,
        key="selected_file",
    )
    selected_group = st.selectbox(
        label="Select Group to Graph", 
        options=groups[selected_file].keys(),
        key="selected_groups",
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