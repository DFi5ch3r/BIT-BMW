import anvil.server
import random
import os
import re
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
def create_databaseTEST(read_path):
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
  return testDB

@anvil.server.callable
def create_database(read_path):
    """
     Creates a database from the files in the specified directory.

     Args:
         read_path (str): The path to the directory containing the files.

     Returns:
         list: A list of dictionaries, each representing a file with extracted information.
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

    return database
@anvil.server.callable
def get_baureihe_and_years(database):
    """
    Creates a list of dictionaries, each containing the name of the Baureihe and the respective years as a list.

    Args:
        database (list): A list of dictionaries, each representing a file with extracted information.

    Returns:
        list: A list of dictionaries, each containing the name of the Baureihe and the respective years as a list.
    """
    baureihe_to_years = {}

    for entry in database:
        baureihe = entry['Baureihe']
        year = entry['Jahr']
        if baureihe != 'Not found' and year != 'Not found':
            if baureihe not in baureihe_to_years:
                baureihe_to_years[baureihe] = set()
            baureihe_to_years[baureihe].add(year)

    #baureihe_years_list = [{'Baureihe': baureihe, 'Years': list(years)} for baureihe, years in baureihe_to_years.items()]

    baureihe_years_list = [
      {
          'Baureihe': baureihe,
          'Years': [{'year': year, 'baureihe': baureihe} for year in years]
      }
      for baureihe, years in baureihe_to_years.items()
    ]
    return baureihe_years_list

@anvil.server.callable
def get_unique_values(database, key):
    """
    Returns the unique values for a specified key in the database.

    Args:
        database (list): A list of dictionaries, each representing a file with extracted information.
        key (str): The key for which unique values are to be found.

    Returns:
        list: A list of unique values for the specified key.
    """
    unique_values = set()

    for entry in database:
        if key in entry:
            unique_values.add(entry[key])

    return sorted(list(unique_values))