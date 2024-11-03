# Updated OperatorAgent with new OpenAI v1 syntax for handling chat completions

import os
from openai import OpenAI
from config.constants import DEFAULT_SECURITY_LEVEL

class OperatorAgent:
    def __init__(self, openai_api_key, config_manager=None, session_manager=None, prompt_path="prompts/operator_prompt.md"):
        """
        Initialize the OperatorAgent with OpenAI API key, configuration, session managers, and system prompt.
        
        Parameters:
        - openai_api_key (str): API key for OpenAI to enable request interpretation.
        - config_manager (ConfigManager, optional): Manages configuration data.
        - session_manager (SessionManager, optional): Manages session data for interactions.
        - prompt_path (str): Path to the system prompt file.
        """
        self.config_manager = config_manager
        self.session_manager = session_manager
        self.agent_registry = {}
        self.client = OpenAI(api_key=openai_api_key)  # Initialize OpenAI client with new syntax

        # Load system prompt from file
        self.system_prompt = self.load_prompt(prompt_path)

    def load_prompt(self, prompt_path):
        """
        Loads the system prompt from a specified file path.
        
        Parameters:
        - prompt_path (str): Path to the system prompt file.
        
        Returns:
        - str: The content of the prompt file.
        """
        if os.path.exists(prompt_path):
            with open(prompt_path, 'r') as file:
                return file.read().strip()
        else:
            raise FileNotFoundError(f"System prompt file not found at {prompt_path}")

    def register_agent(self, name, agent_instance):
        """
        Register an agent to the registry with a given name.
        
        Parameters:
        - name (str): Name of the agent (e.g., 'vPRO_Troubleshooting', 'Document_Processor').
        - agent_instance (object): The instance of the agent to route requests to.
        """
        self.agent_registry[name] = agent_instance

    def interpret_and_respond(self, user_input):
        """
        Conversationally interprets user input and provides a response based on intent.
        
        Parameters:
        - user_input (str): The conversational input from the user.
        
        Returns:
        - str: A conversational response based on the input.
        """
        try:
            # Use the new OpenAI client syntax for chat completions
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": user_input}
                ],
                max_tokens=150,
                temperature=0.7
            )
            
            # Correctly access the response content
            response_text = response.choices[0].message.content.strip()
            return f"Operator Agent: {response_text}"

        except Exception as e:
            print(f"Error in interpreting user input: {e}")
            return "I'm sorry, but I encountered an issue processing your request."


    def route_request(self, request):
        """
        Routes the request to the appropriate agent based on its type.
        
        Parameters:
        - request (dict): A dictionary containing request details.
                          Expected keys are 'type' (str) and 'content' (str).
        
        Returns:
        - response (str): The response from the routed agent.
        """
        request_type = request.get('type')
        
        # Determine the agent based on the request type
        if request_type == 'troubleshooting_vPRO':
            agent = self.agent_registry.get('vPRO_Troubleshooting')
        elif request_type == 'document_processing':
            agent = self.agent_registry.get('Document_Processor')
        else:
            return "Error: Unknown request type."

        if agent:
            # Pass the entire request dictionary to the agent
            return agent.handle_request(request)
        else:
            return f"Error: No agent found for {request_type}"

    def access_control(self, request):
        """
        Simulate access control by checking if the request has proper access permissions.
        
        Parameters:
        - request (dict): A dictionary containing request details, including a 'security_level' key.
        
        Returns:
        - (bool): True if access is allowed, False otherwise.
        """
        required_security_level = request.get('security_level', 'public')
        
        # Placeholder for more detailed access control using config or session data
        if required_security_level == 'confidential':
            return False  # Placeholder restriction on confidential access
        
        return True

# This allows `OperatorAgent` to accept and use both config_manager and session_manager if needed.
