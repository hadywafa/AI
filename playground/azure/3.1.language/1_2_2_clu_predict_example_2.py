import os
from datetime import date
from typing import Any, Dict, List

from azure.core.credentials import AzureKeyCredential
from azure.ai.language.conversations import ConversationAnalysisClient

try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    pass

# 🔐 Load from environment
PREDICTION_ENDPOINT = os.getenv("AZURE_CONVERSATION_ENDPOINT")
PREDICTION_KEY = os.getenv("AZURE_CONVERSATION_KEY")
PROJECT_NAME = os.getenv("AZURE_CONVERSATION_PROJECT", "Menu")
DEPLOYMENT_NAME = os.getenv("AZURE_CONVERSATION_DEPLOYMENT", "production")


def get_client() -> ConversationAnalysisClient:
    if not PREDICTION_ENDPOINT or not PREDICTION_KEY:
        raise EnvironmentError("Azure endpoint or key missing.")
    return ConversationAnalysisClient(
        endpoint=PREDICTION_ENDPOINT,
        credential=AzureKeyCredential(PREDICTION_KEY),
    )


def analyze_query(client: ConversationAnalysisClient, query: str) -> Dict[str, Any]:
    with client:
        result = client.analyze_conversation(
            task={
                "kind": "Conversation",
                "analysisInput": {
                    "conversationItem": {
                        "participantId": "1",
                        "id": "1",
                        "modality": "text",
                        "language": "en",
                        "text": query,
                    },
                    "isLoggingEnabled": False,
                },
                "parameters": {
                    "projectName": PROJECT_NAME,
                    "deploymentName": DEPLOYMENT_NAME,
                    "verbose": True,
                },
            }
        )
    return result


def print_intent_and_entities(result: Dict[str, Any]) -> None:
    prediction = result["result"]["prediction"]
    print("\n🧠 Intent Prediction:")
    print(f"  • Top Intent: {prediction['topIntent']}")
    print(f"  • Category: {prediction['intents'][0]['category']}")
    print(f"  • Confidence: {prediction['intents'][0]['confidenceScore']:.2f}")

    print("\n🔍 Extracted Entities:")
    for entity in prediction["entities"]:
        print(
            f"  • {entity['category']} = {entity['text']} ({entity['confidenceScore']:.2f})"
        )


def handle_intent(intent: str, entities: List[Dict[str, Any]]) -> None:
    def get_entity(category: str) -> str:
        for entity in entities:
            if entity["category"] == category:
                return entity["text"]
        return ""

    if intent == "GetTime":
        location = get_entity("Location") or "local"
        print(get_time(location))

    elif intent == "GetDay":
        date_string = get_entity("Date") or date.today().strftime("%m/%d/%Y")
        print(get_day(date_string))

    elif intent == "GetDate":
        weekday = get_entity("Weekday") or "today"
        print(get_date(weekday))

    else:
        print(
            "🤖 Try asking: 'What’s the time?', 'What day is it?', or 'What’s the date?'."
        )


# 🧪 Example dummy handlers (replace with real logic)
def get_time(location: str) -> str:
    return f"The time in {location} is 12:34 PM."


def get_day(date_string: str) -> str:
    return f"{date_string} is a Tuesday."


def get_date(weekday: str) -> str:
    return f"The next {weekday} is on 06/20/2025."


def main():
    query = "Send an email to Anand"
    print(f"\n💬 Query: {query}")
    client = get_client()
    result = analyze_query(client, query)

    prediction = result["result"]["prediction"]
    top_intent = prediction["topIntent"]
    entities = prediction["entities"]

    print_intent_and_entities(result)
    handle_intent(top_intent, entities)


if __name__ == "__main__":
    main()
