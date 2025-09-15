import requests
import os
import zipfile
from pathlib import Path

def download_font():
    """Download modern rounded fonts"""
    font_dir = Path("fonts")
    font_dir.mkdir(exist_ok=True)
    
    # Modern rounded fonts with working URLs
    font_urls = {
        "Nunito-Regular.ttf": "https://fonts.gstatic.com/s/nunito/v26/XRXV3I6Li01BKofINeaE.ttf",
        "Nunito-Bold.ttf": "https://fonts.gstatic.com/s/nunito/v26/XRXW3I6Li01BKofAjsOUYevN.ttf", 
        "Poppins-Regular.ttf": "https://fonts.gstatic.com/s/poppins/v21/pxiEyp8kv8JHgFVrJJfecg.ttf",
        "Poppins-Bold.ttf": "https://fonts.gstatic.com/s/poppins/v21/pxiByp8kv8JHgFVrLCz7Z1xlFQ.ttf",
        "Inter-Regular.ttf": "https://github.com/rsms/inter/raw/master/docs/font-files/Inter-Regular.ttf",
        "Inter-Bold.ttf": "https://github.com/rsms/inter/raw/master/docs/font-files/Inter-Bold.ttf"
    }
    
    for font_name, url in font_urls.items():
        font_path = font_dir / font_name
        if not font_path.exists():
            try:
                print(f"Downloading {font_name}...")
                response = requests.get(url)
                response.raise_for_status()
                
                with open(font_path, 'wb') as f:
                    f.write(response.content)
                print(f"✓ Downloaded {font_name}")
                
            except Exception as e:
                print(f"✗ Failed to download {font_name}: {e}")
                return False
        else:
            print(f"✓ {font_name} already exists")
    
    return True

if __name__ == "__main__":
    if download_font():
        print("\n✅ All fonts downloaded successfully!")
    else:
        print("\n❌ Font download failed!")