# 文明帝國 IV：超越刀鋒 還原英文原版腳本
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$Host.UI.RawUI.WindowTitle = "文明帝國 IV：超越刀鋒 還原英文原版"

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "    《文明帝國 IV：超越刀鋒》還原官方英文原版程式           " -ForegroundColor Yellow
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

$PSScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$PatchRoot = Split-Path -Parent $PSScriptDir

# 偵測遊戲目錄
$GameRoot = $null
$parentDir = Split-Path -Parent $PatchRoot
if (Test-Path "$parentDir\Beyond the Sword\Civ4BeyondSword.exe") {
    $GameRoot = $parentDir
}

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

while (-not $GameRoot -or -not (Test-Path "$GameRoot\Beyond the Sword")) {
    Write-Host "`n請輸入文明帝國 IV 安裝路徑：" -ForegroundColor Yellow
    $GameRoot = Read-Host "請輸入路徑"
    if ($GameRoot) {
        $GameRoot = $GameRoot.Trim().Trim('"')
    }
    if (-not ($GameRoot -and (Test-Path "$GameRoot\Beyond the Sword"))) {
        Write-Host "[錯誤] 指定路徑不存在，請重新輸入！" -ForegroundColor Red
        $GameRoot = $null
    }
}

$btsRoot = Join-Path $GameRoot "Beyond the Sword"

Write-Host "正在還原備份檔案..." -ForegroundColor Cyan

# 1. 還原主程式
$btsExe = Join-Path $btsRoot "Civ4BeyondSword.exe"
$btsExeBak = Join-Path $btsRoot "Civ4BeyondSword.exe.original"
if (Test-Path $btsExeBak) {
    Copy-Item $btsExeBak $btsExe -Force
    Write-Host "  [✓] 主程式已還原為原版英文執行檔" -ForegroundColor Green
}

# 2. 還原主題
$btsThm = Join-Path $btsRoot "Resource\Themes\Civ4\Civ4Theme_Common.thm"
$btsThmBak = "$btsThm.original_backup"
if (Test-Path $btsThmBak) {
    Copy-Item $btsThmBak $btsThm -Force
    Write-Host "  [✓] 介面主題已還原" -ForegroundColor Green
}

# 3. 還原文本
$btsText = Join-Path $btsRoot "Assets\XML\Text"
$btsTextBak = Join-Path $btsRoot "Assets\XML\Text.original_backup"
if (Test-Path $btsTextBak) {
    Remove-Item -Path $btsText -Recurse -Force -ErrorAction SilentlyContinue
    Copy-Item $btsTextBak $btsText -Recurse -Force
    Write-Host "  [✓] 文本目錄已還原為原版英文" -ForegroundColor Green
}

# 4. 移除桌面捷徑
$desktopPath = [System.Environment]::GetFolderPath([System.Environment+SpecialFolder]::Desktop)
$shortcutPath = Join-Path $desktopPath '文明帝國 IV：超越刀鋒 (繁體中文版).lnk'
if (Test-Path $shortcutPath) {
    Remove-Item $shortcutPath -Force -ErrorAction SilentlyContinue
    Write-Host "  [✓] 已移除繁中版桌面捷徑" -ForegroundColor Green
}

Write-Host "`n============================================================" -ForegroundColor Green
Write-Host "          遊戲已成功還原為官方原版英文狀態！                " -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Green
Write-Host ""
