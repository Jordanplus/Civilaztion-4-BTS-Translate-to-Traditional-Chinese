import os
import xml.etree.ElementTree as ET

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def to_entities(s):
    return ''.join(f'&#{ord(c)};' if ord(c) > 127 else c for c in s)

def update_game_text():
    name_en = "YF-23 Stealth Fighter"
    name_cn = to_entities("YF-23 隱形戰鬥機")

    pedia_en = ('The Northrop/McDonnell Douglas YF-23 (unofficially nicknamed "Black Widow II" '
                'and "Gray Ghost") was an American fifth-generation stealth fighter technology demonstrator '
                'for the United States Air Force ATF program. Featuring advanced diamond wings and V-tails, '
                'it delivered unprecedented stealth, supercruise speed, and long-range combat capabilities.'
                '[NEWLINE][NEWLINE]In Civilization IV, the YF-23 is the unique unit for America, replacing '
                'the Jet Fighter. It features 28 air combat strength, 12 air range, 2 first strikes, '
                'and a 50% evasion rate against anti-air defenses.')

    pedia_cn_raw = ('[H1]YF-23 隱形戰鬥機[\\H1][NEWLINE][BOLD]黑寡婦匿蹤魅影：[\\BOLD][NEWLINE]'
                    '諾斯洛普／麥道 YF-23（代號「黑寡婦二式」Black Widow II 與「灰色幽靈」Gray Ghost）'
                    '是美國空軍先進戰術戰鬥機（ATF）計畫的五代匿蹤空優原型機。採用極具前瞻性的菱形主翼、'
                    'V型全動外傾垂尾與深埋機身進氣道設計，展現出極致的雷達隱形、卓越的超音速巡航能力與頂級長程打擊性能，'
                    '被譽為軍事航空史上最優雅且強悍的隱形戰機之一。[NEWLINE][NEWLINE]'
                    '在《文明帝國 IV》中，YF-23 隱形戰鬥機為美國專屬特色單位，取代噴射戰鬥機。空中戰鬥力提升至 28'
                    '（提升近 17%），巡航作戰半徑延伸至 12 格，自帶 2 次先發制人打擊優勢；更額外繼承了五代匿蹤基因，'
                    '享有高達 50% 規避敵軍防空防禦與截擊的匿蹤突防機率，能神出鬼沒地撕裂防空網並主宰現代空戰！')
    pedia_cn = to_entities(pedia_cn_raw)

    strat_en = ('The YF-23 Stealth Fighter is a unique unit for the American civilization, replacing '
                'the Jet Fighter. It boasts 28 air combat strength, 12 air range, 2 first strikes, and '
                'a 50% evasion rate against anti-air interceptions, ruling the skies with unmatched stealth dominance.')

    strat_cn_raw = ('YF-23 隱形戰鬥機是美國的專屬特色單位，取代噴射戰鬥機。具備高達 28 點空中戰力、12 格遠程'
                    '作戰半徑、2 次先發打擊優勢，並擁有 50% 規避防空攔截之隱形能力，是現代戰場掌控絕對制空權的終極空中王牌。')
    strat_cn = to_entities(strat_cn_raw)

    xml_content = f'''<?xml version="1.0" encoding="ISO-8859-1"?>
<!-- Sid Meier's Civilization 4 Beyond the Sword -->
<!-- American Civilization Expansion Game Text -->
<Civ4GameText xmlns="http://www.firaxis.com">
\t<TEXT>
\t\t<Tag>TXT_KEY_UNIT_AMERICAN_YF23</Tag>
\t\t<English>{name_en}</English>
\t\t<French>{name_cn}</French>
\t\t<German/>
\t\t<Italian/>
\t\t<Spanish/>
\t\t<Chinese>{name_cn}</Chinese>
\t</TEXT>
\t<TEXT>
\t\t<Tag>TXT_KEY_UNIT_AMERICAN_YF23_PEDIA</Tag>
\t\t<English>{pedia_en}</English>
\t\t<French>{pedia_cn}</French>
\t\t<German/>
\t\t<Italian/>
\t\t<Spanish/>
\t\t<Chinese>{pedia_cn}</Chinese>
\t</TEXT>
\t<TEXT>
\t\t<Tag>TXT_KEY_UNIT_AMERICAN_YF23_STRATEGY</Tag>
\t\t<English>{strat_en}</English>
\t\t<French>{strat_cn}</French>
\t\t<German/>
\t\t<Italian/>
\t\t<Spanish/>
\t\t<Chinese>{strat_cn}</Chinese>
\t</TEXT>
</Civ4GameText>
'''

    text_targets = [
        os.path.join(ROOT, 'src', 'bts', 'CIV4GameText_America.xml'),
        os.path.join(ROOT, 'patch', 'PatchFiles', 'Beyond the Sword', 'Assets', 'XML', 'Text', 'CIV4GameText_America.xml')
    ]
    for path in text_targets:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(xml_content)
        print(f"Created {path}")

