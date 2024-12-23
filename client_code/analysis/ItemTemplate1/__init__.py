from ._anvil_designer import ItemTemplate1Template
from anvil import *
import anvil.server
from .. import globals

class ItemTemplate1(ItemTemplate1Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.check_box_type.text = self.item['Baureihe']
    self.repeating_panel_1.items = self.item['Years']

    for br in globals.selected_BaureiheYears:
      if self.check_box_type.text in br:
        self.check_box_type.checked = True
        break


  def button_expandYears_click(self, **event_args):
    self.repeating_panel_1.visible = not(self.repeating_panel_1.visible)


  def check_box_type_change(self, **event_args):
    self.repeating_panel_1.raise_event_on_children('x-toggleBox',check = self.check_box_type.checked)
    self.parent.parent.parent.parent.parent.raise_event('x-dataNotUpToDate')
