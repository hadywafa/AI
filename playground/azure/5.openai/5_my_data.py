import os
import openai
import dotenv

dotenv.load_dotenv()

endpoint = os.environ.get("AZURE_OPENAI_ENDPOINT")
api_key = os.environ.get("AZURE_OPENAI_API_KEY")
deployment = os.environ.get("AZURE_OPEN_AI_DEPLOYMENT_ID")

client = openai.AzureOpenAI(
    base_url=f"{endpoint}/openai/deployments/{deployment}/extensions",
    api_key=api_key,
    api_version="2023-08-01-preview",
)

completion = client.chat.completions.create(
    model=deployment,
    messages=[
        {
            "role": "user",
            "content": "How is Azure machine learning different than Azure OpenAI?",
        },
    ],
    extra_body={
        "dataSources": [
            {
                "type": "AzureCognitiveSearch",
                "parameters": {
                    "endpoint": os.environ["AZURE_AI_SEARCH_ENDPOINT"],
                    "key": os.environ["AZURE_AI_SEARCH_API_KEY"],
                    "indexName": os.environ["AZURE_AI_SEARCH_INDEX"],
                },
            }
        ]
    },
)

print(completion.model_dump_json(indent=2))
