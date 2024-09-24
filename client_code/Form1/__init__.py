from ._anvil_designer import Form1Template
from anvil import *
import anvil.server

from ..input import input
from ..settings import settings
from ..analysis import analysis
from .. import globals

class Form1(Form1Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    
    self.content_panel.clear()
    self.content_panel.add_component(analysis(), full_width_row=True)
    self.deselect_all_links()
    self.link_analysis.role = 'selected'
# Topbar links
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

  def button_loadData_click(self, **event_args):
    """This method is called when the link is clicked"""
    globals.DB = anvil.server.call('create_database','dummy')
    globals.DB = anvil.server.call('addActiveFlags',globals.DB)
    globals.baureihe_years= anvil.server.call('get_baureihe_and_years',globals.DB)
    self.button_loadData.foreground = '#1EB980'
    self.link_analysis_click()

  def button_test_click(self, **event_args):
    print(globals.selected_BaureiheYears)
    print(globals.selected_buildstage)
    print(globals.selected_directions)
    print(globals.selected_clustering)
    print(globals.selected_frequencyRange)
    print(globals.selected_envelopeMethods)
    print(globals.selected_predictCompare)
    print(globals.selected_year)
    #self.content_panel.raise_event_on_children('x-updateResults')
    print(globals.settings_freqClusterIsHierarchical)