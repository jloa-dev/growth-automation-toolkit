import imaplib
import email
import sys, os
import re
from html import unescape
sys.path.insert(0, os.path.dirname(__file__))
from check_emails import get_env_credentials, decode_str

user, pwd = get_env_credentials()
mail = imaplib.IMAP4_SSL('imap.gmail.com')
mail.login(user, pwd)
mail.select('INBOX', readonly=True)

res, msg_data = mail.fetch(b'2393', '(RFC822)')
msg = email.message_from_bytes(msg_data[0][1])

for part in msg.walk():
    if part.get_content_type() == 'text/html':
        html = part.get_payload(decode=True).decode('utf-8', errors='replace')
        # strip css/style/head
        html = re.sub(r'<style.*?</style>', '', html, flags=re.DOTALL)
        html = re.sub(r'<head.*?</head>', '', html, flags=re.DOTALL)
        text = re.sub(r'<[^>]+>', ' ', html)
        text = unescape(text)
        clean = ' '.join(text.split())
        print("=== CONTENIDO DEL CORREO DE OMI (TICKET RECIENTE) ===")
        print(clean)

mail.logout()
