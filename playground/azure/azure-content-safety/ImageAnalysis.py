# Azure AI ContentSafety Image Analysis
# pip install azure-ai-contentsafety


def analyze_image():
    # [START analyze_image]

    import os
    from azure.ai.contentsafety import (
        ContentSafetyClient,
    )  # pip install azure-ai-contentsafety
    from azure.ai.contentsafety.models import ImageCategory
    from azure.core.credentials import AzureKeyCredential
    from azure.core.exceptions import HttpResponseError
    from azure.ai.contentsafety.models import AnalyzeImageOptions, ImageData

    key = "f7324ffadc7e4da0b5b253230a44a849"
    endpoint = "https://azure-content-safety-demo-345.cognitiveservices.azure.com/"
    image_path = os.path.abspath(
        os.path.join(
            os.path.abspath(__file__),
            "..",
            "./sample_data/756692568a236c94619b202e9b68687a.jpg",
        )
    )

    # Create a Content Safety client
    client = ContentSafetyClient(endpoint, AzureKeyCredential(key))

    # Build request
    with open(image_path, "rb") as file:
        request = AnalyzeImageOptions(image=ImageData(content=file.read()))

    # Analyze image
    try:
        response = client.analyze_image(request)
    except HttpResponseError as e:
        print("Analyze image failed.")
        if e.error:
            print(f"Error code: {e.error.code}")
            print(f"Error message: {e.error.message}")
            raise
        print(e)
        raise

    hate_result = next(
        item
        for item in response.categories_analysis
        if item.category == ImageCategory.HATE
    )
    self_harm_result = next(
        item
        for item in response.categories_analysis
        if item.category == ImageCategory.SELF_HARM
    )
    sexual_result = next(
        item
        for item in response.categories_analysis
        if item.category == ImageCategory.SEXUAL
    )
    violence_result = next(
        item
        for item in response.categories_analysis
        if item.category == ImageCategory.VIOLENCE
    )

    if hate_result:
        print(f"Hate severity: {hate_result.severity}")
    if self_harm_result:
        print(f"SelfHarm severity: {self_harm_result.severity}")
    if sexual_result:
        print(f"Sexual severity: {sexual_result.severity}")
    if violence_result:
        print(f"Violence severity: {violence_result.severity}")

    # [END analyze_image]


if __name__ == "__main__":
    analyze_image()
