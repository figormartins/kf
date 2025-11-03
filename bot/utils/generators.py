"""
Utility functions for name and credential generation
"""
import random
import string
import time
from bot.models import AccountCredentials
from bot.config import BotSettings


class NameGenerator:
    """Generate random player names"""
    
    FIRST_NAMES = [
        'Arthur', 'Lancelot', 'Percival', 'Galahad', 'Gawain',
        'Tristan', 'Bedivere', 'Kay', 'Gareth', 'Mordred',
        'Roland', 'Oliver', 'Baldwin', 'Godfrey', 'Richard',
        'William', 'Edward', 'Henry', 'Geoffrey', 'Robert',
        'Thor', 'Odin', 'Bjorn', 'Ragnar', 'Erik',
        'Sigurd', 'Harald', 'Magnus', 'Leif', 'Sven'
    ]
    
    LAST_NAMES = [
        'Pendragon', 'Lionheart', 'Ironside', 'Blackwood', 'Stormborn',
        'Dragonslayer', 'Nightblade', 'Thunderfist', 'Shadowcaster', 'Flameheart',
        'Frostbeard', 'Steelhammer', 'Wolfbane', 'Ravenwind', 'Goldenshield',
        'Darkheart', 'Swiftblade', 'Strongarm', 'Firebrand', 'Icevein',
        'Stonemace', 'Bloodaxe', 'Windwalker', 'Earthshaker', 'Stormbringer'
    ]
    
    @classmethod
    def generate_random_name(cls) -> str:
        """
        Generate a unique concatenated player name
        Examples: ThorThunderfist687950, ArthurDragonslayer42857
        """
        first_name = random.choice(cls.FIRST_NAMES)
        last_name = random.choice(cls.LAST_NAMES)
        
        # Randomly choose between timestamp or random number
        use_timestamp = random.choice([True, False])
        
        if use_timestamp:
            # Use last 4-6 digits of timestamp
            timestamp = str(int(time.time()))
            suffix = timestamp[-random.randint(4, 6):]
        else:
            # Use random 3-5 digit number
            suffix = str(random.randint(100, 99999))
        
        return f"{first_name}{last_name}{suffix}"


class CredentialsGenerator:
    """Generate account credentials"""
    
    @staticmethod
    def generate_credentials() -> AccountCredentials:
        """Generate random account credentials"""
        timestamp = int(time.time())
        username = f"user_{timestamp}"
        email = f"{username}@example.com"
        
        # Generate strong password
        random_part = ''.join(
            random.choices(string.ascii_letters + string.digits, k=BotSettings.PASSWORD_LENGTH)
        )
        password = f"{BotSettings.PASSWORD_PREFIX}{random_part}"
        
        return AccountCredentials(
            username=username,
            email=email,
            password=password,
            timestamp=timestamp
        )
