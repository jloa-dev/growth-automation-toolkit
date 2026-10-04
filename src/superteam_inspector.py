import json
import re
import urllib.request

url = "https://earn.superteam.fun/bounties"
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
try:
    with urllib.request.urlopen(req) as resp:
        html = resp.read().decode("utf-8")
        match = re.search(r'<script id="__NEXT_DATA__"[^>]*>(.*?)</script>', html)
        if match:
            data = json.loads(match.group(1))
            props = data.get("props", {}).get("pageProps", {})
            print("Keys:", list(props.keys()))
            print(json.dumps(props, indent=2)[:500])
        else:
            print("No NEXT_DATA script found")
except Exception as e:
    print("Error:", e)
