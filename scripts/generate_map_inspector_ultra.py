import os
import re
import json
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WBSAVE_PATH = os.path.join(ROOT, "patch", "PatchFiles", "Beyond the Sword", "PublicMaps", "The Earth Ultra (180x90).CivBeyondSwordWBSave")

HTML_INSPECTOR = os.path.join(ROOT, "inspect_the_earth_ultra.html")
PREVIEW_TAIWAN_PNG = os.path.join(ROOT, "the_earth_ultra_taiwan_preview.png")

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
    (154, 45): {"name": "台灣 (蔡英文 - 台北首都)", "en": "Taiwan (Taipei)", "color": (30, 100, 240), "symbol": "TW"},
    (148, 62): {"name": "中國 (秦始皇 - 長安洛陽)", "en": "China (Qin)", "color": (220, 30, 30), "symbol": "CN"},
    (164, 60): {"name": "日本 (德川家康 - 京都東京)", "en": "Japan (Tokugawa)", "color": (200, 20, 50), "symbol": "JP"},
    (131, 53): {"name": "印度 (阿育王 - 德里)", "en": "India (Asoka)", "color": (240, 140, 20), "symbol": "IN"},
    (100, 49): {"name": "埃及 (哈特謝普蘇特 - 尼羅河)", "en": "Egypt (Hatshepsut)", "color": (230, 190, 20), "symbol": "EG"},
    (89, 61):  {"name": "羅馬 (凱撒 - 羅馬城)", "en": "Rome (Caesar)", "color": (140, 20, 130), "symbol": "RO"},
    (93, 69):  {"name": "德國 (俾斯麥 - 柏林)", "en": "Germany (Bismarck)", "color": (60, 60, 60), "symbol": "DE"},
    (84, 68):  {"name": "法國 (路易十四 - 巴黎)", "en": "France (Louis XIV)", "color": (30, 70, 190), "symbol": "FR"},
    (81, 70):  {"name": "英國 (伊莉莎白 - 倫敦)", "en": "England (Elizabeth)", "color": (190, 20, 20), "symbol": "GB"},
    (90, 77):  {"name": "維京 (朗納爾 - 斯堪地那維亞)", "en": "Viking (Ragnar)", "color": (150, 60, 190), "symbol": "VK"},
    (106, 71): {"name": "俄羅斯 (凱薩琳 - 莫斯科)", "en": "Russia (Catherine)", "color": (170, 30, 30), "symbol": "RU"},
    (119, 53): {"name": "波斯 (居魯士 - 波斯波利斯)", "en": "Persia (Cyrus)", "color": (40, 150, 150), "symbol": "IR"},
    (109, 46): {"name": "阿拉伯 (薩拉丁 - 麥加)", "en": "Arabia (Saladin)", "color": (20, 150, 40), "symbol": "SA"},
    (144, 68): {"name": "蒙古 (成吉思汗 - 哈拉和林)", "en": "Mongol (Genghis)", "color": (200, 120, 30), "symbol": "MN"},
    (80, 45):  {"name": "馬利 (曼薩·穆薩 - 廷巴克圖)", "en": "Mali (Mansa Musa)", "color": (190, 80, 170), "symbol": "ML"},
    (41, 60):  {"name": "美國 (華盛頓 - 華府)", "en": "America (Washington)", "color": (20, 60, 180), "symbol": "US"},
    (28, 49):  {"name": "阿茲特克 (蒙特祖瑪 - 特諾奇蒂特蘭)", "en": "Aztec (Montezuma)", "color": (30, 160, 80), "symbol": "MX"},
    (44, 30):  {"name": "印加 (瓦伊納·卡帕克 - 庫斯科)", "en": "Inca (Huayna)", "color": (210, 170, 30), "symbol": "PE"},
}

