import anvil.server
import random
import re
import os
import numpy as np
from scipy.spatial.distance import pdist, cdist
import scipy.cluster.hierarchy as sch
import sklearn.cluster as skl
from sklearn.metrics import pairwise_distances
import plotly.graph_objects as go
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
def clusterComponents(frequencyRange):
    serverGlobals.clusters_components = assembleData('Bauteil')
    serverGlobals.clusters_components = adjustToFrequencyRange(serverGlobals.clusters_components, frequencyRange)
    return True

@anvil.server.callable
def clusterFrequencies(nClusters,frequencyRange, isHierarchical, distanceMetric):

    data = []
    indices = []
    for i in range(len(serverGlobals.selectedData)):
        if 'data' in serverGlobals.selectedData[i]:
            data.append(serverGlobals.selectedData[i]['data'][:,1])
            indices.append(i)
    data = np.array(data).T

    # adjust to frequency range
    dataInClusterFormat = [{}]
    dataInClusterFormat[0]['amplitudes'] = data
    dataInClusterFormat[0]['frequencies'] = serverGlobals.selectedData[0]['data'][:,0]

    dataInClusterFormat = adjustToFrequencyRange(dataInClusterFormat, frequencyRange)
    data = dataInClusterFormat[0]['amplitudes']

    nClustersAuto, serverGlobals.plot_linkage = calcNumberOfClusters(data, distanceMetric, nClusters)
    if not nClusters:
        nClusters = nClustersAuto


    return True


@anvil.server.callable
def clusterPositions(nClusters, frequencyRange, isHierarchical):

    cogs = []
    indices = []
    for i in range(len(serverGlobals.selectedData)):
        if 'cog' in serverGlobals.selectedData[i]:
            cogs.append(serverGlobals.selectedData[i]['cog'])
            indices.append(i)
    cogs = np.array(cogs)

    if indices:
        if isHierarchical:
            clustering = skl.AgglomerativeClustering(nClusters, metric='euclidean', linkage='single')
        else:
            clustering = skl.KMeans(nClusters, random_state=0, n_init=20, init='k-means++')
        clusterIndices = clustering.fit_predict(cogs)

        for i in range(len(indices)):
            serverGlobals.selectedData[indices[i]]['positionCluster'] = clusterIndices[i]

        serverGlobals.clusters_positions = assembleData('positionCluster')
        serverGlobals.clusters_positions = adjustToFrequencyRange(serverGlobals.clusters_positions, frequencyRange)

        return True
    else:
        return False

@anvil.server.callable
def generateEnvelopesForClusters(method):
    if serverGlobals.clusters_components:
        generateEnvelopes(serverGlobals.clusters_components, method)
    if serverGlobals.clusters_positions:
        generateEnvelopes(serverGlobals.clusters_positions, method)
    if serverGlobals.clusters_frequencies:
        generateEnvelopes(serverGlobals.clusters_frequencies, method)

def assembleData(key, db = None):
    """
    Assemble data into clusters based on a unique key.

    Args:
        key (str): The key to group data by.

    Returns:
        list: A list of clusters, each containing 'name', 'frequencies', and 'amplitudes'.
    """
    if db is None:
        db = serverGlobals.selectedData
    else:
        db = db

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
        cluster['cogs'] = []
        # Collect data for each cluster
        for entry in db:
            if key in entry:
                if (entry[key] == tempKey) and ('data' in entry):
                    cluster['data'].append(entry['data'])
                    cluster['components'].add(entry['Bauteil'])
                    if 'cog' in entry:
                        cluster['cogs'].append(entry['cog'])
        # Stack the data arrays for each cluster
        cluster['data'] = np.stack(cluster['data'])
        cluster['cogs'] = np.array(cluster['cogs'])

        # Check if the frequency data arrays match
        frequencies = cluster['data'][0, :, 0]
        for i in range(1, cluster['data'].shape[0]):
            if not np.array_equal(frequencies, cluster['data'][i, :, 0]):
                raise ValueError("frequency data arrays do not match")
        # Extract amplitudes for each cluster
        if cluster['data'].shape[0] == 1:
            amplitudes = cluster['data'][0, :, 1]
        else:
            amplitudes = np.column_stack([cluster['data'][i, :, 1] for i in range(cluster['data'].shape[0])])
        cluster['frequencies'] = frequencies
        cluster['amplitudes'] = amplitudes

        del(cluster['data'])

        clusters.append(cluster)

    return clusters

def adjustToFrequencyRange(clusters,frequencyRange):
    """
    Adjusts the frequency and amplitude data of clusters to a specified frequency range.

    Args:
        clusters (list): A list of clusters, each containing 'frequencies' and 'amplitudes'.
        frequencyRange (tuple): A tuple specifying the minimum and maximum frequency range.

    Returns:
        list: The function modifies the clusters in place and returns the adjusted clusters.

    """
    for cluster in clusters:
        idx = (cluster['frequencies'] >= frequencyRange[0]) & (cluster['frequencies'] <= frequencyRange[1])
        cluster['frequencies'] = cluster['frequencies'][idx]
        cluster['amplitudes'] = cluster['amplitudes'][idx]

    return clusters

