import anvil.server

import numpy as np
from scipy.spatial.distance import pdist, cdist
import scipy.cluster.hierarchy as sch
import sklearn.cluster as skl
from sklearn.metrics import pairwise_distances
import plotly.graph_objects as go

from . import serverGlobals

# This is a server module. It runs on the Anvil server,
# rather than in the user's browser.
#
# To allow anvil.server.call() to call functions here, we mark
# them with @anvil.server.callable.

@anvil.server.callable
def clusterComponents(frequencyRange):
    """
    Cluster components based on the provided frequency range.

    Args:
        frequencyRange (tuple): A tuple specifying the minimum and maximum frequency range.

    Returns:
        bool: True if clustering is successful.

    Functions called:
        - assembleData
        - adjustToFrequencyRange
    """
    serverGlobals.clusters_components = assembleData('Bauteil')
    serverGlobals.clusters_components = adjustToFrequencyRange(serverGlobals.clusters_components, frequencyRange)
    return True

@anvil.server.callable
def clusterFrequencies(nClusters,frequencyRange, isHierarchical, distanceMetric):
    """
    Cluster frequencies based on the provided parameters.

    Args:
        nClusters (int): The number of clusters.
        frequencyRange (tuple): A tuple specifying the minimum and maximum frequency range.
        isHierarchical (bool): If True, use hierarchical clustering; otherwise, use KMeans clustering.
        distanceMetric (str): The distance metric to use for clustering.

    Returns:
        bool: True if clustering is successful.

    Functions called:
        - assembleData
        - adjustToFrequencyRange
        - calcNumberOfClusters
        - hierarchical_clustering
        - kmeans_clustering
    """
    # assemble data for clustering (amplitudes)
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

    # determine the number of clusters automatically if not provided
    nClustersAuto, serverGlobals.plot_linkage = calcNumberOfClusters(data, distanceMetric, nClusters)
    if not nClusters:
        nClusters = nClustersAuto

    # perform clustering
    if isHierarchical:
        clusterIndices = hierarchical_clustering(data, nClusters, distanceMetric)
    else:
        clusterIndices = kmeans_clustering(data, nClusters, distanceMetric)

    # assign cluster indices to selected data
    for i in range(len(indices)):
        serverGlobals.selectedData[indices[i]]['frequencyCluster'] = clusterIndices[i]

    # assemble and adjust clusters to frequency range
    serverGlobals.clusters_frequencies = assembleData('frequencyCluster')
    serverGlobals.clusters_frequencies = adjustToFrequencyRange(serverGlobals.clusters_frequencies, frequencyRange)
    return True

@anvil.server.callable
def clusterPositions(nClusters, frequencyRange, isHierarchical):
    """
    Cluster positions based on the provided parameters.

    Args:
        nClusters (int): the number of clusters.
        frequencyRange (tuple): a tuple specifying the minimum and maximum frequency range.
        isHierarchical (bool): if True, use hierarchical clustering; otherwise, use KMeans clustering.

    Returns:
        bool: True if clustering is successful.

    Functions called:
        - assembleData
        - adjustToFrequencyRange
    """
    # collect center of gravity (cog) data for clustering
    cogs = []
    indices = []
    for i in range(len(serverGlobals.selectedData)):
        if 'cog' in serverGlobals.selectedData[i]:
            cogs.append(serverGlobals.selectedData[i]['cog'])
            indices.append(i)
    cogs = np.array(cogs)

    if indices:
        # perform hierarchical clustering if specified
        if isHierarchical:
            clustering = skl.AgglomerativeClustering(nClusters, metric='euclidean', linkage='single')
        # perform KMeans clustering otherwise
        else:
            clustering = skl.KMeans(nClusters, random_state=0, n_init=20, init='k-means++')
        clusterIndices = clustering.fit_predict(cogs)

        # assign cluster indices to selected data
        for i in range(len(indices)):
            serverGlobals.selectedData[indices[i]]['positionCluster'] = clusterIndices[i]

        # assemble and adjust clusters to frequency range
        serverGlobals.clusters_positions = assembleData('positionCluster')
        serverGlobals.clusters_positions = adjustToFrequencyRange(serverGlobals.clusters_positions, frequencyRange)

        return True
    else:
        return False

@anvil.server.callable
def generateEnvelopesForClusters(method):
    """
    Generate envelopes for each cluster based on the specified method.

    Args:
        method (str): the method to use for generating envelopes.

    Functions called:
        - generateEnvelopes
    """
    if serverGlobals.clusters_components:
        generateEnvelopes(serverGlobals.clusters_components, method)
    if serverGlobals.clusters_positions:
        generateEnvelopes(serverGlobals.clusters_positions, method)
    if serverGlobals.clusters_frequencies:
        generateEnvelopes(serverGlobals.clusters_frequencies, method)

