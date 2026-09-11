# 疑難排解指南 (Troubleshooting)

## 1. 遊戲在載入 XML 時直接閃退 (Crash to Desktop)
* **原因**：文明 4 使用微軟 MSXML 3.0 解析 XML。在 Windows 10/11 的某些更新下，非 ASCII 編碼（如 GBK、Big5）常導致 MSXML 拋出記憶體例外。
* **解法**：本補丁已全數採用 ISO-8859-1 + 十進制 NCR 編碼（`&#...;`），徹底免疫此崩潰問題。若仍閃退，請檢查是否安裝了其他未經 NCR 轉換的第三方模組。

## 2. 遊戲文字顯示為問號「???」或方框「□□□」
* **原因**：未安裝雙字元 CJK 支援包，遊戲引擎缺少支援中文的字型設定與執行檔補丁。
* **解法**：執行 `patch/prerequisites/Civ4Bts_steam_japan.exe` 完成前置修補，然後重新執行 `patch/install.bat`。

## 3. 安裝時出現「存取被拒 (Access Denied)」
* **原因**：Steam 目錄位於 `C:\Program Files (x86)`，受到 Windows UAC 權限保護。
* **解法**：請務必對 `install.bat` 點擊滑鼠右鍵，選擇「以系統管理員身分執行」。

## 4. 如何完全還原至英文原版？
* 執行 `patch/uninstall.bat` 即可無痛還原備份之原始檔案。
* 或於 Steam 遊戲庫對遊戲右鍵 $ightarrow$「內容」$ightarrow$「已安裝檔案」$ightarrow$「驗證遊戲檔案完整性」。
