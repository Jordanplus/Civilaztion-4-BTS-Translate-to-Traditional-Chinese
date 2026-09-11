# 《文明帝國 IV：超越刀鋒》完整繁體中文化專案
### Civilization IV: Beyond the Sword - Traditional Chinese Localization Project

本專案為經典策略遊戲**《文明帝國 IV：超越刀鋒》（Sid Meier's Civilization IV: Beyond the Sword, BtS 3.19）**提供現代化、高品質且 100% 穩定的**繁體中文在地化體驗**。

針對長年困擾玩家的 Windows 10/11 系統閃退、編碼亂碼、文字遺漏以及不通順翻譯，本專案進行了全面的技術重構與文本修復。

---

## 🌟 核心特色與技術修復

### 1. 徹底根治 Windows 10/11 啟動閃退 (MSXML 3.0 相容)
* **技術原理**：現代 Windows 系統上的 `MSXML 3.0` 在解析含有中文原始字元（如 GBK、Big5）的 XML 檔案時極易發生記憶體崩潰。
* **解決方案**：本專案所有 XML 文本一律採用標準 **ISO-8859-1 + 十進制數字字元參照 (Numeric Character Reference, NCR，例如 `&#24037;`)**。引擎無需依賴系統字碼頁即可 100% 穩定解析，徹底解決閃退問題。

### 2. 歷史亂碼與嚴重錯誤全面清洗
* **修復 729 處嚴重亂碼**：修復了原漢化包在 `CIV4GameTextInfos_Objects.xml` 因 GBK 被錯誤按 Latin-1 讀取所產生的大量亂碼（如地形、資源、物件說明）。
* **女領袖文字完全復原**：修復原版遺失的凱薩琳（Catherine）、伊莉莎白（Elizabeth）、哈特謝普蘇特（Hatshepsut）、伊莎貝拉（Isabella）、維多利亞（Victoria）等女性領袖名字與文明百科資訊。
* **日文補丁殘留清除**：徹底移除過往日版殘留之 `ZPATCH_CIV4GameText_JP_Fixtext.xml`，避免遊戲載入衝突。

### 3. 在地化名詞精準校對
* **世界編輯器 (WorldBuilder)**：全面替換原先生硬的「世界建立器」譯名。Esc 選單按鈕、快捷鍵提示（`[CTRL + W]`）與文明百科統一命名為**「世界編輯器」**。
* **資源分佈模式 (Fantasy Realm 地圖腳本)**：
  * `Logical` $
ightarrow$ **合乎常理**（依常規地形分佈）
  * `Irrational` $
ightarrow$ **反常分佈**（打亂地形限制，修正原先誤譯的「不均」）
  * `Crazy` $
ightarrow$ **狂亂模式**（極端少數資源狂暴生成，修正原先的「混亂」）
* **台灣常用語彙支援**：使用 OpenCC `s2twp` 字典深度校對，詞彙貼近台灣玩家閱讀習慣。

### 4. 智慧安裝與一鍵無痛還原
* 支援自動搜尋 Steam 安裝路徑。
* 自動備份英文原版檔案，一鍵還原無任何殘留。

---

## 🚀 快速開始

### 必備需求
* **作業系統**：Windows 10 / 11 (64-bit)
* **遊戲版本**：Steam 版《Sid Meier's Civilization IV: Beyond the Sword》(版本 3.19)

### 安裝步驟
1. 前往本專案 [Releases](https://github.com/Jordanplus/Civilaztion-4-BTS-Translate-to-Traditional-Chinese/releases) 下載最新的發布壓縮檔（`Civilaztion-4-BTS-Traditional-Chinese-Patch-v1.0.0.zip`）。
2. 解壓縮後進入資料夾。
3. **前置步驟**：若初次安裝，請先執行 `prerequisites/Civ4Bts_steam_japan.exe` 完成 CJK 支援環境安裝。
4. **安裝補丁**：滑鼠點擊 `install.bat`（或點右鍵選擇「以系統管理員身分執行」）。
5. 視窗顯示「安裝成功完成！」後，直接從 Steam 啟動遊戲即可！

### 解除安裝（還原英文原版）
* 執行資料夾中的 `uninstall.bat`，即可還原為乾淨官方原版。

---

## 📁 專案目錄結構

```text
Civilaztion-4-BTS-Translate-to-Traditional-Chinese/
├── docs/                           # 詳細技術文件與指南
│   ├── INSTALL_GUIDE.md            # 詳細安裝指引
│   ├── TROUBLESHOOTING.md          # 疑難排解 (Windows 10/11 閃退等)
│   └── ARCHITECTURE.md             # 技術架構與 NCR 編碼原理
├── scripts/                        # 開發與維護工具
│   ├── build_release.py            # 自動編譯與打包發布
│   ├── verify_xml.py               # XML 語法與編碼檢驗工具
│   ├── test_translations.py        # 關鍵詞彙測試腳本
│   └── install_to_steam.py         # 開發時一鍵安裝至 Steam
├── src/                            # 繁體中文原始文本 (XML 來源)
│   ├── base/                       # 主程式 Vanilla 文本 (17 個 XML)
│   ├── bts/                        # Beyond the Sword 文本 (29 個 XML)
│   └── warlords/                   # Warlords 文本 (7 個 XML)
├── patch/                          # 玩家發布包主體
│   ├── install.bat                 # 一鍵安裝啟動檔
│   ├── uninstall.bat               # 一鍵還原啟動檔
│   ├── prerequisites/              # CJK 雙位元組核心支援包
│   └── PatchFiles/                 # 補丁實際檔案與 PowerShell 引擎
└── dist/                           # 打包發布的 Release ZIP
```

---

## 🛠️ 開發與建置

若您希望參與翻譯修改或自行建置補丁包：

1. **環境配置**：
   * Python 3.10+
   * 安裝依賴：`pip install -r scripts/requirements.txt`
2. **驗證 XML 語法**：
   ```bash
   python scripts/verify_xml.py
   ```
3. **打包發布版本**：
   ```bash
   python scripts/build_release.py
   ```
   打包完成之檔案將產生於 `dist/` 目錄。

---

## 📜 授權協議 (License)
本專案代碼與轉換工具採用 [MIT License](LICENSE) 授權開源。
遊戲本身之一切版權歸 2K Games 與 Firaxis Games 所有。
