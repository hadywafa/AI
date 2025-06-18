# Computer vision detect landmarks
import os
from azure.cognitiveservices.vision.computervision import (
    ComputerVisionClient,
)
from msrest.authentication import CognitiveServicesCredentials

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

IMAGES = [
    "https://images.unsplash.com/photo-1564507592333-c60657eea523?q=80&w=2071&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
    "https://lh3.googleusercontent.com/p/AF1QipMHftgSCBlvyjxYphi4gLqDC_62WWvZvyy1EBuh=s1360-w1360-h1020",
    "https://assets.editorial.aetnd.com/uploads/2015/02/topic-golden-gate-bridge-gettyimages-177770941.jpg?width=1920&height=960&crop=1920%3A960%2Csmart&quality=75&auto=webp",
    "https://st.depositphotos.com/1759109/1331/i/450/depositphotos_13315503-stock-photo-tower-bridge-at-dusk.jpg",
    "https://images.unsplash.com/photo-1599676603816-0f92b2d713d2?q=80&w=1000&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8M3x8dG93ZXIlMjBicmlkZ2V8ZW58MHx8MHx8fDA%3D",
]

# Call API with content type (landmarks) and URL
for image_url in IMAGES:
    detect_domain_results_landmarks = computervision_client.analyze_image_by_domain(
        "landmarks", image_url
    )
    print("###### Computer Vision - Domain specific content - Landmarks #######")
    print("Landmarks in the remote image:")
    if len(detect_domain_results_landmarks.result["landmarks"]) == 0:
        print("No landmarks detected.")
    else:
        for landmark in detect_domain_results_landmarks.result["landmarks"]:
            print(landmark["name"])
