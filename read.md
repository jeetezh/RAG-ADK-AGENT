# RAG Agent (Retrieval-Augmented Generation Agent)

A **RAG Agent** enhances a Large Language Model (LLM) by integrating a retrieval component that fetches relevant context from an external knowledge source (e.g., vector database, document store) before generating a response.

## Workflow
1. **Input Processing** – Accepts a natural language query from the user.
2. **Retrieval Step** – Uses embeddings to search a vector store (e.g., ChromaDB, Pinecone) and return the top-k relevant chunks.
3. **Augmentation** – Combines the retrieved content with the user query as additional context for the LLM.
4. **Generation** – The LLM produces a grounded, context-aware answer, optionally calling tools/functions for additional operations.

## Framework
This project uses the **Google Agent Development Kit** as the AI framework.

## Integrated Functions
- `list_collections` – Shows all existing collections in the vector database.
- `create_collection` – Creates a new collection.
- `delete_collection` – Deletes a collection.
- `add_file_to_collection` – Adds a file to a collection.
- `get_files_from_collection` – Lists all files added to a collection.
- `answer_query` – Answers a user query by searching inside a collection.
- `delete_file_from_collection` – Deletes a file from a collection.


## Installing Dependencies

Before running the project, install all required Python packages.

Run the following commands:
```bash
pip install -r requirements.txt
```

## Setup & Execution

### 1. Create Environment Variables
Create a `.env` file in the **same folder** where `agent.py` is located, with the following content:
```env
GOOGLE_GENAI_USE_VERTEXAI=FALSE
GOOGLE_API_KEY="your_gemini_api_key"
```

### 2. Start the API Server
Navigate **out of the folder** containing `agent.py` and run:
```bash
adk api_server
```
This will start the FastAPI server locally.

### 3. Launch the Streamlit Interface
```bash
streamlit run stream.py
```
## This will open a web interface where you can interact with the RAG Agent.
**Features**
1. Retrieval-augmented conversational AI
2. Integration with Google Gemini API
3. Built-in FastAPI endpoints for backend processing
4. Streamlit UI for interactive queries
