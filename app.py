# import streamlit, pandas, and numpy
import streamlit as st
import plotly.express as px

from datetime import time

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

if "groups" not in st.session_state:
    groups = None
else:
    groups = st.session_state['groups']

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
        on_click=process_convert,
        args=(dbc_files, mdf_files),
        use_container_width=True
    )

#########################################

# display metadata form in sidebar
metadata_container = st.sidebar.expander('Metadata', expanded=False)

tester_name = metadata_container.text_input("Tester Name")

start_grass_height = metadata_container.radio(
    "Starting Grass Height", 
    options=[4, 3.75, 3.5, 3.25, 3, 2.75, 2.5, 2.25],
    horizontal=True
)
end_grass_height = metadata_container.radio(
    "Ending Grass Height", 
    options=[3.75, 3.5, 3.25, 3, 2.75, 2.5, 2.25, 2], 
    horizontal=True
)

row1_col1, row1_col2 = metadata_container.columns([1, 1])
test_code = row1_col1.text_input("Test Code")
test_area = row1_col2.text_input("Test Area")

row2_col1, row2_col2, row2_col3 = metadata_container.columns([0.5, 0.5, 1])
week_num = row2_col1.text_input("Week #")
form_num = row2_col2.text_input("Form #")
date     = row2_col3.date_input("Date")

row3_col1, row3_col2 = metadata_container.columns([1, 1])
start_time = row3_col1.time_input("Start Time", time(12, 0), step=60*15)
end_time   = row3_col1.time_input("End Time", time(12, 0), step=60*15)
start_temp = row3_col2.number_input("Start Amb. Temp.", min_value=40, max_value=110, value=70, step=5)
end_temp   = row3_col2.number_input("End Amb. Temp.", min_value=40, max_value=110, value=70, step=5)

# change to multiselect
weather = metadata_container.text_input("Weather Conditions")
test_conditions = metadata_container.text_input("Test Area Conditions")
vehicle_conditions = metadata_container.text_input("Vehicle Operation")
additional_notes = metadata_container.text_area("Additional Notes")

#########################################
    
dbc_path = [f'./DBC Files/{dbc.name}' for dbc in dbc_files]
mdf_file_names = [file.name for file in mdf_files]

#########################################

# display selectbox with DBC groups
if st.session_state["converted"] and files_uploaded:
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

        group = groups[selected_file][selected_group]
        
        # streamlit charts
        for name in group.columns:
            st.write(name)
            st.line_chart(group[name])
        
        # plotly charts
        # fig = px.line(group, height=1000)
        # fig.update_layout(legend_title=None, xaxis_title=None, hovermode='x unified')
        # st.plotly_chart(fig, use_container_width=True)

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