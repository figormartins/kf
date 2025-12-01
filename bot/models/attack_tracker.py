"""
Attack tracking and cooldown management

This module handles tracking of attacks to enforce the 1-hour cooldown rule.
Martyn can only receive one attack per hour, so we need to:
1. Track when the last attack occurred
2. Wait until cooldown expires
3. Attack immediately when available (race against other bots)
"""
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
import json
from typing import Optional


@dataclass
class AttackRecord:
    """Record of an attack on an opponent"""
    opponent_id: str
    timestamp: datetime
    player_name: str
    attack_successful: bool
    email: str
    username: str
    password: str
    
    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization"""
        return {
            'opponent_id': self.opponent_id,
            'timestamp': self.timestamp.isoformat(),
            'player_name': self.player_name,
            'attack_successful': self.attack_successful,
            'email': self.email,
            'username': self.username,
            'password': self.password
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'AttackRecord':
        """Create from dictionary"""
        return cls(
            opponent_id=data['opponent_id'],
            timestamp=datetime.fromisoformat(data['timestamp']),
            player_name=data['player_name'],
            attack_successful=data['attack_successful'],
            email=data.get('email', ''),
            username=data.get('username', ''),
            password=data.get('password', '')
        )


class AttackTracker:
    """Manages attack cooldown tracking"""
    
    COOLDOWN_HOURS = 1
    
    def __init__(self, storage_path: Path):
        self.storage_path = storage_path
        self.storage_path.parent.mkdir(parents=True, exist_ok=True)
    
    def record_attack(self, record: AttackRecord):
        """Record a successful attack"""
        attacks = self._load_attacks()
        attacks.append(record.to_dict())
        self._save_attacks(attacks)
    
    def get_last_attack(self, opponent_id: str) -> Optional[AttackRecord]:
        """Get the last attack record for an opponent"""
        attacks = self._load_attacks()
        opponent_attacks = [
            AttackRecord.from_dict(a) 
            for a in attacks 
            if a['opponent_id'] == opponent_id and a['attack_successful']
        ]
        
        if not opponent_attacks:
            return None
        
        # Return the most recent attack
        return max(opponent_attacks, key=lambda x: x.timestamp)
    
    def get_attacks(self) -> list[AttackRecord]:
        """Get attacks records up to 8 PM of the previous day"""
        attacks = self._load_attacks()
        opponent_attacks = [
            AttackRecord.from_dict(a) 
            for a in attacks
        ]

        if not opponent_attacks:
            return []

        now = datetime.now(timezone.utc).astimezone()
        # Yesterday at 8 PM (20:00)
        cutoff_time = now.replace(hour=20, minute=0, second=0, microsecond=0) - timedelta(days=1)
        
        filtered_list = [
            item for item in opponent_attacks
            if item.timestamp.replace(tzinfo=timezone.utc).astimezone() < cutoff_time
        ]

        return filtered_list
    
    def remove_attack(self, email: str):
        """Remove attack records for a given email"""
        attacks = self._load_attacks()
        filtered_attacks = [a for a in attacks if a.get('email') != email]
        self._save_attacks(filtered_attacks)

    def can_attack(self, opponent_id: str) -> tuple[bool, Optional[datetime], Optional[str]]:
        """
        Check if opponent can be attacked
        
        Returns:
            tuple: (can_attack: bool, next_available: Optional[datetime], reason: Optional[str])
        """
        last_attack = self.get_last_attack(opponent_id)
        
        if last_attack is None:
            return True, None, None
        
        cooldown_end = last_attack.timestamp + timedelta(hours=self.COOLDOWN_HOURS)
        now = datetime.now()
        
        if now >= cooldown_end:
            return True, None, None
        
        time_remaining = cooldown_end - now
        reason = (
            f"Cooldown active. Last attack by '{last_attack.player_name}' "
            f"at {last_attack.timestamp.strftime('%Y-%m-%d %H:%M:%S')}. "
            f"Next available in {self._format_timedelta(time_remaining)}."
        )
        
        return False, cooldown_end, reason
    
    def _format_timedelta(self, td: timedelta) -> str:
        """Format timedelta to human readable string"""
        total_seconds = int(td.total_seconds())
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60
        
        if hours > 0:
            return f"{hours}h {minutes}m {seconds}s"
        elif minutes > 0:
            return f"{minutes}m {seconds}s"
        else:
            return f"{seconds}s"
    
    def _load_attacks(self) -> list:
        """Load attack records from storage"""
        if not self.storage_path.exists():
            return []
        
        try:
            with open(self.storage_path, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return []
    
    def _save_attacks(self, attacks: list):
        """Save attack records to storage"""
        with open(self.storage_path, 'w') as f:
            json.dump(attacks, f, indent=2)
