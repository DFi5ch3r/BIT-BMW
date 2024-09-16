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
    
    self.drop_down_year.items = anvil.server.call('get_unique_values',globals.DB,'Jahr')
    if self.drop_down_year.items: self.drop_down_year.selected_value = self.drop_down_year.items[-1]
    self.drop_down_component.items = anvil.server.call('get_unique_values',globals.DB,'Bauteil')
    self.drop_down_envelope_cluster.items = globals.envelopGenerationMethods
    self.drop_down_envelope_predict.items = globals.envelopGenerationMethods


  
  def radio_button_function_predict_change(self, **event_args):
    self.card_compFile.visible = not(self.card_compFile.visible)
    

  def radio_button_function_compare_clicked(self, **event_args):
    self.card_compFile.visible = not(self.card_compFile.visible)
    

  

