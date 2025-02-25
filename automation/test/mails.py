import imaplib
import email
import time
import getpass
import json
import webbrowser
import re
import pyautogui
from email.header import decode_header

# Kullanıcı bilgileri
EMAIL_ACCOUNT = "yesim.yalcinbayram@gmail.com"  # Gmail adresinizi girin
#APP_PASSWORD = getpass.getpass("Enter your App Password: ")  # Gmail App Password girin
APP_PASSWORD = "uqgy lrse ubay errx"
# IMAP sunucu bilgileri (Gmail için)
IMAP_SERVER = "imap.gmail.com"
IMAP_PORT = 993

# İşlenmiş e-postaları saklamak için JSON dosyası
PROCESSED_EMAILS_FILE = "processed_emails.json"

# Daha önce işlenmiş e-postaları yükle
try:
    with open(PROCESSED_EMAILS_FILE, "r") as f:
        processed_emails = json.load(f)
except FileNotFoundError:
    processed_emails = []


def decode_mime_words(text):
    """MIME kodlu başlıkları (örneğin, Subject) UTF-8 formatına dönüştürür."""
    decoded_words = decode_header(text)
    decoded_string = ""
    for word, encoding in decoded_words:
        if isinstance(word, bytes):  # Eğer byte verisi ise UTF-8'e çevir
            decoded_string += word.decode(encoding or "utf-8", errors="ignore")
        else:
            decoded_string += word
    return decoded_string


def send_whatsapp_message(phone_number, name):
    """Belirtilen numaraya WhatsApp mesajı gönderir."""
    try:
        message = f"Hello {name}, this is Yesim reaching out from Dr. Yalçın Bayram's clinic.\n\n"
        message += "I found you through the information you shared with us on Instagram for facelift surgery.\n\n"
        message += "Would you like me to assist you on your Journey to Beauty?"

        # 📌 WhatsApp Web üzerinden mesajı aç
        whatsapp_url = f"https://web.whatsapp.com/send?phone={phone_number}&text={message}"
        webbrowser.open(whatsapp_url)

        print(f"📲 WhatsApp mesajı gönderiliyor: {phone_number} -> {name}")

        # ⏳ WhatsApp Web’in açılmasını bekle
        time.sleep(10)

        # ✅ Enter tuşuna basarak mesajı gönder
        pyautogui.press("enter")

        print(f"✅ Mesaj başarıyla gönderildi: {phone_number}")

    except Exception as e:
        print(f"❌ WhatsApp mesajı gönderilirken hata oluştu: {e}")


