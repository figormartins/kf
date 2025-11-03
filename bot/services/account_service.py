"""
Account registration service
"""
from playwright.sync_api import Page
from bot.models import AccountCredentials
from bot.config import BotSettings
from bot.utils import ScreenshotManager


class AccountService:
    """Handle account registration operations"""
    
    def __init__(self, page: Page, screenshot_manager: ScreenshotManager):
        self.page = page
        self.screenshot_manager = screenshot_manager
    
    def navigate_to_registration(self) -> None:
        """Navigate to registration page"""
        print("Navigating to site...")
        self.page.goto(BotSettings.RAID_URL)
        
        print("Clicking registration button...")
        self.page.get_by_role('link', name='Register and Play!').click()
        self.page.wait_for_load_state('networkidle')
    
    def fill_registration_form(self, credentials: AccountCredentials) -> None:
        """
        Fill registration form with credentials
        
        Args:
            credentials: Account credentials to use
        """
        print("Filling registration form...")
        
        # Email
        self.page.locator('.container form table #id_email').fill(credentials.email)
        ##self.page.get_by_role('textbox', name='E-mail address:').fill(credentials.email)
        
        # Username
        self.page.locator('.container form table #id_username').fill(credentials.username)
        # self.page.get_by_role('row', name='Nome de utilizador:').locator('#id_username').fill(
        #     credentials.username
        # )
        
        # password
        self.page.locator('.container form table #id_password1').fill(credentials.password)
        ##self.page.get_by_role('textbox', name='Senha:', exact=True).fill(credentials.password)
        
        # Confirm password
        self.page.locator('.container form table #id_password2').fill(credentials.password)
        ##self.page.get_by_role('textbox', name='Confirmar senha:').fill(credentials.password)
        
        # Accept terms
        self.page.locator('.container form table #id_terms_accepted').check()
        ##self.page.get_by_role('checkbox', name='Aceitar termos e condições:').check()
    
    def submit_registration(self) -> str:
        """
        Submit registration form and return final URL
        
        Returns:
            Final URL after registration
        """
        print("Submitting registration form...")
        self.page.locator('.container form table input.register').click()
        ##self.page.get_by_role('button', name='Registar agora').click()
        
        print("Waiting for response...")
        try:
            self.page.wait_for_load_state('networkidle', timeout=BotSettings.NAVIGATION_TIMEOUT)
        except Exception as e:
            print(f"Warning: {e}")
        
        ##self.page.wait_for_timeout(BotSettings.LONG_WAIT)
        return self.page.url
    
    def register_account(self, credentials: AccountCredentials) -> bool:
        """
        Complete account registration process
        
        Args:
            credentials: Account credentials to register
            
        Returns:
            True if registration successful, False otherwise
        """
        try:
            self.navigate_to_registration()
            self.fill_registration_form(credentials)
            final_url = self.submit_registration()
            
            print(f"\nFinal URL: {final_url}")
            
            # Check if redirected to main/game page (success)
            success = any(keyword in final_url for keyword in ['main', 'game', 'raubzug'])
            
            if success:
                print("\n✅ Account created successfully!")
            else:
                print("\n⚠️ Account creation may have failed")
            
            return success
        except Exception as e:
            print(f"❌ Error during registration: {e}")
            return False
