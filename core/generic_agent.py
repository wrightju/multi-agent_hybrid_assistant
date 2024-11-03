import openai
from core.vector_store import build_vector_store, load_vector_store, save_vector_store, query_vector_store
from core.prompt_utils import load_system_prompt

class GenericAgent:
    def __init__(self, openai_api_key, prompt_path, knowledge_base=None, config_manager=None, session_manager=None, vector_store_path="vector_store.index"):
        self.openai_api_key = openai_api_key
        self.system_prompt = load_system_prompt(prompt_path)
        self.knowledge_base = knowledge_base
        self.config_manager = config_manager
        self.session_manager = session_manager
        self.vector_index = None
        self.document_texts = []
        self.vector_store_path = vector_store_path

    def initialize_vector_store(self, documents, force_rebuild=False):
        """
        Initializes the vector store by loading from disk or building anew if necessary.
        
        Parameters:
        - documents (list of str): List of document texts to use if building the vector store.
        - force_rebuild (bool): Whether to force a rebuild even if a stored vector exists.
        """
        document_chunks_path = self.vector_store_path + "_chunks.pkl"  # Path to save/load document chunks

        # Attempt to load existing vector store and document chunks if not forcing rebuild
        if not force_rebuild:
            self.vector_index, self.document_texts = load_vector_store(self.vector_store_path, document_chunks_path)
            if self.vector_index and self.document_texts:
                print("Using existing vector store and document chunks.")
                return  # Exit if successfully loaded
        
        # Build and save vector store if not loaded or if rebuilding
        print("Building a new vector store...")
        self.vector_index, self.document_texts = build_vector_store(documents, self.openai_api_key)
        save_vector_store(self.vector_index, self.vector_store_path, document_chunks_path, self.document_texts)

    def query_vector_store(self, query, top_k=3):
        if not self.vector_index:
            return "Vector store not initialized. Please build or load the vector store."
        return query_vector_store(query, self.vector_index, self.document_texts, self.openai_api_key, top_k=top_k)

    def handle_request(self, query):
        if self.vector_index is None:
            return "The vector store is not initialized. Please build the vector store first."

        full_query = f"{self.system_prompt}\n\nUser Query: {query}"
        results = self.query_vector_store(full_query, top_k=2)
        
        if not results:
            return "No relevant information found for your query."

        combined_results = "\n\n".join(results[:3])
        prompt_with_results = f"{self.system_prompt}\n\nUser Query: {query}\n\nRelevant Information for troubleshooting:\n{combined_results}"

        try:
            # Using the updated OpenAI API client syntax
            client = openai.OpenAI(api_key=self.openai_api_key)
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": prompt_with_results}
                ],
                max_tokens=150,
                temperature=0.7
            )
            
            # Extract and return the response text
            response_text = response.choices[0].message.content.strip()
            return response_text

        except Exception as e:
            print(f"Error generating response with OpenAI API: {e}")
            return "I'm sorry, but I encountered an issue processing your request."