RESOURCE_LABELS = {
    "BONUS_FISH": ("魚產", "Fish", (60, 160, 240)),
    "BONUS_CLAM": ("生蠔", "Clams", (120, 200, 230)),
    "BONUS_CRAB": ("螃蟹", "Crab", (240, 90, 60)),
    "BONUS_WHALE": ("抹香鯨", "Whale", (100, 140, 200)),
    "BONUS_WHEAT": ("小麥", "Wheat", (245, 210, 80)),
    "BONUS_CORN": ("玉米", "Corn", (240, 220, 50)),
    "BONUS_RICE": ("蓬萊米", "Rice", (210, 240, 120)),
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
    "BONUS_STONE": ("文石/石材", "Stone", (150, 150, 150)),
    "BONUS_INCENSE": ("焚香", "Incense", (220, 140, 100)),
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

        pt = [l for l in lines if l.startswith("PlotType=")][0].split("=")[1]
        tt = [l for l in lines if l.startswith("TerrainType=")][0].split("=")[1]
        b = [l.split("=")[1] for l in lines if l.startswith("BonusType=")]
        f = [l.split("=")[1].split(",")[0] for l in lines if l.startswith("FeatureType=")]
        rn = any("isNOfRiver" in l for l in lines)
        rw = any("isWOfRiver" in l for l in lines)
        sp = any("StartingPlot" in l for l in lines)

        plots[(x, y)] = {
            "pt": int(pt),
            "tt": tt,
            "ft": f[0] if f else None,
            "res": b[0] if b else None,
            "rn": rn,
            "rw": rw,
            "sp": sp
        }
    return plots

def render_taiwan_png(plots):
    print("Rendering high-res Taiwan preview PNG...")
    # Region around Taiwan: X in [148..160], Y in [38..48]
    min_x, max_x = 148, 160
    min_y, max_y = 38, 48
    w = max_x - min_x + 1
    h = max_y - min_y + 1
    tile_size = 72

    img = Image.new("RGB", (w * tile_size, h * tile_size), (10, 20, 40))
    draw = ImageDraw.Draw(img)

    try:
        font_large = ImageFont.truetype(FONT_PATH, 16)
        font_small = ImageFont.truetype(FONT_PATH, 12)
        font_bold = ImageFont.truetype(FONT_PATH, 18)
    except Exception:
        font_large = ImageFont.load_default()
        font_small = font_large
        font_bold = font_large

    for Y in range(min_y, max_y + 1):
        for X in range(min_x, max_x + 1):
            p = plots.get((X, Y))
            if not p: continue

            # Civ4 y=0 is south, image y=0 is top
            px = (X - min_x) * tile_size
            py = (max_y - Y) * tile_size

            # Base color
            base_col = TERRAIN_COLORS.get(p["tt"], (50, 50, 50))
            if p["pt"] == 0:  # Peak
                base_col = (180, 180, 190)
            elif p["pt"] == 1: # Hills
                base_col = (int(base_col[0] * 0.8), int(base_col[1] * 0.8), int(base_col[2] * 0.8))

            draw.rectangle([px, py, px + tile_size - 1, py + tile_size - 1], fill=base_col)

            # Feature overlay
            if p["ft"] in FEATURE_COLORS:
                fc = FEATURE_COLORS[p["ft"]]
                draw.rectangle([px + 4, py + 4, px + tile_size - 5, py + tile_size - 5], outline=fc, width=2)

            # Rivers
            if p["rn"]:
                draw.line([px, py, px + tile_size, py], fill=RIVER_COLOR, width=4)
            if p["rw"]:
                draw.line([px, py, px, py + tile_size], fill=RIVER_COLOR, width=4)

            # Grid border
            draw.rectangle([px, py, px + tile_size - 1, py + tile_size - 1], outline=(40, 60, 80), width=1)

            # Coordinates label
            draw.text((px + 4, py + 4), f"{X},{Y}", fill=(200, 200, 200, 160), font=font_small)

            # Starting plot marker
            if (X, Y) in CIVS_INFO:
                cinfo = CIVS_INFO[(X, Y)]
                draw.ellipse([px + 16, py + 16, px + tile_size - 16, py + tile_size - 16], fill=cinfo["color"], outline=(255, 255, 255), width=2)
                draw.text((px + 22, py + 24), cinfo["symbol"], fill=(255, 255, 255), font=font_bold)
                draw.text((px + 4, py + tile_size - 20), cinfo["name"].split(" ")[0], fill=(255, 255, 0), font=font_large)

            # Resource marker
            elif p["res"] and p["res"] in RESOURCE_LABELS:
                zh, en, col = RESOURCE_LABELS[p["res"]]
                draw.rounded_rectangle([px + 8, py + 26, px + tile_size - 8, py + tile_size - 8], radius=4, fill=col, outline=(255, 255, 255))
                draw.text((px + 12, py + 34), zh, fill=(0, 0, 0) if sum(col) > 400 else (255, 255, 255), font=font_large)

    img.save(PREVIEW_TAIWAN_PNG)
    print(f"Saved Taiwan preview to: {PREVIEW_TAIWAN_PNG}")

def generate_html(plots):
    print("Generating interactive HTML inspector for 180x90 Ultra Earth...")
    json_plots = []
    for (x, y), p in plots.items():
        civ_tag = None
        if (x, y) in CIVS_INFO:
            civ_tag = CIVS_INFO[(x, y)]["name"]
        json_plots.append([
            x, y, p["pt"], p["tt"], p["ft"], p["res"],
            1 if p["rn"] else 0, 1 if p["rw"] else 0, civ_tag
        ])

    html_content = f'''<!DOCTYPE html>
<html lang="zh-TW">
<head>
<meta charset="utf-8">
<title>The Earth Ultra (180x90) - 世界地圖全域與台灣特寫檢視器</title>
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Microsoft JhengHei", sans-serif;
    background: #090e17;
    color: #e0e6ed;
    overflow: hidden;
  }}
  #header {{
    height: 52px;
    background: #111a29;
    border-bottom: 1px solid #1f2f47;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 16px;
    z-index: 10;
    box-shadow: 0 2px 10px rgba(0,0,0,0.5);
  }}
  #header h1 {{
    font-size: 17px;
    font-weight: 700;
    color: #4da3ff;
    display: flex;
    align-items: center;
    gap: 8px;
  }}
  #header .badge {{
    font-size: 12px;
    padding: 2px 8px;
    border-radius: 4px;
    background: #1c3659;
    color: #8ac0ff;
    border: 1px solid #295085;
  }}
  #toolbar {{
    display: flex;
    align-items: center;
    gap: 8px;
  }}
  .tool-btn {{
    background: #18263a;
    border: 1px solid #273d5e;
    color: #d1deed;
    padding: 6px 12px;
    border-radius: 4px;
    font-size: 13px;
    cursor: pointer;
    transition: all 0.15s ease;
  }}
  .tool-btn:hover {{
    background: #253b5c;
    color: #fff;
    border-color: #4da3ff;
  }}
  .tool-btn.primary {{
    background: #0f62fe;
    border-color: #0f62fe;
    color: #fff;
    font-weight: 600;
  }}
  .tool-btn.primary:hover {{
    background: #0353e9;
  }}
  .tool-btn.active {{
    background: #1f4370;
    border-color: #4da3ff;
    color: #4da3ff;
  }}
  #container {{
    position: relative;
    width: 100vw;
    height: calc(100vh - 52px);
    display: flex;
  }}
  #mapCanvas {{
    flex: 1;
    height: 100%;
    cursor: grab;
    background: #050a12;
  }}
  #mapCanvas:active {{
    cursor: grabbing;
  }}
  #sidebar {{
    width: 320px;
    background: #111a29;
    border-left: 1px solid #1f2f47;
    height: 100%;
    overflow-y: auto;
    padding: 16px;
    font-size: 13px;
  }}
  #sidebar h3 {{
    font-size: 13px;
    text-transform: uppercase;
    color: #7b93b5;
    margin-bottom: 10px;
    letter-spacing: 0.5px;
  }}
  .civ-btn {{
    width: 100%;
    padding: 8px 10px;
    background: #162233;
    border: 1px solid #20324c;
    color: #d1deed;
    border-radius: 5px;
    text-align: left;
    margin-bottom: 6px;
    cursor: pointer;
    font-size: 13px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    transition: all 0.15s ease;
  }}
  .civ-btn:hover {{
    background: #20334e;
    border-color: #4da3ff;
    color: #fff;
    transform: translateX(2px);
  }}
  .civ-btn.tw {{
    background: #15325b;
    border-color: #3b7cd4;
    color: #9cd0ff;
    font-weight: 700;
    box-shadow: 0 0 10px rgba(59, 124, 212, 0.3);
  }}
  .civ-btn.tw:hover {{
    background: #1d467f;
    border-color: #63a4ff;
  }}
  .legend-item {{
    display: flex;
    align-items: center;
    gap: 8px;
    margin-bottom: 6px;
    color: #b0c2d8;
  }}
  .legend-color {{
    width: 14px;
    height: 14px;
    border-radius: 3px;
    border: 1px solid rgba(255,255,255,0.2);
  }}
  #tooltip {{
    position: absolute;
    display: none;
    background: rgba(14, 23, 38, 0.95);
    border: 1px solid #365077;
    border-radius: 6px;
    padding: 10px 14px;
    color: #e0e6ed;
    font-size: 13px;
    pointer-events: none;
    z-index: 100;
    box-shadow: 0 4px 20px rgba(0,0,0,0.6);
    line-height: 1.5;
  }}
  #tooltip .title {{
    font-weight: bold;
    color: #4da3ff;
    font-size: 14px;
    margin-bottom: 4px;
  }}
  #tooltip .res {{
    color: #ffd043;
    font-weight: bold;
  }}
</style>
</head>
<body>

<div id="header">
  <h1>
    <span>🌏 The Earth Ultra</span>
    <span class="badge">180 x 90 (16,200 Plots)</span>
  </h1>
  <div id="toolbar">
    <button class="tool-btn primary" onclick="focusTaiwan()">🇹🇼 聚焦台灣特寫 (Taiwan Close-Up)</button>
    <button class="tool-btn" onclick="focusEastAsia()">東亞 (East Asia)</button>
    <button class="tool-btn" onclick="focusEurope()">歐洲 (Europe)</button>
    <button class="tool-btn" onclick="focusAmericas()">美洲 (Americas)</button>
    <button class="tool-btn" onclick="resetView()">全圖總覽 (Full World)</button>
    <button class="tool-btn" id="toggleGrid" onclick="toggleOption('grid')">網格: 開</button>
    <button class="tool-btn" id="toggleRes" onclick="toggleOption('res')">資源名稱: 開</button>
    <button class="tool-btn" id="toggleRivers" onclick="toggleOption('rivers')">河流: 開</button>
  </div>
</div>

<div id="container">
  <canvas id="mapCanvas"></canvas>
  <div id="tooltip"></div>
  <div id="sidebar">
    <h3>🇹🇼 台灣專屬導航</h3>
    <button class="civ-btn tw" onclick="focusTaiwan()">🇹🇼 台灣 (台北首都發祥) <span>(154, 45)</span></button>

    <h3 style="margin-top: 15px;">📍 18 大文明起始點</h3>
    <button class="civ-btn" onclick="panTo(148, 62)">🇨🇳 中國 (秦始皇) <span>(148, 62)</span></button>
    <button class="civ-btn" onclick="panTo(164, 60)">🇯🇵 日本 (德川家康) <span>(164, 60)</span></button>
    <button class="civ-btn" onclick="panTo(131, 53)">🇮🇳 印度 (阿育王) <span>(131, 53)</span></button>
    <button class="civ-btn" onclick="panTo(100, 49)">🇪🇬 埃及 (哈特謝普蘇特) <span>(100, 49)</span></button>
    <button class="civ-btn" onclick="panTo(89, 61)">🏛️ 羅馬 (凱撒) <span>(89, 61)</span></button>
    <button class="civ-btn" onclick="panTo(93, 69)">🇩🇪 德國 (俾斯麥) <span>(93, 69)</span></button>
    <button class="civ-btn" onclick="panTo(84, 68)">🇫🇷 法國 (路易十四) <span>(84, 68)</span></button>
    <button class="civ-btn" onclick="panTo(81, 70)">🇬🇧 英國 (伊莉莎白) <span>(81, 70)</span></button>
    <button class="civ-btn" onclick="panTo(90, 77)">⚔️ 維京 (朗納爾) <span>(90, 77)</span></button>
    <button class="civ-btn" onclick="panTo(106, 71)">🇷🇺 俄羅斯 (凱薩琳) <span>(106, 71)</span></button>
    <button class="civ-btn" onclick="panTo(119, 53)">🇮🇷 波斯 (居魯士) <span>(119, 53)</span></button>
    <button class="civ-btn" onclick="panTo(109, 46)">🇸🇦 阿拉伯 (薩拉丁) <span>(109, 46)</span></button>
    <button class="civ-btn" onclick="panTo(144, 68)">🇲🇳 蒙古 (成吉思汗) <span>(144, 68)</span></button>
    <button class="civ-btn" onclick="panTo(80, 45)">🇲🇱 馬利 (曼薩·穆薩) <span>(80, 45)</span></button>
    <button class="civ-btn" onclick="panTo(41, 60)">🇺🇸 美國 (華盛頓) <span>(41, 60)</span></button>
    <button class="civ-btn" onclick="panTo(28, 49)">🇲🇽 阿茲特克 (蒙特祖瑪) <span>(28, 49)</span></button>
    <button class="civ-btn" onclick="panTo(44, 30)">🇵🇪 印加 (瓦伊納·卡帕克) <span>(44, 30)</span></button>

    <h3 style="margin-top: 15px;">🎨 地形圖例</h3>
    <div class="legend-item"><div class="legend-color" style="background:#4a7c36;"></div> 平原草地 (Grassland)</div>
    <div class="legend-item"><div class="legend-color" style="background:#8a844a;"></div> 旱地草原 (Plains)</div>
    <div class="legend-item"><div class="legend-color" style="background:#d4b76e;"></div> 沙漠 (Desert)</div>
    <div class="legend-item"><div class="legend-color" style="background:#6c7866;"></div> 苔原 (Tundra)</div>
    <div class="legend-item"><div class="legend-color" style="background:#e6edf0;"></div> 冰雪 (Snow/Ice)</div>
    <div class="legend-item"><div class="legend-color" style="background:#1f5982;"></div> 近海 (Coast)</div>
    <div class="legend-item"><div class="legend-color" style="background:#0f2d59;"></div> 深海 (Ocean)</div>
    <div class="legend-item"><div class="legend-color" style="background:#48b5f2;"></div> 河流網絡 (Rivers)</div>
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
const RES_LABELS = {json.dumps(RESOURCE_LABELS)};

const canvas = document.getElementById("mapCanvas");
const ctx = canvas.getContext("2d");
const container = document.getElementById("container");
const tooltip = document.getElementById("tooltip");

let mapW = 180, mapH = 90;
let scale = 14;
let offsetX = 0, offsetY = 0;
let isDragging = false, startX, startY;
let showGrid = true, showRes = true, showRivers = true;

const plotGrid = Array.from({{length: mapW}}, () => new Array(mapH));
RAW_PLOTS.forEach(p => {{
  plotGrid[p[0]][p[1]] = {{
    x: p[0], y: p[1], pt: p[2], tt: p[3], ft: p[4], res: p[5],
    rn: p[6], rw: p[7], civ: p[8]
  }};
}});

function resize() {{
  canvas.width = container.clientWidth - 320;
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

function panTo(x, y, customScale = 28) {{
  scale = customScale;
  offsetX = canvas.width / 2 - x * scale;
  offsetY = canvas.height / 2 - (mapH - 1 - y) * scale;
  draw();
}}

function focusTaiwan() {{
  panTo(154, 44, 48); // Large zoom onto Taiwan Island!
}}

function focusEastAsia() {{
  panTo(152, 55, 24);
}}

function focusEurope() {{
  panTo(88, 66, 26);
}}

function focusAmericas() {{
  panTo(36, 52, 20);
}}

function toggleOption(type) {{
  if (type === 'grid') {{
    showGrid = !showGrid;
    document.getElementById("toggleGrid").textContent = "網格: " + (showGrid ? "開" : "關");
  }} else if (type === 'res') {{
    showRes = !showRes;
    document.getElementById("toggleRes").textContent = "資源名稱: " + (showRes ? "開" : "關");
  }} else if (type === 'rivers') {{
    showRivers = !showRivers;
    document.getElementById("toggleRivers").textContent = "河流: " + (showRivers ? "開" : "關");
  }}
  draw();
}}

function draw() {{
  ctx.fillStyle = "#050a12";
  ctx.fillRect(0, 0, canvas.width, canvas.height);

  for (let x = 0; x < mapW; x++) {{
    for (let y = 0; y < mapH; y++) {{
      const p = plotGrid[x][y];
      const sx = offsetX + x * scale;
      const sy = offsetY + (mapH - 1 - y) * scale;

      if (sx + scale < 0 || sx > canvas.width || sy + scale < 0 || sy > canvas.height) continue;

      let color = TERRAIN_MAP[p.tt] || "#444";
      if (p.pt === 0) color = "#b8b8c4"; // Peak
      else if (p.pt === 1) {{
        // Hills: slightly darker
        color = adjustColor(color, -25);
      }}

      ctx.fillStyle = color;
      ctx.fillRect(sx, sy, scale, scale);

      // Feature
      if (p.ft && FEATURE_MAP[p.ft]) {{
        ctx.strokeStyle = FEATURE_MAP[p.ft];
        ctx.lineWidth = Math.max(1, scale * 0.12);
        ctx.strokeRect(sx + 2, sy + 2, scale - 4, scale - 4);
      }}

      // Rivers
      if (showRivers) {{
        ctx.strokeStyle = "#48b5f2";
        ctx.lineWidth = Math.max(2, scale * 0.15);
        if (p.rn) {{
          ctx.beginPath();
          ctx.moveTo(sx, sy);
          ctx.lineTo(sx + scale, sy);
          ctx.stroke();
        }}
        if (p.rw) {{
          ctx.beginPath();
          ctx.moveTo(sx, sy);
          ctx.lineTo(sx, sy + scale);
          ctx.stroke();
        }}
      }}

      // Grid
      if (showGrid && scale >= 8) {{
        ctx.strokeStyle = "rgba(255,255,255,0.06)";
        ctx.lineWidth = 1;
        ctx.strokeRect(sx, sy, scale, scale);
      }}

      // Civilization Starting Marker
      if (p.civ) {{
        ctx.fillStyle = p.civ.includes("台灣") ? "#0f62fe" : "#ff3b30";
        ctx.beginPath();
        ctx.arc(sx + scale/2, sy + scale/2, scale * 0.38, 0, Math.PI * 2);
        ctx.fill();
        ctx.strokeStyle = "#fff";
        ctx.lineWidth = Math.max(1.5, scale * 0.08);
        ctx.stroke();

        if (scale >= 18) {{
          ctx.fillStyle = "#fff";
          ctx.font = "bold " + Math.max(9, scale * 0.28) + "px sans-serif";
          ctx.textAlign = "center";
          ctx.textBaseline = "middle";
          ctx.fillText(p.civ.includes("台灣") ? "TW" : "★", sx + scale/2, sy + scale/2);
        }}
      }}

      // Resource label
      if (showRes && p.res && scale >= 14 && !p.civ) {{
        const rInfo = RES_LABELS[p.res];
        const label = rInfo ? rInfo[0] : p.res.replace("BONUS_", "");
        ctx.fillStyle = "rgba(0,0,0,0.65)";
        const fSize = Math.max(9, Math.min(13, scale * 0.28));
        ctx.font = fSize + "px sans-serif";
        ctx.textAlign = "center";
        ctx.textBaseline = "middle";
        ctx.fillText(label, sx + scale/2, sy + scale/2);
      }}
    }}
  }}
}}

function adjustColor(col, amt) {{
  let num = parseInt(col.replace("#", ""), 16);
  let r = Math.max(0, Math.min(255, (num >> 16) + amt));
  let g = Math.max(0, Math.min(255, ((num >> 8) & 0x00FF) + amt));
  let b = Math.max(0, Math.min(255, (num & 0x0000FF) + amt));
  return "#" + (g | (b << 8) | (r << 16)).toString(16).padStart(6, "0");
}}

// Mouse interactions
canvas.addEventListener("mousedown", e => {{
  isDragging = true;
  startX = e.clientX - offsetX;
  startY = e.clientY - offsetY;
}});

window.addEventListener("mouseup", () => {{ isDragging = false; }});

canvas.addEventListener("mousemove", e => {{
  if (isDragging) {{
    offsetX = e.clientX - startX;
    offsetY = e.clientY - startY;
    draw();
  }}

  // Tooltip
  const rect = canvas.getBoundingClientRect();
  const mx = e.clientX - rect.left;
  const my = e.clientY - rect.top;

  const gx = Math.floor((mx - offsetX) / scale);
  const gy = mapH - 1 - Math.floor((my - offsetY) / scale);

  if (gx >= 0 && gx < mapW && gy >= 0 && gy < mapH) {{
    const p = plotGrid[gx][gy];
    let html = `<div class="title">座標: (${{gx}}, ${{gy}})</div>`;
    const ptNames = ["山峰 (Peak)", "丘陵 (Hills)", "平原陸地 (Land)", "海洋水域 (Water)"];
    html += `<div>地形: ${{ptNames[p.pt]}} - ${{p.tt.replace("TERRAIN_", "")}}</div>`;
    if (p.ft) html += `<div>特徵: ${{p.ft.replace("FEATURE_", "")}}</div>`;
    if (p.rn || p.rw) html += `<div>河流: <span style="color:#4da3ff;">★ 天然淡水水源 (Fresh Water)</span></div>`;
    if (p.res) {{
      const rInfo = RES_LABELS[p.res];
      const rName = rInfo ? rInfo[0] : p.res;
      html += `<div class="res">資源: ${{rName}} (${{p.res}})</div>`;
    }}
    if (p.civ) html += `<div style="color:#60a5fa; font-weight:bold; margin-top:4px;">🏛️ 文明開局: ${{p.civ}}</div>`;

    tooltip.innerHTML = html;
    tooltip.style.left = (e.clientX + 14) + "px";
    tooltip.style.top = (e.clientY + 14) + "px";
    tooltip.style.display = "block";
  }} else {{
    tooltip.style.display = "none";
  }}
}});

canvas.addEventListener("mouseleave", () => {{
  tooltip.style.display = "none";
}});

canvas.addEventListener("wheel", e => {{
  e.preventDefault();
  const zoomFactor = e.deltaY < 0 ? 1.2 : 0.833;
  const rect = canvas.getBoundingClientRect();
  const mouseX = e.clientX - rect.left;
  const mouseY = e.clientY - rect.top;

  const newScale = Math.max(3, Math.min(80, scale * zoomFactor));
  offsetX = mouseX - (mouseX - offsetX) * (newScale / scale);
  offsetY = mouseY - (mouseY - offsetY) * (newScale / scale);
  scale = newScale;
  draw();
}}, {{ passive: false }});

// Initial Setup
resize();
resetView();
</script>
</body>
</html>
'''

    with open(HTML_INSPECTOR, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"Generated HTML inspector: {HTML_INSPECTOR}")

if __name__ == "__main__":
    plots = parse_wbsave()
    render_taiwan_png(plots)
    generate_html(plots)
    print("Map review assets successfully built!")
