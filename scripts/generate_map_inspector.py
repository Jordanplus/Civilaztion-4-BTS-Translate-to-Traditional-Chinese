import os
import re
import json
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WBSAVE_PATH = os.path.join(ROOT, "patch", "PatchFiles", "Beyond the Sword", "PublicMaps", "The Earth.CivBeyondSwordWBSave")

PREVIEW_FULL_PNG = os.path.join(ROOT, "the_earth_map_preview.png")
PREVIEW_AUS_PNG = os.path.join(ROOT, "the_earth_australia_preview.png")
PREVIEW_SCAN_PNG = os.path.join(ROOT, "the_earth_scandinavia_preview.png")
HTML_INSPECTOR = os.path.join(ROOT, "inspect_the_earth.html")

FONT_PATH = r"C:\Windows\Fonts\msyh.ttc"

TERRAIN_COLORS = {
    "TERRAIN_OCEAN": (15, 45, 89),
    "TERRAIN_COAST": (31, 89, 130),
    "TERRAIN_GRASS": (74, 124, 54),
    "TERRAIN_PLAINS": (138, 132, 74),
    "TERRAIN_DESERT": (212, 183, 110),
    "TERRAIN_TUNDRA": (108, 120, 102),
    "TERRAIN_SNOW": (230, 237, 240),
}

FEATURE_COLORS = {
    "FEATURE_FOREST": (35, 74, 26),
    "FEATURE_JUNGLE": (22, 64, 22),
    "FEATURE_FLOOD_PLAINS": (82, 153, 56),
    "FEATURE_OASIS": (43, 153, 128),
    "FEATURE_ICE": (206, 227, 235),
}

RIVER_COLOR = (72, 181, 242)

CIVS_INFO = {
    (118, 16): {"name": "台灣 (蔡英文)", "en": "Taiwan (Tsai)", "color": (30, 90, 220), "symbol": "TW"},
    (102, 47): {"name": "中國 (秦始皇)", "en": "China (Qin)", "color": (210, 30, 30), "symbol": "CN"},
    (113, 45): {"name": "日本 (德川家康)", "en": "Japan (Tokugawa)", "color": (180, 20, 40), "symbol": "JP"},
    (90, 40):  {"name": "印度 (阿育王)", "en": "India (Asoka)", "color": (230, 130, 20), "symbol": "IN"},
    (69, 37):  {"name": "埃及 (哈特謝普蘇特)", "en": "Egypt (Hatshepsut)", "color": (220, 180, 20), "symbol": "EG"},
    (61, 46):  {"name": "羅馬 (凱撒)", "en": "Rome (Caesar)", "color": (130, 20, 120), "symbol": "RO"},
    (62, 52):  {"name": "德國 (腓特烈)", "en": "Germany (Frederick)", "color": (60, 60, 60), "symbol": "DE"},
    (58, 51):  {"name": "法國 (路易十四)", "en": "France (Louis XIV)", "color": (30, 70, 180), "symbol": "FR"},
    (56, 53):  {"name": "英國 (伊莉莎白)", "en": "England (Elizabeth)", "color": (180, 20, 20), "symbol": "GB"},
    (62, 58):  {"name": "維京 (朗納爾)", "en": "Viking (Ragnar)", "color": (140, 60, 180), "symbol": "VK"},
    (73, 54):  {"name": "俄羅斯 (凱薩琳)", "en": "Russia (Catherine)", "color": (160, 30, 30), "symbol": "RU"},
    (82, 40):  {"name": "波斯 (居魯士)", "en": "Persia (Cyrus)", "color": (40, 140, 140), "symbol": "IR"},
    (75, 35):  {"name": "阿拉伯 (薩拉丁)", "en": "Arabia (Saladin)", "color": (20, 140, 40), "symbol": "SA"},
    (99, 51):  {"name": "蒙古 (成吉思汗)", "en": "Mongol (Genghis)", "color": (190, 110, 30), "symbol": "MN"},
    (55, 34):  {"name": "馬利 (曼薩·穆薩)", "en": "Mali (Mansa Musa)", "color": (180, 80, 160), "symbol": "ML"},
    (28, 45):  {"name": "美國 (羅斯福)", "en": "America (Roosevelt)", "color": (20, 50, 160), "symbol": "US"},
    (19, 37):  {"name": "阿茲特克 (蒙特祖瑪)", "en": "Aztec (Montezuma)", "color": (30, 150, 80), "symbol": "MX"},
    (30, 23):  {"name": "印加 (瓦伊納·卡帕克)", "en": "Inca (Huayna)", "color": (200, 160, 30), "symbol": "PE"},
}

