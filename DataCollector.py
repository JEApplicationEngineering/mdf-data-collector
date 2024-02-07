import asammdf
import numpy as np
import pandas as pd
import os, glob
from io import BytesIO

# TODO: pull headers from mdf (extracted var)
# TODO: format data into dataframe
# TODO: utilize plotly instead of pandas.plot
# TODO: add dropdown to select which graph to display
# TODO: add comments/minor changes
# TODO: consider changing .xlsx to .csv
# TODO: generate zip file for downloads

class DataCollector:
  def __init__(self, dbc_files: list = []) -> None:
    if not os.path.exists('./output'):
      os.mkdir('./output')

    if len(dbc_files) == 1:
      self.databases = {'CAN': [(dbc_files[0], 0)]}
    elif len(dbc_files) == 2:
      self.databases = {'CAN': [(dbc_files[0], 0), (dbc_files[1], 0)]}
    else:
      print('Please input a .DBC file.')

  def parse(self, mdf_path: str) -> dict:
    """
    Returns the parsed mdf file contents as a a dictionary.

      Parameters:
        mdf_path (str): mdf file name
      
      Returns:
        groups (dict): dictionary of the mdf file contents
    """
    mdf = asammdf.MDF(mdf_path)
    extracted = mdf.extract_bus_logging(database_files=self.databases)
    
    # list of MDF objects
    groups = list(extracted.iter_groups())

    group_names = self.__get_group_names(extracted)

    # linearly maps group_names to indexes of groups
    groups = dict(zip(group_names, groups))
    return groups
  
  def graph(self, groups: dict, folder_path: str = 'output') -> None:
    """
    Generates PNG images for each of the mdf file's column names.

      Parameters:
        groups (dict): dictionary of the mdf file contents
        folder_path (str): output folder path

      Returns:
        None
    """
    for key, group in groups.items():
      ax = group.plot.line(subplots = True, use_index = True, figsize = (20,20), legend = 'upper right', grid = True)
      ax.T.flatten()

      for axis in ax:
        axis.legend(loc = 'upper right')
        axis.figure.savefig(f'./{folder_path}/{key}.png')

  def to_excel(self, groups: dict, folder_name: str = 'output') -> BytesIO:
    output = BytesIO()

    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
      for key,group in groups.items():

        group.to_excel(writer, sheet_name = key)
        
        workbook = writer.book
        worksheet = writer.sheets[key]
        
        (maxRow,maxCol) = group.shape
      
    processed_data = output.getvalue()
    return processed_data

  def to_zip(self, folder_name: str = 'output', *args):
    processed_data = {}
    for file in args:
      print(file)
      output = BytesIO()
      
      with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        for key,group in groups[file].items():

          group.to_excel(writer, sheet_name = key)
          
          workbook = writer.book
          worksheet = writer.sheets[key]
          
          (maxRow,maxCol) = group.shape
        
      processed_data[file] = output.getvalue()
    return processed_data["00000001.MF4"]

  def export(self, groups: dict, folder_name: str = 'output') -> BytesIO:
    """
    Exports the mdf file contents to a specified location.

      Parameters:
        folder_name (str): output folder path
        groups (dict): dictionary of the mdf file contents

      Returns:
        None
    """
    with pd.ExcelWriter(f"./{folder_name}/OUTPUT.xlsx") as writer:
      for key,group in groups.items():

        group.to_excel(writer, sheet_name = key)
        
        workbook = writer.book
        worksheet = writer.sheets[key]
        
        (maxRow,maxCol) = group.shape
        
        # worksheet.insert_image(2, maxCol + 2, f'./{folder_name}/{key}.png' )
        worksheet.insert_image(2, maxCol + 2, f'./output/{key}.png' )

  def format_data(self):
    pass

  def __get_group_names(self, extracted: asammdf.MDF) -> list:
    """
    Retrives and returns the group names of the mdf file as a list.

      Parameters:
        extracted (MDF): extracted CAN signals
      
      Returns:
        group_names (dict): list of the mdf file contents
    """
    groups = extracted.iter_groups(use_display_names=True)

    group_names = []
    for group in extracted.iter_groups(use_display_names=True):
      x = group.keys().values[0]
      split = x.split('.')
      group_names.append(split[1])

    return group_names


"""
.
|--  DataCollector.py
|-- _DBC Files
|   |-- JEeZTRdbc_3.dbc
|   |-- database-01.07.dbc
|   |-- ...
|-- _00000024
|   |-- 00000001.mf4
|   |-- 00000002.mf4
|   |-- OUTPUT.xlsx
|   |-- PDO1 Traction L.png
|   |-- PDO1 Cutter L.png
|   |-- ...
|-- _00000025
|   |-- 00000001.mf4
|   |-- 00000002.mf4
|   |-- OUTPUT.xlsx
|   |-- PDO1 Traction L.png
|   |-- PDO1 Cutter L.png
|   |-- ...
"""
def get_files(folder_name) -> list:
  """
  Returns the requested DBC and MF4 files.

    Parameters:
      folder_name (str): name of the folder to search in

    Returns:
      output_files (list): list of the DBC and MDF files found
  """ 
  # get .mf4/.dbc files in 'folder_name'
  mdf_files = glob.glob(f'./{folder_name}/**/*.mf4', recursive=True)
  dbc_files = glob.glob(f'./{folder_name}/**/*.dbc', recursive=True)

  return [dbc_files, mdf_files]


if __name__ == "__main__":
  # root_folder = input('Enter folder name of stored files: ')
  root_folder = '00000025'

  files = get_files(root_folder)
  print(files, '\n')

  dc = DataCollector(files[0])

  for file in files[1]:
    normal_file = os.path.normpath(file)
    folder_name = normal_file.split('\\')[0]
    groups = dc.parse(file)

    dc.graph(groups, folder_name)
    dc.export(groups, folder_name)
    
    print(f"Data collection is complete for {file}.")
