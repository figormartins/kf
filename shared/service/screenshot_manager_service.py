"""
Screenshot and file utilities
"""
from pathlib import Path
from playwright.sync_api import Page


class ScreenshotManager:
    """Manage screenshot capturing and storage"""
    
    def __init__(self, screenshots_dir: Path):
        self.screenshots_dir = screenshots_dir
    
    def capture(self, page: Page, filename: str) -> Path:
        """
        Capture and save screenshot
        
        Args:
            page: Playwright page object
            filename: Name of the screenshot file
            
        Returns:
            Path to saved screenshot
        """
        screenshot_path = self.screenshots_dir / filename
        page.screenshot(path=str(screenshot_path))
        return screenshot_path
    
    def save_html(self, page: Page, filename: str) -> Path:
        """
        Save page HTML content
        
        Args:
            page: Playwright page object
            filename: Name of the HTML file
            
        Returns:
            Path to saved HTML file
        """
        html_path = self.screenshots_dir / filename
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(page.content())
        return html_path
    
    def get_screenshot_path(self, name: str, timestamp: int) -> str:
        """Generate screenshot filename with timestamp"""
        return f"{name}_{timestamp}.png"
    
    def get_html_path(self, name: str, timestamp: int) -> str:
        """Generate HTML filename with timestamp"""
        return f"{name}_{timestamp}.html"
