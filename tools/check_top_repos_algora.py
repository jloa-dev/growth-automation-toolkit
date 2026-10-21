import urllib.request
import re

orgs = [
    'tscircuit',
    'calcom',
    'twentyhq',
    'formbricks',
    'dub',
    'posthog',
    'ziverge',
    'hono',
    'documenso',
    'polar',
    'polarsource',
    'trpc',
    'midday',
    'infisical',
    'shadcn'
]

for org in orgs:
    url = f"https://console.algora.io/org/{org}"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req, timeout=5) as resp:
            content = resp.read().decode('utf-8', errors='ignore')
            amounts = re.findall(r'\$\d+', content)
            issues = set(re.findall(r'github\.com/([^/\s"\'<>]+/[^/\s"\'<>]+/issues/\d+)', content))
            print(f"[{org}] -> HTTP {resp.status} | len {len(content)} | amounts: {len(amounts)} | issues: {len(issues)}")
            if issues:
                for iss in list(issues)[:3]:
                    print(f"   https://github.com/{iss}")
    except Exception as e:
        # print(f"[{org}] -> {e}")
        pass
