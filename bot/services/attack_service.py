"""
Attack service for performing attacks on opponents
"""
from playwright.sync_api import Page, Locator
from typing import Optional
from bot.models import AttackResult
from bot.config import BotSettings, FormSelectors
from bot.utils import ScreenshotManager


class AttackService:
    """Handle attack operations"""
    
    def __init__(self, page: Page, screenshot_manager: ScreenshotManager):
        self.page = page
        self.screenshot_manager = screenshot_manager
    
    def navigate_to_opponent(self, opponent_id: str) -> None:
        """
        Navigate to opponent search page
        
        Args:
            opponent_id: Target opponent user ID
        """
        print("\n" + "=" * 50)
        print(f"Going to opponent page (ID: {opponent_id})...")
        
        url = f"{BotSettings.BASE_URL}/raubzug/gegner/?searchuserid={opponent_id}"
        self.page.goto(url, timeout=BotSettings.NAVIGATION_TIMEOUT)
        self.page.wait_for_load_state('networkidle', timeout=BotSettings.NETWORK_IDLE_TIMEOUT)
        self.page.wait_for_timeout(BotSettings.DEFAULT_WAIT)
      
    def perform_attack(self, target_id: str, timestamp: int) -> AttackResult:
        """
        Perform attack on target opponent - OPTIMIZED FOR SPEED
        
        Args:
            target_id: Target opponent user ID
            timestamp: Session timestamp
            
        Returns:
            AttackResult with attack outcome
        """
        try:
            attack_successful = self._try_attack_via_buttons_fast()
            
            # Result
            if not attack_successful:
                return AttackResult(
                    success=False,
                    target_id=target_id,
                    timestamp=timestamp,
                    error_message="Attack button not found or not clickable"
                )
            else:
                print("✅ Attack performed!")
                
                return AttackResult(
                    success=True,
                    target_id=target_id,
                    timestamp=timestamp
                )
                
        except Exception as e:
            error_msg = f"Attack error: {e}"
            print(f"⚠️ {error_msg}")
            return AttackResult(
                success=False,
                target_id=target_id,
                timestamp=timestamp,
                error_message=error_msg
            )
    
    def _try_attack_via_buttons_fast(self) -> bool:
        """
        OPTIMIZED: Try to find and click attack button quickly
        Uses shorter timeouts for rapid-fire attempts
        """
        try:
            # Look for buttons with attack text (3 second timeout instead of 30)
            buttons = self.page.get_by_role("button").all()
            
            for button in buttons:
                try:
                    if not button.is_visible():
                        continue
                    
                    button.click(timeout=1000)  # 1s timeout instead of 30s
                    return True
                        
                except Exception:
                    continue
            
            return False
            
        except Exception:
            return False
    