from ._anvil_designer import inputTemplate
from anvil import *
import anvil.server
from .. import globals

class input(inputTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    # Any code you write here will run before the form opens.
    self.dropDown_inputMethod.selected_value = globals.input_inputMethod
    self.text_box_fileName.text = globals.input_fileName
    self.text_box_path.text = globals.input_customPath
    self.dropDown_inputMethod_change()

  def dropDown_inputMethod_change(self, **event_args):
    if self.dropDown_inputMethod.selected_value == 'directory':
      self.label_3.text = 'Custom path'
      self.text_box_fileName.visible = False
      self.label_4.visible = False
      globals.input_inputMethod = self.dropDown_inputMethod.selected_value
    if self.dropDown_inputMethod.selected_value == 'previously generated database':
      self.label_3.text = 'Custom path'
      self.text_box_fileName.visible = True
      self.label_4.visible = True
      globals.input_inputMethod = self.dropDown_inputMethod.selected_value
    if self.dropDown_inputMethod.selected_value == 'external database':
      self.label_3.text = 'Custom input'
      self.text_box_fileName.visible = False
      self.label_4.visible = False
      globals.input_inputMethod = self.dropDown_inputMethod.selected_value

  def text_box_path_change(self, **event_args):
    globals.input_customPath = self.text_box_path.text

  def text_box_fileName_change(self, **event_args):
    globals.input_fileName = self.text_box_fileName.text

  def file_loader_1_change(self, file, **event_args):
    """This method is called when a new file is loaded into this FileLoader"""
    pass
    

