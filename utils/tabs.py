import streamlit as st
from datetime import time

def metadata_tab(tab1):
    # display metadata form in sidebar
    metadata_container = tab1.container(border=None)

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
    test_code = row1_col1.selectbox(
        "Test Code",
        options=['PREP400', 'PREPMAX', 'C375', 'C350', 'C325', 'C300', 'C275', 'C250', 'C225', 'C200', 'RES'],
        index=None,
        placeholder=""
    )
    test_area = row1_col2.text_input("Test Area")

    row2_col1, row2_col2, row2_col3 = metadata_container.columns([0.5, 0.5, 1])
    week_num = row2_col1.text_input("Week #")
    form_num = row2_col2.text_input("Form #")
    date     = row2_col3.date_input("Date")

    row3_col1, row3_col2 = metadata_container.columns([1, 1])
    start_time = row3_col1.time_input("Start Time", time(12, 0), step=60*15)
    end_time   = row3_col2.time_input("End Time", time(12, 0), step=60*15)
    start_temp = row3_col1.number_input("Start Amb. Temp.", min_value=40, max_value=110, value=70, step=5)
    end_temp   = row3_col2.number_input("End Amb. Temp.", min_value=40, max_value=110, value=70, step=5)
    start_bat  = row3_col1.number_input("Start Battery Level", min_value=1, max_value=5)
    end_bat    = row3_col2.number_input("End Battery Level", min_value=1, max_value=5)

    # change to multiselect
    weather = metadata_container.text_input("Weather Conditions")
    test_conditions = metadata_container.text_input("Test Area Conditions")
    vehicle_conditions = metadata_container.text_input("Vehicle Operation")
    additional_notes = metadata_container.text_area("Additional Notes")

def charts_tab(tab2, mdf_file_names, groups):
    selected_file1 = tab2.selectbox(
        label="Select .MF4 to View",
        options=mdf_file_names,
        key="selected_file",
    )
    selected_group1 = tab2.selectbox(
        label="Select Group to Graph", 
        options=groups[selected_file1].keys(),
        key="selected_groups",
    )

    if selected_group1:
        print("displaying graphs...")

        group = groups[selected_file1][selected_group1]
        
        # streamlit charts
        for name in group.columns:
            tab2.write(name)
            tab2.line_chart(group[name])
        
        # plotly charts
        # fig = px.line(group, height=1000)
        # fig.update_layout(legend_title=None, xaxis_title=None, hovermode='x unified')
        # st.plotly_chart(fig, use_container_width=True)

def tables_tab(tab3, mdf_file_names, groups):
    selected_file2 = tab3.selectbox(
        label="Select .MF4 to View",
        options=mdf_file_names,
    )
    selected_group2 = tab3.selectbox(
        label="Select Group to Graph", 
        options=groups[selected_file2].keys(),
    )

    if selected_group2:
        print("displaying tables...")

        group = groups[selected_file2][selected_group2]

        tab3.write(selected_group2)
        tab3.dataframe(group)