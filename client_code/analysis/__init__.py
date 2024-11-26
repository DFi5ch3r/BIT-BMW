from ._anvil_designer import analysisTemplate

from anvil import *
import anvil.server

from .. import globals


class analysis(analysisTemplate):
###########################################################################################################
# initialisation
###########################################################################################################
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    self.repeating_panel_1.items =  globals.baureihe_years

    self.set_event_handler('x-updateDropDowns', self.updateDropDowns)
    self.set_event_handler('x-updateResults', self.updateResults)
    
    # initialise dropdowns
    if globals.dataLoaded:
      self.updateDropDowns()
    self.drop_down_envelope_cluster.items = globals.envelopGenerationMethods
    self.drop_down_envelope_predict.items = globals.envelopGenerationMethods

    self.drop_down_year.enabled = False
    if globals.selected_compare:
      self.radio_button_function_compare_clicked()

    # initialise GUI globals (selected_*)
    self.saveBoxes(self.card_buildstages, globals.selected_buildstage)
    self.saveBoxes(self.card_directions, globals.selected_directions)
    self.saveBoxes(self.card_clustering, globals.selected_clustering)  
    globals.selected_frequencyRange[0] = int(self.text_box_freq_min.text)
    globals.selected_frequencyRange[1] = int(self.text_box_freq_max.text)
    globals.selected_envelopeMethods[0] = self.drop_down_envelope_cluster.selected_value
    globals.selected_envelopeMethods[1] = self.drop_down_envelope_predict.selected_value
    globals.selected_year = self.drop_down_year.selected_value
    globals.selected_component = self.drop_down_component.selected_value

