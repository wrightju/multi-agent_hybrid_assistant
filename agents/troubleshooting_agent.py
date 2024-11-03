from core.generic_agent import GenericAgent

class VProTroubleshootingAgent(GenericAgent):
    def __init__(self, openai_api_key, config_manager=None, session_manager=None):
        prompt_path = "teams/intel_vpro/prompts/vpro_troubleshooting_prompt.md"
        super().__init__(openai_api_key, prompt_path, config_manager=config_manager, session_manager=session_manager)

