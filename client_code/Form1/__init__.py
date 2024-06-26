from ._anvil_designer import Form1Template
from anvil import *
import anvil.server

from ..input import input
from ..settings import settings
from ..analysis import analysis


class Form1(Form1Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

# Sidebar links
  def deselect_all_links(self):
    """Reset all the roles on the navbar links."""
    for link in self.link_input, self.link_settings, self.link_analysis:
      link.role = ''
      
  def link_input_click(self, **event_args):
    """This method is called when the link is clicked"""
    self.content_panel.clear()
    self.content_panel.add_component(input())
    self.deselect_all_links()
    self.link_input.role = 'selected'

  def link_settings_click(self, **event_args):
    """This method is called when the link is clicked"""
    self.content_panel.clear()
    self.content_panel.add_component(settings())
    self.deselect_all_links()
    self.link_settings.role = 'selected'

  def link_analysis_click(self, **event_args):
    """This method is called when the link is clicked"""
    self.content_panel.clear()
    self.content_panel.add_component(analysis())
    self.deselect_all_links()
    self.link_analysis.role = 'selected'

