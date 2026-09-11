import os
import zipfile
import sys
import xml.etree.ElementTree as ET

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PATCH_DIR = os.path.join(ROOT, 'patch')
DIST_DIR = os.path.join(ROOT, 'dist')
VERSION = "v1.0.0"
ZIP_NAME = f"Civilaztion-4-BTS-Traditional-Chinese-Patch-{VERSION}.zip"
ZIP_PATH = os.path.join(DIST_DIR, ZIP_NAME)

def verify_xmls():
    print("Verifying XML files before build...")
    patch_files = os.path.join(PATCH_DIR, 'PatchFiles')
    err_count = 0
    for root, dirs, files in os.walk(patch_files):
        for f in files:
            if f.endswith('.xml'):
                p = os.path.join(root, f)
                try:
                    ET.parse(p)
                except Exception as e:
                    print(f"Error parsing {p}: {e}")
                    err_count += 1
    if err_count > 0:
        print(f"FAILED: {err_count} XML errors found.")
        sys.exit(1)
    print("All XML files passed validation!")

def package_release():
    os.makedirs(DIST_DIR, exist_ok=True)
    if os.path.exists(ZIP_PATH):
        os.remove(ZIP_PATH)

    print(f"Creating release package: {ZIP_PATH}")
    with zipfile.ZipFile(ZIP_PATH, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(PATCH_DIR):
            for file in files:
                # Skip backup folder if exists
                if 'Backup' in root:
                    continue
                file_path = os.path.join(root, file)
                rel_path = os.path.relpath(file_path, PATCH_DIR)
                # Prefix inside zip
                arc_name = os.path.join('Civilaztion-4-BTS-Traditional-Chinese-Patch', rel_path)
                zipf.write(file_path, arc_name)

    size_mb = os.path.getsize(ZIP_PATH) / (1024 * 1024)
    print(f"Package created successfully! Size: {size_mb:.2f} MB")

if __name__ == '__main__':
    verify_xmls()
    package_release()
