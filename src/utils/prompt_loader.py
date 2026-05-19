import yaml
from config.settings import settings

def load_prompts(path=settings.PROMPTS_PATH):

    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)