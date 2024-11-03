import faiss
import openai
import numpy as np

class VProTroubleshootingAgent:
    def __init__(self, knowledge_base, config_manager=None, session_manager=None, openai_api_key=None):
        """
        Initialize the vPRO Troubleshooting Agent with dependencies, including OpenAI API key for embeddings.
        
        Parameters:
        - knowledge_base (object): Placeholder, typically an object for accessing vectorized knowledge.
        - config_manager (ConfigManager, optional): Manages configuration data.
        - session_manager (SessionManager, optional): Manages session data for multi-step interactions.
        - openai_api_key (str, optional): OpenAI API key for embedding generation.
        """
        self.knowledge_base = knowledge_base
        self.config_manager = config_manager
        self.session_manager = session_manager
        self.vector_index = None  # FAISS index
        self.document_texts = []  # To store documents for result matching
        if openai_api_key:
            openai.api_key = openai_api_key

    def build_vector_store(self, documents):
        """
        Build a vector store from a list of troubleshooting documents.
        
        Parameters:
        - documents (list): List of strings, each representing a troubleshooting document.
        """
        # Generate embeddings for each document
        embeddings = []
        for doc in documents:
            response = openai.Embedding.create(
                input=doc,
                model="text-embedding-ada-002"
            )
            embeddings.append(response['data'][0]['embedding'])
            self.document_texts.append(doc)

        # Convert embeddings to a FAISS index
        embeddings = np.array(embeddings).astype('float32')
        self.vector_index = faiss.IndexFlatL2(embeddings.shape[1])
        self.vector_index.add(embeddings)
        print("Vector store built successfully.")

    def query_vector_store(self, query, top_k=3):
        """
        Query the vector store for relevant documents based on a user query.
        
        Parameters:
        - query (str): The user's troubleshooting query.
        - top_k (int): Number of top matching documents to retrieve.
        
        Returns:
        - list: List of top-k relevant document texts.
        """
        # Generate embedding for the query
        response = openai.Embedding.create(
            input=query,
            model="text-embedding-ada-002"
        )
        query_embedding = np.array(response['data'][0]['embedding']).astype('float32').reshape(1, -1)

        # Retrieve top-k similar documents
        _, indices = self.vector_index.search(query_embedding, top_k)
        results = [self.document_texts[i] for i in indices[0]]
        return results

    def handle_request(self, query, session_id=None):
        """
        Handles a troubleshooting request by querying the vector store for relevant information.
        
        Parameters:
        - query (str): The query or issue description needing troubleshooting.
        - session_id (str, optional): The session ID if tracking multi-step interaction.

        Returns:
        - response (str): The troubleshooting solution or information.
        """
        if self.vector_index is None:
            return "The vector store is not initialized. Please build the vector store first."
        
        results = self.query_vector_store(query)
        return "\n\n".join(results[:3]) if results else "No relevant information found."
