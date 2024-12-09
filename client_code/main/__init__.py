from ._anvil_designer import mainTemplate
from anvil import *
import anvil.server
import anvil.media

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
# ------------------------------------------------------------------------------------------------------- #
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
    
# side-bar links
# ------------------------------------------------------------------------------------------------------- #
  def button_loadDataBase_click(self, **event_args):
    """
    Load the database based on the selected input method.

    This method handles loading the database from different sources such as a directory, a previously generated
    database, or an external database. It also updates the global variables and UI elements accordingly.

    Functions called:
        - anvil.server.call('load_database')
        - anvil.server.call('create_database')
        - anvil.server.call('loadCoGdata')
        - anvil.server.call('addCoGdataToDB')
        - anvil.server.call('get_baureihe_and_years')
    """
    with (Notification("Generating Database...")):
      # load data from directories
      #----------------------------------------------------------#
      if globals.input_inputMethod == 'directory':
          # Prompt the user to use the cached database
          cacheDB = alert('Do you want to use the cached database?', title='Use cached database', buttons=[('Yes', True), ('No', False)], dismissible=False)

          # load database from cache
          if cacheDB:
            dbLoaded = anvil.server.call('load_database')
            if not dbLoaded:
                Notification("No cached database not found, reading from files...", style='warning').show()
          else:
            dbLoaded = False

          # Create database from files
          dbRead = False
          if not dbLoaded:
              dbRead = anvil.server.call('create_database',globals.input_customPath)
              #anvil.server.call('create_databaseTEST',globals.input_customPath)

          if dbRead:
              # load CoG data
              anvil.server.call('loadCoGdata',globals.input_customPath)
              anvil.server.call('addCoGdataToDB')
          else:
              if not dbLoaded:
                Notification("No data found in the selected directory!", style="danger").show()
                if not dbLoaded:
                    return

      # load data from previously generated database
      #----------------------------------------------------------#
      elif globals.input_inputMethod == 'previously generated database':
        # path = os.path.join(globals.input_customPath, globals.input_fileName)
        path = globals.input_customPath + '/' + globals.input_fileName
        dbLoaded = anvil.server.call('load_database', path)
        if not dbLoaded:
            Notification("Database not found!", style="danger").show()
            return

      # load data from external database
      #----------------------------------------------------------#
      elif globals.input_inputMethod == 'external database':
        Notification("External database not implemented yet!", style="danger").show()
        return

      else:
        Notification("No input method selected!", style="danger").show()
        return

      # Update global variables and UI elements
      globals.baureihe_years = anvil.server.call('get_baureihe_and_years')
      self.button_loadDataBase.foreground = '#1EB980'
      self.link_analysis_click()
   
  def button_loadSelectedData_click(self, **event_args):
    """
    Load the selected data based on user input.

    This method filters the database based on the selected criteria such as direction, build stage, and Baureihe and
    year. It also updates the global variables and UI elements accordingly.

    Functions called:
        - anvil.server.call('filter_database')
        - anvil.server.call('excludeMotor')
        - anvil.server.call('readData')
    """
    # Check if any data is selected
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

    # Exclude motor data if the setting is enabled
    if globals.settings_excludeMotor:
        anvil.server.call('excludeMotor')

    # Update the dropdowns in the UI
    self.content_panel.raise_event_on_children('x-updateDropDowns')
    globals.dataLoaded = True

    # Read the data
    with Notification("Reading data ...",):
        anvil.server.call('readData', selectedData=True)
    Notification("...done loading data.", style="success").show()

    # Update the button color to indicate success
    self.button_loadSelectedData.foreground = '#1EB980'
    globals.dataLoaded = True

  def button_clusterData_click(self, **event_args):
    """
    Cluster the selected data based on user input.

    This method clusters the data based on the selected criteria such as component, frequency, and position. It also updates the global variables and UI elements accordingly.

    Functions called:
        - anvil.server.call('clusterComponents')
        - anvil.server.call('clusterFrequencies')
        - anvil.server.call('clusterPositions')
        - anvil.server.call('generateEnvelopesForClusters')
    """
    # Check if any data is selected
    if not globals.selected_BaureiheYears:
        Notification("No data selected!!", style="danger").show()
        return
    # Load selected data if not already loaded
    if not globals.dataLoaded:
      self.button_loadSelectedData_click()

    # Cluster by components if selected
    if 'component' in globals.selected_clustering:
        with Notification("Clustering by components ..."):
            globals.clustered_comp = anvil.server.call('clusterComponents', globals.selected_frequencyRange)

    # Cluster by frequencies if selected
    if 'frequency' in globals.selected_clustering:
        with Notification("Clustering by frequencies ..."):
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

    # Cluster by positions if selected
    if 'position' in globals.selected_clustering:
        with Notification("Clustering by positions ..."):
            globals.clustered_pos = anvil.server.call('clusterPositions', globals.settings_posClusterNumber, globals.selected_frequencyRange,globals.settings_posClusterIsHierarchical)

    # Generate envelopes for clusters
    with Notification("Generating envelopes for clusters..."):
        anvil.server.call('generateEnvelopesForClusters', globals.selected_envelopeMethods[0])
    globals.clustered = True

    # Update the UI elements
    self.content_panel.raise_event_on_children('x-updateResults')
    Notification("...done clustering.", style="success").show()
    self.button_clusterData.foreground = '#1EB980'

  def button_displaySettings_click(self, **event_args):
    self.show_globals()

  def link_reset_click(self, **event_args):
    """
    Reload the current page.

    This method reloads the current page in the browser, effectively resetting the application state.
    """
    anvil.js.window.location.reload(True)

  def button_export_click(self, **event_args):
    export = alert('Download:', title='Export data',
                      buttons=[('database', 'DB'), ('data of clusters', 'clusterData'),('prediction plot', 'predictionPlot')], dismissible=True)
    if export == 'DB':
        file = anvil.server.call('exportDB')

    if export:
        anvil.media.download(file)



  ###########################################################################################################
# auxiliary functions
###########################################################################################################
  def show_globals(self, **event_args):
    """
    Display the global variables.

    This method retrieves all global variables that start with `selected_`, `settings_`, and `input_` from the `globals`
    module and displays them in a notification window.
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
    """
    Mark the data as not up-to-date.

    This method updates the UI to indicate that the data is not up-to-date by changing the button colors and setting the
    `dataLoaded` flag to False in the global variables.
    """
    self.button_loadSelectedData.foreground = '#D64D47'
    self.button_clusterData.foreground = '#D64D47'
    globals.dataLoaded = False

  def clusterNotUpToDate(self, **event_args):
      """
      Mark the data as not up-to-date.

      This method updates the UI to indicate that the data is not up-to-date by changing the button colors and setting the
      `dataLoaded` flag to False in the global variables.
      """
      self.button_clusterData.foreground = '#D64D47'






