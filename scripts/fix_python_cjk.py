import os
import shutil
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STEAM_PATH = r"C:\Program Files (x86)\Steam\steamapps\common\Sid Meier's Civilization IV Beyond the Sword"

def patch_cvutil_bts(content):
    # 1. Patch convertToUnicode and convertToStr
    old_unicode_pattern = r'def convertToUnicode\(s\):[\s\S]*?(?=class RedirectDebug:)'
    new_unicode_code = '''def convertToUnicode(s):
\t"if the string is non unicode, convert it to unicode safely"
\tif (isinstance(s, str)):
\t\tfor enc in ("utf-8", "cp950", "cp936", "cp932", "latin_1"):
\t\t\ttry:
\t\t\t\treturn s.decode(enc)
\t\t\texcept (UnicodeDecodeError, LookupError):
\t\t\t\tcontinue
\t\treturn s.decode("latin_1", "replace")
\treturn s
\t
def convertToStr(s):
\t"if the string is unicode, convert it to str safely"
\tif (isinstance(s, unicode)):
\t\ttry:
\t\t\treturn s.encode("latin_1")
\t\texcept (UnicodeEncodeError, LookupError):
\t\t\tpass
\t\ttry:
\t\t\treturn s.encode("utf-8")
\t\texcept (UnicodeEncodeError, LookupError):
\t\t\tpass
\t\ttry:
\t\t\treturn s.encode("cp950")
\t\texcept (UnicodeEncodeError, LookupError):
\t\t\tpass
\t\treturn s.encode("latin_1", "replace")
\treturn s

'''
    content = re.sub(old_unicode_pattern, new_unicode_code, content)

    # 2. Patch initDynamicFontIcons and addIconToMap
    old_font_pattern = r'def initDynamicFontIcons\(\):[\s\S]*?(?=OtherFontIcons = \{)'
    new_font_code = '''def initDynamicFontIcons():
\tglobal FontIconMap
\t
\tinfo = ""
\tdesc = ""
\t# add Commerce Icons
\tcommerceKeys = ['gold', 'research', 'culture', 'espionage']
\tfor i in range(CommerceTypes.NUM_COMMERCE_TYPES):
\t\tinfo = gc.getCommerceInfo(i)
\t\tdesc = info.getDescription().lower()
\t\taddIconToMap(info.getChar, desc)
\t\tif i < len(commerceKeys):
\t\t\taddIconToMap(info.getChar, commerceKeys[i])
\t# add Yield Icons
\tyieldKeys = ['food', 'production', 'commerce']
\tfor i in range(YieldTypes.NUM_YIELD_TYPES):
\t\tinfo = gc.getYieldInfo(i)
\t\tdesc = info.getDescription().lower()
\t\taddIconToMap(info.getChar, desc)
\t\tif i < len(yieldKeys):
\t\t\taddIconToMap(info.getChar, yieldKeys[i])
\t# add Religion & Holy City Icons
\tfor i in range(gc.getNumReligionInfos()):
\t\tinfo = gc.getReligionInfo(i)
\t\tdesc = info.getDescription().lower()
\t\taddIconToMap(info.getChar, desc)
\t\taddIconToMap(info.getHolyCityChar, desc)
\tfor key in OtherFontIcons.keys():
\t\t#print key
\t\tFontIconMap[key] = (u"%c" % CyGame().getSymbolID(OtherFontIcons.get(key)))
\t
\t#print FontIconMap
\t
def addIconToMap(infoChar, desc):
\tglobal FontIconMap
\ttry:
\t\tprint "%s - %s" %(infoChar(), convertToStr(desc))
\texcept:
\t\tpass
\tuc = infoChar()
\tif (uc>=0):
\t\tcharVal = u"%c" %(uc,)
\t\tFontIconMap[desc] = charVal
\t\ttry:
\t\t\tFontIconMap[convertToStr(desc)] = charVal
\t\texcept:
\t\t\tpass

'''
    content = re.sub(old_font_pattern, new_font_code, content)
    return content

def patch_options_callback(content):
    old_block = '''\tszNewProfileName = getOptionsScreen().getProfileEditCtrlText()
#\tszNarrow = szNewProfileName.encode("latin_1")
\tif (CyGame().getCurrentLanguage() == 1):
\t\tszNarrow = szNewProfileName.encode("cp932")
\telse:
\t\tszNarrow = szNewProfileName.encode("latin_1")'''
    new_block = '''\tszNewProfileName = getOptionsScreen().getProfileEditCtrlText()
\tszNarrow = CvUtil.convertToStr(szNewProfileName)'''
    return content.replace(old_block, new_block)

def patch_wb_desc(content):
    old_block = '''# globals
gc = CyGlobalContext()
version = 11
#fileencoding = "latin_1"\t# aka "iso-8859-1"
if (CyGame().getCurrentLanguage() == 1):
\tfileencoding = "cp932"
else:
\tfileencoding = "latin_1"'''
    new_block = '''# globals
gc = CyGlobalContext()
version = 11
fileencoding = "utf-8"

def safeDecode(v, enc=fileencoding):
\tif isinstance(v, unicode):
\t\treturn v
\ttry:
\t\treturn v.decode(enc)
\texcept (UnicodeDecodeError, LookupError):
\t\tpass
\tfor e in ("utf-8", "cp950", "cp936", "cp932", "latin_1"):
\t\ttry:
\t\t\treturn v.decode(e)
\t\texcept (UnicodeDecodeError, LookupError):
\t\t\tcontinue
\treturn v.decode("latin_1", "replace")'''
    content = content.replace(old_block, new_block)
    content = re.sub(r'(\w+)\.decode\(fileencoding\)', r'safeDecode(\1)', content)
    return content

