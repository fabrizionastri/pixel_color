# From ClaudeAI

import tkinter as tk
from PIL import ImageGrab
import pyperclip
import keyboard
from threading import Thread
import sys

class ColorPickerApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Color Picker")
        self.root.geometry("300x150")
        self.root.attributes('-topmost', True)  # Keep window on top

        # Initialize UI elements
        self.setup_ui()

        # Start color tracking
        self.running = True
        self.track_thread = Thread(target=self.track_color)
        self.track_thread.daemon = True
        self.track_thread.start()

        # Setup hotkey
        keyboard.on_press_key("$", self.copy_color_info)

        # Handle window close
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def setup_ui(self):
        # Color preview
        self.color_preview = tk.Canvas(self.root, width=50, height=50)
        self.color_preview.pack(pady=5)

        # Color information labels
        self.rgb_label = tk.Label(self.root, text="RGB: ")
        self.rgb_label.pack()

        self.hex_label = tk.Label(self.root, text="HEX: ")
        self.hex_label.pack()

        self.hsl_label = tk.Label(self.root, text="HSL: ")
        self.hsl_label.pack()

    def rgb_to_hsl(self, r, g, b):
        r, g, b = r/255, g/255, b/255
        max_val = max(r, g, b)
        min_val = min(r, g, b)

        h, s, l = 0, 0, (max_val + min_val) / 2

        if max_val != min_val:
            d = max_val - min_val
            s = d / (2 - max_val - min_val) if l > 0.5 else d / (max_val + min_val)

            if max_val == r:
                h = (g - b) / d + (6 if g < b else 0)
            elif max_val == g:
                h = (b - r) / d + 2
            else:
                h = (r - g) / d + 4

            h /= 6

        return (round(h * 360), round(s * 100), round(l * 100))

    def track_color(self):
        while self.running:
            try:
                # Get mouse position
                x, y = self.root.winfo_pointerxy()

                # Capture pixel color
                pixel = ImageGrab.grab().load()[x, y]

                # Update UI
                self.root.after(0, self.update_ui, pixel)

            except Exception as e:
                print(f"Error: {e}")

            self.root.after(50)  # Update every 50ms

    def update_ui(self, pixel):
        r, g, b = pixel
        hex_color = f"#{r:02x}{g:02x}{b:02x}"
        hsl = self.rgb_to_hsl(r, g, b)

        # Update labels
        self.rgb_label.config(text=f"RGB: {r}, {g}, {b}")
        self.hex_label.config(text=f"HEX: {hex_color}")
        self.hsl_label.config(text=f"HSL: {hsl[0]}°, {hsl[1]}%, {hsl[2]}%")

        # Update color preview
        self.color_preview.configure(bg=hex_color)

    def copy_color_info(self, e):
        if keyboard.is_pressed('ctrl'):
            color_info = (
                f"{self.rgb_label['text']}\n"
                f"{self.hex_label['text']}\n"
                f"{self.hsl_label['text']}"
            )
            pyperclip.copy(color_info)
            print("\nColor information copied to clipboard:")
            print(color_info)

    def on_closing(self):
        self.running = False
        self.root.quit()
        sys.exit()

if __name__ == "__main__":
    app = ColorPickerApp()
    app.root.mainloop()