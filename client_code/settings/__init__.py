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
    self.text_box_pos_clusters.text = globals.settings_posClusterNumber

    self.radio_button_freq_hierachical.selected = globals.settings_freqClusterIsHierarchical
    self.radio_button_freq_kMeans.selected = not globals.settings_freqClusterIsHierarchical
    self.text_box_freq_superClusters.text = globals.settings_freqSuperClusterNumber
    self.check_box_superClusters.checked = globals.settings_freqSuperClusterNumberCustom
    self.text_box_freq_superClusters.text = globals.settings_freqSuperClusterNumber
    self.text_box_freq_superClusters.enabled = globals.settings_freqSuperClusterNumberCustom
    
    self.drop_down_distance_hierarchical.selected_value = globals.settings_freqDistanceMetricHierarchical
    self.drop_down_distance_kMeans.selected_value = globals.settings_freqDistanceMetricKMeans
    
    self.check_box_excludeMotor.checked = globals.settings_excludeMotor


  def check_box_superClusters_change(self, **event_args):
    self.text_box_freq_superClusters.enabled = self.check_box_superClusters.checked
    globals.settings_freqSuperClusterNumberCustom = self.check_box_superClusters.checked
    self.parent.parent.raise_event('x-clusterNotUpToDate')
    
  def radio_button_pos_hierachical_clicked(self, **event_args):
    globals.settings_posClusterIsHierarchical = self.radio_button_pos_hierachical.selected
    self.parent.parent.raise_event('x-clusterNotUpToDate')

  def radio_button_pos_kMeans_clicked(self, **event_args):
    globals.settings_posClusterIsHierarchical = not self.radio_button_pos_kMeans.selected
    self.parent.parent.raise_event('x-clusterNotUpToDate')
    
  def radio_button_freq_hierachical_clicked(self, **event_args):
    globals.settings_freqClusterIsHierarchical = self.radio_button_freq_hierachical.selected
    self.parent.parent.raise_event('x-clusterNotUpToDate')

  def radio_button_freq_kMeans_clicked(self, **event_args):
    globals.settings_freqClusterIsHierarchical = not self.radio_button_freq_kMeans.selected
    self.parent.parent.raise_event('x-clusterNotUpToDate')

  def text_box_pos_clusters_change(self, **event_args):
     globals.settings_posClusterNumber = int(self.text_box_pos_clusters.text)
     self.parent.parent.raise_event('x-clusterNotUpToDate')

  def text_box_freq_superClusters_change(self, **event_args):
    globals.settings_freqSuperClusterNumber = int(self.text_box_freq_superClusters.text)
    self.parent.parent.raise_event('x-clusterNotUpToDate')

  def check_box_excludeMotor_change(self, **event_args):
    globals.settings_excludeMotor = self.check_box_excludeMotor.checked
    self.parent.parent.raise_event('x-dataNotUpToDate')

  def drop_down_distance_hierarchical_change(self, **event_args):
    globals.settings_freqDistanceMetricHierarchical = self.drop_down_distance_hierarchical.selected_value
    self.parent.parent.raise_event('x-clusterNotUpToDate')

  def drop_down_distance_kMeans_change(self, **event_args):
    globals.settings_freqDistanceMetricKMeans = self.drop_down_distance_kMeans.selected_value
    self.parent.parent.raise_event('x-clusterNotUpToDate')
