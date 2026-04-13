# 技能列表 (Skills)

此目錄存放了開發輔助相關的 AI Agent 技能。透過這些技能，Agent 能夠自動化處理複雜的技術任務，並確保產出符合一致的規格與標準。

---

## 1. ppt-compress
- **簡介**：專門用於壓縮 PPT/PPTX 檔案大小。適合需要分享或上傳大型簡報檔案的場景。
- **核心功能**：
    - **解壓分析**：將 PPTX 視為 ZIP 格式解壓以提取媒體檔案。
    - **圖片壓縮**：自動壓縮超過 1MB 的圖片。
    - **格式轉換**：重新打包並使用 LibreOffice 轉換為體積更小的 PDF 版本。
- **依賴工具**：Python 3, sips (macOS 內建), LibreOffice。

## 2. sa-architect
- **簡介**：具備架構感知能力的通用型 SA 文件工具。能從開發脈絡中逆向產出或更新標準化的 Markdown SA 文件。
- **核心階段**：
    - **開發脈絡掃描**：分析 Git 歷史紀錄（Log/Show）與異動人員，提取業務邏輯。
    - **範本規格同步**：嚴格遵循 `references/template.md` 的章節結構。
    - **規格提取**：掃描 UI 配置（Vue/React/HTML）與 DB 定義，比對前後端驗證邏輯。
    - **自動化維護**：自動更新版本紀錄與需求單號。
- **輸出原則**：支援輸出至 Notion Space 或本地端目錄。

## 3. sql-optimization
- **簡介**：跨資料庫（MySQL, PostgreSQL, SQL Server, Oracle）的通用 SQL 性能優化助手。
- **優化領域**：
    - **查詢分析**：識別低效的查詢模式並提供優化建議。
    - **索引策略**：針對複合索引、覆蓋索引（Covering Index）與部分索引進行優化設計。
    - **架構改進**：包含子查詢轉視窗函數、JOIN 順序調校、分頁優化（Cursor-based）以及批次操作建議。
    - **反模式識別**：偵測 `SELECT *`、WHERE 子句中的函數調用等影響效能的寫法。


## 4. notion2docx

[![Python](https://img.shields.io/badge/python-3.8%2B-blue?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Word](https://img.shields.io/badge/Microsoft-Word-blue?style=for-the-badge&logo=microsoftword&logoColor=white)](#)
[![Pandoc](https://img.shields.io/badge/Pandoc-Supported-red?style=for-the-badge&logo=pandoc&logoColor=white)](https://pandoc.org)
[![Notion](https://img.shields.io/badge/Notion-Supported-red?style=for-the-badge&logo=notion&logoColor=white)](https://developers.notion.com)

**這是一個能幫您將指定的 Notion 頁面完美轉換成 Microsoft Word (.docx) 檔案的匯出工具。**

**優勢**：最大程度地保留在 Notion 上耗費心力排版出來的精美版數、背景顏色與表格結構。

**亮點**：自動將 LaTeX 數學公式無縫轉譯成 Word 內建可重新編輯的 OMML 方程式格式，且轉換出的成果可完美套用 Word 的標題大綱支援。

**使用前準備**：為了確保轉換能順利進行，請確認您的執行環境具備以下條件：

1. **安裝 Microsoft Word**：轉換過程需依賴本機 Word 進行排版渲染。
   
2. **準備 Python 環境**：需具備 Python 以執行後台的自動化腳本。
   
3. **安裝 Pandoc**：這是處理數學與化學方程式轉換時的必備工具。
   
4. **設定 Notion API Key**：請取得您的 Notion 整合金鑰，並將其設定於系統環境變數中，授權工具讀取頁面內容。`NOTION_API_KEY:{your_api_key}`
   
- **使用方法**：
  告訴 AI 需要把 Notion 上的頁面轉成 Word 檔案, 剩下的 AI 會幫你完成。

## 5. git commit

`git commit` 指令用於將暫存區（staging area）中的變更永久地記錄到版本歷史中。每次提交都應該代表一個邏輯上獨立的變更單元，並附帶一個清晰、簡潔且具描述性的提交訊息（commit message）。

#### 如何使用

1.  **暫存變更**: 在提交之前，您需要使用 `git add` 指令將您希望包含在提交中的檔案變更新增到暫存區。
    ```bash
    git add . # 暫存所有變更的檔案
    git add <file_name> # 暫存特定檔案
    ```

2.  **執行提交**:
    *   **帶訊息提交**: 使用 `-m` 旗標直接在指令中提供提交訊息。
        ```bash
        git commit -m "feat: 新增使用者登入功能"
        ```
    *   **開啟編輯器提交**: 如果不帶 `-m` 旗標，Git 會開啟預設的文字編輯器讓您撰寫詳細的提交訊息。
        ```bash
        git commit
        ```

#### 提交訊息的慣例 (Conventional Commits)

為了保持提交歷史的清晰和一致性，建議遵循「Conventional Commits」規範。這有助於自動生成變更日誌、簡化專案維護，並促進團隊協作。

基本格式為：

```
<type>(<scope>): <subject>

[<body>]

[<footer>]
```

*   **`<type>` (類型)**：
    *   `feat`: 新增功能。
    *   `fix`: 錯誤修復。
    *   `docs`: 文件變更。
    *   `style`: 不影響程式碼執行邏輯的格式變更 (空白、格式化、分號等)。
    *   `refactor`: 程式碼重構，不新增功能也不修復錯誤。
    *   `perf`: 效能優化。
    *   `test`: 新增或修改測試。
    *   `build`: 影響建構系統或外部依賴的變更 (例如 npm, gulp, broccoli)。
    *   `ci`: CI 配置或腳本的變更。
    *   `chore`: 其他不修改源碼或測試文件的變更 (例如更新 grunt 任務、package.json)。
    *   `revert`: 回溯到之前的提交。

*   **`<scope>` (範圍 - 可選)**：
    表示此次變更影響的範圍或模組 (例如 `authentication`, `parser`, `ui`, `database`)。

*   **`<subject>` (主題)**：
    *   簡潔的單行描述，使用祈使句 (例如 "change" 而不是 "changed" 或 "changes")。
    *   首字母小寫。
    *   結尾不要句號。

*   **`<body>` (正文 - 可選)**：
    提供更詳細的變更說明，解釋 *為什麼* 進行此變更，而不是 *如何* 變更。每行字數建議不超過 72 字元。

*   **`<footer>` (註腳 - 可選)**：
    *   用於引用相關的 issue 或 PR 號碼 (例如 `Closes #123`, `Fixes #456`)。
    *   標記 `BREAKING CHANGE`，表示引入了不兼容的 API 變更。

**範例:**

```
feat(user): 新增使用者註冊流程

- 實現新的使用者註冊表單。
- 增加電子郵件驗證機制。

Closes #789
```

#### 提示

*   **原子提交**: 每次提交只包含一個邏輯變更。
*   **清晰描述**: 提交訊息應該讓人即使不看程式碼也能理解變更的目的。
*   **定期提交**: 頻繁地提交小的變更，而不是一次性提交大量變更。

---





