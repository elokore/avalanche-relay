import imaplib
import email
from email.header import decode_header

# Connect to the email server
imap_server = "imap.gmail.com"  # For Gmail
email_address = "avalancherelay@gmail.com"
password = "hknw ibzt tljs raex "

def _get_email_body(msg):
    body = ""
    
    if msg.is_multipart():
        # Walk through all parts of the email
        for part in msg.walk():
            content_type = part.get_content_type()
            content_disposition = str(part.get("Content-Disposition"))
            
            # Look for plain text parts that aren't attachments
            if content_type == "text/plain" and "attachment" not in content_disposition:
                try:
                    body = part.get_payload(decode=True).decode()
                    break  # Get the first text/plain part
                except:
                    pass
    else:
        # Not multipart - simple text email
        try:
            body = msg.get_payload(decode=True).decode()
        except:
            pass
    
    return body

class EmailMessage:
    def __init__(self, sender, subject, body, id):
        self.sender = sender
        self.subject = subject
        self.body = body
        self.ID = id

class MailReceiver:
    def __init__(self, imapServer, emailAddress, emailPassword):
        self.imap = imaplib.IMAP4_SSL(imapServer)
        self.imap.login(emailAddress, emailPassword)
        self.imap.select("INBOX")

    def getUnreadEmailIDs(self):
        status, messages = self.imap.search(None, "UNSEEN")
        email_ids = messages[0].split()
        if email_ids:
            return email_ids

    def markEmailsAsSeen(self, email_ids):
        idListString = b','.join(email_ids)
        self.imap.store(idListString, '+FLAGS', '\\Seen')

    def getEmail(self, email_ID):
        status, msg_data = self.imap.fetch(email_ID, "(RFC822)")

        for response_part in msg_data:
            if isinstance(response_part, tuple):
                msg = email.message_from_bytes(response_part[1])
                
                # Get email subject
                subject = decode_header(msg["Subject"])[0][0]
                if isinstance(subject, bytes):
                    subject = subject.decode()
                
                # Get sender
                from_ = msg.get("From")
                body = _get_email_body(msg)

                return EmailMessage(from_, subject, body, email_ID)

    def disconnect(self):
        self.imap.close()
        self.imap.logout()

    
mail = MailReceiver(imap_server, email_address, password)
ids = mail.getUnreadEmailIDs()
newMessage = mail.getEmail(ids[0])

print("From:", newMessage.sender)
print("Subject:", newMessage.subject)
print("Body:", newMessage.body)

mail.markEmailsAsSeen(ids)
mail.disconnect()