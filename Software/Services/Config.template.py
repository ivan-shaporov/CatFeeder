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

# FoodCycleProfile = [(6.8, 1), (5, .5), (6.4, -1), (4, -.5)] # low load
FoodCycleProfile = [(1, 1), (6.5, 1), (5, .5), (1, -1), (5, -1), (4, -.5)]
FoodPourDelay = 1

VideoLocation = '/home/pi/CatFeeder'
VideoName = 'last'
VideoDuration = 30

LightDuration = 140.0
