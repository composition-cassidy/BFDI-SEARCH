# debug_scraper.py
# Run this to see what the BFDI wiki is actually returning

import requests
from bs4 import BeautifulSoup

url = "https://battlefordreamisland.fandom.com/wiki/Take_the_Plunge:_Part_1/Transcript"

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
}

print(f"Fetching: {url}\n")
response = requests.get(url, headers=headers, timeout=30)
print(f"Status: {response.status_code}")
print(f"Content length: {len(response.text)} characters\n")

soup = BeautifulSoup(response.content, "html.parser")

# Check for content div
content_div = soup.find('div', {'class': 'mw-parser-output'})
print(f"Found mw-parser-output: {content_div is not None}")

if content_div:
    # Show first 2000 chars of the content
    text = content_div.get_text()[:2000]
    print(f"\n=== FIRST 2000 CHARS OF CONTENT ===\n{text}")
    
    # Count elements
    tables = content_div.find_all('table')
    lis = content_div.find_all('li')
    ps = content_div.find_all('p')
    dls = content_div.find_all('dl')
    
    print(f"\n=== ELEMENT COUNTS ===")
    print(f"Tables: {len(tables)}")
    print(f"List items (li): {len(lis)}")
    print(f"Paragraphs (p): {len(ps)}")
    print(f"Definition lists (dl): {len(dls)}")
    
    # Show some list items if they exist
    if lis:
        print(f"\n=== FIRST 5 LIST ITEMS ===")
        for i, li in enumerate(lis[:5]):
            print(f"{i+1}. {li.get_text()[:100]}...")
else:
    # Show what classes ARE present
    all_divs = soup.find_all('div', class_=True)
    classes = set()
    for div in all_divs[:50]:
        classes.update(div.get('class', []))
    print(f"\n=== DIV CLASSES FOUND ===")
    print(sorted(classes)[:30])
    
    # Show raw HTML snippet
    print(f"\n=== RAW HTML (first 3000 chars) ===")
    print(response.text[:3000])
