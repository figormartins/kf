#!/usr/bin/env python3
"""
Battlefield Bot - Main Entry Point

Continuous mode:
Login → Go to BF → Attacks Zombies using Ids
"""
import time
import re
from datetime import datetime
from bot_battlefield.config.settings import BotSettings
from bot_battlefield.models.player_tracker import PlayerTracker
from bot_battlefield.services.player_service import PlayerService
from playwright.sync_api import sync_playwright


class KnightFightBot:
    """Main bot orchestrator"""
    
    def __init__(self, headless: bool = False):
        self.headless = headless
        self.tracker = PlayerTracker(BotSettings.ATTACK_TRACKER_FILE)
    
    @staticmethod
    def extract_player_id(url: str) -> str:
        """
        Extract player ID from URL
        
        Args:
            url: URL in format "https://int7.knightfight.moonid.net/battleserver/player/2941436821/"
            
        Returns:
            Player ID as string: "2941436821"
        """
        match = re.search(r'/player/(\d+)/?$', url)
        if match:
            return match.group(1)
        raise ValueError(f"Could not extract player ID from URL: {url}")
    
    def run(self) -> None:
        """
        Execute single bot cycle: log in → attack
        
        Returns:
            BotSession with execution results
        """
        
        with sync_playwright() as p:
            # Launch browser
            browser = p.chromium.launch(headless=self.headless, executable_path=None)
            page = browser.new_page()
            #Each knight can only be attacked once every 60 minutes!
 
            # Initialize services
            player_service = PlayerService(page)
            player_service.login_player()
            page.goto(f"{BotSettings.BASE_URL}/raubzug/")
            player_service.wait_timer_if_needed()

            while True:
                try:

                    player_id = "522000450" #### TARGET OPPONENT ID
                    is_attack_performed = player_service.find_player_and_attack_by_id(player_id)
                    if is_attack_performed:
                        print("\n" + f"⚔️  Attack performed at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                        break

                except Exception as e:
                    print(f"⚠️ Error during battlefield operations: {e}")


def main():
    """Main entry point - runs in continuous mode"""
    BotSettings.ensure_directories()
    bot = KnightFightBot(headless=BotSettings.HEADLESS)
        
    print("\n" + "🔄" * 60)
    print("BOT STARTED - CONTINUOUS MODE - HEADLESS: " + bot.headless.__str__())
    print("Login on main account and attacks target opponent when available.")
    print("Press Ctrl+C to stop")
    print("🔄" * 60 + "\n")
    
    print("\n" + "=" * 60)
    print("Running on " + ("INT7" if BotSettings.IS_INT_SERVER else "DE15") + " server and efficiency: " + BotSettings.EFICIENCY_MIN)
    print(f"Attacks started - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    bot.run()

if __name__ == "__main__":
    main()
