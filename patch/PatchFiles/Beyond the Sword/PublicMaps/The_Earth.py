#
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

TERRAIN_LIST = ['TERRAIN_OCEAN', 'TERRAIN_COAST', 'TERRAIN_GRASS', 'TERRAIN_SNOW', 'TERRAIN_PLAINS', 'TERRAIN_TUNDRA', 'TERRAIN_DESERT']
FEATURE_LIST = [None, 'FEATURE_ICE', 'FEATURE_JUNGLE', 'FEATURE_FOREST', 'FEATURE_OASIS', 'FEATURE_FLOOD_PLAINS']
BONUS_LIST = [None, 'BONUS_FISH', 'BONUS_DEER', 'BONUS_CRAB', 'BONUS_GOLD', 'BONUS_OIL', 'BONUS_CLAM', 'BONUS_COPPER', 'BONUS_SILVER', 'BONUS_COAL', 'BONUS_STONE', 'BONUS_FUR', 'BONUS_URANIUM', 'BONUS_DYE', 'BONUS_CORN', 'BONUS_MARBLE', 'BONUS_SPICES', 'BONUS_ALUMINUM', 'BONUS_IRON', 'BONUS_WHALE', 'BONUS_GEMS', 'BONUS_SHEEP', 'BONUS_IVORY', 'BONUS_WINE', 'BONUS_HORSE', 'BONUS_COW', 'BONUS_WHEAT', 'BONUS_PIG', 'BONUS_INCENSE', 'BONUS_SUGAR', 'BONUS_RICE', 'BONUS_BANANA', 'BONUS_SILK']

MAP_DATA_B64 = """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"""

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