############################################################################################################
# auxiliary functions
############################################################################################################
  def updateDropDowns(self, **event_args):
    """
    Update the dropdown menus with unique values from the selected data.

    This method retrieves unique values for the 'Jahr' and 'Bauteil' fields from the selected data and updates the corresponding dropdown menus. It also updates the global variables with the selected values.

    Functions called:
        - anvil.server.call('get_unique_values')
    """
    self.drop_down_year.items = anvil.server.call('get_unique_values','Jahr', sourceSelectedData=True)
    if self.drop_down_year.items:
      self.drop_down_year.selected_value = self.drop_down_year.items[-1]
    self.drop_down_component.items = anvil.server.call('get_unique_values','Bauteil', sourceSelectedData=True, prefixes=True)

    globals.selected_year = self.drop_down_year.selected_value
    globals.selected_component = self.drop_down_component.selected_value

  def updateResults(self, **event_args):
    self.updatePlots()
  
  def saveBoxes(self, card, globalSet):
    """
    Save the state of checkboxes in a card to a global set.

    This method iterates over all checkbox components within a given card and updates the provided global set based on
    whether each checkbox is checked or not.

    Functions called:
        - None
    """

    for box in card.get_components():
      if box.checked:
        globalSet.add(box.text)
      else:
        globalSet.discard(box.text)

  def updatePlots(self, **event_args):
    """
    Update the plots based on the selected data and clustering results.

    This method retrieves various plots from the server, including linkage, component-based, frequency-based,
    position-based, overview, comparison, and cog plots. It updates the UI elements with the retrieved plots and
    displays notifications if necessary.

    Functions called:
        - anvil.server.call('getLinkagePlot')
        - anvil.server.call('getPlot')
        - anvil.server.call('getOverviewPlot')
        - anvil.server.call('assembleComparisonData')
        - anvil.server.call('getComparisonDataFileNames')
        - anvil.server.call('addComparisonDataToOverviewPlot')
        - anvil.server.call('getErrors')
        - anvil.server.call('getCogPlot')
    """

    # Retrieve linkage plot
    globals.plots_link = anvil.server.call('getLinkagePlot')

    if globals.clustered:
      if globals.clustered_comp and 'component' in globals.selected_clustering:
        # Retrieve component-based plot
        globals.plots_component, componentEnv, stDev = anvil.server.call('getPlot', 'component', self.drop_down_component.selected_value,
                                               self.drop_down_envelope_predict.selected_value)
        self.label_results_stdDev_comp.text = f"{stDev:.2f}"
      if globals.clustered_freq and 'frequency' in globals.selected_clustering:
        # Retrieve frequency-based plot
        globals.plots_frequency, freqencyEnv, stDev = anvil.server.call('getPlot', 'frequency', self.drop_down_component.selected_value,
                                               self.drop_down_envelope_predict.selected_value)
        self.label_results_stdDev_freq.text = f"{stDev:.2f}"

      if globals.clustered_pos and 'position' in globals.selected_clustering:
        # Retrieve position-based plot
        globals.plots_position, positionEnv, stDev = anvil.server.call('getPlot', 'position', self.drop_down_component.selected_value,
                                                 self.drop_down_envelope_predict.selected_value)
        # check if position data for components exist
        if positionEnv:
          globals.positionDataForComponentsExist = True
          self.label_results_stdDev_pos.text = f"{stDev:.2f}"
        else:
          globals.positionDataForComponentsExist = False
          self.label_results_stdDev_pos.text = '-'
          Notification("Position data for "+ self.drop_down_component.selected_value + " not available.", style="warning").show()

      # Retrieve overview plot
      globals.plots_overview = anvil.server.call('getOverviewPlot', globals.selected_component, globals.plots_component, globals.plots_position, globals.plots_frequency)

      # Retrieve comparison data if selected
      if globals.selected_compare:
        if globals.selected_showComparisonData:
          fileName = self.drop_down_compFile.selected_value
        else:
          fileName = None

        # Assemble comparison data
        anvil.server.call('assembleComparisonData', globals.selected_year, globals.selected_component,
                            globals.selected_frequencyRange,globals.selected_envelopeMethods[1])
        # Retrieve comparison data file names
        self.drop_down_compFile.items = anvil.server.call('getComparisonDataFileNames')
        # Add comparison data to overview plot
        globals.plots_overview, success, stDev = anvil.server.call('addComparisonDataToOverviewPlot', globals.plots_overview, fileName)

        # Check if adding comparison data was successful and update UI elements with error and shape confidence values
        if not success:
            Notification("Comparison data not available for selected component and year.", style="warning").show()
            self.label_results_stdDev_measurements.text = '-'
        else:
            self.label_results_stdDev_measurements.text = f"{stDev:.2f}"
            if globals.clustered_comp:
              # Update component error and shape confidence
              magError, shapeConf = anvil.server.call('getErrors', componentEnv)
              self.label_results_error_comp.text = f"{magError:.0f}"
              self.label_results_shape_comp.text = f"{shapeConf:.3f}"
            else:
              self.label_results_error_comp.text = '-'
              self.label_results_shape_comp.text = '-'
            if globals.clustered_freq:
              # Update component error and shape confidence
              magError, shapeConf = anvil.server.call('getErrors', freqencyEnv)
              self.label_results_error_freq.text = f"{magError:.0f}"
              self.label_results_shape_freq.text = f"{shapeConf:.3f}"
            else:
              self.label_results_error_freq.text = '-'
              self.label_results_shape_freq.text = '-'
            if globals.clustered_pos and positionEnv:
              # Update component error and shape confidence
              magError, shapeConf = anvil.server.call('getErrors', positionEnv)
              self.label_results_error_pos.text = f"{magError:.0f}"
              self.label_results_shape_pos.text = f"{shapeConf:.3f}"
            else:
              self.label_results_error_pos.text = '-'
              self.label_results_shape_pos.text = '-'

      # Retrieve cog plot
      globals.plots_cog = anvil.server.call('getCogPlot')

      # Select active plot
      if globals.activePlot == 'overview':
          self.link_plot_overview_click()
      if globals.activePlot == 'comp':
          self.link_plot_comp_click()
      elif globals.activePlot == 'freq':
          self.link_plot_freq_click()
      elif globals.activePlot == 'pos':
          self.link_plot_pos_click()
      elif globals.activePlot == 'cog':
          self.link_plot_cog_click()
      elif globals.activePlot == 'link':
          self.link_link_click()

############################################################################################################
# checkboxes
############################################################################################################

