# core/session_manager.py

class SessionManager:
    def __init__(self):
        """
        Initializes the SessionManager with an empty session store.
        This session store can hold temporary data, such as multi-step interaction contexts.
        """
        self.sessions = {}

    def create_session(self, session_id, initial_data=None):
        """
        Creates a new session with an optional initial data dictionary.
        
        Parameters:
        - session_id (str): A unique identifier for the session.
        - initial_data (dict): Initial data to populate the session (default is empty dict).
        """
        self.sessions[session_id] = initial_data if initial_data else {}

    def get_session_data(self, session_id, key, default=None):
        """
        Retrieves data from an existing session.
        
        Parameters:
        - session_id (str): The unique session identifier.
        - key (str): The key for the data to retrieve.
        - default: Default value if the key is not found in the session.
        
        Returns:
        - The value associated with the key, or the default if the key does not exist.
        """
        return self.sessions.get(session_id, {}).get(key, default)

    def set_session_data(self, session_id, key, value):
        """
        Sets data in an existing session.
        
        Parameters:
        - session_id (str): The unique session identifier.
        - key (str): The key for the data to set.
        - value: The value to store under the given key.
        """
        if session_id in self.sessions:
            self.sessions[session_id][key] = value
        else:
            print(f"Session '{session_id}' does not exist. Use create_session() first.")

    def delete_session(self, session_id):
        """
        Deletes a session from the session store.
        
        Parameters:
        - session_id (str): The unique session identifier.
        """
        if session_id in self.sessions:
            del self.sessions[session_id]

# Example usage:
# session_manager = SessionManager()
# session_manager.create_session('session_123', {'step': 1})
# session_manager.set_session_data('session_123', 'step', 2)
# step = session_manager.get_session_data('session_123', 'step')
