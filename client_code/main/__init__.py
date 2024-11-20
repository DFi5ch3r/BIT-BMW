from ._anvil_designer import mainTemplate
from anvil import *
import anvil.server
import plotly.graph_objects as go

from ..input import input
from ..settings import settings
from ..analysis import analysis

from .. import globals


class main(mainTemplate):
  def __init__(self, **properties):
###########################################################################################################
# initialisation
###########################################################################################################
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.set_event_handler('x-dataNotUpToDate', self.dataNotUpToDate)
    self.set_event_handler('x-clusterNotUpToDate', self.clusterNotUpToDate)

    self.dataNotUpToDate()

    self.content_panel.clear()
    self.content_panel.add_component(analysis(), full_width_row=True)
    self.deselect_all_links()
    self.link_analysis.role = 'selected'


  ###########################################################################################################
  # links
  ###########################################################################################################
# Topbar links
  def deselect_all_links(self):
    """Reset all the roles on the navbar links."""
    for link in self.link_input, self.link_settings, self.link_analysis:
      link.role = ''
      
  def link_input_click(self, **event_args):
    """This method is called when the link is clicked"""
    self.content_panel.clear()
    self.content_panel.add_component(input(), full_width_row=True)
    self.deselect_all_links()
    self.link_input.role = 'selected'

  def link_settings_click(self, **event_args):
    """This method is called when the link is clicked"""
    self.content_panel.clear()
    self.content_panel.add_component(settings(), full_width_row=True)
    self.deselect_all_links()
    self.link_settings.role = 'selected'

  def link_analysis_click(self, **event_args):
    """This method is called when the link is clicked"""
    self.content_panel.clear()
    self.content_panel.add_component(analysis(), full_width_row=True)
    self.deselect_all_links()
    self.link_analysis.role = 'selected'
    
# side bar links
  def button_loadDataBase_click(self, **event_args):
    """This method is called when the link is clicked"""

    with Notification("Generating Database..."):

      # create database
      anvil.server.call('create_database',globals.input_customPath)
      #anvil.server.call('create_databaseTEST',globals.input_customPath)
      globals.baureihe_years = anvil.server.call('get_baureihe_and_years')

      # load CoG data
      anvil.server.call('loadCoGdata',globals.input_customPath)
      anvil.server.call('addCoGdataToDB')

      self.button_loadDataBase.foreground = '#1EB980'
      self.link_analysis_click()
   
  def button_loadSelectedData_click(self, **event_args):

    if not globals.selected_BaureiheYears:
        Notification("No data selected!", style="danger").show()
        return

    Notification("Filtering database ...").show()
    # filter by direction
    anvil.server.call('filter_database', key = 'Richtung', values = list(globals.selected_directions), sourceFullDB = True)
    # filter by buildstage
    anvil.server.call('filter_database', key = 'Baustufe', values = list(globals.selected_buildstage), sourceFullDB = False)
    # filter by Baureihe and year
    anvil.server.call('filter_database', key = 'Baureihe', secondKey = 'Jahr', values = list(globals.selected_BaureiheYears), sourceFullDB = False)
    globals.dataLoaded = True
    self.content_panel.raise_event_on_children('x-updateDropDowns')

    with Notification("Reading data ...",):
        anvil.server.call('readData', selectedData=True)
    Notification("...done loading data.", style="success").show()

    self.button_loadSelectedData.foreground = '#1EB980'
    globals.dataLoaded = True

  def button_clusterData_click(self, **event_args):

    if not globals.selected_BaureiheYears:
        Notification("No data selected!!", style="danger").show()
        return

    if not globals.dataLoaded:
      self.button_loadSelectedData_click()

    if 'component' in globals.selected_clustering:
        Notification("Clustering by components ...").show()
        globals.clustered_comp = anvil.server.call('clusterComponents', globals.selected_frequencyRange)
    if 'frequency' in globals.selected_clustering:
        Notification("Clustering by frequencies ...").show()

        # automatic cluster number or custom number of clusters
        if globals.settings_freqSuperClusterNumberCustom:
            nClusters = globals.settings_freqSuperClusterNumber
        else:
            nClusters = False

        # distance metric
        if globals.settings_freqClusterIsHierarchical:
            distanceMetric = globals.settings_freqDistanceMetricHierarchical
        else:
            distanceMetric = globals.settings_freqDistanceMetricKMeans

        globals.clustered_freq = anvil.server.call('clusterFrequencies',nClusters, globals.selected_frequencyRange, globals.settings_freqClusterIsHierarchical, distanceMetric)



    if 'position' in globals.selected_clustering:
        Notification("Clustering by positions ...").show()
        globals.clustered_pos = anvil.server.call('clusterPositions', globals.settings_posClusterNumber, globals.selected_frequencyRange,globals.settings_posClusterIsHierarchical)


    Notification("Generating envelopes ...").show()
    anvil.server.call('generateEnvelopesForClusters', globals.selected_envelopeMethods[0])
    globals.clustered = True

    self.content_panel.raise_event_on_children('x-updateResults')

    Notification("...done clustering.", style="success").show()
    self.button_clusterData.foreground = '#1EB980'


  def button_displaySettings_click(self, **event_args):
    self.show_globals()

  def button_test_click(self, **event_args):
    anvil.server.call('test')
    #self.show_globals()
    #self.content_panel.raise_event_on_children('x-updateResults')

  def link_reset_click(self, **event_args):
    anvil.js.window.location.reload(True)

###########################################################################################################
# auxiliary functions
###########################################################################################################
  def show_globals(self, **event_args):
    """
    Creates a notification window within the Anvil GUI containing all the values of the variables
    starting with selected_, settings_, and input_ within globals, displayed as a table.
    """
    # Retrieve all variables from globals that start with selected_, settings_, and input_
    variables = {name: value for name, value in globals.__dict__.items() if name.startswith(('selected_', 'settings_', 'input_'))}

    # Create the table string with headers
    table_string = "{:<50} {:<50}\n".format("Variable", "Value")

    # Add each variable and its value as a row in the table string
    for name, value in variables.items():
        table_string += "{:<60} {:<200}\n".format(name, str(value))
    # Display the notification window
    anvil.Notification(table_string, title="Global Variables", style="info", timeout=None).show()


  def dataNotUpToDate(self, **event_args):
    self.button_loadSelectedData.foreground = '#D64D47'
    self.button_clusterData.foreground = '#D64D47'
    globals.dataLoaded = False

  def clusterNotUpToDate(self, **event_args):
      self.button_clusterData.foreground = '#D64D47'