# buildstage checkboxes
  def check_box_BS_BS0_change(self, **event_args):
    self.saveBoxes(self.card_buildstages, globals.selected_buildstage)
    self.parent.parent.raise_event('x-dataNotUpToDate')
  def check_box_BS_BS1_change(self, **event_args):
    self.saveBoxes(self.card_buildstages, globals.selected_buildstage)
    self.parent.parent.raise_event('x-dataNotUpToDate')
  def check_box_BS_VS1_change(self, **event_args):
    self.saveBoxes(self.card_buildstages, globals.selected_buildstage)
    self.parent.parent.raise_event('x-dataNotUpToDate')
  def check_box_BS_VS2_change(self, **event_args):
    self.saveBoxes(self.card_buildstages, globals.selected_buildstage)
    self.parent.parent.raise_event('x-dataNotUpToDate')
  def check_box_BS_KEX_change(self, **event_args):
    self.saveBoxes(self.card_buildstages, globals.selected_buildstage)
    self.parent.parent.raise_event('x-dataNotUpToDate')
  def check_box_BS_SERIE_change(self, **event_args):
    self.saveBoxes(self.card_buildstages, globals.selected_buildstage)
    self.parent.parent.raise_event('x-dataNotUpToDate')
  def check_box_BS_notFound_change(self, **event_args):
    self.saveBoxes(self.card_buildstages, globals.selected_buildstage)  
    self.parent.parent.raise_event('x-dataNotUpToDate')
  def check_box_4_BS_FB_change(self, **event_args):
    self.saveBoxes(self.card_buildstages, globals.selected_buildstage)
    self.parent.parent.raise_event('x-dataNotUpToDate')
  def check_box_4_BS_AS_change(self, **event_args):
    self.saveBoxes(self.card_buildstages, globals.selected_buildstage)
    self.parent.parent.raise_event('x-dataNotUpToDate')

# direction checkboxes
  def check_box_dir_xNeg_change(self, **event_args):
    self.saveBoxes(self.card_directions, globals.selected_directions)
    self.parent.parent.raise_event('x-dataNotUpToDate')
  def check_box_dir_xPos_change(self, **event_args):
    self.saveBoxes(self.card_directions, globals.selected_directions)
    self.parent.parent.raise_event('x-dataNotUpToDate')
  def check_box_dir_yNeg_change(self, **event_args):
    self.saveBoxes(self.card_directions, globals.selected_directions)
    self.parent.parent.raise_event('x-dataNotUpToDate')
  def check_box_dir_yPos_change(self, **event_args):
    self.saveBoxes(self.card_directions, globals.selected_directions)
    self.parent.parent.raise_event('x-dataNotUpToDate')
  def check_box_dir_zNeg_change(self, **event_args):
    self.saveBoxes(self.card_directions, globals.selected_directions)
    self.parent.parent.raise_event('x-dataNotUpToDate')
  def check_box_dir_zPos_change(self, **event_args):
    self.saveBoxes(self.card_directions, globals.selected_directions)
    self.parent.parent.raise_event('x-dataNotUpToDate')

# clustering checkboxes
  def check_box_cluster_frequ_change(self, **event_args):
    self.saveBoxes(self.card_clustering, globals.selected_clustering)
    self.parent.parent.raise_event('x-clusterNotUpToDate')
  def check_box_cluster_pos_change(self, **event_args):
    self.saveBoxes(self.card_clustering, globals.selected_clustering)
    self.parent.parent.raise_event('x-clusterNotUpToDate')
  def check_box_cluster_comp_change(self, **event_args):
    self.saveBoxes(self.card_clustering, globals.selected_clustering)
    self.parent.parent.raise_event('x-clusterNotUpToDate')

############################################################################################################
# textboxes
############################################################################################################
# frequency range textboxes
  def text_box_freq_min_change(self, **event_args):
    """
    Handle changes to the minimum frequency text box.

    This method ensures that the minimum frequency value is valid and updates the global variable accordingly. It also
    triggers an event to mark the data as not up-to-date.
    """
    if (int(self.text_box_freq_min.text) >= int(self.text_box_freq_max.text)):
      self.text_box_freq_min.text = int(self.text_box_freq_max.text) - 10
    elif int(self.text_box_freq_min.text) <0:
      self.text_box_freq_min.text = 0
    globals.selected_frequencyRange[0] = int(self.text_box_freq_min.text)
    self.parent.parent.raise_event('x-dataNotUpToDate')
    
  def text_box_freq_max_change(self, **event_args):
    globals.selected_frequencyRange[1] = int(self.text_box_freq_max.text)
    self.parent.parent.raise_event('x-dataNotUpToDate')

