from ._anvil_designer import inputTemplate
from anvil import *
import anvil.server

class input(inputTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

  def dropDown_inputMethod_change(self, **event_args):
    """This method is called when an item is selected"""
    if self.dropDown_inputMethod.selected_value == 'directory':
      self.label_3.text = 'Custom path'
      self.text_box_1.visible = True
      self.text_box_2.visible = False
      self.label_4.visible = False
    if self.dropDown_inputMethod.selected_value == 'previously generated database':
      self.label_3.text = 'Custom path'
      self.text_box_1.visible = True
      self.text_box_2.visible = True
      self.label_4.visible = True

    if self.dropDown_inputMethod.selected_value == 'external database':
      self.label_3.text = 'Custom input'
      self.text_box_1.visible = True
      self.text_box_2.visible = False
      self.label_4.visible = False
    pass

  def button_loadDB_click(self, **event_args):
    """This method is called when the button is clicked"""
    pass
