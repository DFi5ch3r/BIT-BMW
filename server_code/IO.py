import anvil.server
import anvil.media

import random
import re
import os
import numpy as np
import pandas as pd
import chardet
import time
import plotly.graph_objects as go
import plotly.io as pio
import shapely.geometry
import pickle
from scipy.spatial.distance import pdist

import json

import openpyxl
import kaleido


from . import serverGlobals
from . import dataAnalysis


# This is a server module. It runs on the Anvil server,
# rather than in the user's browser.
#
# To allow anvil.server.call() to call functions here, we mark
# them with @anvil.server.callable.



###########################################################################################################
# input
###########################################################################################################
@anvil.server.callable
def create_databaseTEST(read_path):
  """
    Creates a test database with predefined entries and random data.

    Args:
        read_path (str): The path to the directory containing the files to be processed.

    Updates:
        serverGlobals.DB: The global variable storing the test database.
  """
  testDB = [
    {
        'ID': 1,
        'Dateiname': 'K12345_12.12.2023_Bauteil1_+X_GL-HL_1',
        'Pfad': '/path/to/folder',
        'Unterpfad': 'subfolder1',
        'Jahr': '2023',
        'Baureihe': 'K12345',
        'Nummer': '123456',
        'Bauteil': 'Bauteil1',
        'Baustufe': 'KEX',
        'Richtung': '+X',
        'Last': 'GL',
        'Gang': '1'
    },
    {
        'ID': 2,
        'Dateiname': 'M67890_11.11.2022_Bauteil2_-Y_VL-HL_2',
        'Pfad': '/path/to/folder',
        'Unterpfad': 'subfolder2',
        'Jahr': '2022',
        'Baureihe': 'M67890',
        'Nummer': '678901',
        'Bauteil': 'Bauteil2',
        'Baustufe': 'BS1',
        'Richtung': '-Y',
        'Last': 'VL',
        'Gang': '2'
    },
      {
        'ID': 3,
        'Dateiname': 'M67890_11.11.1999_Bauteil2_-Y_VL-HL_2',
        'Pfad': '/path/to/folder',
        'Unterpfad': 'subfolder2',
        'Jahr': '1999',
        'Baureihe': 'M67890',
        'Nummer': '678901',
        'Bauteil': 'Bauteil2',
        'Baustufe': 'BS1',
        'Richtung': '-Y',
        'Last': 'VL',
        'Gang': '2'
    },
    {
        'ID': 4,
        'Dateiname': 'M67890_11.11.1999_Bauteil2_-Y_VL-HL_2',
        'Pfad': '/path/to/folder',
        'Unterpfad': 'subfolder2',
        'Jahr': '1999',
        'Baureihe': 'M67890',
        'Nummer': '678901',
        'Bauteil': 'Bauteil2',
        'Baustufe': 'BS1',
        'Richtung': '-Y',
        'Last': 'VL',
        'Gang': '2'
    }

  ]

  # define lists of possible values for random data generatio
  baureihen = ['K12345', 'M67890', 'A11111', 'R22222']
  bauteile = ['Bauteil1', 'Bauteil2', 'Bauteil3', 'Bauteil4']
  richtungen = ['+X', '-Y', '+Z', '-X']
  lasten = ['GL', 'VL', 'GS']
  baustufen = ['KEX', 'BS1', 'FB', 'VS1']
  years = ['2023', '2022', '2021', '2020', '2019', '2018', '2017', '2016', '2015', '2014']

  # generate additional random entries for the test database
  for i in range(5, 15):
      testDB.append({
          'ID': i,
          'Dateiname': f'{random.choice(baureihen)}_{random.randint(1, 31):02d}.{random.randint(1, 12):02d}.{random.choice(years)}_{random.choice(bauteile)}_{random.choice(richtungen)}_{random.choice(lasten)}-HL_{random.randint(1, 5)}',
          'Pfad': f'/path/to/folder{i}',
          'Unterpfad': f'subfolder{i}',
          'Jahr': random.choice(years),
          'Baureihe': random.choice(baureihen),
          'Nummer': f'{random.randint(100000, 999999)}',
          'Bauteil': random.choice(bauteile),
          'Baustufe': random.choice(baustufen),
          'Richtung': random.choice(richtungen),
          'Last': random.choice(lasten),
          'Gang': f'{random.randint(1, 5)}'
      })

  # Store the test database in the global variable
  #return testDB
  serverGlobals.DB = testDB
  #print(serverGlobals.DB)

@anvil.server.callable
def load_database(specificPath = False):
    """
    Load the database from a specified path or a default path if not provided.

    Args:
        specificPath (str, optional): The path to the database file. Defaults to False.

    Returns:
        bool: True if the database was successfully loaded, False otherwise.

    Updates:
        serverGlobals.DB: The global variable storing the loaded database.
    """
    if specificPath:
        path = specificPath
    else:
        path = 'cacheDB.pkl'

    # check if the specified path exists
    if os.path.exists(path):
        with open(path, 'rb') as file:
            serverGlobals.DB = pickle.load(file)
        return True
    else:
        return False

@anvil.server.callable
def loadUploadedDatabase(mediaObject):
    """
    Load the database from an uploaded file.

    Args:
        file (anvil.BlobMedia): The uploaded file containing the database.

    Returns:
        bool: True if the database was successfully loaded, False otherwise.

    Updates:
        serverGlobals.DB: The global variable storing the loaded database.
    """
    with anvil.media.TempFile(mediaObject) as fileName:
        with open(fileName, 'rb') as file:
            serverGlobals.DB = pickle.load(file)

    # save the updated database to a cache file
    pickle.dump(serverGlobals.DB, open("cacheDB.pkl", "wb"))

