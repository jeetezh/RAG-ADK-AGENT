from google.adk.agents import Agent
from .tools.rag_tools import *


#define the instruction
instruction = """
You are a RAG agent
that can create, manage, and search collections in a vector database.
Use the following tools to interact with the database:

- `list_collections`: Shows all existing collections in the vector database.
- `create_collection`: Creates a new collection.
- `delete_collection`: Deletes a collection.
- `add_file_to_collection`: Adds a file to a collection.
- `get_files_from_collection`: Lists all files added to a collection.
- `answer_query`: Answers a user query by searching inside a collection.
- `delete_file_from_collection`: Deletes a file from a collection.

NOTE: `answer_query` returns a dictionary with the query and the retrieved context.
Always answer the query using ONLY the provided context.
Do NOT up any information.
Try to answer in point wise format for long answers

"""


# Create the root LLM agent with the MCP tool

root_agent = Agent(
        name="RAG_AGENT",
        model="gemini-2.0-flash", 
        description="A RAG AGENT that can create and manage collections in a vector database.",
        instruction=instruction,
        tools=[list_collections, 
               create_collection,
               delete_collection,
               add_file_to_collection,
               answer_query,
               get_files_from_collection,
               delete_file_from_collection,
               ], 
        
    )
   
            