def assembleData(key, db = None):
    """
    Assemble data into clusters based on a specified key.

    Args:
        key (str): the key to cluster the data by.
        db (list, optional): the database to use. Defaults to None, which uses serverGlobals.selectedData.

    Returns:
        list: a list of clusters, each containing 'name', 'components', 'frequencies', 'amplitudes', and 'cogs'.

    Functions called:
        - None
    """

    if db is None:
        db = serverGlobals.selectedData
    else:
        db = db

    unique_keys = set()

    # iterate through each entry in the database to find unique keys
    for entry in db:
        if key in entry:
            unique_keys.add(entry[key])

    unique_keys = sorted(list(unique_keys))

    # create clusters based on unique keys
    clusters = []
    for tempKey in unique_keys:
        cluster =  {}
        cluster['name'] = tempKey
        cluster['components'] = set()
        cluster['fileName'] = set()
        cluster['data'] = []
        cluster['cogs'] = []
        # collect data for each cluster
        for entry in db:
            if key in entry:
                if (entry[key] == tempKey) and ('data' in entry):
                    cluster['data'].append(entry['data'])
                    cluster['components'].add(entry['Bauteil'])
                    cluster['fileName'].add(entry['Dateiname'])
                    if 'cog' in entry:
                        cluster['cogs'].append(entry['cog'])
        # stack the data arrays for each cluster
        cluster['data'] = np.stack(cluster['data'])
        cluster['cogs'] = np.array(cluster['cogs'])

        # check if the frequency data arrays match
        frequencies = cluster['data'][0, :, 0]
        for i in range(1, cluster['data'].shape[0]):
            if not np.array_equal(frequencies, cluster['data'][i, :, 0]):
                raise ValueError("frequency data arrays do not match")
        # extract amplitudes for each cluster
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
    Adjust clusters to the specified frequency range.

    Args:
        clusters (list): a list of clusters, each containing 'frequencies' and 'amplitudes'.
        frequencyRange (tuple): a tuple specifying the minimum and maximum frequency range.

    Returns:
        list: the adjusted list of clusters.

    Functions called:
        - None
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

    Functions called:
        - None

    Raises:
        ValueError: If the selected method is not implemented.

    """
    for cluster in clusters:
        # if amplitudes have less than 2 dimensions, use them directly as envelope
        if len(cluster['amplitudes'].shape) < 2:
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
    Generate a super envelope for the given clusters based on the specified method.

    Args:
        clusters (list): A list of clusters, each containing 'frequencies' and 'envelope'.
        method (str): The method to use for generating the super envelope.
        component (str): The name of the component for which the super envelope is generated.

    Returns:
        dict: The generated super envelope containing 'name', 'frequencies', 'amplitudes', 'envelope', and 'meanStdDev'.

    Functions called:
        - generateEnvelopes
    """
    envelope = {}

    if len(clusters) > 1:
        envelope['name'] = component
        envelope['frequencies'] = clusters[0]['frequencies']
        envelope['amplitudes'] = []

        # Collect envelopes from each cluster
        for cluster in clusters:
            envelope['amplitudes'].append(cluster['envelope'])
        envelope['amplitudes'] = np.column_stack(envelope['amplitudes'])

        # Calculate the mean standard deviation of the amplitudes
        envelope['meanStdDev'] = np.mean(np.std(envelope['amplitudes'], axis=1))
        generateEnvelopes([envelope], method)
    else:
        envelope = clusters[0]
        envelope['meanStdDev'] = 0

    return envelope

# comparison data functions
#----------------------------------------------------------------------------------------------------------------------#

@anvil.server.callable
def assembleComparisonData(year, component, frequencyRange, envelopeMethod):
    """
    Assemble comparison data for a given year and component, adjust it to the specified frequency range, and generate
    envelopes.

    Args:
        year (int): The year to filter the data by.
        component (str): The component to filter the data by.
        frequencyRange (tuple): A tuple specifying the minimum and maximum frequency range.
        envelopeMethod (str): The method to use for generating envelopes.

    Functions called:
        - assembleData
        - adjustToFrequencyRange
        - generateEnvelopes

    Returns:
        None
    """
    db = serverGlobals.selectedData
    comparisonData = []

    # filter the database for entries matching the specified year and component
    for entry in db:
        if (entry['Jahr'] == year) and (component in entry['Bauteil'] ) and ('data' in entry):
            comparisonData.append(entry)

    # assemble and adjust clusters to the specified frequency range
    clusters = assembleData('Jahr', comparisonData)
    clusters = adjustToFrequencyRange(clusters, frequencyRange)
    generateEnvelopes(clusters, envelopeMethod)

    # assemble comparison data by filename
    comparisonData = assembleData('Dateiname', comparisonData)

    # ensure amplitudes have the correct shape
    for entry in comparisonData:        #todo: revise, here due to strange bug with K03/2015/Blinker_hi
        if len(entry['amplitudes'].shape) > 1:
            entry['amplitudes'] = entry['amplitudes'][:, 0]

    # adjust comparison data to the specified frequency range
    comparisonData = adjustToFrequencyRange(comparisonData, frequencyRange)

    # store the comparison data and envelope in serverGlobals
    serverGlobals.comparisonData = comparisonData
    if len(clusters)<1:
        serverGlobals.comparisonEnvelope = None
    else:
        serverGlobals.comparisonEnvelope = [clusters[0]['frequencies'], clusters[0]['envelope']]
        serverGlobals.comparisonEnvelope_meanStdDev = np.mean(np.std(clusters[0]['amplitudes'], axis=1))

