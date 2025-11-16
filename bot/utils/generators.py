"""
Utility functions for name and credential generation
"""
import random
import string
import time
from bot.models import AccountCredentials
from bot.config import BotSettings
from faker import Faker



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
        fake = Faker()
        list_of_domains = (
        'com',
        'com.br',
        'net',
        'net.br',
        'org',
        'org.br',
        'gov',
        'gov.br'
    )
        # Primeiro nome
        first_name = fake.first_name()
        
        # Segundo nome
        last_name = fake.last_name()
        
        # Empresa, tem que cortar só o primeiro nome
        # do nome gerado e remover as virgulas
        # .split()[0] Primeira posição separada por espaços
        # .strip(',') Limpa as virgulas
        company = fake.company().split()[0].strip(',')

        # Gera uma lista de escolhas aleatórias da lista de domínios
        # limitada a um único valor e tiramos ele da lista
        dns_org = fake.random_choices(
            elements=list_of_domains,
            length=1
        )[0]
        
        # Formata o email no formato fulano.tal@empresa.dominio
        # todo em minúsculas
        email = f"{first_name}.{last_name}@{company}.{dns_org}".lower()
        timestamp = int(time.time())
        username = email.split('@')[0]
        
        # Generate strong password
        random_part = ''.join(
            random.choices(string.ascii_letters + string.digits, k=BotSettings.PASSWORD_LENGTH)
        )
        password = f"{BotSettings.PASSWORD_PREFIX}{random_part}"
        
        return AccountCredentials(
            username=username,
            email=email,
            password=email,
            timestamp=timestamp
        )
