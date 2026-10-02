import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SOURCE_WBSAVE = os.path.join(ROOT, "patch", "PatchFiles", "Beyond the Sword", "PublicMaps", "The Earth.CivBeyondSwordWBSave")

MAP_NAME_DISPLAY = "The Earth Ultra (180x90)"
OUTPUT_WBSAVE_PATCH = os.path.join(ROOT, "patch", "PatchFiles", "Beyond the Sword", "PublicMaps", f"{MAP_NAME_DISPLAY}.CivBeyondSwordWBSave")
OUTPUT_PY_PATCH = os.path.join(ROOT, "patch", "PatchFiles", "Beyond the Sword", "PublicMaps", "The_Earth_Ultra.py")

STEAM_PATH = r"C:\Program Files (x86)\Steam\steamapps\common\Sid Meier's Civilization IV Beyond the Sword"
USER_MY_GAMES_MAPS = os.path.expanduser(r"~\OneDrive\文件\My Games\beyond the sword\PublicMaps")
STEAM_BTS_MAPS = os.path.join(STEAM_PATH, "Beyond the Sword", "PublicMaps")
STEAM_ROOT_MAPS = os.path.join(STEAM_PATH, "PublicMaps")

W_SRC, H_SRC = 124, 68
W_TGT, H_TGT = 180, 90

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

