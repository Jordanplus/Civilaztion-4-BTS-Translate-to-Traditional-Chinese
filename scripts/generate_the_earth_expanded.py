import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SOURCE_WBSAVE = os.path.join(ROOT, "patch", "PatchFiles", "Beyond the Sword", "PublicMaps", "The Earth.CivBeyondSwordWBSave")

OUTPUT_WBSAVE_PATCH = os.path.join(ROOT, "patch", "PatchFiles", "Beyond the Sword", "PublicMaps", "The Earth (Huge 50% Expanded).CivBeyondSwordWBSave")
OUTPUT_PY_PATCH = os.path.join(ROOT, "patch", "PatchFiles", "Beyond the Sword", "PublicMaps", "The_Earth_Huge.py")

STEAM_PATH = r"C:\Program Files (x86)\Steam\steamapps\common\Sid Meier's Civilization IV Beyond the Sword"
USER_MY_GAMES_MAPS = os.path.expanduser(r"~\OneDrive\文件\My Games\beyond the sword\PublicMaps")
STEAM_BTS_MAPS = os.path.join(STEAM_PATH, "Beyond the Sword", "PublicMaps")
STEAM_ROOT_MAPS = os.path.join(STEAM_PATH, "PublicMaps")

W_SRC, H_SRC = 124, 68
W_TGT, H_TGT = 158, 80

rx = float(W_SRC) / float(W_TGT)
ry = float(H_SRC) / float(H_TGT)

TERRAIN_LIST = [
    'TERRAIN_OCEAN', 'TERRAIN_COAST', 'TERRAIN_GRASS', 'TERRAIN_SNOW',
    'TERRAIN_PLAINS', 'TERRAIN_TUNDRA', 'TERRAIN_DESERT'
]

FEATURE_LIST = [
    None, 'FEATURE_ICE', 'FEATURE_JUNGLE', 'FEATURE_FOREST',
    'FEATURE_OASIS', 'FEATURE_FLOOD_PLAINS'
]

BONUS_LIST = [
    None, 'BONUS_FISH', 'BONUS_DEER', 'BONUS_CRAB', 'BONUS_GOLD',
    'BONUS_OIL', 'BONUS_CLAM', 'BONUS_COPPER', 'BONUS_SILVER',
    'BONUS_COAL', 'BONUS_STONE', 'BONUS_FUR', 'BONUS_URANIUM',
    'BONUS_DYE', 'BONUS_CORN', 'BONUS_MARBLE', 'BONUS_SPICES',
    'BONUS_ALUMINUM', 'BONUS_IRON', 'BONUS_WHALE', 'BONUS_GEMS',
    'BONUS_SHEEP', 'BONUS_IVORY', 'BONUS_WINE', 'BONUS_HORSE',
    'BONUS_COW', 'BONUS_WHEAT', 'BONUS_PIG', 'BONUS_INCENSE',
    'BONUS_SUGAR', 'BONUS_RICE', 'BONUS_BANANA', 'BONUS_SILK'
]

