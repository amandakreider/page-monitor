# Page Change Monitor

A lightweight GitHub Actions setup that monitors a web page for content changes and creates a GitHub Issue when a change is detected.

Designed to be:
- Low-frequency (e.g. once per day)
- Respectful of target sites
- Reliable in GitHub Actions
- Safe to use in a public repository with a private target URL

---

## How it works

- A scheduled GitHub Actions workflow runs `watchpage.py`
- The script fetches the target page using a realistic browser profile
- Conditional requests (`If-Modified-Since`) are used when available
- Visible page text is hashed and compared to the previous run
- If the content changes, a GitHub Issue is created
- GitHub automatically emails repository watchers

Temporary blocks (403/405/etc.) are treated as “no data”, not failures.

---

## Configuration

### Target URL (required)

The monitored URL is **not stored in the repository**.  
It must be provided via the environment variable: `TARGET_URL`.

### GitHub Actions

Set `TARGET_URL` as a repository secret:

1. Go to **Settings → Secrets and variables → Actions**
2. Add a new repository secret:
   - Name: `TARGET_URL`
   - Value: the URL you want to monitor

The URL will not appear in the code, logs, or commits.

---

## Running locally

You can run the script locally using the same configuration.

### Option 1: Environment variable

```bash
export TARGET_URL="https://example.com/page"
python watchpage.py
```

### Option 2: .env file (recommended)

Create a file named .env (not committed) that contains:

```env
TARGET_URL=https://example.com/page
```

---

## State files

This repository commits two small state files:
- `page_hash.txt` — SHA-256 hash of the last known page content
- `last_modified.txt` — HTTP Last-Modified timestamp (if provided)

These files:
- Do not contain the target URL
- Do not contain page content
- Are safe to commit
- Allow state to persist across GitHub Actions runs

---

## Dependencies 

- Python 3.11+
- `requests`
- `beautifulsoup4`

Install locally with:

```bash
pip install -r requirements.txt
```
---

## Notes on blocking & usage

Some sites (especially `.gov` domains) may block requests from cloud IPs such as those used by GitHub Actions.

This project intentionally:
- Avoids aggressive retries
- Avoids proxy or IP rotation
- Avoids CAPTCHA bypass techniques
- Treats blocks as non-fatal events

It is intended for personal or low-volume monitoring. Please ensure your usage complies with the target site's terms of service.
