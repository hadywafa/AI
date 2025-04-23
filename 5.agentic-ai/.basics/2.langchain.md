# 🧠 LangChain + OpenAI (v0.3+): Mastering LLM Integration

LangChain is a **framework for developing applications powered by language models**. With its updated `v0.3+` API, it provides modular abstractions for prompts, memory, tools, and agents — all wrapped beautifully for real-world use cases like **chatbots, question answering, agents, and more**.

---

## 🚀 What You'll Learn

- How LangChain integrates with OpenAI (ChatGPT, GPT-4)
- How to create prompts and models using `langchain-core` and `langchain-openai`
- Memory and chains overview
- Simple chatbot and agent use cases
- Best practices for LangChain 0.3+

---

## 📦 Prerequisites

Ensure your environment has the following:

```bash
pip install langchain langchain-openai openai
```

And set your OpenAI API key:

```bash
export OPENAI_API_KEY="your-api-key"
```

Or set it inside your code:

```python
import os
os.environ["OPENAI_API_KEY"] = "your-api-key"
```

---

## 🧱 LangChain v0.3+ Core Concepts

LangChain has broken into modular packages:

| Package               | Use                                           |
| --------------------- | --------------------------------------------- |
| `langchain-core`      | Core interfaces for messages, prompts, chains |
| `langchain-openai`    | Integration with OpenAI's LLM APIs            |
| `langchain-community` | Tools, retrievers, external integrations      |

---

## ✨ Step 1: Load OpenAI Model

```python
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-3.5-turbo")  # or "gpt-4"
```

---

## 📝 Step 2: Create Prompt Templates

LangChain encourages using structured prompt templates:

```python
from langchain_core.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant."),
    ("human", "{question}")
])
```

---

## 🔗 Step 3: Combine Prompt + Model into a Chain

```python
from langchain_core.chains import LLMChain

chain = LLMChain(llm=llm, prompt=prompt)
response = chain.invoke({"question": "What's the capital of Japan?"})

print(response)
```

✅ **Output**:

```bash
Tokyo
```

---

## 🧠 Step 4: Add Memory for Stateful Chatbots

```python
from langchain_core.memory import ConversationBufferMemory

memory = ConversationBufferMemory(return_messages=True)

chat_chain = LLMChain(llm=llm, prompt=prompt, memory=memory)

chat_chain.invoke({"question": "Who won the 2022 World Cup?"})
chat_chain.invoke({"question": "What year was that?"})
```

---

## 🦾 Step 5: Using Tools and Agents (Optional)

LangChain agents can make decisions and call tools like search or calculator.

```python
from langchain.agents import load_tools, initialize_agent

tools = load_tools(["llm-math"], llm=llm)
agent = initialize_agent(tools, llm, agent="zero-shot-react-description")

result = agent.run("What is 9.3 times 1.8?")
print(result)
```

---

## 🛠️ Use Case: Build a Mini Chatbot with Memory

```python
from langchain.chains import ConversationChain

chatbot = ConversationChain(llm=llm, memory=ConversationBufferMemory())

print(chatbot.invoke("Hello!"))
print(chatbot.invoke("Who are you?"))
print(chatbot.invoke("What's 5 plus 7?"))
```

---

## ✅ Best Practices for v0.3+

- Use `langchain-core` + `langchain-openai` for clean imports
- Prefer `ChatOpenAI` over `OpenAI` for better structured outputs
- Use structured prompts for consistency and clarity
- Use `ConversationBufferMemory` or `ConversationSummaryMemory` for chat state
- For production, consider:
  - **Streaming responses**
  - **Retry logic**
  - **Rate limit handling**

---

## 🧩 Bonus: Streaming Responses with Async

```python
async for chunk in llm.astream("Tell me a joke about ducks"):
    print(chunk.content, end="")
```

---

## 📚 Further References

- [LangChain Docs](https://docs.langchain.com/)
- [OpenAI API](https://platform.openai.com/docs/)
- [LangChain Cookbook](https://github.com/hwchase17/langchain-cookbook)

---

## 🎯 Summary

✅ With LangChain v0.3+, you can:

- Use OpenAI models easily and cleanly
- Build prompt-based chains
- Add memory for chat context
- Extend with tools and agents for smarter workflows

---

If you'd like, I can walk you through **how to use LangChain in a FastAPI or Flask app**, or how to **connect it to vector stores and RAG (Retrieval-Augmented Generation)**. Just say the word!
