import keyboard

print("Press any key (Press 'Esc' to stop)...")

# Continuously listen for key presses and print them
while True:
    event = keyboard.read_event()
    
    # Only print on key down events (not on key release)
    if event.event_type == keyboard.KEY_DOWN:
        print(f"Key pressed: {event.name}")
    
