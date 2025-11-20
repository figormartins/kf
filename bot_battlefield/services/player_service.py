"""
Player service for managing player creation and naming
"""
from datetime import datetime
import random
import re 
from bot_battlefield.config.settings import BotSettings
from playwright.sync_api import Page, expect


class PlayerService:
    """Handle player login"""
    
    def __init__(self, page: Page):
        self.page = page

    def __navigate_to_login(self) -> None:
        """Navigate to login page"""
        print("Navigating to login page...")
        self.page.goto(BotSettings.LOGIN_URL)
    
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
        self.page.wait_for_load_state('load')
        if not "battleserver" in self.page.url:
            print("With not in battleserver, navigating there...")
            self.page.locator('#content > nav > ul:nth-child(2) > li:nth-child(2) > a').click()
            self.page.wait_for_load_state('networkidle')
        
        expect(self.page).to_have_url(re.compile(".*battleserver"))
        self.page.locator('#content > nav > ul:nth-child(1) > li:nth-child(2) > a').click()
        self.page.wait_for_load_state('load')
        self.page.wait_for_timeout(BotSettings.LONG_WAIT)
        print("Loaded fight")

    def __should_attack_enemy(self, status: list) -> bool:
        """
        Determine if an enemy should be attacked based on their stats
        
        Args:
            status: List of enemy stats
            
        Returns:
            True if enemy meets attack criteria
        """
        # Base
        lvl = int(status[0])
        eficiency = status[1][1:]
        vitality = int(status[3])

        # Equipment
        armor = int(status[4])
        one_hand_weapon = int(status[5])
        two_hand_weapon = int(status[6])

        strength = int(status[7])
        stamina = int(status[8])
        dexterity = int(status[9])
        fighting_ability = int(status[10])
        parry = int(status[11])

        print(f"Level: {lvl}, Eficiency: {eficiency}, Armor: {armor}, 1H Weapon: {one_hand_weapon}, 2H Weapon: {two_hand_weapon}")
        print(f"Status - Strength: {strength}, Stamina: {stamina}, Dexterity: {dexterity}, Fighting Ability: {fighting_ability}, Parry: {parry}")
        
        if BotSettings.IS_INT_SERVER:
            return armor != 0 and one_hand_weapon != 0 and two_hand_weapon != 0 and parry <= 17
        
        
        return ((armor == 91 and one_hand_weapon == 23) or
            (armor == 48 and one_hand_weapon == 65 and
            (fighting_ability > 200 or stamina > 200 or dexterity > 200))) and parry <= 195
        

    def find_zombies_and_attack(self) -> bool:
        """Find zombies on battlefield and attack them"""
        print("\n" + "=" * 90 + "\n" * 2 + "🔍 Searching for zombies to attack...")
        
        scroll_to_locator = "el => el.scrollIntoView({ behavior: 'smooth', block: 'center' })"
        self.page.wait_for_timeout(BotSettings.QUICK_WAIT)
        enemy_search_locator = self.page.locator('form[name="enemysearch"] button')
        enemy_search_locator.evaluate(scroll_to_locator)
        enemy_search_locator.click()
        self.page.wait_for_timeout(BotSettings.DEFAULT_WAIT)
        
        enemies_locator = self.page.locator('div.fsbox')
        enemies = enemies_locator.all()
        random_mod = 4 #random.randint(3, 4)
        count = 1

        for enemy in enemies:
            # Status
            status = [s.inner_text() for s in enemy.locator('tr .fsval').all()]
            name = enemy.locator('.enemyname').inner_text()

            print("\n" + "=" * 90 + "\n")
            print(f"Zombie: {name}")

            # Attack
            if self.__should_attack_enemy(status):
                attack_btn_locator = enemy.locator('form .fsattackbut')
                attack_btn_locator.evaluate(scroll_to_locator)
                attack_btn_locator.click()
                expect(self.page.locator('.batrep-grid3')).to_be_visible(timeout=BotSettings.LONG_WAIT)
                return True
            
            if count % random_mod == 0:
                enemy.evaluate(scroll_to_locator)
                self.page.wait_for_timeout(random.randrange(BotSettings.DEFAULT_WAIT, BotSettings.LONG_WAIT))

            count += 1
        return False

    def wait_timer_if_needed(self) -> bool:
        """Wait if timer is active on battlefield and return True if waited"""
        print("Waiting for active timer...")
        try:
            counter_locator = self.page.locator("#counter")
            count = counter_locator.count()
            if count == 0:
                print("No active timer found. Continuing...")
                return False

            timer_text = counter_locator.inner_text()
            print(f"Timer active: {timer_text}. Waiting...")
            expect(counter_locator).to_be_empty(timeout=BotSettings.NEXT_ATTACK_WAIT * 1000)
            return True
        except Exception:
            print("No active timer found. Continuing...")
            return False