# Additional Handcrafted Real-World Resources for the 180x90 Scale
# Format: (X, Y): (BonusType, PlotType, TerrainType, FeatureType, Name)
# PlotType: 1=Hills, 2=Land, 3=Ocean/Coast
ULTRA_GLOBAL_RESOURCES = {
    # ==================== 1. TAIWAN & SURROUNDING SEAS (台灣與周邊海域 - 合理真實分配) ====================
    (154, 45): (None, "2", "TERRAIN_GRASS", None, "Taiwan Taipei Site"),
    (155, 45): ("BONUS_GOLD", "1", "TERRAIN_GRASS", "FeatureType=FEATURE_FOREST, FeatureVariety=0", "Taiwan Jinguashi Gold Mine"),
    (154, 44): ("BONUS_RICE", "2", "TERRAIN_GRASS", None, "Taiwan Chianan Plain Ponlai Rice"),
    (155, 44): (None, "1", "TERRAIN_GRASS", "FeatureType=FEATURE_FOREST, FeatureVariety=1", "Taiwan Central Range / Yushan"),
    (154, 43): ("BONUS_SUGAR", "2", "TERRAIN_GRASS", "FeatureType=FEATURE_JUNGLE, FeatureVariety=0", "Taiwan Kaohsiung / Tainan Cane Sugar"),
    (155, 43): (None, "1", "TERRAIN_GRASS", "FeatureType=FEATURE_FOREST, FeatureVariety=0", "Taiwan Taitung / Hualien Hills"),
    (154, 42): (None, "2", "TERRAIN_GRASS", "FeatureType=FEATURE_FOREST, FeatureVariety=0", "Taiwan Hengchun Peninsula"),
    (152, 44): (None, "1", "TERRAIN_PLAINS", None, "Taiwan Penghu Islands"),
    # Taiwan Marine Resources (合理真實分配)
    (154, 46): ("BONUS_FISH", "3", "TERRAIN_COAST", None, "Taiwan North Coast Fugui Fishery"),
    (153, 44): ("BONUS_FISH", "3", "TERRAIN_COAST", None, "Taiwan Strait Kuroshio Current Fishery"),
    (153, 43): ("BONUS_CRAB", "3", "TERRAIN_COAST", None, "Taiwan Kaohsiung Offshore Crab"),
    (153, 45): ("BONUS_OIL", "3", "TERRAIN_COAST", None, "Taiwan Hsinchu Offshore Gas & Oil Field"),

    # ==================== 2. EAST ASIA & JAPAN (東亞與日本) ====================
    (164, 61): ("BONUS_GOLD", "1", "TERRAIN_GRASS", None, "Japan Sado Island Gold Mine"),
    (165, 60): ("BONUS_COPPER", "1", "TERRAIN_GRASS", "FeatureType=FEATURE_FOREST, FeatureVariety=0", "Japan Ashio Copper Mine"),
    (166, 64): ("BONUS_COAL", "1", "TERRAIN_PLAINS", "FeatureType=FEATURE_FOREST, FeatureVariety=0", "Japan Hokkaido Yubari Coal Basin"),
    (167, 65): ("BONUS_FISH", "3", "TERRAIN_COAST", None, "Japan Sanriku / Nemuro Pacific Fishery"),
    (163, 59): ("BONUS_CLAM", "3", "TERRAIN_COAST", None, "Japan Seto Inland Sea Clams"),
    (162, 57): ("BONUS_COAL", "1", "TERRAIN_GRASS", None, "Japan Kyushu Chikuho Coal Mine"),
    # Japan Central Honshu Peak De-isolation (高山降階解鎖通道與歷史資源配置)
    (163, 56): (None, "0", "TERRAIN_PLAINS", None, "Japan Mount Fuji (Sacred Peak)"),
    (162, 56): ("BONUS_SILVER", "1", "TERRAIN_GRASS", None, "Japan Iwami / Ikuno Historic Silver Mine"),
    (162, 55): ("BONUS_RICE", "2", "TERRAIN_GRASS", "", "Japan Kansai / Kyoto Rice Heartland"),
    (163, 55): ("BONUS_SPICES", "1", "TERRAIN_GRASS", None, "Japan Shizuoka / Uji Green Tea & Spices"),
    (160, 53): ("BONUS_PIG", "2", "TERRAIN_GRASS", None, "Japan Kyushu Kagoshima Kurobuta Pork"),
    # Korea
    (158, 64): ("BONUS_COAL", "1", "TERRAIN_PLAINS", None, "Korea Pyongyang Anthracite Coal"),
    (157, 65): ("BONUS_IRON", "1", "TERRAIN_GRASS", "FeatureType=FEATURE_FOREST, FeatureVariety=0", "Korea Musan Iron Ore"),
    (158, 63): ("BONUS_IRON", "1", "TERRAIN_GRASS", "FeatureType=FEATURE_FOREST, FeatureVariety=1", "Korea Hamgyong Musan Iron Mine"),
    (158, 62): ("BONUS_RICE", "2", "TERRAIN_GRASS", None, "Korea Honam Plain Rice"),

    # ==================== 3. MAINLAND CHINA (中國大陸) ====================
    (149, 63): ("BONUS_IRON", "1", "TERRAIN_PLAINS", None, "China Anshan Iron Basin"),
    (145, 64): ("BONUS_COAL", "1", "TERRAIN_PLAINS", None, "China Shanxi Datong Coal Field"),
    (151, 65): ("BONUS_OIL", "2", "TERRAIN_PLAINS", None, "China Northeast Daqing Oil Field"),
    (149, 58): ("BONUS_RICE", "2", "TERRAIN_GRASS", None, "China Yangtze Delta Taihu Rice"),
    (146, 56): ("BONUS_RICE", "2", "TERRAIN_GRASS", None, "China Poyang / Dongting Lake Rice Bowl"),
    (140, 56): ("BONUS_SPICES", "2", "TERRAIN_GRASS", "FeatureType=FEATURE_FOREST, FeatureVariety=0", "China Sichuan Basin Tea & Salt"),
    (134, 57): ("BONUS_GEMS", "1", "TERRAIN_DESERT", None, "China Xinjiang Hotan Jade"),
    (133, 62): ("BONUS_OIL", "2", "TERRAIN_DESERT", None, "China Xinjiang Tarim Basin Oil Field"),
    (147, 50): ("BONUS_SUGAR", "2", "TERRAIN_GRASS", "FeatureType=FEATURE_JUNGLE, FeatureVariety=0", "China Pearl River Delta Sugar & Fruit"),
    # China Wheat Heartland (黃河流域、華北平原與中原小麥糧倉體系)
    (149, 61): ("BONUS_WHEAT", "2", "TERRAIN_PLAINS", "", "China Hebei / North China Plain Winter Wheat"),
    (150, 59): ("BONUS_WHEAT", "2", "TERRAIN_PLAINS", None, "China Central Plains Henan Wheat Heartland"),
    (145, 59): ("BONUS_WHEAT", "2", "TERRAIN_PLAINS", "", "China Shaanxi Guanzhong Plain Wheat"),
    # China Rice Bowls (天府之國、鄱陽湖與嶺南珠三角水稻)
    (147, 47): ("BONUS_RICE", "2", "TERRAIN_GRASS", "FeatureType=FEATURE_JUNGLE, FeatureVariety=0", "China Pearl River Delta Lingnan Double-Crop Rice"),
    (150, 51): ("BONUS_RICE", "2", "TERRAIN_GRASS", None, "China Poyang Lake Basin Rice Heartland"),
    (141, 53): ("BONUS_RICE", "2", "TERRAIN_GRASS", "FeatureType=FEATURE_JUNGLE, FeatureVariety=0", "China Chengdu Plain Dujiangyan Heavenly Rice Bowl"),

    # ==================== 4. SOUTHEAST ASIA & OCEANIA (東南亞與大洋洲) ====================
    (148, 38): ("BONUS_RICE", "2", "TERRAIN_GRASS", None, "Vietnam Mekong Delta Rice (Saigon)"),
    (149, 42): ("BONUS_RICE", "2", "TERRAIN_GRASS", "FeatureType=FEATURE_JUNGLE, FeatureVariety=0", "Vietnam Red River Delta Rice (Hanoi)"),
    (145, 39): ("BONUS_RICE", "2", "TERRAIN_GRASS", "FeatureType=FEATURE_JUNGLE, FeatureVariety=0", "Thailand Chao Phraya Basin Rice"),
    (142, 42): ("BONUS_RICE", "2", "TERRAIN_GRASS", "FeatureType=FEATURE_JUNGLE, FeatureVariety=0", "Myanmar Irrawaddy Delta Rice"),
    (144, 34): ("BONUS_IRON", "1", "TERRAIN_GRASS", "FeatureType=FEATURE_JUNGLE, FeatureVariety=0", "Malaysia Kinta Valley Tin & Strategic Metals"),
    (159, 36): ("BONUS_COPPER", "1", "TERRAIN_GRASS", "FeatureType=FEATURE_JUNGLE, FeatureVariety=0", "Philippines Cebu / Atlas Porphyry Copper"),
    (165, 33): ("BONUS_SPICES", "2", "TERRAIN_GRASS", "FeatureType=FEATURE_JUNGLE, FeatureVariety=0", "Indonesia Moluccas Spice Islands (Nutmeg & Cloves)"),
    (150, 29): ("BONUS_OIL", "2", "TERRAIN_GRASS", "FeatureType=FEATURE_JUNGLE, FeatureVariety=0", "Indonesia Sumatra Minas Oil Field"),
    (154, 29): ("BONUS_RICE", "2", "TERRAIN_GRASS", None, "Indonesia Java Rice Heartland"),
    # Australia (台灣文明大洋洲發祥地與各州資源)
    (171, 21): (None, "2", "TERRAIN_GRASS", None, "Australia Sydney Starting Plot"),
    (172, 21): ("BONUS_CLAM", "3", "TERRAIN_COAST", None, "Sydney Harbour Rock Oysters"),
    (172, 20): ("BONUS_FISH", "3", "TERRAIN_COAST", None, "Sydney Offshore Fishery"),
    (170, 21): ("BONUS_COAL", "1", "TERRAIN_GRASS", None, "Lithgow / Blue Mountains Coal"),
    (170, 22): ("BONUS_IRON", "1", "TERRAIN_GRASS", None, "Blue Mountains Iron Ore"),
    (167, 19): ("BONUS_SHEEP", "2", "TERRAIN_GRASS", None, "Australia NSW Murray-Darling Merino Wool"),
    (164, 16): ("BONUS_WHEAT", "2", "TERRAIN_PLAINS", None, "Australia Victoria Wheat Belt"),
    (165, 16): ("BONUS_COW", "2", "TERRAIN_GRASS", None, "Victoria / Gippsland Dairy Cattle"),
    (171, 24): ("BONUS_SUGAR", "2", "TERRAIN_GRASS", None, "Queensland Sugar Cane (Brisbane)"),
    (166, 24): ("BONUS_COAL", "2", "TERRAIN_PLAINS", None, "Australia Queensland Bowen Basin Coal"),
    (170, 25): ("BONUS_BANANA", "2", "TERRAIN_GRASS", None, "Queensland Sunshine Coast Bananas"),
    (171, 25): ("BONUS_GOLD", "1", "TERRAIN_GRASS", None, "Queensland Gold Coast / Mount Morgan Gold"),
    (172, 25): ("BONUS_CRAB", "3", "TERRAIN_COAST", None, "Queensland Great Barrier Reef Mud Crab"),
    (153, 19): ("BONUS_GOLD", "1", "TERRAIN_PLAINS", None, "Australia WA Kalgoorlie Super Pit Gold"),
    (151, 21): ("BONUS_IRON", "1", "TERRAIN_PLAINS", None, "Australia WA Pilbara Giant Iron Range"),
    (150, 16): ("BONUS_WHEAT", "2", "TERRAIN_PLAINS", None, "WA Wheatbelt (Perth)"),
    (149, 17): ("BONUS_WINE", "1", "TERRAIN_PLAINS", None, "Swan Valley Wine (Perth)"),
    (160, 21): ("BONUS_OIL", "2", "TERRAIN_PLAINS", None, "Cooper Basin Oil Field"),
    (168, 12): ("BONUS_OIL", "3", "TERRAIN_COAST", None, "Bass Strait Offshore Oil"),
    (169, 10): ("BONUS_FISH", "3", "TERRAIN_COAST", None, "Australia Tasmania Southern Ocean Fishery"),
    (174, 9):  ("BONUS_SHEEP", "1", "TERRAIN_GRASS", None, "New Zealand South Island Pasture Sheep"),
    (177, 12): ("BONUS_FISH", "3", "TERRAIN_COAST", None, "New Zealand North Island Coastal Fishery"),

    # ==================== 5. NORTH AMERICA (北美洲) ====================
    (31, 60):  ("BONUS_WHEAT", "2", "TERRAIN_PLAINS", None, "US Kansas Breadbasket Wheat"),
    (29, 64):  ("BONUS_WHEAT", "2", "TERRAIN_PLAINS", None, "US North Dakota Spring Wheat"),
    (27, 67):  ("BONUS_WHEAT", "2", "TERRAIN_PLAINS", None, "Canada Saskatchewan Wheat"),
    (31, 56):  ("BONUS_OIL", "2", "TERRAIN_DESERT", None, "US Texas Permian Basin Oil"),
    (31, 57):  ("BONUS_COW", "2", "TERRAIN_PLAINS", None, "US Texas Longhorns Beef Cattle"),
    (37, 63):  ("BONUS_IRON", "1", "TERRAIN_GRASS", "FeatureType=FEATURE_FOREST, FeatureVariety=0", "US Lake Superior Mesabi Iron Range"),
    (40, 61):  ("BONUS_COAL", "1", "TERRAIN_GRASS", "FeatureType=FEATURE_FOREST, FeatureVariety=0", "US Appalachian Bituminous Coal Basin"),
    (42, 62):  ("BONUS_CLAM", "3", "TERRAIN_COAST", None, "US Long Island & Chesapeake Clams"),
    (20, 61):  ("BONUS_GOLD", "1", "TERRAIN_PLAINS", None, "US California 1849 Gold Rush"),
    (19, 60):  ("BONUS_WINE", "2", "TERRAIN_PLAINS", None, "US California Napa Valley Wine"),
    (18, 66):  ("BONUS_FISH", "3", "TERRAIN_COAST", None, "US Pacific Northwest Salmon Fishery"),
    (16, 76):  ("BONUS_OIL", "2", "TERRAIN_TUNDRA", None, "US Alaska Prudhoe Bay Giant Oil Field"),
    (22, 73):  ("BONUS_GOLD", "1", "TERRAIN_TUNDRA", None, "Canada Yukon Klondike Gold Fields"),
    (47, 64):  ("BONUS_FISH", "3", "TERRAIN_COAST", None, "Canada Newfoundland Grand Banks Cod Fishery"),

    # ==================== 6. SOUTH AMERICA (南美洲) ====================
    (61, 33):  ("BONUS_IRON", "1", "TERRAIN_GRASS", "FeatureType=FEATURE_FOREST, FeatureVariety=0", "Brazil Minas Gerais Carajas Giant Iron"),
    (58, 31):  ("BONUS_SPICES", "2", "TERRAIN_GRASS", "FeatureType=FEATURE_FOREST, FeatureVariety=0", "Brazil Sao Paulo Coffee"),
    (63, 37):  ("BONUS_SUGAR", "2", "TERRAIN_GRASS", "FeatureType=FEATURE_JUNGLE, FeatureVariety=0", "Brazil Salvador Sugar"),
    (47, 23):  ("BONUS_COPPER", "1", "TERRAIN_DESERT", None, "Chile Atacama Chuquicamata Copper"),
    (49, 34):  ("BONUS_SILVER", "1", "TERRAIN_GRASS", None, "Bolivia Potosi Mountain of Silver"),
    (51, 18):  ("BONUS_WHEAT", "2", "TERRAIN_PLAINS", None, "Argentina Pampas Wheat"),
    (53, 18):  ("BONUS_COW", "2", "TERRAIN_GRASS", None, "Argentina Pampas Beef Cattle"),
    (52, 17):  ("BONUS_HORSE", "2", "TERRAIN_PLAINS", None, "Argentina Gaucho Horses"),
    (49, 20):  ("BONUS_WINE", "1", "TERRAIN_PLAINS", None, "Argentina Mendoza Malbec Wine"),
    (49, 39):  ("BONUS_OIL", "2", "TERRAIN_GRASS", "FeatureType=FEATURE_JUNGLE, FeatureVariety=0", "Venezuela Lake Maracaibo Oil"),
    (47, 37):  ("BONUS_SPICES", "2", "TERRAIN_GRASS", "FeatureType=FEATURE_JUNGLE, FeatureVariety=0", "Colombia Medellin Arabica Coffee"),

    # ==================== 7. EUROPE & MEDITERRANEAN (歐洲與地中海) ====================
    (81, 72):  ("BONUS_COAL", "1", "TERRAIN_GRASS", None, "Britain Yorkshire Coalfield"),
    (79, 71):  ("BONUS_IRON", "1", "TERRAIN_GRASS", None, "Britain South Wales Iron Ore"),
    (83, 75):  ("BONUS_OIL", "3", "TERRAIN_COAST", None, "Britain Aberdeen North Sea Brent Oil"),
    (86, 73):  ("BONUS_FISH", "3", "TERRAIN_COAST", None, "North Sea Dogger Bank Herring Fishery"),
    (89, 70):  ("BONUS_COAL", "2", "TERRAIN_PLAINS", None, "Germany Ruhr Valley Industrial Coal"),
    (90, 69):  ("BONUS_IRON", "1", "TERRAIN_GRASS", "FeatureType=FEATURE_FOREST, FeatureVariety=0", "Germany Siegerland / Lorraine Iron"),
    (83, 66):  ("BONUS_WINE", "2", "TERRAIN_PLAINS", None, "France Bordeaux Wine"),
    (86, 68):  ("BONUS_WINE", "2", "TERRAIN_PLAINS", None, "France Champagne Vineyard"),
    (80, 59):  ("BONUS_COPPER", "1", "TERRAIN_PLAINS", None, "Spain Rio Tinto Historic Copper"),
    (79, 61):  ("BONUS_WINE", "2", "TERRAIN_PLAINS", None, "Spain Andalusia Jerez Olive & Wine"),
    (89, 64):  ("BONUS_WHEAT", "2", "TERRAIN_GRASS", None, "Italy Po Valley Breadbasket Wheat"),
    (90, 62):  ("BONUS_MARBLE", "1", "TERRAIN_GRASS", None, "Italy Carrara Marble"),
    (91, 82):  ("BONUS_IRON", "1", "TERRAIN_TUNDRA", None, "Sweden Kiruna Giant Magnetite Iron"),
    (84, 80):  ("BONUS_FISH", "3", "TERRAIN_COAST", None, "Norway Bergen Cod Fishery"),
    (103, 65): ("BONUS_WHEAT", "2", "TERRAIN_PLAINS", None, "Ukraine Dnieper Chornozem Black Soil Wheat"),
    (105, 65): ("BONUS_COAL", "2", "TERRAIN_PLAINS", None, "Ukraine Donbas Coal Basin"),
    (104, 64): ("BONUS_IRON", "1", "TERRAIN_PLAINS", None, "Ukraine Kryvyi Rih Iron Ore"),
    (98, 64):  ("BONUS_OIL", "2", "TERRAIN_PLAINS", None, "Romania Ploiesti Historic Oil Field"),
    (115, 60): ("BONUS_OIL", "2", "TERRAIN_PLAINS", None, "Azerbaijan Baku Historic Oil Basin"),
    (117, 74): ("BONUS_OIL", "2", "TERRAIN_TUNDRA", "FeatureType=FEATURE_FOREST, FeatureVariety=0", "Russia West Siberia Tyumen Oil Field"),

    # ==================== 8. MIDDLE EAST (中東) ====================
    (113, 49): ("BONUS_OIL", "2", "TERRAIN_DESERT", None, "Saudi Arabia Ghawar Super Giant Oil Field"),
    (114, 53): ("BONUS_OIL", "2", "TERRAIN_DESERT", None, "Kuwait Burgan Oil Field"),
    (113, 55): ("BONUS_WHEAT", "2", "TERRAIN_PLAINS", None, "Mesopotamia Fertile Crescent Euphrates Wheat"),
    (114, 56): ("BONUS_OIL", "2", "TERRAIN_DESERT", None, "Iraq Kirkuk Giant Oil Field"),
    (117, 54): ("BONUS_OIL", "2", "TERRAIN_DESERT", None, "Iran Ahvaz Oil Field"),
    (110, 43): ("BONUS_INCENSE", "2", "TERRAIN_DESERT", None, "Southern Arabia Frankincense Trail"),

    # ==================== 9. AFRICA (非洲) ====================
    (100, 48): ("BONUS_WHEAT", "2", "TERRAIN_DESERT", "FeatureType=FEATURE_FLOOD_PLAINS, FeatureVariety=0", "Egypt Nile Delta Wheat"),
    (97, 48):  ("BONUS_WHEAT", "2", "TERRAIN_DESERT", "FeatureType=FEATURE_FLOOD_PLAINS, FeatureVariety=0", "Egypt Nile Delta Ancient Mediterranean Breadbasket Wheat"),
    (79, 56):  ("BONUS_COPPER", "1", "TERRAIN_DESERT", None, "Morocco Atlas Mountains Copper"),
    (84, 40):  ("BONUS_GOLD", "1", "TERRAIN_PLAINS", None, "Ghana Gold Coast Ashanti Mines"),
    (90, 37):  ("BONUS_OIL", "2", "TERRAIN_GRASS", "FeatureType=FEATURE_JUNGLE, FeatureVariety=0", "Nigeria Niger Delta Oil"),
    (96, 25):  ("BONUS_COPPER", "1", "TERRAIN_PLAINS", None, "DR Congo Katanga Copperbelt"),
    (95, 17):  ("BONUS_GOLD", "1", "TERRAIN_PLAINS", None, "South Africa Witwatersrand Gold Reef"),
    (96, 18):  ("BONUS_GEMS", "1", "TERRAIN_PLAINS", None, "South Africa Kimberley Diamond Pipes"),
    (97, 17):  ("BONUS_COAL", "2", "TERRAIN_PLAINS", None, "South Africa Transvaal Coal Basin"),
    (93, 14):  ("BONUS_WINE", "2", "TERRAIN_PLAINS", None, "South Africa Stellenbosch Wine"),
    (107, 39): ("BONUS_SPICES", "2", "TERRAIN_GRASS", "FeatureType=FEATURE_FOREST, FeatureVariety=0", "Ethiopia Kaffa Highland Coffee"),
    (106, 34): ("BONUS_COW", "2", "TERRAIN_PLAINS", None, "East Africa Serengeti / Kenya Pastures"),
}

