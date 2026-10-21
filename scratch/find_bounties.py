import urllib.request
import json
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

def fetch(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=10) as r:
            return r.read().decode('utf-8')
    except Exception as e:
        return f"Error: {e}"

# Test Opire
print("--- OPIRE ---")
data = fetch("https://api.opire.dev/bounties")
try:
    j = json.loads(data)
    print("Opire count:", len(j) if isinstance(j, list) else j.keys())
    if isinstance(j, list):
        for item in j[:10]:
            print(item)
except Exception as e:
    print("Opire parse error:", e, data[:200])

# Test Bountycaster
print("\n--- BOUNTYCASTER ---")
bc_data = fetch("https://api.bountycaster.xyz/bounties/open")
print("Bountycaster:", bc_data[:300])
