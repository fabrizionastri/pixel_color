import pyautogui
from PIL import ImageGrab
import tkinter as tk
import keyboard
import pyperclip
import threading


def rgb_to_hex(rgb):
    """Convert RGB to HEX."""
    return "#{:02x}{:02x}{:02x}".format(rgb[0], rgb[1], rgb[2])


def update_color():
    """Update the color displayed in the window."""
    while running:
        try:
            # Get the current mouse position
            x, y = pyautogui.position()
            # Capture the screen
            screen = ImageGrab.grab()
            # Get the color at the mouse position
            color = screen.getpixel((x, y))
            hex_color = rgb_to_hex(color)

            # Update the labels in the window
            rgb_label.config(text=f"RGB: {color}")
            hex_label.config(text=f"Hex: {hex_color}")

            # Update the window
            root.update()
        except tk.TclError:
            break  # Exit the loop if the window is closed


def copy_to_clipboard():
    """Copy color information to the clipboard and print it."""
    x, y = pyautogui.position()
    screen = ImageGrab.grab()
    color = screen.getpixel((x, y))
    hex_color = rgb_to_hex(color)

    color_info = f"RGB: {color}\nHex: {hex_color}"
    pyperclip.copy(color_info)
    print(color_info)


def on_closing():
    """Stop the program when the window is closed."""
    global running
    running = False
    root.destroy()


# Initialize tkinter window
root = tk.Tk()
root.title("Color Picker")
root.geometry("200x100")
root.attributes('-topmost', True)  # Always on top

# Create labels to display color information
rgb_label = tk.Label(root, text="RGB: ")
rgb_label.pack(pady=5)

hex_label = tk.Label(root, text="Hex: ")
hex_label.pack(pady=5)

# Bind Ctrl + $ to copy color info
keyboard.add_hotkey('ctrl+$', copy_to_clipboard)

# Run the update_color function in a separate thread
running = True
thread = threading.Thread(target=update_color, daemon=True)
thread.start()

# Handle window close
root.protocol("WM_DELETE_WINDOW", on_closing)

# Run the tkinter event loop
root.mainloop()