@anvil.server.callable
def getErrors(predictionEnvelope):
    """
    Calculate the magnitude and angular errors between the comparison envelope and the prediction envelope.

    Args:
        predictionEnvelope (list): A list containing the predicted envelope data with frequencies and amplitudes.

    Functions called:
        - None

    Returns:
        tuple: A tuple containing the magnitude error and angular error.
    """
    errorVec = np.vstack((serverGlobals.comparisonEnvelope[1], predictionEnvelope[1]))
    magError = serverGlobals.frequencyResolution * np.sum(np.abs(errorVec[1,:] - errorVec[0,:])) / 1000
    anglErr =  1 - pdist(errorVec, 'cosine')[0]

    return magError, anglErr

# clustering functions
#----------------------------------------------------------------------------------------------------------------------#

def kmeans_clustering(data, nClusters, distanceMetric='correlation'):
    """
    Perform KMeans clustering on the given data using the specified distance metric.

    Args:
        data (np.ndarray): The data to cluster, shape (m,n) where n is the number of dimensions and m is the number of
                           measurements, n dimensions.
        nClusters (int): The number of clusters.
        distanceMetric (str): The distance metric to use for clustering. Default is 'correlation'.
                              ‘braycurtis’, ‘canberra’, ‘chebyshev’, ‘cityblock’, ‘correlation’, ‘cosine’, ‘dice’,
                              ‘euclidean’, ‘hamming’, ‘jaccard’, ‘jensenshannon’, ‘kulczynski1’, ‘mahalanobis’,
                              ‘matching’, ‘minkowski’, ‘rogerstanimoto’, ‘russellrao’, ‘seuclidean’, ‘sokalmichener’,
                              ‘sokalsneath’, ‘sqeuclidean’, ‘yule’

    Returns:
        np.ndarray: The cluster labels.

    Functions called:
        - None
    """

    # transpose the data to shape (m, n) for KMeans
    data = data.T

    # initialize KMeans with kmeans++ initialization
    kmeans = skl.KMeans(n_clusters=nClusters, init='k-means++', random_state=0, n_init=20)

    # fit the model
    kmeans.fit(data)

    # compute the distance matrix using the specified distance metric
    distance_matrix = cdist(data, kmeans.cluster_centers_, metric=distanceMetric)

    # assign labels based on the minimum distance
    labels = np.argmin(distance_matrix, axis=1)

    return labels

def hierarchical_clustering(data, nClusters, distanceMetric='seuclidean'):
    """
    Perform hierarchical clustering with specified distance metric.

    Args:
        data (np.ndarray): The data to cluster, shape (n, m) where n is the number of dimensions and m is the number of measurements.
        n_clusters (int): The number of clusters.
        distance_metric (str): The distance metric to use ('euclidean', 'cityblock', 'cosine', etc.).

    distanceMetric options: ‘cityblock’, ‘cosine’, ‘euclidean’, ‘l1’, ‘l2’, ‘manhattan’, ‘braycurtis’, ‘canberra’, ‘chebyshev’, ‘correlation’, ‘dice’, ‘hamming’, ‘jaccard’, ‘kulsinski’, ‘mahalanobis’, ‘minkowski’, ‘rogerstanimoto’, ‘russellrao’, ‘seuclidean’, ‘sokalmichener’, ‘sokalsneath’, ‘sqeuclidean’, ‘yule’

    Functions called:
        - None

    Returns:
        np.ndarray: The cluster labels.
    """
    # Transpose the data to shape (m, n) for distance computation
    data = data.T

    # Compute the distance matrix using the specified distance metric
    distance_matrix = pairwise_distances(data, metric=distanceMetric)

    if distanceMetric == 'euclidean':
        linkage = 'ward'
    else:
        linkage = 'average'
    # Perform Agglomerative Clustering with the precomputed distance matrix
    clustering = skl.AgglomerativeClustering(n_clusters=nClusters, metric='precomputed', linkage=linkage)
    labels = clustering.fit_predict(distance_matrix)

    return labels

def calcNumberOfClusters(data,distanceMetric,manualNClusters=False, mean_window = 5, sensitivity=False):
    """
    Calculate the optimal number of clusters for the given data using the specified distance metric. Code is adapted
    from the original Matlab tool.

    Args:
        data (np.ndarray): The data to cluster, shape (n, m) where n is the number of dimensions and m is the number of measurements.
        distanceMetric (str): The distance metric to use for clustering.
        manualNClusters (int, optional): The manually specified number of clusters. Defaults to False.
        mean_window (int, optional): The window size for calculating the mean linkage. Defaults to 5.
        sensitivity (float, optional): The sensitivity threshold for determining the optimal number of clusters. Defaults to False.

    Returns:
        tuple: A tuple containing the optimal number of clusters and the plotly figure object.

    Functions called:
        - None

    Raises:
        ValueError: If the distance metric is not supported.
    """

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
#            autorangeoptions_clipmin=0,

        ),
    )
    return Clusternumber, fig