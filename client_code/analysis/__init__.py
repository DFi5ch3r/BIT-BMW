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
    
    #initialise dropdowns
    self.drop_down_year.items = anvil.server.call('get_unique_values',globals.DB,'Jahr')
    if self.drop_down_year.items: self.drop_down_year.selected_value = self.drop_down_year.items[-1]
    self.drop_down_component.items = anvil.server.call('get_unique_values',globals.DB,'Bauteil')
    self.drop_down_envelope_cluster.items = globals.envelopGenerationMethods
    self.drop_down_envelope_predict.items = globals.envelopGenerationMethods

    #initialise checkbox globals
    if not globals.selected_buildstage:
      globals.selected_buildstage.add('Not found')
    if not globals.selected_direction:
      globals.selected_direction.add('-X')
      globals.selected_direction.add('-Y')
      globals.selected_direction.add('-Z')
      globals.selected_direction.add('+X')
      globals.selected_direction.add('+Y')
      globals.selected_direction.add('+Z')
    if not globals.selected_clustering:
      globals.selected_clustering.add('frequency')
      globals.selected_clustering.add('position')
      globals.selected_clustering.add('component')
   

  
  def radio_button_function_predict_change(self, **event_args):
    self.card_compFile.visible = not(self.card_compFile.visible)
    

  def radio_button_function_compare_clicked(self, **event_args):
    self.card_compFile.visible = not(self.card_compFile.visible)

  def check_box_BS_BS0_change(self, **event_args):
    if self.check_box_BS_BS0.checked:
      globals.selected_buildstage.add(self.check_box_BS_BS0.text)
    else:
      globals.selected_buildstage.discard(self.check_box_BS_BS0.text)

  def check_box_BS_BS1_change(self, **event_args):
      if self.check_box_BS_BS1.checked:
          globals.selected_buildstage.add(self.check_box_BS_BS1.text)
      else:
          globals.selected_buildstage.discard(self.check_box_BS_BS1.text)
  
  def check_box_BS_VS1_change(self, **event_args):
      if self.check_box_BS_VS1.checked:
          globals.selected_buildstage.add(self.check_box_BS_VS1.text)
      else:
          globals.selected_buildstage.discard(self.check_box_BS_VS1.text)
  
  def check_box_BS_VS2_change(self, **event_args):
      if self.check_box_BS_VS2.checked:
          globals.selected_buildstage.add(self.check_box_BS_VS2.text)
      else:
          globals.selected_buildstage.discard(self.check_box_BS_VS2.text)
  
  def check_box_BS_FB_change(self, **event_args):
      if self.check_box_BS_FB.checked:
          globals.selected_buildstage.add(self.check_box_BS_FB.text)
      else:
          globals.selected_buildstage.discard(self.check_box_BS_FB.text)
  
  def check_box_BS_KEX_change(self, **event_args):
      if self.check_box_BS_KEX.checked:
          globals.selected_buildstage.add(self.check_box_BS_KEX.text)
      else:
          globals.selected_buildstage.discard(self.check_box_BS_KEX.text)
  
  def check_box_BS_AS_change(self, **event_args):
      if self.check_box_BS_AS.checked:
          globals.selected_buildstage.add(self.check_box_BS_AS.text)
      else:
          globals.selected_buildstage.discard(self.check_box_BS_AS.text)
  
  def check_box_BS_SERIE_change(self, **event_args):
      if self.check_box_BS_SERIE.checked:
          globals.selected_buildstage.add(self.check_box_BS_SERIE.text)
      else:
          globals.selected_buildstage.discard(self.check_box_BS_SERIE.text)
  
  def check_box_BS_notFound_change(self, **event_args):
      if self.check_box_BS_notFound.checked:
          globals.selected_buildstage.add(self.check_box_BS_notFound.text)
      else:
          globals.selected_buildstage.discard(self.check_box_BS_notFound.text)    



