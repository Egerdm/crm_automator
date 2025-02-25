import re

class EmailProcessor:
    def __init__(self):
        pass

    def extract_info_from_email(self, body):
        """E-posta içeriğinden ismi, telefon numarasını ve tam ismi çıkarır."""
        # Yeni formatı kontrol et
        if body.startswith("Deneme"):
            parts = body.split('&')
            if len(parts) >= 6:
                full_name = parts[2].strip()
                country_code = parts[3].strip().replace(" ", "").replace("+", "")
                phone_number = parts[4].strip().replace(" ", "")
                
                # Eğer country_code kısmında tam numara varsa ve + ile başlamıyorsa
                if phone_number.startswith(country_code):
                    phone_number = f"+{phone_number}"
                elif not phone_number.startswith("+"):
                    phone_number = f"+{country_code}{phone_number}"

                # Ensure the phone number starts with the country code
                if not phone_number.startswith("+"):
                    phone_number = f"+{country_code}{phone_number}"

                first_name = full_name.split()[0]

                # Aynı isim doğrulamalarını yap
                if len(first_name) < 3:
                    print(f"⛔ Geçersiz isim: {first_name}, mesaj gönderilmeyecek.")
                    return None, None, None

                if any(char.isdigit() for char in first_name):
                    print(f"⛔ Geçersiz isim (sayı içeriyor): {first_name}, mesaj gönderilmeyecek.")
                    return None, None, None

                if not first_name.isalpha():
                    print(f"⛔ Geçersiz isim (özel karakter içeriyor): {first_name}, mesaj gönderilmeyecek.")
                    return None, None, None

                if len(first_name) > 20:
                    print(f"⛔ Geçersiz isim (çok uzun): {first_name}, mesaj gönderilmeyecek.")
                    return None, None, None

                return first_name, phone_number, full_name

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
                return None, None, None

            # Eğer isimde sayı varsa geçersiz say
            if any(char.isdigit() for char in first_name):
                print(f"⛔ Geçersiz isim (sayı içeriyor): {first_name}, mesaj gönderilmeyecek.")
                return None, None, None

            # Eğer isimde özel karakter varsa geçersiz say
            if not first_name.isalpha():
                print(f"⛔ Geçersiz isim (özel karakter içeriyor): {first_name}, mesaj gönderilmeyecek.")
                return None, None, None

            # Eğer isim çok uzunsa geçersiz say
            if len(first_name) > 20:
                print(f"⛔ Geçersiz isim (çok uzun): {first_name}, mesaj gönderilmeyecek.")
                return None, None, None

            # Telefon numarası doğrulama
            if not phone_number.startswith("+"):
                print(f"⛔ Geçersiz telefon numarası (ülke kodu eksik): {phone_number}, mesaj gönderilmeyecek.")
                return None, None, None

            # Eğer telefon numarası 0 ile başlıyorsa, 0'ı ülke kodu ile değiştir
            if phone_number.startswith("0"):
                phone_number = phone_number[1:]
                phone_number = f"+{country_code}{phone_number}"

            return first_name, phone_number, full_name

        return None, None, None

# Test the class   
if __name__ == "__main__":
    email_processor = EmailProcessor()
    email_body = "Deneme &  Face Lift Reklam Datası &Suzy rakoci & DONT KNOW & 07919 215503 & suzzanna37@hotmail.com & august 2025"
    first_name, phone_number, full_name = email_processor.extract_info_from_email(email_body)
    print(first_name, phone_number, full_name) # Should print Suzy +61476879302 Suzy rakoci

    email_body_old = "Face Lift Reklam Datası &JacquiPalfrey & +61433271508 & jacq.oz@hotmail.com & Unsure & Whatsapp & 55-64 ."
    first_name, phone_number, full_name = email_processor.extract_info_from_email(email_body_old)
    print(first_name, phone_number, full_name) # Should print Jacqui +61433271508 JacquiPalfrey