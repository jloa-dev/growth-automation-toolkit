import urllib.request
import re

url = 'https://console.algora.io/bounties'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})

try:
    with urllib.request.urlopen(req, timeout=10) as resp:
        content = resp.read().decode('utf-8', errors='ignore')
        print(f"Status: {resp.status}, Length: {len(content)}")
        
        # Look for org links
        org_links = set(re.findall(r'/org/([^/]+)/bounties', content))
        print("Org links found:", org_links)
        
        # Look for issue links
        gh_links = set(re.findall(r'https://github\.com/([^/\s"\'<>]+)/([^/\s"\'<>]+)/issues/(\d+)', content))
        print(f"GitHub issues found: {len(gh_links)}")
        for r_owner, r_name, r_num in sorted(gh_links):
            print(f"- https://github.com/{r_owner}/{r_name}/issues/{r_num}")
            
except Exception as e:
    print("Error:", e)
