# Enterprise GenAI Data Pipeline: Intelligent Audit Assistant 🚀

An end-to-end Retrieval-Augmented Generation (RAG) pipeline designed to ingest, process, and query unstructured enterprise audit logs. This project bridges the gap between traditional Data Engineering and state-of-the-art Generative AI.

## 🏗️ Architecture Overview

This project simulates a modern enterprise data workflow, moving from raw cloud storage to an interactive AI interface.

1. **Cloud Storage (Azure Blob Storage):** Raw audit CSV logs are hosted in an Azure Data Lake container.
2. **Data Processing (Pandas/Python):** Raw data is downloaded, cleaned, and contextually structured. *(Note: Designed with a PySpark fallback architecture for larger-scale Databricks deployments).*
3. **Embeddings (HuggingFace):** Processed text is chunked and embedded using the open-source `all-MiniLM-L6-v2` model.
4. **Vector Database (FAISS):** Embeddings are stored in a local FAISS index for high-speed similarity search.
5. **LLM Orchestration (LangChain & Groq):** A "bare-metal" RAG pipeline retrieves relevant context and injects it into a strict prompt for Meta's `Llama-3.3-70b-versatile` model via the ultra-fast Groq API.

## 💡 Key Engineering Decisions & Optimizations

* **Cost-Optimized Compute:** Bypassed expensive OpenAI embedding APIs in favor of local HuggingFace `sentence-transformers`, reducing PoC embedding costs to $0.
* **Model Lifecycle Management:** Actively managed LLM deprecations by upgrading the inference engine to the latest Llama 3.3 model during development to ensure pipeline uptime and leverage improved reasoning capabilities.
* **Bare-Metal RAG Control:** Replaced high-level LangChain wrapper chains with custom orchestration to ensure strict prompt adherence and eliminate dependency conflicts in modern Python environments.
* **Contextual Anomaly Detection:** The pipeline successfully detects nuances in the data, such as flagging audit records where a "routine check passed" note conflicts with a "Critical" risk severity score.

## 🚀 How to Run Locally

1. Clone the repository.
   
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   
3. Add your Groq API key to your environment variables.
   
4. Generate the dataset and upload to Azure (requires an Azure Storage connection string):
    ```bash
    python upload_to_azure.py
    
5. Process the data:
   ```bash
   python data_prep.py

6.Build the local FAISS vector index:
   ```bashpython build_vector_db.py
    
7. Launch the AI Audit Assistant interactive chat:
    ```bash
    python rag_chatbot.py
