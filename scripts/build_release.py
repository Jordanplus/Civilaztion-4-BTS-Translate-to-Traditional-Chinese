import os
import zipfile
import sys
import re
import xml.etree.ElementTree as ET

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PATCH_DIR = os.path.join(ROOT, 'patch')
DIST_DIR = os.path.join(ROOT, 'dist')
CHANGELOG_PATH = os.path.join(ROOT, 'CHANGELOG.md')

def resolve_version():
    """Resolve release version from CLI arguments, CHANGELOG.md, or default."""
    # Check CLI argument: e.g. python build_release.py v1.1.0
    for arg in sys.argv[1:]:
        if not arg.startswith('-'):
            return arg if arg.startswith('v') else f"v{arg}"
    
    # Read the latest released version from CHANGELOG.md
    if os.path.exists(CHANGELOG_PATH):
        with open(CHANGELOG_PATH, 'r', encoding='utf-8') as f:
            for line in f:
                # Match e.g. ## [v1.1.0] - 2026-09-28 or ## [1.1.0]
                m = re.search(r'##\s*\[v?(\d+\.\d+\.\d+)\]', line)
                if m:
                    return f"v{m.group(1)}"
    
    return "v1.0.0"

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

def package_release(version):
    zip_name = f"Civilaztion-4-BTS-Traditional-Chinese-Patch-{version}.zip"
    zip_path = os.path.join(DIST_DIR, zip_name)

    os.makedirs(DIST_DIR, exist_ok=True)
    if os.path.exists(zip_path):
        os.remove(zip_path)

    print(f"Creating release package ({version}): {zip_path}")
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(PATCH_DIR):
            for file in files:
                # Skip backup folder if exists
                if 'Backup' in root:
                    continue
                # Skip Python bytecode and cache
                if '__pycache__' in root or file.endswith(('.pyc', '.pyo')):
                    continue
                # Never package the player's own private files (e.g. the CJK exe)
                if 'private' in os.path.relpath(root, PATCH_DIR).split(os.sep):
                    continue
                file_path = os.path.join(root, file)
                rel_path = os.path.relpath(file_path, PATCH_DIR)
                # Prefix inside zip
                arc_name = os.path.join('Civilaztion-4-BTS-Traditional-Chinese-Patch', rel_path)
                zipf.write(file_path, arc_name)

    size_mb = os.path.getsize(zip_path) / (1024 * 1024)
    print(f"Package created successfully! File: {zip_name} ({size_mb:.2f} MB)")

if __name__ == '__main__':
    version = resolve_version()
    print(f"Target release version: {version}")
    verify_xmls()
    package_release(version)
