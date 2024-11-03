# Configuration Manager for `core/config_manager.py` to load and manage configuration files.

import yaml

class ConfigManager:
    def __init__(self, config_path):
        """
        Initialize the ConfigManager with a path to the global configuration file.
        
        Parameters:
        - config_path (str): Path to the main team configuration YAML file.
        """
        self.config_path = config_path
        self.config_data = self.load_config()

    def load_config(self):
        """
        Load configuration data from a YAML file.
        
        Returns:
        - dict: Parsed configuration data.
        """
        try:
            with open(self.config_path, 'r') as file:
                return yaml.safe_load(file)
        except FileNotFoundError:
            print(f"Configuration file not found at {self.config_path}.")
            return {}
        except yaml.YAMLError as e:
            print(f"Error parsing YAML configuration: {e}")
            return {}

    def get_global_setting(self, key, default=None):
        """
        Retrieve a global setting from the configuration.
        
        Parameters:
        - key (str): The setting key to retrieve.
        - default: Default value if the key is not found.
        
        Returns:
        - The value of the setting, or the default if not found.
        """
        return self.config_data.get('global', {}).get(key, default)

    def get_team_config(self, team_name):
        """
        Retrieve team-specific configuration by team name.
        
        Parameters:
        - team_name (str): Name of the team (e.g., 'intel_vpro', 'intel_wifi').
        
        Returns:
        - dict: The configuration data for the specified team, or an empty dict if not found.
        """
        return self.config_data.get('teams', {}).get(team_name, {})

# Example usage:
# config_manager = ConfigManager('config/team_config.yaml')
# global_setting = config_manager.get_global_setting('some_key')
# team_config = config_manager.get_team_config('intel_vpro')
