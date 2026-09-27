import os
import re
import struct
import zlib
import base64

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STEAM_PATH = r"C:\Program Files (x86)\Steam\steamapps\common\Sid Meier's Civilization IV Beyond the Sword"
SOURCE_MAP = os.path.join(STEAM_PATH, "PublicMaps", "Earth18Civs.Civ4WorldBuilderSave")

OUTPUT_WBSAVE_PATCH = os.path.join(ROOT, "patch", "PatchFiles", "Beyond the Sword", "PublicMaps", "The Earth.CivBeyondSwordWBSave")
OUTPUT_PY_PATCH = os.path.join(ROOT, "patch", "PatchFiles", "Beyond the Sword", "PublicMaps", "The_Earth.py")

USER_MY_GAMES_MAPS = os.path.expanduser(r"~\OneDrive\文件\My Games\beyond the sword\PublicMaps")
STEAM_BTS_MAPS = os.path.join(STEAM_PATH, "Beyond the Sword", "PublicMaps")
STEAM_ROOT_MAPS = os.path.join(STEAM_PATH, "PublicMaps")

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

def build_wbsave():
    print(f"Reading base map: {SOURCE_MAP}")
    with open(SOURCE_MAP, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()

    # 1. Update Teams (Team 3: Taiwan, Team 11: Viking)
    team_blocks = re.split(r"(BeginTeam\s+.*?EndTeam)", content, flags=re.DOTALL)
    team_idx = 0
    new_blocks = []
    for block in team_blocks:
        if block.startswith("BeginTeam"):
            if team_idx == 3:
                block = ("BeginTeam\n"
                         "\tTech=TECH_AGRICULTURE\n"
                         "\tTech=TECH_MINING\n"
                         "EndTeam")
            elif team_idx == 11:
                block = ("BeginTeam\n"
                         "\tTech=TECH_FISHING\n"
                         "\tTech=TECH_HUNTING\n"
                         "EndTeam")
            team_idx += 1
        new_blocks.append(block)
    content = "".join(new_blocks)

    # 2. Update Player 3 (Replace Alexander/Greece with Tsai Ing-wen/Taiwan in Australia)
    player_3_orig = re.search(r"BeginPlayer\s+LeaderType=LEADER_ALEXANDER\s+CivType=CIVILIZATION_GREECE.*?EndPlayer", content, re.DOTALL)
    if not player_3_orig:
        raise ValueError("Could not find Player 3 (LEADER_ALEXANDER) in WBSave")

    player_3_new = ("BeginPlayer\n"
                    "\tLeaderType=LEADER_TSAI_ING_WEN\n"
                    "\tCivType=CIVILIZATION_TAIWAN\n"
                    "\tTeam=3\n"
                    "\tPlayableCiv=1\n"
                    "\tStartingX=118, StartingY=16\n"
                    "\tHandicap=HANDICAP_NOBLE\n"
                    "EndPlayer")
    content = content.replace(player_3_orig.group(0), player_3_new)

    # 3. Update Player 11 (Replace Isabella/Spain with Ragnar/Viking in Scandinavia)
    player_11_orig = re.search(r"BeginPlayer\s+LeaderType=LEADER_ISABELLA\s+CivType=CIVILIZATION_SPAIN.*?EndPlayer", content, re.DOTALL)
    if not player_11_orig:
        raise ValueError("Could not find Player 11 (LEADER_ISABELLA) in WBSave")

    player_11_new = ("BeginPlayer\n"
                     "\tLeaderType=LEADER_RAGNAR\n"
                     "\tCivType=CIVILIZATION_VIKING\n"
                     "\tTeam=11\n"
                     "\tPlayableCiv=1\n"
                     "\tStartingX=62, StartingY=58\n"
                     "\tHandicap=HANDICAP_NOBLE\n"
                     "EndPlayer")
    content = content.replace(player_11_orig.group(0), player_11_new)

    # 4. Update Plots
    plot_header_pos = content.find("BeginPlot")
    header_part = content[:plot_header_pos]
    plots_part = content[plot_header_pos:]

    plots = re.findall(r"(BeginPlot\s+.*?EndPlot)", plots_part, re.DOTALL)
    print(f"Total plots found: {len(plots)}")

    modified_plots = []
    for p in plots:
        lines = [line.rstrip() for line in p.split("\n")]
        coords_line = [l for l in lines if l.strip().startswith("x=")][0]
        parts = coords_line.strip().split(",")
        x = int(parts[0].split("=")[1])
        y = int(parts[1].split("=")[1])

        # (67, 43): Greece old start - remove StartingPlot
        if x == 67 and y == 43:
            lines = [l for l in lines if l.strip() != "StartingPlot"]

        # (55, 46): Spain old start - remove StartingPlot
        elif x == 55 and y == 46:
            lines = [l for l in lines if l.strip() != "StartingPlot"]

        # (62, 58): Viking Scandinavia Capital (Uppsala / Lake Malaren isthmus)
        elif x == 62 and y == 58:
            if not any(l.strip() == "StartingPlot" for l in lines):
                lines.insert(-1, "\tStartingPlot")
            if not any("isNOfRiver" in l for l in lines):
                lines.insert(-1, "\tisNOfRiver")
                lines.insert(-1, "\tRiverWEDirection=1")

        # (62, 57): Kattegat / Skagerrak Fjord Fish for Viking Capital
        elif x == 62 and y == 57:
            lines = [l for l in lines if not l.strip().startswith("BonusType=")]
            lines.insert(-1, "\tBonusType=BONUS_FISH")

        # (60, 58): Great Copper Mountain of Falun (Stora Kopparberg)
        elif x == 60 and y == 58:
            lines = [l for l in lines if not l.strip().startswith("BonusType=")]
            lines.insert(-1, "\tBonusType=BONUS_COPPER")

        # (118, 16): Taiwan Australia Capital (Sydney basin)
        elif x == 118 and y == 16:
            if not any(l.strip() == "StartingPlot" for l in lines):
                lines.insert(-1, "\tStartingPlot")
            if not any("isNOfRiver" in l for l in lines):
                lines.insert(-1, "\tisNOfRiver")
                lines.insert(-1, "\tRiverWEDirection=1")

        # (119, 16): Sydney Coastal Fish
        elif x == 119 and y == 16:
            lines = [l for l in lines if not l.strip().startswith("BonusType=")]
            lines.insert(-1, "\tBonusType=BONUS_FISH")

        # (119, 17): Sydney Coastal Clams / Oysters
        elif x == 119 and y == 17:
            lines = [l for l in lines if not l.strip().startswith("BonusType=")]
            lines.insert(-1, "\tBonusType=BONUS_CLAM")

        # (118, 17): Wheat Belt
        elif x == 118 and y == 17:
            lines = [l for l in lines if not l.strip().startswith("BonusType=")]
            lines.insert(-1, "\tBonusType=BONUS_WHEAT")

        # (117, 15): Pasture Cattle
        elif x == 117 and y == 15:
            lines = [l for l in lines if not l.strip().startswith("BonusType=")]
            lines.insert(-1, "\tBonusType=BONUS_COW")

        # (116, 16): Merino Sheep
        elif x == 116 and y == 16:
            lines = [l for l in lines if not l.strip().startswith("BonusType=")]
            lines.insert(-1, "\tBonusType=BONUS_SHEEP")

        # (115, 10): Melbourne Ballarat Gold
        elif x == 115 and y == 10:
            lines = [l for l in lines if not l.strip().startswith("BonusType=")]
            lines.insert(-1, "\tBonusType=BONUS_GOLD")

        # (115, 9): Port Phillip Bay Fish
        elif x == 115 and y == 9:
            lines = [l for l in lines if not l.strip().startswith("BonusType=")]
            lines.insert(-1, "\tBonusType=BONUS_FISH")

        # (118, 20): Brisbane Moreton Bay Fish
        elif x == 118 and y == 20:
            lines = [l for l in lines if not l.strip().startswith("BonusType=")]
            lines.insert(-1, "\tBonusType=BONUS_FISH")

        # (105, 12): Perth Coast Fish
        elif x == 105 and y == 12:
            lines = [l for l in lines if not l.strip().startswith("BonusType=")]
            lines.insert(-1, "\tBonusType=BONUS_FISH")

        # (116, 14): Australia Blue Mountains / Lithgow Iron
        elif x == 116 and y == 14:
            lines = [l for l in lines if not l.strip().startswith("BonusType=")]
            lines.insert(-1, "\tBonusType=BONUS_IRON")

        # (110, 16): Australia Cooper Basin Desert Land Oil
        elif x == 110 and y == 16:
            lines = [l for l in lines if not l.strip().startswith("BonusType=")]
            lines.insert(-1, "\tBonusType=BONUS_OIL")

        # (114, 9): Australia Bass Strait / Gippsland Offshore Oil
        elif x == 114 and y == 9:
            lines = [l for l in lines if not l.strip().startswith("BonusType=")]
            lines.insert(-1, "\tBonusType=BONUS_OIL")

        # (111, 14): Australia Coober Pedy Opals (Gems)
        elif x == 111 and y == 14:
            lines = [l for l in lines if not l.strip().startswith("BonusType=")]
            lines.insert(-1, "\tBonusType=BONUS_GEMS")

        # (54, 32): Mali Bambuk / Bure Gold Field (Mansa Musa)
        elif x == 54 and y == 32:
            lines = [l for l in lines if not l.strip().startswith("BonusType=")]
            lines.insert(-1, "\tBonusType=BONUS_GOLD")

        # (56, 33): Mali Niger River Flood Plains Wheat
        elif x == 56 and y == 33:
            lines = [l for l in lines if not l.strip().startswith("BonusType=")]
            lines.insert(-1, "\tBonusType=BONUS_WHEAT")

        # (72, 53): Russia Volga / Chernozem Black Earth Wheat
        elif x == 72 and y == 53:
            lines = [l for l in lines if not l.strip().startswith("BonusType=")]
            lines.insert(-1, "\tBonusType=BONUS_WHEAT")

        # (28, 45): America Washington Potomac River freshwater
        elif x == 28 and y == 45:
            if not any("isNOfRiver" in l for l in lines):
                lines.insert(-1, "\tisNOfRiver")
                lines.insert(-1, "\tRiverWEDirection=1")

        # (27, 45): America Virginia Pasture Cattle
        elif x == 27 and y == 45:
            lines = [l for l in lines if not l.strip().startswith("BonusType=")]
            lines.insert(-1, "\tBonusType=BONUS_COW")

        # (67, 47): Europe Romania Ploiești Land Oil Field
        elif x == 67 and y == 47:
            lines = [l for l in lines if not l.strip().startswith("BonusType=")]
            lines.insert(-1, "\tBonusType=BONUS_OIL")

        # (105, 27): Southeast Asia Sumatra Palembang Land Oil Field
        elif x == 105 and y == 27:
            lines = [l for l in lines if not l.strip().startswith("BonusType=")]
            lines.insert(-1, "\tBonusType=BONUS_OIL")

        # (78, 33): Arabia Oman Ancient Magan Copper Mine
        elif x == 78 and y == 33:
            lines = [l for l in lines if not l.strip().startswith("BonusType=")]
            lines.insert(-1, "\tBonusType=BONUS_COPPER")

        # (91, 35): India Deccan / Golconda Diamonds (Gems)
        elif x == 91 and y == 35:
            lines = [l for l in lines if not l.strip().startswith("BonusType=")]
            lines.insert(-1, "\tBonusType=BONUS_GEMS")

        # (28, 32): South America Colombia Muzo Emeralds (Gems)
        elif x == 28 and y == 32:
            lines = [l for l in lines if not l.strip().startswith("BonusType=")]
            lines.insert(-1, "\tBonusType=BONUS_GEMS")

        # (62, 50): Central Europe Bohemia / Saxony Erzgebirge Silver
        elif x == 62 and y == 50:
            lines = [l for l in lines if not l.strip().startswith("BonusType=")]
            lines.insert(-1, "\tBonusType=BONUS_SILVER")

        # (66, 48): Eastern Europe Transylvania Roșia Montană Gold Mine
        elif x == 66 and y == 48:
            lines = [l for l in lines if not l.strip().startswith("BonusType=")]
            lines.insert(-1, "\tBonusType=BONUS_GOLD")

        modified_plots.append("\n".join(lines))

    final_wbsave = header_part + "\n".join(modified_plots) + "\n"

    # Save to patch
    os.makedirs(os.path.dirname(OUTPUT_WBSAVE_PATCH), exist_ok=True)
    with open(OUTPUT_WBSAVE_PATCH, "w", encoding="utf-8", newline="\r\n") as f:
        f.write(final_wbsave)
    print(f"Saved WBSave to: {OUTPUT_WBSAVE_PATCH}")

    # Deploy to Steam and User directories
    deploy_targets = [
        STEAM_BTS_MAPS,
        STEAM_ROOT_MAPS,
        USER_MY_GAMES_MAPS
    ]
    for target_dir in deploy_targets:
        if os.path.exists(target_dir):
            target_file = os.path.join(target_dir, "The Earth.CivBeyondSwordWBSave")
            with open(target_file, "w", encoding="utf-8", newline="\r\n") as f:
                f.write(final_wbsave)
            print(f"Deployed WBSave to: {target_file}")

    return final_wbsave, modified_plots

def build_py_script(plots):
    print("Compressing plot data for Python map script...")
    terrain_map = {name: i for i, name in enumerate(TERRAIN_LIST)}
    feature_map = {name: i for i, name in enumerate(FEATURE_LIST)}
    bonus_map = {name: i for i, name in enumerate(BONUS_LIST)}

    packed = []
    for p in plots:
        lines = [l.strip() for l in p.split("\n")]
        pt = int([l for l in lines if l.startswith("PlotType=")][0].split("=")[1])
        tt = [l for l in lines if l.startswith("TerrainType=")][0].split("=")[1]

        feat = [l for l in lines if l.startswith("FeatureType=")]
        if feat:
            f_name = feat[0].split(",")[0].split("=")[1]
            f_var = int(feat[0].split("FeatureVariety=")[1]) if "FeatureVariety=" in feat[0] else 0
            f_code = (feature_map[f_name] << 2) | (f_var & 3)
        else:
            f_code = 0

        bonus = [l for l in lines if l.startswith("BonusType=")]
        b_code = bonus_map[bonus[0].split("=")[1]] if bonus else 0

        rn = any("isNOfRiver" in l for l in lines)
        rw = any("isWOfRiver" in l for l in lines)
        rwe = [int(l.split("=")[1]) for l in lines if l.startswith("RiverWEDirection=")]
        rns = [int(l.split("=")[1]) for l in lines if l.startswith("RiverNSDirection=")]
        river_byte = (1 if rn else 0) | ((1 if rw else 0) << 1) | ((rwe[0] if rwe else 0) << 2) | ((rns[0] if rns else 0) << 5)

        b0 = (pt & 3) | ((terrain_map[tt] & 63) << 2)
        packed.append(struct.pack("BBBB", b0, f_code, b_code, river_byte))

    raw = b"".join(packed)
    comp = zlib.compress(raw, 9)
    b64_str = base64.b64encode(comp).decode("ascii")

    py_content = f'''#
#   FILE:    The_Earth.py
#   PURPOSE: Historically Researched 124x68 Earth Map for Civilization IV BTS
#            Features 18 Real-World Civilizations with Taiwan in Australia and Vikings in Scandinavia
#
from CvPythonExtensions import *
import CvUtil
import zlib
import base64

MAP_WIDTH = 124
MAP_HEIGHT = 68
NUM_PLOTS = 8432

TERRAIN_LIST = {repr(TERRAIN_LIST)}
FEATURE_LIST = {repr(FEATURE_LIST)}
BONUS_LIST = {repr(BONUS_LIST)}

MAP_DATA_B64 = """{b64_str}"""

_cached_decomp = None

def _byte(val):
    if type(val) is int:
        return val
    return ord(val)

def get_decompressed_data():
    global _cached_decomp
    if _cached_decomp is None:
        if hasattr(base64, 'b64decode'):
            raw_comp = base64.b64decode(MAP_DATA_B64)
        else:
            raw_comp = base64.decodestring(MAP_DATA_B64)
        _cached_decomp = zlib.decompress(raw_comp)
    return _cached_decomp

def getDescription():
    return "TXT_KEY_MAP_SCRIPT_THE_EARTH_DESCR"

def isAdvancedMap():
    return 0

def getGridSize(argsList):
    return (31, 17)

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

def isClimateMap():
    return 0

def isSeaLevelMap():
    return 0

def generatePlotTypes():
    data = get_decompressed_data()
    plot_types = [PlotTypes.PLOT_OCEAN] * NUM_PLOTS
    for x in range(MAP_WIDTH):
        for y in range(MAP_HEIGHT):
            wb_idx = x * MAP_HEIGHT + y
            map_idx = y * MAP_WIDTH + x
            b0 = _byte(data[wb_idx * 4])
            pt = b0 & 3
            if pt == 0:
                plot_types[map_idx] = PlotTypes.PLOT_PEAK
            elif pt == 1:
                plot_types[map_idx] = PlotTypes.PLOT_HILLS
            elif pt == 2:
                plot_types[map_idx] = PlotTypes.PLOT_LAND
            else:
                plot_types[map_idx] = PlotTypes.PLOT_OCEAN
    return plot_types

def generateTerrainTypes():
    gc = CyGlobalContext()
    data = get_decompressed_data()
    terrain_types = [0] * NUM_PLOTS
    for x in range(MAP_WIDTH):
        for y in range(MAP_HEIGHT):
            wb_idx = x * MAP_HEIGHT + y
            map_idx = y * MAP_WIDTH + x
            b0 = _byte(data[wb_idx * 4])
            t_idx = (b0 >> 2) & 63
            t_name = TERRAIN_LIST[t_idx]
            terrain_types[map_idx] = gc.getInfoTypeForString(t_name)
    return terrain_types

def addRivers():
    data = get_decompressed_data()
    cy_map = CyMap()
    for x in range(MAP_WIDTH):
        for y in range(MAP_HEIGHT):
            wb_idx = x * MAP_HEIGHT + y
            offset = wb_idx * 4
            river_byte = _byte(data[offset + 3])
            rn = bool(river_byte & 1)
            rw = bool(river_byte & 2)
            rwe = (river_byte >> 2) & 7
            rns = (river_byte >> 5) & 7
            pPlot = cy_map.plot(x, y)
            if rn:
                eCard = CardinalDirectionTypes(rwe)
                pPlot.setNOfRiver(True, eCard)
            if rw:
                eCard = CardinalDirectionTypes(rns)
                pPlot.setWOfRiver(True, eCard)

def addLakes():
    return None

def addFeatures():
    gc = CyGlobalContext()
    data = get_decompressed_data()
    cy_map = CyMap()
    for x in range(MAP_WIDTH):
        for y in range(MAP_HEIGHT):
            wb_idx = x * MAP_HEIGHT + y
            offset = wb_idx * 4
            f_code = _byte(data[offset + 1])
            if f_code > 0:
                f_idx = f_code >> 2
                f_var = f_code & 3
                f_name = FEATURE_LIST[f_idx]
                if f_name:
                    iFeat = gc.getInfoTypeForString(f_name)
                    pPlot = cy_map.plot(x, y)
                    pPlot.setFeatureType(iFeat, f_var)

def addBonuses():
    gc = CyGlobalContext()
    data = get_decompressed_data()
    cy_map = CyMap()
    for x in range(MAP_WIDTH):
        for y in range(MAP_HEIGHT):
            wb_idx = x * MAP_HEIGHT + y
            offset = wb_idx * 4
            b_code = _byte(data[offset + 2])
            if b_code > 0:
                b_name = BONUS_LIST[b_code]
                if b_name:
                    iBonus = gc.getInfoTypeForString(b_name)
                    pPlot = cy_map.plot(x, y)
                    pPlot.setBonusType(iBonus)

def addGoodies():
    return None

def assignStartingPlots():
    gc = CyGlobalContext()
    cy_map = CyMap()

    civ_coords = {{
        "CIVILIZATION_TAIWAN": (118, 16),
        "CIVILIZATION_CHINA": (102, 47),
        "CIVILIZATION_JAPAN": (113, 45),
        "CIVILIZATION_INDIA": (90, 40),
        "CIVILIZATION_EGYPT": (69, 37),
        "CIVILIZATION_ROME": (61, 46),
        "CIVILIZATION_GERMANY": (62, 52),
        "CIVILIZATION_FRANCE": (58, 51),
        "CIVILIZATION_ENGLAND": (56, 53),
        "CIVILIZATION_SPAIN": (55, 46),
        "CIVILIZATION_RUSSIA": (73, 54),
        "CIVILIZATION_PERSIA": (82, 40),
        "CIVILIZATION_ARABIA": (75, 35),
        "CIVILIZATION_MONGOL": (99, 51),
        "CIVILIZATION_MALI": (55, 34),
        "CIVILIZATION_AMERICA": (28, 45),
        "CIVILIZATION_AZTEC": (19, 37),
        "CIVILIZATION_INCA": (30, 23),
        "CIVILIZATION_BABYLON": (79, 41),
        "CIVILIZATION_BYZANTIUM": (69, 45),
        "CIVILIZATION_CARTHAGE": (60, 41),
        "CIVILIZATION_CELT": (55, 56),
        "CIVILIZATION_ETHIOPIA": (74, 30),
        "CIVILIZATION_KHMER": (99, 35),
        "CIVILIZATION_KOREA": (108, 48),
        "CIVILIZATION_MAYA": (17, 36),
        "CIVILIZATION_NATIVE_AMERICA": (21, 49),
        "CIVILIZATION_NETHERLANDS": (59, 53),
        "CIVILIZATION_OTTOMAN": (70, 44),
        "CIVILIZATION_PORTUGAL": (52, 45),
        "CIVILIZATION_SUMERIA": (80, 39),
        "CIVILIZATION_VIKING": (62, 58),
        "CIVILIZATION_ZULU": (67, 12),
    }}

    assigned_plots = []
    unassigned_players = []

    for i in range(gc.getMAX_CIV_PLAYERS()):
        pPlayer = gc.getPlayer(i)
        if pPlayer.isAlive():
            iCiv = pPlayer.getCivilizationType()
            civ_info = gc.getCivilizationInfo(iCiv)
            civ_type = ""
            if civ_info:
                civ_type = civ_info.getType()
            if civ_type in civ_coords and civ_coords[civ_type] not in assigned_plots:
                x, y = civ_coords[civ_type]
                pPlot = cy_map.plot(x, y)
                pPlayer.setStartingPlot(pPlot, True)
                assigned_plots.append((x, y))
            else:
                unassigned_players.append(pPlayer)

    fallback_plots = [
        (118, 16), (102, 47), (69, 37), (90, 40), (61, 46),
        (73, 54), (28, 45), (58, 51), (99, 51), (82, 40),
        (56, 53), (62, 58), (62, 52), (113, 45), (55, 34),
        (30, 23), (19, 37), (75, 35)
    ]
    for pPlayer in unassigned_players:
        for x, y in fallback_plots:
            if (x, y) not in assigned_plots:
                pPlot = cy_map.plot(x, y)
                pPlayer.setStartingPlot(pPlot, True)
                assigned_plots.append((x, y))
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

    # Clean up old space-named file in patch if it exists
    old_patch_py = os.path.join(ROOT, "patch", "PatchFiles", "Beyond the Sword", "PublicMaps", "The Earth.py")
    if os.path.exists(old_patch_py):
        os.remove(old_patch_py)
        print(f"Removed old space-named script: {old_patch_py}")

    os.makedirs(os.path.dirname(OUTPUT_PY_PATCH), exist_ok=True)
    with open(OUTPUT_PY_PATCH, "w", encoding="utf-8", newline="\r\n") as f:
        f.write(py_content)
    print(f"Saved Python script to: {OUTPUT_PY_PATCH}")

    deploy_targets = [
        STEAM_BTS_MAPS,
        STEAM_ROOT_MAPS,
        USER_MY_GAMES_MAPS
    ]
    for target_dir in deploy_targets:
        if os.path.exists(target_dir):
            old_file = os.path.join(target_dir, "The Earth.py")
            if os.path.exists(old_file):
                os.remove(old_file)
                print(f"Removed old space-named script: {old_file}")
            target_file = os.path.join(target_dir, "The_Earth.py")
            with open(target_file, "w", encoding="utf-8", newline="\r\n") as f:
                f.write(py_content)
            print(f"Deployed Python script to: {target_file}")

if __name__ == "__main__":
    final_wbsave, modified_plots = build_wbsave()
    build_py_script(modified_plots)

