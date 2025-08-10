import os
from sentence_transformers import SentenceTransformer
import chromadb

# Path to the ChromaDB database
CHROMA_PATH= "DB_PATH"


#Function to list collections in vectorDB
def list_collections()-> list:
    """
    List all collections in the vector database."""
    try:
        # Initialize ChromaDB persistent client
        client = chromadb.PersistentClient(path=CHROMA_PATH)

        # List all collections
        collections = client.list_collections()
    except Exception as e:
        return f"An error occurred while listing collections: {e}"

    # Format and return collection names
    return [col.name for col in collections]

#Function to create a collection in vectorDB

def create_collection(collection_name: str)-> str:
    """
    Create a collection in the vector database.
    
    Args:
        collection_name (str): The name of the collection to create.
        IMPORTANT: the length of the collection name should be greater than 4 characters
        
    Returns:
        str: A message indicating the result of the operation.
    """
    # Here you would implement the logic to create a collection in your vector database
    # For example, using a library like Pinecone, Weaviate, or similar.
    os.makedirs(CHROMA_PATH, exist_ok=True)

    # Load embedding model
    model = SentenceTransformer('all-MiniLM-L6-v2')
    try:
        # Initialize ChromaDB persistent client
        client = chromadb.PersistentClient(path=CHROMA_PATH)

        # create collection
        collection = client.create_collection(collection_name)
    except Exception as e:
        return f"An error occurred while creating the collection: {e}"

    return "✅ Collection '{}' created successfully!".format(collection_name)


#Function to delete the mentioned collection in vectorDB
def delete_collection(collection_name: str )-> str:
    """
    Delete the mentioned collection in the vector database.
    param collection_name: The name of the collection to delete.
    return: A message indicating the result of the operation.
    """
    #check whether Database exists or not
    if not os.path.exists(CHROMA_PATH):
        return "Database does not exist."
    client = chromadb.PersistentClient(path=CHROMA_PATH)    

    try:
        
        client.delete_collection(collection_name)

    except Exception as e:
        return f"An error occurred while deleting the collection: {e}"
    
#Function to add file to mentioned database
def add_file_to_collection(collection_name: str, file_path: str) -> str:
    """
    This function used to add a file to the specified collection in the vector database.    
    parameter:
        collection_name (str): The name of the collection to which the file will be added.
        file_path (str): The path to the file to be added.
    return:
        str: A message indicating the result of the operation.
    """
    # Create the database directory if it doesn't exist
    os.makedirs(CHROMA_PATH, exist_ok=True)
    
    # Load embedding model
    model = SentenceTransformer('all-MiniLM-L6-v2')

    # Initialize ChromaDB persistent client
    client = chromadb.PersistentClient(path=CHROMA_PATH)

    # Get or create collection
    try:
        collection =client.get_collection(collection_name)
        #read the given file
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()
    except Exception as e:
        return f"An error occurred : {e}"

    #split the text into chunks
    chunk_size = 400
    chunks = [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]

    #Generate embeddings
    embeddings = model.encode(chunks)

        #Add to ChromaDB
    filename = os.path.basename(file_path)
    collection.add(
        ids=[f"{filename}_chunk{i}" for i in range(len(chunks))],
        embeddings=embeddings.tolist(),
        documents=chunks,
        metadatas=[{"file": filename} for _ in chunks]
    )

    return f"File {file_path} added to collection '{collection_name}' successfully!"


#Function to answer query from the mentioned collection
def answer_query(query: str,collection_name : str) -> dict:
    """
    Answer a query using the vector database.
    
    Args:
        query (str): The query to answer.
        collection_name (str): The name of the collection to search in.
        
    Returns:
        dict: A dictionary containing the query and the context retrieved from the collection.
    """
    client = chromadb.PersistentClient(path=CHROMA_PATH )

    collection = client.get_collection(collection_name)

    model = SentenceTransformer('all-MiniLM-L6-v2')

    # Embed the query using the same model
    query_embedding = model.encode([query])


    # Run a similarity search in ChromaDB
    results = collection.query(
    query_embeddings=query_embedding.tolist(),
    n_results=8 # Top 8 most similar chunks
    )
    print(results)
    # Display the results
    context=results.get("documents", [])


    if not context:
        return "No relevant information found in the collection."
    return {"query": query,
            "context": context}


#function to get all files in the specified collection
def get_files_from_collection(collection_name: str) -> list:
    """
    Get all files in the specified collection.
    
    Args:
        collection_name (str): The name of the collection to retrieve files from.
        
    Returns:
        list: A list of file names in the collection.
    """
    client = chromadb.PersistentClient(path=CHROMA_PATH)

    try:
        collection = client.get_collection(collection_name)
    except Exception as e:
        return f"An error occurred while accessing the collection: {e}"

    
    
    # Get all items including their metadata
    results = collection.get(include=["metadatas"])
    list_of_files ={filename["file"] for filename in results["metadatas"]}

    return list(list_of_files)



def delete_file_from_collection(collection_name: str, file_name: str) -> str:
    """
    Delete a file from the specified collection.
    
    Args:
        collection_name (str): The name of the collection to delete the file from.
        file_name (str): The name of the file to delete.
        
    Returns:
        str: A message indicating the result of the operation.
    """
    client = chromadb.PersistentClient(path=CHROMA_PATH)

    try:
        collection = client.get_collection(collection_name)
        collection.delete(where={"file": file_name})
    except Exception as e:
        return f"An error occurred while deleting the file: {e}"
    
    return f"File '{file_name}' deleted from collection '{collection_name}' successfully!"

