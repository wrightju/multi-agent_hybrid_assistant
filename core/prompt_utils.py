import os

def load_system_prompt(prompt_path):
    """
    Loads the system prompt from a specified file path.
    
    Parameters:
    - prompt_path (str): Path to the system prompt file.
    
    Returns:
    - str: The content of the prompt file.
    
    Raises:
    - FileNotFoundError: If the prompt file is not found.
    """
    if os.path.exists(prompt_path):
        with open(prompt_path, 'r') as file:
            return file.read().strip()
    else:
        raise FileNotFoundError(f"System prompt file not found at {prompt_path}")
