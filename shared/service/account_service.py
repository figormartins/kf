"""
Player service for managing player creation and naming
"""
from datetime import datetime
from bot_battlefield.config.settings import BotSettings
from playwright.sync_api import Page, expect


class AccountService:
    """Handle player login"""
    
    def __init__(self, page: Page, username: str, password: str):
        self.page = page
        self.username = username
        self.password = password

    def _navigate_to_login(self) -> None:
        """Navigate to login page"""
        print("Navigating to login page...")
        self.page.goto("https://moonid.net/account/login/?next=/api/account/connect/286/")
    
    def _fill_login_form_and_submit_login(self) -> None:
        """Fill login form and submit"""

        print("Filling login form...")
        self.page.locator('form .form input#id_username').fill(self.username)
        self.page.locator('form .form input#id_password').fill(self.password)
                
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

            if "https://moonid.net/account/login/" in self.page.url:
                print("⚠️ Login failed - check credentials")
                return False
            
            print("✅ Login successful")
            return True
                
        except Exception as e:
            print(f"⚠️ Error on login: {e}")
            return False
        
    def remove_account(self) -> bool:
        """Remove the logged-in account"""
        try:
            print("Navigating to account removal page...")
            self.page.goto("https://moonid.net/account/data/")
            self.page.wait_for_load_state('networkidle')
            
            print("Submitting account removal form...")
            self.page.locator('#id_confirmed').click()
            self.page.locator('#content > div > div > div.subcolumn.right > div > div > form > table > tbody > tr:nth-child(2) > td:nth-child(2) > input').click()
            self.page.wait_for_load_state('networkidle')
            
            print("✅ Account removal successful")
            return True
        except Exception as e:
            print(f"⚠️ Error on account removal: {e}")
            return False