@anvil.server.callable
def create_database(read_path, addDataToDB = False):
    """
    Create a database from the files in the specified directory path.

    Args:
        read_path (str): The path to the directory containing the files to be processed.
        addDataToDB (bool, optional): If True, append new entries to an existing database. Defaults to False.

    Updates:
        serverGlobals.DB: The global variable storing the created database.

    Database format:
        [
            {
                'ID': int,
                'Dateiname': str,
                'Pfad': str,
                'Unterpfad': str,
                'Jahr': str,
                'Baureihe': str,
                'Nummer': str,
                'Bauteil': str,
                'Baustufe': str,
                'Richtung': str,
                'Last': str,
                'Gang': str
            },
            ...
        ]
    """
    # Extract folder and name from the read_path
    folder, name = os.path.split(read_path)

    # Initialize a list to store all names and subfolders
    names_all = []

    # Initialize a dictionary to store names and subfolders for the current path
    current_data = {
        'names': [],
        'folder': folder,
        'subfolders': []
    }

    # Get all files matching the pattern in the current directory
    current_dir = [os.path.join(dp, f) for dp, dn, filenames in os.walk(os.path.join(folder, name)) for f in filenames if re.match(r'K.*\.txt', f)]

    # Iterate through all files in the current directory
    for file in current_dir:
        current_data['names'].append(os.path.basename(file))
        subfolder = os.path.relpath(os.path.dirname(file), folder)
        current_data['subfolders'].append(subfolder)

    # Append the current data to the names_all list
    names_all.append(current_data)

    # Count the number of empty folders
    empty_folder_vec = [not data['names'] for data in names_all]

    # Calculate the total number of valid files
    total_files = sum(len(data['names']) for data in names_all) - sum(1 for data in names_all for name in data['names'] if 'Kopie' in name)

    # Initialize the database with the required fields
    database = [{
        'ID': 0,
        'Dateiname': '',
        'Pfad': '',
        'Unterpfad': '',
        'Jahr': '',
        'Baureihe': '',
        'Nummer': '',
        'Bauteil': '',
        'Baustufe': '',
        'Richtung': '',
        'Last': '',
        'Gang': ''
    } for _ in range(total_files)]

    # Define regular expressions for extracting information from filenames and paths
    expression = re.compile(r'(?P<Baureihe>[KMAR]+\d*)_?(?:\sMUE2|MÜ_Funtionsba_-|-20|_-|_TUE)*_*(?P<Nummer>V?\d{6})?_\d\d\.\d\d\.(?P<Jahr>\d{4})_(?P<Bauteil>.+)_(?P<Richtung>[\+-][XYZ])?S?_(?P<Last>GL|VL|GS)[_-]HL_(?P<Gang>\d)')
    exp_Baustufe = re.compile(r'.*_(?P<Baustufe>Kex|KEX|BS\d|FB|VS\d|AS|S|Serie)_.*')
    exp_Nummer = re.compile(r'.*(?P<Nummer>\d{6}).*')

    current_pos = 0

    # Iterate through all data in names_all
    for data in names_all:
        if not empty_folder_vec[names_all.index(data)]:
            m = 0

            # Extract Baustufe and Nummer from the folder path
#            tmp_Baustufe = exp_Baustufe.match(data['folder'])
            tmp_Nummer = exp_Nummer.match(data['folder'])

            for name, subfolder in zip(data['names'], data['subfolders']):
                if 'Kopie' not in name:
                    m += 1
                    k = current_pos + m
                    tmp_Baustufe = exp_Baustufe.match(subfolder)
                    tmp = expression.match(name)

                    database[k - 1]['Dateiname'] = name
                    database[k - 1]['Pfad'] = data['folder']
                    database[k - 1]['Unterpfad'] = subfolder
                    database[k - 1]['Jahr'] = tmp.group('Jahr') if tmp else ''
                    database[k - 1]['Baureihe'] = tmp.group('Baureihe') if tmp else ''
                    database[k - 1]['Nummer'] = tmp.group('Nummer') if tmp else (tmp_Nummer.group('Nummer') if tmp_Nummer else '')
                    database[k - 1]['Bauteil'] = tmp.group('Bauteil') if tmp else ''
                    database[k - 1]['Richtung'] = tmp.group('Richtung') if tmp else ''
                    database[k - 1]['Last'] = tmp.group('Last') if tmp else ''
                    database[k - 1]['Gang'] = tmp.group('Gang') if tmp else ''
                    database[k - 1]['Baustufe'] = tmp_Baustufe.group('Baustufe').upper() if tmp_Baustufe else ''

                    database[k - 1]['ID'] = k

            current_pos += m

    # Replace empty entries with "Not found"
    for entry in database:
        for key in entry:
            if not entry[key]:
                entry[key] = 'Not found'

    # If addDataToDB is True, append new entries to the existing database
    if addDataToDB:
        keys = ['Jahr', 'Baureihe', 'Bauteil', 'Baustufe', 'Richtung', 'Last', 'Gang']
        unique_entries = set()
        filtered_database = []

        # Add existing entries to the set of unique entries
        for entry in serverGlobals.DB:
            key_tuple = tuple(entry[key] for key in keys)
            if key_tuple not in unique_entries:
                unique_entries.add(key_tuple)
        # Add new entries to the filtered database if they are unique
        for new_entry in database:
            key_tuple = tuple(new_entry[key] for key in keys)
            if key_tuple not in unique_entries:
                unique_entries.add(key_tuple)
                filtered_database.append(new_entry)

        # Combine the filtered new entries with the existing database
        database = filtered_database + serverGlobals.DB

    database = sorted(database, key=lambda x: x['Baureihe'])

    serverGlobals.DB = database

    if serverGlobals.DB:
        return True
    else:
        return False

