#
#   FILE:    The Earth.py
#   PURPOSE: Historically Researched 124x68 Earth Map for Civilization IV BTS
#            Features 18 Real-World Civilizations with Taiwan in Australia and Vikings in Scandinavia
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
        "CIVILIZATION_VIKING": (62, 58),
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
        (56, 53), (62, 58), (62, 52), (113, 45), (55, 34),
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
