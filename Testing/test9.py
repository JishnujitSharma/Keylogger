import socket
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import time

# Email credentials
SENDER_EMAIL = "bytessquad2024@gmail.com"
SENDER_PASSWORD = "lzvi hnmt caxz ixsu"
RECEIVER_EMAIL = "jishnujitshama@gmail.com"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

# Function to get the current IP address
def get_ip_address():
    try:
        # Retrieve the hostname
        hostname = socket.gethostname()
        # Get the IP address
        ip_address = socket.gethostbyname(hostname)
        return ip_address
    except Exception as e:
        return f"Error fetching IP address: {e}"

# Function to send an email with the IP address
def send_email_with_ip(ip_address):
    try:
        msg = MIMEMultipart()
        msg['From'] = SENDER_EMAIL
        msg['To'] = RECEIVER_EMAIL
        msg['Subject'] = "IP Address Monitoring Report"

        # Add IP address to email body
        body = f"The current IP address of the system is:\n{ip_address}"
        msg.attach(MIMEText(body, 'plain'))

        # Send the email
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, msg.as_string())
        print("IP Address email sent successfully!")
        server.quit()
    except Exception as e:
        print(f"Error sending email: {e}")

# Function to monitor IP address changes
def monitor_ip_address():
    try:
        last_ip_address = None
        while True:
            # Get the current IP address
            current_ip_address = get_ip_address()
            
            # If IP address has changed, send an email
            if current_ip_address != last_ip_address:
                print(f"IP address changed to: {current_ip_address}")
                send_email_with_ip(current_ip_address)
                last_ip_address = current_ip_address

            # Check every 5 minutes
            time.sleep(300)
    except Exception as e:
        print(f"Error monitoring IP address: {e}")

# Main program
if __name__ == "__main__":
    print("Starting IP address monitoring...")
    monitor_ip_address()