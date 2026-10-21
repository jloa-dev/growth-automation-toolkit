import imaplib
import email
from email.header import decode_header
import os
import sys

def get_env_credentials():
    env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
    if not os.path.exists(env_path):
        env_path = '.env'
    creds = {}
    if os.path.exists(env_path):
        with open(env_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    k, v = line.split('=', 1)
                    creds[k.strip()] = v.strip()
    return creds.get('GMAIL_USER'), creds.get('GMAIL_APP_PASSWORD')

def decode_str(s):
    if not s:
        return ""
    try:
        decoded_fragments = decode_header(s)
        result = []
        for text, enc in decoded_fragments:
            if isinstance(text, bytes):
                result.append(text.decode(enc or 'utf-8', errors='replace'))
            else:
                result.append(str(text))
        return "".join(result)
    except Exception:
        return str(s)

def extract_body(msg):
    text_content = ""
    for part in msg.walk():
        ctype = part.get_content_type()
        cdispo = str(part.get('Content-Disposition'))
        if ctype == 'text/plain' and 'attachment' not in cdispo:
            payload = part.get_payload(decode=True)
            if payload:
                text_content += payload.decode('utf-8', errors='replace') + "\n"
    if not text_content:
        for part in msg.walk():
            ctype = part.get_content_type()
            if ctype == 'text/html':
                payload = part.get_payload(decode=True)
                if payload:
                    raw_html = payload.decode('utf-8', errors='replace')
                    import re
                    clean_text = re.sub(r'<[^>]+>', ' ', raw_html)
                    clean_text = re.sub(r'\s+', ' ', clean_text)
                    text_content += clean_text[:1500] + "\n"
    return text_content.strip()

def main():
    user, pwd = get_env_credentials()
    if not user or not pwd:
        print("[ERROR] No credentials found")
        return

    mail = imaplib.IMAP4_SSL('imap.gmail.com')
    mail.login(user, pwd)
    mail.select('INBOX', readonly=True)

    # 1. Search UNSEEN
    status, unseen_data = mail.search(None, 'UNSEEN')
    unseen_ids = unseen_data[0].split() if status == 'OK' and unseen_data[0] else []
    print(f"=== CORREOS NO LEIDOS (UNSEEN): {len(unseen_ids)} ===")

    for msg_id in unseen_ids:
        res, msg_data = mail.fetch(msg_id, '(RFC822)')
        if res != 'OK':
            continue
        msg = email.message_from_bytes(msg_data[0][1])
        sender = decode_str(msg.get('From'))
        subj = decode_str(msg.get('Subject'))
        date = msg.get('Date')
        body = extract_body(msg)
        print(f"\n[UNSEEN ID {msg_id.decode()}]")
        print(f"DE: {sender}")
        print(f"ASUNTO: {subj}")
        print(f"FECHA: {date}")
        print(f"PREVIEW CUERPO:\n{body[:600]}")
        print("-" * 50)

    # 2. Search Last 15 emails overall
    status, all_data = mail.search(None, 'ALL')
    all_ids = all_data[0].split() if status == 'OK' and all_data[0] else []
    recent_ids = all_ids[-15:]
    print(f"\n=== ULTIMOS 15 CORREOS EN BANDEJA ===")
    for msg_id in reversed(recent_ids):
        res, msg_data = mail.fetch(msg_id, '(RFC822)')
        if res != 'OK':
            continue
        msg = email.message_from_bytes(msg_data[0][1])
        sender = decode_str(msg.get('From'))
        subj = decode_str(msg.get('Subject'))
        date = msg.get('Date')
        body = extract_body(msg)
        print(f"\n[ID {msg_id.decode()}]")
        print(f"DE: {sender}")
        print(f"ASUNTO: {subj}")
        print(f"FECHA: {date}")
        print(f"PREVIEW CUERPO:\n{body[:300]}")
        print("-" * 40)

    mail.logout()

if __name__ == '__main__':
    main()
