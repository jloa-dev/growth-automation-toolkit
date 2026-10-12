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
    decoded_fragments = decode_header(s)
    result = []
    for text, enc in decoded_fragments:
        if isinstance(text, bytes):
            result.append(text.decode(enc or 'utf-8', errors='replace'))
        else:
            result.append(str(text))
    return "".join(result)

def check_mailbox(max_emails=15):
    user, password = get_env_credentials()
    if not user or not password:
        print("[ERROR] Credenciales no encontradas en .env")
        return

    print(f"[*] Conectando a imap.gmail.com como {user}...")
    mail = imaplib.IMAP4_SSL("imap.gmail.com")
    try:
        mail.login(user, password)
        print("[OK] Autenticación exitosa en Gmail.")
    except Exception as e:
        print(f"[FAIL] Error de login: {e}")
        return

    mail.select("INBOX", readonly=True)

    # Buscar mensajes recientes
    status, messages = mail.search(None, 'ALL')
    if status != 'OK':
        print("[ERROR] No se pudo buscar en la bandeja.")
        mail.logout()
        return

    msg_ids = messages[0].split()
    total = len(msg_ids)
    print(f"[*] Total de correos en bandeja: {total}. Analizando los ultimos {max_emails}...")

    recent_ids = msg_ids[-max_emails:]
    results = []

    for msg_id in reversed(recent_ids):
        res, data = mail.fetch(msg_id, '(RFC822.HEADER)')
        if res != 'OK':
            continue
        msg = email.message_from_bytes(data[0][1])
        subject = decode_str(msg.get("Subject", "(Sin asunto)"))
        sender = decode_str(msg.get("From", "(Desconocido)"))
        date = msg.get("Date", "")
        
        # Filtrar o etiquetar remitentes de interés
        is_relevant = any(k in sender.lower() or k in subject.lower() for k in [
            'basedhardware', 'omi', 'paypal', 'upwork', 'expensify', 'ticket', 'bounty', 'github'
        ])
        
        results.append({
            'id': msg_id.decode(),
            'from': sender,
            'subject': subject,
            'date': date,
            'relevant': is_relevant
        })

    print("\n" + "="*70)
    print(" CORREOS RELEVANTES / RECIENTES DE PLATAFORMAS")
    print("="*70)
    found_relevant = False
    for r in results:
        flag = "[! RELEVANTE]" if r['relevant'] else "  "
        print(f"{flag} Fecha: {r['date']}")
        print(f"    De: {r['from']}")
        print(f"    Asunto: {r['subject']}")
        print("-" * 70)
        if r['relevant']:
            found_relevant = True

    if not found_relevant:
        print("No se encontraron notificaciones criticas nuevas en los ultimos correos.")

    mail.logout()

if __name__ == '__main__':
    max_count = int(sys.argv[1]) if len(sys.argv) > 1 else 15
    check_mailbox(max_count)
