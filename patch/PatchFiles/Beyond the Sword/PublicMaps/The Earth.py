#
#   FILE:    The Earth.py
#   PURPOSE: Historically Researched 124x68 Earth Map for Civilization IV BTS
#            Features 18 Real-World Civilizations with Taiwan Civilization located in Australia
#
from CvPythonExtensions import *
import CvUtil
import struct
import zlib
import base64

MAP_WIDTH = 124
MAP_HEIGHT = 68
NUM_PLOTS = 8432

TERRAIN_LIST = ['TERRAIN_OCEAN', 'TERRAIN_COAST', 'TERRAIN_GRASS', 'TERRAIN_SNOW', 'TERRAIN_PLAINS', 'TERRAIN_TUNDRA', 'TERRAIN_DESERT']
FEATURE_LIST = [None, 'FEATURE_ICE', 'FEATURE_JUNGLE', 'FEATURE_FOREST', 'FEATURE_OASIS', 'FEATURE_FLOOD_PLAINS']
BONUS_LIST = [None, 'BONUS_FISH', 'BONUS_DEER', 'BONUS_CRAB', 'BONUS_GOLD', 'BONUS_OIL', 'BONUS_CLAM', 'BONUS_COPPER', 'BONUS_SILVER', 'BONUS_COAL', 'BONUS_STONE', 'BONUS_FUR', 'BONUS_URANIUM', 'BONUS_DYE', 'BONUS_CORN', 'BONUS_MARBLE', 'BONUS_SPICES', 'BONUS_ALUMINUM', 'BONUS_IRON', 'BONUS_WHALE', 'BONUS_GEMS', 'BONUS_SHEEP', 'BONUS_IVORY', 'BONUS_WINE', 'BONUS_HORSE', 'BONUS_COW', 'BONUS_WHEAT', 'BONUS_PIG', 'BONUS_INCENSE', 'BONUS_SUGAR', 'BONUS_RICE', 'BONUS_BANANA', 'BONUS_SILK']

MAP_DATA_B64 = """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"""

_cached_decomp = None

def get_decompressed_data():
    global _cached_decomp
    if _cached_decomp is None:
        raw_comp = base64.b64decode(MAP_DATA_B64)
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
            b0 = struct.unpack_from("B", data, wb_idx * 4)[0]
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
            b0 = struct.unpack_from("B", data, wb_idx * 4)[0]
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
            river_byte = struct.unpack_from("B", data, offset + 3)[0]
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
            f_code = struct.unpack_from("B", data, offset + 1)[0]
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
            b_code = struct.unpack_from("B", data, offset + 2)[0]
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

    civ_coords = {
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
        "CIVILIZATION_VIKING": (65, 59),
        "CIVILIZATION_ZULU": (67, 12),
    }

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
        (118, 16), (102, 47), (69, 37), (90, 40), (61, 46),
        (73, 54), (28, 45), (58, 51), (99, 51), (82, 40),
        (56, 53), (55, 46), (62, 52), (113, 45), (55, 34),
        (30, 23), (19, 37), (75, 35)
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
