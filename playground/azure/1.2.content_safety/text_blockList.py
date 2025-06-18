import os
from typing import List, Optional
from azure.ai.contentsafety import ContentSafetyClient, BlocklistClient
from azure.ai.contentsafety.models import (
    AnalyzeTextOptions,
    TextBlocklist,
    TextBlocklistItem,
    AddOrUpdateTextBlocklistItemsOptions,
    RemoveTextBlocklistItemsOptions,
)
from azure.core.credentials import AzureKeyCredential
from azure.core.exceptions import HttpResponseError

# Optional: load from .env file (if using python-dotenv)
try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    pass

# Load from environment or .env
AZURE_CONTENT_SAFETY_KEY = os.getenv("AZURE_CONTENT_SAFETY_KEY")
AZURE_CONTENT_SAFETY_ENDPOINT = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
BLOCKLIST_NAME = "TestBlocklist"


def create_blocklist_client() -> BlocklistClient:
    if not AZURE_CONTENT_SAFETY_KEY or not AZURE_CONTENT_SAFETY_ENDPOINT:
        raise EnvironmentError("Azure Content Safety credentials not set.")

    return BlocklistClient(
        AZURE_CONTENT_SAFETY_ENDPOINT, AzureKeyCredential(AZURE_CONTENT_SAFETY_KEY)
    )


def create_content_safety_client() -> ContentSafetyClient:
    if not AZURE_CONTENT_SAFETY_KEY or not AZURE_CONTENT_SAFETY_ENDPOINT:
        raise EnvironmentError("Azure Content Safety credentials not set.")

    return ContentSafetyClient(
        AZURE_CONTENT_SAFETY_ENDPOINT, AzureKeyCredential(AZURE_CONTENT_SAFETY_KEY)
    )


def handle_error(prefix: str, e: HttpResponseError):
    print(f"\n{prefix} failed:")
    if e.error:
        print(f"Error code: {e.error.code}")
        print(f"Error message: {e.error.message}")
    else:
        print(e)
    raise


def create_or_update_text_blocklist(
    description: str = "Test blocklist management.",
) -> None:
    client = create_blocklist_client()
    try:
        blocklist = client.create_or_update_text_blocklist(
            blocklist_name=BLOCKLIST_NAME,
            options=TextBlocklist(
                blocklist_name=BLOCKLIST_NAME, description=description
            ),
        )
        print(f"\nCreated or updated blocklist: {blocklist.blocklist_name}")
    except HttpResponseError as e:
        handle_error("Create/Update blocklist", e)


def add_block_items(texts: List[str]) -> None:
    client = create_blocklist_client()
    items = [TextBlocklistItem(text=text) for text in texts]
    try:
        result = client.add_or_update_blocklist_items(
            blocklist_name=BLOCKLIST_NAME,
            options=AddOrUpdateTextBlocklistItemsOptions(blocklist_items=items),
        )
        print("\nAdded block items:")
        for item in result.blocklist_items:
            print(f"ID: {item.blocklist_item_id}, Text: {item.text}")
    except HttpResponseError as e:
        handle_error("Add block items", e)


def analyze_text_with_blocklists(text: str) -> None:
    client = create_content_safety_client()
    try:
        result = client.analyze_text(
            AnalyzeTextOptions(
                text=text, blocklist_names=[BLOCKLIST_NAME], halt_on_blocklist_hit=False
            )
        )
        if result.blocklists_match:
            print("\nBlocklist matches:")
            for match in result.blocklists_match:
                print(
                    f"Blocklist: {match.blocklist_name}, ID: {match.blocklist_item_id}, Text: {match.blocklist_item_text}"
                )
        else:
            print("\nNo blocklist matches.")
    except HttpResponseError as e:
        handle_error("Analyze text", e)


def list_text_blocklists() -> None:
    client = create_blocklist_client()
    try:
        blocklists = client.list_text_blocklists()
        print("\nAvailable blocklists:")
        for bl in blocklists:
            print(f"Name: {bl.blocklist_name}, Description: {bl.description}")
    except HttpResponseError as e:
        handle_error("List blocklists", e)


def get_text_blocklist() -> None:
    client = create_blocklist_client()
    try:
        blocklist = client.get_text_blocklist(blocklist_name=BLOCKLIST_NAME)
        print(
            f"\nBlocklist: {blocklist.blocklist_name}, Description: {blocklist.description}"
        )
    except HttpResponseError as e:
        handle_error("Get blocklist", e)


def list_block_items() -> None:
    client = create_blocklist_client()
    try:
        items = client.list_text_blocklist_items(blocklist_name=BLOCKLIST_NAME)
        print("\nBlock items:")
        for item in items:
            print(
                f"ID: {item.blocklist_item_id}, Text: {item.text}, Description: {item.description}"
            )
    except HttpResponseError as e:
        handle_error("List block items", e)


def get_block_item(text: str) -> Optional[str]:
    client = create_blocklist_client()
    try:
        result = client.add_or_update_blocklist_items(
            blocklist_name=BLOCKLIST_NAME,
            options=AddOrUpdateTextBlocklistItemsOptions(
                blocklist_items=[TextBlocklistItem(text=text)]
            ),
        )
        if result.blocklist_items:
            item_id = result.blocklist_items[0].blocklist_item_id
            item = client.get_text_blocklist_item(
                blocklist_name=BLOCKLIST_NAME, blocklist_item_id=item_id
            )
            print(
                f"\nFetched block item: ID: {item.blocklist_item_id}, Text: {item.text}"
            )
            return item.blocklist_item_id
    except HttpResponseError as e:
        handle_error("Get block item", e)
    return None


def remove_block_items_by_text(text: str) -> None:
    client = create_blocklist_client()
    try:
        result = client.add_or_update_blocklist_items(
            blocklist_name=BLOCKLIST_NAME,
            options=AddOrUpdateTextBlocklistItemsOptions(
                blocklist_items=[TextBlocklistItem(text=text)]
            ),
        )
        if result.blocklist_items:
            item_id = result.blocklist_items[0].blocklist_item_id
            client.remove_blocklist_items(
                blocklist_name=BLOCKLIST_NAME,
                options=RemoveTextBlocklistItemsOptions(blocklist_item_ids=[item_id]),
            )
            print(f"\nRemoved block item ID: {item_id}")
    except HttpResponseError as e:
        handle_error("Remove block item", e)


def delete_blocklist() -> None:
    client = create_blocklist_client()
    try:
        client.delete_text_blocklist(blocklist_name=BLOCKLIST_NAME)
        print(f"\nDeleted blocklist: {BLOCKLIST_NAME}")
    except HttpResponseError as e:
        handle_error("Delete blocklist", e)


if __name__ == "__main__":
    create_or_update_text_blocklist()
    add_block_items(["k*ll", "h*te"])
    analyze_text_with_blocklists("I h*te you and I want to k*ll you.")
    list_text_blocklists()
    get_text_blocklist()
    list_block_items()
    get_block_item("k*ll")
    remove_block_items_by_text("k*ll")
    delete_blocklist()
