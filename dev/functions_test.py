def display_unique_attributes(database,):
    unique_values = {
        'ID': set(),
        'Dateiname': set(),
        'Pfad': set(),
        'Unterpfad': set(),
        'Jahr': set(),
        'Baureihe': set(),
        'Nummer': set(),
        'Bauteil': set(),
        'Baustufe': set(),
        'Richtung': set(),
        'Last': set(),
        'Gang': set()
    }

    for entry in database:
        for key in unique_values:
            unique_values[key].add(entry[key])

    for key, values in unique_values.items():
        print(f"{key}: {values}")