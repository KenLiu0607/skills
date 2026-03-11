# Agent Skills

這是一個專門存放 AI Agent 擴充技能的專案。透過這些預設好的技能設計，Agent 能夠為您處理各式各樣的任務，如文件格式轉接、流程自動化及資料分析等。專案開發秉持**低耦合、高擴充、易維護**的原則，並在原始碼中都有清楚的註解。

---

## 🛠️ 目前擁有的技能清單

本專案目前包含以下三個主要的技能模組，各資料夾內皆附有詳細的 `SKILL.md` 指南以供查閱。

### 1. [MarkItDown](./markitdown)

由微軟釋出的開源轉換工具，主要用來將多達 15 種以上的各式文件（PDF、Word(DOCX)、PPTX、Excel、圖片、音檔、網頁等）一鍵轉換為乾淨結構化的 Markdown 格式。

- **優勢**：Markdown 非常適合讓大語言模型 (LLM) 閱讀吸收，節省 Token 並保持架構清晰。
- **亮點**：不僅限於純文字提取，還支援利用 AI 進行圖片讀取 (OCR) 或解釋圖片內容，甚至可以完成音檔聽寫轉換與產生精美科學流程表。

### 2. [n8n Nodes 參考指南](./n8n-nodes)

這是一份針對 n8n 工作流 (Workflow) 自動化開發工具的快速參考手冊。

- **優勢**：快速協助查找與學習 n8n 核心邏輯節點與資料整理的特性與用法。
- **亮點**：羅列常用的重要節點如：邏輯判斷(If/Switch)、資料迴圈(Loop)、資料處理與合併(Merge、Filter) 以及與外部 API 互動(HTTP Request)。

### 3. [Notion to Docx](./notion2docx)

[![Python](https://img.shields.io/badge/python-3.8%2B-blue?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Word](https://img.shields.io/badge/Microsoft-Word-blue?style=for-the-badge&logo=microsoftword&logoColor=white)](#)
[![Pandoc](https://img.shields.io/badge/Pandoc-Supported-red?style=for-the-badge&logo=pandoc&logoColor=white)](https://pandoc.org)
[![Notion](https://img.shields.io/badge/Notion-Supported-red?style=for-the-badge&logo=notion&logoColor=white)](https://developers.notion.com)

**這是一個能幫您將指定的 Notion 頁面完美轉換成 Microsoft Word (.docx) 檔案的匯出工具。**

- **優勢**：最大程度地保留在 Notion 上耗費心力排版出來的精美版數、背景顏色與表格結構。

- **亮點**：自動將 LaTeX 數學公式無縫轉譯成 Word 內建可重新編輯的 OMML 方程式格式，且轉換出的成果可完美套用 Word 的標題大綱支援。

- **使用前準備**：
  為了確保轉換能順利進行，請確認您的執行環境具備以下條件：
    1. **安裝 Microsoft Word**：轉換過程需依賴本機 Word 進行排版渲染。
    2. **準備 Python 環境**：需具備 Python 以執行後台的自動化腳本。
    3. **安裝 Pandoc**：這是處理數學與化學方程式轉換時的必備工具。
    4. **設定 Notion API Key**：請取得您的 Notion 整合金鑰，並將其設定於系統環境變數中，授權工具讀取頁面內容。`NOTION_API_KEY:{your_api_key}`
- **使用方法**：
  告訴 AI 需要把 Notion 上的頁面轉成 Word 檔案, 剩下的 AI 會幫你完成。
