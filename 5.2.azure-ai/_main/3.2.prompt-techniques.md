# 🧠 Azure OpenAI Prompt Engineering Techniques (AI-102 Style Guide)

Prompt engineering is the **core art** of working with large language models (LLMs). In Azure AI, especially with Azure OpenAI Service, writing effective prompts can make or break your solution. For the AI-102 exam, you'll need to understand various **prompting strategies**, **design patterns**, and **key techniques** like:

- 🔹 Few-shot learning
- 🔹 Zero-shot learning
- 🔹 One-shot learning
- 🔹 Priming
- 🔹 Data conditioning
- 🔹 Context-based learning
- 🔹 Chain-of-thought prompting

Let’s break them down one by one—with real-world Azure use cases and tips for the exam.

---

## 🎯 1. Zero-shot Learning

### 📘 Definition:

You provide **only the task**, with no examples. You rely entirely on the LLM’s pretraining.

### ✅ Example Prompt:

> "Translate this sentence to French: 'I am going to the market.'"

### 🧠 Real Scenario:

In Azure OpenAI, if you're using a chat model like GPT-4 Turbo and just ask for classification without examples, that’s zero-shot.

### 📌 When to Use:

- Simple tasks with clear language
- Fast prototypes
- High generalization required

---

## 🎯 2. One-shot Learning

### 📘 Definition:

You provide **one example** of the task to help the model learn the pattern.

### ✅ Example Prompt:

> "Translate this sentence to French.
> Example: 'Good morning' → 'Bonjour'
> Now translate: 'How are you?'"

### 🧠 Real Scenario:

Useful when the model struggles with nuanced tasks unless guided by an example.

---

## 🎯 3. Few-shot Learning

### 📘 Definition:

You provide **a few labeled examples** of the task to "teach" the model the desired output format or reasoning.

### ✅ Example Prompt:

> "Translate these sentences into French:
> 'Good morning' → 'Bonjour'
> 'Thank you' → 'Merci'
> 'Where is the train station?' →"

### 🧠 Real Scenario:

Used in classification, summarization, or extraction tasks within Azure OpenAI Studio or REST API chat completions.

### 💡 Tip for AI-102:

If you see a question with **multiple examples provided**, that’s few-shot learning.

---

## 🎯 4. Priming

### 📘 Definition:

Setting a **system message or initial instruction** that changes the model’s behavior during the entire conversation.

### ✅ Example:

> System Message:
> "You are a helpful math tutor who explains things in simple terms like teaching a 4-year-old."

---

> User: "What's 2 + 3?"

### 🧠 Real Scenario:

In Azure OpenAI, you set this using the `system` role in a chat message to guide the assistant's tone and personality.

### 📌 Use Case:

- Customer service agent emulation
- Medical assistant with specific tone
- Math tutor, coding helper, legal assistant

**📚 Exam Note:**
If you see a system instruction like "Act as a polite assistant," it's **priming**.

---

## 🎯 5. Data Conditioning

### 📘 Definition:

Preprocessing the **input data** so that it fits well into prompts. It's about **formatting**, **cleaning**, or **structuring** the inputs, not changing the model itself.

### ✅ Example:

You might transform a messy table into structured JSON before sending it in a prompt.

> "Given this data:
> { "product": "laptop", "price": 1499 }
> Generate a marketing sentence."

→ Output:

> "Check out our latest laptop for just \$1499!"

### 🧠 Real Scenario:

Used in Document Intelligence → extract text → condition → pass to OpenAI.

---

## 🎯 6. Context-based Learning

### 📘 Definition:

Providing the **relevant knowledge or facts** as part of the prompt so that the model can reason based on that information.

### ✅ Example:

> "You are a support bot for Contoso Electronics.
> Here’s the user manual: \[insert long context here].
> Now answer: 'How do I reset my device?'"

### 🧠 Real Scenario:

Used heavily in RAG (Retrieval-Augmented Generation), like the Azure Search + OpenAI demo.

### 📌 Why it matters:

- Reduces hallucination
- Keeps answers grounded in business data

---

## 🎯 7. Chain-of-Thought Prompting

### 📘 Definition:

Explicitly prompting the model to **show its reasoning step-by-step**.

### ✅ Example:

> "What’s 24 × 5? Explain how you got the answer."

→ Output:

> "First, 20 × 5 = 100. Then, 4 × 5 = 20. So, the total is 120."

### 🧠 Real Scenario:

Used in math tutor bots, document processing with multi-step logic, or code reasoning assistants.

---

## 📚 Cheat Sheet for the Exam

| Technique              | Definition                                   | Example Cue in Question                               |
| ---------------------- | -------------------------------------------- | ----------------------------------------------------- |
| Zero-shot              | No examples, just the task                   | "Translate this..."                                   |
| One-shot               | One example given                            | "Here’s an example: ..., now do..."                   |
| Few-shot               | Several examples given                       | "Classify the following with these examples..."       |
| Priming                | System message to change model behavior      | "System prompt: Act as..."                            |
| Data Conditioning      | Input preprocessing/formatting               | "Data cleaned/structured before sending to the model" |
| Context-based Learning | Feeding relevant domain data into the prompt | "You’re given this knowledge/context..."              |
| Chain-of-Thought       | Prompting to show reasoning steps            | "Explain your answer step-by-step"                    |

---

## 🏁 Summary

Prompt engineering isn't just about writing text—it's about understanding **how LLMs learn**, how to **minimize hallucination**, and how to **guide the model toward your business goal**. These techniques show up not just in the Azure OpenAI Playground, but also in Azure AI Studio, Prompt Flow, and integrated Document Intelligence workflows.

> ✅ For AI-102, make sure you know:
>
> - Definitions + examples of each technique
> - When to use which
> - How they appear in Azure Studio (system messages, temperature, etc.)
