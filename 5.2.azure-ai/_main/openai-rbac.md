# 🛡️ Azure OpenAI RBAC in Azure AI Foundry – Full Guide

Azure OpenAI supports **Azure Role-Based Access Control (RBAC)** to secure and delegate access to resources like GPT deployments, fine-tuning capabilities, and quota monitoring — using **specific roles** and **granular permissions**.

This guide explains:

- What each role does ✅/❌
- How to assign roles
- Real scenarios for each role (perfect for AI-102 exam prep!)

---

## 📌 What is Azure RBAC?

RBAC = _who_ can do _what_ on _which_ resource.

In Azure:

- You assign **roles** to **users, groups, service principals**, or **managed identities**.
- Each role has a set of **Actions** and **DataActions** it can perform.
- Scope: You can assign a role at:

  - 🔸 Subscription
  - 🔹 Resource Group
  - 🔸 Single Resource

---

## 🏗️ How to Assign an RBAC Role

**Step-by-step:**

1. Go to **Azure Portal > Azure OpenAI**
2. Select your deployed **Azure OpenAI resource**
3. Click **Access control (IAM)** in the left panel
4. Click ➕ **Add > Add role assignment**
5. Pick the **Role**
6. Choose **Member(s)** (user, group, identity)
7. Click ✅ **Review + assign**

Done! 🎉 Access takes effect within a few minutes.

---

## 🧩 Built-In Azure OpenAI Roles Explained

Here's a breakdown of the **four primary roles** for Azure OpenAI service and what each one **can and can't do**.

---

### 1️⃣ Cognitive Services **OpenAI User**

👤 Use-only access – ideal for testers or LLM app consumers.

| ✅ Can do                                     | ❌ Cannot do                |
| --------------------------------------------- | --------------------------- |
| View Azure OpenAI resource in Portal          | Create new resources        |
| Use Playground (Chat, Completion, DALL-E)     | Copy/Regenerate Keys        |
| See deployed models in AI Foundry             | Create/Edit deployments     |
| Call model via **Microsoft Entra ID (OAuth)** | Upload fine-tuning datasets |
| See model endpoint info                       | View quota usage            |
| Use deployed models                           | Add "On Your Data" sources  |

📌 **Use case:** Great for developers testing deployed models or using APIs with Entra ID auth.

---

### 2️⃣ Cognitive Services **OpenAI Contributor**

🛠️ Power contributor – ideal for ML engineers or prompt engineers.

| ✅ Can do everything OpenAI User can, plus:          | ❌ Still restricted from:            |
| ---------------------------------------------------- | ------------------------------------ |
| Create custom fine-tuned models                      | Creating new Azure OpenAI resources  |
| Upload datasets for fine-tuning                      | View/Copy/Regenerate keys            |
| Deploy/edit model deployments                        | View quota usage                     |
| View and filter **stored completions data**          | Create content filters               |
| Add "On Your Data" sources (requires extra role too) | Full access to all resource metadata |

📌 **Use case:** For engineers managing fine-tuning and deployment pipelines.

---

### 3️⃣ Cognitive Services **Contributor**

🏗️ Admin-level power at the resource group level.

| ✅ Can do:                        | ❌ Cannot do:          |
| --------------------------------- | ---------------------- |
| Create new Azure OpenAI resources | Use Entra ID inference |
| View/Copy/Regenerate keys         | –                      |
| Access resource endpoint          | –                      |
| Manage model deployments          | –                      |
| Add "On Your Data" sources        | –                      |
| Upload fine-tune datasets         | –                      |
| Create custom content filters     | –                      |

📌 **Use case:** DevOps engineer or resource administrator managing the entire RG/project.

---

### 4️⃣ Cognitive Services **Usages Reader**

📊 Quota visibility only.

| ✅ Can do                           | ❌ Cannot do                  |
| ----------------------------------- | ----------------------------- |
| View quota usage                    | All other tasks               |
| View quota allocation in AI Foundry | Cannot view or edit resources |

📌 **Use case:** Helpful for monitoring usage and cost by a separate team (like finance or ops).

---

## 🧩 Composite Roles (Combos)

### 🔹 OpenAI User + Usages Reader

➡️ Use the models + view quota (minimalist user access with insights)

### 🔹 OpenAI Contributor + Usages Reader

➡️ Full model management + quota monitoring

### 🔹 Cognitive Services Contributor + Usages Reader

➡️ Full admin with quota edit ability (power combo for DevOps/AI Architect)

---

## 🧠 Real-World Scenarios for Exam

| Scenario                                                        | Role Needed                                               |
| --------------------------------------------------------------- | --------------------------------------------------------- |
| You want to upload training data to fine-tune GPT-3.5           | **OpenAI Contributor**                                    |
| You want to view the deployed models and test in Playground     | **OpenAI User**                                           |
| You need to regenerate API keys                                 | **Cognitive Services Contributor**                        |
| You want to monitor quota usage for OpenAI usage                | **Usages Reader**                                         |
| You need to deploy a model to AI Foundry and add a search index | **OpenAI Contributor + Contributor (subscription level)** |

---

## ⚠️ Common Issues

### ❌ Can’t See Search Indexes in AI Foundry

📌 **Root Cause:** Lacking subscription-level read access to Azure Cognitive Search.

✅ **Fix:** Assign Reader/Contributor role at **subscription level**.

---

### ❌ Can’t Upload File for "On Your Data" Feature

📌 **Root Cause:** No permission for:
`Microsoft.Storage/storageAccounts/listAccountSas/action`

✅ **Fix:** Assign subscription-level role that allows SAS key access or ask admin to upload.

---

## ✅ Summary Table

| Feature / Action               | OpenAI User | OpenAI Contributor | Cognitive Services Contributor | Usages Reader |
| ------------------------------ | ----------- | ------------------ | ------------------------------ | ------------- |
| Use Chat/Completion Playground | ✅          | ✅                 | ✅                             | ➖            |
| View deployed models           | ✅          | ✅                 | ✅                             | ➖            |
| Deploy models                  | ❌          | ✅                 | ✅                             | ➖            |
| Fine-tune models               | ❌          | ✅                 | ✅                             | ➖            |
| View/Regenerate Keys           | ❌          | ❌                 | ✅                             | ➖            |
| Add “On Your Data” sources     | ❌          | ✅ (partial)       | ✅                             | ➖            |
| Monitor quota                  | ❌          | ❌                 | ❌                             | ✅            |
| Create OpenAI resource         | ❌          | ❌                 | ✅                             | ❌            |

---

## 🏁 Final Tip for Exam

💡 When you see questions like:

> “User can call deployed models, but not upload fine-tune data. What role?”

✅ **Answer:** OpenAI User

> “User can upload dataset, but not create the resource”
> ✅ **Answer:** OpenAI Contributor

---

## 📌 [Click here for more](https://docs.microsoft.com/en-us/azure/cognitive-services/openai/how-to/role-based-access-control#visual-diagram)
