import os
from openai import AzureOpenAI

client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version="2023-12-01-preview",
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
)

deployment_name = "REPLACE_WITH_YOUR_DEPLOYMENT_NAME"  # This will correspond to the custom name you chose for your deployment when you deployed a model. Use a gpt-35-turbo-instruct deployment.

# Send a completion call to generate an answer
print("Sending a test completion job")
start_phrase = "Write a tagline for an ice cream shop. "  # Create a python code
response = client.completions.create(
    model=deployment_name, prompt=start_phrase, max_tokens=10
)
print(start_phrase + response.choices[0].text)
