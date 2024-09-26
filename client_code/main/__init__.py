from ._anvil_designer import mainTemplate
from anvil import *
import anvil.server


from ..input import input
from ..settings import settings
from ..analysis import analysis

from .. import globals


class main(mainTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.set_event_handler('x-dataNotUpToDate', self.dataNotUpToDate)
    
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
    
# side bar
  def button_loadDataBase_click(self, **event_args):
    """This method is called when the link is clicked"""
    notificationString = "Generating Database..."
    with Notification(notificationString):
      #anvil.server.call('create_database',globals.input_customPath)
      anvil.server.call('create_databaseTEST',globals.input_customPath)
      globals.baureihe_years = anvil.server.call('get_baureihe_and_years')
      self.button_loadDataBase.foreground = '#1EB980'
      self.link_analysis_click()

   
  def button_loadSelectedData_click(self, **event_args):
    self.button_loadSelectedData.foreground = '#1EB980'
    globals.dataLoaded = True
    self.content_panel.raise_event_on_children('x-updateDropDowns')
    
  def button_clusterData_click(self, **event_args):
    pass

  def button_displaySettings_click(self, **event_args):
    self.show_globals()

  def button_test_click(self, **event_args):
    print(anvil.server.call('test')) 
    #self.show_globals()
    #self.content_panel.raise_event_on_children('x-updateResults')
    
# others  
  def show_globals(self, **event_args):
    """
    Creates a notification window within the Anvil GUI containing all the values of the variables
    starting with selected_, settings_, and input_ within globals, displayed as a table.
    """
    # Retrieve all variables from globals that start with selected_, settings_, and input_
    variables = {name: value for name, value in globals.__dict__.items() if name.startswith(('selected_', 'settings_', 'input_'))}

    # Create the table string with headers
    table_string = "{:<50} {:<50}\n".format("Variable", "Value")

    # Add each variable and its value as a row in the table string
    for name, value in variables.items():
        table_string += "{:<60} {:<200}\n".format(name, str(value))
    # Display the notification window
    anvil.Notification(table_string, title="Global Variables", style="info", timeout=None).show()

  def dataNotUpToDate(self, **event_args):
    self.button_loadSelectedData.foreground = '#D64D47'
    globals.dataLoaded = False




