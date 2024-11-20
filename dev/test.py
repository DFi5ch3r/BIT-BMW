import functions_test
import server_code.IO as IO
import server_code.dataAnalysis as DA
from server_code import serverGlobals
import os
import numpy as np
import anvil.server
import plotly.graph_objects as go

path = '/home/dfischer/12-Projects/09-BMW-BIT/01-originalMatlabTool/BMW_BIT_TUB/BMW_Phase2_txtonly_BackUp'
IO.create_database(path)
#db = serverGlobals.DB

IO.filter_database('Baureihe', ['K51'], sourceFullDB = True)
# IO.filter_database('Baureihe', ['K02'], sourceFullDB = True)
#IO.filter_database('Baureihe', ['K03'], sourceFullDB = True)

IO.readData(selectedData=True)


IO.loadCoGdata(path)
#IO.addCoGdataToDB()
db2 = serverGlobals.selectedData

#clusters = DA.clusterPositions(6,[72,2000],True)
#clusters = serverGlobals.clusters_positions
#clusters = DA.assembleData('Bauteil')

#DA.generateEnvelopes(clusters, envelopGenerationMethods[2])

DA.clusterFrequencies(False,[72,2000], True, 'seuclidean')

serverGlobals.plot_linkage.show
serverGlobals.plot_linkage.show()



import numpy as np
import plotly.graph_objects as go




############################################



#fig = IO.getCogPlot()
#fig.show()
def plot_cluster(cluster):
    """
    Plots all amplitude rows over frequencies in black and the envelope over frequencies in red.

    Args:
        cluster (dict): A dictionary containing 'frequencies', 'amplitudes', and 'envelope' arrays.
    """
    frequencies = cluster['frequencies']
    amplitudes = cluster['amplitudes']
    envelope = cluster['envelope']

    # Create a Plotly figure
    fig = go.Figure()

    # Plot all amplitude rows in black
    for i in range(amplitudes.shape[1]):
        fig.add_trace(go.Scatter(x=frequencies, y=amplitudes[:, i], mode='lines', line=dict(color='black', width=1), opacity=0.5))

    # Plot the envelope in red
    fig.add_trace(go.Scatter(x=frequencies, y=envelope, mode='lines', line=dict(color='red', width=2)))

    # Add labels and title
    fig.update_layout(
        title=cluster['name'],
        xaxis_title='Frequencies',
        yaxis_title='Amplitudes'
    )

    # Show the plot
    fig.show()

#plot_cluster(clusters[0])