def main():
    print("=== Patching Civ4 BTS Python files for CJK/Traditional Chinese ===")
    bts_py_orig = os.path.join(STEAM_PATH, r"Beyond the Sword\Assets\Python\CvUtil.py")
    if not os.path.exists(bts_py_orig):
        print(f"Error: {bts_py_orig} not found!")
        return

    content_cvutil = open(bts_py_orig, 'r', encoding='latin-1').read()
    patched_cvutil = patch_cvutil_bts(content_cvutil)

    # 1. Beyond the Sword/Assets/Python/CvUtil.py
    bts_patch_dir = os.path.join(ROOT, "patch", "PatchFiles", "Beyond the Sword", "Assets", "Python")
    os.makedirs(bts_patch_dir, exist_ok=True)
    bts_patch_file = os.path.join(bts_patch_dir, "CvUtil.py")
    with open(bts_patch_file, 'w', encoding='latin-1') as f:
        f.write(patched_cvutil)
    print(f"[OK] Created {bts_patch_file}")

    # Copy to src/bts/Assets/Python/CvUtil.py
    src_bts_dir = os.path.join(ROOT, "src", "bts", "Assets", "Python")
    os.makedirs(src_bts_dir, exist_ok=True)
    shutil.copy2(bts_patch_file, os.path.join(src_bts_dir, "CvUtil.py"))
    print(f"[OK] Created {os.path.join(src_bts_dir, 'CvUtil.py')}")

    # Copy directly to Steam
    shutil.copy2(bts_patch_file, bts_py_orig)
    print(f"[OK] Deployed directly to Steam: {bts_py_orig}")

    # 2. Options Screen Callback Interface
    opt_orig = os.path.join(STEAM_PATH, r"Beyond the Sword\Assets\Python\EntryPoints\CvOptionsScreenCallbackInterface.py")
    content_opt = open(opt_orig, 'r', encoding='latin-1').read()
    patched_opt = patch_options_callback(content_opt)

    bts_entry_dir = os.path.join(bts_patch_dir, "EntryPoints")
    os.makedirs(bts_entry_dir, exist_ok=True)
    bts_opt_file = os.path.join(bts_entry_dir, "CvOptionsScreenCallbackInterface.py")
    with open(bts_opt_file, 'w', encoding='latin-1') as f:
        f.write(patched_opt)
    print(f"[OK] Created {bts_opt_file}")

    src_entry_dir = os.path.join(src_bts_dir, "EntryPoints")
    os.makedirs(src_entry_dir, exist_ok=True)
    shutil.copy2(bts_opt_file, os.path.join(src_entry_dir, "CvOptionsScreenCallbackInterface.py"))
    shutil.copy2(bts_opt_file, opt_orig)
    print(f"[OK] Deployed directly to Steam: {opt_orig}")

    # 3. pyWB/CvWBDesc.py
    wb_orig = os.path.join(STEAM_PATH, r"Beyond the Sword\Assets\Python\pyWB\CvWBDesc.py")
    content_wb = open(wb_orig, 'r', encoding='latin-1').read()
    patched_wb = patch_wb_desc(content_wb)

    bts_wb_dir = os.path.join(bts_patch_dir, "pyWB")
    os.makedirs(bts_wb_dir, exist_ok=True)
    bts_wb_file = os.path.join(bts_wb_dir, "CvWBDesc.py")
    with open(bts_wb_file, 'w', encoding='latin-1') as f:
        f.write(patched_wb)
    print(f"[OK] Created {bts_wb_file}")

    src_wb_dir = os.path.join(src_bts_dir, "pyWB")
    os.makedirs(src_wb_dir, exist_ok=True)
    shutil.copy2(bts_wb_file, os.path.join(src_wb_dir, "CvWBDesc.py"))
    shutil.copy2(bts_wb_file, wb_orig)
    print(f"[OK] Deployed directly to Steam: {wb_orig}")

    # 4. Also patch base game and Warlords CvUtil.py
    base_py_orig = os.path.join(STEAM_PATH, r"Assets\Python\CvUtil.py")
    if os.path.exists(base_py_orig):
        content_base = open(base_py_orig, 'r', encoding='latin-1').read()
        patched_base = patch_cvutil_bts(content_base)
        base_patch_dir = os.path.join(ROOT, "patch", "PatchFiles", "Assets", "Python")
        os.makedirs(base_patch_dir, exist_ok=True)
        with open(os.path.join(base_patch_dir, "CvUtil.py"), 'w', encoding='latin-1') as f:
            f.write(patched_base)
        shutil.copy2(os.path.join(base_patch_dir, "CvUtil.py"), base_py_orig)
        print(f"[OK] Deployed base game CvUtil.py to Steam: {base_py_orig}")

    warlords_py_orig = os.path.join(STEAM_PATH, r"Warlords\Assets\Python\CvUtil.py")
    if os.path.exists(warlords_py_orig):
        content_wl = open(warlords_py_orig, 'r', encoding='latin-1').read()
        patched_wl = patch_cvutil_bts(content_wl)
        wl_patch_dir = os.path.join(ROOT, "patch", "PatchFiles", "Warlords", "Assets", "Python")
        os.makedirs(wl_patch_dir, exist_ok=True)
        with open(os.path.join(wl_patch_dir, "CvUtil.py"), 'w', encoding='latin-1') as f:
            f.write(patched_wl)
        shutil.copy2(os.path.join(wl_patch_dir, "CvUtil.py"), warlords_py_orig)
        print(f"[OK] Deployed Warlords CvUtil.py to Steam: {warlords_py_orig}")

    print("\nAll Python files successfully patched and deployed!")

if __name__ == '__main__':
    main()
