import streamlit as st
import os, shutil
from DataCollector import DataCollector

def process_convert(dbc_files, mdf_files):
    save_files(dbc_files, mdf_files)
    convert(dbc_files, mdf_files)
    generate_output(mdf_files)
    st.session_state["converted"] = True

def save_files(dbc_files, mdf_files):
    for file in dbc_files:
        if file.name not in os.listdir("./DBC Files"):
            bytes_data = file.read()
            with open(os.path.join("./DBC Files", file.name), 'wb') as f:
                f.write(bytes_data)

def convert(dbc_files, mdf_files):
    print("\nconverting...")

    dbc_path = [f'./DBC Files/{dbc.name}' for dbc in dbc_files]
    dc = DataCollector(dbc_path)

    mdf_file_names = [file.name for file in mdf_files]
    groups = dict.fromkeys(mdf_file_names)

    for file in mdf_files:
        groups[file.name] = dc.parse(file)
    
    st.session_state['groups'] = groups

def generate_output(mdf_files):
    groups = st.session_state['groups']
    os.makedirs('tmp/out/')
    
    # loop through mdf files
    for file in mdf_files:
        file_prefix = file.name.split('.')[0]

        # create folder to store csv files
        os.makedirs(f'./tmp/out/{file_prefix}')
        
        # create csv for each PDO
        for key,group in groups[file.name].items():
            group.to_csv(f'./tmp/out/{file_prefix}/{key}')
    
    # zip output folders
    shutil.make_archive('tmp/temp_output', 'zip', 'tmp/out/')

def reset_page():
    delete_zip()
    st.session_state["converted"]  = False
    st.session_state["downloaded"] = False

def delete_zip():
    if os.path.exists('tmp/'):
        shutil.rmtree('tmp/')

    st.session_state["downloaded"] = True
