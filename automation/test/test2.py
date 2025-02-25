import re
import imaplib
import pyautogui
import time

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

# Test the function
a, b = extract_info_from_email("Deneme &  Face Lift Reklam Datası &Suzan rakıcı & 61 433303456 & 61 4333034562& suzzannahh@hotmail.com & august 2025")
print(a, b)
a, b = extract_info_from_email("Deneme &  Face Lift Reklam Datası &Suzan rakıcı & 61+ & +61 476 842 234 &suzzannahh@hotmail.com & august 2025")
print(a, b)