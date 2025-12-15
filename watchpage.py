import requests
import hashlib
from bs4 import BeautifulSoup
from pathlib import Path

URL = "https://www.nia.nih.gov/2026-dementia-care-summit"
STATE_FILE = Path("page_hash.txt")

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:146.0) Gecko/20100101 Firefox/146.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9"
}

response = requests.get(URL, headers=headers, timeout=30)

if response.status_code != 200:
    print(f"PAGE_STATUS=HTTP_{response.status_code}")
    print("PAGE_CHANGED=false")
    exit(0)

soup = BeautifulSoup(response.text, "html.parser")
main = soup.find("main") or soup.body
text = main.get_text(separator=" ", strip=True)

current_hash = hashlib.sha256(text.encode("utf-8")).hexdigest()

changed = False

if STATE_FILE.exists():
    old_hash = STATE_FILE.read_text()
    if old_hash != current_hash:
        changed = True
else:
    changed = True  # first run

STATE_FILE.write_text(current_hash)

if changed:
    print("PAGE_CHANGED=true")
else:
    print("PAGE_CHANGED=false")
