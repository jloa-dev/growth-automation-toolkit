import subprocess
import json

verified_repos = [
    "calcom/cal.com",
    "twentyhq/twenty",
    "medusajs/medusa",
    "documenso/documenso",
    "formbricks/formbricks",
    "danny-avila/LibreChat",
    "novuhq/novu",
    "spacedriveapp/spacedrive",
    "payloadcms/payload",
    "BasedHardware/omi",
    "gitroomhq/postiz-app",
    "infisical/infisical",
    "dubinc/dub",
    "huggingface/transformers"
]

print("Scanning verified Algora / Bounty repositories...")
for repo in verified_repos:
    cmd = [
        "gh", "search", "issues",
        f"repo:{repo} is:open bounty",
        "--sort", "updated",
        "--limit", "5",
        "--json", "number,title,url,labels,body,commentsCount,updatedAt"
    ]
    try:
        res = subprocess.run(cmd, capture_output=True, text=True, check=True)
        issues = json.loads(res.stdout)
        if issues:
            print(f"\n=== {repo} ({len(issues)} issues found) ===")
            for iss in issues:
                labels = [l.get('name', '') for l in iss.get('labels', [])]
                print(f"#{iss['number']}: {iss['title']} (Labels: {labels})")
                print(f"URL: {iss['url']}")
    except Exception as e:
        # pass
        pass
