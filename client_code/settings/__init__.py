from ._anvil_designer import settingsTemplate
from anvil import *
import anvil.server
from .. import globals

class settings(settingsTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    
    self.drop_down_distance_hierarchical.items = globals.settings_freqDistanceMetricsHierarchical
    self.drop_down_distance_kMeans.items = globals.settings_freqDistanceMetricsKMeans

    self.radio_button_pos_hierachical.selected = globals.settings_posClusterIsHierarchical
    self.radio_button_pos_kMeans.selected = not globals.settings_posClusterIsHierarchical
    self.text_box_pos_clusters.text = int(globals.settings_posClusterNumber)

    self.radio_button_freq_hierachical.selected = globals.settings_freqClusterIsHierarchical
    self.radio_button_freq_kMeans.selected = not globals.settings_freqClusterIsHierarchical
    self.text_box_freq_superClusters.text = globals.settings_freqSuperClusterNumber
    self.check_box_superClusters.checked = int(globals.settings_freqSuperClusterNumberCustom)
    self.text_box_freq_superClusters.enable = self.check_box_superClusters.checked

    self.drop_down_distance_hierarchical.selected_value = globals.settings_freqDistanceMetricHierarchical
    self.drop_down_distance_kMeans.selected_value = globals.settings_freqDistanceMetricKMeans

    self.check_box_excludeMotor.checked = globals.settings_excludeMotor

  def check_box_superClusters_change(self, **event_args):
    self.text_box_freq_superClusters.enabled = self.check_box_superClusters.checked

  def radio_button_pos_hierachical_clicked(self, **event_args):
    globals.settings_posClusterIsHierarchical = self.radio_button_pos_hierachical.selected

  def radio_button_pos_kMeans_clicked(self, **event_args):
    globals.settings_posClusterIsHierarchical = not self.radio_button_pos_kMeans.selected
    
  def radio_button_freq_hierachical_clicked(self, **event_args):
    globals.settings_freqClusterIsHierarchical = self.radio_button_freq_hierachical.selected

  def radio_button_freq_kMeans_clicked(self, **event_args):
    globals.settings_freqClusterIsHierarchical = not self.radio_button_freq_kMeans.selected