# Isolated Islands: ensure Settleable Hills (PlotType=1) and appropriate Resources
# Seafood items: (island_x, island_y, bonus, (water_x, water_y))
ISLAND_SEAFOOD_OVERHAUL = [
    # Atlantic Islands Seafood
    (71, 52, "BONUS_FISH", (72, 52)),    # Azores
    (70, 50, "BONUS_FISH", (69, 50)),    # Madeira
    (71, 47, "BONUS_FISH", (71, 46)),    # Canary Islands
    (68, 41, "BONUS_FISH", (68, 40)),    # Cape Verde
    (79, 28, "BONUS_FISH", (80, 28)),    # Ascension
    (83, 23, "BONUS_FISH", (84, 23)),    # Saint Helena
    (53, 11, "BONUS_WHALE", (54, 11)),   # Falkland Islands
    (61, 8,  "BONUS_WHALE", (62, 8)),    # South Georgia
    (72, 79, "BONUS_FISH", (73, 79)),    # Iceland South Coast
    (90, 88, "BONUS_WHALE", (91, 88)),   # Svalbard Spitsbergen Whales

    # Indian Ocean Islands Seafood
    (115, 23, "BONUS_FISH", (116, 23)),  # Madagascar East Coast
    (121, 23, "BONUS_FISH", (122, 23)),  # Mauritius / Reunion
    (117, 31, "BONUS_FISH", (118, 31)),  # Seychelles
    (124, 40, "BONUS_FISH", (124, 39)),  # Maldives
    (123, 7,  "BONUS_WHALE", (124, 7)),  # Kerguelen Subantarctic Whales

    # Pacific Islands Seafood
    (9, 50,  "BONUS_FISH", (9, 51)),     # Hawaii Oahu / Honolulu
    (2, 24,  "BONUS_FISH", (2, 25)),     # Tahiti / French Polynesia
    (178, 33, "BONUS_FISH", (177, 33)),  # Fiji
    (168, 44, "BONUS_FISH", (167, 44)),  # Guam / Marianas
    (43, 37, "BONUS_FISH", (42, 37)),    # Galapagos Islands
]

