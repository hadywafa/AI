# 🧠 How to Access Azure AI Services (From Beginner to Pro)

## 🌱 What Are Azure AI Services?

**Azure AI Services** are Microsoft’s prebuilt cloud APIs for common AI tasks — no machine learning skills needed.

### 🔧 What can they do?

| Category          | Services                             | Use Cases                        |
| ----------------- | ------------------------------------ | -------------------------------- |
| 👁️ Vision         | Image tagging, OCR, object detection | Read signs, analyze photos       |
| 🗣️ Speech         | Text-to-speech, speech-to-text       | Voice assistants, captions       |
| 🌍 Language       | Sentiment, key phrases, NER          | Analyze documents, chat logs     |
| 🌐 Translator     | Real-time translation                | Global apps, cross-language chat |
| 🤖 OpenAI         | GPT-4, ChatGPT, embeddings           | Chatbots, summarization, RAG     |
| 🛡️ Content Safety | Detect harmful content               | Moderate AI output & user input  |

---

## 🏗️ 3 Ways to Access Azure AI Services

Azure now provides **three ways** to provision AI services depending on your needs:

| Method                                             | Description                                                     | Best For                      | Free Tier |
| -------------------------------------------------- | --------------------------------------------------------------- | ----------------------------- | --------- |
| 1️⃣ **Standalone Resource**                         | Single AI API (e.g., just Vision or just Translator)            | Beginners, free testing       | ✅ Yes    |
| 2️⃣ **Multi-Service Resource** (`kind: AIServices`) | All AI APIs with one key/endpoint                               | Real apps using many services | ❌ No     |
| 3️⃣ **AI Foundry Project + Hub**                    | Full development platform incl. agents, Prompt Flow, team tools | Enterprise apps, GenAI        | ❌ No     |

---

## 1️⃣ Standalone Azure AI Service (e.g., Computer Vision, Translator)

### ✅ Best for:

- Learning one service (like OCR, text-to-speech, etc.)
- Testing APIs
- Using the **Free Tier** (F0 pricing)

---

### ☁️ Portal Setup

1. Go to [Azure Portal](https://portal.azure.com)
2. Click **Create a resource**
3. Search for the service:

   - "Computer Vision"
   - "Translator"
   - "Text Analytics"
   - "Speech"

4. Fill form:

   - Name: `my-ai-test`
   - Region: East US
   - Pricing: Select **F0** if available

✅ Done! Now copy your:

- **Endpoint**
- **Key1**

---

### 🖥️ CLI Setup

```bash
az group create --name my-rg --location eastus

az cognitiveservices account create \
  --name myStandaloneAI \
  --resource-group my-rg \
  --kind TextAnalytics \  # or Translator, Speech, etc.
  --sku F0 \
  --location eastus
```

---

### 💻 Example Code (Text Analytics SDK)

```python
from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics import TextAnalyticsClient

endpoint = "https://myStandaloneAI.cognitiveservices.azure.com/"
key = "<your-key>"

client = TextAnalyticsClient(endpoint, AzureKeyCredential(key))

docs = ["Azure is awesome!", "Cognitive Services make life easier."]
result = client.analyze_sentiment(docs)

for doc in result:
    print(doc.sentiment)
```

---

## 2️⃣ Azure AI Services (Multi-Service Resource)

### ✅ Best for:

- Using multiple AI services in one app (Vision + Translator + OpenAI)
- Shared authentication, endpoint, and billing

---

### ☁️ Portal Setup

1. Go to [Azure Portal](https://portal.azure.com)
2. Create resource → search: **Azure AI Services**
3. Select `Azure AI Services` (Kind: `AIServices`)
4. Name: `my-multi-ai`
5. SKU: `S0`

✅ Copy:

- **Endpoint**
- **Key**

---

### 🖥️ CLI Setup

```bash
az group create --name my-ai-rg --location eastus

az cognitiveservices account create \
  --name myAIServicesRes \
  --resource-group my-ai-rg \
  --kind AIServices \
  --sku S0 \
  --location eastus
```

---

### 💻 Example Code (Speech SDK)

```python
import azure.cognitiveservices.speech as speechsdk

speech_config = speechsdk.SpeechConfig(
    subscription="<your-key>",
    region="eastus"
)

synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)
synthesizer.speak_text_async("Hello from Azure AI Services!")
```

> ✅ You can use this same endpoint/key with Translator, Vision, OpenAI, etc.

---

## 3️⃣ Azure AI Foundry Project + Hub

### ✅ Best for:

- Production AI applications (agents + prompts + teams)
- Apps combining **GPT + Content Safety + Vision + Workflow**
- Access to **Prompt Flow**, **Agent Service**, **tracing**, **environments**

---

### ☁️ Portal Setup ([https://ai.azure.com](https://ai.azure.com))

1. Create a **Hub**

   - Name: `my-hub`
   - Region: `East US`

2. Create a **Project**

   - Name: `my-ai-project`
   - Link to your Hub
   - Enable AI Services ✅

🎁 What you get:

- A built-in **multi-service** AI resource
- Prompt Flow environment
- Built-in secrets & agent registration

---

### 🧠 How to Use It

You can either:

- Open the **Foundry Portal → Resources** → Copy endpoint/key
- OR use **Foundry SDK** (preview):

```python
from azure.identity import DefaultAzureCredential
from azure.ai.foundry import FoundryClient
from azure.ai.textanalytics import TextAnalyticsClient

foundry = FoundryClient(
    project_name="my-ai-project",
    credential=DefaultAzureCredential()
)

text_ai = foundry.get_ai_service("textanalytics")

client = TextAnalyticsClient(
    text_ai.endpoint,
    AzureKeyCredential(text_ai.key)
)
result = client.analyze_sentiment(["This is brilliant!"])
```

---

## 🔐 Authentication Methods (Simple Explanation)

| Method              | Description                                    | Use Case                  |
| ------------------- | ---------------------------------------------- | ------------------------- |
| 🔑 Key-based        | Copy-paste a key from Azure                    | Quick testing             |
| 🪪 Entra ID          | Secure login via Azure Identity                | Enterprise apps           |
| 🛡️ Managed Identity | Auto-login for Azure-hosted apps (VM, Web App) | Secure production         |
| 🔐 Azure Key Vault  | Store keys securely                            | Best for all environments |

---

## 🧾 Summary Table

| You want to...                                      | Use this                         |
| --------------------------------------------------- | -------------------------------- |
| Test one AI service with free calls                 | Standalone resource (F0)         |
| Use Vision + Translator + GPT + Speech              | Multi-service (AIServices)       |
| Build full AI apps with prompts, workflows, tracing | Foundry Project + Hub            |
| Keep it simple with keys                            | Use key-based auth               |
| Securely deploy to production                       | Use Entra ID or Managed Identity |
