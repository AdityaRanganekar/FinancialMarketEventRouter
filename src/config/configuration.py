import os
from dotenv import load_dotenv
from src.constants import CONFIG_FILE_PATH, PARAMS_FILE_PATH
from src.utils.common import read_yaml
from src.entity.config_entity import LLMConfig

load_dotenv()

class ConfigurationManager:
    def __init__(
        self,
        config_filepath=CONFIG_FILE_PATH,
        params_filepath=PARAMS_FILE_PATH
    ):
        self.config = read_yaml(config_filepath)
        self.params = read_yaml(params_filepath)

    def get_llm_config(self) -> LLMConfig:
        config = self.config["llm"]
        params = self.params["llm_params"]

        return LLMConfig(
            model_name=config["model_name"],
            base_url=config["base_url"],
            temperature=params["temperature"],
            max_tokens=params["max_tokens"]
        )