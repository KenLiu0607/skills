# Skills

這是一個專門存放 AI Agent 擴充技能的專案。透過這些預設好的技能設計，Agent 能夠為您處理各式各樣的任務，專案開發秉持**低耦合、高擴充、易維護**的原則，並在原始碼中都有清楚的註解。

---

## notion2docx

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
