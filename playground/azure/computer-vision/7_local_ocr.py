from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials

from array import array
import os
from PIL import Image
import sys
import time
import requests

'''
Authenticate
Authenticates your credentials and creates a client.
'''
subscription_key = "61c48f73017b4f459aff90393d9a6011"
endpoint = "https://bbscvis1.cognitiveservices.azure.com/"


computervision_client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))

# Location to your image
local_image = open('.\\Handwritten_Notes\\20240201_201437_1.jpg', "rb")

# Call API
read_response = computervision_client.read_in_stream(local_image, raw=True)


read_operation_location = read_response.headers["Operation-Location"]
# Grab the ID from the URL
operation_id = read_operation_location.split("/")[-1]

# Call the "GET" API and wait for it to retrieve the results 
while True:
    read_result = computervision_client.get_read_result(operation_id)
    if read_result.status not in ['notStarted', 'running']:
        break
    time.sleep(1)

# Print the detected text, line by line
if read_result.status == OperationStatusCodes.succeeded:
    for text_result in read_result.analyze_result.read_results:
        for line in text_result.lines:
            print(line.text)
            print(line.bounding_box)
print()
'''
END - Read File - local
'''