@anvil.server.callable
def create_databaseJSON(read_path, addDataToDB = False):
    """
    Create a database from the json files in the specified directory path.

    Args:
        read_path (str): The path to the directory containing the files to be processed.
        addDataToDB (bool, optional): If True, append new entries to an existing database. Defaults to False.

    Updates:
        serverGlobals.DB: The global variable storing the created database.

    Database format:
        [
            {
                'ID': int,
                'Dateiname': str,
                'Pfad': str,
                'Unterpfad': str,
                'Jahr': str,
                'Baureihe': str,
                'Nummer': str,
                'Bauteil': str,
                'Baustufe': str,
                'Richtung': str,
                'Last': str,
                'Gang': str
            },
            ...
        ]
    """
    json_files = []
    for root, dirs, files in os.walk(read_path):
        for file in files:
            if file.endswith('.json'):
                json_files.append(os.path.join(root, file))

    # Calculate the total number of valid files
    total_files = len(json_files)

    # Initialize the database with the required fields
    database = [{
        'ID': 0,
        'Dateiname': '',
        'Pfad': '',
        'Unterpfad': '',
        'Jahr': '',
        'Baureihe': '',
        'Nummer': '',
        'Bauteil': '',
        'Baustufe': '',
        'Richtung': '',
        'Last': '',
        'Gang': ''
    } for _ in range(total_files)]

    current_pos = 0
    for file in json_files:
        with open(file, 'r') as f:
            data = json.load(f)
            data = data['folder_info']
            database[current_pos]['ID'] = current_pos+1
            database[current_pos]['Dateiname'] = file
            database[current_pos]['Pfad'] = read_path
            database[current_pos]['Unterpfad'] = '/'
            database[current_pos]['Jahr'] = re.findall(r'\d+', data['Year'])[0]
            database[current_pos]['Baureihe'] = data['Model']
            database[current_pos]['Nummer'] = data['V_number']
            database[current_pos]['Bauteil'] = data['Bauteil']
            database[current_pos]['Baustufe'] = data['Bauphase']
            database[current_pos]['Richtung'] = data['Axis']
            database[current_pos]['Last'] = data['Last']
            database[current_pos]['Gang'] = data['Gang']
        current_pos += 1

    # Replace empty entries with "Not found"
    for entry in database:
        for key in entry:
            if not entry[key]:
                entry[key] = 'Not found'

    # If addDataToDB is True, append new entries to the existing database
    if addDataToDB:
        keys = ['Jahr', 'Baureihe', 'Bauteil', 'Baustufe', 'Richtung', 'Last', 'Gang']
        unique_entries = set()
        filtered_database = []

        # Add existing entries to the set of unique entries
        for entry in serverGlobals.DB:
            key_tuple = tuple(entry[key] for key in keys)
            if key_tuple not in unique_entries:
                unique_entries.add(key_tuple)
        # Add new entries to the filtered database if they are unique
        for new_entry in database:
            key_tuple = tuple(new_entry[key] for key in keys)
            if key_tuple not in unique_entries:
                unique_entries.add(key_tuple)
                filtered_database.append(new_entry)

        # Combine the filtered new entries with the existing database
        database = filtered_database + serverGlobals.DB

    database = sorted(database, key=lambda x: x['Baureihe'])

    serverGlobals.DB = database

    if serverGlobals.DB:
        return True
    else:
        return False

@anvil.server.callable
def filter_database(key, values, sourceFullDB = True, secondKey = False, returnDB = False):
    """
    Filter the database based on the specified key and values.

    Args:
        key (str): The key to filter the database by.
        values (list): The list of values to filter the database entries.
        sourceFullDB (bool, optional): If True, use the full database from serverGlobals.DB. If False, use the selected
                                       data from serverGlobals.selectedData. Defaults to True.
        secondKey (str, optional): An additional key to filter the database entries. Defaults to False.
        returnDB (bool, optional): If True, return the filtered database. If False, update serverGlobals.selectedData
                                   with the filtered entries. Defaults to False.

    Returns:
        list or None: The filtered database if returnDB is True, otherwise None.

    Updates:
        serverGlobals.selectedData: The global variable storing the filtered database entries if returnDB is False.
    """
    # Access the global database
    if sourceFullDB:
        global_database = serverGlobals.DB
    else:
        global_database = serverGlobals.selectedData

    # Initialize an empty list to store the filtered entries
    filtered_database = []

    # Iterate through each entry in the global database
    for entry in global_database:
        if not secondKey:
            if entry[key] in values:
                # Append the entry to the filtered database
                filtered_database.append(entry)
        else:
            if (entry[key] + '-.-'+entry[secondKey]) in values:
                # Append the entry to the filtered database
                filtered_database.append(entry)

    if returnDB:
        return filtered_database
    else:
        serverGlobals.selectedData = filtered_database

@anvil.server.callable
def excludeMotor():
    """
    Exclude entries with 'Motor' in the 'Bauteil' field from the selected data.

    Updates:
        serverGlobals.selectedData: The global variable storing the filtered database entries.
    """
    # Access the selected data from the global variable
    database = serverGlobals.selectedData
    # Filter out entries where 'Bauteil' contains 'Motor'
    filtered_database = [entry for entry in database if 'Motor' not in entry['Bauteil']]
    # Update the global variable with the filtered data
    serverGlobals.selectedData = filtered_database

@anvil.server.callable
def get_baureihe_and_years():
    """
    Retrieve unique 'Baureihe' and their corresponding 'Years' from the database.

    Returns:
        list: A list of dictionaries, each containing a 'Baureihe' and a list of 'Years'.

    Updates:
        serverGlobals.DB: The global variable storing the database entries.
    """
    # Access the global database
    database = serverGlobals.DB
    # Initialize a dictionary to store 'Baureihe' and their corresponding 'Years'
    baureihe_to_years = {}

    # Iterate through each entry in the database
    for entry in database:
        baureihe = entry['Baureihe']
        year = entry['Jahr']
        if baureihe != 'Not found' and year != 'Not found':
            if baureihe not in baureihe_to_years:
                baureihe_to_years[baureihe] = set()
            baureihe_to_years[baureihe].add(year)

    # Convert the dictionary to a list of dictionaries
    baureihe_years_list = [
      {
          'Baureihe': baureihe,
          'Years': [{'year': year, 'baureihe': baureihe} for year in years]
      }
      for baureihe, years in baureihe_to_years.items()
    ]
    return baureihe_years_list

@anvil.server.callable
def get_unique_values(key, sourceSelectedData=False, prefixes = False):
    """
    Retrieve unique values for a specified key from the database.

    Args:
        key (str): The key to retrieve unique values for.
        sourceSelectedData (bool, optional): If True, use the selected data from serverGlobals.selectedData. If False, use the full database from serverGlobals.DB. Defaults to False.
        prefixes (bool, optional): If True, return unique prefixes of the values. Defaults to False.

    Returns:
        list: A sorted list of unique values or prefixes.

    Functions called:
        - None

    """
    # initialize a set to store unique values
    unique_values = set()

    # determine the source database
    if sourceSelectedData:
      DB = serverGlobals.selectedData
    else:
      DB = serverGlobals.DB

    # iterate through each entry in the database
    for entry in DB:
        if key in entry:
            unique_values.add(entry[key])

    if prefixes:

        unique_prefixes = set()
        # initialize a dictionary to count prefix occurrences
        prefix_counts = {}

        # iterate through each unique value
        for value in unique_values:
            parts = value.split('_')
            for i in range(1, len(parts) + 1):
                prefix = '_'.join(parts[:i])
                if prefix not in prefix_counts:
                    prefix_counts[prefix] = 0
                prefix_counts[prefix] += 1

        # add prefixes that occur more than once or are in unique values
        for prefix, count in prefix_counts.items():
            if count > 1 or prefix in unique_values:
                unique_prefixes.add(prefix)

        return sorted(list(unique_prefixes))

    else:
        return sorted(list(unique_values))

