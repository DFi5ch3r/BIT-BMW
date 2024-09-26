import os
import numpy as np
import pandas as pd
import chardet

def detect_encoding(file_path):
    with open(file_path, 'rb') as f:
        result = chardet.detect(f.read())
    return result['encoding']

# Load and process CoG-data
path = '/home/dfischer/12-Projects/09-BMW-BIT/01-originalMatlabTool/BMW_BIT_TUB/BMW_Phase2_txtonly_BackUp/'

CoGfiles = []

path = path + '/Schwerpunktdaten'
cog_files = []
for root, dirs, files in os.walk(path):
    for file in files:
        if file.endswith('.csv'):
            cog_files.append(root + '/' + file)

cog_files = [file for file in cog_files if not os.path.isdir(file)]

for file in cog_files:
    encoding = detect_encoding(file)

    # Read file Radstände
    if os.path.basename(file) == 'Radstände.csv':
        wheelbase = pd.read_csv(file, encoding='latin1', delimiter=';').values.tolist()
        if wheelbase[0][0] == 'Baureihe':  # remove first line from list
            wheelbase = wheelbase[1:]
        continue

    baureihe = os.path.splitext(os.path.basename(file))[0]
    try:
        tmp_cogdata_raw = pd.read_csv(file, encoding=encoding, delimiter=';')
    except pd.errors.ParserError as e:
        print(f"Error parsing {file}: {e}")
        continue

    raw_parts = tmp_cogdata_raw.iloc[:, 0].astype(str).values
    raw_cogs_tmp = tmp_cogdata_raw.iloc[:, 1:].values
    raw_cogs = []
    for i in range(raw_cogs_tmp.shape[0]):
        raw_cogs.append(raw_cogs_tmp[i][1:])
    raw_cogs = np.array(raw_cogs)

    parts, comps_idx = np.unique(raw_parts, return_inverse=True)

    # Mittel der CoGs für Bauteile mit mehreren Komponenten
    cogs = np.zeros((len(parts), 3))
    for part_index in range(len(parts)):
        part_cog_mean = np.mean(raw_cogs[comps_idx == part_index, :], axis=0)
        cogs[part_index, :] = part_cog_mean

    # CoG des Schwingenlagers für Transformation bestimmen
    cog_swila = cogs[np.char.find(list(parts), "SwiLa Links und Recht") >= 0, :]
    # Transformation ins Schwingen KOS
    cogs = cogs - cog_swila

    CoGfiles.append({
        'Baureihe': baureihe,
        'parts': parts,
        'CoGs': cogs
    })

    # serverGlobals.CoGfiles = CoGfiles
    # serverGlobals.wheelbase = wheelbase