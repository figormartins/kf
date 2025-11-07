"""
Player service for managing player creation and naming
"""
from datetime import datetime
from bot_battlefield.config.settings import BotSettings
from playwright.sync_api import Page, expect


class PlayerService:
    """Handle player login"""
    
    def __init__(self, page: Page):
        self.page = page

    def __navigate_to_login(self) -> None:
        """Navigate to login page"""
        print("Navigating to login page...")
        self.page.goto("https://moonid.net/account/login/?next=/api/account/connect/286/")
        #self.page.goto("https://moonid.net/account/login/?next=/api/account/connect/238/") ## remover
    
    def __fill_login_form_and_submit_login(self) -> None:
        """Fill login form and submit"""
        print("Filling login form...")
        
        # Fill username
        self.page.locator('form .form input#id_username').fill(BotSettings.LOGIN_USERNAME)
        
        # Fill password
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
            self.__navigate_to_login()
            self.__fill_login_form_and_submit_login()
            
            print("✅ Login successful")
            return True
                
        except Exception as e:
            print(f"⚠️ Error on login: {e}")
            return False
        
    def go_to_battlefield(self) -> None:
        """Navigate to battlefield page"""
        print("Navigating to battlefield page...")
        self.page.goto(BotSettings.BATTLE_SERVER_URL)
        self.page.wait_for_load_state('networkidle')

    def find_zombies_and_attack(self) -> bool:
        """Find zombies on battlefield and attack them"""
        print("Searching for zombies to attack...")
        
       # while True:
        self.page.locator('form[name="enemysearch"] button').click()
        self.page.wait_for_load_state('networkidle')
        self.page.wait_for_timeout(BotSettings.DEFAULT_WAIT)
        enemies_locator = self.page.locator('div.fsbox')
        enemies = enemies_locator.all()
        print("Iniciando análise do inimigo")

        for enemy in enemies:
            #lvl = enemy.locator('.level').inner_text()

            # Status
            status = enemy.locator('.sk4').all()
            strength = int(status[0].inner_text())
            stamina = int(status[1].inner_text())
            dexterity = int(status[2].inner_text())
            fighting_ability = int(status[3].inner_text())
            parry = int(status[4].inner_text())
            print(f"Status - Strength: {strength}, Stamina: {stamina}, Dexterity: {dexterity}, Fighting Ability: {fighting_ability}, Parry: {parry}")

            # Attack
            if  fighting_ability <= 12 or (parry < 30 and fighting_ability < 15):
                enemy.locator('form .fsattackbut').click()
                print("Ataque realizado com sucesso!")
                return True

        return False

    def wait_timer_if_needed(self) -> None:
        """Wait if timer is active on battlefield"""
        print("Waiting for active timer...")
        try:
            counter_locator = self.page.locator("#counter")
            count = counter_locator.count()
            if count == 0:
                print("No active timer found. Continuing...")
                return

            timer_text = counter_locator.inner_text()
            print(f"Timer active: {timer_text}. Waiting...")
            expect(counter_locator).to_be_empty(timeout=BotSettings.NEXT_ATTACK_WAIT * 1000)
        except Exception:
            print("No active timer found. Continuing...")