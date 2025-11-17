import time
from bot.main import KnightFightBot
from bot.models.attack_tracker import AttackTracker
from bot_battlefield.config.settings import BotSettings
from playwright.sync_api import sync_playwright
from shared.service.account_service import AccountService


class Knife:
    """Used to remove all bot opponents craated from game"""

    def __init__(self,  headless: bool = False):
        self.headless = headless
        self.tracker = AttackTracker(BotSettings.ATTACK_TRACKER_FILE)

    def run(self):
        """Run the knife bot to remove bot-created opponents"""

        attacks = self.tracker.get_attacks()
        print(f"Found {len(attacks)} bot-created opponents to remove.")
        if not attacks: return

        with sync_playwright() as p:
            # Launch browser
            browser = p.chromium.launch(headless=self.headless, executable_path=None)
            page = browser.new_page()

            for user in attacks:
                print("\n" + "="*50 + "\n")
                print(f"Removing account for opponent: email: {user.email}")
                account_service =  AccountService(page, user.username, user.password)
                if not account_service.login_player():
                    print(f"Skipping account removal due to login failure. Email: {user.email}")
                    continue

                if not account_service.remove_account():
                    print(f"Failed to remove account for email: {user.email}")
                    continue
                print(f"Successfully removed account for email: {user.email}")
                self.tracker.remove_attack(user.email)
                print(f"Removed {user.email} from json tracker.")
                print("\n" + "="*50 + "\n")
        

def main():
    """Main entry point - removes all bot opponents created from game"""
    knife = Knife(headless=False)
    print("KNIFE BOT STARTED - HEADLESS: " + knife.headless.__str__())
    knife.run()
    print("KNIFE BOT FINISHED")


    

if __name__ == "__main__":
    main()
