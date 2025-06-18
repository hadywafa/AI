import os.path
from pprint import pprint
import time
from io import BytesIO
from random import random
import uuid


from pathlib import Path

from azure.cognitiveservices.vision.contentmoderator import ContentModeratorClient
import azure.cognitiveservices.vision.contentmoderator.models
from msrest.authentication import CognitiveServicesCredentials

# Load the environment variables from the .env file
CONTENT_MODERATOR_ENDPOINT = "https://testcm1-bbs.cognitiveservices.azure.com/"
subscription_key = "3a5d266753c4407a8f35f5975308666a"

client = ContentModeratorClient(
    endpoint=CONTENT_MODERATOR_ENDPOINT,
    credentials=CognitiveServicesCredentials(subscription_key),
)

IMAGE_LIST = {
    "Sports": [
        "https://media.istockphoto.com/id/1550540247/photo/decision-thinking-and-asian-man-in-studio-with-glasses-questions-and-brainstorming-on-grey.jpg?s=2048x2048&w=is&k=20&c=AHKcPCjnl3pP21Kl9G8JA4N22lZLICuoyKlJTHU9D-E="
    ]
}

IMAGES_TO_MATCH = [
    "https://media.istockphoto.com/id/1550540247/photo/decision-thinking-and-asian-man-in-studio-with-glasses-questions-and-brainstorming-on-grey.jpg?s=2048x2048&w=is&k=20&c=AHKcPCjnl3pP21Kl9G8JA4N22lZLICuoyKlJTHU9D-E="
]

#
# Create list
#
print("Creating list MyList\n")
custom_list = client.list_management_image_lists.create(
    content_type="application/json",
    body={
        "name": "MyList",
        "description": "A sample list",
        "metadata": {"key_one": "Acceptable", "key_two": "Potentially racy"},
    },
)
print("List created:")
# assert isinstance(custom_list, ImageList)
pprint(custom_list.as_dict())
list_id = custom_list.id
time.sleep(5)


#
# Add images
#
def add_images(list_id, image_url, label):
    """Generic add_images from url and label."""
    print(
        "\nAdding image {} to list {} with label {}.".format(image_url, list_id, label)
    )
    try:
        added_image = client.list_management_image.add_image_url_input(
            list_id=list_id,
            content_type="application/json",
            data_representation="URL",
            value=image_url,
            label=label,
        )
    except Exception as err:
        # sample4 will fail
        print("Unable to add image to list: {}".format(err))
    else:
        # assert isinstance(added_image, Image)
        pprint(added_image.as_dict())
        return added_image


print("\nAdding images to list {}".format(list_id))
index = {}  # Keep an index url to id for later removal
for label, urls in IMAGE_LIST.items():
    for url in urls:
        image = add_images(list_id, url, label)
        if image:
            index[url] = image.content_id

#
# Match images against the image list.
#
for image_url in IMAGES_TO_MATCH:
    print("\nMatching image {} against list {}".format(image_url, list_id))
    match_result = client.image_moderation.match_url_input(
        content_type="application/json",
        list_id=list_id,
        data_representation="URL",
        value=image_url,
    )
    # assert isinstance(match_result, MatchResponse)
    print("Is match? {}".format(match_result.is_match))
    print("Complete match details:")
    pprint(match_result.as_dict())

#
# Delete all images
#
print("\nDelete all images in the image list {}".format(list_id))
client.list_management_image.delete_all_images(list_id=list_id)

#
# Delete list
#
print("\nDelete the image list {}".format(list_id))
client.list_management_image_lists.delete(list_id=list_id)
