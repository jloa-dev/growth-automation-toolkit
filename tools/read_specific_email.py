import imaplib
import email
from email.header import decode_header
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from check_emails import get_env_credentials, decode_str

user, pwd = get_env_credentials()
mail = imaplib.IMAP4_SSL('imap.gmail.com')
mail.login(user, pwd)
mail.select('INBOX', readonly=True)

status, data = mail.search(None, 'FROM "email@omi.me"')
print("IDs encontrados:", data[0].split())
for msg_id in data[0].split():
    res, msg_data = mail.fetch(msg_id, '(RFC822)')
    msg = email.message_from_bytes(msg_data[0][1])
    print('FROM:', decode_str(msg.get('From')))
    print('SUBJECT:', decode_str(msg.get('Subject')))
    print('DATE:', msg.get('Date'))
    for i, part in enumerate(msg.walk()):
        ctype = part.get_content_type()
        payload = part.get_payload(decode=True)
        print(f"Part {i}: {ctype}, decoded len: {len(payload) if payload else 0}")
        if payload and ctype in ['text/plain', 'text/html']:
            print("--- TEXT PREVIEW ---")
            print(payload.decode('utf-8', errors='replace')[:1000])

mail.logout()
