import imaplib, email, os
from email.header import decode_header

with open('.env') as f:
    env = dict(l.strip().split('=', 1) for l in f if '=' in l and not l.startswith('#'))

mail = imaplib.IMAP4_SSL('imap.gmail.com')
mail.login(env['GMAIL_USER'], env['GMAIL_APP_PASSWORD'])
mail.select('INBOX', readonly=True)
status, data = mail.search(None, 'ALL')
ids = data[0].split()
print(f"Total emails: {len(ids)}")
for i in ids[-8:]:
    res, msg_data = mail.fetch(i, '(RFC822.HEADER)')
    msg = email.message_from_bytes(msg_data[0][1])
    subj = decode_header(msg.get('Subject', ''))[0]
    s = subj[0].decode(subj[1] or 'utf-8', errors='replace') if isinstance(subj[0], bytes) else subj[0]
    sender = decode_header(msg.get('From', ''))[0]
    sndr = sender[0].decode(sender[1] or 'utf-8', errors='replace') if isinstance(sender[0], bytes) else sender[0]
    print(f"[{msg.get('Date', '')[:25]}] From: {sndr[:40]} | Subject: {s[:60]}")
mail.logout()
