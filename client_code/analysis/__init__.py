from ._anvil_designer import analysisTemplate

from anvil import *
import plotly.graph_objects as go
import anvil.server
from .. import globals


class analysis(analysisTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties) 
    self.repeating_panel_1.items =  globals.baureihe_years
    
    self.set_event_handler('x-updateResults', self.updateResults)
    
    #initialise dropdowns
    self.drop_down_year.items = anvil.server.call('get_unique_values','Jahr')
    if self.drop_down_year.items: 
      self.drop_down_year.selected_value = self.drop_down_year.items[-1]
    self.drop_down_component.items = anvil.server.call('get_unique_values','Bauteil')
    self.drop_down_envelope_cluster.items = globals.envelopGenerationMethods
    self.drop_down_envelope_predict.items = globals.envelopGenerationMethods

# initialise GUI globals (selected_*)
   # if not globals.selected_buildstage:
    self.saveBoxes(self.card_buildstages, globals.selected_buildstage)
    #if not globals.selected_directions:  
    self.saveBoxes(self.card_directions, globals.selected_directions)
    #if not globals.selected_clustering:
    self.saveBoxes(self.card_clustering, globals.selected_clustering)  
    globals.selected_frequencyRange[0] = self.text_box_freq_min.text
    globals.selected_frequencyRange[1] = self.text_box_freq_max.text
    globals.selected_envelopeMethods[0] = self.drop_down_envelope_cluster.selected_value
    globals.selected_envelopeMethods[1] = self.drop_down_envelope_predict.selected_value
    globals.selected_year = self.drop_down_year.selected_value
    globals.selected_component = self.drop_down_component.selected_value

# other functions
  def updateResults(self, **event_args):
    pass
  
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
        
# buildstage checkboxes
  def check_box_BS_BS0_change(self, **event_args):
    self.saveBoxes(self.card_buildstages, globals.selected_buildstage)
    
  def check_box_BS_BS1_change(self, **event_args):
    self.saveBoxes(self.card_buildstages, globals.selected_buildstage)
  def check_box_BS_VS1_change(self, **event_args):
    self.saveBoxes(self.card_buildstages, globals.selected_buildstage)
  
  def check_box_BS_VS2_change(self, **event_args):
    self.saveBoxes(self.card_buildstages, globals.selected_buildstage)
  
  def check_box_BS_KEX_change(self, **event_args):
    self.saveBoxes(self.card_buildstages, globals.selected_buildstage)
  
  def check_box_BS_SERIE_change(self, **event_args):
    self.saveBoxes(self.card_buildstages, globals.selected_buildstage)
  
  def check_box_BS_notFound_change(self, **event_args):
    self.saveBoxes(self.card_buildstages, globals.selected_buildstage)  

  def check_box_4_BS_FB_change(self, **event_args):
    self.saveBoxes(self.card_buildstages, globals.selected_buildstage)

  def check_box_4_BS_AS_change(self, **event_args):
    self.saveBoxes(self.card_buildstages, globals.selected_buildstage)

# direction checkboxes
  def check_box_dir_xNeg_change(self, **event_args):
    self.saveBoxes(self.card_directions, globals.selected_directions)

  def check_box_dir_xPos_change(self, **event_args):
    self.saveBoxes(self.card_directions, globals.selected_directions)

  def check_box_dir_yNeg_change(self, **event_args):
    self.saveBoxes(self.card_directions, globals.selected_directions)

  def check_box_dir_yPos_change(self, **event_args):
    self.saveBoxes(self.card_directions, globals.selected_directions)

  def check_box_dir_zNeg_change(self, **event_args):
    self.saveBoxes(self.card_directions, globals.selected_directions)

  def check_box_dir_zPos_change(self, **event_args):
    self.saveBoxes(self.card_directions, globals.selected_directions)

# frequency range textboxes
  def text_box_freq_min_change(self, **event_args):
    if (int(self.text_box_freq_min.text) >= int(self.text_box_freq_max.text)):
      self.text_box_freq_min.text = int(self.text_box_freq_max.text) - 10
    elif int(self.text_box_freq_min.text) <0:
      self.text_box_freq_min.text = 0
    globals.selected_frequencyRange[0] = self.text_box_freq_min.text

  def text_box_freq_max_change(self, **event_args):
    globals.selected_frequencyRange[1] = self.text_box_freq_max.text

# clustering checkboxes
  def check_box_cluster_frequ_change(self, **event_args):
    self.saveBoxes(self.card_clustering, globals.selected_clustering)

  def check_box_cluster_pos_change(self, **event_args):
    self.saveBoxes(self.card_clustering, globals.selected_clustering)

  def check_box_cluster_comp_change(self, **event_args):
    self.saveBoxes(self.card_clustering, globals.selected_clustering)

# envelope generation dropdowns
  def drop_down_envelope_cluster_change(self, **event_args):
    globals.selected_envelopeMethods[0] = self.drop_down_envelope_cluster.selected_value

  def drop_down_envelope_predict_change(self, **event_args):
    globals.selected_envelopeMethods[1] = self.drop_down_envelope_predict.selected_value

# function radio buttons
  def radio_button_function_predict_change(self, **event_args):
    self.card_compFile.visible = not(self.card_compFile.visible)
    globals.selected_predictCompare = self.radio_button_function_predict.selected
  
  def radio_button_function_compare_clicked(self, **event_args):
    self.card_compFile.visible = not(self.card_compFile.visible)  
    globals.selected_predictCompare = self.radio_button_function_predict.selected

# plot selection links
  def deselect_all_links(self):
    for link in self.card_plotSelection.get_components():
      link.bold=False
      
  def link_plot_overview_click(self, **event_args):
    self.deselect_all_links()
    self.link_plot_overview.bold = True
  def link_plot_freq_click(self, **event_args):
    self.deselect_all_links()
    self.link_plot_freq.bold = True

  def link_plot_comp_click(self, **event_args):
    self.deselect_all_links()
    self.link_plot_comp.bold = True

  def link_plot_pos_click(self, **event_args):
    self.deselect_all_links()
    self.link_plot_pos.bold = True

  def link_plot_cog_click(self, **event_args):
    self.deselect_all_links()
    self.link_plot_cog.bold = True

  def link_link_click(self, **event_args):
    self.deselect_all_links()
    self.link_plot_link.bold = True
    
# dorpdowns
  def drop_down_compFile_change(self, **event_args):
    globals.selected_comparisonFilePath = self.drop_down_compFile.selected_value

  def check_box_compFile_show_change(self, **event_args):
    globals.selected_showComparisonData = self.check_box_compFile_show.checked

  def drop_down_year_change(self, **event_args):
    globals.selected_year = self.drop_down_year.selected_value

  def drop_down_component_change(self, **event_args):
   globals.selected_component = self.drop_down_component.selected_value
  
# legacy handlers
  def text_box_freq_max_pressed_enter(self, **event_args):
    """This method is called when the user presses Enter in this text box"""
    pass




      




    

