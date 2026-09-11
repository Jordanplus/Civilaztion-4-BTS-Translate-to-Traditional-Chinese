import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PATCH_FILES = os.path.join(ROOT, 'patch', 'PatchFiles')

def from_ncr(text):
    return re.sub(r'&#(\d+);', lambda m: chr(int(m.group(1))), text)

tags_to_check = {
    'TXT_KEY_POPUP_ENTER_WB': '世界編輯器',
    'TXT_KEY_WORLD_BUILDER': '世界編輯器',
    'TXT_KEY_WB_EXIT': '退出世界編輯器',
    'TXT_KEY_MAP_SCRIPT_LOGICAL': '合乎常理',
    'TXT_KEY_MAP_SCRIPT_IRRATIONAL': '反常分佈',
    'TXT_KEY_MAP_SCRIPT_CRAZY': '狂亂模式',
}

def main():
    print("Checking key translations...")
    all_ok = True
    for root, dirs, files in os.walk(PATCH_FILES):
        for f in files:
            if f.endswith('.xml'):
                p = os.path.join(root, f)
                with open(p, 'r', encoding='latin-1') as fp:
                    c = fp.read()
                for tag, expected in tags_to_check.items():
                    if f'<Tag>{tag}</Tag>' in c:
                        m = re.search(r'<TEXT>\s*<Tag>' + tag + r'</Tag>(.*?)</TEXT>', c, re.DOTALL)
                        if m:
                            dec = from_ncr(m.group(1))
                            ch = re.search(r'<Chinese>(.*?)</Chinese>', dec, re.DOTALL)
                            val = ch.group(1).strip() if ch else ''
                            if val != expected:
                                print(f"[MISMATCH] In {f}: {tag} is '{val}', expected '{expected}'")
                                all_ok = False
                            else:
                                print(f"[OK] In {f}: {tag} -> '{val}'")
    if all_ok:
        print("All key translations verified successfully!")

if __name__ == '__main__':
    main()
