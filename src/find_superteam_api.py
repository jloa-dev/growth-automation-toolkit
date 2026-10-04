import re
import urllib.request

url = "https://earn.superteam.fun/bounties"
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
with urllib.request.urlopen(req) as resp:
    html = resp.read().decode("utf-8")
    scripts = re.findall(r'src="(/_next/static/(?:immutable/)?chunks/[^"]+)"', html)
    all_apis = set()
    for s in scripts:
        s_url = f"https://earn.superteam.fun{s}"
        try:
            s_req = urllib.request.Request(s_url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(s_req) as s_resp:
                content = s_resp.read().decode("utf-8", errors="ignore")
                apis = set(re.findall(r'["\'](/api/[a-zA-Z0-9_\-/]+)["\']', content))
                all_apis.update(apis)
        except Exception:
            pass
    print("Discovered APIs:", sorted(list(all_apis)))
