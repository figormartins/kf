"""
Player service for managing player creation and naming
"""
from datetime import datetime
from bot_battlefield.config.settings import BotSettings
from playwright.sync_api import Page, expect


class AccountService:
    """Handle player login"""
    
    def __init__(self, page: Page):
        self.page = page

    def _navigate_to_login(self) -> None:
        """Navigate to login page"""
        print("Navigating to login page...")
        self.page.goto("https://moonid.net/account/login/?next=/api/account/connect/286/")
    
    def _fill_login_form_and_submit_login(self) -> None:
        """Fill login form and submit"""

        print("Filling login form...")
        self.page.locator('form .form input#id_username').fill(BotSettings.LOGIN_USERNAME)
        self.page.locator('form .form input#id_password').fill(BotSettings.LOGIN_PASSWORD)
                
        # Submit form
        print("Submitting login form...")
        self.page.locator('form .form input.btn').click()
        self.page.wait_for_load_state('networkidle')
    
    def login_player(self) -> bool:
        """
        Login existing player
        Returns:
            True if login successful

        """

        print("Continuing with Login selection process...")
        
        try:
            self._navigate_to_login()
            self._fill_login_form_and_submit_login()
            
            print("✅ Login successful")
            return True
                
        except Exception as e:
            print(f"⚠️ Error on login: {e}")
            return False