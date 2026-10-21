import urllib.request
import re
from bs4 import BeautifulSoup

url = 'https://algora.io/tscircuit/bounties'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    content = urllib.request.urlopen(req, timeout=10).read().decode('utf-8', errors='ignore')
    links = set(re.findall(r'https://github\.com/tscircuit/[^\s"\'<>]+', content))
    print(f'Total GitHub links in tscircuit: {len(links)}')
    for l in sorted(links):
        print(l)
        
    # Also check other links or texts
    matches = re.findall(r'(\$\d+)\s*([^<>\n]+)', content)
    print('\nBounty text matches:')
    for m in matches[:15]:
        print(m[0], m[1].strip()[:80])
except Exception as e:
    print('Error:', e)
