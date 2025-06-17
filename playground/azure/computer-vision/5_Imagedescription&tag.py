from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials

from array import array
import os
from PIL import Image     # pip install pillow
import sys
import time

subscription_key = "61c48f73017b4f459aff90393d9a6011"
endpoint = "https://bbscvis1.cognitiveservices.azure.com/"


computervision_client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))

remote_image_url = "https://universe.nasa.gov/rails/active_storage/blobs/redirect/eyJfcmFpbHMiOnsibWVzc2FnZSI6IkJBaHBBdklCIiwiZXhwIjpudWxsLCJwdXIiOiJibG9iX2lkIn19--358fddd8d97c87255be0adfa918f14b1affcd437/BH_AccretionDisk_Sim_Stationary_1080.jpeg?disposition=inline"

print("********Describe an image - remote*********")
# Call ComputerVision API
description_results = computervision_client.describe_image(remote_image_url)

# Get the captions (descriptions) from the response, with confidence level
print("Description of remote image: ")
if len(description_results.captions) == 0:
    print("No description detected.")
else:
    for caption in description_results.captions:
        print("'{}' with confidence {:.2f}%".format(caption.text, caption.confidence * 100))
print()

print("===== Tag an image - remote =====")
# Call API with remote image
tags_result_remote = computervision_client.tag_image(remote_image_url)

# Print results with confidence score
print("Tags in the remote image: \n")
if len(tags_result_remote.tags) == 0:
    print("No tags detected.")
else:
    for tag in tags_result_remote.tags:
        print("'{}' with confidence {:.2f}%".format(tag.name, tag.confidence * 100))
print()
