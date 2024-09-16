import anvil.server
import random
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
# NAK

@anvil.server.callable
def create_database(read_path):
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
def addActiveFlags(database):
    for entry in database:
        entry['Active'] = False
    return database
  
@anvil.server.callable
def set_active_flag(database, baureihe, years):
    for entry in database:
        if entry['Baureihe'] == baureihe and entry['Jahr'] in years:
            entry['Active'] = True
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