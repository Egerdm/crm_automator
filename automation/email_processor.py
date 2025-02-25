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

                # Telefon numarasını formatla
                phone_number = self.format_phone_number(phone_number, country_code)

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

    def format_phone_number(self, phone_number, country_code):
        """Telefon numarasını doğru formata getirir."""
        phone_number = phone_number.replace(" ", "")
        if phone_number.startswith("0"):
            phone_number = phone_number[1:]
            if country_code == "44" or phone_number.startswith("7"):
                phone_number = f"+44{phone_number}"
            elif country_code == "61" or phone_number.startswith("4"):
                phone_number = f"+61{phone_number}"
        elif not phone_number.startswith("+"):
            if phone_number.startswith("4"):
                phone_number = f"+61{phone_number}"
            elif phone_number.startswith("7"):
                phone_number = f"+44{phone_number}"
            else:
                phone_number = f"+{country_code}{phone_number}"
        return phone_number

    def validate_phone_number(self, phone_number):
        """Telefon numarasını doğrular ve ülke koduna göre formatını kontrol eder."""
        # Örnek ülke kodu ve formatları
        country_code_formats = {
            "61": r"^\+61\d{9}$",  # Australia
            "44": r"^\+44\d{10}$",  # United Kingdom
            "90": r"^\+90\d{10}$",  # Turkey
            # Diğer ülke kodları ve formatları buraya eklenebilir
        }

        for country_code, pattern in country_code_formats.items():
            if phone_number.startswith(f"+{country_code}"):
                if re.match(pattern, phone_number):
                    return True
                else:
                    return False
        return False

# Test the class   
if __name__ == "__main__":
    email_processor = EmailProcessor()
    email_body = "Deneme &  Face Lift Reklam Datası &Suzy rakıcı & 61 433303456 & 61 4333034562& suzzannahh@hotmail.com & august 2025"
    first_name, phone_number, full_name = email_processor.extract_info_from_email(email_body)
    print(first_name, phone_number, full_name) # Should print Suzy +61433300212 Suzy rakoci

    email_body_old = "Face Lift Reklam Datası &JacqualPalkan & +61433365436 & jacqazz@hotmail.com & Unsure & Whatsapp & 55-64 ."
    first_name, phone_number, full_name = email_processor.extract_info_from_email(email_body_old)
    print(first_name, phone_number, full_name) # Should print Jacqui +61433271508 JacquiPalfrey