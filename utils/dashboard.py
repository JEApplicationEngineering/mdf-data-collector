import streamlit as st
import os
from DataCollector import DataCollector

def convert(mdf_files, dc):
    print("\nconverting...")

    mdf_file_names = [file.name for file in mdf_files]
    groups = dict.fromkeys(mdf_file_names)

    for file in mdf_files:
        groups[file.name] = dc.parse(file)
        st.toast(f"Data collection is complete for {file.name}.")
    
    st.session_state["converted"] = True
    
    return groups

def reset_page():
    st.session_state["converted"] = False

def save_files(dbc_files, mdf_files):
    for file in dbc_files:
        if file.name not in os.listdir("./DBC Files"):
            bytes_data = file.read()
            with open(os.path.join("./DBC Files", file.name), 'wb') as f:
                f.write(bytes_data)