RESOURCE_LABELS = {
    "BONUS_FISH": ("魚產", "Fish", (60, 160, 240)),
    "BONUS_CLAM": ("生蠔", "Clams", (120, 200, 230)),
    "BONUS_CRAB": ("螃蟹", "Crab", (240, 90, 60)),
    "BONUS_WHEAT": ("小麥", "Wheat", (245, 210, 80)),
    "BONUS_CORN": ("玉米", "Corn", (240, 220, 50)),
    "BONUS_RICE": ("稻米", "Rice", (210, 240, 120)),
    "BONUS_COW": ("乳牛", "Cow", (160, 120, 70)),
    "BONUS_SHEEP": ("綿羊", "Sheep", (230, 230, 220)),
    "BONUS_PIG": ("生豬", "Pig", (250, 160, 180)),
    "BONUS_DEER": ("野鹿", "Deer", (190, 140, 80)),
    "BONUS_HORSE": ("馬匹", "Horse", (180, 100, 40)),
    "BONUS_GOLD": ("金礦", "Gold", (255, 215, 0)),
    "BONUS_SILVER": ("銀礦", "Silver", (200, 210, 225)),
    "BONUS_COPPER": ("銅礦", "Copper", (205, 127, 50)),
    "BONUS_IRON": ("鐵礦", "Iron", (140, 140, 150)),
    "BONUS_COAL": ("煤礦", "Coal", (40, 40, 45)),
    "BONUS_OIL": ("石油", "Oil", (30, 30, 35)),
    "BONUS_ALUMINUM": ("鋁土", "Aluminum", (180, 200, 210)),
    "BONUS_URANIUM": ("鈾礦", "Uranium", (80, 255, 80)),
    "BONUS_SUGAR": ("甘蔗", "Sugar", (230, 170, 210)),
    "BONUS_SPICES": ("香料", "Spices", (210, 100, 60)),
    "BONUS_SILK": ("絲綢", "Silk", (230, 190, 140)),
    "BONUS_DYE": ("染料", "Dye", (160, 60, 180)),
    "BONUS_WINE": ("葡萄", "Wine", (130, 40, 90)),
    "BONUS_BANANA": ("香蕉", "Banana", (240, 230, 60)),
    "BONUS_GEMS": ("寶石", "Gems", (70, 210, 240)),
    "BONUS_MARBLE": ("大理石", "Marble", (220, 220, 230)),
    "BONUS_STONE": ("採石", "Stone", (150, 150, 150)),
}

def parse_wbsave():
    print(f"Parsing: {WBSAVE_PATH}")
    with open(WBSAVE_PATH, "r", encoding="utf-8") as f:
        text = f.read()

    plot_blocks = re.findall(r"BeginPlot\s+(.*?)\s+EndPlot", text, re.DOTALL)
    plots = {}
    for p in plot_blocks:
        lines = [l.strip() for l in p.split("\n")]
        coords = [l for l in lines if l.startswith("x=")][0].split(",")
        x = int(coords[0].split("=")[1])
        y = int(coords[1].split("=")[1])

        pt = int([l for l in lines if l.startswith("PlotType=")][0].split("=")[1])
        tt = [l for l in lines if l.startswith("TerrainType=")][0].split("=")[1]

        feat_lines = [l for l in lines if l.startswith("FeatureType=")]
        feat = feat_lines[0].split(",")[0].split("=")[1] if feat_lines else None

        bonus_lines = [l for l in lines if l.startswith("BonusType=")]
        bonus = bonus_lines[0].split("=")[1] if bonus_lines else None

        rn = any("isNOfRiver" in l for l in lines)
        rw = any("isWOfRiver" in l for l in lines)
        starting = any("StartingPlot" in l for l in lines)

        plots[(x, y)] = {
            "x": x, "y": y,
            "plot_type": pt,
            "terrain": tt,
            "feature": feat,
            "bonus": bonus,
            "river_n": rn,
            "river_w": rw,
            "starting": starting
        }
    return plots