# Island Land Resources (placed directly on island hills/land)
# Format: (X, Y, Bonus, PlotType, TerrainType)
ISLAND_LAND_RESOURCES = [
    (10, 49, "BONUS_SUGAR", "1", "TERRAIN_GRASS"),    # Hawaii Big Island Cane
    (70, 81, "BONUS_SILVER", "1", "TERRAIN_TUNDRA"),  # Iceland Highland Silver/Geothermal
    (112, 22, "BONUS_IRON", "1", "TERRAIN_GRASS"),    # Madagascar Highland Iron
    (172, 34, "BONUS_SPICES", "1", "TERRAIN_GRASS"),  # Solomon Islands Spices
]

# 43 Historical Indigenous Tribal Villages mapped to 180x90
GOODY_HUTS_180 = [
    # Australia & New Zealand
    (151, 22), (153, 18), (158, 20), (160, 21), (160, 26),
    (165, 24), (167, 20), (168, 11), (174, 8), (177, 11),
    # North America
    (32, 61), (33, 58), (17, 65), (22, 73), (16, 74),
    (23, 57), (26, 54), (36, 69), (30, 70),
    # South America
    (51, 33), (48, 30), (49, 15), (45, 12), (52, 23), (57, 25),
    # Siberia & Steppes
    (128, 74), (139, 77), (150, 74), (161, 69), (171, 73), (118, 64), (125, 64),
    # Sub-Saharan Africa
    (96, 28), (93, 30), (96, 19), (97, 17), (94, 41), (87, 41), (107, 21),
    # Southeast Asia & Pacific Islands
    (158, 32), (168, 32), (151, 36), (161, 36)
]

