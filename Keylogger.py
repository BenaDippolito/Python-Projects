from pynput import keyboard

def on_press(key):
    """Callback when a key is pressed."""
    try:
        print(f"Key pressed: {key.char}")  # Printable character
    except AttributeError:
        print(f"Special key pressed: {key}")  # Special keys like shift, ctrl, etc.

def on_release(key):
    """Callback when a key is released."""
    print(f"Key released: {key}")
    # Stop listener if ESC is released
    if key == keyboard.Key.esc:
        print("Exiting listener...")
        return False  # Returning False stops the listener

# Create and start the listener
with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
