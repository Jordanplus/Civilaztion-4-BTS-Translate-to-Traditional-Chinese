# 詳細安裝指南 (Installation Guide)

## 前提條件
1. 確保已於 Steam 安裝《Sid Meier's Civilization IV: Beyond the Sword》。
2. 建議在安裝補丁前，先啟動一次遊戲並確認能正常進入主畫面後關閉。

## 步驟詳解

### 第一步：安裝 CJK 雙字元支援前置包
文明帝國 4 原始英文版無法直接渲染雙位元組字元（繁體中文、簡體中文、日文）。
1. 進入 `patch/prerequisites/` 目錄。
2. 執行 `Civ4Bts_steam_japan.exe`。
3. 按照安裝畫面指示進行安裝（若跳出路徑選擇，請選擇您的遊戲主目錄）。

### 第二步：套用繁體中文補丁
1. 進入 `patch/` 目錄。
2. 對 `install.bat` 按下滑鼠右鍵，點擊「以系統管理員身分執行」。
3. 安裝程式將會：
   * 自動搜尋您的 Steam 遊戲庫路徑（如 `C:\Program Files (x86)\Steam\steamapps\common\Sid Meier's Civilization IV Beyond the Sword`）。
   * 自動建立備份資料夾 `PatchFiles\Backup\`。
   * 將經過繁體化、NCR 安全編碼的文字檔與執行檔複製至遊戲目錄。
4. 終端機顯示「安裝成功完成！」後，按下任意鍵退出。

### 第三步：開始遊戲
* 從 Steam 正常啟動遊戲，遊戲主介面、百科、科技樹、地圖腳本即全數呈現繁體中文！
