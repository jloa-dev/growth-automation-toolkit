import json
import subprocess
from datetime import datetime, timezone, timedelta

pet_offset = timezone(timedelta(hours=-5))

res = subprocess.run(['gh', 'issue', 'list', '--repo', 'Expensify/App', '--limit', '100', '--label', 'Help Wanted', '--state', 'all', '--json', 'number,createdAt,updatedAt'], capture_output=True, text=True)
if res.returncode == 0:
    data = json.loads(res.stdout)
    hours_pet = {}
    for it in data:
        dt_utc = datetime.fromisoformat(it['createdAt'].replace('Z', '+00:00'))
        dt_pet = dt_utc.astimezone(pet_offset)
        h = dt_pet.hour
        hours_pet[h] = hours_pet.get(h, 0) + 1
        
    print('Distribución de issues con Help Wanted (Hora Perú UTC-5):')
    for h in range(24):
        cnt = hours_pet.get(h, 0)
        bar = '#' * cnt
        print(f'{h:02d}:00 - {h:02d}:59 : {cnt:2d} {bar}')
