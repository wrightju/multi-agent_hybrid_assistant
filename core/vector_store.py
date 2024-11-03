
import faiss
import os
import openai
import pickle
import numpy as np
from tqdm import tqdm
from core.text_utils import chunk_text

def save_vector_store(vector_index, vector_store_path, document_chunks_path, document_chunks):
    """
    Saves the FAISS vector store and document chunks to disk.
    
    Parameters:
    - vector_index (faiss.IndexFlatL2): The FAISS index to save.
    - vector_store_path (str): Path to save the vector store index.
    - document_chunks_path (str): Path to save the document chunks list.
    - document_chunks (list): List of document text chunks.
    """
    faiss.write_index(vector_index, vector_store_path)
    with open(document_chunks_path, 'wb') as f:
        pickle.dump(document_chunks, f)
    print("Vector store and document chunks saved to disk.")

def load_vector_store(vector_store_path, document_chunks_path):
    """
    Loads the FAISS vector store and document chunks from disk, if available.
    
    Parameters:
    - vector_store_path (str): Path to load the vector store index.
    - document_chunks_path (str): Path to load the document chunks list.
    
    Returns:
    - (faiss.IndexFlatL2, list): The FAISS index and list of document text chunks.
    """
    if os.path.exists(vector_store_path) and os.path.exists(document_chunks_path):
        vector_index = faiss.read_index(vector_store_path)
        with open(document_chunks_path, 'rb') as f:
            document_chunks = pickle.load(f)
        print("Vector store and document chunks loaded from disk.")
        return vector_index, document_chunks
    return None, None


def build_vector_store(documents, openai_api_key, model="text-embedding-ada-002"):
    """
    Builds a FAISS vector store from a list of documents by creating embeddings for each.
    
    Parameters:
    - documents (list): List of document texts to embed.
    - openai_api_key (str): OpenAI API key to use for embedding generation.
    - model (str): OpenAI model for embedding generation.

    Returns:
    - (faiss.IndexFlatL2, list): The FAISS index and list of processed document chunks.
    """
    client = openai.OpenAI(api_key=openai_api_key)  # Initialize OpenAI client
    embeddings = []
    document_chunks = []

    for doc in tqdm(documents, desc="Processing documents", unit="doc"):
        chunks = chunk_text(doc, max_tokens=1000)
        
        for chunk in chunks:
            response = client.embeddings.create(
                model=model,
                input=chunk
            )
            embeddings.append(response.data[0].embedding)
            document_chunks.append(chunk)

    # Convert embeddings to a FAISS index
    embeddings = np.array(embeddings).astype('float32')
    vector_index = faiss.IndexFlatL2(embeddings.shape[1])
    vector_index.add(embeddings)
    print("Vector store built successfully.")

    return vector_index, document_chunks

def query_vector_store(query, vector_index, document_chunks, openai_api_key, model="text-embedding-ada-002", top_k=3):
    """
    Queries the vector store to find the most relevant documents for a given query.
    
    Parameters:
    - query (str): The query text.
    - vector_index (faiss.IndexFlatL2): The FAISS index for similarity search.
    - document_chunks (list): List of document chunks corresponding to the FAISS index entries.
    - openai_api_key (str): OpenAI API key for embedding generation.
    - model (str): OpenAI model for embedding generation.
    - top_k (int): Number of top documents to retrieve.

    Returns:
    - list: List of top-k relevant document texts, or an empty list if no results found.
    """
    client = openai.OpenAI(api_key=openai_api_key)  # Initialize OpenAI client
    response = client.embeddings.create(
        model=model,
        input=query
    )
    query_embedding = np.array(response.data[0].embedding).astype('float32').reshape(1, -1)

    # Retrieve top-k similar documents
    distances, indices = vector_index.search(query_embedding, top_k)

    # Check if any indices were returned; if not, return an empty list
    if len(indices[0]) == 0 or indices[0][0] == -1:
        print("No relevant documents found for the query.")
        return []  # No results found

    # Otherwise, retrieve and return the document chunks
    results = [document_chunks[i] for i in indices[0] if i < len(document_chunks)]
    return results

