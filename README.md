# Fab's Pixel Color

A simple app that gives the color of a pixel on the screen that your mouse is hovering over. It shows the color in a box and provides the color in 3 formats: RGB, HEX, and HSL.
Press `Ctrl + $` to copy the color to your clipboard.

## Installation

- install rye on your machine (see [rye](https://rye.astral.sh/))
- `rye rye` to install the dependencies from the `rye.toml` file
- `python pixcol.py` to run the app
- `Ctrl + $` to copy the color to your clipboard

## Creating the executable

- `rye add pyinstaller` to instal PyInstaller with Rye
- `rye run pyinstaller --onefile --noconsole pixcol.py` to create the executable
- The executable will be in the `dist` folder
