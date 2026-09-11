# 文明帝國 IV：超越刀鋒 繁體中文一鍵安裝核心腳本
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$Host.UI.RawUI.WindowTitle = "文明帝國 IV：超越刀鋒 繁體中文化補丁"

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "    《文明帝國 IV：超越刀鋒》(Beyond the Sword 3.19)        " -ForegroundColor Yellow
Write-Host "           繁體中文化一鍵補丁 (Steam 專用)                  " -ForegroundColor Yellow
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

$PSScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$PatchRoot = Split-Path -Parent $PSScriptDir
$PatchFilesDir = Join-Path $PatchRoot "PatchFiles"

# 1. 偵測遊戲根目錄
Write-Host "[1/5] 正在偵測遊戲安裝路徑..." -ForegroundColor Cyan
$GameRoot = $null

# 檢查上層目錄是否即為遊戲目錄
$parentDir = Split-Path -Parent $PatchRoot
if (Test-Path "$parentDir\Beyond the Sword\Civ4BeyondSword.exe") {
    $GameRoot = $parentDir
}

# 檢查 Steam 登錄檔
if (-not $GameRoot) {
    $regKeys = @(
        "HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\Steam App 8800",
        "HKLM:\SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall\Steam App 8800",
        "HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\Steam App 8830",
        "HKLM:\SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall\Steam App 8830"
    )
    foreach ($k in $regKeys) {
        if (Test-Path $k) {
            $loc = (Get-ItemProperty -Path $k -ErrorAction SilentlyContinue).InstallLocation
            if ($loc -and (Test-Path "$loc\Beyond the Sword")) {
                $GameRoot = $loc
                break
            }
        }
    }
}

# 檢查常見預設安裝路徑
if (-not $GameRoot) {
    $candidates = @(
        "C:\Program Files (x86)\Steam\steamapps\common\Sid Meier's Civilization IV Beyond the Sword",
        "C:\Program Files\Steam\steamapps\common\Sid Meier's Civilization IV Beyond the Sword",
        "D:\Steam\steamapps\common\Sid Meier's Civilization IV Beyond the Sword",
        "D:\SteamLibrary\steamapps\common\Sid Meier's Civilization IV Beyond the Sword",
        "E:\SteamLibrary\steamapps\common\Sid Meier's Civilization IV Beyond the Sword",
        "F:\SteamLibrary\steamapps\common\Sid Meier's Civilization IV Beyond the Sword"
    )
    foreach ($c in $candidates) {
        if (Test-Path "$c\Beyond the Sword") {
            $GameRoot = $c
            break
        }
    }
}

# 若仍未找到，提示使用者手動輸入
while (-not $GameRoot -or -not (Test-Path "$GameRoot\Beyond the Sword")) {
    Write-Host "`n[提示] 未能自動找到遊戲目錄，請手動輸入文明帝國 IV 安裝路徑：" -ForegroundColor Yellow
    Write-Host "（例：C:\Program Files (x86)\Steam\steamapps\common\Sid Meier's Civilization IV Beyond the Sword）" -ForegroundColor Gray
    $GameRoot = Read-Host "請輸入路徑"
    if ($GameRoot) {
        $GameRoot = $GameRoot.Trim().Trim('"')
    }
    if (-not ($GameRoot -and (Test-Path "$GameRoot\Beyond the Sword"))) {
        Write-Host "[錯誤] 指定路徑不存在或未包含 'Beyond the Sword' 資料夾，請重新輸入！" -ForegroundColor Red
        $GameRoot = $null
    }
}

Write-Host "  [✓] 成功確認遊戲目錄：" -ForegroundColor Green
Write-Host "      $GameRoot" -ForegroundColor White
$btsRoot = Join-Path $GameRoot "Beyond the Sword"

# 2. 備份原始檔案
Write-Host "`n[2/5] 正在備份原版英文檔案..." -ForegroundColor Cyan

$btsExe = Join-Path $btsRoot "Civ4BeyondSword.exe"
$btsExeBak = Join-Path $btsRoot "Civ4BeyondSword.exe.original"
if ((Test-Path $btsExe) -and -not (Test-Path $btsExeBak)) {
    Copy-Item $btsExe $btsExeBak -Force
    Write-Host "  [✓] 原版主程式已備份為：Civ4BeyondSword.exe.original" -ForegroundColor Green
} else {
    Write-Host "  [i] 主程式原版備份已就位" -ForegroundColor Gray
}

$btsThm = Join-Path $btsRoot "Resource\Themes\Civ4\Civ4Theme_Common.thm"
$btsThmBak = "$btsThm.original_backup"
if ((Test-Path $btsThm) -and -not (Test-Path $btsThmBak)) {
    Copy-Item $btsThm $btsThmBak -Force
    Write-Host "  [✓] 原版介面主題已備份為：Civ4Theme_Common.thm.original_backup" -ForegroundColor Green
}

$btsText = Join-Path $btsRoot "Assets\XML\Text"
$btsTextBak = Join-Path $btsRoot "Assets\XML\Text.original_backup"
if ((Test-Path $btsText) -and -not (Test-Path $btsTextBak)) {
    Copy-Item $btsText $btsTextBak -Recurse -Force
    Write-Host "  [✓] 原版文本目錄已備份為：Text.original_backup" -ForegroundColor Green
}

