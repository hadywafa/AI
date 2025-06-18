from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential

endpoint = "https://langsvcbbs1.cognitiveservices.azure.com/"
key = "401ee05be18e4971bc0ed2060677b12a"


# Authenticate the client using your key and endpoint.
def authenticate_client():
    ta_credential = AzureKeyCredential(key)
    text_analytics_client = TextAnalyticsClient(
        endpoint=endpoint, credential=ta_credential
    )
    return text_analytics_client


client = authenticate_client()


# Example function for recognizing entities and providing a link to an online data source.
def entity_linking_example(client):
    try:
        documents = [
            """Entity linking is one of the features offered by Azure AI Language, 
                     a collection of machine learning and AI algorithms in the cloud for developing intelligent applications that involve written language. 
                     Entity linking identifies and disambiguates the identity of entities found in text."""
        ]
        result = client.recognize_linked_entities(documents=documents)[0]

        print("Linked Entities:\n")
        for entity in result.entities:
            print(
                "\tName: ",
                entity.name,
                "\tId: ",
                entity.data_source_entity_id,
                "\tUrl: ",
                entity.url,
                "\n\tData Source: ",
                entity.data_source,
            )
            print("\tMatches:")
            for match in entity.matches:
                print("\t\tText:", match.text)
                print("\t\tConfidence Score: {0:.2f}".format(match.confidence_score))
                print("\t\tOffset: {}".format(match.offset))
                print("\t\tLength: {}".format(match.length))

    except Exception as err:
        print("Encountered exception. {}".format(err))


entity_linking_example(client)
