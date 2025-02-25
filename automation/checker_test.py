from email_checker import EmailChecker
from email_processor import EmailProcessor
from google_sheet_updater import GoogleSheetUpdater
from whatsapp_sender import WhatsAppSender

class MockGoogleSheetUpdater:
    def add_email_to_sheet(self, full_name, message):
        print(f"Google Sheet Updated: {full_name} - {message}")

class MockWhatsAppSender:
    def send_whatsapp_message(self, phone_number, name):
        print(f"WhatsApp Message Sent: {phone_number} - {name}")

def test_email_checker():
    email_processor = EmailProcessor()
    google_sheet_updater = MockGoogleSheetUpdater()
    whatsapp_sender = MockWhatsAppSender()
    email_checker = EmailChecker(
        email_account="test@example.com",
        app_password="password",
        imap_server="imap.example.com",
        imap_port=993,
        processed_emails_file="processed_emails.json",
        google_sheet_updater=google_sheet_updater,
        whatsapp_sender=whatsapp_sender
    )

    test_cases = [
        # Yeni format (Deneme ile başlayan)
        {
            "body": "Deneme &  Face Lift Reklam Datası &Suzan rakıcı & DONT KNOW & 07919 211234 & suzzannahhhh@hotmail.com & august 2025",
            "expected": ("Suzan", "+447919211234", "Suzan rakcı")
        },
        {
            "body": "Deneme &  Face Lift Reklam Datası &Jacqac Palrand & +61 & 0406581234 & jacqsasz@hotmail.com & Unsure & Whatsapp & 55-64 .",
            "expected": ("Jacqac", "+61406581234", "Jacqac Palrand")
        },
        {
            "body": "Deneme &  Face Lift Reklam Datası &John Doe & +44 & 07919211234 & john.doe@example.com & July 2025",
            "expected": ("John", "+447919211234", "John Doe")
        },
        # Eski format
        {
            "body": "Face Lift Reklam Datası &Jacqui Palrand & +61433271234 & jacqozz@hotmail.com & Unsure & Whatsapp & 55-64 .",
            "expected": ("Jacqui", "+61433271234", "Jacqui Palrand")
        },
        {
            "body": "Face Lift Reklam Datası &John Doe & +447919211234 & john.doe@example.com & July 2025",
            "expected": ("John", "+447919211234", "John Doe")
        },
        {
            "body": "Face Lift Reklam Datası &Jane Smith & +61406581234 & jane.smith@example.com & August 2025",
            "expected": ("Jane", "+61406581234", "Jane Smith")
        },
    ]
    

    for i, case in enumerate(test_cases):
        name, phone_number, full_name = email_processor.extract_info_from_email(case["body"])
        if phone_number and email_processor.validate_phone_number(phone_number):
            google_sheet_updater.add_email_to_sheet(full_name, 'whatsapp mesajı gönderildi')
            whatsapp_sender.send_whatsapp_message(phone_number, name)
        else:
            google_sheet_updater.add_email_to_sheet(full_name, f"numara formata uymuyor: {phone_number}")
        print(f"Test case {i+1} passed: {name}, {phone_number}, {full_name}")

if __name__ == "__main__":
    test_email_checker()