############################################################################################################
# radio buttons
############################################################################################################
# function radio buttons
  def radio_button_function_predict_change(self, **event_args):
    """
    Handle changes to the predict function radio button.

    This method updates the global variable `selected_compare` based on the state of the compare radio button.
    It also updates the visibility of related UI elements and triggers the plot update.

    Functions called:
        - self.updatePlots()
    """
    globals.selected_compare = self.radio_button_function_compare.selected
    self.card_compFile.visible = globals.selected_compare
    self.card_error.visible = globals.selected_compare
    self.label_measEnv.visible = globals.selected_compare
    self.label_results_stdDev_measurements.visible = globals.selected_compare
    self.drop_down_year.enabled = False
    self.updatePlots()
  
  def radio_button_function_compare_clicked(self, **event_args):
    """
    Handle the click event for the compare function radio button.

    This method sets the global variable `selected_compare` to True and updates the visibility of related UI elements.
    It also enables the year dropdown and triggers the plot update.

    Functions called:
        - self.updatePlots()
    """
    globals.selected_compare = True
    self.card_compFile.visible = globals.selected_compare
    self.card_error.visible = globals.selected_compare
    self.label_measEnv.visible = globals.selected_compare
    self.label_results_stdDev_measurements.visible = globals.selected_compare
    self.drop_down_year.enabled = True
    self.updatePlots()

############################################################################################################
# links
############################################################################################################
# plot selection links
  def deselect_all_links(self):
    """
    Deselect all plot selection links.

    This method iterates over all link components within the `card_plotSelection` card and sets their `bold` attribute to False.
    It is used to ensure that no plot selection link is highlighted.

    Functions called:
        - None
    """
    for link in self.card_plotSelection.get_components():
      link.bold=False
      
  def link_plot_overview_click(self, **event_args):
    self.deselect_all_links()
    self.link_plot_overview.bold = True
    globals.activePlot = 'overview'
    self.plot.figure = globals.plots_overview

  def link_plot_freq_click(self, **event_args):
    self.deselect_all_links()
    self.link_plot_freq.bold = True
    globals.activePlot = 'freq'
    self.plot.figure = globals.plots_frequency

  def link_plot_comp_click(self, **event_args):
    self.deselect_all_links()
    self.link_plot_comp.bold = True
    globals.activePlot = 'comp'
    self.plot.figure = globals.plots_component

  def link_plot_pos_click(self, **event_args):
    self.deselect_all_links()
    self.link_plot_pos.bold = True
    globals.activePlot = 'pos'
    self.plot.figure = globals.plots_position

  def link_plot_cog_click(self, **event_args):
    self.deselect_all_links()
    self.link_plot_cog.bold = True
    globals.activePlot = 'cog'
    self.plot.figure = globals.plots_cog

  def link_link_click(self, **event_args):
    self.deselect_all_links()
    self.link_plot_link.bold = True
    globals.activePlot = 'link'
    self.plot.figure = globals.plots_link

############################################################################################################
# dropdowns
############################################################################################################

  def drop_down_compFile_change(self, **event_args):
    globals.selected_comparisonFile = self.drop_down_compFile.selected_value
    self.updatePlots()

  def check_box_compFile_show_change(self, **event_args):
    globals.selected_showComparisonData = self.check_box_compFile_show.checked
    self.updatePlots()

  def drop_down_year_change(self, **event_args):
    globals.selected_year = self.drop_down_year.selected_value
    self.updatePlots()

  def drop_down_component_change(self, **event_args):
   globals.selected_component = self.drop_down_component.selected_value
   self.updatePlots()

   # envelope generation dropdowns

  def drop_down_envelope_cluster_change(self, **event_args):
   globals.selected_envelopeMethods[0] = self.drop_down_envelope_cluster.selected_value
   if globals.clustered:
     anvil.server.call('generateEnvelopesForClusters', globals.selected_envelopeMethods[0])
     self.updatePlots()

  def drop_down_envelope_predict_change(self, **event_args):
   globals.selected_envelopeMethods[1] = self.drop_down_envelope_predict.selected_value
   if globals.clustered:
     self.updatePlots()







    

