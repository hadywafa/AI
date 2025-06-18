# content moderator
# https://learn.microsoft.com/en-us/azure/ai-services/content-moderator/client-libraries?pivots=programming-language-python&tabs=visual-studio

import os.path
from pprint import pprint
import time
from io import BytesIO
from random import random
import uuid
from azure.core.credentials import AzureKeyCredential  # pip install azure-core

# from dotenv import load_dotenv
from pathlib import Path

from azure.cognitiveservices.vision.contentmoderator import (
    ContentModeratorClient,
)  # pip install azure-cognitiveservices-vision-contentmoderator
import azure.cognitiveservices.vision.contentmoderator.models  # pip install azure-cognitiveservices-vision-contentmoderator
from msrest.authentication import CognitiveServicesCredentials  # pip install msrest

# Load the environment variables from the .env file
# dotenv_path = Path('D:\\Sourcelens_trainings\\Azure_AI_102\\python_code\\My_python_code\\2_Content_Moderator\\creds_contentModerator.env')
# load_dotenv(dotenv_path=dotenv_path)


CONTENT_MODERATOR_ENDPOINT = "https://testcm1-bbs.cognitiveservices.azure.com/"
subscription_key = "3a5d266753c4407a8f35f5975308666a"

client = ContentModeratorClient(
    endpoint=CONTENT_MODERATOR_ENDPOINT,
    credentials=CognitiveServicesCredentials(subscription_key),
)


TEXT_FOLDER = os.path.join(os.path.dirname(os.path.realpath(__file__)), "text_files")

# TEXT_FOLDER = os.path.join(os.path.dirname(
#      os.path.realpath(__file__)), "2_Content_Moderator")

# Screen the input text: check for profanity,
# do autocorrect text, and check for personally identifying
# information (PII)
with open(os.path.join(TEXT_FOLDER, "ContentModerator.txt"), "rb") as text_fd:
    screen = client.text_moderation.screen_text(
        text_content_type="text/plain",
        text_content=text_fd,
        language="eng",
        autocorrect=True,
        pii=True,
    )
    # assert isinstance(screen, Screen )
    pprint(screen.as_dict())
