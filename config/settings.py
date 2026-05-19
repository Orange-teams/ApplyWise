from pathlib import Path
from pydantic_settings import BaseSettings
import yaml
import os
from dotenv import load_dotenv
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

class Settings(BaseSettings):

    # ===== Project =====
    PROJECT_NAME: str = "job-agent"
    ENVIRONMENT: str = "dev"


    # API KEYS
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY")

    # ===== Paths =====
    BASE_DIR: Path = BASE_DIR
    DATA_DIR: Path = BASE_DIR / "data"
    OUTPUT_DIR: Path = DATA_DIR / "outputs"
    LOG_DIR: Path = BASE_DIR / "logs"

    PROMPTS_PATH: Path = BASE_DIR / "src" / "prompts" / "prompts.yaml"
    MASTER_RESUME_PATH: Path = BASE_DIR / "src" / "resume" / "templates" / "master_resume.tex"
    GENERATED_TEX_PATH: Path = BASE_DIR / "generated"
    OUTPUT_DIR: Path = BASE_DIR / "data" / "outputs"
    # ===== Requests =====
    REQUEST_TIMEOUT: int = 20
    REQUEST_DELAY: int = 3
    MAX_RETRIES: int = 3

    # ===== LLM =====
    GEMINI_MODEL : str = "gemini-2.5-flash"

    # ===== Logging =====
    LOG_LEVEL: str = "INFO"

    # ===== Browser Headers =====
    USER_AGENT: str = (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    )

    class Config:
        env_file = ".env"


settings = Settings()
DB_PATH = BASE_DIR / "data" / "app.db"
DB_URL = f"sqlite:///{DB_PATH}"