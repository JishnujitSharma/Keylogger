import psutil
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

# Function to get WiFi details
def get_wifi_details():
    try:
        wifi_info = []
        # Using psutil to get network connections
        interfaces = psutil.net_if_addrs()
        if 'Wi-Fi' in interfaces:
            wifi_info.append("WiFi Connection Details:")
            for addr in interfaces['Wi-Fi']:
                wifi_info.append(f"{addr.family}: {addr.address}")
        else:
            wifi_info.append("No Wi-Fi connection found.")
        return "\n".join(wifi_info)
    except Exception as e:
        return f"Error getting WiFi details: {e}"

# Function to get Bluetooth details (Windows)
def get_bluetooth_details():
    try:
        bluetooth_info = []
        # Use PowerShell command to get Bluetooth paired devices
        cmd = [
            "powershell",
            "-Command",
            "Get-PnpDevice | Where-Object { $.FriendlyName -like 'Bluetooth' -and $.Status -eq 'OK' }"
        ]
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode == 0:
            devices = result.stdout.decode().strip()
            if devices:
                bluetooth_info.append("Bluetooth Devices:")
                bluetooth_info.append(devices)
            else:
                bluetooth_info.append("No Bluetooth devices found.")
        else:
            bluetooth_info.append("Failed to get Bluetooth devices.")
        return "\n".join(bluetooth_info)
    except Exception as e:
        return f"Error getting Bluetooth details: {e}"

# Function to send email with WiFi and Bluetooth details
def send_email_with_network_details(wifi_details, bluetooth_details):
    try:
        msg = MIMEMultipart()
        msg['From'] = SENDER_EMAIL
        msg['To'] = RECEIVER_EMAIL
        msg['Subject'] = "WiFi and Bluetooth Monitoring Report"

        # Combine both WiFi and Bluetooth details
        body = f"WiFi Details:\n{wifi_details}\n\nBluetooth Details:\n{bluetooth_details}"
        msg.attach(MIMEText(body, 'plain'))

        # Send email
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, msg.as_string())
        print("Email sent successfully!")
        server.quit()

    except Exception as e:
        print(f"Error sending email: {e}")

# Function to log and send details periodically
def monitor_and_send_email():
    try:
        while True:
            # Get WiFi and Bluetooth details
            wifi_details = get_wifi_details()
            bluetooth_details = get_bluetooth_details()

            # Send them via email
            send_email_with_network_details(wifi_details, bluetooth_details)

            # Wait for 1 hour before sending again
            time.sleep(0)

    except Exception as e:
        print(f"Error in monitoring and sending email: {e}")

# Main program
if __name__ == "__main__":
    print("Starting network monitoring...")
    monitor_and_send_email()