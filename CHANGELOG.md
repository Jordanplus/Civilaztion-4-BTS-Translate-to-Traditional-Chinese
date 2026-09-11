# 版本更新紀錄 (Changelog)

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
