# Quick debug - save what the 3101 byte response actually contains
import cloudscraper
import os

scraper = cloudscraper.create_scraper(
    browser={'browser': 'chrome', 'platform': 'windows', 'desktop': True}
)

url = "https://battlefordreamisland.fandom.com/wiki/Power_of_Three/Transcript"
r = scraper.get(url, timeout=30)

print(f"Status: {r.status_code}")
print(f"Content length: {len(r.content)} bytes")
print(f"\n{'='*60}")
print("FULL RESPONSE:")
print("="*60)
print(r.text)