def build_expanded_map():
    print(f"Reading source 124x68 map: {SOURCE_WBSAVE}")
    with open(SOURCE_WBSAVE, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Parse header up to BeginMap
    map_idx = content.find("BeginMap")
    header_part = content[:map_idx]

    # Parse source plots
    plots_raw = re.findall(r"(BeginPlot\s+.*?EndPlot)", content, re.DOTALL)
    print(f"Found {len(plots_raw)} source plots.")

    src_grid = {}
    src_bonuses = []
    src_starts = []

    for p in plots_raw:
        lines = [l.strip() for l in p.splitlines()]
        coords = [l for l in lines if l.startswith("x=")][0]
        parts = coords.split(",")
        x = int(parts[0].split("=")[1])
        y = int(parts[1].split("=")[1])
        pt = [l for l in lines if l.startswith("PlotType=")][0].split("=")[1]
        tt = [l for l in lines if l.startswith("TerrainType=")][0].split("=")[1]
        b = [l for l in lines if l.startswith("BonusType=")]
        f = [l for l in lines if l.startswith("FeatureType=")]
        rn = "isNOfRiver" in lines
        rw = "isWOfRiver" in lines
        rwe = [int(l.split("=")[1]) for l in lines if l.startswith("RiverWEDirection=")]
        rns = [int(l.split("=")[1]) for l in lines if l.startswith("RiverNSDirection=")]
        sp = "StartingPlot" in lines

        src_grid[(x, y)] = {
            "pt": pt, "tt": tt,
            "f": f[0] if f else None,
            "rn": rn, "rw": rw,
            "rwe": rwe[0] if rwe else 0,
            "rns": rns[0] if rns else 0,
        }
        if b:
            src_bonuses.append((x, y, b[0].split("=")[1]))
        if sp:
            src_starts.append((x, y))

    print(f"Loaded {len(src_bonuses)} bonuses and {len(src_starts)} starting plots.")

    # 2. Build target 158x80 grid
    tgt_grid = {}
    for Y in range(H_TGT):
        for X in range(W_TGT):
            # Map to source float coords
            xs = X * rx
            ys = Y * ry
            x0 = int(round(xs))
            y0 = int(round(ys))
            x0 = max(0, min(W_SRC - 1, x0))
            y0 = max(0, min(H_SRC - 1, y0))

            src_plot = src_grid[(x0, y0)]
            tgt_grid[(X, Y)] = {
                "pt": src_plot["pt"],
                "tt": src_plot["tt"],
                "f": src_plot["f"],
                "rn": False,
                "rw": False,
                "rwe": 0,
                "rns": 0,
                "b": None,
                "sp": False
            }

    # 3. Preserve critical straits & islands
    # English Channel: ensure water between England (X: 70-73, Y: 62-65) and France (X: 73-77, Y: 58-61)
    for cx in range(71, 75):
        if tgt_grid.get((cx, 61), {}).get("pt") == "2" and tgt_grid.get((cx, 63), {}).get("pt") == "2":
            tgt_grid[(cx, 61)]["pt"] = "3"
            tgt_grid[(cx, 61)]["tt"] = "TERRAIN_COAST"

    # Tsushima / Korea Strait: ensure water between Korea (X: 137) and Japan (X: 140)
    for ty in range(45, 49):
        tgt_grid[(138, ty)]["pt"] = "3"
        tgt_grid[(138, ty)]["tt"] = "TERRAIN_COAST"
        tgt_grid[(139, ty)]["pt"] = "3"
        tgt_grid[(139, ty)]["tt"] = "TERRAIN_COAST"

    # Taiwan Strait & Taiwan Island:
    tgt_grid[(135, 39)]["pt"] = "2" # Taiwan plain
    tgt_grid[(135, 39)]["tt"] = "TERRAIN_GRASS"
    tgt_grid[(135, 39)]["f"] = "FeatureType=FEATURE_JUNGLE, FeatureVariety=0"
    tgt_grid[(135, 38)]["pt"] = "2" # Taiwan plain
    tgt_grid[(135, 38)]["tt"] = "TERRAIN_GRASS"
    tgt_grid[(135, 38)]["f"] = "FeatureType=FEATURE_JUNGLE, FeatureVariety=0"
    # Taiwan Strait between mainland China (X: 130-132) and Taiwan (X: 135)
    for ty in range(37, 41):
        for tx in [133, 134]:
            tgt_grid[(tx, ty)]["pt"] = "3"
            tgt_grid[(tx, ty)]["tt"] = "TERRAIN_COAST"

    # 4. Map Starting Plots
    # 18 Civilizations mapping
    civ_coord_map = {
        "CIVILIZATION_EGYPT": (69, 37),
        "CIVILIZATION_INDIA": (90, 40),
        "CIVILIZATION_CHINA": (102, 47),
        "CIVILIZATION_TAIWAN": (118, 16),
        "CIVILIZATION_ROME": (61, 46),
        "CIVILIZATION_PERSIA": (82, 40),
        "CIVILIZATION_JAPAN": (113, 45),
        "CIVILIZATION_GERMANY": (62, 52),
        "CIVILIZATION_MONGOL": (99, 51),
        "CIVILIZATION_FRANCE": (58, 51),
        "CIVILIZATION_ARABIA": (75, 35),
        "CIVILIZATION_VIKING": (62, 58),
        "CIVILIZATION_ENGLAND": (56, 53),
        "CIVILIZATION_RUSSIA": (73, 54),
        "CIVILIZATION_MALI": (55, 34),
        "CIVILIZATION_INCA": (30, 23),
        "CIVILIZATION_AZTEC": (19, 37),
        "CIVILIZATION_AMERICA": (28, 45),
    }

    tgt_civ_starts = {}
    for civ_name, (sx, sy) in civ_coord_map.items():
        TX = int(round(sx / rx))
        TY = int(round(sy / ry))
        # Ensure starting plot is land and not peak
        if tgt_grid[(TX, TY)]["pt"] in ["0", "3"]:
            # Find nearest land tile
            for d in [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]:
                nx, ny = TX + d[0], TY + d[1]
                if tgt_grid.get((nx, ny), {}).get("pt") in ["1", "2"]:
                    TX, TY = nx, ny
                    break
        tgt_grid[(TX, TY)]["sp"] = True
        tgt_civ_starts[civ_name] = (TX, TY)

    # 5. Map Rivers
    # For every river in source, map to target
    for (sx, sy), p in src_grid.items():
        if p["rn"] or p["rw"]:
            TX = int(round(sx / rx))
            TY = int(round(sy / ry))
            if (TX, TY) in tgt_grid:
                if p["rn"]:
                    tgt_grid[(TX, TY)]["rn"] = True
                    tgt_grid[(TX, TY)]["rwe"] = p["rwe"]
                if p["rw"]:
                    tgt_grid[(TX, TY)]["rw"] = True
                    tgt_grid[(TX, TY)]["rns"] = p["rns"]

    # 6. Map Bonuses
    WATER_BONUSES = {'BONUS_FISH', 'BONUS_CLAM', 'BONUS_CRAB', 'BONUS_WHALE'}
    for sx, sy, b_name in src_bonuses:
        TX = int(round(sx / rx))
        TY = int(round(sy / ry))
        is_water_bonus = b_name in WATER_BONUSES
        
        # Check target tile compatibility
        pt = tgt_grid[(TX, TY)]["pt"]
        if is_water_bonus and pt != "3":
            # Find nearest water plot
            found = False
            for dx in [0, -1, 1, -2, 2]:
                for dy in [0, -1, 1, -2, 2]:
                    nx, ny = TX + dx, TY + dy
                    if tgt_grid.get((nx, ny), {}).get("pt") == "3" and not tgt_grid[(nx, ny)]["b"]:
                        TX, TY = nx, ny
                        found = True
                        break
                if found: break
        elif not is_water_bonus and pt == "3" and b_name != "BONUS_OIL":
            # Find nearest land plot
            found = False
            for dx in [0, -1, 1, -2, 2]:
                for dy in [0, -1, 1, -2, 2]:
                    nx, ny = TX + dx, TY + dy
                    if tgt_grid.get((nx, ny), {}).get("pt") in ["1", "2"] and not tgt_grid[(nx, ny)]["b"]:
                        TX, TY = nx, ny
                        found = True
                        break
                if found: break

        # Peak cannot have bonus
        if tgt_grid[(TX, TY)]["pt"] == "0":
            for dx in [0, -1, 1]:
                for dy in [0, -1, 1]:
                    nx, ny = TX + dx, TY + dy
                    if tgt_grid.get((nx, ny), {}).get("pt") in ["1", "2"] and not tgt_grid[(nx, ny)]["b"]:
                        TX, TY = nx, ny
                        break

        # If already occupied, shift slightly
        if tgt_grid[(TX, TY)]["b"]:
            for dx in [1, -1, 0, 0, 1, -1]:
                for dy in [0, 0, 1, -1, 1, -1]:
                    nx, ny = TX + dx, TY + dy
                    if (nx, ny) in tgt_grid and not tgt_grid[(nx, ny)]["b"]:
                        n_pt = tgt_grid[(nx, ny)]["pt"]
                        if (is_water_bonus and n_pt == "3") or (not is_water_bonus and n_pt in ["1", "2"]):
                            TX, TY = nx, ny
                            break
                if not tgt_grid[(TX, TY)]["b"]:
                    break

        tgt_grid[(TX, TY)]["b"] = b_name

    # 7. Update Players in header with new StartingX, StartingY
    new_header = header_part
    for civ_name, (tx, ty) in tgt_civ_starts.items():
        # Replace StartingX=..., StartingY=... in the civ block
        pattern = rf"(CivType={civ_name}.*?StartingX=)\d+(,\s*StartingY=)\d+"
        new_header = re.sub(pattern, rf"\g<1>{tx}\g<2>{ty}", new_header, flags=re.DOTALL)

    # 8. Update BeginMap
    map_text = (
        "BeginMap\n"
        f"\tgrid width={W_TGT}\n"
        f"\tgrid height={H_TGT}\n"
        "\twrap X=1\n"
        "\twrap Y=0\n"
        "\ttop latitude=90\n"
        "\tbottom latitude=-90\n"
        "\tworld size=WORLDSIZE_HUGE\n"
        "\tclimate=CLIMATE_TEMPERATE\n"
        "\tsealevel=SEALEVEL_MEDIUM\n"
        f"\tnum plots written={W_TGT * H_TGT}\n"
        "EndMap\n"
    )

    # 9. Format plots
    plot_strings = []
    for Y in range(H_TGT):
        for X in range(W_TGT):
            p = tgt_grid[(X, Y)]
            lines = [f"BeginPlot", f"\tx={X},y={Y}"]
            if p["rn"]:
                lines.append("\tisNOfRiver")
                lines.append(f"\tRiverWEDirection={p['rwe']}")
            if p["rw"]:
                lines.append("\tisWOfRiver")
                lines.append(f"\tRiverNSDirection={p['rns']}")
            if p["sp"]:
                lines.append("\tStartingPlot")
            if p["b"]:
                lines.append(f"\tBonusType={p['b']}")
            if p["f"]:
                lines.append(f"\t{p['f']}")
            lines.append(f"\tTerrainType={p['tt']}")
            lines.append(f"\tPlotType={p['pt']}")
            lines.append("EndPlot")
            plot_strings.append("\n".join(lines))

    final_wbsave = new_header + map_text + "\n".join(plot_strings) + "\n"

    # Save to patch
    os.makedirs(os.path.dirname(OUTPUT_WBSAVE_PATCH), exist_ok=True)
    with open(OUTPUT_WBSAVE_PATCH, "w", encoding="utf-8", newline="\r\n") as f:
        f.write(final_wbsave)
    print(f"Saved expanded WBSave to: {OUTPUT_WBSAVE_PATCH}")

    # Deploy to Steam and User directories
    deploy_targets = [
        STEAM_BTS_MAPS,
        STEAM_ROOT_MAPS,
        USER_MY_GAMES_MAPS
    ]
    for target_dir in deploy_targets:
        if os.path.exists(target_dir):
            target_file = os.path.join(target_dir, "The Earth (Huge 50% Expanded).CivBeyondSwordWBSave")
            with open(target_file, "w", encoding="utf-8", newline="\r\n") as f:
                f.write(final_wbsave)
            print(f"Deployed expanded WBSave to: {target_file}")

    return final_wbsave, plot_strings, tgt_grid

def build_py_script(plot_strings, tgt_grid):
    print("Formatting plot data for expanded Python map script...")
    terrain_map = dict((name, i) for i, name in enumerate(TERRAIN_LIST))
    feature_map = dict((name, i) for i, name in enumerate(FEATURE_LIST))
    bonus_map = dict((name, i) for i, name in enumerate(BONUS_LIST))

    MAP_WIDTH = W_TGT
    MAP_HEIGHT = H_TGT

    plot_types_str = "".join([str(tgt_grid[(X, Y)]["pt"]) for Y in range(MAP_HEIGHT) for X in range(MAP_WIDTH)])
    terrain_types_str = "".join([str(terrain_map[tgt_grid[(X, Y)]["tt"]]) for Y in range(MAP_HEIGHT) for X in range(MAP_WIDTH)])

    rivers = []
    features = []
    bonuses = []
    for (X, Y), p in tgt_grid.items():
        if p["rn"] or p["rw"]:
            rivers.append((X, Y, 1 if p["rn"] else 0, 1 if p["rw"] else 0, p["rwe"], p["rns"]))
        if p["f"]:
            f_name = p["f"].split(",")[0].split("=")[1]
            f_var = int(p["f"].split("FeatureVariety=")[1]) if "FeatureVariety=" in p["f"] else 0
            if f_name in feature_map:
                features.append((X, Y, feature_map[f_name], f_var))
        if p["b"] and p["b"] in bonus_map:
            bonuses.append((X, Y, bonus_map[p["b"]]))

    py_content = f'''#
#   FILE:    The_Earth_Huge.py
#   PURPOSE: Historically Researched 158x80 (Huge +50% Expanded) Earth Map for Civilization IV BTS
#            Features 18 Real-World Civilizations with Taiwan in Australia and Vikings in Scandinavia
#
from CvPythonExtensions import *
import CvUtil

MAP_WIDTH = 158
MAP_HEIGHT = 80
NUM_PLOTS = 12640

TERRAIN_LIST = {repr(TERRAIN_LIST)}
FEATURE_LIST = {repr(FEATURE_LIST)}
BONUS_LIST = {repr(BONUS_LIST)}

PLOT_TYPES_DATA = "{plot_types_str}"
TERRAIN_TYPES_DATA = "{terrain_types_str}"
RIVERS_DATA = {repr(rivers)}
FEATURES_DATA = {repr(features)}
BONUSES_DATA = {repr(bonuses)}

def getDescription():
    return "TXT_KEY_MAP_SCRIPT_THE_EARTH_DESCR"

def isAdvancedMap():
    return 0

def getNumCustomMapOptions():
    return 0

def getNumHiddenCustomMapOptions():
    return 0

def isClimateMap():
    return 0

def isSeaLevelMap():
    return 0

def getGridSize(argsList):
    return (39, 20)

def getWrapX():
    return True

def getWrapY():
    return False

def getTopLatitude():
    return 90

def getBottomLatitude():
    return -90

def isBonusIgnoreLatitude():
    return True

def generatePlotTypes():
    plot_map = [PlotTypes.PLOT_PEAK, PlotTypes.PLOT_HILLS, PlotTypes.PLOT_LAND, PlotTypes.PLOT_OCEAN]
    return [plot_map[int(c)] for c in PLOT_TYPES_DATA]

def generateTerrainTypes():
    gc = CyGlobalContext()
    terrain_ids = [gc.getInfoTypeForString(name) for name in TERRAIN_LIST]
    return [terrain_ids[int(c)] for c in TERRAIN_TYPES_DATA]

def addRivers():
    cy_map = CyMap()
    for x, y, rn, rw, rwe, rns in RIVERS_DATA:
        pPlot = cy_map.plot(x, y)
        if rn:
            pPlot.setNOfRiver(True, CardinalDirectionTypes(rwe))
        if rw:
            pPlot.setWOfRiver(True, CardinalDirectionTypes(rns))

def addLakes():
    return None

def addFeatures():
    gc = CyGlobalContext()
    cy_map = CyMap()
    feature_ids = []
    for name in FEATURE_LIST:
        if name:
            feature_ids.append(gc.getInfoTypeForString(name))
        else:
            feature_ids.append(-1)
    for x, y, f_idx, f_var in FEATURES_DATA:
        iFeat = feature_ids[f_idx]
        if iFeat != -1:
            pPlot = cy_map.plot(x, y)
            pPlot.setFeatureType(iFeat, f_var)

def addBonuses():
    gc = CyGlobalContext()
    cy_map = CyMap()
    bonus_ids = []
    for name in BONUS_LIST:
        if name:
            bonus_ids.append(gc.getInfoTypeForString(name))
        else:
            bonus_ids.append(-1)
    for x, y, b_idx in BONUSES_DATA:
        iBonus = bonus_ids[b_idx]
        if iBonus != -1:
            pPlot = cy_map.plot(x, y)
            pPlot.setBonusType(iBonus)

def addGoodies():
    return None

def assignStartingPlots():
    gc = CyGlobalContext()
    cy_map = CyMap()

    civ_coords = {{
        "CIVILIZATION_EGYPT": (88, 44),
        "CIVILIZATION_INDIA": (115, 47),
        "CIVILIZATION_CHINA": (130, 55),
        "CIVILIZATION_TAIWAN": (150, 19),
        "CIVILIZATION_ROME": (78, 54),
        "CIVILIZATION_PERSIA": (104, 47),
        "CIVILIZATION_JAPAN": (144, 53),
        "CIVILIZATION_GERMANY": (79, 61),
        "CIVILIZATION_MONGOL": (126, 60),
        "CIVILIZATION_FRANCE": (74, 60),
        "CIVILIZATION_ARABIA": (96, 41),
        "CIVILIZATION_VIKING": (79, 68),
        "CIVILIZATION_ENGLAND": (71, 62),
        "CIVILIZATION_RUSSIA": (93, 64),
        "CIVILIZATION_MALI": (70, 40),
        "CIVILIZATION_INCA": (38, 27),
        "CIVILIZATION_AZTEC": (24, 44),
        "CIVILIZATION_AMERICA": (36, 53),
    }}

    assigned_plots = set()
    unassigned_players = []

    for i in range(gc.getMAX_CIV_PLAYERS()):
        pPlayer = gc.getPlayer(i)
        if pPlayer.isAlive():
            iCiv = pPlayer.getCivilizationType()
            civ_info = gc.getCivilizationInfo(iCiv)
            civ_type = civ_info.getType() if civ_info else ""
            if civ_type in civ_coords and civ_coords[civ_type] not in assigned_plots:
                x, y = civ_coords[civ_type]
                pPlot = cy_map.plot(x, y)
                pPlayer.setStartingPlot(pPlot, True)
                assigned_plots.add((x, y))
            else:
                unassigned_players.append(pPlayer)

    fallback_plots = [
        (150, 19), (130, 55), (88, 44), (115, 47), (78, 54),
        (93, 64), (36, 53), (74, 60), (126, 60), (104, 47),
        (71, 62), (70, 40), (79, 61), (144, 53), (70, 40),
        (38, 27), (24, 44), (96, 41)
    ]
    for pPlayer in unassigned_players:
        for x, y in fallback_plots:
            if (x, y) not in assigned_plots:
                pPlot = cy_map.plot(x, y)
                pPlayer.setStartingPlot(pPlot, True)
                assigned_plots.add((x, y))
                break

def findStartingPlot(argsList):
    playerID = argsList[0]
    return CyGlobalContext().getPlayer(playerID).getStartingPlot()

def normalizeStartingPlotLocations():
    return None

def normalizeAddRiver():
    return None

def normalizeRemovePeaks():
    return None

def normalizeAddLakes():
    return None

def normalizeRemoveBadFeatures():
    return None

def normalizeRemoveBadTerrain():
    return None

def normalizeAddFoodBonuses():
    return None

def normalizeAddGoodTerrain():
    return None

def normalizeAddExtras():
    return None
'''

    os.makedirs(os.path.dirname(OUTPUT_PY_PATCH), exist_ok=True)
    with open(OUTPUT_PY_PATCH, "w", encoding="utf-8", newline="\r\n") as f:
        f.write(py_content)
    print(f"Saved expanded Python script to: {OUTPUT_PY_PATCH}")

    deploy_targets = [
        STEAM_BTS_MAPS,
        STEAM_ROOT_MAPS,
        USER_MY_GAMES_MAPS
    ]
    for target_dir in deploy_targets:
        if os.path.exists(target_dir):
            target_file = os.path.join(target_dir, "The_Earth_Huge.py")
            with open(target_file, "w", encoding="utf-8", newline="\r\n") as f:
                f.write(py_content)
            print(f"Deployed expanded Python script to: {target_file}")

if __name__ == "__main__":
    final_wbsave, plot_strings, tgt_grid = build_expanded_map()
    build_py_script(plot_strings, tgt_grid)
