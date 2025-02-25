import time
from email_checker import EmailChecker
from google_sheet_updater import GoogleSheetUpdater
from whatsapp_sender import WhatsAppSender

# Kullanıcı bilgileri
EMAIL_ACCOUNT = "y.y@gmail.com"  # Gmail adresinizi girin
APP_PASSWORD = ""
# IMAP sunucu bilgileri (Gmail için)
IMAP_SERVER = "imap.gmail.com"
IMAP_PORT = 993
# İşlenmiş e-postaları saklamak için JSON dosyası
PROCESSED_EMAILS_FILE = "processed_emails.json"
# Google Sheets bilgileri
CREDENTIALS_FILE = "automate_credentials.json"
SPREADSHEET_NAME = "Automate Test"

# GoogleSheetUpdater sınıfını başlat
google_sheet_updater = GoogleSheetUpdater(CREDENTIALS_FILE, SPREADSHEET_NAME)

# WhatsAppSender sınıfını başlat
whatsapp_sender = WhatsAppSender()

# EmailChecker sınıfını başlat
send_whatsapp = True  # WhatsApp mesajı gönderme seçeneği
email_checker = EmailChecker(EMAIL_ACCOUNT, APP_PASSWORD, IMAP_SERVER, IMAP_PORT, PROCESSED_EMAILS_FILE, google_sheet_updater, whatsapp_sender if send_whatsapp else None)

# 📌 5 dakikada bir çalıştıran döngü
while True:
    print("📡 Yeni e-postalar kontrol ediliyor...")
    email_checker.check_new_emails()
    print("⏳ 5 dakika bekleniyor...")
    time.sleep(20)  # 300 saniye = 5 dakika