def build_ultra_map():
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
    src_rivers = []

    for p in plots_raw:
        lines = [l.strip() for l in p.splitlines()]
        coords = [l for l in lines if l.startswith("x=")][0].split(",")
        x = int(coords[0].split("=")[1])
        y = int(coords[1].split("=")[1])
        pt = [l for l in lines if l.startswith("PlotType=")][0].split("=")[1]
        tt = [l for l in lines if l.startswith("TerrainType=")][0].split("=")[1]
        b = [l for l in lines if l.startswith("BonusType=")]
        f = [l for l in lines if l.startswith("FeatureType=")]
        rn = "isNOfRiver" in lines
        rw = "isWOfRiver" in lines
        rwe = [int(l.split("=")[1]) for l in lines if l.startswith("RiverWEDirection=")]
        rns = [int(l.split("=")[1]) for l in lines if l.startswith("RiverNSDirection=")]

        src_grid[(x, y)] = {
            "pt": pt, "tt": tt,
            "f": f[0] if f else None,
            "rn": rn, "rw": rw,
            "rwe": rwe[0] if rwe else 0,
            "rns": rns[0] if rns else 0,
        }
        if b:
            src_bonuses.append((x, y, b[0].split("=")[1]))

    # 2. Build target 180x90 grid
    tgt_grid = {}
    for Y in range(H_TGT):
        for X in range(W_TGT):
            xs = min(W_SRC - 1, max(0, int(round(X * rx))))
            ys = min(H_SRC - 1, max(0, int(round(Y * ry))))
            sp = src_grid[(xs, ys)]
            tgt_grid[(X, Y)] = {
                "pt": sp["pt"],
                "tt": sp["tt"],
                "f": sp["f"],
                "rn": False, "rw": False,
                "rwe": 0, "rns": 0,
                "b": None,
                "imp": None,
                "sp": False
            }

    # 2.5 Australia Desert Reduction (縮減最左邊西澳與下方南澳沙漠，利於建城開拓)
    for Y in range(12, 27):
        for X in range(148, 175):
            p = tgt_grid.get((X, Y))
            if not p or p["pt"] == "3": continue
            # 1. West Australia (Left edge: X: 149..155, Y: 18..25)
            if 149 <= X <= 155 and 18 <= Y <= 25:
                if p["tt"] == "TERRAIN_DESERT":
                    p["tt"] = "TERRAIN_GRASS" if X <= 151 else "TERRAIN_PLAINS"
            # 2. South Australia (Bottom: X: 154..166, Y: 16..19)
            if 154 <= X <= 166 and 16 <= Y <= 19:
                if p["tt"] == "TERRAIN_DESERT":
                    p["tt"] = "TERRAIN_GRASS" if Y <= 17 else "TERRAIN_PLAINS"

    # 2.8 Australia East Grassland Expansion (原定台北/雪梨正上方 170, 24 與 171, 24 之上方新增兩格草原)
    tgt_grid[(170, 25)]["pt"] = "2"
    tgt_grid[(170, 25)]["tt"] = "TERRAIN_GRASS"
    tgt_grid[(170, 25)]["f"] = None
    tgt_grid[(171, 25)]["pt"] = "2"
    tgt_grid[(171, 25)]["tt"] = "TERRAIN_GRASS"
    tgt_grid[(171, 25)]["f"] = None

    # 3. Topographical Sculpting: Taiwan Island & Straits
    # Clear Taiwan Strait: X: 151..153, Y: 41..47 except Penghu (152, 44)
    for ty in range(41, 48):
        for tx in range(151, 154):
            if (tx, ty) != (152, 44):
                tgt_grid[(tx, ty)]["pt"] = "3"
                tgt_grid[(tx, ty)]["tt"] = "TERRAIN_COAST"
                tgt_grid[(tx, ty)]["f"] = None

    # Clear East Pacific waters around Taiwan: X: 156..157, Y: 41..47
    for ty in range(41, 48):
        for tx in range(156, 158):
            if (tx, ty) not in [(156, 45), (156, 43)]:
                tgt_grid[(tx, ty)]["pt"] = "3"
                tgt_grid[(tx, ty)]["tt"] = "TERRAIN_COAST"
                tgt_grid[(tx, ty)]["f"] = None

    # Straits Isolation across the Globe
    # Korea - Japan Strait:
    for ty in range(60, 64):
        tgt_grid[(159, ty)]["pt"] = "3"
        tgt_grid[(159, ty)]["tt"] = "TERRAIN_COAST"
        tgt_grid[(160, ty)]["pt"] = "3"
        tgt_grid[(160, ty)]["tt"] = "TERRAIN_COAST"

    # English Channel:
    for tx in range(81, 85):
        if tgt_grid[(tx, 69)]["pt"] != "3":
            tgt_grid[(tx, 69)]["pt"] = "3"
            tgt_grid[(tx, 69)]["tt"] = "TERRAIN_COAST"
            tgt_grid[(tx, 69)]["f"] = None

    # Bosphorus & Dardanelles (Connect Aegean Sea to Black Sea - Open Istanbul waterway)
    tgt_grid[(100, 60)]["pt"] = "3"
    tgt_grid[(100, 60)]["tt"] = "TERRAIN_COAST"
    tgt_grid[(100, 60)]["f"] = None

    # Strait of Hormuz (Clear passage into Persian Gulf)
    tgt_grid[(118, 50)]["pt"] = "3"
    tgt_grid[(118, 50)]["tt"] = "TERRAIN_COAST"

    # Ocean Barrier: Taiwan/China to Philippines
    for tx in range(152, 162):
        for ty in [39, 40]:
            if tgt_grid[(tx, ty)]["pt"] == "3":
                tgt_grid[(tx, ty)]["tt"] = "TERRAIN_OCEAN"

    # Ocean Barrier: Philippines to Indonesia
    for tx in range(153, 168):
        for ty in [32, 33]:
            if tgt_grid[(tx, ty)]["pt"] == "3":
                tgt_grid[(tx, ty)]["tt"] = "TERRAIN_OCEAN"

    # Ocean Barrier: Indonesia to Australia
    for tx in list(range(140, W_TGT)) + list(range(0, 25)):
        if tgt_grid[(tx, 27)]["pt"] == "3":
            tgt_grid[(tx, 27)]["tt"] = "TERRAIN_OCEAN"

    # 4. Map Rivers (Vertex-Preserving River Mapping: Continuous Flows Without Gaps)
    def map_vx(vx):
        return int(round(vx * W_TGT / W_SRC))

    def map_vy(vy):
        return int(round(vy * H_TGT / H_SRC))

    for p in tgt_grid.values():
        p["rn"] = False
        p["rw"] = False
        p["rwe"] = 0
        p["rns"] = 0

    for (sx, sy), sp in src_grid.items():
        if sp["rn"]:
            # Horizontal segment on North edge of (sx, sy): vertices (sx, sy+1) -> (sx+1, sy+1)
            tx1 = map_vx(sx)
            tx2 = map_vx(sx + 1)
            ty = map_vy(sy + 1)
            py = ty - 1
            if 0 <= py < H_TGT:
                for px in range(tx1, tx2):
                    tgt_grid[(px % W_TGT, py)]["rn"] = True
                    tgt_grid[(px % W_TGT, py)]["rwe"] = sp["rwe"]
        if sp["rw"]:
            # Vertical segment on West edge of (sx, sy): vertices (sx, sy) -> (sx, sy+1)
            tx = map_vx(sx)
            ty1 = map_vy(sy)
            ty2 = map_vy(sy + 1)
            px = tx % W_TGT
            for py in range(ty1, ty2):
                if 0 <= py < H_TGT:
                    tgt_grid[(px, py)]["rw"] = True
                    tgt_grid[(px, py)]["rns"] = sp["rns"]

    # 4.2 Major World Rivers Flow & Estuary Healing (尼羅河、長江、黃河、密西西比河等完整貫通)
    # 1. Nile River (Lake Victoria to Alexandria / Mediterranean)
    for ny in range(41, 50):
        tgt_grid[(100, ny)]["rw"] = True
        tgt_grid[(100, ny)]["rns"] = 0  # Northbound flow to Mediterranean
    tgt_grid[(100, 48)]["rn"] = True
    tgt_grid[(100, 48)]["rwe"] = 1  # Delta fork

    # 2. Yangtze River (Sichuan Basin to East China Sea / Shanghai)
    for nx in range(141, 149):
        tgt_grid[(nx, 57)]["rn"] = True
        tgt_grid[(nx, 57)]["rwe"] = 1  # Eastbound flow
    tgt_grid[(148, 57)]["rw"] = True
    tgt_grid[(148, 57)]["rns"] = 2

    # 3. Yellow River (Qinghai / Ordos to Bohai Sea)
    for nx in range(143, 148):
        tgt_grid[(nx, 61)]["rn"] = True
        tgt_grid[(nx, 61)]["rwe"] = 1
    tgt_grid[(147, 61)]["rw"] = True
    tgt_grid[(147, 61)]["rns"] = 0

    # 4. Danube River (Central Europe to Black Sea)
    for nx in range(91, 100):
        tgt_grid[(nx, 63)]["rn"] = True
        tgt_grid[(nx, 63)]["rwe"] = 1

    # 5. Mississippi River (North America Heartland to Gulf of Mexico)
    for ny in range(56, 64):
        tgt_grid[(34, ny)]["rw"] = True
        tgt_grid[(34, ny)]["rns"] = 2  # Southbound flow into Gulf of Mexico

    # 4.5 Add Realistic Taiwan & Australia River Networks
    # 1. Tamsui & Keelung Rivers (淡水河水系：流經台北 154, 45 與基隆 155, 45 北流入海)
    tgt_grid[(155, 45)]["rw"] = True
    tgt_grid[(155, 45)]["rns"] = 0  # 基隆河/新店溪匯流
    tgt_grid[(154, 45)]["rn"] = True
    tgt_grid[(154, 45)]["rwe"] = 1  # 台北淡水河出海口

    # 2. Choshui River (濁水溪：橫貫中央山脈 155, 44 與中南部 154, 44 西流入海)
    tgt_grid[(155, 44)]["rw"] = True
    tgt_grid[(155, 44)]["rns"] = 2
    tgt_grid[(154, 44)]["rn"] = True
    tgt_grid[(154, 44)]["rwe"] = 1  # 濁水溪西流入台灣海峽

    # 3. Australia Sydney Hawkesbury River (雪梨霍克斯伯里河水系，提供開局淡水)
    tgt_grid[(171, 21)]["rn"] = True
    tgt_grid[(171, 21)]["rwe"] = 1
    tgt_grid[(171, 21)]["rw"] = True
    tgt_grid[(171, 21)]["rns"] = 0

    # 4. Australia Southeast Murray / Melbourne River (澳洲右下偏中河流向右移一格至 X=164 並向下入海)
    tgt_grid[(162, 15)]["rw"] = False
    tgt_grid[(162, 16)]["rw"] = False
    for r_y in range(14, 18):
        tgt_grid[(164, r_y)]["rw"] = True
        tgt_grid[(164, r_y)]["rns"] = 2  # 向南奔流注入巴斯海峽海洋
    tgt_grid[(164, 18)]["rn"] = True
    tgt_grid[(164, 18)]["rwe"] = 1  # 內陸水系匯入

    # 5. Australia East Brisbane / Fitzroy River (原台北/雪梨正上方甘蔗與新增兩格草原 170, 25 與 171, 25 之河流延伸北流入海)
    tgt_grid[(171, 22)]["rw"] = True
    tgt_grid[(171, 22)]["rns"] = 0
    tgt_grid[(171, 23)]["rw"] = True
    tgt_grid[(171, 23)]["rns"] = 0
    tgt_grid[(171, 24)]["rw"] = True
    tgt_grid[(171, 24)]["rns"] = 0
    tgt_grid[(171, 25)]["rw"] = True
    tgt_grid[(171, 25)]["rns"] = 0  # 北流穿過兩格新草原
    tgt_grid[(171, 25)]["rn"] = True
    tgt_grid[(171, 25)]["rwe"] = 1  # 於 Y=25 北側直接流入珊瑚海海洋

    # 4.8 Canyon Peak-Trapped River Relief (消除被兩座絕壁山峰夾住的河流，微調一側為壯麗峽谷丘陵)
    for (x, y), p in tgt_grid.items():
        if p["rn"]:
            p_north = tgt_grid.get((x, y + 1))
            if p_north and p["pt"] == "0" and p_north["pt"] == "0":
                p["pt"] = "1"
        if p["rw"]:
            p_west = tgt_grid.get(((x - 1) % W_TGT, y))
            if p_west and p["pt"] == "0" and p_west["pt"] == "0":
                p_west["pt"] = "1"

    # 5. Base Resource Scaling
    WATER_BONUSES = {'BONUS_FISH', 'BONUS_CLAM', 'BONUS_CRAB', 'BONUS_WHALE'}
    land_plots = {coord for coord, p in tgt_grid.items() if p["pt"] in ["1", "2"]}
    bfc_offsets = [(dx, dy) for dx in range(-2, 3) for dy in range(-2, 3) if not (abs(dx) == 2 and abs(dy) == 2)]

    for sx, sy, b_name in src_bonuses:
        TX = int(round(sx / rx))
        TY = int(round(sy / ry))
        if b_name in WATER_BONUSES:
            best_cand = None
            min_d2 = 999999
            for r in range(0, 6):
                for dx in range(-r, r + 1):
                    for dy in range(-r, r + 1):
                        nx, ny = (TX + dx) % W_TGT, TY + dy
                        if 0 <= ny < H_TGT and tgt_grid[(nx, ny)]["pt"] == "3" and not tgt_grid[(nx, ny)]["b"]:
                            if any(((nx - bx) % W_TGT, ny - by) in land_plots for bx, by in bfc_offsets):
                                d2 = dx * dx + dy * dy
                                if d2 < min_d2:
                                    min_d2 = d2
                                    best_cand = (nx, ny)
                if best_cand: break
            if best_cand:
                tgt_grid[best_cand]["b"] = b_name
                tgt_grid[best_cand]["tt"] = "TERRAIN_COAST"
        else:
            if tgt_grid[(TX, TY)]["pt"] in ["1", "2"] and not tgt_grid[(TX, TY)]["b"]:
                tgt_grid[(TX, TY)]["b"] = b_name

    # 6. Apply Ultra Handcrafted Resources (Taiwan & Global)
    for (gx, gy), (b_type, req_pt, req_terr, req_feat, name) in ULTRA_GLOBAL_RESOURCES.items():
        if 0 <= gx < W_TGT and 0 <= gy < H_TGT:
            if req_pt: tgt_grid[(gx, gy)]["pt"] = req_pt
            if req_terr: tgt_grid[(gx, gy)]["tt"] = req_terr
            if req_feat is not None: tgt_grid[(gx, gy)]["f"] = req_feat
            tgt_grid[(gx, gy)]["b"] = b_type  # Sets bonus or clears if None

    # 7. Apply Island Seafood & Peak-to-Hills Overhaul
    for ix, iy, b_type, (tx, ty) in ISLAND_SEAFOOD_OVERHAUL:
        if 0 <= ix < W_TGT and 0 <= iy < H_TGT:
            if tgt_grid[(ix, iy)]["pt"] == "0":
                tgt_grid[(ix, iy)]["pt"] = "1"
        if 0 <= tx < W_TGT and 0 <= ty < H_TGT:
            tgt_grid[(tx, ty)]["pt"] = "3"
            tgt_grid[(tx, ty)]["tt"] = "TERRAIN_COAST"
            tgt_grid[(tx, ty)]["b"] = b_type

    # 7.5 Apply Island Land Resources (Hills/Land on Islands)
    for lx, ly, b_type, req_pt, req_terr in ISLAND_LAND_RESOURCES:
        if 0 <= lx < W_TGT and 0 <= ly < H_TGT:
            tgt_grid[(lx, ly)]["pt"] = req_pt
            tgt_grid[(lx, ly)]["tt"] = req_terr
            tgt_grid[(lx, ly)]["b"] = b_type

    # 7.8 Cartographic Oceanography & Coastline Smoothing (製圖學大陸棚平滑與海岸深淺層次修復)
    # Pass 1: Eliminate 1-tile isolated inland water puddles (surrounded by 8 land plots)
    for y in range(H_TGT):
        for x in range(W_TGT):
            p = tgt_grid[(x, y)]
            if p["pt"] == "3":
                land_neighbors = 0
                for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:
                        if dx == 0 and dy == 0: continue
                        nx, ny = (x + dx) % W_TGT, y + dy
                        if 0 <= ny < H_TGT and tgt_grid[(nx, ny)]["pt"] in ["0", "1", "2"]:
                            land_neighbors += 1
                if land_neighbors == 8:
                    p["pt"] = "2"
                    p["tt"] = "TERRAIN_PLAINS"
                    if p["b"] in WATER_BONUSES:
                        p["b"] = None

    # Pass 2: Continental Shelf Smoothing (Ensure ALL water plots adjacent to land are TERRAIN_COAST)
    for y in range(H_TGT):
        for x in range(W_TGT):
            p = tgt_grid[(x, y)]
            if p["pt"] == "3":
                adj_land = False
                for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:
                        if dx == 0 and dy == 0: continue
                        nx, ny = (x + dx) % W_TGT, y + dy
                        if 0 <= ny < H_TGT and tgt_grid[(nx, ny)]["pt"] in ["0", "1", "2"]:
                            adj_land = True
                            break
                    if adj_land: break
                if adj_land:
                    p["tt"] = "TERRAIN_COAST"

    # Pass 3: Deep Ocean Cleanup (Eliminate floating shallow coast in deep ocean with no land within 2 tiles)
    for y in range(H_TGT):
        for x in range(W_TGT):
            p = tgt_grid[(x, y)]
            if p["pt"] == "3" and p["tt"] == "TERRAIN_COAST" and not p["b"]:
                has_land = False
                for dx in range(-2, 3):
                    for dy in range(-2, 3):
                        nx, ny = (x + dx) % W_TGT, y + dy
                        if 0 <= ny < H_TGT and tgt_grid[(nx, ny)]["pt"] in ["0", "1", "2"]:
                            has_land = True
                            break
                    if has_land: break
                if not has_land:
                    p["tt"] = "TERRAIN_OCEAN"

    # 7.9 Strict Strategic Ocean Barriers (大航海時代前跨洋深海屏障體系，確保早期船隻無法跨洲偷渡)
    # 1. Australia / Oceania Isolation Barrier (澳洲與印尼/新幾內亞跨大洋隔離：帝汶海、托雷斯海峽深海槽)
    for x in list(range(140, W_TGT)) + list(range(0, 25)):
        for y in [27, 28]:
            p = tgt_grid.get((x, y))
            if p and p["pt"] == "3" and not p["b"]:
                p["tt"] = "TERRAIN_OCEAN"

    # 2. Indonesia to Philippines Barrier (西里伯斯海與密克羅尼西亞深海隔斷)
    for x in range(150, 178):
        for y in [32, 33]:
            p = tgt_grid.get((x, y))
            if p and p["pt"] == "3" and not p["b"]:
                p["tt"] = "TERRAIN_OCEAN"

    # 3. Philippines to Taiwan Barrier (巴士海峽/呂宋海峽深海隔斷)
    for x in range(150, 164):
        for y in [39, 40]:
            p = tgt_grid.get((x, y))
            if p and p["pt"] == "3" and not p["b"]:
                p["tt"] = "TERRAIN_OCEAN"

    # 4. Taiwan to Mainland China Trench (台灣海峽深水隔離，除澎湖 152, 44 與沿海一例外)
    for tx in [151, 153]:
        for ty in range(41, 48):
            p = tgt_grid.get((tx, ty))
            if p and p["pt"] == "3" and not p["b"]:
                p["tt"] = "TERRAIN_OCEAN"

    # 5. Southeast Asia Mainland to Borneo Barrier (南海深海盆地：越南/泰國至婆羅洲隔斷)
    for x in range(145, 156):
        for y in [34, 35]:
            p = tgt_grid.get((x, y))
            if p and p["pt"] == "3" and not p["b"]:
                p["tt"] = "TERRAIN_OCEAN"

    # 6. North America to Greenland Barrier (戴維斯海峽深海隔斷：巴芬島/拉布拉多至格陵蘭)
    for x in range(53, 62):
        for y in range(71, 80):
            p = tgt_grid.get((x, y))
            if p and p["pt"] == "3" and not p["b"]:
                p["tt"] = "TERRAIN_OCEAN"

    # 7. Greenland to Iceland Barrier (丹麥海峽深海隔斷：格陵蘭至冰島)
    for x in range(67, 72):
        for y in range(78, 86):
            p = tgt_grid.get((x, y))
            if p and p["pt"] == "3" and not p["b"]:
                p["tt"] = "TERRAIN_OCEAN"

    # 8. Africa to Madagascar Barrier (莫三比克海峽縱向深海槽)
    for y in range(17, 30):
        for x in range(107, 112):
            p = tgt_grid.get((x, y))
            if p and p["pt"] == "3" and not p["b"]:
                p["tt"] = "TERRAIN_OCEAN"

    # 9. Asia to America Bering Strait Barrier (白令海峽深海隔斷)
    for x in [178, 179, 0, 1]:
        for y in [76, 77]:
            p = tgt_grid.get((x, y))
            if p and p["pt"] == "3" and not p["b"]:
                p["tt"] = "TERRAIN_OCEAN"

    # 10. Japan to Korea Tsushima Strait Trench (對馬海峽深水隔斷)
    for ty in range(60, 64):
        for tx in [159, 160]:
            p = tgt_grid.get((tx, ty))
            if p and p["pt"] == "3" and not p["b"]:
                p["tt"] = "TERRAIN_OCEAN"

    # 11. Australia to New Zealand Tasman Sea (塔斯曼海廣闊深海隔斷)
    for x in range(172, 176):
        for y in range(11, 20):
            p = tgt_grid.get((x, y))
            if p and p["pt"] == "3" and not p["b"]:
                p["tt"] = "TERRAIN_OCEAN"

    # 8. Apply Tribal Villages (Goody Huts)
    for hx, hy in GOODY_HUTS_180:
        if 0 <= hx < W_TGT and 0 <= hy < H_TGT:
            if tgt_grid[(hx, hy)]["pt"] in ["1", "2"] and not tgt_grid[(hx, hy)]["sp"]:
                tgt_grid[(hx, hy)]["imp"] = "IMPROVEMENT_GOODY_HUT"

    # 9. Configure 18 Civilizations Starting Plots
    civ_coord_map = {
        "CIVILIZATION_EGYPT": (100, 49),
        "CIVILIZATION_INDIA": (131, 53),
        "CIVILIZATION_CHINA": (148, 62),
        "CIVILIZATION_TAIWAN": (171, 21),   # Taiwan Capital (Australia Sydney)
        "CIVILIZATION_ROME": (89, 61),
        "CIVILIZATION_PERSIA": (119, 53),
        "CIVILIZATION_JAPAN": (164, 60),
        "CIVILIZATION_GERMANY": (93, 69),
        "CIVILIZATION_MONGOL": (144, 68),
        "CIVILIZATION_FRANCE": (84, 68),
        "CIVILIZATION_ARABIA": (109, 46),
        "CIVILIZATION_VIKING": (90, 77),
        "CIVILIZATION_ENGLAND": (81, 70),
        "CIVILIZATION_RUSSIA": (106, 71),
        "CIVILIZATION_MALI": (80, 45),
        "CIVILIZATION_INCA": (44, 30),
        "CIVILIZATION_AZTEC": (28, 49),
        "CIVILIZATION_AMERICA": (41, 60),
    }

    tgt_civ_starts = {}
    for civ_name, (cx, cy) in civ_coord_map.items():
        if tgt_grid[(cx, cy)]["pt"] in ["0", "3"]:
            for d in [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (-1, -1)]:
                nx, ny = cx + d[0], cy + d[1]
                if tgt_grid.get((nx, ny), {}).get("pt") in ["1", "2"]:
                    cx, cy = nx, ny
                    break
        tgt_grid[(cx, cy)]["sp"] = True
        tgt_civ_starts[civ_name] = (cx, cy)

    # 10. Update WBSave Header
    new_header = header_part
    for civ_name, (tx, ty) in tgt_civ_starts.items():
        pattern = rf"(CivType={civ_name}.*?StartingX=)\d+(,\s*StartingY=)\d+"
        new_header = re.sub(pattern, rf"\g<1>{tx}\g<2>{ty}", new_header, flags=re.DOTALL)

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
            if p.get("imp"):
                lines.append(f"\tImprovementType={p['imp']}")
            lines.append(f"\tTerrainType={p['tt']}")
            lines.append(f"\tPlotType={p['pt']}")
            lines.append("EndPlot")
            plot_strings.append("\n".join(lines))

    final_wbsave = new_header + map_text + "\n".join(plot_strings) + "\n"

    # Save to Patch directory
    os.makedirs(os.path.dirname(OUTPUT_WBSAVE_PATCH), exist_ok=True)
    with open(OUTPUT_WBSAVE_PATCH, "w", encoding="utf-8", newline="\r\n") as f:
        f.write(final_wbsave)
    print(f"Saved ultra WBSave to: {OUTPUT_WBSAVE_PATCH}")

    # Deploy to Steam and My Games
    deploy_targets = [STEAM_BTS_MAPS, STEAM_ROOT_MAPS, USER_MY_GAMES_MAPS]
    for target_dir in deploy_targets:
        if os.path.exists(target_dir):
            target_file = os.path.join(target_dir, f"{MAP_NAME_DISPLAY}.CivBeyondSwordWBSave")
            with open(target_file, "w", encoding="utf-8", newline="\r\n") as f:
                f.write(final_wbsave)
            print(f"Deployed ultra WBSave to: {target_file}")

    return final_wbsave, plot_strings, tgt_grid, tgt_civ_starts

