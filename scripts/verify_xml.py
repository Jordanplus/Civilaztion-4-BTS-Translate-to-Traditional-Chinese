import os
import xml.etree.ElementTree as ET

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TARGET_DIRS = [
    os.path.join(ROOT, 'src'),
    os.path.join(ROOT, 'patch', 'PatchFiles')
]

def check_xml(path):
    try:
        ET.parse(path)
        return True, None
    except Exception as e:
        return False, str(e)

def main():
    total = 0
    failed = 0
    print("Scanning XML files...")
    for target in TARGET_DIRS:
        for root, dirs, files in os.walk(target):
            for f in files:
                if f.endswith('.xml'):
                    total += 1
                    p = os.path.join(root, f)
                    ok, err = check_xml(p)
                    if not ok:
                        failed += 1
                        print(f"[FAIL] {p}: {err}")
    print(f"Verification complete: {total} files checked, {failed} errors.")
    if failed == 0:
        print("All XML files are healthy!")

if __name__ == '__main__':
    main()
