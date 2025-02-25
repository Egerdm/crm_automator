import imaplib
import email
import json
from email.header import decode_header
from email_processor import EmailProcessor
from google_sheet_updater import GoogleSheetUpdater
from whatsapp_sender import WhatsAppSender

class EmailChecker:
    def __init__(self, email_account, app_password, imap_server, imap_port, processed_emails_file, google_sheet_updater, whatsapp_sender=None):
        self.email_account = email_account
        self.app_password = app_password
        self.imap_server = imap_server
        self.imap_port = imap_port
        self.processed_emails_file = processed_emails_file
        self.processed_emails = self.load_processed_emails()
        self.email_processor = EmailProcessor()
        self.google_sheet_updater = google_sheet_updater
        self.whatsapp_sender = whatsapp_sender

    def load_processed_emails(self):
        try:
            with open(self.processed_emails_file, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            return []

    def save_processed_emails(self):
        with open(self.processed_emails_file, "w") as f:
            json.dump(self.processed_emails, f)

    def decode_mime_words(self, text):
        """MIME kodlu başlıkları (örneğin, Subject) UTF-8 formatına dönüştürür."""
        decoded_words = decode_header(text)
        decoded_string = ""
        for word, encoding in decoded_words:
            if isinstance(word, bytes):  # Eğer byte verisi ise UTF-8'e çevir
                decoded_string += word.decode(encoding or "utf-8", errors="ignore")
            else:
                decoded_string += word
        return decoded_string

    def check_new_emails(self):
        """Yeni e-postaları kontrol eder ve gerekirse Google Sheet'e ekler."""
        try:
            # IMAP bağlantısını başlat
            imap = imaplib.IMAP4_SSL(self.imap_server, self.imap_port)
            imap.login(self.email_account, self.app_password)

            # Gelen kutusunu seç
            imap.select("INBOX")

            # Kısmi konu ile e-postaları ara (örneğin "Hasta" kelimesini arıyoruz)
            search_criteria = 'UNSEEN SUBJECT "Egerdm"'
            _, message_ids = imap.search(None, search_criteria)

            # Eğer hiç e-posta bulunamazsa
            if not message_ids[0]:
                print("📭 Yeni e-posta bulunamadı.")
                return

            for message_id in message_ids[0].split():
                # Daha önce işlenmiş mi?
                if message_id.decode() in self.processed_emails:
                    continue

                # E-postayı çek
                _, message_data = imap.fetch(message_id, "(RFC822)")
                email_message = email.message_from_bytes(message_data[0][1])

                # Gönderici bilgilerini al
                sender = email_message["From"]
                raw_subject = email_message["Subject"]
                subject = self.decode_mime_words(raw_subject)  # Konuyu UTF-8'e çevir

                print("\n📩 Yeni E-Posta Bulundu!")
                print(f"🧑‍💼 Gönderen: {sender}")
                print(f"📌 Konu: {subject}")

                # E-posta içeriğini al ve isim, numara çıkarmaya çalış
                name, phone_number = None, None
                for part in email_message.walk():
                    if part.get_content_type() == "text/plain":
                        body = part.get_payload(decode=True).decode("utf-8", errors="ignore")
                        print(f"📜 İçerik: {body}")

                        # İsmi ve telefon numarasını çıkar
                        name, phone_number, full_name = self.email_processor.extract_info_from_email(body)
                        break

                # E-postayı Google Sheet'e ekle
                if name:
                    self.google_sheet_updater.add_email_to_sheet(full_name, 'whatsapp mesajı gönderildi')

                # Eğer WhatsAppSender varsa ve telefon numarası bulunduysa, mesaj at
                if self.whatsapp_sender and phone_number and phone_number not in self.processed_emails:
                    self.whatsapp_sender.send_whatsapp_message(phone_number, name)
                    self.processed_emails.append(phone_number)

                # İşlenmiş e-posta listesini güncelle
                self.processed_emails.append(message_id.decode())
                self.save_processed_emails()

            # Bağlantıyı kapat
            imap.close()
            imap.logout()

        except Exception as e:
            print(f"❌ Hata: {e}")