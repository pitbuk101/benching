import os
from pathlib import Path
from src.utils.logs import get_custom_logger
from tqdm import tqdm
from src.env import METADATA_LOCATION
logger = get_custom_logger(__name__)
class PromptLibrary:
    """A library for managing prompts.
    """
    def __init__(self):
        logger.info(f"Loading prompts from {METADATA_LOCATION}")
        self.prompt_path = Path(METADATA_LOCATION)
        self.prompts = {}
        self._load_prompts(self.prompt_path)

    def _load_prompts(self, path):
        for file in tqdm(os.listdir(path)):
            if file.endswith(".txt"):
                with open(path/ file, "r") as f:
                    file_name = file.split(".")[0]
                    tenant_id = str(path).split("/")[-1]
                    logger.info(f"Loading prompt: {path/file_name}")
                    # self.prompts[tenant_id] = {file_name: f.read()}
                    if self.prompts.get(tenant_id) is None:
                        self.prompts[tenant_id] = {}
                    self.prompts[tenant_id][file_name] = f.read()
            if (path/file).is_dir():
                self._load_prompts(path/file)

    def add_prompt(self, tenant_id: str, prompt_name: str, prompt_content: str):
        self.prompts[tenant_id][prompt_name] = prompt_content

    def get_prompts(self, tenant_id: str, prompt_name: str) -> str:
        return self.prompts.get(tenant_id, {}).get(prompt_name, None)

    def __str__(self):
        return f"PromptLibrary({self.prompts})"
    def __repr__(self):
        return self.__str__()

prompt_library = PromptLibrary()

# if __name__ == "__main__":
#     prompt_library = PromptLibrary()
#     print(prompt_library.get_prompts("048ee4ca-43b3-48e5-b95a-bd442ba15c91", "intent_classification"))