from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from msrest.authentication import CognitiveServicesCredentials
import os

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
Detect Brands - remote image url
This example detects common brands like logos and puts a bounding box around them.
"""
# print("Detect Brands - remote")
# # Get a URL with a brand logo
# remote_image_url = "https://blog.logomyway.com/wp-content/uploads/2020/07/top-brand-logos.jpg"

# # Select the visual feature(s) you want
# remote_image_features = ["brands"]
# # Call API with URL and features
# detect_brands_results_remote = computervision_client.analyze_image(remote_image_url, remote_image_features)

# if len(detect_brands_results_remote.brands) == 0:
#     print("No brands detected.")
# else:
#     for brand in detect_brands_results_remote.brands:
#         print("'{}' brand detected with confidence {:.1f}% at location {}, {}, {}, {}".format(
#             brand.name, brand.confidence * 100, brand.rectangle.x, brand.rectangle.x + brand.rectangle.w,
#             brand.rectangle.y, brand.rectangle.y + brand.rectangle.h))
# print()
"""
Detect Brands - local folder
This example detects common brands and puts a bounding box around them.
"""
print("===== Detect Brands - local =====")
# Open image file
local_image_path = ".\\Brand_Images\\s-l960.jpg"
local_image = open(local_image_path, "rb")
# Select the visual feature(s) you want
local_image_features = ["brands"]
# Call API with image and features
detect_brands_results_local = computervision_client.analyze_image_in_stream(
    local_image, local_image_features
)

# Print detection results with bounding box and confidence score
print("Detecting brands in local image: \n")
if len(detect_brands_results_local.brands) == 0:
    print("No brands detected.")
else:
    for brand in detect_brands_results_local.brands:
        print(
            "'{}' brand detected with confidence {:.1f}% at location {}, {}, {}, {}".format(
                brand.name,
                brand.confidence * 100,
                brand.rectangle.x,
                brand.rectangle.x + brand.rectangle.w,
                brand.rectangle.y,
                brand.rectangle.y + brand.rectangle.h,
            )
        )
print()
"""
END - Detect brands - local
"""