@anvil.server.callable
def loadCoGdata(rootPath):
    """
    Load Center of Gravity (CoG) data from CSV files in the specified root path.

    Args:
        rootPath (str): The root directory path containing the 'Schwerpunktdaten' folder with CoG data files.

    Updates:
        serverGlobals.CoGData: The global variable storing the processed CoG data.
        serverGlobals.wheelbase: The global variable storing the wheelbase information.

    Functions called:
        - detect_encoding
        - os.walk
        - pd.read_csv
        - np.mean
        - shapely.geometry.MultiPoint
    """

    # Initialize an empty list to store CoG file data
    CoGData = []

    # Construct the path to the 'Schwerpunktdaten' directory
    path = rootPath + '/Schwerpunktdaten'

    # Initialize an empty list to store paths to CSV files
    cog_files = []

    # Recursively search for CSV files in the 'Schwerpunktdaten' directory
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith('.csv'):
                cog_files.append(root + '/' + file)

    # Filter out directories from the list of files
    cog_files = [file for file in cog_files if not os.path.isdir(file)]

    if len(cog_files) == 0:
        print("No cog files found in the specified directory.")
        return

    # Process each CSV file
    for file in cog_files:
        encoding = detect_encoding(file)

        # Read wheelbase data from 'Radstände.csv' file
        if os.path.basename(file) == 'Radstände.csv':
            wheelbase = pd.read_csv(file, encoding=encoding, delimiter=';').values.tolist()
            if wheelbase[0][0] == 'Baureihe':  # Remove the first line if it contains headers
                wheelbase = wheelbase[1:]
            continue

        # Extract the base name of the file (without extension) as the 'Baureihe'
        baureihe = os.path.splitext(os.path.basename(file))[0]

        try:
            # Read the CSV file into a DataFrame
            tmp_cogdata_raw = pd.read_csv(file, encoding=encoding, delimiter=';')
        except pd.errors.ParserError as e:
            print(f"Error parsing {file}: {e}")
            continue

        # Extract part names and CoG values from the DataFrame
        raw_parts = tmp_cogdata_raw.iloc[:, 0].astype(str).values
        raw_cogs_tmp = tmp_cogdata_raw.iloc[:, 1:].values

        # Remove the first column from the CoG values
        raw_cogs = []
        for i in range(raw_cogs_tmp.shape[0]):
            raw_cogs.append(raw_cogs_tmp[i][1:])
        raw_cogs = np.array(raw_cogs)

        # Identify unique parts and create an index array
        parts, comps_idx = np.unique(raw_parts, return_inverse=True)

        # Initialize an array to store the mean CoG values for each unique part
        cogs = np.zeros((len(parts), 3))

        # Calculate the mean CoG values for each unique part
        for part_index in range(len(parts)):
            part_cog_mean = np.mean(raw_cogs[comps_idx == part_index, :], axis=0)
            cogs[part_index, :] = part_cog_mean

        # Determine the CoG of the 'Schwingenlager' part for transformation
        cog_swila = cogs[np.char.find(list(parts), "SwiLa Links und Recht") >= 0, :]

        # Adjust the CoG values based on the CoG of the 'Schwingenlager' part
        cogs = cogs - cog_swila

        # Append the processed CoG data to the list
        CoGData.append({
            'Baureihe': baureihe,
            'parts': parts,
            'cogs': cogs
        })

    # Store the processed CoG data and wheelbase information in global variables
    wheelbase = [{'Baureihe': item[0], 'Radstand': item[1]} for item in wheelbase]

    for entry in CoGData:
        for entry2 in wheelbase:
            if entry2['Baureihe'] == entry['Baureihe']:
                wb =  entry2['Radstand']
        entry['cogs'] = entry['cogs']/wb

    serverGlobals.CoGData = CoGData
    serverGlobals.wheelbase = wheelbase

