# **🚀 Topics to Study for Data Storage (Stage 3)**

Data storage is a critical stage in data pipelines, ensuring that processed data is **stored efficiently, remains accessible, and supports analytics, machine learning, and real-time queries**. Below are the key topics you should study.

---

## **📌 1️⃣ Introduction to Data Storage**

- What is Data Storage?
- Why is it essential in modern data pipelines?
- Categories of Data Storage:
  - **Relational Databases (SQL)**
  - **NoSQL Databases**
  - **Data Lakes**
  - **Data Warehouses**
  - **Data Lakehouses**
  - **Real-Time Storage Systems**

---

## **📌 2️⃣ Types of Data Storage and Their Use Cases**

| **Storage Type**                 | **Definition**                                                                        | **Best For**                                        | **Examples**                                     |
| -------------------------------- | ------------------------------------------------------------------------------------- | --------------------------------------------------- | ------------------------------------------------ |
| **Data Warehouse** 🏢            | Stores **structured** data optimized for analytics & BI                               | Reporting, Business Intelligence, Query Performance | Amazon Redshift, Snowflake, Google BigQuery      |
| **Data Lake** 🌊                 | Stores **raw data** (structured, semi-structured, unstructured) for future processing | Machine Learning, AI, Storing Unstructured Data     | AWS S3, Azure Data Lake, Google Cloud Storage    |
| **Data Lakehouse** 🏠            | Combines **Data Lakes & Data Warehouses**                                             | Unified Storage for Structured & Unstructured Data  | Databricks Lakehouse, Delta Lake, Apache Iceberg |
| **Relational Databases (SQL)** 🛢 | Traditional structured database system                                                | Transactional systems, ACID compliance              | PostgreSQL, MySQL, Microsoft SQL Server          |
| **NoSQL Databases** 📦           | Schema-less databases optimized for fast reads/writes                                 | High-speed applications, Flexible Data Models       | MongoDB, DynamoDB, Cassandra                     |
| **Real-Time Databases** ⚡       | Designed for ultra-fast storage and querying                                          | Streaming Data, Real-Time Dashboards                | Apache Druid, Elasticsearch, Redis               |

---

## **📌 3️⃣ Data Storage Architectures**

- **OLAP vs. OLTP**
  - **OLAP (Online Analytical Processing)** – Used for data analytics (Data Warehouses)
  - **OLTP (Online Transaction Processing)** – Used for real-time transactions (SQL, NoSQL)
- **Lambda vs. Kappa Architecture for Storage**
  - How storage is structured in each architecture
  - Pros & cons of each

---

## **📌 4️⃣ Data Partitioning & Indexing**

- What is Data Partitioning?
- Horizontal vs. Vertical Partitioning
- Indexing Techniques for Fast Queries (B-Trees, Hash Indexing, Columnar Indexing)
- Partitioning in Data Lakes & Warehouses (Hive Partitions, BigQuery Partitioning)

---

## **📌 5️⃣ Storage Formats & File Types**

| **Format**                         | **Best For**                     | **Examples**          |
| ---------------------------------- | -------------------------------- | --------------------- |
| **Row-Based (CSV, JSON, Avro)**    | Fast transactional data          | CSV, JSON, Avro       |
| **Columnar (Parquet, ORC)**        | Optimized for analytics & BI     | Apache Parquet, ORC   |
| **Binary (Protobuf, MessagePack)** | Lightweight & fast serialization | Protobuf, MessagePack |

---

## **📌 6️⃣ Real-Time vs. Batch Storage**

- **Batch Storage** (Redshift, Snowflake, S3)
- **Real-Time Storage** (Apache Druid, Elasticsearch, DynamoDB)
- **Hybrid Approaches** (Using both for performance & cost optimization)

---

## **📌 7️⃣ Data Security, Governance & Compliance**

- **Data Encryption (At Rest & In Transit)**
- **Access Controls & Authentication**
- **Regulatory Compliance (GDPR, HIPAA, CCPA)**
- **Data Retention & Archiving Strategies**