def update_art_defines():
    art_def_entry = '''\t\t<UnitArtInfo>
\t\t\t<Type>ART_DEF_UNIT_AMERICAN_YF23</Type>
\t\t\t<Button>Art/Interface/Buttons/Units/american_yf23.dds</Button>
\t\t\t<fScale>0.48</fScale>
\t\t\t<fInterfaceScale>1.0</fInterfaceScale>
\t\t\t<bActAsLand>0</bActAsLand>
\t\t\t<bActAsAir>0</bActAsAir>
\t\t\t<NIF>Art/Units/American_YF23/f23.nif</NIF>
\t\t\t<KFM>Art/Units/JetFighter/JetFighter.kfm</KFM>
\t\t\t<SHADERNIF>Art/Units/American_YF23/f23.nif</SHADERNIF>
\t\t\t<ShadowDef>
\t\t\t\t<ShadowNIF>Art/Units/01_UnitShadows/JetFighterShadow.nif</ShadowNIF>
\t\t\t\t<ShadowAttachNode>BIP Pelvis</ShadowAttachNode>
\t\t\t\t<fShadowScale>0.75</fShadowScale>
\t\t\t</ShadowDef>
\t\t\t<iDamageStates>4</iDamageStates>
\t\t\t<fBattleDistance>0.35</fBattleDistance>
\t\t\t<fRangedDeathTime>0.31</fRangedDeathTime>
\t\t\t<bSmoothMove>1</bSmoothMove>
\t\t\t<fBankRate>0.35</fBankRate>
\t\t\t<bActAsRanged>0</bActAsRanged>
\t\t\t<TrainSound>AS2D_UNIT_BUILD_UNIT</TrainSound>
\t\t\t<AudioRunSounds>
\t\t\t\t<AudioRunTypeLoop/>
\t\t\t\t<AudioRunTypeEnd/>
\t\t\t</AudioRunSounds>
\t\t\t<PatrolSound>AS3D_UN_JET_PATROL</PatrolSound>
\t\t\t<SelectionSound>AS3D_UN_JET_COMMAND_PATROL</SelectionSound>
\t\t\t<ActionSound>AS3D_UN_JET_COMMAND_PATROL</ActionSound>
\t\t</UnitArtInfo>
\t</UnitArtInfos>
</Civ4ArtDefines>
'''
    art_targets = [
        os.path.join(ROOT, 'src', 'bts', 'CIV4ArtDefines_Unit.xml'),
        os.path.join(ROOT, 'patch', 'PatchFiles', 'Beyond the Sword', 'Assets', 'XML', 'Art', 'CIV4ArtDefines_Unit.xml')
    ]
    for path in art_targets:
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        if 'ART_DEF_UNIT_AMERICAN_YF23' in content:
            print(f"Already in {path}")
            continue
        content = content.replace('\t</UnitArtInfos>\n</Civ4ArtDefines>', art_def_entry)
        content = content.replace('</UnitArtInfos>\n</Civ4ArtDefines>', art_def_entry)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated {path}")

def update_civilization_infos():
    unit_entry = '''\t\t\t\t<Unit>
\t\t\t\t\t<UnitClassType>UNITCLASS_JET_FIGHTER</UnitClassType>
\t\t\t\t\t<UnitType>UNIT_AMERICAN_YF23</UnitType>
\t\t\t\t</Unit>
\t\t\t</Units>'''
    civ_targets = [
        os.path.join(ROOT, 'src', 'bts', 'CIV4CivilizationInfos.xml'),
        os.path.join(ROOT, 'patch', 'PatchFiles', 'Beyond the Sword', 'Assets', 'XML', 'Civilizations', 'CIV4CivilizationInfos.xml')
    ]
    for path in civ_targets:
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        if 'UNIT_AMERICAN_YF23' in content:
            print(f"Already in {path}")
            continue
        target_str = '''\t\t\t\t<Unit>
\t\t\t\t\t<UnitClassType>UNITCLASS_MARINE</UnitClassType>
\t\t\t\t\t<UnitType>UNIT_AMERICAN_NAVY_SEAL</UnitType>
\t\t\t\t</Unit>
\t\t\t</Units>'''
        if target_str in content:
            content = content.replace(target_str, f'''\t\t\t\t<Unit>
\t\t\t\t\t<UnitClassType>UNITCLASS_MARINE</UnitClassType>
\t\t\t\t\t<UnitType>UNIT_AMERICAN_NAVY_SEAL</UnitType>
\t\t\t\t</Unit>
{unit_entry}''')
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Updated {path}")
        else:
            print(f"ERROR: Target string not found in {path}")

