# 詳細安裝指南 (Installation Guide)

## 前提條件
1. 確保已於 Steam 安裝《Sid Meier's Civilization IV: Beyond the Sword》。
2. 建議在安裝補丁前，先啟動一次遊戲並確認能正常進入主畫面後關閉。

## 步驟詳解

### 第一步：準備可顯示中文的主程式
文明帝國 4 原始英文版無法直接渲染雙位元組字元（繁體中文、簡體中文、日文）。
本補丁不附原版主程式與日文 CJK 支援包。請自行準備可顯示雙位元組文字（中文）的主程式，放到與 `install.bat` 同一層的 `private\Civ4BeyondSword.exe`（在 repo 裡就是 `patch/private/`），安裝程式會自動套用。
沒有放這個檔案時，安裝程式仍會套用文字與美術，但遊戲畫面無法顯示中文。

臺灣文明的旗幟圖示會在安裝時從你自己遊戲附帶的 Road to War mod 複製（Steam 版 BtS 內建）。

### 第二步：套用繁體中文補丁
1. 進入 `patch/` 目錄。
2. 對 `install.bat` 按下滑鼠右鍵，點擊「以系統管理員身分執行」。
3. 安裝程式將會：
   * 自動搜尋您的 Steam 遊戲庫路徑（如 `C:\Program Files (x86)\Steam\steamapps\common\Sid Meier's Civilization IV Beyond the Sword`）。
   * 自動建立備份資料夾 `PatchFiles\Backup\`。
   * 將經過繁體化、NCR 安全編碼的文字檔複製至遊戲目錄；若有 `private\Civ4BeyondSword.exe`（與 `install.bat` 同一層）也一併套用。
   * 從你的遊戲目錄複製臺灣文明的旗幟圖示。
4. 終端機顯示「安裝成功完成！」後，按下任意鍵退出。

### 第三步：開始遊戲
* 從 Steam 正常啟動遊戲，遊戲主介面、百科、科技樹、地圖腳本即全數呈現繁體中文！
