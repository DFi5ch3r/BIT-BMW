from ._anvil_designer import analysisTemplate
from anvil import *
import anvil.server
from .. import globals


class analysis(analysisTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    self.repeating_panel_1.items =  globals.baureihe_years
    # Any code you write here will run before the form opens.

  def outlined_button_1_click(self, **event_args):
   pass