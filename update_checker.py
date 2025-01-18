import requests
import json
from packaging import version
import webbrowser

GITHUB_API = "https://api.github.com/repos/{owner}/{repo}/releases/latest"
GITHUB_REPO = "your-username/SRTeew"  # Thay thế bằng username của bạn

class UpdateChecker:
    def __init__(self, current_version):
        self.current_version = version.parse(current_version)
        self.latest_version = None
        self.release_notes = None
        self.download_url = None
        
    def check_for_updates(self):
        """
        Kiểm tra phiên bản mới từ GitHub
        Returns: (has_update, version, notes)
        """
        try:
            response = requests.get(GITHUB_API.format(
                owner=GITHUB_REPO.split('/')[0],
                repo=GITHUB_REPO.split('/')[1]
            ))
            response.raise_for_status()
            
            data = response.json()
            latest_version = version.parse(data['tag_name'].lstrip('v'))
            self.latest_version = latest_version
            self.release_notes = data['body']
            
            # Lấy URL download của file exe
            for asset in data['assets']:
                if asset['name'].endswith('.exe'):
                    self.download_url = asset['browser_download_url']
                    break
            
            return (
                latest_version > self.current_version,
                str(latest_version),
                self.release_notes
            )
            
        except Exception as e:
            print(f"Error checking for updates: {e}")
            return False, None, None
    
    def open_download_page(self):
        """Mở trang download trong trình duyệt"""
        if self.download_url:
            webbrowser.open(self.download_url)
            
    def get_changelog(self):
        """Lấy changelog của phiên bản mới nhất"""
        if self.release_notes:
            return self.release_notes
        return "Không có thông tin changelog" 