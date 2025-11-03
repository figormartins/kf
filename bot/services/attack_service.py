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
    
    def _try_attack_via_images(self) -> bool:
        """Try to find and click attack via images"""
        print("Looking for clickable attack images...")
        images = self.page.locator(FormSelectors.ATTACK_IMAGES).all()
        print(f"Found {len(images)} images")
        
        for img in images:
            try:
                src = img.get_attribute('src') or ''
                alt = img.get_attribute('alt') or ''
                onclick = img.get_attribute('onclick') or ''
                
                # Check if image contains attack-related keywords
                if any(keyword in src.lower() for keyword in FormSelectors.ATTACK_KEYWORDS) or \
                   any(keyword in alt.lower() for keyword in FormSelectors.ATTACK_KEYWORDS) or \
                   any(keyword in onclick.lower() for keyword in FormSelectors.ATTACK_KEYWORDS):
                    print(f"Found attack image: src={src}, alt={alt}")
                    
                    if onclick:
                        img.click()
                        self.page.wait_for_timeout(BotSettings.LONG_WAIT)
                        return True
                    else:
                        parent = img.locator('xpath=..').first
                        if parent:
                            parent.click()
                            self.page.wait_for_timeout(BotSettings.LONG_WAIT)
                            return True
            except Exception as e:
                print(f"Error trying to click image: {e}")
                continue
        
        return False
    
    def _try_attack_via_links(self) -> bool:
        """Try to find and click attack via specific links"""
        print("Looking for specific attack links...")
        links = self.page.locator(FormSelectors.ATTACK_LINKS).all()
        print(f"Found {len(links)} links")
        
        for link in links:
            try:
                href = link.get_attribute('href') or ''
                text = link.inner_text() if link.is_visible() else ""
                
                # Look for links with attack parameters
                if any(keyword in href.lower() for keyword in ['attack', 'angriff']) and \
                   ('?' in href or '&' in href):
                    print(f"Found specific attack link: {href} | Text: {text}")
                    if link.is_visible():
                        link.click()
                        self.page.wait_for_timeout(BotSettings.LONG_WAIT)
                        return True
            except:
                continue
        
        return False
    
    def _try_attack_via_buttons(self) -> bool:
        """Try to find and click attack via visible buttons"""
        print("Looking for buttons with attack text...")
        visible_buttons = self.page.locator(FormSelectors.VISIBLE_BUTTONS).all()
        print(f"Found {len(visible_buttons)} visible elements")
        
        for btn in visible_buttons:
            try:
                text = btn.inner_text().lower()
                
                # Check for attack-specific words (excluding "missão")
                if any(keyword in text for keyword in FormSelectors.ATTACK_KEYWORDS) and \
                   not any(exclude in text for exclude in FormSelectors.EXCLUDE_KEYWORDS):
                    print(f"Trying to click button with text: {text}")
                    btn.click()
                    self.page.wait_for_timeout(BotSettings.LONG_WAIT)
                    return True
            except:
                continue
        
        return False
    
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
    