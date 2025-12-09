#!/usr/bin/env python3
"""
Battlefield Bot - Main Entry Point

Continuous mode:
Login → Go to BF → Attacks Zombies
"""
import time
from datetime import datetime
from bot_battlefield.config.settings import BotSettings
from bot_battlefield.services.player_service import PlayerService
from playwright.sync_api import sync_playwright


class KnightFightBot:
    """Main bot orchestrator"""
    
    def __init__(self, headless: bool = False):
        self.headless = headless
    
    def run(self) -> None:
        """
        Execute single bot cycle: log in → attack
        
        Returns:
            BotSession with execution results
        """
        while True:
            with sync_playwright() as p:
                # Launch browser
                browser = p.chromium.launch(headless=self.headless, executable_path=None)
                page = browser.new_page()
                
                # Initialize services
                player_service = PlayerService(page)
                player_service.login_player()

                while True:
                    try:
                        player_service.go_to_battlefield()
                        if player_service.wait_timer_if_needed(): continue
                        start_time = time.perf_counter()

                        while True:
                            is_attack_performed = player_service.find_zombies_and_attack()

                            if is_attack_performed:
                                print("\n" + f"⚔️  Attack performed at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                                end_time = time.perf_counter()
                                request_duration = end_time - start_time
                                print(f"⏰ Attack to zombie took {request_duration:.2f} seconds.")
                                break
                    except StopIteration as si:
                        print(si)
                        break
                    except Exception as e:
                        print(f"⚠️ Error during battlefield operations: {e}")


def main():
    """Main entry point - runs in continuous mode"""
    BotSettings.ensure_directories()
    bot = KnightFightBot(headless=BotSettings.HEADLESS)
        
    print("\n" + "🔄" * 60)
    print("BOT STARTED - CONTINUOUS MODE - HEADLESS: " + bot.headless.__str__())
    print("Login on main account and attacks zombies repeatedly")
    print("Press Ctrl+C to stop")
    print("🔄" * 60 + "\n")
    
    print("\n" + "=" * 60)
    print("Running on " + ("INT7" if BotSettings.IS_INT_SERVER else "DE15") + " server and efficiency: " + BotSettings.EFICIENCY_MIN)
    print(f"Attacks started - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    bot.run()

if __name__ == "__main__":
    main()
