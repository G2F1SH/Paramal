#!/usr/bin/env python3

import argparse
import os
import numpy as np
from PIL import Image

def get_target_size(current_size: int, scale: int = 1) -> int:
    """
    scale size
    
    Args:
        current_size: current size
        scale: scale factor, default 1 (no scale)
    """
    return current_size * scale


def blend_overlay(base: np.ndarray, blend: np.ndarray) -> np.ndarray:
    """
    Overlay
    base: 0-255
    blend: 0-255
    """
    base_f = base.astype(np.float32) / 255.0
    blend_f = blend.astype(np.float32) / 255.0
    
    result = np.where(base_f < 0.5,
                      2 * base_f * blend_f,
                      1 - 2 * (1 - base_f) * (1 - blend_f))
    
    return (result * 255).astype(np.uint8)


def sobel_gradients(height: np.ndarray, strength: float) -> tuple[np.ndarray, np.ndarray]:
    """
    Compute Sobel gradients from a height map using edge padding.
    """
    padded = np.pad(height, ((1, 1), (1, 1)), mode='edge')

    top_left = padded[:-2, :-2]
    top = padded[:-2, 1:-1]
    top_right = padded[:-2, 2:]
    left = padded[1:-1, :-2]
    right = padded[1:-1, 2:]
    bottom_left = padded[2:, :-2]
    bottom = padded[2:, 1:-1]
    bottom_right = padded[2:, 2:]

    dx = (
        -top_left + top_right
        - 2.0 * left + 2.0 * right
        - bottom_left + bottom_right
    ) * strength

    dy = (
        top_left + 2.0 * top + top_right
        - bottom_left - 2.0 * bottom - bottom_right
    ) * strength

    dx /= 8.0
    dy /= 8.0

    return dx, dy


def alpha_to_normal(input_path: str, output_path: str,
                    strength: float = 2.0,
                    mode: str = 'opengl',
                    mix: bool = False,
                    scale: int = 1):
    img = Image.open(input_path)

    if img.mode != 'RGBA':
        img = img.convert('RGBA')

    w, h = img.size
    target_w = get_target_size(w, scale)
    target_h = get_target_size(h, scale)

    if scale > 1:
        print(f"Zoom in: {w}x{h} -> {target_w}x{target_h} (x{scale})")
        img = img.resize((target_w, target_h), Image.NEAREST)
    
    img_rgb = img.convert('RGB')
    img_rgb_array = np.array(img_rgb)
    
    height = np.array(img.split()[3], dtype=np.float32)
    
    height = height / 255.0
    
    dx, dy = sobel_gradients(height, strength)
    
    normal_x = -dx
    
    if mode == 'dx':
        normal_y = dy  
    else:
        normal_y = -dy 
    
    normal_z = np.ones_like(height)
    
    length = np.sqrt(normal_x**2 + normal_y**2 + normal_z**2)
    normal_x /= length
    normal_y /= length
    normal_z /= length
    
    r = ((normal_x + 1.0) * 0.5 * 255).astype(np.uint8)
    g = ((normal_y + 1.0) * 0.5 * 255).astype(np.uint8)
    b = (normal_z * 255).astype(np.uint8)
    
    normal_map = np.stack([r, g, b], axis=-1)
    
    if mix:
        print("Blend the original image with the height normal map using overlay mode")
        mixed = np.zeros_like(normal_map)
        for c in range(3):
            mixed[:, :, c] = blend_overlay(img_rgb_array[:, :, c], normal_map[:, :, c])
        result = Image.fromarray(mixed, mode='RGB')
    else:
        result = Image.fromarray(normal_map, mode='RGB')

    output_dir = os.path.dirname(output_path)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Created directory: {output_dir}")

    result.save(output_path)
    
    if mix:
        print(f"Saved successfully by ({mode.upper()} Mode): {output_path}")
    else:
        print(f"Saved successfully by ({mode.upper()} Mode): {output_path}")


def main():
    parser = argparse.ArgumentParser(
        description='alpha channel as height information'
    )
    parser.add_argument('input', help='input path')
    parser.add_argument('output', help='output path')
    parser.add_argument('-s', '--strength', type=float, default=5.0,
                        help='strength,normal is 5.0')
    parser.add_argument('-m', '--mode', choices=['opengl', 'dx'], 
                        default='opengl',
                        help='normal mode: opengl or dx')
    parser.add_argument('--mix', action='store_true',
                        help='mix set')
    parser.add_argument('--scale', type=int, default=1,
                        help='scale factor, default 1 (no scale), e.g. 8 means 16x16 -> 128x128')

    args = parser.parse_args()

    alpha_to_normal(args.input, args.output, args.strength, args.mode, args.mix, args.scale)


if __name__ == '__main__':
    main()
