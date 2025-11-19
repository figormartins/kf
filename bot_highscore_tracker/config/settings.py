"""
Configuration settings for KnightFight Bot
"""
from pathlib import Path

class BotSettings:
    """Bot configuration settings"""
    
    # Paths - using relative paths from project root
    # Get the directory where this config file is located (bot/config/)
    _CONFIG_DIR = Path(__file__).parent.resolve()
    # Go up two levels: bot/config/ -> bot/ -> project_root/
    BASE_DIR = _CONFIG_DIR.parent
    DATA_DIR = BASE_DIR / "data"
    ATTACK_TRACKER_FILE = DATA_DIR / "player_history.json"
    
    @classmethod
    def ensure_directories(cls):
        """Ensure required directories exist"""
        cls.DATA_DIR.mkdir(exist_ok=True)
