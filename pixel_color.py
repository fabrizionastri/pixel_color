import pyautogui
from PIL import ImageGrab
print("Packages are working!")

# Get the current mouse position
x, y = pyautogui.position()
# Capture the screen
screen = ImageGrab.grab()
# Get the color at the mouse position
color = screen.getpixel((x, y))
print(f"RGB Color: {color}")
