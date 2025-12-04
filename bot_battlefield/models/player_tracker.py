

from dataclasses import dataclass
from datetime import datetime, timedelta
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

    def get_players(self) -> list[PlayerRecord]:
        """Get all tracked players"""
        players_data = self.__load_players()
        return [PlayerRecord.from_dict(p) for p in players_data]
    
    def get_players_available_to_attack(self) -> list[PlayerRecord]:
        """Get players that were attacked more than 12 hours ago"""
        now = datetime.now()
        threshold = timedelta(hours=12)
        
        all_players = self.get_players()
        return [
            p for p in all_players
            if (now - p.attacked_at) >= threshold
        ]
    
    def record_player(self, record: PlayerRecord):
        """Record a successful player"""
        players = self.__load_players()
        filtered_players = [
            p for p in players
            if p['url'] != record.url
        ]
        filtered_players.append(record.to_dict())
        self._save_players(filtered_players)

    def remove_player(self, record: PlayerRecord):
        """Remove a player from tracking"""
        players = self.__load_players()
        filtered_players = [
            p for p in players
            if p['url'] != record.url
        ]
        self._save_players(filtered_players)

    def __load_players(self) -> list:
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