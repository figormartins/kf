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
    
    def run(self) -> bool:
        """
        Execute single bot cycle: log in → attack
        
        Returns:
            BotSession with execution results
        """
        
        with sync_playwright() as p:
            # Launch browser
            browser = p.chromium.launch(headless=self.headless, executable_path=None)
            page = browser.new_page()
            first_run = True
            
            # Initialize services
            player_service = PlayerService(page)
            player_service.login_player()

            while True:
                player_service.go_to_battlefield()
                
                if first_run:
                    player_service.wait_timer_if_needed()
                    first_run = False
                    continue

                #start attack zombies loop here
                while True:
                    is_attack_performed = player_service.find_zombies_and_attack()

                    if is_attack_performed:
                        print(f"Attack performed at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                        print("Waiting few minutos before next attack...")
                        time.sleep(BotSettings.NEXT_ATTACK_WAIT)
                        break

                
            
            return True

def main():
    """Main entry point - runs in continuous mode"""    
    bot = KnightFightBot(headless=BotSettings.HEADLESS)
    
    cycle = 0
    
    print("\n" + "🔄" * 25)
    print("BOT STARTED - CONTINUOUS MODE - HEADLESS: " + bot.headless.__str__())
    print("Login on main account and attacks zombies repeatedly")
    print("Press Ctrl+C to stop")
    print("🔄" * 25 + "\n")
    
    try:
        while True:
            cycle += 1
            
            print("\n" + "=" * 60)
            print(f"🔄 CYCLE #{cycle} - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            print("=" * 60)
            
            # Run complete bot workflow (account + player + attack)
            session = bot.run()
            
            if session:
                print(f"\n✅ Cycle #{cycle} completed successfully!")
            else:
                print(f"\n⚠️  Cycle #{cycle} failed - retrying...")
                continue
            
            # Small delay before next cycle
            print(f"\n⏳ Waiting 10 seconds before starting cycle #{cycle + 1}...")
            time.sleep(10)
            
    except KeyboardInterrupt:
        print("\n\n" + "=" * 60)
        print(f"⚠️  BOT STOPPED BY USER (Ctrl+C)")
        print(f"Total cycles completed: {cycle}")
        print("=" * 60)
    except Exception as e:
        print(f"\n❌ Error in cycle #{cycle}: {e}")


if __name__ == "__main__":
    main()
