import imaplib
import email
from email.header import decode_header
import os

with open(".env") as f:
    creds = dict(line.strip().split("=", 1) for line in f if "=" in line and not line.startswith("#"))
user, pwd = creds.get("GMAIL_USER"), creds.get("GMAIL_APP_PASSWORD")

mail = imaplib.IMAP4_SSL("imap.gmail.com")
mail.login(user, pwd)
mail.select("INBOX", readonly=True)

status, data = mail.search(None, "ALL")
msg_ids = data[0].split()
print("Total emails:", len(msg_ids))

for mid in reversed(msg_ids[-30:]):
    res, mdata = mail.fetch(mid, "(BODY.PEEK[HEADER.FIELDS (FROM SUBJECT DATE)] FLAGS)")
    hdr = mdata[0][1].decode("utf-8", errors="replace")
    flags = str(mdata[0][0])
    is_unread = "\\Seen" not in flags
    print(f"ID: {mid.decode()} | Unread: {is_unread}")
    for line in hdr.strip().splitlines():
        print("  ", line)
    print("-" * 50)
mail.logout()