def build_py_script(tgt_grid, tgt_civ_starts):
    print("Formatting plot data for ultra Python map script...")
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
#   FILE:    The_Earth_Ultra.py
#   PURPOSE: Historically Researched 180x90 Ultra Earth Map for Civilization IV BTS
#            Features 18 Real-World Civilizations with Taiwan in Taiwan Island (Taipei)
#
from CvPythonExtensions import *
import CvUtil

MAP_WIDTH = {MAP_WIDTH}
MAP_HEIGHT = {MAP_HEIGHT}
NUM_PLOTS = {MAP_WIDTH * MAP_HEIGHT}

TERRAIN_LIST = {repr(TERRAIN_LIST)}
FEATURE_LIST = {repr(FEATURE_LIST)}
BONUS_LIST = {repr(BONUS_LIST)}

PLOT_TYPES_DATA = "{plot_types_str}"
TERRAIN_TYPES_DATA = "{terrain_types_str}"
RIVERS_DATA = {repr(rivers)}
FEATURES_DATA = {repr(features)}
BONUSES_DATA = {repr(bonuses)}

def getDescription():
    return "TXT_KEY_MAP_SCRIPT_THE_EARTH_ULTRA_DESCR"

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
    return (45, 22)

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
    CyPythonMgr().allowDefaultImpl()

