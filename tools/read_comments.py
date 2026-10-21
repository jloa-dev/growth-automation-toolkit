import subprocess
import json

def view_comments(repo, num, is_pr=False):
    t = 'pr' if is_pr else 'issue'
    cmd = ['gh', t, 'view', str(num), '--repo', repo, '--json', 'comments']
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode == 0:
        data = json.loads(res.stdout)
        comments = data.get('comments', [])
        print(f"=== {repo} #{num} ({t.upper()}) | ULTIMOS COMENTARIOS: ===")
        for c in comments[-3:]:
            author = c.get('author', {}).get('login')
            created = c.get('createdAt')
            body = c.get('body', '')
            print(f"-- Autor: {author} ({created})")
            print(body[:800])
            print('-'*50)

if __name__ == '__main__':
    view_comments('BasedHardware/omi', 21336, is_pr=True)
    view_comments('Expensify/App', 103775, is_pr=False)
    view_comments('Expensify/App', 103492, is_pr=False)
