import os
import psutil
import platform
import socket
import time
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from email.mime.multipart import MIMEMultipart
import smtplib
import logging
import os

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def get_system_configuration():
    """
    Collect and return key system configuration details.
    """
    config = {}

    # System Info
    config['System'] = platform.system()
    config['Node Name'] = platform.node()
    config['Release'] = platform.release()
    config['Version'] = platform.version()
    config['Architecture'] = platform.architecture()[0]

    # CPU Info
    config['CPU Count'] = psutil.cpu_count(logical=True)
    config['CPU Usage (%)'] = psutil.cpu_percent(interval=1)

    # Memory Info
    mem = psutil.virtual_memory()
    config['Total Memory (GB)'] = round(mem.total / (1024 ** 3), 2)
    config['Available Memory (GB)'] = round(mem.available / (1024 ** 3), 2)
    config['Memory Usage (%)'] = mem.percent

    # Disk Info
    disk = psutil.disk_usage('/')
    config['Total Disk Space (GB)'] = round(disk.total / (1024 ** 3), 2)
    config['Used Disk Space (GB)'] = round(disk.used / (1024 ** 3), 2)
    config['Free Disk Space (GB)'] = round(disk.free / (1024 ** 3), 2)
    config['Disk Usage (%)'] = disk.percent

    # Network Info
    try:
        hostname = socket.gethostname()
        config['Hostname'] = hostname
        config['IP Address'] = socket.gethostbyname(hostname)
    except Exception as e:
        config['Hostname'] = "N/A"
        config['IP Address'] = f"Error: {e}"

    return config

def send_email(receiver_email, subject, body):
    """
    Send an email with the specified subject and body.
    """
    try:
        sender_email = os.getenv("bytessquad2024@gmail.com")
        password = os.getenv("lzvi hnmt caxz ixsu")  # Use environment variables for security
        
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = receiver_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))
        
        if attachment_path and os.path.exists(attachment_path):
            with open(attachment_path, 'rb') as file:
                attachment = MIMEBase('application', 'octet-stream')
                attachment.set_payload(file.read())
                encoders.encode_base64(attachment)
                attachment.add_header(
                    'Content-Disposition',
                    f'attachment; filename={os.path.basename(attachment_path)}'
                )
                msg.attach(attachment)

        # Connect to SMTP server
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        logging.info("Email sent successfully!")
    except Exception as e:
        logging.error(f"Error sending email: {e}")
    finally:
        try:
            server.quit()
        except Exception as e:
            logging.error(f"Error closing SMTP server: {e}")

def system_monitor_email(log_interval=3600, receiver_email="jishnujitshama@gmail.com"):
    """
    Monitor system configuration and send it via email at regular intervals.
    
    Args:
        log_interval (int): Time interval in seconds between emails.
        receiver_email (str): Recipient email address.
    """
    logging.info("System Configuration Monitor started.")
    while True:
        try:
            # Collect system configuration
            config = get_system_configuration()
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Prepare email content
            email_body = f"System Configuration Report - {timestamp}\n\n"
            for key, value in config.items():
                email_body += f"{key}: {value}\n"
            
            # Send email
            send_email(receiver_email, f"System Configuration Report - {timestamp}", email_body)
        except Exception as e:
            logging.error(f"Error in system monitoring: {e}")
        
        # Wait for the next interval
        time.sleep(log_interval)

# Example Usage
if __name__ == "__main__":
    system_monitor_email(log_interval=3600, receiver_email="jishnujitshama@gmail.com")
