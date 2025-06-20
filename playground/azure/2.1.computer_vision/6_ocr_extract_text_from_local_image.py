from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from msrest.authentication import CognitiveServicesCredentials

import os
import time

"""
Authenticate
Authenticates your credentials and creates a client.
"""

try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    pass


AZURE_VISION_ENDPOINT = os.getenv("AZURE_VISION_ENDPOINT")
AZURE_VISION_KEY = os.getenv("AZURE_VISION_KEY")

if not AZURE_VISION_ENDPOINT or not AZURE_VISION_KEY:
    raise EnvironmentError("Azure Vision endpoint or key is missing.")


computervision_client = ComputerVisionClient(
    AZURE_VISION_ENDPOINT, CognitiveServicesCredentials(AZURE_VISION_KEY)
)

# Location to your image
local_image = open(".\\Handwritten_Notes\\20240201_201437_1.jpg", "rb")

# Call API
read_response = computervision_client.read_in_stream(local_image, raw=True)


read_operation_location = read_response.headers["Operation-Location"]
# Grab the ID from the URL
operation_id = read_operation_location.split("/")[-1]

# Call the "GET" API and wait for it to retrieve the results
while True:
    read_result = computervision_client.get_read_result(operation_id)
    if read_result.status not in ["notStarted", "running"]:
        break
    time.sleep(1)

# Print the detected text, line by line
if read_result.status == OperationStatusCodes.succeeded:
    for text_result in read_result.analyze_result.read_results:
        for line in text_result.lines:
            print(line.text)
            print(line.bounding_box)
print()
"""
END - Read File - local
"""
