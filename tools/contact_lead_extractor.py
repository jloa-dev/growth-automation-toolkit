"""
Contact & Lead Extractor (Emails, Phones, Socials from URLs)
Usage:
  python contact_lead_extractor.py --urls "https://example.com" --output leads.csv
"""

import sys
import re
import csv
import argparse
import urllib.request
from bs4 import BeautifulSoup

EMAIL_REGEX = re.compile(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+')
PHONE_REGEX = re.compile(r'(?:\+?\d{1,3}[-.\s]?)?\(?\d{2,4}\)?[-.\s]?\d{3,4}[-.\s]?\d{3,4}')

def extract_from_url(url: str):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as resp:
            html = resp.read().decode('utf-8', errors='ignore')
            
        soup = BeautifulSoup(html, 'html.parser')
        text = soup.get_text()
        
        emails = set(EMAIL_REGEX.findall(text))
        # Filter out common file extensions mistakenly matched
        emails = [e for e in emails if not e.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.svg', '.webp'))]
        
        phones = list(set(PHONE_REGEX.findall(text)))[:5]
        
        socials = []
        for a in soup.find_all('a', href=True):
            href = a['href']
            if any(s in href.lower() for s in ['linkedin.com', 'twitter.com', 'x.com', 'facebook.com', 'instagram.com']):
                socials.append(href)
                
        return {
            'url': url,
            'title': soup.title.string.strip() if soup.title and soup.title.string else '',
            'emails': '; '.join(emails),
            'phones': '; '.join(phones),
            'socials': '; '.join(list(set(socials))[:3]),
        }
    except Exception as e:
        return {'url': url, 'title': 'Error', 'emails': '', 'phones': '', 'socials': f'Failed: {e}'}

def process_urls(urls, output_file="extracted_leads.csv"):
    results = []
    for u in urls:
        u = u.strip()
        if not u: continue
        if not u.startswith(('http://', 'https://')):
            u = 'https://' + u
        print(f"[*] Extracting: {u}")
        res = extract_from_url(u)
        results.append(res)
        
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['url', 'title', 'emails', 'phones', 'socials'])
        writer.writeheader()
        writer.writerows(results)
        
    print(f"[✓] Extracted data saved to {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Lead & Contact Extractor")
    parser.add_argument("--urls", required=True, help="Comma-separated URLs or path to txt file")
    parser.add_argument("--output", default="leads.csv", help="Output CSV filename")
    args = parser.parse_args()
    
    if args.urls.endswith('.txt'):
        with open(args.urls, 'r', encoding='utf-8') as f:
            url_list = f.read().splitlines()
    else:
        url_list = [u.strip() for u in args.urls.split(',')]
        
    process_urls(url_list, args.output)
