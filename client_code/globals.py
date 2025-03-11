DB = [{'Baureihe': 'load database',}]
baureihe_years = []

envelopGenerationMethods = ['Maximum', 'Minimum', 'Mean', '+3*std.dev.(99%)', '+2*std.dev.(95%)', '+1*std.dev.(68%)', '99th-percentile (each freq.)', '95th-percentile (each freq.)', '75th-percentile (each freq.)', 'Median (each freq.)', '99th-percentile (total)', '95th-percentile (total)', '75th-percentile (total)', 'Median (total)']

dataLoaded = False
clustered = False
clustered_pos = False
clustered_freq = False
clustered_comp = False

selected_BaureiheYears = set()
selected_directions = set()
selected_buildstage = set()
selected_clustering = set()
selected_frequencyRange = [72,2000]
selected_envelopeMethods = ['a', 'b']
selected_compare = False
selected_comparisonFile = None
selected_showComparisonData = False
selected_year = 0
selected_component = ''

settings_posClusterIsHierarchical = True
settings_posClusterNumber = 6
settings_freqClusterIsHierarchical = True
settings_freqSuperClusterNumber = 30
settings_freqSuperClusterNumberCustom = False
settings_freqDistanceMetricsHierarchical = ["seuclidean","euclidean","sqeuclidean","cityblock","minkowski","chebychev","cosine","correlation"]
settings_freqDistanceMetricHierarchical = settings_freqDistanceMetricsHierarchical[0]
settings_freqDistanceMetricsKMeans = ['correlation', 'seuclidean', 'sqeuclidean', 'cityblock', 'cosine']
settings_freqDistanceMetricKMeans = settings_freqDistanceMetricsKMeans[0]
settings_excludeMotor = False

input_inputMethod = 'directory'
input_customPath = '/home/anvil/dataDir/'
input_fileName ='fileName'

plots_component = []
plots_frequency = []
plots_position = []
plots_overview = []
plots_cog = []
plots_link = []
activePlot = 'overview'

positionDataForComponentsExist = False