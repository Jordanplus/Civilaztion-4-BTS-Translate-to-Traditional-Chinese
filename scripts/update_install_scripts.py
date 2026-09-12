import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INSTALL_PS1 = os.path.join(ROOT, "patch", "PatchFiles", "install.ps1")
UNINSTALL_PS1 = os.path.join(ROOT, "patch", "PatchFiles", "uninstall.ps1")

def update_install():
    with open(INSTALL_PS1, "r", encoding="utf-8") as f:
        content = f.read()

    # Add python backup to Step 2
    py_backup_block = '''$btsText = Join-Path $btsRoot "Assets\\XML\\Text"
$btsTextBak = Join-Path $btsRoot "Assets\\XML\\Text.original_backup"
if ((Test-Path $btsText) -and -not (Test-Path $btsTextBak)) {
    Copy-Item $btsText $btsTextBak -Recurse -Force
    Write-Host "  [✓] 原版文本目錄已備份為：Text.original_backup" -ForegroundColor Green
}

$btsPy = Join-Path $btsRoot "Assets\\Python"
$btsPyBak = Join-Path $btsRoot "Assets\\Python.original_backup"
if ((Test-Path $btsPy) -and -not (Test-Path $btsPyBak)) {
    Copy-Item $btsPy $btsPyBak -Recurse -Force
    Write-Host "  [✓] 原版 Python 目錄已備份為：Python.original_backup" -ForegroundColor Green
}'''

    content = content.replace('''$btsText = Join-Path $btsRoot "Assets\\XML\\Text"
$btsTextBak = Join-Path $btsRoot "Assets\\XML\\Text.original_backup"
if ((Test-Path $btsText) -and -not (Test-Path $btsTextBak)) {
    Copy-Item $btsText $btsTextBak -Recurse -Force
    Write-Host "  [✓] 原版文本目錄已備份為：Text.original_backup" -ForegroundColor Green
}''', py_backup_block)

    # Replace ini candidate detection
    old_ini_block = '''$docsPath = [System.Environment]::GetFolderPath([System.Environment+SpecialFolder]::MyDocuments)
$iniCandidates = @(
    "$docsPath\\My Games\\beyond the sword\\CivilizationIV.ini",
    "$docsPath\\My Games\\Sid Meier's Civilization IV Beyond the Sword\\CivilizationIV.ini"
)'''

    new_ini_block = '''$docsCandidates = @(
    [System.Environment]::GetFolderPath([System.Environment+SpecialFolder]::MyDocuments),
    (Join-Path $env:USERPROFILE "Documents"),
    (Join-Path $env:USERPROFILE "OneDrive\\Documents"),
    (Join-Path $env:USERPROFILE "OneDrive\\文件")
)
try {
    $regPersonal = (Get-ItemProperty 'HKCU:\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\User Shell Folders' -ErrorAction SilentlyContinue).Personal
    if ($regPersonal) { $docsCandidates += $regPersonal }
} catch {}

$iniCandidates = @()
foreach ($doc in ($docsCandidates | Select-Object -Unique)) {
    if ($doc -and (Test-Path $doc)) {
        $iniCandidates += (Join-Path $doc "My Games\\beyond the sword\\CivilizationIV.ini")
        $iniCandidates += (Join-Path $doc "My Games\\Sid Meier's Civilization IV Beyond the Sword\\CivilizationIV.ini")
    }
}'''

    content = content.replace(old_ini_block, new_ini_block)

    # Save with UTF-8 BOM
    with open(INSTALL_PS1, "w", encoding="utf-8-sig") as f:
        f.write(content)
    print("Updated install.ps1 with UTF-8 BOM and improved ini search.")

def update_uninstall():
    with open(UNINSTALL_PS1, "r", encoding="utf-8") as f:
        content = f.read()

    py_restore_block = '''# 3. 還原文本
$btsText = Join-Path $btsRoot "Assets\\XML\\Text"
$btsTextBak = Join-Path $btsRoot "Assets\\XML\\Text.original_backup"
if (Test-Path $btsTextBak) {
    Remove-Item -Path $btsText -Recurse -Force -ErrorAction SilentlyContinue
    Copy-Item $btsTextBak $btsText -Recurse -Force
    Write-Host "  [✓] 文本目錄已還原為原版英文" -ForegroundColor Green
}

# 3.1 還原 Python
$btsPy = Join-Path $btsRoot "Assets\\Python"
$btsPyBak = Join-Path $btsRoot "Assets\\Python.original_backup"
if (Test-Path $btsPyBak) {
    Remove-Item -Path $btsPy -Recurse -Force -ErrorAction SilentlyContinue
    Copy-Item $btsPyBak $btsPy -Recurse -Force
    Write-Host "  [✓] Python 目錄已還原為原版" -ForegroundColor Green
}'''

    old_text_block = '''# 3. 還原文本
$btsText = Join-Path $btsRoot "Assets\\XML\\Text"
$btsTextBak = Join-Path $btsRoot "Assets\\XML\\Text.original_backup"
if (Test-Path $btsTextBak) {
    Remove-Item -Path $btsText -Recurse -Force -ErrorAction SilentlyContinue
    Copy-Item $btsTextBak $btsText -Recurse -Force
    Write-Host "  [✓] 文本目錄已還原為原版英文" -ForegroundColor Green
}'''

    content = content.replace(old_text_block, py_restore_block)

    with open(UNINSTALL_PS1, "w", encoding="utf-8-sig") as f:
        f.write(content)
    print("Updated uninstall.ps1 with UTF-8 BOM and Python restore.")

if __name__ == "__main__":
    update_install()
    update_uninstall()
