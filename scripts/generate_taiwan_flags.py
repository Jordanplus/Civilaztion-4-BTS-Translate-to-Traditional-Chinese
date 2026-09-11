"""
Generate official Republic of China (青天白日滿地紅) Flag and Civilization Button
for Civilization IV: Beyond the Sword (Taiwan Civilization).

Geometry strictly follows the Republic of China National Emblem and National Flag Act
(中華民國國徽國旗法):
- Flag field: Red (RGB 222, 41, 16 / Pantone 186 C)
- Canton: Navy Blue (RGB 0, 0, 149 / Pantone 280 C), occupying the top-left 1/2 x 1/2 quadrant
- White Sun: Centered at (1/4 width, 1/4 height)
- Dimensions based on canton height (L):
  - Ray tip outer radius: 3/8 L (12 rays at 30-degree intervals)
  - Blue separating ring: outer radius 17/80 L (width = 1/15 of sun diameter = 1/40 L)
  - White sun disc: radius 3/16 L (diameter = 3/8 L)
"""

import os
import io
import math
import base64
import numpy as np
from PIL import Image, ImageDraw

# Embedded official Civ4 civilization button frame overlay and corner alpha mask
B64_FRAME_OVERLAY = "iVBORw0KGgoAAAANSUhEUgAAAEAAAABACAYAAACqaXHeAAADfElEQVR4nO2bzY4TORDH/13+wEmHpEeIEVduPAcSBzjyGhwRb8B5T7wG3BgOPAC3Pa3EBYnjIGAmYTSZeDpfK7e703YnE2Z22cO6+Ekdp2J12lXtr7LL2cNHz9YIMNKEIixsJJuFxF7kYm92/G83xyAuHzrFGSN+fs/uL48EM0xf8TaAvZhXRjC5up4BjKQ6FdXVrYHbDKrP6dkU6pbCaKQxuyhhZ3NfgDrtojP/nHK9in5Xqn1jQggUhS9AaZfQRqAXaDCzSxgLjMvlzwrpdco1JGSnVS7+3Hw9ev8hQwI8efy07efMfZ8ojaJn4M2+g1SUdxy9exPpUgwNipHBwai32wApKd81QqN8A3FQvmsE9+bd5YhGfWVKpM7B4QHyw8ONTGDKcJRXaWQAIa83fKRkBAJzpA1mNj+d4yRA4WZKzsNZiEpmVwNU7tt+A4E5BGboTg2QhRz/Omf9f4AW3gBGym1vkALPK1VIZlc3AZ17V5YTFArl9BzckHbhnQJHMUh/gUiquAlIMIME8R4GuxCYI8NldMtgHoBaYQXfFxCYQ2AOhYI937+NlCIyXBVU/fTXBFtt/VYBgTkE5lAoCB3vy3FAhosAdoLkWWUa5bqEznQlRzXg/oN74ECj/JYBpmcspoIRBObI0BfIdfo1YIE1VmsBypZ8a0Cj/HYfcM5rb5BtDdCijVOS4aKYcEFQiSNuKSyhsFpcVDK7GiBkOwdgaYCuESjMOP6S/jDYRYYecnEv2CdMlBxz3k0gH/yOD0BoBAlm5Ldr5b/4RIbh9O0uYbocFN7l/4jjKmXXB3QhMIfAHBnuC8xs+r2AgcVfnz5vAqJok6FK2DL9GCHH1/Hkiq2xOQ8DhFAoFLl3EVPGV/8W6dqEI+8Z6NtDpM7ZeBLFRMt82Ip5fYqCE5SPDNzlmP6Y4dmL59FJ0pR4ffR2Szdyb91fbU1I0Qi7lHdkL/94FWcYg2LQNgW1avvJ+apzqJEIc7rphmpraJ1dgtbx48v6AKUWzaqNhSB/j9YF1ssJTM/Lvb7BncEQh3fvbO63daDT99MxTk4nOAmGvF3Ifl9B62AxVF7dDzQBxjGtAvPg+39BWU6ghDt9ajdGcHz9duLT7yfVdRNkpPwOBF1/ttxEXu0jyy735q/qo7N24d+kkcBy1S7VLesgFmeEySlw3Pi1/xD6V3cnwN8bZOC9CeEcGgAAAABJRU5ErkJggg=="
B64_CORNER_ALPHA = "iVBORw0KGgoAAAANSUhEUgAAAEAAAABACAAAAACPAi4CAAAAuklEQVR4nO2XwQ2DMAxFv71BGIGu0hUyC8wEK7BKV4hHSGVKpZZTY0eiBz+J4//EL7kY6ETKS6m/UpacTvmptjJ9xsdqYdyzpPmHcW46vmoVp2EGvqZpQpOEVMwFGASMuz2vWUZ2FGQdoZzfRAMygOx3oJDegg+OAoQDhAOEg3DwguGEowDhAOEA4eBfHIgjLVqwOQo2LVgdBWuXfUFmc36WPjsTbuYjHCWozhOAqN3DTLT//I13d76QJ+Oi1o94hQ8SAAAAAElFTkSuQmCC"