@anvil.server.callable
def CoG_TranslationTable():
    """
    Creates a translation table for CoG data (adapted from matlab tool).

    Returns:
        dict: A dictionary where keys are strings in CoG data and values are lists of corresponding strings in measurement data.
    """
    trans_tab = {
        "Batterie (Blei)": ["Batterie"],
        "Blinker / FIBL": ["Blinker_h_l", "Blinker_h_r", "Blinker_hi_li", "Blinker_hi_re", "Blinker_v_l", "Blinker_v_r", "Blinker_vo_li", "Blinker_vo_re", "Blinker_LH_o_A", "Blinker_RH_o_A", "Blinker_hi_li", "Blinker_hi_re", "Blinker_vo_li", "Blinker_vo_re"],
        "Federung Hinten": ["FB_H_o", "FB_H_u", "FB_hi_ob_Ant", "FB_hi_un_Ant", "Federb_hi_Ant_o", "Federb_hi_Ant_u", "Federb_hi_Ausgl"],
        "Frontträger": ["FrontTr_l_u", "FrontTr_r_u", "Frontr_Ant_o", "Frontr_Ant_o", "Frontr_Ant_u", "Fronttr_Antw_ob", "Fronttr_Antw_u"],
        "HECU": ["Hecu", "Hecu Anb", "Hecu2", "Hecu_A", "Hecu_Anb", "Hecu_StG_Deck_re", "Hecu", "Hecu Anb", "Hecu_A", "Hecu_Anb", "Hecu_u_Anb"],
        "Heckleute": ["Heckl_Anb", "Heckl_Ant", "Heckl_oben"],
        "HRM": ["HeckR_re_vo_ob", "HeckRa_RAP_L", "HeckRa_RAP_R", "HeckRa_RAP_l", "HeckRa_RAP_r", "HeckRa_l_m_o", "HeckRa_l_m_u", "HeckRa_l_o_A", "HeckRa_l_u_A", "HeckRa_r_m_o", "HeckRa_r_m_u", "HeckRa_r_o_A", "HeckRa_r_u_A", "Heckr_RAP_li", "Heckr_RAP_re", "Heckr_li_hi", "Heckr_re_hi", "HeckRa_RAP_l", "HeckRa_RAP_r", "HeckRa_l_o_A", "HeckRa_r_o_A", "Heckr_RAP_li", "Heckr_RAP_re", "Heckr_li_mi_o", "Heckr_li_mi_ob", "Heckr_re_hi", "Heckr_re_mit_ob", "Heckr_re_mit_u", "Heckr_re_vo_ob", "Heckr_re_vo_u", "Heckr_li_vo_o", "Heckr_li_vo_ob", "Heckr_li_vo_u", "Heckr_re_mi_o", "Heckr_re_mi_ob", "Heckr_re_vo_o", "Heckr_re_vo_ob", "Heckr_re_vo_u"],
        "I-Kombi": ["I-Kombi", "I-Kombi_ob"],
        "Kennzeichenträger": ["KennzTr_l_o_A", "KennzTr_r_o_A", "KennzTräger"],
        "Kennzeichnenleuchte": ["KennzL_m", "KennzLeuchte", "KennzLeuchte_Anb", "KennzLeuchte"],
        "Keylessride": ["KeylRide_Anb_GP", "KeylRide_Anb_Tr", "KeylRide_Anb_li", "KeylRide_Anb_re", "KeylRide_GrPl_li", "KeylRide_GrPl_re", "KeylRide_ob_hi", "KeylRide_ob_vo", "Keyl_Anb_rs_li", "Keyl_Ant_o_hi", "Keyl_Ant_o_vo", "Keyl_GrPl_li", "Keyl_GrPl_re", "Keyl_Halter_li_o", "Keyl_Halter_li_u", "Keyl_Ride_Anb", "Keyl_Ride_Ant", "Keyl_Ride_Ant_Gr", "Keyl_Ride_Ant_ob"],
        "Kofferträger": ["Koffer_Anb_li", "Koffer_Anb_re"],
        "Lenkerarmaturen": ["LKR-Arma_L", "LKR-Arma_R", "LKR_Arma_l", "LKR_Arma_r", "Lenker_Arma_li", "Lenker_Arma_re"],
        "Lenkergrundplatte": ["LKRGrPl_m", "LenkerGrPl", "LenkerGrPl_2", "LenkerGrPl_mi", "Lenker_Gr_Pl", "LenkerGrPl", "Lenkergrdpl"],
        "Motor": ["Motor", "Motor2"],
        "SAF-Slave": ["SAF"],
        "Scheinwerfer": ["SW_Ant_li", "SW_Ant_re", "SW_l", "SW_r", "SW_Anb_li", "SW_Anb_li_o", "SW_Anb_li_u", "SW_Anb_re", "SW_Anb_re_o", "SW_Anb_re_u", "SW_Antw_li", "SW_Antw_re", "SW_Geh_Ant_li", "SW_Geh_Ant_re", "SW_LED_Steuerg", "Scheinw_Anb_li", "Scheinw_Anb_re", "Scheinw_Geh_hi", "Scheinw_Geh_ob"],
        "Seitenstützenschalter": ["SSS"],
        "Sensorbox": ["Sensorbox", "Sensorbox_Anb", "Sensorbox_Ant", "Sensorbox_Integr", "Sensorbox_innen", "Sensorbox_l_A", "Sensorbox_r_A", "Sensorbox_Anb_al", "Sensorbox_Ant", "Sensorbox_Ant_ne", "Sensorbox_Integr", "Sensorbox_Steck", "Sensorbox_innen", "Sensorbox_li_Anb", "Sensorbox_r_A", "Sensorbox_re_Anb", "SB_Aufn_Fahrer_h", "SB_Aufn_Fahrer_v", "SB_Aufn_Sozius_h", "SB_Aufn_Sozius_v", "Sensorbox_Anb", "Sensorbox_Ant", "Sensorbox_Antw"],
        "Steuerkopf": ["Steuerkopf", "Steuerkopf ob", "Steuerkopf_o", "Steuerkopf_ob", "Steuerkopf_u", "Steuerkopf_un", "Steuerkopf_unt"],
        "SwiLa Links und Rechts": ["SchwiLa_L", "SchwiLa_R", "SchwiLa_l", "SchwiLa_r", "SchwingenL_li", "SchwingenL_re", "Schwingenlager_r", "SchwiLa_l", "SchwiLa_r", "Schwingenl_li", "Schwingenl_re", "Schwingenl_li", "Schwingenl_re"],
        "Seitenstützenschalter": ["Seitenst_Schalt"],
        "Tank": ["Tank_h_A", "Tankdeckel", "Tank_Anb_hi", "Tank_Anb_vo_li", "Tank_Anb_vo_re", "Tank_Anbind_hi", "Tank_Anb_vo_li", "Tank_Anb_vo_re", "Tank_Anbind_hi", "Tankdeckel"],
        "Zundlenkschloss": ["ZLS", "ZLS_A", "ZLS_r_A", "ZLS Anb", "ZLS_Anb", "ZLS_Ant_GrPl", "ZLS_Ant_Seite"]
    }
    return trans_tab

@anvil.server.callable
def addCoGdataToDB():
    """
    Add Center of Gravity (CoG) data to the database entries.

    Updates:
        serverGlobals.DB: The global variable storing the database entries with added CoG data.

    Functions called:
        - CoG_TranslationTable
    """
    # create a set to store unique 'Baureihe' values from CoG data
    baureihen = set()
    for entry in serverGlobals.CoGData:
        baureihen.add(entry['Baureihe'])
    baureihen = list(baureihen)

    # get the translation table for CoG data
    translationTable = CoG_TranslationTable()

    # iterate through each entry in the database
    for entry in serverGlobals.DB:
        if entry['Baureihe'] in baureihen:
            for CoG in serverGlobals.CoGData:
                if CoG['Baureihe'] == entry['Baureihe']:
                    translation = False
                    for key, values in translationTable.items():
                        if entry['Bauteil'] in values:
                            translation = key
                            # find the index of the translated part in CoG data
                            cogIndex = list(CoG['parts']).index(translation)
                            # add CoG data to the database entry
                            entry['cog'] = CoG['cogs'][cogIndex]
                            entry['cog_Bauteil'] = translation
                            break