# 3. 清理舊版日文安裝器殘留的檔案與重複子目錄
Write-Host "`n[3/5] 正在檢查並清理日文殘留項目與異常巢狀資料夾..." -ForegroundColor Cyan
$redundantItems = @(
    (Join-Path $btsRoot "Beyond the Sword"),
    (Join-Path $btsRoot "CvGameCoreDLL"),
    (Join-Path $btsRoot "Warlords"),
    (Join-Path $btsRoot "Assets\XML\Text\ZPATCH_CIV4GameText_JP_Fixtext.xml"),
    (Join-Path $btsRoot "Assets\XML\Text\INSTALL.DAT")
)
foreach ($rf in $redundantItems) {
    if (Test-Path $rf) {
        Remove-Item -Path $rf -Recurse -Force -ErrorAction SilentlyContinue
        Write-Host "  [✓] 已清除舊殘留項目：$rf" -ForegroundColor Gray
    }
}

# 4. 部署繁體中文補丁檔案
Write-Host "`n[4/5] 正在部署繁體中文化核心與文本檔案..." -ForegroundColor Cyan

# Beyond the Sword
Copy-Item -Path (Join-Path $PatchFilesDir "Beyond the Sword\*") -Destination $btsRoot -Recurse -Force
Write-Host "  [✓] 已部署 BtS 核心雙位元組主程式 (Civ4BeyondSword.exe)" -ForegroundColor Green
Write-Host "  [✓] 已部署微軟正黑體主題設定 (Civ4Theme_Common.thm)" -ForegroundColor Green
Write-Host "  [✓] 已部署 27 個 BtS 繁體中文全量文本 (已轉台灣用語 + NCR 防閃退)" -ForegroundColor Green

# Base game
if (Test-Path (Join-Path $GameRoot "Assets\XML\Text")) {
    Copy-Item -Path (Join-Path $PatchFilesDir "Assets\*") -Destination (Join-Path $GameRoot "Assets") -Recurse -Force
    if (Test-Path (Join-Path $PatchFilesDir "Resource")) {
        Copy-Item -Path (Join-Path $PatchFilesDir "Resource\*") -Destination (Join-Path $GameRoot "Resource") -Recurse -Force
    }
    Write-Host "  [✓] 已同步更新原版主程式文本與主題字型" -ForegroundColor Green
}

# Warlords
if (Test-Path (Join-Path $GameRoot "Warlords\Assets\XML\Text")) {
    Copy-Item -Path (Join-Path $PatchFilesDir "Warlords\*") -Destination (Join-Path $GameRoot "Warlords") -Recurse -Force
    Write-Host "  [✓] 已同步更新戰神 (Warlords) 文本" -ForegroundColor Green
}

# 5. 設定 CivilizationIV.ini 語系與桌面捷徑
Write-Host "`n[5/5] 正在更新設定檔與桌面捷徑..." -ForegroundColor Cyan

$docsPath = [System.Environment]::GetFolderPath([System.Environment+SpecialFolder]::MyDocuments)
$iniCandidates = @(
    "$docsPath\My Games\beyond the sword\CivilizationIV.ini",
    "$docsPath\My Games\Sid Meier's Civilization IV Beyond the Sword\CivilizationIV.ini"
)
foreach ($ini in $iniCandidates) {
    if (Test-Path $ini) {
        $content = Get-Content -Path $ini -Raw -ErrorAction SilentlyContinue
        if ($content -and $content -match 'Language\s*=') {
            $content = [System.Text.RegularExpressions.Regex]::Replace($content, 'Language\s*=\s*\d+', 'Language = 1')
            Set-Content -Path $ini -Value $content -NoNewline
            Write-Host "  [✓] 已設定使用者語系 (Language = 1)：$ini" -ForegroundColor Green
        }
    }
}

try {
    $WshShell = New-Object -ComObject WScript.Shell
    $desktopPath = [System.Environment]::GetFolderPath([System.Environment+SpecialFolder]::Desktop)
    $shortcutPath = Join-Path $desktopPath '文明帝國 IV：超越刀鋒 (繁體中文版).lnk'
    $shortcut = $WshShell.CreateShortcut($shortcutPath)
    $shortcut.TargetPath = (Join-Path $btsRoot "Civ4BeyondSword.exe")
    $shortcut.WorkingDirectory = $btsRoot
    $shortcut.Description = "文明帝國 IV：超越刀鋒 (繁體中文版)"
    $shortcut.IconLocation = "$btsRoot\Civ4BeyondSword.exe,0"
    $shortcut.Save()
    Write-Host "  [✓] 桌面啟動捷徑建立成功！" -ForegroundColor Green
} catch {
    Write-Host "  [i] 桌面捷徑建立略過，您仍可隨時從 Steam 啟動。" -ForegroundColor Gray
}

Write-Host ""
Write-Host "============================================================" -ForegroundColor Green
Write-Host "      恭喜！《文明帝國 IV：超越刀鋒》繁體中文補丁安裝成功！  " -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Green
Write-Host ""
Write-Host "【如何開始遊戲】" -ForegroundColor Cyan
Write-Host "  方式一：雙擊桌面捷徑「文明帝國 IV：超越刀鋒 (繁體中文版)」" -ForegroundColor White
Write-Host "  方式二：直接在 Steam 收藏庫中點擊「開始遊戲」執行" -ForegroundColor White
Write-Host ""
Write-Host "（若日後需還原英文原版，執行「還原英文原版.bat」即可）" -ForegroundColor Gray
Write-Host ""
