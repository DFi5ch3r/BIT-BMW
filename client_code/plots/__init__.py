from ._anvil_designer import plotsTemplate
from anvil import *
import anvil.server
import plotly.graph_objects as go

class plots(plotsTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

  def button_plotPrep_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.fig1, self.fig2, self.fig3 = anvil.server.call('prepPlots')