@anvil.server.callable
def readData(selectedData = True, readFromJson = False):
    """
    Read data from files and update the database entries with the data.

   Args:
    selectedData (bool, optional): If True, use the selected data from serverGlobals.selectedData.
                                   If False, use the full database from serverGlobals.DB. Defaults to True.
    readFromJson (bool, optional): If True, read data from JSON files. If False, read data from text files. Defaults to False.

    Updates:
        serverGlobals.DB: The global variable storing the database entries with added data.
        serverGlobals.selectedData: The global variable storing the selected database entries with added data.

    Functions called:
        - None
    """
    start_time = time.time()

    # determine the source database
    if selectedData:
        db = serverGlobals.selectedData
    else:
        db = serverGlobals.DB

    total_entries = len(db)
    progress_interval = max(1, total_entries // 10)  # Print progress every 10% or at least once

    # iterate through each entry in the database
    for i, entry in enumerate(db):
        # check if the entry already has 'data'
        if 'data' in entry:
            continue

        filePath = os.path.join(entry['Pfad'], entry['Unterpfad'], entry['Dateiname'])
        if not "Kopie" in filePath:
            # load the data from the file
            if readFromJson:
                filePath = os.path.join(entry['Pfad'], entry['Dateiname'])
                input = json.load(open(filePath, 'r'))
                input = input['content'].split(';')
                input.pop(0)
                input.pop(0)
                input.pop(-1)
                input.pop(-1)
                try:
                    data = np.array( [list(map(float, item.split(','))) for item in input] )
                except:
                    print(f"Skipped {entry['Dateiname']}, since Data could not be read")
                    continue
            else:
                data = np.loadtxt(filePath)

            # check if the data length is 800
            if len(data) == 800:
                # update the entry with the loaded data
                entry['data'] = data

                # Find the corresponding element in serverGlobals.DB and update it
                for db_entry in serverGlobals.DB:
                    if all(db_entry[key] == entry[key] for key in ['Jahr', 'Baureihe', 'Bauteil', 'Baustufe', 'Richtung', 'Last', 'Gang']):
                        db_entry['data'] = data
                        break
            else:
                print(f"Skipped {entry['Dateiname']}, since Data length is {len(data)}")
        else:
            print(f"Skipped {entry['Dateiname']}, since it is a copy")

        # Print progress
        if (i + 1) % progress_interval == 0 or (i + 1) == total_entries:
            print(f"Progress: {i + 1}/{total_entries} entries processed")

    print(f"Data reading completed in {time.time() - start_time:.2f} seconds")

    # save the updated database to a cache file
    pickle.dump(serverGlobals.DB, open("cacheDB.pkl", "wb"))

def detect_encoding(file_path):
    """
    Detects the encoding of a given file using the chardet library.

    Args:
        file_path (str): The path to the file whose encoding needs to be detected.

    Returns:
        str: The detected encoding of the file.

    Functions called:
        - None
    """
    with open(file_path, 'rb') as f:
        result = chardet.detect(f.read())
    return result['encoding']

###########################################################################################################
# output
###########################################################################################################
@anvil.server.callable
def getPlot(clusteringMethod, component, envelopeMethod):
    """
    Generate a plot based on the specified clustering method, component, and envelope method.

    Args:
        clusteringMethod (str): The method used for clustering ('component', 'frequency', 'position').
        component (str): The component to be plotted.
        envelopeMethod (str): The method used to generate the envelope.

    Returns:
        tuple: A tuple containing the plotly figure object, the envelope data, and the mean standard deviation.

    Functions called:
        - dataAnalysis.generateSuperEnvelope
    """
    plotData = []
    showLegend = False

    # Determine the clusters and envelope color based on the clustering method
    if clusteringMethod == 'component':
        clusters = serverGlobals.clusters_components
        envelopeColour = 'purple'
        showLegend = True
    elif clusteringMethod == 'frequency':
        clusters = serverGlobals.clusters_frequencies
        envelopeColour = 'red'
    elif clusteringMethod == 'position':
        clusters = serverGlobals.clusters_positions
        envelopeColour = 'gold'

    # Collect plot data for the specified component
    for cluster in clusters:
        for comp in cluster['components']:
            if component in comp:
                plotData.append(cluster)

    # Initialize the plotly figure
    fig = go.Figure()
    fig.update_layout(
        showlegend = showLegend,
        xaxis_title='<b>' + 'f [Hz]' + '</b>',
        yaxis_title='<b>' + 'a [m/s²]' + '</b>',
        title='<b>' + component + ' - ' + clusteringMethod + ' based clustering' + '</b>',
        title_x=0.5,
        plot_bgcolor='white',
        xaxis=dict(
            showline=True,
            linewidth=2,
            linecolor='black',
            mirror=True,
            showgrid=True,
            gridcolor='rgb(211,211,211)',
            gridwidth=1,
            griddash='dot',
        ),
        yaxis=dict(
            showline=True,
            linewidth=2,
            linecolor='black',
            mirror=True,
            showgrid=True,
            gridcolor='rgb(211,211,211)',
            gridwidth=1,
            griddash='dot',
        ),

    )
    # Add lines to the plot
    if plotData:
        superEnvelope = dataAnalysis.generateSuperEnvelope(plotData, envelopeMethod,component)

        for cluster in plotData:
            fig.add_trace(go.Scatter(x=cluster['frequencies'], y=cluster['envelope'], name=str(cluster['name']),  mode='lines', line=dict(color='black', width=1)))

        fig.add_trace(go.Scatter(x=superEnvelope['frequencies'], y=superEnvelope['envelope'],name='prediction', mode='lines', opacity=0.5, line=dict(color=envelopeColour, width=5)))

        return fig, [superEnvelope['frequencies'], superEnvelope['envelope']], superEnvelope['meanStdDev']
    else:
        return False, [], []

@anvil.server.callable
def getCogPlot():
    """
    Generate a plot of Center of Gravity (CoG) data for selected components.

    Groups the data by 'Baureihe' and 'Jahr', and plots the CoG for each group.
    Additionally, plots the clusters if available.

    Returns:
        plotly.graph_objects.Figure: The generated plotly figure object.

    Functions called:
        - None
    """
    # Group data by Baureihe and Jahr
    grouped_data = {}
    for entry in serverGlobals.selectedData:
        if 'cog' in entry:
            baureihe = entry.get('Baureihe')
            jahr = entry.get('Jahr')
            cog = entry.get('cog')
            cogBauteil = entry.get('cog_Bauteil')

            key = (baureihe, jahr)
            if key not in grouped_data:
                grouped_data[key] = {'cogs': [], 'cogBauteil': []}
            grouped_data[key]['cogs'].append(cog)
            grouped_data[key]['cogBauteil'].append(cogBauteil)

    fig = go.Figure()

    # Plot CoG for each Baureihe-year combination
    for (baureihe, jahr), data in grouped_data.items():
        cogs = data['cogs']
        cogBauteil = data['cogBauteil']
        x = [cog[0] for cog in cogs]
        y = [cog[2] for cog in cogs]
        text = cogBauteil
        fig.add_trace(go.Scatter(
            x=x, y=y,
            mode='markers+text',
            marker=dict(size=5),
            text=text,
            textposition='top center',
            name=f'{baureihe} ({jahr})'
        ))

    # Plot clusters if available
    if serverGlobals.clusters_positions:
        for cluster in serverGlobals.clusters_positions:
            # Extract x and y coordinates of the cluster's center of gravity (CoG)
            x = list(cluster['cogs'][:, 0])
            y = list(cluster['cogs'][:, 2])
            # Calculate the convex hull of the CoG points
            convex_hull = shapely.geometry.MultiPoint([xy for xy in zip(x, y)]).convex_hull
            # Check if the convex hull is a polygon or a line
            if isinstance(convex_hull, shapely.geometry.Polygon):
                coords = np.array(convex_hull.exterior.coords)
            else:
                coords = np.array(convex_hull.coords)
            # Add the convex hull as a trace to the plot
            fig.add_trace(go.Scatter(x=coords[:, 0], y=coords[:, 1], mode='lines', fill="toself", name='cluster ' + str(cluster['name'])))

    fig.update_layout(
        xaxis_title='<b>' + 'x/wheelbase [-]' + '</b>',
        yaxis_title='<b>' + 'y/wheelbase [-]' + '</b>',
        title='<b> CoG of all components </b>',
        title_x=0.5,
        plot_bgcolor='white',
        xaxis=dict(
            showline=True,
            linewidth=2,
            linecolor='black',
            mirror=True,
            showgrid=True,
            gridcolor='rgb(211,211,211)',
            gridwidth=1,
            griddash='dot',
        ),
        yaxis=dict(
            showline=True,
            linewidth=2,
            linecolor='black',
            mirror=True,
            showgrid=True,
            gridcolor='rgb(211,211,211)',
            gridwidth=1,
            griddash='dot',
        ),
    )
    return fig

@anvil.server.callable
def getOverviewPlot(component, compPlot, posPlot, freqPlot):
    """
    Generate an overview plot combining component, position, and frequency-based predictions.

    Args:
        component (str): The component to be plotted.
        compPlot (plotly.graph_objects.Figure): The plotly figure object for component-based prediction.
        posPlot (plotly.graph_objects.Figure): The plotly figure object for position-based prediction.
        freqPlot (plotly.graph_objects.Figure): The plotly figure object for frequency-based prediction.

    Returns:
        plotly.graph_objects.Figure: The generated plotly figure object.

    Functions called:
        - None
    """

    fig = go.Figure()
    if compPlot:
        fig.add_trace(compPlot.data[-1])
        fig.data[-1].name = 'component based prediction'
        fig.data[-1].line.color = 'purple'
    if posPlot:
        fig.add_trace(posPlot.data[-1])
        fig.data[-1].name = 'position based prediction'
        fig.data[-1].line.color = 'gold'
    if freqPlot:
        fig.add_trace(freqPlot.data[-1])
        fig.data[-1].name = 'frequency based prediction'
        fig.data[-1].line.color = 'red'

    fig['data'][0]['showlegend']=True

    fig.update_layout(
        xaxis_title='<b>' + 'f [Hz]' + '</b>',
        yaxis_title='<b>' + 'a [m/s²]' + '</b>',
        title='<b>' + component + ' - cluster envelopes' + '</b>',
        title_x=0.5,
        plot_bgcolor='white',
        xaxis=dict(
            showline=True,
            linewidth=2,
            linecolor='black',
            mirror=True,
            showgrid=True,
            gridcolor='rgb(211,211,211)',
            gridwidth=1,
            griddash='dot',
        ),
        yaxis=dict(
            showline=True,
            linewidth=2,
            linecolor='black',
            mirror=True,
            showgrid=True,
            gridcolor='rgb(211,211,211)',
            gridwidth=1,
            griddash='dot',
        ),
    )
    return fig

@anvil.server.callable
def getLinkagePlot():
    """
    Retrieve the linkage plot from the server globals.

    Returns:
        plotly.graph_objects.Figure: The linkage plot stored in serverGlobals.
    """
    return serverGlobals.plot_linkage

@anvil.server.callable
def addComparisonDataToOverviewPlot(overviewPlot, measurementFileName=None):
    """
    Add comparison data to the overview plot.

    Args:
        overviewPlot (plotly.graph_objects.Figure): The existing overview plot to which comparison data will be added.
        measurementFileName (str, optional): The name of the measurement file to retrieve data for. Defaults to None.

    Returns:
        tuple: A tuple containing the updated overview plot, a success flag, and the mean standard deviation of the comparison envelope.

    Functions called:
        - getComparisonDataEnvelope
        - getComparisonDataFileNames
        - getComparisonData
    """
    success = False
    envelope = getComparisonDataEnvelope()

    # cut of previous comparison data
    if len(overviewPlot.data) > 3:
        overviewPlot.data = overviewPlot.data[:3]
    # add the comparison envelope to the plot if available
    if envelope is not None:
        overviewPlot.add_trace(go.Scatter(x=envelope[0], y=envelope[1],name='measurement envelope', mode='lines', opacity=1, line=dict(color='black', width=2)))
        success = True
    # add the selected measurement data to the plot if a valid file name is provided
    if measurementFileName:
        if measurementFileName in getComparisonDataFileNames():
            x,y = getComparisonData(measurementFileName)
            overviewPlot.add_trace(go.Scatter(x=x, y=y, name='selected measurement', mode='lines', opacity=1, line=dict(color='blue', width=2)))

    return overviewPlot, success, serverGlobals.comparisonEnvelope_meanStdDev

@anvil.server.callable
def getComparisonData(fileName):
    """
    Retrieve the comparison data for a given file name.

    Args:
        fileName (str): The name of the file to retrieve comparison data for.

    Returns:
        tuple: A tuple containing the frequencies and amplitudes from the comparison data.

    Functions called:
        - None
    """
    for entry in serverGlobals.comparisonData:
        if entry['name'] == fileName:
            return entry['frequencies'], entry['amplitudes']

@anvil.server.callable
def getComparisonDataFileNames():
    """
    Retrieve the list of comparison data file names.

    Returns:
        list: A sorted list of unique comparison data file names.

    Functions called:
        - None
    """
    filenames = set()
    for entry in serverGlobals.comparisonData:
        filenames.add(entry['name'])

    return sorted(list(filenames))

@anvil.server.callable
def getComparisonDataEnvelope():
    """
    Retrieve the comparison data envelope from the server globals.

    Returns:
        tuple: A tuple containing the frequencies and amplitudes of the comparison data envelope.

    Functions called:
        - None
    """
    return serverGlobals.comparisonEnvelope

###########################################################################################################
# export
###########################################################################################################

@anvil.server.callable
def exportDB():
    """
    Export the database entries that contain 'data' to a pickle file.

    This function filters the global database (`serverGlobals.DB`) to include only entries that have the 'data' field.
    It then serializes these entries into a pickle file and returns it as an `anvil.BlobMedia` object.

    Returns:
        anvil.BlobMedia: A blob media object containing the serialized database entries with 'data' field.
    """
    tmpDB = []
    for entry in serverGlobals.DB:
        if 'data' in entry:
            tmpDB.append(entry)

    return anvil.BlobMedia("application/octet-stream", pickle.dumps(tmpDB), name="exportDB.pkls")

@anvil.server.callable
def exportClusterData(component,envelopeMethod, clusteringType, compare):
    """
    Export cluster data to an Excel file.

    This function generates and exports cluster data, including information, components, envelopes, and members,
    to an Excel file based on the specified component, envelope method, clustering type, and comparison flag.

    Args:
        component (str): The component to be analyzed and exported.
        envelopeMethod (str): The method used to generate the envelope.
        clusteringType (str): The type of clustering ('component', 'frequency', 'position').
        compare (bool): If True, include comparison data in the export.

    Returns:
        anvil.BlobMedia: A blob media object containing the exported Excel file.

    Functions called:
        - dataAnalysis.generateSuperEnvelope
    """
    # Determine the clusters and envelope color based on the clustering method
    if clusteringType == 'component':
        clusters = serverGlobals.clusters_components
    elif clusteringType == 'frequency':
        clusters = serverGlobals.clusters_frequencies
    elif clusteringType == 'position':
        clusters = serverGlobals.clusters_positions

    clustersWithComponent = []
    # Collect plot data for the specified component
    for cluster in clusters:
        for comp in cluster['components']:
            if component in comp:
                clustersWithComponent.append(cluster)
                break
    superEnvelope = dataAnalysis.generateSuperEnvelope(clustersWithComponent, envelopeMethod, component)

    # info sheet
    info = {'Group': [],'Number of selected Component in Cluster': [], 'Distance to SuperEnvelope': [], 'Distance Envelope of Comparison Files': []}
    for cluster in clustersWithComponent:
        info['Group'].append(cluster['name'])
        if len(cluster['amplitudes'].shape) < 2:
            nComponent = 1
        else:
            nComponent = cluster['amplitudes'].shape[1]
        info['Number of selected Component in Cluster'].append(nComponent)

        distance = pdist(np.array([cluster['envelope'], superEnvelope['envelope']]))
        info['Distance to SuperEnvelope'].append(distance[0])

        if serverGlobals.comparisonEnvelope:
            distance = pdist(np.array([cluster['envelope'], serverGlobals.comparisonEnvelope[1]]))
            info['Distance Envelope of Comparison Files'].append(distance[0])
        else:
            info['Distance Envelope of Comparison Files'].append('No Comparison Data')
    info = pd.DataFrame(info)

    # Components Sheet
    components = {'Group': [], 'Components in Group': []}
    for cluster in clustersWithComponent:
        components['Group'].append(cluster['name'])
        components['Components in Group'].append(pd.DataFrame(cluster['components']))
    components = pd.DataFrame(components)

    # Envelopes Sheet
    envelopes = {'Frequency [Hz]': superEnvelope['frequencies'], 'Super Envelope': superEnvelope['envelope']}
    if serverGlobals.comparisonEnvelope and compare:
        envelopes['Comparison Envelope'] = serverGlobals.comparisonEnvelope[1]
    for cluster in clustersWithComponent:
        envelopes[cluster['name']] = cluster['envelope']
    envelopes = pd.DataFrame(envelopes)

    # Members Sheet
    members = {'Group': [], 'Files in Group': []}
    for cluster in clustersWithComponent:
        members['Group'].append(cluster['name'])
        members['Files in Group'].append(pd.DataFrame(cluster['fileName']))
    members = pd.DataFrame(members)

    # write data to .xlsx file
    with pd.ExcelWriter('ClusterData.xlsx') as writer:
        # info sheet
        info.to_excel(writer, sheet_name='Info', index=False)
        # members sheet
        members.transpose().to_excel(writer, sheet_name='Members', index=True, header=False)
        for i in range(0,components.shape[0]):
            members['Files in Group'][i].to_excel(writer, sheet_name='Members', index=False, header=False, startrow=1,startcol=i+1)
        # envelopes sheet
        envelopes.transpose().to_excel(writer, sheet_name='Envelopes', header=False, index=True)
        # components sheet
        components.transpose().to_excel(writer, sheet_name='Components', index=True, header=False)
        for i in range(0,components.shape[0]):
            components['Components in Group'][i].to_excel(writer, sheet_name='Components', index=False, header=False, startrow=1,startcol=i+1)




    with open('ClusterData.xlsx', 'rb') as file:
        file_content = file.read()
    return anvil.BlobMedia("application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", file_content, name="ClusterData-" + clusteringType + ".xlsx")

@anvil.server.callable
def exportPlot(fig, format='png', name="plot"):
    """
    Export a Plotly figure to an image file.

    This function saves a given Plotly figure to an image file in the specified format and with the specified name.

    Args:
        fig (plotly.graph_objects.Figure): The Plotly figure to be exported.
        format (str, optional): The format of the output image file (e.g., 'png', 'pdf', 'svg'). Defaults to 'png'.
        name (str, optional): The base name of the output image file. Defaults to 'plot'.

    Returns:
        anvil.BlobMedia: A blob media object containing the exported image file.

    Functions called:
        - plotly.io.write_image
        - anvil.media.from_file
    """
    pio.write_image(fig, name + '.' + format, width=1920, height=1080)

    return anvil.media.from_file(name + '.' + format,"image/"+format)

@anvil.server.callable
def cleanupPlots():
    """
    Remove all image files with extensions 'png', 'pdf', and 'svg' from the current directory.

    This function uses the `os.system` command to execute shell commands that delete all files
    with the specified extensions in the current directory.

    Functions called:
        - os.system
    """
    os.system("rm *.png")
    os.system("rm *.pdf")
    os.system("rm *.svg")