@anvil.server.callable
def generateEnvelopes(clusters,method):
    """
    Generate envelopes for each cluster based on the specified method.

    Args:
        clusters (list): A list of clusters, each containing 'frequencies' and 'amplitudes'.
        method (str): The method to use for generating envelopes. Options include:
            - "Maximum": Maximum value across amplitudes.
            - "Minimum": Minimum value across amplitudes.
            - "Mean": Mean value across amplitudes.
            - "+1*std.dev.(68%)": Mean plus one standard deviation.
            - "+2*std.dev.(95%)": Mean plus two standard deviations.
            - "+3*std.dev.(99%)": Mean plus three standard deviations.
            - "99th-percentile (each freq.)": 99th percentile for each frequency.
            - "95th-percentile (each freq.)": 95th percentile for each frequency.
            - "75th-percentile (each freq.)": 75th percentile for each frequency.
            - "Median (each freq.)": Median for each frequency.
            - "99th-percentile (total)": 99th percentile across all data.
            - "95th-percentile (total)": 95th percentile across all data.
            - "75th-percentile (total)": 75th percentile across all data.
            - "Median (total)": Median across all data.

    Raises:
        ValueError: If the selected method is not implemented.
    """
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
    """
    Generate a super envelope for a set of clusters based on the specified method.

    Args:
        clusters (list): A list of clusters, each containing 'frequencies' and 'envelope'.
        method (str): The method to use for generating the super envelope.
        component (str): The name of the component for which the super envelope is generated.

    Returns:
        dict: A dictionary representing the super envelope, containing 'name', 'components', 'frequencies', and 'amplitudes'.
    """
    envelope = {}

    if len(clusters) > 1:
        envelope['name'] = component
        envelope['frequencies'] = clusters[0]['frequencies']
        envelope['amplitudes'] = []

        for cluster in clusters:
            envelope['amplitudes'].append(cluster['envelope'])
        envelope['amplitudes'] = np.column_stack(envelope['amplitudes'])

        envelope['meanStdDev'] = np.mean(np.std(envelope['amplitudes'], axis=1))
        generateEnvelopes([envelope], method)
    else:
        envelope = clusters[0]
        envelope['meanStdDev'] = 0
    return envelope

#comparison data
@anvil.server.callable
def assembleComparisonData(year, component, frequencyRange, envelopeMethod):
    """
    Assemble comparison data for a specific year and component.

    Args:
        year (int): The year to filter the data.
        component (str): The component to filter the data.
        envelopeMethod (str): The method to use for generating envelopes.
        frequencyRange (tuple): The frequency range to adjust the data.

    Returns:
        dict: The envelope of comparison data.
    """
    db = serverGlobals.selectedData
    comparisonData = []

    for entry in db:
        if (entry['Jahr'] == year) and (component in entry['Bauteil'] ) and ('data' in entry):
            comparisonData.append(entry)

    clusters = assembleData('Jahr', comparisonData)
    clusters = adjustToFrequencyRange(clusters, frequencyRange)
    generateEnvelopes(clusters, envelopeMethod)


    comparisonData = assembleData('Dateiname', comparisonData)

    for entry in comparisonData:        #todo: revise, here due to strange bug with K03/2015/Blinker_hi
        if len(entry['amplitudes'].shape) > 1:
            entry['amplitudes'] = entry['amplitudes'][:, 0]

    comparisonData = adjustToFrequencyRange(comparisonData, frequencyRange)

    serverGlobals.comparisonData = comparisonData
    if len(clusters)<1:
        serverGlobals.comparisonEnvelope = None
    else:
        serverGlobals.comparisonEnvelope = [clusters[0]['frequencies'], clusters[0]['envelope']]
        serverGlobals.comparisonEnvelope_meanStdDev = np.mean(np.std(clusters[0]['amplitudes'], axis=1))

@anvil.server.callable
def getErrors(predictionEnvelope):

    errorVec = np.vstack((serverGlobals.comparisonEnvelope[1], predictionEnvelope[1]))
    magError = serverGlobals.frequencyResolution * np.sum(np.abs(errorVec[1,:] - errorVec[0,:])) / 1000
    anglErr =  1 - pdist(errorVec, 'cosine')[0]

    return magError, anglErr

