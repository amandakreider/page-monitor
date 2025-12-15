import requests
import hashlib
from bs4 import BeautifulSoup
from pathlib import Path

URL = "https://www.nia.nih.gov/2026-dementia-care-summit"
STATE_FILE = Path("page_hash.txt")

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:146.0) Gecko/20100101 Firefox/146.0"
}

response = requests.get(URL, headers=headers, timeout=30)
response.raise_for_status()

soup = BeautifulSoup(response.text, "html.parser")

# 🔍 Pick the main content area
main = soup.find("main") or soup.body
text = main.get_text(separator=" ", strip=True)
print(text)

# Hash the visible text
current_hash = hashlib.sha256(text.encode("utf-8")).hexdigest()

if STATE_FILE.exists():
    old_hash = STATE_FILE.read_text()
    if old_hash != current_hash:
        print("🚨 Page content changed!")
    else:
        print("No change.")
else:
    print("Tracking started.")

STATE_FILE.write_text(current_hash)