def render_roc_flag(width=1024, height=1024):
    """
    Renders the ROC flag with 8x supersampling for high-quality antialiasing.
    """
    RED = (222, 41, 16, 255)
    BLUE = (0, 0, 149, 255)
    WHITE = (255, 255, 255, 255)

    img = Image.new('RGBA', (width, height), RED)
    draw = ImageDraw.Draw(img)

    # Canton (Top-left quadrant)
    canton_w = width // 2
    canton_h = height // 2
    draw.rectangle([0, 0, canton_w, canton_h], fill=BLUE)

    cx = canton_w / 2.0
    cy = canton_h / 2.0
    L = float(canton_h)

    # Statutory dimensions
    r_outer = (3.0 / 8.0) * L       # 12-ray tip radius
    r_disc = (3.0 / 16.0) * L       # Central white disc radius
    r_ring = (17.0 / 80.0) * L      # Blue ring outer radius (disc + 1/40 L)

    # Draw 12 rays: each ray is an isosceles triangle with 30-degree apex
    # First ray points straight up (-90 degrees)
    for i in range(12):
        angle = math.radians(i * 30.0 - 90.0)
        tip = (cx + r_outer * math.cos(angle), cy + r_outer * math.sin(angle))
        left_angle = math.radians(i * 30.0 - 90.0 - 15.0)
        right_angle = math.radians(i * 30.0 - 90.0 + 15.0)
        base_l = (cx + r_outer * 0.5 * math.cos(left_angle), cy + r_outer * 0.5 * math.sin(left_angle))
        base_r = (cx + r_outer * 0.5 * math.cos(right_angle), cy + r_outer * 0.5 * math.sin(right_angle))
        draw.polygon([tip, (cx, cy), base_l], fill=WHITE)
        draw.polygon([tip, (cx, cy), base_r], fill=WHITE)

    # Blue ring separating rays from inner disc
    draw.ellipse([cx - r_ring, cy - r_ring, cx + r_ring, cy + r_ring], fill=BLUE)

    # Central white sun disc
    draw.ellipse([cx - r_disc, cy - r_disc, cx + r_disc, cy + r_disc], fill=WHITE)

    return img

def create_teamcolor_flag(flag_high):
    """
    Creates 128x128 TeamColor/TaiwanFlag.dds
    For bWhiteFlag=1, alpha channel must be 0.
    """
    im128 = flag_high.resize((128, 128), Image.Resampling.LANCZOS)
    arr = np.array(im128)
    arr[:, :, 3] = 0  # Civ4 white flag requirement
    return Image.fromarray(arr, 'RGBA')

def create_civ_button(flag_high):
    """
    Creates 64x64 Buttons/Civilizations/TaiwanFlag.dds
    Applies the official Civ4 civilization button metallic border frame and alpha mask.
    """
    flag_btn = flag_high.resize((64, 64), Image.Resampling.LANCZOS)
    flag_arr = np.array(flag_btn).astype(float)

    # Subtle inner bevel and directional lighting
    y_coords, x_coords = np.mgrid[0:64, 0:64]
    dist_left = np.clip(x_coords - 4, 0, 6) / 6.0
    dist_right = np.clip(59 - x_coords, 0, 6) / 6.0
    dist_top = np.clip(y_coords - 4, 0, 6) / 6.0
    dist_bottom = np.clip(59 - y_coords, 0, 6) / 6.0
    vignette = 0.92 + 0.08 * (dist_left * dist_right * dist_top * dist_bottom)
    diag = ((64 - x_coords) + (64 - y_coords)) / 128.0
    sheen = 1.0 + 0.05 * (diag - 0.5)

    for c in range(3):
        flag_arr[:, :, c] = np.clip(flag_arr[:, :, c] * vignette * sheen, 0, 255)

    base_img = Image.fromarray(flag_arr.astype(np.uint8), 'RGBA')

    # Alpha composite the official Civ4 frame overlay
    overlay_bytes = base64.b64decode(B64_FRAME_OVERLAY)
    overlay = Image.open(io.BytesIO(overlay_bytes))
    base_img.alpha_composite(overlay)

    # Apply corner alpha mask
    corner_bytes = base64.b64decode(B64_CORNER_ALPHA)
    corner_alpha = Image.open(io.BytesIO(corner_bytes))

    arr = np.array(base_img)
    arr[:, :, 3] = np.array(corner_alpha)

    # Set outside pixels to dark border tone so no color fringe bleeds
    zero_alpha = (arr[:, :, 3] == 0)
    arr[zero_alpha, 0] = 66
    arr[zero_alpha, 1] = 69
    arr[zero_alpha, 2] = 107

    return Image.fromarray(arr, 'RGBA')

def main():
    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    teamcolor_dest = os.path.join(
        repo_root, "patch", "PatchFiles", "Beyond the Sword", "Assets",
        "Art", "Interface", "TeamColor", "TaiwanFlag.dds"
    )
    button_dest = os.path.join(
        repo_root, "patch", "PatchFiles", "Beyond the Sword", "Assets",
        "Art", "Interface", "Buttons", "Civilizations", "TaiwanFlag.dds"
    )

    print("Rendering high-resolution ROC flag (1024x1024)...")
    flag_1024 = render_roc_flag(1024, 1024)

    print(f"Generating TeamColor flag (128x128) -> {teamcolor_dest}")
    flag_128 = create_teamcolor_flag(flag_1024)
    os.makedirs(os.path.dirname(teamcolor_dest), exist_ok=True)
    flag_128.save(teamcolor_dest, format="DDS")

    print(f"Generating Civilization button (64x64) -> {button_dest}")
    btn_64 = create_civ_button(flag_1024)
    os.makedirs(os.path.dirname(button_dest), exist_ok=True)
    btn_64.save(button_dest, format="DDS")

    print("Done! ROC flag and button textures successfully generated.")

if __name__ == "__main__":
    main()