def render_full_map(plots):
    print("Rendering high-res full world map...")
    tile_size = 18
    w, h = 124 * tile_size, 68 * tile_size
    img = Image.new("RGB", (w, h), (15, 35, 65))
    draw = ImageDraw.Draw(img)

    try:
        font_sm = ImageFont.truetype(FONT_PATH, 11)
        font_badge = ImageFont.truetype(FONT_PATH, 13)
        font_title = ImageFont.truetype(FONT_PATH, 22)
    except:
        font_sm = font_badge = font_title = ImageFont.load_default()

    # Draw tiles
    for (x, y), p in plots.items():
        sy = (67 - y) * tile_size
        sx = x * tile_size

        color = TERRAIN_COLORS.get(p["terrain"], (20, 50, 80))
        draw.rectangle([sx, sy, sx + tile_size - 1, sy + tile_size - 1], fill=color)

        # PlotType (0: Peak, 1: Hill)
        if p["plot_type"] == 0: # Mountain Peak
            draw.polygon([
                (sx + tile_size // 2, sy + 1),
                (sx + 1, sy + tile_size - 1),
                (sx + tile_size - 1, sy + tile_size - 1)
            ], fill=(60, 55, 50), outline=(220, 220, 220))
        elif p["plot_type"] == 1: # Hill
            draw.arc([sx + 2, sy + 3, sx + tile_size - 2, sy + tile_size + 2], start=180, end=360, fill=(45, 40, 35), width=2)

        # Features
        if p["feature"] in FEATURE_COLORS:
            fc = FEATURE_COLORS[p["feature"]]
            if p["feature"] in ["FEATURE_FOREST", "FEATURE_JUNGLE"]:
                draw.ellipse([sx + 3, sy + 3, sx + tile_size - 3, sy + tile_size - 3], fill=fc)
            elif p["feature"] == "FEATURE_ICE":
                draw.rectangle([sx + 1, sy + 1, sx + tile_size - 2, sy + tile_size - 2], fill=fc)
            elif p["feature"] == "FEATURE_FLOOD_PLAINS":
                draw.rectangle([sx + 2, sy + 2, sx + tile_size - 2, sy + tile_size - 2], fill=fc)

        # Rivers
        if p["river_n"]:
            # North of plot in Civ4 means bottom edge of (x,y) tile, which is sy + tile_size in screen coordinates
            draw.line([(sx, sy + tile_size), (sx + tile_size, sy + tile_size)], fill=RIVER_COLOR, width=2)
        if p["river_w"]:
            # West of plot in Civ4 means right edge of (x,y) tile, which is sx + tile_size
            draw.line([(sx + tile_size, sy), (sx + tile_size, sy + tile_size)], fill=RIVER_COLOR, width=2)

    # Draw grid overlay (very subtle)
    for x in range(0, 125):
        draw.line([(x * tile_size, 0), (x * tile_size, h)], fill=(255, 255, 255, 15), width=1)
    for y in range(0, 69):
        draw.line([(0, y * tile_size), (w, y * tile_size)], fill=(255, 255, 255, 15), width=1)

    # Draw civilization start markers
    for (x, y), civ in CIVS_INFO.items():
        sx = x * tile_size + tile_size // 2
        sy = (67 - y) * tile_size + tile_size // 2

        # Draw pulsing outer ring
        is_tw = "台灣" in civ["name"]
        radius = 16 if is_tw else 11
        ring_color = (255, 220, 0) if is_tw else (255, 255, 255)

        draw.ellipse([sx - radius, sy - radius, sx + radius, sy + radius], fill=civ["color"], outline=ring_color, width=3 if is_tw else 2)

        # Draw label box
        label_text = civ["name"]
        bbox = font_badge.getbbox(label_text)
        tw = bbox[2] - bbox[0]
        th = bbox[3] - bbox[1]

        # Offset label depending on position to avoid edge clipping
        lx = sx - tw // 2
        ly = sy - radius - th - 8
        if ly < 10:
            ly = sy + radius + 4
        if lx < 10:
            lx = 10
        if lx + tw + 10 > w:
            lx = w - tw - 12

        box_padding = 4
        box_bg = (10, 20, 40, 230) if not is_tw else (180, 20, 30, 240)
        box_border = (255, 220, 0) if is_tw else (200, 220, 255)
        draw.rounded_rectangle([lx - box_padding, ly - box_padding, lx + tw + box_padding, ly + th + box_padding], radius=4, fill=box_bg, outline=box_border, width=2 if is_tw else 1)
        draw.text((lx, ly), label_text, font=font_badge, fill=(255, 255, 255))

    # Add Map Title Box
    title_text = "文明帝國 IV：超越刀鋒 —「The Earth」巨型地球地圖 (124x68，18大文明歷史發祥位址)"
    sub_title = "★ 台灣文明：澳洲大陸 (118, 16) | 維京文明：北歐斯堪地那維亞 (62, 58) | 18大文明歷史發祥位址"
    draw.rounded_rectangle([20, 15, 880, 75], radius=6, fill=(10, 15, 25), outline=(255, 215, 0), width=2)
    draw.text((32, 22), title_text, font=font_title, fill=(255, 215, 0))
    draw.text((32, 50), sub_title, font=font_badge, fill=(200, 235, 255))

    img.save(PREVIEW_FULL_PNG)
    print(f"Saved full preview to: {PREVIEW_FULL_PNG}")
    return img

def render_australia_map(plots):
    print("Rendering high-res Australia & Taiwan civilization zoom-in...")
    # Australia subgrid: x: 104..123, y: 7..24
    min_x, max_x = 104, 123
    min_y, max_y = 7, 24
    tile_size = 52

    grid_w = max_x - min_x + 1
    grid_h = max_y - min_y + 1
    w = grid_w * tile_size
    h = grid_h * tile_size

    img = Image.new("RGB", (w, h), (15, 45, 89))
    draw = ImageDraw.Draw(img)

    try:
        font_lg = ImageFont.truetype(FONT_PATH, 20)
        font_md = ImageFont.truetype(FONT_PATH, 14)
        font_res = ImageFont.truetype(FONT_PATH, 12)
    except:
        font_lg = font_md = font_res = ImageFont.load_default()

    for x in range(min_x, max_x + 1):
        for y in range(min_y, max_y + 1):
            p = plots.get((x, y))
            if not p: continue
            sx = (x - min_x) * tile_size
            sy = (max_y - y) * tile_size

            color = TERRAIN_COLORS.get(p["terrain"], (15, 45, 89))
            draw.rectangle([sx, sy, sx + tile_size - 1, sy + tile_size - 1], fill=color, outline=(255, 255, 255, 30))

            # Peak / Hill
            if p["plot_type"] == 0:
                draw.polygon([
                    (sx + tile_size // 2, sy + 4),
                    (sx + 4, sy + tile_size - 4),
                    (sx + tile_size - 4, sy + tile_size - 4)
                ], fill=(55, 50, 45), outline=(230, 230, 230), width=2)
            elif p["plot_type"] == 1:
                draw.arc([sx + 6, sy + 8, sx + tile_size - 6, sy + tile_size + 4], start=180, end=360, fill=(45, 40, 35), width=3)

            # Features
            if p["feature"] in FEATURE_COLORS:
                fc = FEATURE_COLORS[p["feature"]]
                if p["feature"] in ["FEATURE_FOREST", "FEATURE_JUNGLE"]:
                    draw.ellipse([sx + 8, sy + 8, sx + tile_size - 8, sy + tile_size - 8], fill=fc)

            # Rivers
            if p["river_n"]:
                draw.line([(sx, sy + tile_size), (sx + tile_size, sy + tile_size)], fill=RIVER_COLOR, width=5)
            if p["river_w"]:
                draw.line([(sx + tile_size, sy), (sx + tile_size, sy + tile_size)], fill=RIVER_COLOR, width=5)

            # Coordinate text (faint)
            draw.text((sx + 3, sy + 2), f"{x},{y}", font=font_res, fill=(255, 255, 255, 120))

            # Resources
            if p["bonus"] in RESOURCE_LABELS:
                zh_name, en_name, r_color = RESOURCE_LABELS[p["bonus"]]
                # Draw resource badge
                rx = sx + tile_size // 2
                ry = sy + tile_size // 2 + 4
                badge_w = 44
                draw.rounded_rectangle([rx - badge_w//2, ry - 9, rx + badge_w//2, ry + 11], radius=3, fill=(15, 25, 35, 220), outline=r_color, width=2)
                draw.text((rx - 18, ry - 8), zh_name, font=font_res, fill=r_color)

    # Highlight Taiwan Capital at (118, 16)
    tw_x = (118 - min_x) * tile_size + tile_size // 2
    tw_y = (max_y - 16) * tile_size + tile_size // 2

    # Capital ring
    draw.ellipse([tw_x - 32, tw_y - 32, tw_x + 32, tw_y + 32], fill=(210, 30, 30, 180), outline=(255, 215, 0), width=4)
    draw.text((tw_x - 24, tw_y - 12), "★ 臺北", font=font_md, fill=(255, 255, 255))

    # Banner placed in the open ocean area to the right, pointing to the capital
    banner_text = "★ 台灣首都（雪梨流域 118, 16）"
    bx1 = tw_x + 65
    by1 = tw_y - 18
    bx2 = bx1 + 250
    by2 = by1 + 36
    draw.line([(tw_x + 32, tw_y), (bx1, by1 + 18)], fill=(255, 215, 0), width=2)
    draw.rounded_rectangle([bx1, by1, bx2, by2], radius=5, fill=(180, 20, 30), outline=(255, 215, 0), width=2)
    draw.text((bx1 + 10, by1 + 8), banner_text, font=font_md, fill=(255, 255, 255))

    # Legend / Title Box
    title_box_w = 460
    draw.rounded_rectangle([20, 20, 20 + title_box_w, 140], radius=6, fill=(10, 15, 25, 240), outline=(255, 215, 0), width=2)
    draw.text((32, 28), "澳洲大陸地理物產與台灣文明開局特寫", font=font_lg, fill=(255, 215, 0))
    draw.text((32, 60), "• 預設領袖：蔡英文（保國＋理財＋魅力超群）", font=font_md, fill=(255, 255, 255))
    draw.text((32, 84), "• 首都雙漁產：雪梨深海魚 (119,16) ＋ 雪梨生蠔 (119,17)", font=font_md, fill=(100, 220, 255))
    draw.text((32, 108), "• 內陸物產：小麥、乳牛、美麗諾綿羊、大分水嶺煤/銀/金礦", font=font_md, fill=(255, 210, 120))

    img.save(PREVIEW_AUS_PNG)
    print(f"Saved Australia preview to: {PREVIEW_AUS_PNG}")
    return img

def render_scandinavia_map(plots):
    print("Rendering high-res Northern Europe & Viking civilization zoom-in...")
    # Northern Europe & Scandinavia subgrid: x: 52..74, y: 48..64
    min_x, max_x = 52, 74
    min_y, max_y = 48, 64
    tile_size = 52

    grid_w = max_x - min_x + 1
    grid_h = max_y - min_y + 1
    w = grid_w * tile_size
    h = grid_h * tile_size

    img = Image.new("RGB", (w, h), (15, 45, 89))
    draw = ImageDraw.Draw(img)

    try:
        font_lg = ImageFont.truetype(FONT_PATH, 20)
        font_md = ImageFont.truetype(FONT_PATH, 14)
        font_res = ImageFont.truetype(FONT_PATH, 12)
    except:
        font_lg = font_md = font_res = ImageFont.load_default()

    for x in range(min_x, max_x + 1):
        for y in range(min_y, max_y + 1):
            p = plots.get((x, y))
            if not p: continue
            sx = (x - min_x) * tile_size
            sy = (max_y - y) * tile_size

            color = TERRAIN_COLORS.get(p["terrain"], (15, 45, 89))
            draw.rectangle([sx, sy, sx + tile_size - 1, sy + tile_size - 1], fill=color, outline=(255, 255, 255, 30))

            # Peak / Hill
            if p["plot_type"] == 0:
                draw.polygon([
                    (sx + tile_size // 2, sy + 4),
                    (sx + 4, sy + tile_size - 4),
                    (sx + tile_size - 4, sy + tile_size - 4)
                ], fill=(55, 50, 45), outline=(230, 230, 230), width=2)
            elif p["plot_type"] == 1:
                draw.arc([sx + 6, sy + 8, sx + tile_size - 6, sy + tile_size + 4], start=180, end=360, fill=(45, 40, 35), width=3)

            # Features
            if p["feature"] in FEATURE_COLORS:
                fc = FEATURE_COLORS[p["feature"]]
                if p["feature"] in ["FEATURE_FOREST", "FEATURE_JUNGLE"]:
                    draw.ellipse([sx + 8, sy + 8, sx + tile_size - 8, sy + tile_size - 8], fill=fc)

            # Rivers
            if p["river_n"]:
                draw.line([(sx, sy + tile_size), (sx + tile_size, sy + tile_size)], fill=RIVER_COLOR, width=5)
            if p["river_w"]:
                draw.line([(sx + tile_size, sy), (sx + tile_size, sy + tile_size)], fill=RIVER_COLOR, width=5)

            # Coordinate text (faint)
            draw.text((sx + 3, sy + 2), f"{x},{y}", font=font_res, fill=(255, 255, 255, 100))

            # Bonus Resource
            if p["bonus"] in RESOURCE_LABELS:
                zh_name, en_name, b_col = RESOURCE_LABELS[p["bonus"]]
                cx, cy = sx + tile_size // 2, sy + tile_size // 2 + 4
                r = 13
                draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=b_col, outline=(20, 20, 20), width=2)
                draw.text((cx - 10, cy - 7), zh_name[:2], font=font_res, fill=(10, 10, 10))

    # Mark Civilizations in this viewport
    vk_x, vk_y = 0, 0
    for (cx, cy), c_data in CIVS_INFO.items():
        if min_x <= cx <= max_x and min_y <= cy <= max_y:
            px = (cx - min_x) * tile_size + tile_size // 2
            py = (max_y - cy) * tile_size + tile_size // 2
            is_vk = (cx == 62 and cy == 58)
            if is_vk:
                vk_x, vk_y = px, py

            # Star badge
            star_r = 18 if is_vk else 14
            star_fill = (255, 215, 0) if is_vk else c_data["color"]
            star_outline = (180, 20, 30) if is_vk else (255, 255, 255)
            draw.ellipse([px - star_r, py - star_r, px + star_r, py + star_r], fill=star_fill, outline=star_outline, width=3 if is_vk else 2)
            sym = c_data["symbol"]
            draw.text((px - 8, py - 8), sym, font=font_md, fill=(0, 0, 0) if is_vk else (255, 255, 255))

            # Civ Label
            c_label = c_data["name"]
            tw = len(c_label) * 12
            draw.rounded_rectangle([px - tw // 2 - 4, py + 16, px + tw // 2 + 4, py + 34], radius=3, fill=(10, 20, 35, 230), outline=star_outline, width=1)
            draw.text((px - tw // 2, py + 18), c_label, font=font_res, fill=(255, 255, 255))

    # Viking Banner pointing to capital
    if vk_x and vk_y:
        banner_text = "★ 維京首都（斯堪地那維亞 62, 58）"
        bx1 = vk_x + 60
        by1 = vk_y - 30
        bx2 = bx1 + 270
        by2 = by1 + 36
        draw.line([(vk_x + 18, vk_y), (bx1, by1 + 18)], fill=(255, 215, 0), width=2)
        draw.rounded_rectangle([bx1, by1, bx2, by2], radius=5, fill=(110, 30, 160), outline=(255, 215, 0), width=2)
        draw.text((bx1 + 10, by1 + 8), banner_text, font=font_md, fill=(255, 255, 255))

    # Legend / Title Box
    title_box_w = 510
    draw.rounded_rectangle([20, 20, 20 + title_box_w, 140], radius=6, fill=(10, 15, 25, 240), outline=(255, 215, 0), width=2)
    draw.text((32, 28), "北歐斯堪地那維亞與維京文明開局特寫", font=font_lg, fill=(255, 215, 0))
    draw.text((32, 60), "• 領袖：朗納爾（理財＋侵略，海上經濟與陸戰雙神級特質）", font=font_md, fill=(255, 255, 255))
    draw.text((32, 84), "• 首都水陸資源：斯卡格拉克峽灣深海魚 (62,57) ＋ 淡水運河 (62,58)", font=font_md, fill=(100, 220, 255))
    draw.text((32, 108), "• 斯堪地那維亞物產：法倫銅礦 (60,58)、薩拉銀礦、野鹿、毛皮、生豬", font=font_md, fill=(255, 210, 120))

    img.save(PREVIEW_SCAN_PNG)
    print(f"Saved Scandinavia preview to: {PREVIEW_SCAN_PNG}")
    return img

def generate_interactive_html(plots):
    print("Generating interactive web inspector HTML...")
    # Export plots to compact JSON for Canvas rendering
    json_plots = []
    for (x, y), p in plots.items():
        civ = CIVS_INFO.get((x, y))
        civ_name = civ["name"] if civ else None
        res_info = RESOURCE_LABELS.get(p["bonus"])
        res_name = f"{res_info[0]} ({res_info[1]})" if res_info else None
        json_plots.append([
            x, y, p["plot_type"], p["terrain"],
            p["feature"], res_name,
            1 if p["river_n"] else 0,
            1 if p["river_w"] else 0,
            civ_name
        ])

    html_content = f'''<!DOCTYPE html>
<html lang="zh-TW">
<head>
<meta charset="UTF-8">
<title>文明帝國 IV：The Earth 巨型地球地圖檢視器</title>
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{ background: #0c121e; color: #e6edfa; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Microsoft JhengHei", sans-serif; overflow: hidden; }}
  #header {{ height: 56px; background: #131c2d; border-bottom: 1px solid #243550; display: flex; align-items: center; justify-content: space-between; padding: 0 20px; }}
  #header h1 {{ font-size: 18px; color: #ffd700; font-weight: 600; display: flex; align-items: center; gap: 8px; }}
  .badge {{ background: #1f304d; color: #8bb5f8; font-size: 12px; padding: 3px 8px; border-radius: 4px; border: 1px solid #334e77; }}
  #toolbar {{ display: flex; align-items: center; gap: 10px; }}
  button {{ background: #1e2c44; color: #f0f4fc; border: 1px solid #364e75; padding: 6px 14px; border-radius: 4px; cursor: pointer; font-size: 13px; transition: all 0.15s; }}
  button:hover {{ background: #2b3e60; border-color: #5375ad; color: #fff; }}
  button.active {{ background: #1952a8; border-color: #3b82f6; }}
  #container {{ position: relative; width: 100vw; height: calc(100vh - 56px); cursor: grab; background: #070c14; }}
  #container:active {{ cursor: grabbing; }}
  canvas {{ display: block; }}
  #tooltip {{ position: absolute; pointer-events: none; background: rgba(12, 19, 32, 0.95); border: 1px solid #3b82f6; border-radius: 6px; padding: 10px 14px; font-size: 12px; line-height: 1.6; color: #e6edfa; box-shadow: 0 8px 24px rgba(0,0,0,0.6); display: none; z-index: 100; min-width: 200px; }}
  #tooltip .title {{ font-weight: 600; color: #ffd700; font-size: 14px; margin-bottom: 4px; border-bottom: 1px solid #253650; padding-bottom: 2px; }}
  #sidebar {{ position: absolute; top: 15px; right: 15px; width: 280px; background: rgba(15, 23, 38, 0.92); border: 1px solid #2b3d5d; border-radius: 8px; padding: 15px; font-size: 13px; max-height: calc(100vh - 90px); overflow-y: auto; backdrop-filter: blur(8px); }}
  #sidebar h3 {{ color: #ffd700; font-size: 14px; margin-bottom: 10px; border-bottom: 1px solid #2b3d5d; padding-bottom: 4px; }}
  .civ-btn {{ display: flex; align-items: center; justify-content: space-between; width: 100%; text-align: left; padding: 6px 8px; margin-bottom: 4px; font-size: 12px; border-radius: 4px; border: 1px solid transparent; background: #162338; color: #d0deee; }}
  .civ-btn:hover {{ background: #223554; border-color: #3b82f6; color: #fff; }}
  .civ-btn.tw {{ background: rgba(220, 38, 38, 0.2); border-color: #dc2626; color: #fca5a5; font-weight: 600; }}
  .civ-btn.tw:hover {{ background: rgba(220, 38, 38, 0.35); }}
  .legend-item {{ display: flex; align-items: center; gap: 8px; margin-bottom: 4px; font-size: 11px; }}
  .legend-color {{ width: 14px; height: 14px; border-radius: 2px; }}
</style>
</head>
<body>
<div id="header">
  <h1>🌍 文明帝國 IV：超越刀鋒 —「The Earth」地圖檢視器 <span class="badge">124 × 68 Huge</span></h1>
  <div id="toolbar">
    <button id="btnZoomIn">放大 (+)</button>
    <button id="btnZoomOut">縮小 (-)</button>
    <button id="btnReset">重置視圖</button>
    <button id="btnToggleGrid" class="active">網格開關</button>
    <button id="btnToggleCivs" class="active">文明標記</button>
  </div>
</div>
<div id="container">
  <canvas id="mapCanvas"></canvas>
  <div id="tooltip"></div>
  <div id="sidebar">
    <h3>📍 18 大文明快速導航</h3>
    <button class="civ-btn tw" onclick="panTo(118, 16)">🇹🇼 台灣 (蔡英文 - 澳洲雪梨) <span>(118, 16)</span></button>
    <button class="civ-btn" onclick="panTo(102, 47)">🇨🇳 中國 (秦始皇) <span>(102, 47)</span></button>
    <button class="civ-btn" onclick="panTo(113, 45)">🇯🇵 日本 (德川家康) <span>(113, 45)</span></button>
    <button class="civ-btn" onclick="panTo(90, 40)">🇮🇳 印度 (阿育王) <span>(90, 40)</span></button>
    <button class="civ-btn" onclick="panTo(69, 37)">🇪🇬 埃及 (哈特謝普蘇特) <span>(69, 37)</span></button>
    <button class="civ-btn" onclick="panTo(61, 46)">🏛️ 羅馬 (凱撒) <span>(61, 46)</span></button>
    <button class="civ-btn" onclick="panTo(62, 52)">🇩🇪 德國 (腓特烈) <span>(62, 52)</span></button>
    <button class="civ-btn" onclick="panTo(58, 51)">🇫🇷 法國 (路易十四) <span>(58, 51)</span></button>
    <button class="civ-btn" onclick="panTo(56, 53)">🇬🇧 英國 (伊莉莎白) <span>(56, 53)</span></button>
    <button class="civ-btn" onclick="panTo(55, 46)">🇪🇸 西班牙 (伊莎貝拉) <span>(55, 46)</span></button>
    <button class="civ-btn" onclick="panTo(73, 54)">🇷🇺 俄羅斯 (凱薩琳) <span>(73, 54)</span></button>
    <button class="civ-btn" onclick="panTo(82, 40)">🇮🇷 波斯 (居魯士) <span>(82, 40)</span></button>
    <button class="civ-btn" onclick="panTo(75, 35)">🇸🇦 阿拉伯 (薩拉丁) <span>(75, 35)</span></button>
    <button class="civ-btn" onclick="panTo(99, 51)">🇲🇳 蒙古 (成吉思汗) <span>(99, 51)</span></button>
    <button class="civ-btn" onclick="panTo(55, 34)">🇲🇱 馬利 (曼薩·穆薩) <span>(55, 34)</span></button>
    <button class="civ-btn" onclick="panTo(28, 45)">🇺🇸 美國 (羅斯福) <span>(28, 45)</span></button>
    <button class="civ-btn" onclick="panTo(19, 37)">🇲🇽 阿茲特克 (蒙特祖瑪) <span>(19, 37)</span></button>
    <button class="civ-btn" onclick="panTo(30, 23)">🇵🇪 印加 (瓦伊納·卡帕克) <span>(30, 23)</span></button>

    <h3 style="margin-top: 15px;">🎨 地形圖例</h3>
    <div class="legend-item"><div class="legend-color" style="background:#4a7c36;"></div> 平原草地 (Grassland)</div>
    <div class="legend-item"><div class="legend-color" style="background:#8a844a;"></div> 旱地草原 (Plains)</div>
    <div class="legend-item"><div class="legend-color" style="background:#d4b76e;"></div> 沙漠 (Desert)</div>
    <div class="legend-item"><div class="legend-color" style="background:#6c7866;"></div> 苔原 (Tundra)</div>
    <div class="legend-item"><div class="legend-color" style="background:#e6edf0;"></div> 冰雪 (Snow/Ice)</div>
    <div class="legend-item"><div class="legend-color" style="background:#1f5982;"></div> 近海 (Coast)</div>
    <div class="legend-item"><div class="legend-color" style="background:#0f2d59;"></div> 深海 (Ocean)</div>
  </div>
</div>

<script>
const RAW_PLOTS = {json.dumps(json_plots)};
const TERRAIN_MAP = {{
  "TERRAIN_OCEAN": "#0f2d59",
  "TERRAIN_COAST": "#1f5982",
  "TERRAIN_GRASS": "#4a7c36",
  "TERRAIN_PLAINS": "#8a844a",
  "TERRAIN_DESERT": "#d4b76e",
  "TERRAIN_TUNDRA": "#6c7866",
  "TERRAIN_SNOW": "#e6edf0"
}};
const FEATURE_MAP = {{
  "FEATURE_FOREST": "#234a1a",
  "FEATURE_JUNGLE": "#164016",
  "FEATURE_FLOOD_PLAINS": "#529938",
  "FEATURE_OASIS": "#2b9980",
  "FEATURE_ICE": "#cee3eb"
}};

const canvas = document.getElementById("mapCanvas");
const ctx = canvas.getContext("2d");
const container = document.getElementById("container");
const tooltip = document.getElementById("tooltip");

let mapW = 124, mapH = 68;
let scale = 16;
let offsetX = 0, offsetY = 0;
let isDragging = false, startX, startY;
let showGrid = true, showCivs = true;

const plotGrid = Array.from({{length: mapW}}, () => new Array(mapH));
RAW_PLOTS.forEach(p => {{
  plotGrid[p[0]][p[1]] = {{
    x: p[0], y: p[1], pt: p[2], tt: p[3], ft: p[4], res: p[5],
    rn: p[6], rw: p[7], civ: p[8]
  }};
}});

function resize() {{
  canvas.width = container.clientWidth;
  canvas.height = container.clientHeight;
  draw();
}}
window.addEventListener("resize", resize);

function resetView() {{
  scale = Math.min(canvas.width / (mapW * 1.05), canvas.height / (mapH * 1.05));
  offsetX = (canvas.width - mapW * scale) / 2;
  offsetY = (canvas.height - mapH * scale) / 2;
  draw();
}}

function panTo(x, y) {{
  scale = 28;
  offsetX = canvas.width / 2 - x * scale;
  offsetY = canvas.height / 2 - (67 - y) * scale;
  draw();
}}

function draw() {{
  ctx.fillStyle = "#070c14";
  ctx.fillRect(0, 0, canvas.width, canvas.height);

  for (let x = 0; x < mapW; x++) {{
    for (let y = 0; y < mapH; y++) {{
      const p = plotGrid[x][y];
      const sx = offsetX + x * scale;
      const sy = offsetY + (67 - y) * scale;

      if (sx + scale < 0 || sx > canvas.width || sy + scale < 0 || sy > canvas.height) continue;

      ctx.fillStyle = TERRAIN_MAP[p.tt] || "#112233";
      ctx.fillRect(sx, sy, scale, scale);

      // Peak / Hill
      if (p.pt === 0) {{
        ctx.fillStyle = "#3d3731";
        ctx.beginPath();
        ctx.moveTo(sx + scale/2, sy + 1);
        ctx.lineTo(sx + 1, sy + scale - 1);
        ctx.lineTo(sx + scale - 1, sy + scale - 1);
        ctx.closePath();
        ctx.fill();
      }} else if (p.pt === 1) {{
        ctx.strokeStyle = "#38322c";
        ctx.lineWidth = Math.max(1, scale * 0.1);
        ctx.beginPath();
        ctx.arc(sx + scale/2, sy + scale * 0.7, scale * 0.35, Math.PI, 0);
        ctx.stroke();
      }}

      // Features
      if (p.ft && FEATURE_MAP[p.ft]) {{
        ctx.fillStyle = FEATURE_MAP[p.ft];
        if (p.ft === "FEATURE_FOREST" || p.ft === "FEATURE_JUNGLE") {{
          ctx.beginPath();
          ctx.arc(sx + scale/2, sy + scale/2, scale * 0.35, 0, Math.PI * 2);
          ctx.fill();
        }}
      }}

      // Rivers
      if (p.rn) {{
        ctx.strokeStyle = "#48b5f2";
        ctx.lineWidth = Math.max(2, scale * 0.12);
        ctx.beginPath();
        ctx.moveTo(sx, sy + scale);
        ctx.lineTo(sx + scale, sy + scale);
        ctx.stroke();
      }}
      if (p.rw) {{
        ctx.strokeStyle = "#48b5f2";
        ctx.lineWidth = Math.max(2, scale * 0.12);
        ctx.beginPath();
        ctx.moveTo(sx + scale, sy);
        ctx.lineTo(sx + scale, sy + scale);
        ctx.stroke();
      }}

      // Resources
      if (p.res && scale >= 14) {{
        ctx.fillStyle = "#ffd700";
        ctx.beginPath();
        ctx.arc(sx + scale/2, sy + scale/2, Math.max(2, scale * 0.15), 0, Math.PI * 2);
        ctx.fill();
      }}

      // Grid
      if (showGrid && scale >= 12) {{
        ctx.strokeStyle = "rgba(255,255,255,0.08)";
        ctx.lineWidth = 1;
        ctx.strokeRect(sx, sy, scale, scale);
      }}

      // Civilizations
      if (showCivs && p.civ) {{
        const isTW = p.civ.includes("台灣");
        ctx.fillStyle = isTW ? "#ef4444" : "#3b82f6";
        ctx.strokeStyle = isTW ? "#ffd700" : "#ffffff";
        ctx.lineWidth = isTW ? 3 : 2;
        ctx.beginPath();
        ctx.arc(sx + scale/2, sy + scale/2, Math.max(5, scale * 0.4), 0, Math.PI * 2);
        ctx.fill();
        ctx.stroke();

        if (scale >= 12 || isTW) {{
          ctx.font = isTW ? "bold 13px sans-serif" : "11px sans-serif";
          ctx.fillStyle = isTW ? "#ffd700" : "#ffffff";
          ctx.textAlign = "center";
          ctx.fillText(p.civ.split(" ")[0], sx + scale/2, sy - 6);
        }}
      }}
    }}
  }}
}}

container.addEventListener("mousedown", e => {{
  isDragging = true;
  startX = e.clientX - offsetX;
  startY = e.clientY - offsetY;
}});

window.addEventListener("mouseup", () => isDragging = false);

container.addEventListener("mousemove", e => {{
  if (isDragging) {{
    offsetX = e.clientX - startX;
    offsetY = e.clientY - startY;
    draw();
  }}

  const rect = canvas.getBoundingClientRect();
  const mx = e.clientX - rect.left - offsetX;
  const my = e.clientY - rect.top - offsetY;
  const gx = Math.floor(mx / scale);
  const gy = 67 - Math.floor(my / scale);

  if (gx >= 0 && gx < mapW && gy >= 0 && gy < mapH) {{
    const p = plotGrid[gx][gy];
    let html = `<div class="title">${{p.civ ? '👑 ' + p.civ : '地塊座標 (' + gx + ', ' + gy + ')'}}</div>`;
    html += `<div>• 地形：${{p.tt.replace('TERRAIN_', '')}} (${{p.pt === 0 ? '山脈 Peak' : p.pt === 1 ? '丘陵 Hill' : '平地 Flat'}})</div>`;
    if (p.ft) html += `<div>• 地貌：${{p.ft.replace('FEATURE_', '')}}</div>`;
    if (p.res) html += `<div style="color:#ffd700;">• 特產資源：<strong>${{p.res}}</strong></div>`;
    if (p.rn || p.rw) html += `<div style="color:#38bdf8;">• 鄰近河川：淡水補給加成</div>`;
    tooltip.innerHTML = html;
    tooltip.style.left = (e.clientX + 15) + "px";
    tooltip.style.top = (e.clientY + 15) + "px";
    tooltip.style.display = "block";
  }} else {{
    tooltip.style.display = "none";
  }}
}});

container.addEventListener("wheel", e => {{
  e.preventDefault();
  const zoomFactor = e.deltaY < 0 ? 1.2 : 0.83;
  const mouseX = e.clientX - canvas.getBoundingClientRect().left;
  const mouseY = e.clientY - canvas.getBoundingClientRect().top;
  const nextScale = Math.max(6, Math.min(60, scale * zoomFactor));

  offsetX = mouseX - (mouseX - offsetX) * (nextScale / scale);
  offsetY = mouseY - (mouseY - offsetY) * (nextScale / scale);
  scale = nextScale;
  draw();
}});

document.getElementById("btnZoomIn").onclick = () => {{ scale = Math.min(60, scale * 1.3); draw(); }};
document.getElementById("btnZoomOut").onclick = () => {{ scale = Math.max(6, scale * 0.7); draw(); }};
document.getElementById("btnReset").onclick = resetView;
document.getElementById("btnToggleGrid").onclick = function() {{ showGrid = !showGrid; this.classList.toggle("active", showGrid); draw(); }};
document.getElementById("btnToggleCivs").onclick = function() {{ showCivs = !showCivs; this.classList.toggle("active", showCivs); draw(); }};

resize();
resetView();
</script>
</body>
</html>
'''

    with open(HTML_INSPECTOR, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"Saved interactive HTML to: {HTML_INSPECTOR}")

if __name__ == "__main__":
    plots = parse_wbsave()
    render_full_map(plots)
    render_australia_map(plots)
    render_scandinavia_map(plots)
    generate_interactive_html(plots)
