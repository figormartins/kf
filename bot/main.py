#!/usr/bin/env python3
"""
KnightFight Bot - Main Entry Point

Continuous mode:
Creates new account → Creates player → Attacks → Closes session → Repeats forever
"""
import time
from datetime import datetime
from playwright.sync_api import sync_playwright
from bot.config import BotSettings
from bot.models import BotSession
from bot.services import AccountService, PlayerService, AttackScheduler
from bot.utils import CredentialsGenerator, ScreenshotManager


class KnightFightBot:
    """Main bot orchestrator"""
    
    def __init__(self, headless: bool = False):
        self.headless = headless
        self.screenshot_manager = ScreenshotManager()
    
    def run(self) -> BotSession:
        """
        Execute single bot cycle: account creation → player creation → attack
        
        Returns:
            BotSession with execution results
        """
        # Generate credentials
        credentials = CredentialsGenerator.generate_credentials()
        timestamp = credentials.timestamp
        
        print("Creating account with the following credentials:")
        print(f"Email: {credentials.email}")
        print(f"Username: {credentials.username}")
        print(f"Password: {credentials.password}")
        print("-" * 50)
        
        with sync_playwright() as p:
            # Launch browser
            browser = p.chromium.launch(headless=self.headless, executable_path=None)
            page = browser.new_page()
            
            try:
                # Initialize services
                account_service = AccountService(page, self.screenshot_manager)
                player_service = PlayerService(page, self.screenshot_manager)
                attack_scheduler = AttackScheduler(page, self.screenshot_manager)
                
                # Step 1: Register account
                account_created = account_service.register_account(credentials)
                
                if not account_created:
                    print("❌ Failed to create account. Aborting.")
                    return None
                
                # Step 2: Create and register player
                player = player_service.create_player(credentials)
                player_registered = player_service.register_player_name(player, timestamp)
                
                # Step 3: Perform attack with cooldown management
                print(f"\n{'='*50}")
                print("PHASE 3: ATTACK")
                print(f"{'='*50}")
                
                attack_success = attack_scheduler.schedule_attack(
                    player=player,
                    opponent_id=BotSettings.TARGET_OPPONENT_ID
                )
                
                # Capture final screenshot
                # final_screenshot_file = self.screenshot_manager.get_screenshot_path(
                #     "final_registration",
                #     timestamp
                # )
                # final_screenshot_path = self.screenshot_manager.capture(page, final_screenshot_file)
                # print(f"Final screenshot saved at: {final_screenshot_path}")
                
                # Create session summary with simple success boolean
                attack_result = {
                    'success': attack_success,
                    'reason': 'success' if attack_success else 'failed',
                    'player_name': player.name,
                    'timestamp': datetime.now() if attack_success else None,
                    'Email': credentials.email,
                    'Login': credentials.username,
                    'Password': credentials.password
                }
                session = BotSession(player=player, attack_result=attack_result)
                # session.add_screenshot(str(final_screenshot_path))
                
                # Keep browser open briefly to see results
                page.wait_for_timeout(BotSettings.FINAL_WAIT)
                
                return session
                
            finally:
                browser.close()
    
    def print_summary(self, session: BotSession) -> None:
        """
        Print session summary
        
        Args:
            session: BotSession to summarize
        """
        print("\n" + "=" * 50)
        print("PROCESS COMPLETED!")
        print("=" * 50)
        
        summary = session.summary()
        print(f"Email: {summary['email']}")
        print(f"Username: {summary['username']}")
        print(f"Password: {summary['password']}")
        print(f"Player Name: {summary['player_name']}")
        print(f"Name Registered: {'✅ Yes' if summary['is_registered'] else '⚠️ No'}")
        
        # Handle attack result dict instead of AttackResult object
        attack_result = session.attack_result
        if attack_result:
            if attack_result.get('success'):
                print(f"Attack Status: ✅ Success")
            elif attack_result.get('reason') == 'cooldown':
                print(f"Attack Status: ⏰ Cooldown")
                if attack_result.get('next_available'):
                    print(f"Next Available: {attack_result['next_available'].strftime('%Y-%m-%d %H:%M:%S')}")
                if attack_result.get('cooldown_info'):
                    print(f"Info: {attack_result['cooldown_info']}")
            else:
                print(f"Attack Status: ❌ Failed ({attack_result.get('reason')})")
        
        print(f"Screenshots Saved: {summary['screenshots_count']}")
        print("=" * 50)


def main():
    """Main entry point - runs in continuous mode"""
    # Ensure directories exist
    BotSettings.ensure_directories()
    
    bot = KnightFightBot(headless=BotSettings.HEADLESS)
    
    cycle = 0
    
    print("\n" + "🔄" * 25)
    print("BOT STARTED - CONTINUOUS MODE - HEADLESS: " + bot.headless.__str__())
    print("Creates new accounts and attacks repeatedly")
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
                bot.print_summary(session)
                time.sleep(3360)
            else:
                print(f"\n⚠️  Cycle #{cycle} failed - retrying in 30s...")
                time.sleep(30)
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
