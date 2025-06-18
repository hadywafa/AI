import os.path
from pprint import pprint
import time
from io import BytesIO
from random import random
import uuid

# from dotenv import load_dotenv
from pathlib import Path

from azure.cognitiveservices.vision.contentmoderator import ContentModeratorClient
import azure.cognitiveservices.vision.contentmoderator.models
from msrest.authentication import CognitiveServicesCredentials

# Load the environment variables from the .env file
# dotenv_path = Path('D:\\Sourcelens_trainings\\Azure_AI_102\\python_code\\My_python_code\\2_Content_Moderator\\creds_contentModerator.env')
# load_dotenv(dotenv_path=dotenv_path)


CONTENT_MODERATOR_ENDPOINT = "https://testcm1-bbs.cognitiveservices.azure.com/"
subscription_key = "3a5d266753c4407a8f35f5975308666a"


client = ContentModeratorClient(
    endpoint=CONTENT_MODERATOR_ENDPOINT,
    credentials=CognitiveServicesCredentials(subscription_key),
)

IMAGE_LIST = [
    # "https://moderatorsampleimages.blob.core.windows.net/samples/sample5.png",
    "https://content.api.news/v3/images/bin/756692568a236c94619b202e9b68687a?width=650",
    "https://mockuptree.com/wp-content/uploads/edd/2022/01/minecraft-text-effect-psd.jpg",
    "https://media.istockphoto.com/id/1550540247/photo/decision-thinking-and-asian-man-in-studio-with-glasses-questions-and-brainstorming-on-grey.jpg?s=2048x2048&w=is&k=20&c=AHKcPCjnl3pP21Kl9G8JA4N22lZLICuoyKlJTHU9D-E=",
]


for image_url in IMAGE_LIST:
    print("\nEvaluate image {}".format(image_url))
    # Iterate through image list

    # Detect adult and racy content
    print("\nEvaluate for adult and racy content.")
    evaluation = client.image_moderation.evaluate_url_input(
        content_type="application/json",
        cache_image=True,
        data_representation="URL",
        value=image_url,
    )
    # assert isinstance(evaluation, Evaluate)
    pprint(evaluation.as_dict())

    # extract text
    print("\nDetect and extract text.")
    evaluation = client.image_moderation.ocr_url_input(
        language="eng",
        content_type="application/json",
        data_representation="URL",
        value=image_url,
        cache_image=True,
    )
    # assert isinstance(evaluation, OCR)
    pprint(evaluation.as_dict())

    # detect faces and returns coordinates of bounding boxes
    print("\nDetect faces.")
    evaluation = client.image_moderation.find_faces_url_input(
        content_type="application/json",
        cache_image=True,
        data_representation="URL",
        value=image_url,
    )
    # assert isinstance(evaluation, FoundFaces)
    pprint(evaluation.as_dict())