def update_unit_infos():
    unit_info_xml = '''\t\t<UnitInfo>
\t\t\t<Class>UNITCLASS_JET_FIGHTER</Class>
\t\t\t<Type>UNIT_AMERICAN_YF23</Type>
\t\t\t<UniqueNames/>
\t\t\t<Special>SPECIALUNIT_FIGHTER</Special>
\t\t\t<Capture>NONE</Capture>
\t\t\t<Combat>UNITCOMBAT_AIR</Combat>
\t\t\t<Domain>DOMAIN_AIR</Domain>
\t\t\t<DefaultUnitAI>UNITAI_DEFENSE_AIR</DefaultUnitAI>
\t\t\t<Invisible>NONE</Invisible>
\t\t\t<SeeInvisible>NONE</SeeInvisible>
\t\t\t<Description>TXT_KEY_UNIT_AMERICAN_YF23</Description>
\t\t\t<Civilopedia>TXT_KEY_UNIT_AMERICAN_YF23_PEDIA</Civilopedia>
\t\t\t<Strategy>TXT_KEY_UNIT_AMERICAN_YF23_STRATEGY</Strategy>
\t\t\t<Advisor>ADVISOR_MILITARY</Advisor>
\t\t\t<bAnimal>0</bAnimal>
\t\t\t<bFood>0</bFood>
\t\t\t<bNoBadGoodies>0</bNoBadGoodies>
\t\t\t<bOnlyDefensive>0</bOnlyDefensive>
\t\t\t<bNoCapture>0</bNoCapture>
\t\t\t<bQuickCombat>0</bQuickCombat>
\t\t\t<bRivalTerritory>0</bRivalTerritory>
\t\t\t<bMilitaryHappiness>0</bMilitaryHappiness>
\t\t\t<bMilitarySupport>1</bMilitarySupport>
\t\t\t<bMilitaryProduction>1</bMilitaryProduction>
\t\t\t<bPillage>0</bPillage>
\t\t\t<bSpy>0</bSpy>
\t\t\t<bSabotage>0</bSabotage>
\t\t\t<bDestroy>0</bDestroy>
\t\t\t<bStealPlans>0</bStealPlans>
\t\t\t<bInvestigate>0</bInvestigate>
\t\t\t<bCounterSpy>0</bCounterSpy>
\t\t\t<bFound>0</bFound>
\t\t\t<bGoldenAge>0</bGoldenAge>
\t\t\t<bInvisible>0</bInvisible>
\t\t\t<bFirstStrikeImmune>0</bFirstStrikeImmune>
\t\t\t<bNoDefensiveBonus>0</bNoDefensiveBonus>
\t\t\t<bIgnoreBuildingDefense>1</bIgnoreBuildingDefense>
\t\t\t<bCanMoveImpassable>0</bCanMoveImpassable>
\t\t\t<bCanMoveAllTerrain>0</bCanMoveAllTerrain>
\t\t\t<bFlatMovementCost>0</bFlatMovementCost>
\t\t\t<bIgnoreTerrainCost>0</bIgnoreTerrainCost>
\t\t\t<bNukeImmune>0</bNukeImmune>
\t\t\t<bPrereqBonuses>0</bPrereqBonuses>
\t\t\t<bPrereqReligion>0</bPrereqReligion>
\t\t\t<bMechanized>1</bMechanized>
\t\t\t<bSuicide>0</bSuicide>
\t\t\t<bHiddenNationality>0</bHiddenNationality>
\t\t\t<bAlwaysHostile>0</bAlwaysHostile>
\t\t\t<UnitClassUpgrades/>
\t\t\t<UnitClassTargets/>
\t\t\t<UnitCombatTargets/>
\t\t\t<UnitClassDefenders/>
\t\t\t<UnitCombatDefenders/>
\t\t\t<FlankingStrikes/>
\t\t\t<UnitAIs>
\t\t\t\t<UnitAI>
\t\t\t\t\t<UnitAIType>UNITAI_DEFENSE_AIR</UnitAIType>
\t\t\t\t\t<bUnitAI>1</bUnitAI>
\t\t\t\t</UnitAI>
\t\t\t\t<UnitAI>
\t\t\t\t\t<UnitAIType>UNITAI_CARRIER_AIR</UnitAIType>
\t\t\t\t\t<bUnitAI>1</bUnitAI>
\t\t\t\t</UnitAI>
\t\t\t\t<UnitAI>
\t\t\t\t\t<UnitAIType>UNITAI_ATTACK_AIR</UnitAIType>
\t\t\t\t\t<bUnitAI>1</bUnitAI>
\t\t\t\t</UnitAI>
\t\t\t</UnitAIs>
\t\t\t<NotUnitAIs/>
\t\t\t<Builds/>
\t\t\t<ReligionSpreads/>
\t\t\t<CorporationSpreads/>
\t\t\t<GreatPeoples/>
\t\t\t<Buildings/>
\t\t\t<ForceBuildings/>
\t\t\t<HolyCity>NONE</HolyCity>
\t\t\t<ReligionType>NONE</ReligionType>
\t\t\t<StateReligion>NONE</StateReligion>
\t\t\t<PrereqReligion>NONE</PrereqReligion>
\t\t\t<PrereqCorporation>NONE</PrereqCorporation>
\t\t\t<PrereqBuilding>NONE</PrereqBuilding>
\t\t\t<PrereqTech>TECH_ADVANCED_FLIGHT</PrereqTech>
\t\t\t<TechTypes/>
\t\t\t<BonusType>BONUS_OIL</BonusType>
\t\t\t<PrereqBonuses>
\t\t\t\t<BonusType>BONUS_ALUMINUM</BonusType>
\t\t\t\t<BonusType>NONE</BonusType>
\t\t\t\t<BonusType>NONE</BonusType>
\t\t\t\t<BonusType>NONE</BonusType>
\t\t\t</PrereqBonuses>
\t\t\t<ProductionTraits/>
\t\t\t<Flavors/>
\t\t\t<iAIWeight>0</iAIWeight>
\t\t\t<iCost>150</iCost>
\t\t\t<iHurryCostModifier>0</iHurryCostModifier>
\t\t\t<iAdvancedStartCost>100</iAdvancedStartCost>
\t\t\t<iAdvancedStartCostIncrease>0</iAdvancedStartCostIncrease>
\t\t\t<iMinAreaSize>-1</iMinAreaSize>
\t\t\t<iMoves>1</iMoves>
\t\t\t<bNoRevealMap>0</bNoRevealMap>
\t\t\t<iAirRange>12</iAirRange>
\t\t\t<iAirUnitCap>1</iAirUnitCap>
\t\t\t<iDropRange>0</iDropRange>
\t\t\t<iNukeRange>-1</iNukeRange>
\t\t\t<iWorkRate>0</iWorkRate>
\t\t\t<iBaseDiscover>0</iBaseDiscover>
\t\t\t<iDiscoverMultiplier>0</iDiscoverMultiplier>
\t\t\t<iBaseHurry>0</iBaseHurry>
\t\t\t<iHurryMultiplier>0</iHurryMultiplier>
\t\t\t<iBaseTrade>0</iBaseTrade>
\t\t\t<iTradeMultiplier>0</iTradeMultiplier>
\t\t\t<iGreatWorkCulture>0</iGreatWorkCulture>
\t\t\t<iEspionagePoints>0</iEspionagePoints>
\t\t\t<TerrainImpassables/>
\t\t\t<FeatureImpassables/>
\t\t\t<TerrainPassableTechs/>
\t\t\t<FeaturePassableTechs/>
\t\t\t<iCombat>0</iCombat>
\t\t\t<iCombatLimit>0</iCombatLimit>
\t\t\t<iAirCombat>28</iAirCombat>
\t\t\t<iAirCombatLimit>50</iAirCombatLimit>
\t\t\t<iXPValueAttack>4</iXPValueAttack>
\t\t\t<iXPValueDefense>4</iXPValueDefense>
\t\t\t<iFirstStrikes>2</iFirstStrikes>
\t\t\t<iChanceFirstStrikes>0</iChanceFirstStrikes>
\t\t\t<iInterceptionProbability>100</iInterceptionProbability>
\t\t\t<iEvasionProbability>50</iEvasionProbability>
\t\t\t<iWithdrawalProb>0</iWithdrawalProb>
\t\t\t<iCollateralDamage>0</iCollateralDamage>
\t\t\t<iCollateralDamageLimit>0</iCollateralDamageLimit>
\t\t\t<iCollateralDamageMaxUnits>0</iCollateralDamageMaxUnits>
\t\t\t<iCityAttack>0</iCityAttack>
\t\t\t<iCityDefense>0</iCityDefense>
\t\t\t<iAnimalCombat>0</iAnimalCombat>
\t\t\t<iHillsAttack>0</iHillsAttack>
\t\t\t<iHillsDefense>0</iHillsDefense>
\t\t\t<TerrainNatives/>
\t\t\t<FeatureNatives/>
\t\t\t<TerrainAttacks/>
\t\t\t<TerrainDefenses/>
\t\t\t<FeatureAttacks/>
\t\t\t<FeatureDefenses/>
\t\t\t<UnitClassAttackMods/>
\t\t\t<UnitClassDefenseMods/>
\t\t\t<UnitCombatMods/>
\t\t\t<UnitCombatCollateralImmunes/>
\t\t\t<DomainMods/>
\t\t\t<BonusProductionModifiers/>
\t\t\t<iBombRate>14</iBombRate>
\t\t\t<iBombardRate>0</iBombardRate>
\t\t\t<SpecialCargo>NONE</SpecialCargo>
\t\t\t<DomainCargo>NONE</DomainCargo>
\t\t\t<iCargo>0</iCargo>
\t\t\t<iConscription>0</iConscription>
\t\t\t<iCultureGarrison>0</iCultureGarrison>
\t\t\t<iExtraCost>0</iExtraCost>
\t\t\t<iAsset>4</iAsset>
\t\t\t<iPower>28</iPower>
\t\t\t<UnitMeshGroups>
\t\t\t\t<iGroupSize>1</iGroupSize>
\t\t\t\t<fMaxSpeed>0.75</fMaxSpeed>
\t\t\t\t<fPadTime>1</fPadTime>
\t\t\t\t<iMeleeWaveSize>1</iMeleeWaveSize>
\t\t\t\t<iRangedWaveSize>1</iRangedWaveSize>
\t\t\t\t<UnitMeshGroup>
\t\t\t\t\t<iRequired>1</iRequired>
\t\t\t\t\t<EarlyArtDefineTag>ART_DEF_UNIT_AMERICAN_YF23</EarlyArtDefineTag>
\t\t\t\t</UnitMeshGroup>
\t\t\t</UnitMeshGroups>
\t\t\t<FormationType>FORMATION_TYPE_MACHINE</FormationType>
\t\t\t<HotKey/>
\t\t\t<bAltDown>0</bAltDown>
\t\t\t<bShiftDown>0</bShiftDown>
\t\t\t<bCtrlDown>0</bCtrlDown>
\t\t\t<iHotKeyPriority>0</iHotKeyPriority>
\t\t\t<FreePromotions/>
\t\t\t<LeaderPromotion>NONE</LeaderPromotion>
\t\t\t<iLeaderExperience>0</iLeaderExperience>
\t\t</UnitInfo>
\t</UnitInfos>
</Civ4UnitInfos>
'''
    unit_targets = [
        os.path.join(ROOT, 'src', 'bts', 'CIV4UnitInfos.xml'),
        os.path.join(ROOT, 'patch', 'PatchFiles', 'Beyond the Sword', 'Assets', 'XML', 'Units', 'CIV4UnitInfos.xml')
    ]
    for path in unit_targets:
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        if 'UNIT_AMERICAN_YF23' in content:
            print(f"Already in {path}")
            continue
        content = content.replace('\t</UnitInfos>\n</Civ4UnitInfos>', unit_info_xml)
        content = content.replace('</UnitInfos>\n</Civ4UnitInfos>', unit_info_xml)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated {path}")

def main():
    print("Step 1: Creating GameText...")
    update_game_text()
    print("Step 2: Updating ArtDefines...")
    update_art_defines()
    print("Step 3: Updating CivilizationInfos...")
    update_civilization_infos()
    print("Step 4: Updating UnitInfos...")
    update_unit_infos()
    print("Done adding YF-23!")

if __name__ == '__main__':
    main()
