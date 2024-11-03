
import os
import os
from agents.troubleshooting_agent import VProTroubleshootingAgent
from core.config_manager import ConfigManager
from core.session_manager import SessionManager
from core.pdf_tools import extract_text_from_pdfs
from config.constants import DEFAULT_SECURITY_LEVEL

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

    config_manager = ConfigManager('config/team_config.yaml')
    session_manager = SessionManager()

    # Initialize VProTroubleshootingAgent with the generic agent structure
    vpro_agent = VProTroubleshootingAgent(
        openai_api_key=openai_api_key,
        config_manager=config_manager,
        session_manager=session_manager
    )
    
    # Option to rebuild vector store on demand
    regenerate = input("Would you like to regenerate the vector store? (yes/no): ").strip().lower()
    force_rebuild = regenerate == 'yes'
    
    pdf_folder_path = "teams/intel_vpro/reference_materials/public"
    documents = extract_text_from_pdfs(pdf_folder_path)
    
    # Initialize (load or build) vector store based on user input
    vpro_agent.initialize_vector_store(documents, force_rebuild=force_rebuild)

    print("\nVector store ready.")
    print("\n--- Start Interaction ---")
    print("Type 'exit' to end the conversation.\n")
    
    while True:
        user_query = input("Enter your troubleshooting query: ")
        if user_query.lower() == "exit":
            print("Ending interaction.")
            break
        
        response = vpro_agent.handle_request(user_query)
        print("Troubleshooting Response:", response)

# Run the main function
main()