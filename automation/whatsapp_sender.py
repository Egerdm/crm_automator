import webbrowser
import time
import pyautogui

class WhatsAppSender:
    def __init__(self):
        pass

    def send_whatsapp_message(self, phone_number, name):
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