from azure.core.credentials import AzureKeyCredential
from azure.ai.language.conversations.authoring import ConversationAuthoringClient
from azure.core.polling import LROPoller
from azure.core.exceptions import HttpResponseError

endpoint = "https://langsvcbbs1.cognitiveservices.azure.com/"
credential = AzureKeyCredential("401ee05be18e4971bc0ed2060677b12a")

client = ConversationAuthoringClient(endpoint, credential)

project_name = "Menu"

# Define our project assets and import. In practice this would most often be read from a file.
import_data = {
    "projectFileVersion": "2022-05-01",
    "metadata": {
        "projectName": project_name,
        "projectKind": "Conversation",
        "multilingual": True,
        "language": "en",
    },
    "assets": {
        "projectKind": "Conversation",
        "entities": [
            {
                "category": "Contact",
                "compositionSetting": "combineComponents",
                "prebuilts": [
                    {
                        "category": "Person.Name",
                    },
                ],
                # ... more entities.
            }
        ],
        "intents": [
            {
                "category": "Send",
            },
            # ... more intents.
        ],
        "utterances": [
            {
                "text": "Send an email to Johnson",
                "language": "en",
                "intent": "Send",
                "entities": [
                    {
                        "category": "Contact",
                        "offset": 17,
                        "length": 7,
                    },
                ],
            },
            {
                "text": "Send Kathy a calendar invite",
                "language": "en",
                "intent": "Send",
                "entities": [
                    {
                        "category": "Contact",
                        "offset": 5,
                        "length": 5,
                    },
                ],
            },
                        {
                "text": "Send Chali a calendar invite",
                "language": "en",
                "intent": "Send",
                "entities": [
                    {
                        "category": "Contact",
                        "offset": 5,
                        "length": 5,
                    },
                ],
            },
                        {
                "text": "Send Annas a calendar invite",
                "language": "en",
                "intent": "Send",
                "entities": [
                    {
                        "category": "Contact",
                        "offset": 5,
                        "length": 5,
                    },
                ],
            },
                        {
                "text": "Send Benny a calendar invite",
                "language": "en",
                "intent": "Send",
                "entities": [
                    {
                        "category": "Contact",
                        "offset": 5,
                        "length": 5,
                    },
                ],
            },
                        {
                "text": "Send Einna a calendar invite",
                "language": "en",
                "intent": "Send",
                "entities": [
                    {
                        "category": "Contact",
                        "offset": 5,
                        "length": 5,
                    },
                ],
            },
                        {
                "text": "Send Adian a calendar invite",
                "language": "en",
                "intent": "Send",
                "entities": [
                    {
                        "category": "Contact",
                        "offset": 5,
                        "length": 5,
                    },
                ],
            },
                        {
                "text": "Send Zassi a calendar invite",
                "language": "en",
                "intent": "Send",
                "entities": [
                    {
                        "category": "Contact",
                        "offset": 5,
                        "length": 5,
                    },
                ],
            },
                        {
                "text": "Send Saide a calendar invite",
                "language": "en",
                "intent": "Send",
                "entities": [
                    {
                        "category": "Contact",
                        "offset": 5,
                        "length": 5,
                    },
                ],
            },
                        {
                "text": "Send Denni a calendar invite",
                "language": "en",
                "intent": "Send",
                "entities": [
                    {
                        "category": "Contact",
                        "offset": 5,
                        "length": 5,
                    },
                ],
            },
                        {
                "text": "Send Donna a calendar invite",
                "language": "en",
                "intent": "Send",
                "entities": [
                    {
                        "category": "Contact",
                        "offset": 5,
                        "length": 5,
                    },
                ],
            },
                        {
                "text": "Send Chahi a calendar invite",
                "language": "en",
                "intent": "Send",
                "entities": [
                    {
                        "category": "Contact",
                        "offset": 5,
                        "length": 5,
                    },
                ],
            },
                        {
                "text": "Send Cathi a calendar invite",
                "language": "en",
                "intent": "Send",
                "entities": [
                    {
                        "category": "Contact",
                        "offset": 5,
                        "length": 5,
                    },
                ],
            },
                        {
                "text": "Send Junan a calendar invite",
                "language": "en",
                "intent": "Send",
                "entities": [
                    {
                        "category": "Contact",
                        "offset": 5,
                        "length": 5,
                    },
                ],
            },
                        {
                "text": "Send Ninay a calendar invite",
                "language": "en",
                "intent": "Send",
                "entities": [
                    {
                        "category": "Contact",
                        "offset": 5,
                        "length": 5,
                    },
                ],
            },
                        {
                "text": "Send Tijos a calendar invite",
                "language": "en",
                "intent": "Send",
                "entities": [
                    {
                        "category": "Contact",
                        "offset": 5,
                        "length": 5,
                    },
                ],
            },
                        {
                "text": "Send Lason a calendar invite",
                "language": "en",
                "intent": "Send",
                "entities": [
                    {
                        "category": "Contact",
                        "offset": 5,
                        "length": 5,
                    },
                ],
            },
                        {
                "text": "Send Goege a calendar invite",
                "language": "en",
                "intent": "Send",
                "entities": [
                    {
                        "category": "Contact",
                        "offset": 5,
                        "length": 5,
                    },
                ],
            },
                        {
                "text": "Send Aksah a calendar invite",
                "language": "en",
                "intent": "Send",
                "entities": [
                    {
                        "category": "Contact",
                        "offset": 5,
                        "length": 5,
                    },
                ],
            },
                        {
                "text": "Send Joshp a calendar invite",
                "language": "en",
                "intent": "Send",
                "entities": [
                    {
                        "category": "Contact",
                        "offset": 5,
                        "length": 5,
                    },
                ],
            },

            # ... more utterances.
        ],
    },
    "stringIndexType": "Utf16CodeUnit",
}

try:
    import_operation = client.begin_import_project(project_name, import_data)
    import_operation.wait()
    print("Import complete")
except HttpResponseError as e:
    print(f"Import failed: {e}")

# Train the model.
train_data = {
    "modelLabel": "Sample5",
    "trainingMode": "standard",
}

try:
    print(f"Training project {project_name}...")
    train_operation = client.begin_train(project_name, train_data)
    train_operation.wait()
    print("Training complete")
except HttpResponseError as e:
    print(f"Training failed: {e}")

# Deploy the model.
deploy_data = {
    "trainedModelLabel": "Sample5",
}

try:
    print(f"Deploying project {project_name} to production...")
    deploy_operation = client.begin_deploy_project(project_name, "production", deploy_data)
    deploy_operation.wait()
    print("Deployment complete")
except HttpResponseError as e:
    print(f"Deployment failed: {e}")
