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
"""
END - Authenticate
"""

"""
OCR: Read File using the Read API, extract text - remote
This example will extract text in an image, then print results, line by line.
This API call can also extract handwriting style text (not shown).
"""
print("===== Read File - remote =====")
# Get an image with text
read_image_url = "https://learn.microsoft.com/azure/ai-services/computer-vision/media/quickstarts/presentation.png"

# Call API with URL and raw response (allows you to get the operation location)
read_response = computervision_client.read(read_image_url, raw=True)

# Get the operation location (URL with an ID at the end) from the response
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
END - Read File - remote
"""

print("End of Computer Vision quickstart.")
