from ._anvil_designer import ItemTemplate2Template
from anvil import *
import anvil.server


class ItemTemplate2(ItemTemplate2Template):
  def __init__(self, **properties):

    self.init_components(**properties)
    self.check_box_years.text = self.item['year']
    
    self.set_event_handler('x-toggleBox', self.toggleBox)

  def toggleBox(self, **event_args):
    self.check_box_years.checked=event_args['check']

  def check_box_years_change(self, **event_args):
    """This method is called when this checkbox is checked or unchecked"""
    pass
 
