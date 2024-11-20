import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(sender_email, receiver_email, subject, body, password):
    # Create a multipart message
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject
    
    # Add body to email
    msg.attach(MIMEText(body, 'plain'))

    try:
        # Connect to the server
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()  # Use TLS
        server.login(sender_email, password)
        
        # Send the email
        server.sendmail(sender_email, receiver_email, msg.as_string())
        print("Email sent successfully!")
    except Exception as e:
        print(f"Error occurred: {e}")
    finally:
        server.quit()

# Usage
sender_email = "bytessquad2024@gmail.com"
receiver_email = "jishnujitshama@gmail.com"
subject = "Test Email"
body = "Hello, this is a test email from Python!"
password = "lzvi hnmt caxz ixsu"  # Use app password if 2FA is enabled

send_email(sender_email, receiver_email, subject, body, password)
