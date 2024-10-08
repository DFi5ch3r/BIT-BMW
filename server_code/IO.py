import anvil.server
import random
import re
import os
import numpy as np
import pandas as pd
import chardet
from . import serverGlobals

# This is a server module. It runs on the Anvil server,
# rather than in the user's browser.
#
# To allow anvil.server.call() to call functions here, we mark
# them with @anvil.server.callable.
# Here is an example - you can replace it with your own:
#
# @anvil.server.callable
# def say_hello(name):
#   print("Hello, " + name + "!")
#   return 42

@anvil.server.callable
def test():
  print(serverGlobals.selectedData)
  print('\n---------------------------------------------\n')
  #print(serverGlobals.CoGfiles)
  #print('\n---------------------------------------------\n')
  #print(serverGlobals.wheelbase)

@anvil.server.callable
def create_databaseTEST(read_path):
  """
    Creates a test database with randomly generated entries and updates the global database.

    Args:
        read_path (str): The path to the directory containing the files to be processed.

    This function performs the following steps:
    1. Initializes a test database with predefined entries.
    2. Defines lists of possible values for various fields.
    3. Generates additional random entries and appends them to the test database.
    4. Updates the global database variable with the test database.
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
  baureihen = ['K12345', 'M67890', 'A11111', 'R22222']
  bauteile = ['Bauteil1', 'Bauteil2', 'Bauteil3', 'Bauteil4']
  richtungen = ['+X', '-Y', '+Z', '-X']
  lasten = ['GL', 'VL', 'GS']
  baustufen = ['KEX', 'BS1', 'FB', 'VS1']
  years = ['2023', '2022', '2021', '2020', '2019', '2018', '2017', '2016', '2015', '2014']

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
  #return testDB
  serverGlobals.DB = testDB
  #print(serverGlobals.DB)

@anvil.server.callable
def create_database(read_path):
    """
    Creates a database by processing files in the specified directory and extracting relevant information.

    Args:
        read_path (str): The path to the directory containing the files to be processed.

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


    database = sorted(database, key=lambda x: x['Baureihe'])
    #return database
    serverGlobals.DB = database

@anvil.server.callable
def filter_database(key, values, sourceFullDB = True, secondKey = False):
    """
    Filters the global database based on the specified key and values.

    Args:
        key (str): The key to filter the database entries by.
        values (list): A list of values to filter the entries.
        sourceFullDB (bool, optional): If True, use the full database from serverGlobals.DB.
                                       If False, use the selected data from serverGlobals.selectedData.
                                       Defaults to True.
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

    # Update the global database variable with the filtered database
    serverGlobals.selectedData = filtered_database

@anvil.server.callable
def get_baureihe_and_years():
    """
    Creates a list of dictionaries, each containing the name of the Baureihe and the respective years as a list.

    Args:
        database (list): A list of dictionaries, each representing a file with extracted information.

    Returns:
        list: A list of dictionaries, each containing the name of the Baureihe and the respective years as a list.
    """
    database = serverGlobals.DB
    baureihe_to_years = {}

    for entry in database:
        baureihe = entry['Baureihe']
        year = entry['Jahr']
        if baureihe != 'Not found' and year != 'Not found':
            if baureihe not in baureihe_to_years:
                baureihe_to_years[baureihe] = set()
            baureihe_to_years[baureihe].add(year)

    baureihe_years_list = [
      {
          'Baureihe': baureihe,
          'Years': [{'year': year, 'baureihe': baureihe} for year in years]
      }
      for baureihe, years in baureihe_to_years.items()
    ]
    return baureihe_years_list

@anvil.server.callable
def get_unique_values(key, sourceSelectedData=False):
    """
    Retrieves unique values for a specified key from the database.

    Args:
        key (str): The key for which unique values are to be found.
        sourceSelectedData (bool, optional): If True, use the selected data from serverGlobals.selectedData.
                                             If False, use the full database from serverGlobals.DB. Defaults to False.

    Returns:
        list: A sorted list of unique values for the specified key.
    """
    unique_values = set()

    if sourceSelectedData:
      DB = serverGlobals.selectedData
    else:
      DB = serverGlobals.DB
  
    for entry in DB:
        if key in entry:
            unique_values.add(entry[key])

    return sorted(list(unique_values))

@anvil.server.callable
def loadCoGdata(rootPath):
    """
    Loads and processes center of gravity (CoG) data from CSV files located in the specified root path.

    Args:
        rootPath (str): The root directory path containing the 'Schwerpunktdaten' folder with CSV files.

    The processed CoG data is stored in the `serverGlobals.CoGfiles` global variable.
    The wheelbase information is stored in the `serverGlobals.wheelbase` global variable.
    """

    # Initialize an empty list to store CoG file data
    CoGfiles = []

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
        CoGfiles.append({
            'Baureihe': baureihe,
            'parts': parts,
            'CoGs': cogs
        })

    # Store the processed CoG data and wheelbase information in global variables
    serverGlobals.CoGfiles = CoGfiles
    serverGlobals.wheelbase = wheelbase

@anvil.server.callable
def readData(selectedData = True):

    if selectedData:
        db = serverGlobals.selectedData
    else:
        db = serverGlobals.DB

    total_entries = len(db)
    progress_interval = max(1, total_entries // 10)  # Print progress every 10% or at least once

    for i, entry in enumerate(db):
        filePath = os.path.join(entry['Pfad'], entry['Unterpfad'], entry['Dateiname'])
        # filePath = filePath.replace(' ', '\\ ')

        if (not "Kopie" in filePath):
            data = np.loadtxt(filePath)
            if len(data) == 800:
                entry['data'] = data
            else:
                print(f"Skipped {entry['Dateiname']}, since Data length is {len(data)}")
        else:
            print(f"Skipped {entry['Dateiname']}, since it is a copy")

        # Print progress
        if (i + 1) % progress_interval == 0 or (i + 1) == total_entries:
            print(f"Progress: {i + 1}/{total_entries} entries processed")

def detect_encoding(file_path):
    """
    Detects the encoding of a given file using the chardet library.

    Args:
        file_path (str): The path to the file whose encoding needs to be detected.

    Returns:
        str: The detected encoding of the file.
    """
    with open(file_path, 'rb') as f:
        result = chardet.detect(f.read())
    return result['encoding']