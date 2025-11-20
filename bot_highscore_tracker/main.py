#!/usr/bin/env python3
"""
Battlefield Bot - Main Entry Point

Continuous mode:
Login → Go to Highscore → Track data
"""
import time
from datetime import datetime
from bot_highscore_tracker.config.settings import BotSettings
from bot_highscore_tracker.models.player_tracker import PlayerRecord, PlayerTracker
from playwright.sync_api import sync_playwright
from shared.service.account_service import AccountService


class HighscoreBot:
    """Main bot orchestrator"""
    
    def __init__(self, headless: bool = False):
        self.headless = headless
        self.tracker = PlayerTracker(BotSettings.ATTACK_TRACKER_FILE)
    
    def run(self) -> None:
        """
        Execute single bot cycle: log in → track highscores
        """

        with sync_playwright() as p:
            # Launch browser
            browser = p.chromium.launch(headless=self.headless, executable_path=None)
            page = browser.new_page()
            
            # Initialize services
            account_service = AccountService(page, "timejo5100", "timejo5100@fermiro.com")
            account_service.login_player()

            while True:
                print(f"Tracking started - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                count = 100
                is_to_stop = False
                players_data = []
                json_players = self.tracker.load_player_records()

                while True:
                    print(f"Fetching players from highscore... {count}")
                    page.goto(f"https://int7.knightfight.moonid.net/highscore/spieler/?count={count}&filter=beute&hsort=0", wait_until="load")
                    players = page.locator("tbody .highscore").all()[1:]

                    for player in players:
                        player_statistics = player.locator("td").all()
                        data = [p.inner_text().replace(',', '') for p in player_statistics]
                        record = PlayerRecord(
                            name=data[1],
                            url=player.locator("td a").get_attribute("href"),
                            level=int(data[2]),
                            loot=int(data[3]),
                            loot_updated_at=datetime.now(),
                            fights=int(data[4]),
                            last_fight_at=datetime.now(),
                            gold_lost=int(data[9]),
                            gold_lost_at=datetime.now(),
                            gold_difference=0
                        )
                        
                        if record.loot == 0:
                            is_to_stop = True
                            break
                        
                        json_player = next((p for p in json_players if p.url == record.url), None)

                        if json_player is None:
                            players_data.append(record)
                            continue

                        record.loot_updated_at = json_player.loot_updated_at
                        record.last_fight_at = json_player.last_fight_at
                        record.gold_lost_at = json_player.gold_lost_at
                        record.gold_difference = json_player.gold_difference

                        if record.loot != json_player.loot:
                            record.loot_updated_at = datetime.now()
                        
                        if record.fights != json_player.fights:
                            record.last_fight_at = datetime.now()

                        if record.gold_lost != json_player.gold_lost:
                            record.gold_lost_at = datetime.now()
                            record.gold_difference = record.gold_lost - json_player.gold_lost

                        players_data.append(record)

                    if is_to_stop: break

                    count += 100

                print(f"Total players fetched: {len(players_data)}")
                players_data.sort(key=lambda x: x.gold_difference, reverse=True)
                self.tracker.record_players(players_data)
                print(f"Tracking ended - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                time.sleep(300)


def main():
    """Main entry point - runs in continuous mode"""    
    BotSettings.ensure_directories()
    bot = HighscoreBot(True)
    print("\n" + "🔄" * 60)
    print("BOT STARTED - CONTINUOUS MODE - HEADLESS: " + bot.headless.__str__())
    print("Login account and track zombies statistics repeatedly")
    print("Press Ctrl+C to stop")
    print("🔄" * 60 + "\n")
    
    print("\n" + "=" * 60)
    
    bot.run()

if __name__ == "__main__":
    main()
