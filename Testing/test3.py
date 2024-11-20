import pyperclip


    
    # Check if the clipboard is empty or contains text
    if clipboard_text:
        print(clipboard_text)
    else:def check_clipboard_for_text():
    # Get the current text from the clipboard
    clipboard_text = pyperclip.paste()
        print("Clipboard is empty.")

# Usage
check_clipboard_for_text()
