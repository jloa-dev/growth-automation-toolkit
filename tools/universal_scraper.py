"""
Universal Web Scraper & Data Extractor (Fast Freelance Delivery)
Usage:
  python universal_scraper.py --url <URL> --selector <CSS_SELECTOR> --output data.csv
"""

import sys
import argparse
import urllib.request
import csv
import json
from bs4 import BeautifulSoup

def scrape_url(url: str, item_selector: str = None, output_file: str = "output.csv"):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    print(f"[*] Fetching: {url}")
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=15) as resp:
        html = resp.read().decode('utf-8', errors='ignore')
        
    soup = BeautifulSoup(html, 'html.parser')
    
    # Auto-detect tables if no selector given
    if not item_selector:
        tables = soup.find_all('table')
        if tables:
            print(f"[+] Found {len(tables)} table(s). Extracting the first table...")
            rows = []
            for tr in tables[0].find_all('tr'):
                cells = [td.get_text(strip=True) for td in tr.find_all(['td', 'th'])]
                if cells:
                    rows.append(cells)
            
            with open(output_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerows(rows)
            print(f"[✓] Extracted {len(rows)} rows to {output_file}")
            return rows

    # If selector provided, extract matching items
    items = soup.select(item_selector)
    print(f"[+] Found {len(items)} elements matching selector '{item_selector}'")
    
    extracted_data = []
    for item in items:
        text = item.get_text(separator=' | ', strip=True)
        link = item.get('href') or (item.find('a')['href'] if item.find('a') else None)
        extracted_data.append({'text': text, 'link': link})
        
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['text', 'link'])
        writer.writeheader()
        writer.writerows(extracted_data)
        
    print(f"[✓] Successfully exported {len(extracted_data)} items to {output_file}")
    return extracted_data

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Universal Web Scraper")
    parser.add_argument("--url", required=True, help="Target URL to scrape")
    parser.add_argument("--selector", default=None, help="CSS selector for target items")
    parser.add_argument("--output", default="scraped_data.csv", help="Output CSV filename")
    args = parser.parse_args()
    
    scrape_url(args.url, args.selector, args.output)
