import streamlit as st
import os, shutil
from DataCollector import DataCollector

@st.cache_data
def convert(mdf_files, dbc_files):
    print("\nconverting...")

    dc = DataCollector(dbc_files)

    mdf_file_names = [file.name for file in mdf_files]
    groups = dict.fromkeys(mdf_file_names)

    for file in mdf_files:
        groups[file.name] = dc.parse(file)
    
    return groups

def reset_page():
    delete_zip()
    st.session_state["converted"]  = False
    st.session_state["downloaded"] = False

def save_files(dbc_files, mdf_files):
    for file in dbc_files:
        if file.name not in os.listdir("./DBC Files"):
            bytes_data = file.read()
            with open(os.path.join("./DBC Files", file.name), 'wb') as f:
                f.write(bytes_data)

def delete_zip():
    if os.path.exists('tmp/temp_output.zip'):
        os.remove('tmp/temp_output.zip')

    if not os.path.exists('tmp/out/'):
        os.makedirs(f'./tmp/out/')

    for dir in os.listdir('tmp/out/'):
        shutil.rmtree(f'tmp/out/{dir}')

    st.session_state["downloaded"] = True

def generate_output(groups, mdf_file_names):
    # loop through mdf files
    for file in mdf_file_names:
        file_prefix = file.split('.')[0]

        # create folder to store csv files
        os.makedirs(f'./tmp/out/{file_prefix}')
        
        # create csv for each PDO
        for key,group in groups[file].items():
            group.to_csv(f'./tmp/out/{file_prefix}/{key}')
    
    # zip output folders
    shutil.make_archive('tmp/temp_output', 'zip', 'tmp/out/')