"""
Data models for KnightFight Bot
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class AccountCredentials:
    """Account credentials for registration and login"""
    username: str
    email: str
    password: str
    timestamp: int
    
    def __repr__(self):
        return f"AccountCredentials(username={self.username}, email={self.email})"


@dataclass
class Player:
    """Player information"""
    name: str
    credentials: AccountCredentials
    created_at: datetime
    is_registered: bool = False
    
    def __repr__(self):
        return f"Player(name={self.name}, username={self.credentials.username})"


@dataclass
class AttackResult:
    """Result of an attack attempt"""
    success: bool
    target_id: str
    timestamp: int
    screenshot_path: Optional[str] = None
    error_message: Optional[str] = None
    
    def __repr__(self):
        status = "Success" if self.success else f"Failed: {self.error_message}"
        return f"AttackResult(target={self.target_id}, {status})"


@dataclass
class BotSession:
    """Bot execution session data"""
    player: Player
    attack_result: Optional[AttackResult] = None
    screenshots: list[str] = None
    
    def __post_init__(self):
        if self.screenshots is None:
            self.screenshots = []
    
    def add_screenshot(self, path: str):
        """Add screenshot path to session"""
        self.screenshots.append(path)
    
    def summary(self) -> dict:
        """Get session summary"""
        # Handle attack_result being either AttackResult object or dict
        attack_success = None
        if self.attack_result:
            if isinstance(self.attack_result, dict):
                attack_success = self.attack_result.get('success')
            else:
                attack_success = self.attack_result.success
        
        return {
            'player_name': self.player.name,
            'username': self.player.credentials.username,
            'email': self.player.credentials.email,
            'password': self.player.credentials.password,
            'is_registered': self.player.is_registered,
            'attack_success': attack_success,
            'screenshots_count': len(self.screenshots)
        }
