
names = [cluster['name'] for cluster in clusters]

def generate_unique_prefixes(clusters):
    unique_prefixes = set()

    for cluster in clusters:
        name = cluster['name']
        parts = name.split('_')

        for i in range(1, len(parts) + 1):
            prefix = '_'.join(parts[:i])
            unique_prefixes.add(prefix)

    return list(unique_prefixes)



specific_string = 'A_B'
unique_entries = list(set([component for component in components if specific_string in component]))
