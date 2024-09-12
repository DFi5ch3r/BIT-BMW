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
    # Any code you write here will run before the form opens.

  def radio_button_function_predict_change(self, **event_args):
    self.card_compFile.visible = not(self.card_compFile.visible)
    pass

  def radio_button_function_compare_clicked(self, **event_args):
    self.card_compFile.visible = not(self.card_compFile.visible)
    pass

  

