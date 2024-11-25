from ._anvil_designer import ItemTemplate2Template
from anvil import *
import anvil.server
from .. import globals


class ItemTemplate2(ItemTemplate2Template):
  def __init__(self, **properties):

    self.init_components(**properties)
    self.check_box_years.text = self.item['year']
    self.set_event_handler('x-toggleBox', self.toggleBox)

    if self.item['baureihe'] + '-.-' + self.item['year'] in globals.selected_BaureiheYears:
      self.check_box_years.checked = True
    else:
      self.check_box_years.checked = False

  def toggleBox(self, **event_args):
    self.check_box_years.checked=event_args['check']
    self.check_box_years_change()

  def check_box_years_change(self, **event_args):
    baureiheYear = self.item['baureihe'] + '-.-' + self.item['year']
    if self.check_box_years.checked:
      globals.selected_BaureiheYears.add(baureiheYear)
    else:
      globals.selected_BaureiheYears.discard(baureiheYear)
    self.parent.parent.parent.parent.parent.parent.parent.parent.raise_event('x-dataNotUpToDate')

    

