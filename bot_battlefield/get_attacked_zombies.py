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


class KnightFightGetBots:
    """Main bot orchestrator"""
    
    def __init__(self, headless: bool = False):
        self.headless = headless
    
    def run(self) -> None:
        """
        Execute single bot cycle: log in → get attacked zombies on battlefield
        
        Returns:
            BotSession with execution results
        """
        
        with sync_playwright() as p:
            # Launch browser
            self.headless = False
            browser = p.chromium.launch(headless=self.headless, executable_path=None)
            page = browser.new_page()
            
            # Initialize services
            player_service = PlayerService(page)
            player_service.login_player()

            try:
                player_service.go_to_battlefield()
                player_service.wait_timer_if_needed()
                player_service.go_to_battle_reports()

                while True:
                    # Extract all dates and enemies from battle reports
                    battle_data = page.evaluate("""
                        () => {
                            const rows = document.querySelectorAll('table tbody tr');
                            const data = [];
                            
                            for (let i = 0; i < rows.length; i += 2) {
                                const dateCell = rows[i].querySelector('td.tdn.center.w20.dyntext');
                                const enemyCell = rows[i].querySelector('td.tdn.center.w25.dyntext.breakword a');
                                
                                if (dateCell && enemyCell) {
                                    data.push({
                                        date: dateCell.textContent.trim(),
                                        enemy: enemyCell.textContent.trim()
                                    });
                                }
                            }
                            return data;
                        }
                    """)
                    print(battle_data)
                    page.locator("table .r.w30 a").click()
                    time.sleep(10)
            except Exception as e:
                print(f"⚠️ Error during battlefield operations: {e}")


def main():
    """Main entry point - runs in continuous mode"""
    BotSettings.ensure_directories()
    bot = KnightFightGetBots(headless=BotSettings.HEADLESS)
        
    print("\n" + "🔄" * 60)
    print("BOT STARTED - HEADLESS: " + bot.headless.__str__())
    print("Login on main account and get attacked zombies")
    print("Press Ctrl+C to stop")
    print("🔄" * 60 + "\n")
    
    print("\n" + "=" * 60)
    print("Running on " + ("INT7" if BotSettings.IS_INT_SERVER else "DE15") + " server and efficiency: " + BotSettings.EFICIENCY_MIN)
    print(f"Operation started - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    bot.run()

if __name__ == "__main__":
    main()
