# [Exercise - Create a generative AI app that uses your own data](https://microsoftlearning.github.io/mslearn-ai-studio/Instructions/04-Use-own-data.html)

## 🤖 Why Use `text-embedding-ada-002` in a RAG Flow — Even with Azure AI Search?

---

### 🧠 First, Let’s Review the Key RAG Flow Pieces

RAG = **Retrieval-Augmented Generation**

💡 It means:

1. Find the right info from **your data** (Retrieval)
2. Use a language model like GPT-4o to answer using that info (Generation)

And this workflow needs 3 major building blocks:

| Part          | What it Does                                            | Tool Used                  |
| ------------- | ------------------------------------------------------- | -------------------------- |
| 1️⃣ Embedding  | Turns your PDFs + user questions into vectors (numbers) | `text-embedding-ada-002`   |
| 2️⃣ Indexing   | Stores those vectors in a searchable format             | Azure AI Search            |
| 3️⃣ Chat Model | Reads retrieved chunks and answers                      | `gpt-4o` or `gpt-35-turbo` |

---

## 🔍 Why Use `text-embedding-ada-002` If I Already Use Azure AI Search?

Because **Azure AI Search (vector-based search)** doesn't work magically by itself — it **needs embeddings to work**. That’s where `text-embedding-ada-002` comes in.

### 🧩 Here's What Happens:

1. 🧾 Your PDFs are broken into chunks (ex: paragraphs).
2. Each chunk is converted into a vector using `text-embedding-ada-002`.
3. These vectors are stored in **Azure AI Search’s vector index**.

When the user asks a question:

1. Their question is **also embedded** with `text-embedding-ada-002`.
2. Azure AI Search **compares the embedded question to the stored chunk vectors** to find the most relevant info (nearest neighbors).
3. The most similar chunks are passed to GPT-4o to **answer grounded in your data**.

---

## ✅ Summary: You Need `text-embedding-ada-002` for 2 Jobs

| Where It's Used              | Why It's Needed                          |
| ---------------------------- | ---------------------------------------- |
| 🧾 While uploading data      | To embed the chunks into vectors         |
| ❓ While user asks questions | To embed the query and match with chunks |

Even though **Azure AI Search handles the indexing**, it needs vectors — and `text-embedding-ada-002` is what **creates them**.

---

## 🧠 Real-World Analogy

Imagine your PDF data is like a room full of books.
You can’t search by flipping pages manually — so you:

- Use `text-embedding-ada-002` to turn each book into a **set of coordinates** (like GPS).
- Azure AI Search stores those coordinates in a map.
- When the user asks something, you **convert their question** into GPS coordinates using the **same embedding model**.
- Azure AI Search finds the books closest to that location and gives them to GPT.

---

## 📌 Final Takeaway

Even though Azure AI Search is doing the "search", **embedding is what powers the search**.
Without `text-embedding-ada-002`, **there are no vectors to compare** — so RAG wouldn't work.
