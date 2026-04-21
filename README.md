# Paramal
[EN] | [[中文]](README_CN.md)  

A command-line tool for converting alpha channels to normal maps.

## Features

- Convert alpha channel to normal map using height information
- Support for OpenGL and DirectX normal map modes
- Adjustable strength parameter for normal intensity
- Optional overlay blending with original image
- Image scaling support for higher resolution output
- Automatic creation of output directories

## Usage

```bash
python Paramal.py <input> <output> [options]
```

### Options

- `-s, --strength`: Normal strength (default: 5.0)
- `-m, --mode`: Normal mode - `opengl` or `dx` (default: opengl)
- `--mix`: Blend the original image with the normal map using overlay mode
- `--scale`: Scale factor (default: 1, e.g. 8 means 16x16 -> 128x128)

### Examples

```bash
# Basic conversion
python Paramal.py input.png output.png

# Custom strength with DirectX mode
python Paramal.py input.png output.png -s 3.0 -m dx

# Mix with original image and scale up
python Paramal.py input.png output.png --mix --scale 4
```

## Dependencies

```bash
pip install Pillow numpy
```

## Build

```bash
pip install Pillow numpy PyInstaller
python -m PyInstaller --onefile --name Paramal --icon logo.ico Paramal.py
```
