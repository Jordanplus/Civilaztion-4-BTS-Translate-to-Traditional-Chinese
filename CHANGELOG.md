# 版本更新紀錄 (Changelog)

## [Unreleased] - 2026-09-28
### 🌍 新增巨型世界地圖：「The Earth」(124x68 Huge Map)
* **全模式支援**：同步產出 `The Earth.CivBeyondSwordWBSave` 與 `The Earth.py`，支援「自定義遊戲」(Custom Game) 地圖選單、「進行劇本」(Play A Scenario) 及「自定義劇本」(Custom Scenario)。
* **官方極限尺寸**：採用遊戲引擎允許之最大官方世界尺寸（`WORLDSIZE_HUGE`，124 x 68，共 8,432 地塊），完整重現各大洲山川水系、海峽關隘與資源分佈。
* **18 大文明歷史真位**：嚴謹還原世界 18 大文明發祥地（埃及、印度、中國、台灣、羅馬、波斯、日本、德國、蒙古、法國、阿拉伯、西班牙、英國、俄羅斯、馬利、印加、阿茲特克、美國）。替換地中海過度擁擠之希臘，平衡歐洲發展空間。
* **台灣文明進駐澳洲**：考量台灣本島腹地狹窄，將台灣文明開局改設於幅員遼闊的澳洲大陸東南部（雪梨流域起步，坐標 118, 16），配置河川淡水、海港雙漁產（生蠔、魚產）、小麥農田、牛羊牧場與大分水嶺金銀煤鐵礦藏，並由 4 名開拓者展開大洋洲爭霸！

### 🔒 不再散布原版檔案
* 從 repo 與整個 git 歷史移除原版主程式（`Civ4BeyondSword.exe`）、日文 CJK 支援包（`Civ4Bts_steam_japan.exe`），以及 26 個和遊戲安裝內容相同的美術檔。
* 雙位元組主程式改由玩家自行準備（`private\` 資料夾不進 git，也不會被打包進 Release）。
* 那 26 個美術檔中，目前的 XML 只用到 2 個臺灣旗幟圖示，改成安裝時從遊戲附帶的 Road to War mod 複製（清單見 `patch/PatchFiles/game_art_sources.csv`，含 SHA-1 檢查）；其餘 24 個自 03181f8 改用自製 2D 肖像後已不再被引用，直接移除。
* 雙位元組主程式放到與 `install.bat` 同一層的 `private\` 資料夾；安裝程式在複製失敗或缺檔時會如實顯示「安裝未完成」。
* `install.ps1` 改存成含 BOM 的 UTF-8：Windows PowerShell 5.1 讀取沒有 BOM 的腳本時會用系統的 ANSI 編碼，中文字串可能讓整支腳本無法執行。

## [v1.0.0] - 2026-09-11
### 💥 重大技術修復 (Major Fixes)
* **全面 NCR 編碼化**：將所有 XML 文本轉換為 ISO-8859-1 十進制 Numeric Character References，徹底解決 Windows 10/11 上 MSXML 3.0 解析錯誤導致啟動閃退問題。
* **重構 CIV4GameTextInfos_Objects.xml**：清洗修復 729 處因早期 GBK/Latin-1 混淆產生的嚴重亂碼。
* **女領袖文字修復**：修正凱薩琳、伊莉莎白、哈特謝普蘇特、伊莎貝拉、維多利亞等女性領袖因 XML 結構嵌套導致名稱與背景故事遺失的 Bug。
* **移除日文殘留補丁**：移除 `ZPATCH_CIV4GameText_JP_Fixtext.xml`，防止字串被日文字元覆蓋。

### 🎨 翻譯與在地化優化 (Localization Improvements)
* **世界編輯器 (WorldBuilder)**：
  * 主選單與暫停選單：`TXT_KEY_POPUP_ENTER_WB` 由「進入世界建立器」改為「世界編輯器」。
  * 介面與控制：`TXT_KEY_WORLD_BUILDER` 改為「世界編輯器」，退出按鈕改為「退出世界編輯器」。
  * 載入提示與文明百科：提示訊息與百科條目全面統稱「世界編輯器」。
* **夢幻國度 (Fantasy Realm) 地圖腳本**：
  * 修正 `TXT_KEY_MAP_SCRIPT_LOGICAL` 為「合乎常理」。
  * 修正 `TXT_KEY_MAP_SCRIPT_IRRATIONAL` 為「反常分佈」（原誤譯為不均）。
  * 修正 `TXT_KEY_MAP_SCRIPT_CRAZY` 為「狂亂模式」（原誤譯為混亂）。
* **台灣繁體化**：經 OpenCC `s2twp` 詞庫全域校對，符合台灣用語習慣。

* **新增「臺灣文明」(CIVILIZATION_TAIWAN)**：
  * 正統青天白日滿地紅國旗（3D 旗幟與專屬 UI 按鈕）。
  * 初始科技：捕魚 ＋ 採礦。
  * 特色單位：諸葛弩；特色建築：養生堂。
  * 完整收錄臺灣主要縣市名錄（臺北、高雄、臺中、臺南、新竹、桃園等）。
  * **新增領袖：蔣經國**（特質：勤奮＋理財；喜好市政：國家重商主義；配備專屬 3D 外交模型）。
  * **新增領袖：蔡英文**（特質：保國＋理財；喜好市政：自由市場；配備 Civ4 藝術風格精美肖像立繪）。

### 📦 安裝程式升級 (Installer)
* 升級 `install.ps1` 與 `uninstall.ps1`，支援自動偵測 Steam 預設庫與自訂庫路徑。
* 提供無亂碼、相容性佳的 ASCII `install.bat` 與 `uninstall.bat`，支援管理員身分自動提權。
* 自動備份機制：安裝前完整備份官方英文原版檔案，解除安裝時 100% 原樣還原。
