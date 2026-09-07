from src.config.configuration import ConfigurationManager
from src.logging.logger import logging

try:
    config_manager = ConfigurationManager()
    llm_config = config_manager.get_llm_config()
    
    logging.info(f"Successfully loaded config for model: {llm_config.model_name}")
    print(f"Success! Model Name: {llm_config.model_name}")
    print(f"Base URL: {llm_config.base_url}")
except Exception as e:
    print(f"Failed to load configuration: {e}")