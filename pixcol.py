import pyautogui
from PIL import ImageGrab
import tkinter as tk
import keyboard
import pyperclip
import threading
import colorsys


def rgb_to_hex(rgb):
    """Convert RGB to HEX."""
    return "#{:02x}{:02x}{:02x}".format(rgb[0], rgb[1], rgb[2])


def rgb_to_hsl(rgb):
    """Convert RGB to HSL."""
    r, g, b = [x / 255.0 for x in rgb]
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    return round(h * 360), round(s * 100), round(l * 100)


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
            hsl_color = rgb_to_hsl(color)

            # Update the labels in the window
            rgb_label.config(text=f"RGB: {color}")
            hex_label.config(text=f"Hex: {hex_color}")
            hsl_label.config(text=f"HSL: {hsl_color}")

            # Update the color box
            color_box.config(bg=hex_color)

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
    hsl_color = rgb_to_hsl(color)

    color_info = f"RGB: {color}\nHex: {hex_color}\nHSL: {hsl_color}"
    pyperclip.copy(color_info)

    # Display a message in the window
    message_label.config(text="Colors copied to clipboard!")
    root.after(2000, lambda: message_label.config(text=""))  # Clear message after 2 seconds
    print(color_info)


def on_closing():
    """Stop the program when the window is closed."""
    global running
    running = False
    root.destroy()


# Initialize tkinter window
root = tk.Tk()
root.title("Fab's Pixel Color")
root.geometry("600x400")
root.attributes('-topmost', True)  # Always on top

# Add title inside the window
title_label = tk.Label(root, text="Fab's Pixel Color", font=("Helvetica", 11))
title_label.pack(pady=10)

# Add message below the title
message_label = tk.Label(root, text="Press Ctrl + $ to copy the colors to the clipboard", font=("Helvetica", 9))
message_label.pack(pady=5)


# Create a box to show the color
color_box = tk.Label(root, width=5, height=2, bg="white", relief="solid")
color_box.pack(pady=5)

# Create labels to display color information
rgb_label = tk.Label(root, text="RGB: ")
rgb_label.pack(pady=2)

hex_label = tk.Label(root, text="Hex: ")
hex_label.pack(pady=2)

hsl_label = tk.Label(root, text="HSL: ")
hsl_label.pack(pady=2)

# Create a label for messages
message_label = tk.Label(root, text="", fg="green")
message_label.pack(pady=5)

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
