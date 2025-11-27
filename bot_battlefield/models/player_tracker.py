

from dataclasses import dataclass
from datetime import datetime
import json
from pathlib import Path
from typing import Optional


@dataclass
class PlayerRecord:
    """Record of a player's highscore"""
    name: str
    url: str
    attacked_at: datetime
    data: str
    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization"""
        return {
            'name': self.name,
            'url': self.url,
            'attacked_at': self.attacked_at.isoformat(),
            'data': self.data
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'PlayerRecord':
        """Create from dictionary"""
        return cls(
            name=data['name'],
            url=data['url'],
            attacked_at=datetime.fromisoformat(data['attacked_at']),
            data=data['data']
        )
    
class PlayerTracker:
    """Manages player tracking"""

    def __init__(self, storage_path: Path):
        self.storage_path = storage_path
        self.storage_path.parent.mkdir(parents=True, exist_ok=True)
    
    def record_player(self, record: PlayerRecord):
        """Record a successful player"""
        players = self._load_players()
        players.append(record.to_dict())
        self._save_players(players)

    def _load_players(self) -> list:
        """Load player records from storage"""
        if not self.storage_path.exists():
            return []
        
        try:
            with open(self.storage_path, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return []
    
    def _save_players(self, players: list):
        """Save player records to storage"""
        with open(self.storage_path, 'w') as f:
            json.dump(players, f, indent=2)