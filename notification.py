import smtplib
from email.message import EmailMessage
from constants import EMAIL_ADDRESS, SMTP_SERVER, SMTP_PORT, EMAIL_PASSWORD

class EmailSender:

  def __init__(self):
    
    # Initialize with email credentials and SMTP server details
    
    self.email_address = EMAIL_ADDRESS
    self.email_password = EMAIL_PASSWORD
    self.smtp_server = SMTP_SERVER
    self.smtp_port = SMTP_PORT 

  def send_email(self, receiver_address, user_name, attachment_path):
    
    # Compose email subject and content
    
    subject = f"Greetings {user_name}, your Data is Ready to be Downloaded"
    content_text = f"Hi {user_name}, we are excited to inform you that the data you requested has been successfully scraped and is now ready for your use.\n\nYou can download the data from the attachment provided with this email."

    # Extract filename from attachment path
    
    file_name = attachment_path.split('/')[-1].split('.')[0]

    # Create EmailMessage object
    
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = self.email_address
    msg['To'] = receiver_address
    msg.set_content(content_text)
    
    # Add attachment to the email
    
    with open(attachment_path, 'rb') as f:
      file_data = f.read()
    msg.add_attachment(file_data,
                       maintype='text',
                       subtype='plain',
                       filename=attachment_path.split('/')[-1])
    
    # Send the email using SMTP server

    with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
      server.starttls()
      server.login(self.email_address, self.email_password)
      server.send_message(msg)
