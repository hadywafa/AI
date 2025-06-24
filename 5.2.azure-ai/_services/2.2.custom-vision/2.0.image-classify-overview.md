# 🧠 Azure AI Custom Vision – Build Your Own Vision Models

**Azure AI Custom Vision** enables you to build, train, deploy, and use **custom image classification** and **object detection models** without deep machine learning expertise.

Use it when **prebuilt models (like Azure AI Vision)** aren’t specific enough for your domain—e.g., identifying a product line, plant species, or medical images.

---

## 🧱 Architecture Overview

To use Custom Vision, you'll provision **two resources**:

| Resource Type              | Purpose                                               |
| -------------------------- | ----------------------------------------------------- |
| 🧠 **Training Resource**   | Used to upload data and train a model                 |
| 🎯 **Prediction Resource** | Used to deploy the trained model and make predictions |

🔄 You can train in one region and deploy predictions in another for scalability.

---

## 🌐 Accessing the Portal

Use the [Custom Vision Portal](https://www.customvision.ai/) to:

- Create projects (image classification or object detection)
- Upload and tag images
- Train models (multiclass or multilabel)
- Evaluate, test, and publish your model

✅ Portal is ideal for **getting started**, while the **SDK or REST API** supports automation and DevOps.

---

## 🎯 Classification Modes

| Mode           | Description                        | Example                                  |
| -------------- | ---------------------------------- | ---------------------------------------- |
| **Multiclass** | One image → one class label        | Classify fruit as either Apple or Banana |
| **Multilabel** | One image → multiple tags possible | Identify multiple landmarks in one photo |

---

## 🛠️ Train an Image Classification Model

You can train a model using:

| Method                | Best For                     |
| --------------------- | ---------------------------- |
| 🖥️ **Portal UI**      | Visual tagging & experiments |
| 📦 **SDK / REST API** | Automation / CI/CD           |

Portal Training Steps:

1. Create a **project** (choose classification + multiclass/multilabel)
2. Upload and tag **training images**
3. Click **Train**
4. Evaluate metrics (precision, recall, avg precision)
5. Click **Publish** to make model available for prediction

---

## 🤖 Predict with a Trained Model

You can send new images to the **published model** using:

- ✅ Python SDK
- ✅ .NET SDK
- ✅ REST API (via `curl`)
- ✅ Logic Apps / Power Automate

---

### 🐍 Python SDK Example

```python
from msrest.authentication import ApiKeyCredentials
from azure.cognitiveservices.vision.customvision.prediction import CustomVisionPredictionClient

# Authenticate prediction client
credentials = ApiKeyCredentials(
    in_headers={"Prediction-key": "<YOUR_PREDICTION_KEY>"}
)
prediction_client = CustomVisionPredictionClient(
    endpoint="<YOUR_PREDICTION_ENDPOINT>",
    credentials=credentials
)

# Load image data
with open("image.jpg", "rb") as img_file:
    image_data = img_file.read()

# Classify image
results = prediction_client.classify_image(
    project_id="<YOUR_PROJECT_ID>",
    published_name="<YOUR_PUBLISHED_MODEL_NAME>",
    image_data=image_data
)

# Output predictions
for prediction in results.predictions:
    if prediction.probability > 0.5:
        print(f"{prediction.tag_name}: {prediction.probability:.2%}")
```

---

### 💻 C# SDK Example

```csharp
using Microsoft.Azure.CognitiveServices.Vision.CustomVision.Prediction;
using Microsoft.Azure.CognitiveServices.Vision.CustomVision.Prediction.Models;
using System.IO;

var predictionKey = "<YOUR_PREDICTION_KEY>";
var endpoint = "<YOUR_PREDICTION_ENDPOINT>";
var projectId = Guid.Parse("<YOUR_PROJECT_ID>");
var publishedModelName = "<YOUR_PUBLISHED_MODEL_NAME>";

var credentials = new ApiKeyServiceClientCredentials(predictionKey);
var predictionClient = new CustomVisionPredictionClient(credentials)
{
    Endpoint = endpoint
};

using var stream = File.OpenRead("image.jpg");
var result = predictionClient.ClassifyImage(projectId, publishedModelName, stream);

foreach (var prediction in result.Predictions)
{
    if (prediction.Probability > 0.5)
        Console.WriteLine($"{prediction.TagName}: {prediction.Probability:P1}");
}
```

---

### 📡 Equivalent REST API (cURL)

```bash
curl -X POST "https://<your-prediction-endpoint>/customvision/v3.0/Prediction/<your-project-id>/classify/iterations/<your-model-name>/image" \
  -H "Prediction-Key: <YOUR_PREDICTION_KEY>" \
  -H "Content-Type: application/octet-stream" \
  --data-binary "@image.jpg"
```

📤 Response:

```json
{
  "id": "xxx",
  "project": "fruit-classifier",
  "predictions": [
    {
      "tagName": "Banana",
      "probability": 0.94
    },
    {
      "tagName": "Apple",
      "probability": 0.05
    }
  ]
}
```

---

## 🔐 Authentication Options

| Type               | Use Case               |
| ------------------ | ---------------------- |
| 🔑 API Key         | Easy, fast for testing |
| 🪪 Entra ID (OAuth) | Secure, production use |

Each **training** and **prediction** resource has **separate keys** and **endpoints**.

---

## ✅ Summary Table

| Step                           | Tool / Method                          |
| ------------------------------ | -------------------------------------- |
| Create project + upload images | Custom Vision Portal                   |
| Train model                    | Portal / SDK / REST API                |
| Publish model                  | Portal or `publish_iteration()` method |
| Classify new image             | Python/C#/REST SDK                     |

---

## 🧠 Common Real-World Scenarios

| Use Case                          | Type                     | Mode       |
| --------------------------------- | ------------------------ | ---------- |
| Classify fruits in images         | Image classification     | Multiclass |
| Tag multiple objects in a product | Image classification     | Multilabel |
| Detect objects and bounding boxes | Object detection project | N/A        |
