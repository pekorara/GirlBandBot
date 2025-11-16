import os
from dotenv import load_dotenv

load_dotenv()

def _get_required_env(name: str) -> str:
    value = os.getenv(name)
    if value is None or value == "":
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value


TOKEN = _get_required_env("TOKEN")
MY_GUILD_ID = _get_required_env("MY_GUILD_ID")

MYGO_BASE_URL = _get_required_env("MYGO_BASE_URL")
MUJICA_BASE_URL = _get_required_env("MUJICA_BASE_URL")

GOOGLE_DRIVE_API_KEY = _get_required_env("GOOGLE_DRIVE_API_KEY")
MUJICA_FOLDER_URL = _get_required_env("MUJICA_FOLDER_URL")


