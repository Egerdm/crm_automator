import webbrowser
import time
import pyautogui

phone_number = "+905448101092"  # Ülke kodu ile birlikte numara
message = "Hello, this is a test message."

# 📌 WhatsApp Web URL formatında aç
whatsapp_url = f"https://web.whatsapp.com/send?phone={phone_number}&text={message}"
webbrowser.open(whatsapp_url)

# ⏳ WhatsApp Web’in açılmasını bekle (sen kendi hızına göre artırabilirsin)
time.sleep(20)

# ✅ Enter tuşuna basarak mesajı gönder
pyautogui.press("enter")

print("✅ Mesaj başarıyla gönderildi!")