# clustering functions
def kmeans_clustering(data, nClusters, distanceMetric='correlation'):
    """
    Perform KMeans clustering with kmeans++ initialization and specified distance metric.

    distanceMetric options: ‘braycurtis’, ‘canberra’, ‘chebyshev’, ‘cityblock’, ‘correlation’, ‘cosine’, ‘dice’, ‘euclidean’, ‘hamming’, ‘jaccard’, ‘jensenshannon’, ‘kulczynski1’, ‘mahalanobis’, ‘matching’, ‘minkowski’, ‘rogerstanimoto’, ‘russellrao’, ‘seuclidean’, ‘sokalmichener’, ‘sokalsneath’, ‘sqeuclidean’, ‘yule’
    data: m x n numpy array, m measurements, n dimensions
    """

    # Transpose the data to shape (m, n) for KMeans
    data = data.T

    # Initialize KMeans with kmeans++ initialization
    kmeans = skl.KMeans(n_clusters=nClusters, init='k-means++', random_state=0, n_init=20)

    # Fit the model
    kmeans.fit(data)

    # Compute the distance matrix using the specified distance metric
    distance_matrix = cdist(data, kmeans.cluster_centers_, metric=distanceMetric)

    # Assign labels based on the minimum distance
    labels = np.argmin(distance_matrix, axis=1)

    return labels, kmeans

def hierarchical_clustering(data, nClusters, distanceMetric='seuclidean'):
    """
    Perform hierarchical clustering with specified distance metric.

    Args:
        data (np.ndarray): The data to cluster, shape (n, m) where n is the number of dimensions and m is the number of measurements.
        n_clusters (int): The number of clusters.
        distance_metric (str): The distance metric to use ('euclidean', 'cityblock', 'cosine', etc.).

    distanceMetric options: ‘cityblock’, ‘cosine’, ‘euclidean’, ‘l1’, ‘l2’, ‘manhattan’, ‘braycurtis’, ‘canberra’, ‘chebyshev’, ‘correlation’, ‘dice’, ‘hamming’, ‘jaccard’, ‘kulsinski’, ‘mahalanobis’, ‘minkowski’, ‘rogerstanimoto’, ‘russellrao’, ‘seuclidean’, ‘sokalmichener’, ‘sokalsneath’, ‘sqeuclidean’, ‘yule’

    Returns:
        np.ndarray: The cluster labels.
    """
    # Transpose the data to shape (m, n) for distance computation
    data = data.T

    # Compute the distance matrix using the specified distance metric
    distance_matrix = pairwise_distances(data, metric=distanceMetric)

    if 'euclidean' in distanceMetric:
        linkage = 'ward'
    else:
        linkage = 'average'
    # Perform Agglomerative Clustering with the precomputed distance matrix
    clustering = skl.AgglomerativeClustering(n_clusters=nClusters, metric='precomputed', linkage=linkage)
    labels = clustering.fit_predict(distance_matrix)

    return labels, clustering

def calcNumberOfClusters(data,distanceMetric,manualNClusters=False, mean_window = 5, sensitivity=False):

    # Compute the distance matrix using the specified distance metric
    distance_matrix = pdist(data.T, metric=distanceMetric)
    if 'euclidean' in distanceMetric:
        linkage = 'ward'
    else:
        linkage = 'average'

    linkVector = sch.linkage(distance_matrix, method=linkage)
    linkVector = linkVector[:, 2]

    # get sensitivity (from original matlab tool)
    sensitivityDict = dict()
    sensitivityDict['seuclidean'] = 0.3
    sensitivityDict['euclidean'] = 40
    sensitivityDict['sqeuclidean'] = 10e4
    sensitivityDict['cityblock'] = 50
    sensitivityDict['minkowski'] = 4
    sensitivityDict['chebychev'] = 1
    sensitivityDict['cosine'] = 4e-4
    sensitivityDict['correlation'] = 10e-3

    if not sensitivity:
        sensitivity = sensitivityDict[distanceMetric]

    # Translated matlab code
    nSClstrs = len(linkVector) - np.arange(1, len(linkVector) + 1)

    # Filtering linkVector with mean window
    link_mean = np.zeros(len(linkVector))
    for i in range(mean_window + 1, len(link_mean) - mean_window - 1):
        link_mean[i] = np.mean(linkVector[i - mean_window:i + mean_window])

    # Derive mean linkage
    mean_link_p = np.concatenate([
        np.zeros(mean_window + 1),
        np.diff(link_mean[mean_window + 1: -mean_window - 1]),
        np.zeros(mean_window + 1)
    ])

    # Find optimum cluster number based on derivative
    Clusternumber_idx = np.argmax(mean_link_p > sensitivity)
    Clusternumber = nSClstrs[Clusternumber_idx]


    fig = go.Figure()
    fig.add_trace(go.Scatter(x=nSClstrs, y=linkVector, mode='lines', name='linkage'))
    fig.add_trace(go.Scatter(x=[Clusternumber,Clusternumber], y=[0,np.max(linkVector)], mode='lines', line=dict(color='red', width=2), name='automatic cluster number'))
    if manualNClusters:
        fig.add_trace(go.Scatter(x=[manualNClusters, manualNClusters], y=[0.1, np.max(linkVector)], mode='lines', line=dict(color='green', width=2), name='manual cluster number'))

    fig.update_layout(
        showlegend=True,
        xaxis_title='<b>' + 'number of clusters' + '</b>',
        yaxis_title='<b>' + 'error in clusters' + '</b>',
        title='<b> Automated number of clusters selections: '+ str(Clusternumber)+ '</b>',
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
            autorangeoptions_clipmin=0,

        ),
    )
    return Clusternumber, fig