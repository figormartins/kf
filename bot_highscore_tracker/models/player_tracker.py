

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
    level: int
    loot: int
    fights: int
    gold_lost: int
    loot_updated_at: datetime = None
    last_fight_at: datetime = None
    gold_lost_at: datetime = None
    gold_difference: int = None

    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization"""
        return {
            'name': self.name,
            'url': self.url,
            'level': self.level,
            'loot': self.loot,
            'loot_updated_at': self.loot_updated_at.isoformat(),
            'fights': self.fights,
            'last_fight_at': self.last_fight_at.isoformat(),
            'gold_lost': self.gold_lost,
            'gold_lost_at': self.gold_lost_at.isoformat(),
            'gold_difference': self.gold_difference
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'PlayerRecord':
        """Create from dictionary"""
        return cls(
            name=data['name'],
            url=data['url'],
            level=data['level'],
            loot=data['loot'],
            loot_updated_at=datetime.fromisoformat(data['loot_updated_at'] or datetime.now().isoformat()),
            fights=data['fights'],
            last_fight_at=datetime.fromisoformat(data['last_fight_at'] or datetime.now().isoformat()),
            gold_lost=data['gold_lost'],
            gold_lost_at=datetime.fromisoformat(data['gold_lost_at'] or datetime.now().isoformat()),
            gold_difference=data['gold_difference']
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

    def record_players(self, list: list[PlayerRecord]):
        """Record a list of players"""
        records = [record.to_dict() for record in list]
        self._save_players(records)
    
    def load_player_records(self) -> list[PlayerRecord]:
        """Load player records from storage"""
        raw_players = self._load_players()
        return [PlayerRecord.from_dict(data) for data in raw_players]

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