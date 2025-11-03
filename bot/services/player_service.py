"""
Player service for managing player creation and naming
"""
from datetime import datetime
from playwright.sync_api import Page
from bot.models import Player, AccountCredentials
from bot.config import BotSettings
from bot.utils import NameGenerator, ScreenshotManager


class PlayerService:
    """Handle player creation and naming operations"""
    
    def __init__(self, page: Page, screenshot_manager: ScreenshotManager):
        self.page = page
        self.screenshot_manager = screenshot_manager
    
    def create_player(self, credentials: AccountCredentials) -> Player:
        """
        Create player with generated name
        
        Args:
            credentials: Account credentials
            
        Returns:
            Player object
        """
        player_name = NameGenerator.generate_random_name()
        print(f"Generated player name: {player_name}")
        
        return Player(
            name=player_name,
            credentials=credentials,
            created_at=datetime.now(),
            is_registered=False
        )
    
    def register_player_name(self, player: Player, timestamp: int) -> bool:
        """
        Register player name in-game
        
        Args:
            player: Player object with name to register
            timestamp: Session timestamp
            
        Returns:
            True if name registered successfully
        """
        print("Continuing with name selection process...")
        print(f"Chosen name: {player.name}")
        
        # Wait for page to load
        self.page.wait_for_timeout(BotSettings.DEFAULT_WAIT)
        
        # Try to find and fill name field
        print("Looking for name field...")
        try:
            self.page.wait_for_timeout(BotSettings.DEFAULT_WAIT)
            
            # Find text input fields
            inputs = self.page.locator('input[type="text"]').all()
            print(f"Found {len(inputs)} text fields")
            
            if len(inputs) > 0:
                # Fill first text field with name
                inputs[0].fill(player.name)
                print(f"Name '{player.name}' entered in field")
                
                # Look for submit button
                self.page.wait_for_timeout(1000)
                
                # Find and click confirmation button
                buttons = self.page.locator('button, input[type="submit"]').all()
                if len(buttons) > 0:
                    print("Clicking confirmation button...")
                    buttons[0].click()
                    self.page.wait_for_timeout(BotSettings.LONG_WAIT)
                    
                    print("✅ Name registered!")
                    player.is_registered = True
                    return True
                else:
                    print("⚠️ No confirmation button found")
                    return False
            else:
                print("⚠️ No text field found on page")
                return False
                
        except Exception as e:
            print(f"⚠️ Error trying to fill name: {e}")
            return False
