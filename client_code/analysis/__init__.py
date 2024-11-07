from ._anvil_designer import analysisTemplate

from anvil import *
import plotly.graph_objects as go
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
    
    #initialise dropdowns
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
    Updates the items in the dropdown menus for year and component.
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
    Updates the given global set based on the checked state of checkboxes within the provided card.

    Args:
        card (anvil.Card): The card component containing checkboxes.
        globalSet (set): The global set to be updated with the text of checked checkboxes.

    This function iterates over all components within the provided card. If a component is a checkbox and it is checked,
    the text of the checkbox is added to the global set. If the checkbox is not checked, the text is removed from the global set.
    """

    for box in card.get_components():
      if box.checked:
        globalSet.add(box.text)
      else:
        globalSet.discard(box.text)

  def updatePlots(self, **event_args):
    if globals.clustered:
      if 'component' in globals.selected_clustering:
        # component based
        globals.plots_component, stDev = anvil.server.call('getPlot', 'component', self.drop_down_component.selected_value,
                                               self.drop_down_envelope_predict.selected_value)
        self.label_results_stdDev_comp.text = f"{stDev:.2f}"
      if 'frequency' in globals.selected_clustering:
        # frequency based
        globals.plots_frequency, stDev = anvil.server.call('getPlot', 'frequency', self.drop_down_component.selected_value,
                                               self.drop_down_envelope_predict.selected_value)
        self.label_results_stdDev_freq.text = f"{stDev:.2f}"
      if 'position' in globals.selected_clustering:
          # position based
          globals.plots_position, stDev = anvil.server.call('getPlot', 'position', self.drop_down_component.selected_value,
                                                   self.drop_down_envelope_predict.selected_value)
          self.label_results_stdDev_pos.text = f"{stDev:.2f}"

      globals.plots_overview = anvil.server.call('getOverviewPlot', globals.selected_component, globals.plots_component, globals.plots_position, globals.plots_frequency)

      if globals.selected_compare:
        if globals.selected_showComparisonData:
          fileName = self.drop_down_compFile.selected_value
        else:
          fileName = None

        anvil.server.call('assembleComparisonData', globals.selected_year, globals.selected_component,
                            globals.selected_frequencyRange,globals.selected_envelopeMethods[1])
        self.drop_down_compFile.items = anvil.server.call('getComparisonDataFileNames')
        globals.plots_overview, success, stDev = anvil.server.call('addComparisonDataToOverviewPlot', globals.plots_overview, globals.selected_envelopeMethods[1], globals.selected_frequencyRange, fileName)

        if not success:
            Notification("Comparison data not available for selected component and year.", style="warning").show()
            self.label_results_stdDev_measurements.text = '-'
        else:
            self.label_results_stdDev_measurements.text = f"{stDev:.2f}"

      if globals.activePlot == 'overview':
          self.link_plot_overview_click()
      if globals.activePlot == 'comp':
          self.link_plot_comp_click()
      elif globals.activePlot == 'freq':
          self.link_plot_freq_click()
      elif globals.activePlot == 'pos':
          self.link_plot_pos_click()
      elif globals.activePlot == 'cog':
          pass
      elif globals.activePlot == 'link':
          pass




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
  def check_box_cluster_pos_change(self, **event_args):
    self.saveBoxes(self.card_clustering, globals.selected_clustering)
  def check_box_cluster_comp_change(self, **event_args):
    self.saveBoxes(self.card_clustering, globals.selected_clustering)
############################################################################################################
# textboxes
############################################################################################################
# frequency range textboxes
  def text_box_freq_min_change(self, **event_args):
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
    globals.selected_compare = self.radio_button_function_compare.selected
    self.card_compFile.visible = globals.selected_compare
    self.card_error.visible = globals.selected_compare
    self.label_measEnv.visible = globals.selected_compare
    self.label_results_stdDev_measurements.visible = globals.selected_compare
    self.drop_down_year.enabled = False
    self.updatePlots()
  
  def radio_button_function_compare_clicked(self, **event_args):
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
  def link_plot_comp_click(self, **event_args):
    self.deselect_all_links()
    self.link_plot_comp.bold = True
    globals.activePlot = 'comp'
    self.plot.figure = globals.plots_component

  def link_plot_pos_click(self, **event_args):
    self.deselect_all_links()
    self.link_plot_pos.bold = True
    globals.activePlot = 'pos'

  def link_plot_cog_click(self, **event_args):
    self.deselect_all_links()
    self.link_plot_cog.bold = True
    globals.activePlot = 'cog'

  def link_link_click(self, **event_args):
    self.deselect_all_links()
    self.link_plot_link.bold = True
    globals.activePlot = 'link'

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







    

