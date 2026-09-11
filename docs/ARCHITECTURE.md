# 技術架構與 NCR 編碼原理 (Architecture & Technical Details)

## 遊戲文本架構
Civilization IV 的文字系統透過 XML 字典組織，分為三層繼承架構：
1. **Vanilla Core**：`Assets/XML/Text/`
2. **Warlords Expansion**：`Warlords/Assets/XML/Text/`
3. **Beyond the Sword Expansion**：`Beyond the Sword/Assets/XML/Text/`

BtS 載入時會優先讀取自身的 XML，並向後相容擴展。

## 為什麼採用 NCR (Numeric Character Reference)？
* **歷史背景**：原版 Civ4 釋出於 2005-2007 年代（Windows XP 時期），主要設計為 ISO-8859-1 單字元集。
* **MSXML 衝突**：現代 Windows 10/11 的 MSXML 3.0 解析器對多位元組編碼極為嚴苛。
* **NCR 的優勢**：
  * 每個繁體中文字元均被編碼為純 ASCII 十進制實體，例如「世界編輯器」編碼為：
    `&#19990;&#30028;&#32232;&#36655;&#22120;`
  * 檔案保持 `encoding="ISO-8859-1"`，完全由 ASCII 碼構成，任何 XML 解析器皆保證 100% 通過驗證。
  * 遊戲引擎內建的 GameTextManager 在顯示時會自動將 NCR 實體字元還原為 Unicode 點陣字型渲染。
