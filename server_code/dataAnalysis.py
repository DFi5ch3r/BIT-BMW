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
def clusterComponents():
    serverGlobals.clusters_components = assembleData('Bauteil')

@anvil.server.callable
def clusterFrequencies():
    pass

@anvil.server.callable
def clusterPositions():
    pass

@anvil.server.callable
def generateEnvelopesForClusters(method):
    if serverGlobals.clusters_components:
        generateEnvelopes(serverGlobals.clusters_components, method)
    if serverGlobals.clusters_positions:
        generateEnvelopes(serverGlobals.clusters_positions, method)
    if serverGlobals.clusters_frequencies:
        generateEnvelopes(serverGlobals.clusters_frequencies, method)

def assembleData(key):
    """
    Assemble data into clusters based on a unique key.

    Args:
        key (str): The key to group data by.

    Returns:
        list: A list of clusters, each containing 'name', 'frequencies', and 'amplitudes'.
    """

    db = serverGlobals.selectedData
    unique_keys = set()

    # Iterate through each entry in the database to find unique keys
    for entry in db:
        if key in entry:
            unique_keys.add(entry[key])

    unique_keys = sorted(list(unique_keys))

    # Create clusters based on unique keys
    clusters = []
    for tempKey in unique_keys:
        cluster =  {}
        cluster['name'] = tempKey
        cluster['components'] = set()
        cluster['data'] = []
        # Collect data for each cluster
        for entry in db:
            if (entry[key] == tempKey) and ('data' in entry):
                cluster['data'].append(entry['data'])
                cluster['components'].add(entry['Bauteil'])
        # Stack the data arrays for each cluster
        cluster['data'] = np.stack(cluster['data'])

        # Check if the frequency data arrays match
        frequencies = cluster['data'][0, :, 0]
        for i in range(1, cluster['data'].shape[0]):
            if not np.array_equal(frequencies, cluster['data'][i, :, 0]):
                raise ValueError("frequency data arrays do not match")
        # Extract amplitudes for each cluster
        amplitudes = np.column_stack([cluster['data'][i, :, 1] for i in range(cluster['data'].shape[0])])
        cluster['frequencies'] = frequencies
        cluster['amplitudes'] = amplitudes

        del(cluster['data'])

        clusters.append(cluster)

    return clusters

@anvil.server.callable
def generateEnvelopes(clusters,method):
    for cluster in clusters:
        if cluster['amplitudes'].shape[1] < 2:
            cluster['envelope'] = cluster['amplitudes']
        else:
            if method == "Maximum":
                cluster['envelope'] = np.max(cluster['amplitudes'], axis=1)
            elif method == "Minimum":
                cluster['envelope'] = np.min(cluster['amplitudes'], axis=1)
            elif method == "Mean":
                cluster['envelope'] = np.mean(cluster['amplitudes'], axis=1)
            # normal distribution based methods
            elif method == "+1*std.dev.(68%)":
                cluster['envelope'] = np.mean(cluster['amplitudes'], axis=1) + np.std(cluster['amplitudes'], axis=1)
            elif method == "+2*std.dev.(95%)":
                cluster['envelope'] = np.mean(cluster['amplitudes'], axis=1) + 2 * np.std(cluster['amplitudes'], axis=1)
            elif method == "+3*std.dev.(99%)":
                cluster['envelope'] = np.mean(cluster['amplitudes'], axis=1) + 3 * np.std(cluster['amplitudes'], axis=1)

            # percentiles (each freq.)
            elif method in ["99th-percentile (each freq.)", "95th-percentile (each freq.)", "75th-percentile (each freq.)",
                            "Median (each freq.)"]:
                p = \
                {"99th-percentile (each freq.)": 99, "95th-percentile (each freq.)": 95, "75th-percentile (each freq.)": 75,
                 "Median (each freq.)": 50}[method]
                cluster['envelope']  = np.percentile(cluster['amplitudes'], p, axis=1)

            # percentiles (total)
            elif method in ["99th-percentile (total)", "95th-percentile (total)", "75th-percentile (total)",
                            "Median (total)"]:
                N_data = cluster['amplitudes'].shape[1]
                norm_vec = np.linalg.norm(cluster['amplitudes'], axis=0)
                idx_vec = np.argsort(norm_vec)
                sEnvs_srtd = cluster['amplitudes'][:,idx_vec]
                p = {"99th-percentile (total)": 0.99, "95th-percentile (total)": 0.95, "75th-percentile (total)": 0.75,
                     "Median (total)": 0.50}[method]
                idx_prctg = int(np.floor(N_data * p + 1))
                cluster['envelope']  = np.max(sEnvs_srtd[:,:idx_prctg], axis=1)

            else:
                raise ValueError("Selected Method for generation of envelopes not implemented yet!")

@anvil.server.callable
def generateSuperEnvelope(clusters, method, component):
    envelope = {}
    envelope['name'] = component
    envelope['components'] = set()
    envelope['frequencies'] = clusters[0]['frequencies']
    envelope['amplitudes'] = []

    for cluster in clusters:
        envelope['amplitudes'].append(cluster['envelope'])
    envelope['amplitudes'] = np.column_stack(envelope['amplitudes'])

    generateEnvelopes([envelope], method)

    return envelope