def extract_info_from_email(body):
    """E-posta içeriğinden sadece ismi ve telefon numarasını çıkarır."""
    # Yeni formatı kontrol et
    new_format_match = re.search(r"&([\w\s]+)&\s*(\d{1,4}\+|\+\d{1,4})\s*&\s*(\+?\d{1,4}\s?\d{3}\s?\d{3}\s?\d{3,4})\s*&", body)
    
    if new_format_match:
        print('new format')
        full_name = new_format_match.group(1).strip()
        country_code = new_format_match.group(2).replace(" ", "").replace("+", "")
        phone_number = new_format_match.group(3).replace(" ", "")
        print(full_name, country_code, phone_number)
        
        # Eğer telefon numarası 0 ile başlıyorsa, 0'ı ülke kodu ile değiştir
        if phone_number.startswith("0"):
            phone_number = phone_number[1:]
            phone_number = f"+{country_code}{phone_number}"
        elif not phone_number.startswith("+"):
            phone_number = f"+{country_code}{phone_number}"

        # Eğer telefon numarası içinde ülke kodu varsa, ülke kodunu kaldır
        if phone_number.startswith(f"+{country_code}"):
            phone_number = phone_number[len(country_code)+1:]

        # Ensure the phone number starts with the country code
        if not phone_number.startswith("+"):
            phone_number = f"+{country_code}{phone_number}"

        first_name = full_name.split()[0]

        # Aynı isim doğrulamalarını yap
        if len(first_name) < 3:
            print(f"⛔ Geçersiz isim: {first_name}, mesaj gönderilmeyecek.")
            return None, None

        if any(char.isdigit() for char in first_name):
            print(f"⛔ Geçersiz isim (sayı içeriyor): {first_name}, mesaj gönderilmeyecek.")
            return None, None

        if not first_name.isalpha():
            print(f"⛔ Geçersiz isim (özel karakter içeriyor): {first_name}, mesaj gönderilmeyecek.")
            return None, None

        if len(first_name) > 20:
            print(f"⛔ Geçersiz isim (çok uzun): {first_name}, mesaj gönderilmeyecek.")
            return None, None

        return first_name, phone_number

    # Eski formatı kontrol et
    name_match = re.search(r"&([\w\s]+)&", body)
    phone_match = re.search(r"(\+\d{1,4}\s?\d{3}\s?\d{3}\s?\d{4})", body)

    if name_match and phone_match:
        full_name = name_match.group(1).strip()  # Tam isim (Ad + Soyad)
        phone_number = phone_match.group(1).replace(" ", "")  # Telefon numarasını boşluksuz yap

        first_name = full_name.split()[0]  # İlk ismi al

        # Eğer ilk isim 3 harften kısa ise geçersiz say
        if len(first_name) < 3:
            print(f"⛔ Geçersiz isim: {first_name}, mesaj gönderilmeyecek.")
            return None, None

        # Eğer isimde sayı varsa geçersiz say
        if any(char.isdigit() for char in first_name):
            print(f"⛔ Geçersiz isim (sayı içeriyor): {first_name}, mesaj gönderilmeyecek.")
            return None, None

        # Eğer isimde özel karakter varsa geçersiz say
        if not first_name.isalpha():
            print(f"⛔ Geçersiz isim (özel karakter içeriyor): {first_name}, mesaj gönderilmeyecek.")
            return None, None

        # Eğer isim çok uzunsa geçersiz say
        if len(first_name) > 20:
            print(f"⛔ Geçersiz isim (çok uzun): {first_name}, mesaj gönderilmeyecek.")
            return None, None

        # Telefon numarası doğrulama
        if not phone_number.startswith("+"):
            print(f"⛔ Geçersiz telefon numarası (ülke kodu eksik): {phone_number}, mesaj gönderilmeyecek.")
            return None, None

        # Eğer telefon numarası 0 ile başlıyorsa, 0'ı ülke kodu ile değiştir
        if phone_number.startswith("0"):
            phone_number = phone_number[1:]
            phone_number = f"+{country_code}{phone_number}"

        return first_name, phone_number

    return None, None

def check_new_emails():
    """Yeni e-postaları kontrol eder ve gerekirse WhatsApp mesajı atar."""
    global processed_emails

    try:
        # IMAP bağlantısını başlat
        imap = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT)
        imap.login(EMAIL_ACCOUNT, APP_PASSWORD)

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
            if message_id.decode() in processed_emails:
                continue

            # E-postayı çek
            _, message_data = imap.fetch(message_id, "(RFC822)")
            email_message = email.message_from_bytes(message_data[0][1])

            # Gönderici bilgilerini al
            sender = email_message["From"]
            raw_subject = email_message["Subject"]
            subject = decode_mime_words(raw_subject)  # Konuyu UTF-8'e çevir

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
                    name, phone_number = extract_info_from_email(body)
                    break

            # Eğer isim 3 harften kısa ise mesaj gönderme
            if name and len(name) < 3:
                print(f"⛔ Geçersiz isim: {name}, mesaj gönderilmeyecek.")
                continue

            # Eğer telefon numarası bulunduysa ve bu kişiye mesaj atılmadıysa, mesaj at
            if phone_number and phone_number not in processed_emails:
                send_whatsapp_message(phone_number, name)
                processed_emails.append(phone_number)

            # İşlenmiş e-posta listesini güncelle
            processed_emails.append(message_id.decode())
            with open(PROCESSED_EMAILS_FILE, "w") as f:
                json.dump(processed_emails, f)

        # Bağlantıyı kapat
        imap.close()
        imap.logout()

    except Exception as e:
        print(f"❌ Hata: {e}")


# 📌 5 dakikada bir çalıştıran döngü
while True:
    print("📡 Yeni e-postalar kontrol ediliyor...")
    check_new_emails()
    print("⏳ 5 dakika bekleniyor...")
    time.sleep(30)  # 300 saniye = 5 dakika
