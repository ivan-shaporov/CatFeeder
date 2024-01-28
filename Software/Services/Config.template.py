# Copy to Config.py

AppInsightsConnectionString = 'InstrumentationKey= <key> ;IngestionEndpoint=https://westus2-2.in.applicationinsights.azure.com/'

StorageAccount = 'catmonitor'
StorageContainer = 'catfeedervideo'

AzureCognitiveServiceUrl = 'https:// ...'
AzureCognitiveServiceKey = '<key>'
DetectionThreshold = 0.5

ReadSas = 'si=read& ... '
BlobUploadSas = 'si=blobUpload& ...'
UploadRetryCount = 3

# FoodCycleProfile = [(7.5, 1), (4, .55), (6.5, -1), (4, -.45)]  # low food
# FoodCycleProfile = [(6, 1), (5, .5), (6.5, -1), (3, -.35)]  # full food
FoodCycleProfile = [(8, 1), (5, .6), (6.5, -1), (4, -.45)]  # cold
FoodPourDelay = 3

VideoLocation = '/home/pi/CatFeeder'
VideoName = 'last'
VideoDuration = 30

LightDuration = 140.0
