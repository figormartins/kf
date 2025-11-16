"""
Attack scheduling service with cooldown management

Simplified flow:
1. Load attack history
2. Check cooldown
3. Wait if necessary
4. Continuously attempt attack until success
"""
from datetime import datetime, timedelta
import time
from typing import Optional
from playwright.sync_api import Page

from ..config.settings import BotSettings
from ..models.attack_tracker import AttackTracker, AttackRecord
from ..models.entities import Player
from .attack_service import AttackService


class AttackScheduler:
    """Simplified attack scheduler - handles cooldown and continuous attack attempts"""
    
    def __init__(self, page: Page, screenshot_manager):
        self.page = page
        self.screenshot_manager = screenshot_manager
        self.attack_service = AttackService(page, screenshot_manager)
        self.tracker = AttackTracker(BotSettings.ATTACK_TRACKER_FILE)
    
    def schedule_attack(self, player: Player, opponent_id: str) -> bool:
        """
        Main attack flow:
        1. Load attack history
        2. Check cooldown
        3. Wait if necessary
        4. Continuously attempt attack
        
        Args:
            player: Player performing the attack
            opponent_id: Target opponent ID
            
        Returns:
            bool: True if attack succeeded, False otherwise
        """
        print("\n" + "="*50)
        print("🎯 STARTING ATTACK SEQUENCE")
        print("="*50)
        
        # 1. Check cooldown
        can_attack, next_available, reason = self.tracker.can_attack(opponent_id)
        
        if not can_attack:
            wait_seconds = (next_available - datetime.now()).total_seconds()
            
            print(f"\n⏰ COOLDOWN ACTIVE")
            print(f"   {reason}")
            print(f"   Next attack available at: {next_available.strftime('%H:%M:%S')}")
            print(f"   Waiting for: {self._format_time(int(wait_seconds))}")
            print(f"   Current time: {datetime.now().strftime('%H:%M:%S')}")
            
            # 2. Wait for cooldown
            self._wait_with_countdown(int(wait_seconds))
        else:
            print(f"\n✅ NO COOLDOWN - Ready to attack!")
        
        # 3. Continuously attempt attack until success
        print(f"\n🔄 STARTING CONTINUOUS ATTACK ATTEMPTS...")
        return self._attempt_attack_continuously(player, opponent_id)
    
    def _wait_with_countdown(self, seconds: int):
        """Wait with visual countdown"""
        if seconds <= 0:
            return
        
        # Start 5 seconds before cooldown ends for aggressive timing
        aggressive_start = max(0, seconds - BotSettings.AGGRESSIVE_ATTACK_WINDOW_SECONDS)
        
        if aggressive_start > 0:
            print(f"\n⏳ Waiting {self._format_time(aggressive_start)} until aggressive window...")
            time.sleep(aggressive_start)
            seconds -= aggressive_start
        
        # Final countdown
        print(f"\n⚡ AGGRESSIVE WINDOW - {seconds}s until attack available")
        for remaining in range(seconds, 0, -1):
            print(f"   ⏱️  {remaining}s...", end='\r')
            time.sleep(1)
        print("\n")
    
    def _attempt_attack_continuously(
        self, 
        player: Player, 
        opponent_id: str, 
        max_attempts: int = 50, 
        interval: float = 0.5
    ) -> bool:
        """
        Continuously attempt attack until success or max attempts reached
        
        Args:
            player: Player performing the attack
            opponent_id: Target opponent ID
            max_attempts: Maximum number of attempts (default: 30)
            interval: Seconds between attempts (default: 0.5)
            
        Returns:
            bool: True if attack succeeded
        """
        print(f"🎯 Attempting attack every {interval}s (max {max_attempts} attempts)")
        
        print(f"   📍 Navigating to opponent page...")
        opponent_url = f"{BotSettings.BASE_URL}/raubzug/gegner/?searchuserid={opponent_id}"
        record = AttackRecord(
                    opponent_id=opponent_id,
                    timestamp=datetime.now(),
                    player_name=player.name,
                    attack_successful=True,
                    email=player.credentials.email,
                    username=player.credentials.username,
                    password=player.credentials.password
                )
        for attempt in range(1, max_attempts + 1):
            
            print(f"\n📍 Attempt {attempt}/{max_attempts}")
            # Pre-navigate to opponent page
            try:
                self.page.goto(
                    opponent_url,
                    timeout=BotSettings.LONG_WAIT,
                    wait_until='networkidle'
                )
                print(f"   ✅ Page loaded - ready to attack!")
                timestamp = int(datetime.now().timestamp())
                attack_result = self.attack_service.perform_attack(opponent_id, timestamp)
            except Exception as e:
                print(f"   ⚠️ Navigation warning: {str(e)}")
                continue
                
            if attack_result.success:
                # SUCCESS! Record the attack
                record.timestamp = datetime.now()
                self.tracker.record_attack(record)
                
                print(f"\n🎉 ATTACK SUCCESSFUL!")
                print(f"   ✅ Attack recorded at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                break
            else:
                print(f"   ❌ Attack failed")
        
        record.timestamp = datetime.now()
        record.attack_successful = False

        self.tracker.record_attack(record)
        return record.attack_successful

    
    def _format_time(self, seconds: int) -> str:
        """Format seconds into readable time string"""
        if seconds < 60:
            return f"{seconds}s"
        
        minutes = seconds // 60
        secs = seconds % 60
        
        if minutes < 60:
            return f"{minutes}m {secs}s"
        
        hours = minutes // 60
        mins = minutes % 60
        return f"{hours}h {mins}m {secs}s"

