
import os
from agents.operator import OperatorAgent
from agents.troubleshooting_agent import VProTroubleshootingAgent
from agents.document_processor_agent import DocumentProcessorAgent
from core.config_manager import ConfigManager
from core.session_manager import SessionManager
from config.constants import DEFAULT_SECURITY_LEVEL

# Mock knowledge base (for demonstration purposes)
class MockKnowledgeBase:
    def query(self, query_text):
        return f"Mock response for '{query_text}'"

import os
from agents.operator import OperatorAgent
from agents.troubleshooting_agent import VProTroubleshootingAgent
from agents.document_processor_agent import DocumentProcessorAgent
from core.config_manager import ConfigManager
from core.session_manager import SessionManager

def clear_screen():
    # Clear screen for Windows, Mac, and Linux
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    clear_screen()
    # Fetch OpenAI API key from environment
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if not openai_api_key:
        raise EnvironmentError("OPENAI_API_KEY not found in environment variables.")
    
    print("OpenAI API Key successfully retrieved.")

    # Initialize ConfigManager and SessionManager
    config_manager = ConfigManager('config/team_config.yaml')
    session_manager = SessionManager()
    print("ConfigManager and SessionManager initialized.")

    # Initialize OperatorAgent with OpenAI API key and prompt
    operator = OperatorAgent(openai_api_key=openai_api_key, config_manager=config_manager, session_manager=session_manager)
    print("OperatorAgent initialized with conversational capabilities.")

    # Initialize knowledge base and agents with config and session support
    knowledge_base = MockKnowledgeBase()
    vpro_agent = VProTroubleshootingAgent(knowledge_base=knowledge_base, config_manager=config_manager, session_manager=session_manager)
    doc_processor = DocumentProcessorAgent(templates={
        'knowledge_article': "Title: {title}\n\nContent:\n{content}\n"
    })

    # Register agents with the OperatorAgent
    operator.register_agent('vPRO_Troubleshooting', vpro_agent)
    operator.register_agent('Document_Processor', doc_processor)
    print("Agents registered with OperatorAgent.")

    # Interactive loop for user input
    print("\n--- Start Interaction ---")
    print("Type 'exit' to end the conversation.\n")
    
    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            print("Ending conversation.")
            break
        
        # Pass input to the OperatorAgent and get the response
        response = operator.interpret_and_respond(user_input)
        print(response)

# Run the main function
main()
