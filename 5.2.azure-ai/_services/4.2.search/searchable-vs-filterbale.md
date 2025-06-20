# **`searchable`** and **`filterable`** in **Azure AI Search**

## 🔎 `searchable` — Think **full-text search**

- Enables **text analysis** like word-breaking, stemming, and case-insensitive matching.
- Used when users **search for words/phrases** within a field.
- Supports fuzzy, wildcard, and partial matches.

🧠 **Example**:

```json
{ "Review": "This laptop has amazing battery life" }
```

A search for `"battery"` or `"amazing"` will match this document **if `Review` is searchable**.

---

## 🧮 `filterable` — Think **exact matches** and **WHERE conditions**

- Allows filtering using **exact values**.
- Used in structured queries like:

  - `price lt 100`
  - `rating eq 5`
  - `brand eq 'Sony'`

- **No full-text matching**; no stemming or tokenization.

🧠 **Example**:

```json
{ "Brand": "Sony" }
```

A filter like `brand eq 'Sony'` works **only if `Brand` is filterable**.

---

## ⚖️ Side-by-Side Comparison

| Feature       | `searchable`                     | `filterable`                         |
| ------------- | -------------------------------- | ------------------------------------ |
| Use case      | Full-text search                 | Exact filtering                      |
| Tokenization  | Yes (e.g., breaks into words)    | No                                   |
| Query syntax  | `search=great laptop`            | `filter=brand eq 'Sony'`             |
| Field type    | Typically used with long text    | Best for enums, categories, keywords |
| Search method | Matches inside text (partial ok) | Only exact matches                   |

---

## 📌 Tip:

A field can be both **`searchable` and `filterable`**, like a `ProductName` field where you want to:

- search for "Pro Max"
- and also filter for exact models like `"filter=ProductName eq 'iPhone 15 Pro Max'"`
