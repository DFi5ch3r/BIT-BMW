import os
import re
import numpy as np

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