def assignStartingPlots():
    gc = CyGlobalContext()
    cy_map = CyMap()

    civ_coords = {{
        "CIVILIZATION_TAIWAN": {repr(tgt_civ_starts.get("CIVILIZATION_TAIWAN", (171, 21)))},
        "CIVILIZATION_CHINA": {repr(tgt_civ_starts.get("CIVILIZATION_CHINA", (148, 62)))},
        "CIVILIZATION_JAPAN": {repr(tgt_civ_starts.get("CIVILIZATION_JAPAN", (164, 60)))},
        "CIVILIZATION_INDIA": {repr(tgt_civ_starts.get("CIVILIZATION_INDIA", (131, 53)))},
        "CIVILIZATION_EGYPT": {repr(tgt_civ_starts.get("CIVILIZATION_EGYPT", (100, 49)))},
        "CIVILIZATION_ROME": {repr(tgt_civ_starts.get("CIVILIZATION_ROME", (89, 61)))},
        "CIVILIZATION_GERMANY": {repr(tgt_civ_starts.get("CIVILIZATION_GERMANY", (93, 69)))},
        "CIVILIZATION_FRANCE": {repr(tgt_civ_starts.get("CIVILIZATION_FRANCE", (84, 68)))},
        "CIVILIZATION_ENGLAND": {repr(tgt_civ_starts.get("CIVILIZATION_ENGLAND", (81, 70)))},
        "CIVILIZATION_SPAIN": (80, 61),
        "CIVILIZATION_RUSSIA": {repr(tgt_civ_starts.get("CIVILIZATION_RUSSIA", (106, 71)))},
        "CIVILIZATION_PERSIA": {repr(tgt_civ_starts.get("CIVILIZATION_PERSIA", (119, 53)))},
        "CIVILIZATION_ARABIA": {repr(tgt_civ_starts.get("CIVILIZATION_ARABIA", (109, 46)))},
        "CIVILIZATION_MONGOL": {repr(tgt_civ_starts.get("CIVILIZATION_MONGOL", (144, 68)))},
        "CIVILIZATION_MALI": {repr(tgt_civ_starts.get("CIVILIZATION_MALI", (80, 45)))},
        "CIVILIZATION_AMERICA": {repr(tgt_civ_starts.get("CIVILIZATION_AMERICA", (41, 60)))},
        "CIVILIZATION_AZTEC": {repr(tgt_civ_starts.get("CIVILIZATION_AZTEC", (28, 49)))},
        "CIVILIZATION_INCA": {repr(tgt_civ_starts.get("CIVILIZATION_INCA", (44, 30)))},
        "CIVILIZATION_BABYLON": (114, 55),
        "CIVILIZATION_BYZANTIUM": (100, 60),
        "CIVILIZATION_CARTHAGE": (87, 54),
        "CIVILIZATION_CELT": (80, 74),
        "CIVILIZATION_ETHIOPIA": (107, 39),
        "CIVILIZATION_KHMER": (144, 46),
        "CIVILIZATION_KOREA": (158, 63),
        "CIVILIZATION_MAYA": (25, 48),
        "CIVILIZATION_NATIVE_AMERICA": (30, 65),
        "CIVILIZATION_NETHERLANDS": (86, 70),
        "CIVILIZATION_OTTOMAN": (102, 59),
        "CIVILIZATION_PORTUGAL": (75, 60),
        "CIVILIZATION_SUMERIA": (116, 52),
        "CIVILIZATION_VIKING": {repr(tgt_civ_starts.get("CIVILIZATION_VIKING", (90, 77)))},
        "CIVILIZATION_ZULU": (97, 16),
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

    fallback_plots = list(civ_coords.values())
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

    os.makedirs(os.path.dirname(OUTPUT_PY_PATCH), exist_ok=True)
    with open(OUTPUT_PY_PATCH, "w", encoding="utf-8", newline="\r\n") as f:
        f.write(py_content)
    print(f"Saved ultra Python map script to: {OUTPUT_PY_PATCH}")

    deploy_targets = [STEAM_BTS_MAPS, STEAM_ROOT_MAPS, USER_MY_GAMES_MAPS]
    for target_dir in deploy_targets:
        if os.path.exists(target_dir):
            target_file = os.path.join(target_dir, "The_Earth_Ultra.py")
            with open(target_file, "w", encoding="utf-8", newline="\r\n") as f:
                f.write(py_content)
            print(f"Deployed ultra Python map script to: {target_file}")

if __name__ == "__main__":
    final_wbsave, plot_strings, tgt_grid, tgt_civ_starts = build_ultra_map()
    build_py_script(tgt_grid, tgt_civ_starts)
    print("All tasks completed successfully!")
