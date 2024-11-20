import subprocess
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

# Function to get the list of installed applications
def get_installed_apps():
    try:
        # Command to fetch installed programs (Windows only)
        cmd = 'wmic product get name,version'
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        output, error = process.communicate()

        if process.returncode != 0:
            raise Exception(f"Command failed: {error.strip()}")

        return output.strip()
    except Exception as e:
        return f"Error fetching installed applications: {e}"

# Function to send the list of installed applications via email
def send_email_with_apps(apps_list):
    try:
        msg = MIMEMultipart()
        msg['From'] = SENDER_EMAIL
        msg['To'] = RECEIVER_EMAIL
        msg['Subject'] = "Installed Applications Report"

        # Add the list to the email body
        body = f"The current list of installed applications:\n\n{apps_list}"
        msg.attach(MIMEText(body, 'plain'))

        # Send the email
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, msg.as_string())
        print("Installed applications email sent successfully!")
        server.quit()
    except Exception as e:
        print(f"Error sending email: {e}")

# Function to monitor installed applications periodically
def monitor_installed_apps():
    try:
        last_apps_list = None
        while True:
            # Get the current list of installed applications
            current_apps_list = get_installed_apps()

            # Send an email if the list changes
            if current_apps_list != last_apps_list:
                print("Installed applications list updated.")
                send_email_with_apps(current_apps_list)
                last_apps_list = current_apps_list

            # Check every 24 hours
            time.sleep(86400)
    except Exception as e:
        print(f"Error monitoring installed applications: {e}")

# Main program
if __name__ == "__main__":
    print("Starting installed applications monitoring...")
    monitor_installed_apps()