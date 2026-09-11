import os
import shutil
import sys

DEFAULT_STEAM_PATH = r"C:\Program Files (x86)\Steam\steamapps\common\Sid Meier's Civilization IV Beyond the Sword"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PATCH_FILES = os.path.join(ROOT, 'patch', 'PatchFiles')

def main():
    steam_path = DEFAULT_STEAM_PATH
    if len(sys.argv) > 1:
        steam_path = sys.argv[1]

    if not os.path.exists(steam_path):
        print(f"Error: Game directory not found at: {steam_path}")
        sys.exit(1)

    print(f"Deploying patch directly to Steam: {steam_path}")
    count = 0
    for root, dirs, files in os.walk(PATCH_FILES):
        for f in files:
            if f in ['install.ps1', 'uninstall.ps1']:
                continue
            src_file = os.path.join(root, f)
            rel_path = os.path.relpath(src_file, PATCH_FILES)
            dst_file = os.path.join(steam_path, rel_path)
            os.makedirs(os.path.dirname(dst_file), exist_ok=True)
            shutil.copy2(src_file, dst_file)
            count += 1

    print(f"Deployed {count} files to game directory successfully!")

if __name__ == '__main__':
    main()
