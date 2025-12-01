"""
Configuration settings for KnightFight Bot
"""
from pathlib import Path
import os
from dotenv import load_dotenv


class BotSettings:
    """Bot configuration settings"""
    load_dotenv()
    IS_INT_SERVER = os.getenv('KF_IS_INT_SERVER', 'true').lower() == 'true'
    # Login
    LOGIN_USERNAME = os.getenv('KF_LOGIN_USERNAME')
    LOGIN_PASSWORD = os.getenv('KF_LOGIN_PASSWORD')
    # URLs
    BASE_URL = "https://int7.knightfight.moonid.net" if IS_INT_SERVER else "https://de15.knightfight.moonid.net"
    BATTLE_SERVER_URL = f"{BASE_URL}/battleserver/raubzug/"
    REGISTER_URL = "https://moonid.net/account/register/knightfight/"
    LOGIN_URL = "https://moonid.net/account/login/?next=/api/account/connect/286/" if IS_INT_SERVER else "https://moonid.net/account/login/?next=/api/account/connect/238/"
    
    # Target opponent
    TARGET_OPPONENT_ID = "522001088"
    OPPONENT_SEARCH_URL = f"{BASE_URL}/raubzug/gegner/?searchuserid={TARGET_OPPONENT_ID}"
    EFICIENCY_MIN =  os.getenv('KF_EFICIENCY_MIN')
    
    # Timeouts (milliseconds)
    NAVIGATION_TIMEOUT = 30000
    NETWORK_IDLE_TIMEOUT = 10000
    DEFAULT_WAIT = 1000
    LONG_WAIT = 3000
    FINAL_WAIT = 10000
    QUICK_WAIT = 300

    # Timeouts (seconds)
    NEXT_ATTACK_WAIT = 600
    
    # Browser settings
    HEADLESS = os.getenv('HEADLESS', 'true').lower() == 'true'
    # Attack cooldown settings
    ATTACK_COOLDOWN_HOURS = 1  # Martyn can only be attacked once per hour
    CHECK_INTERVAL_SECONDS = 60  # Check every minute if cooldown is over
    
    # Rapid-fire attack settings (to win race against other bots)
    AGGRESSIVE_ATTACK_WINDOW_SECONDS = 10  # Start trying 5 seconds BEFORE cooldown ends
    AGGRESSIVE_RETRY_INTERVAL = 0.5  # Try every 0.5 seconds
    MAX_AGGRESSIVE_ATTEMPTS = 30  # Maximum attempts (covers 15 seconds)
    
    # Paths - using relative paths from project root
    # Get the directory where this config file is located (bot/config/)
    _CONFIG_DIR = Path(__file__).parent.resolve()
    # Go up two levels: bot/config/ -> bot/ -> project_root/
    BASE_DIR = _CONFIG_DIR.parent
    DATA_DIR = BASE_DIR / "data"
    ATTACK_TRACKER_FILE = DATA_DIR / "attack_history.json"

    KNIFE_TRACKER_FILE = BASE_DIR.parent / "bot_data" / "attack_history.json"
    
    # Password settings
    PASSWORD_PREFIX = "KnightFight2025!"
    PASSWORD_LENGTH = 16
    
    @classmethod
    def ensure_directories(cls):
        """Ensure required directories exist"""
        cls.DATA_DIR.mkdir(exist_ok=True)


class FormSelectors:
    """CSS selectors and form field identifiers"""
    
    # Registration form
    EMAIL_FIELD = 'textbox[name="Endereço de e-mail:"]'
    USERNAME_ROW = 'row[name="Nome de utilizador:"]'
    USERNAME_ID = '#id_username'
    PASSWORD_FIELD = 'textbox[name="Senha:"]'
    CONFIRM_PASSWORD_FIELD = 'textbox[name="Confirmar senha:"]'
    TERMS_CHECKBOX = 'checkbox[name="Aceitar termos e condições:"]'
    REGISTER_BUTTON = 'button[name="Registar agora"]'
    
    # Player name form
    TEXT_INPUT = 'input[type="text"]'
    SUBMIT_BUTTON = 'button, input[type="submit"]'
    
    # Attack elements
    ATTACK_IMAGES = 'img[onclick], a img'
    ATTACK_LINKS = 'a[href]'
    VISIBLE_BUTTONS = 'button:visible, input[type="submit"]:visible, a:visible'
    
    # Attack keywords
    ATTACK_KEYWORDS = ['attack', 'sword', 'fight', 'angriff', 'kampf', 'atac', 'raid']
    EXCLUDE_KEYWORDS = ['miss']  # Exclude "missão"
