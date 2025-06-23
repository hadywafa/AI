import os
from azure.ai.vision import VisionClient
from azure.core.credentials import AzureKeyCredential
from dotenv import load_dotenv

# ✅ Load environment variables
load_dotenv()

# 🔐 Load config from environment
AZURE_AI_SERVICE_ENDPOINT = os.getenv("AZURE_AI_SERVICE_ENDPOINT")
AZURE_AI_SERVICE_KEY = os.getenv("AZURE_AI_SERVICE_KEY")

client = VisionClient(
    "https://myVisionDemo.cognitiveservices.azure.com/",
    AzureKeyCredential("<your-key>"),
)
result = client.read("https://example.com/text.jpg")
print(result.content)
