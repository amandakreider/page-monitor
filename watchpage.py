import requests
import hashlib
import time
from bs4 import BeautifulSoup
from pathlib import Path

URL = "https://www.nia.nih.gov/2026-dementia-care-summit"
STATE_FILE = Path("page_hash.txt")
LAST_MOD_FILE = Path("last_modified.txt")
DEFAULT_IF_MODIFIED_SINCE = "Sat, 29 Nov 2025 00:00:00 GMT"

def fetch_with_retry(session, url):
    response = session.get(url, timeout=30)
    if response.status_code in (200, 304):
        return response
    time.sleep(30)
    return session.get(url, timeout=30)

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:146.0) Gecko/20100101 Firefox/146.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9"
}

if LAST_MOD_FILE.exists():
    headers["If-Modified-Since"] = LAST_MOD_FILE.read_text().strip()
else:
    headers["If-Modified-Since"] = DEFAULT_IF_MODIFIED_SINCE

session = requests.Session()
session.headers.update(headers)

response = fetch_with_retry(session, URL)

# ---- Graceful handling ----
if response.status_code == 304:
    print("PAGE_STATUS=NOT_MODIFIED")
    print("PAGE_CHANGED=false")
    exit(0)

if response.status_code != 200:
    print(f"PAGE_STATUS=HTTP_{response.status_code}")
    print("PAGE_CHANGED=false")
    exit(0)

# ---- Record Last-Modified for next time ----
last_modified = response.headers.get("Last-Modified")
if last_modified:
    LAST_MOD_FILE.write_text(last_modified)

# ---- Normal hashing path ----
soup = BeautifulSoup(response.text, "html.parser")
main = soup.find("main") or soup.body
text = main.get_text(separator=" ", strip=True)

current_hash = hashlib.sha256(text.encode("utf-8")).hexdigest()

changed = False
if STATE_FILE.exists():
    if STATE_FILE.read_text() != current_hash:
        changed = True
else:
    changed = True  # first successful fetch

STATE_FILE.write_text(current_hash)

print(f"PAGE_CHANGED={'true' if changed else 'false'}")


