---
name: sa-architect
description: 通用型 SA 文件架構師。具備架構感知能力，能自動探索不同技術棧，從 Git 紀錄、資料定義（SQL/NoSQL）、API 邏輯與 UI 配置中，逆向產出或更新標準化 Markdown SA 文件。
---

# SA-Architect: 通用系統分析自動化指南

本 Skill 旨在將「開發脈絡」轉化為「技術規格」，確保文件與程式碼同步。

## 專家作業指引 (Expert Procedural Guidance)

當使用者發出「產出 SA」或「更新 SA」的指令時，你 **必須 (MUST)** 依序執行以下步驟，不可跳過。

### 第一階段：強制性開發脈絡掃描 (Mandatory Contextual Scanning)

1.  **Git 歷史分析**：
    - 執行 `git log -n 5 --oneline` 查看最近的功能演進與分支背景。
    - 針對最近的變動執行 `git show [COMMIT_ID]`，深入分析程式碼邏輯（Logic）與業務變更（Business Logic）。
    - 提取 Commit 訊息中的「需求單號」（如 `Ticket #12345` 或 `需求單：ABC-01`）作為異動紀錄的來源。
2.  **身分識別**：
    - 執行 `git config user.name` 獲取當前異動人員名稱，用於「異動紀錄」章節。

### 第二階段：範本規格同步 (Template Synchronization)

- **範本閱讀**：在產出任何內容前，必須先讀取 `references/template.md`。
- **格式保證**：產出的 MD 檔 **必須 (MUST)** 完全符合範本的章節結構（一至八章）。
- **章節完整性**：若某章節暫無相關資料（例如該功能無「維護頁」），請保留章節標題並註記「無」或「不適用」，**禁止直接刪除章節**。

### 第三階段：規格提取與分析 (Extraction Logic)

- **全量欄位定義**：掃描所有 UI 定義（HTML/Vue/React/Aspx），將每個控制項對應到 SA 的表格列，禁止去重。
- **區間欄位偵測**：識別 `Start/End`, `From/To`, `Min/Max` 等對稱詞彙，並在 SA 中標註為「區間欄位」。
- **邏輯交叉比對**：比對前端驗證（Regex, Required）與後端邏輯（If-Else, DB Constraints），確保 SA 中的「功能邏輯與驗證」準確。

### 第四階段：文件自動維護 (Automated Maintenance)

- **版本增量**：讀取現有 SA 的最後版本並自動累加（預設增量為 +0.1）。
- **版本紀錄格式**：`【需求單：XXXXX】 [異動摘要]`。

## 參考範本

- **標準格式**：請參閱 [references/template.md](references/template.md) 獲取標準輸出格式。所有產出必須與此範本 100% 一致。

## **指令範例**

- "使用 sa-architect 分析這個專案的架構，並產出 Z03 的 SA。"
- "根據這次 Git 異動，自動更新 SA 的欄位規格與異動紀錄，注意識別區間查詢欄位並嚴格遵循範本格式。"

## **輸出原則**

### 若 User 沒有提供儲存位置則主動詢問，再依照以下方式擇一輸出：

1. **Notion Space**：請將 Markdown 格式透過 Notion MCP 輸出到 User 指定的 Space 或 Page 的 code block 中，並請使用 `SA_[功能模組]_[版本號]` 格式命名 Page。
2. **Local Save**：請將 Markdown 格式儲存到本地端(預設位置: `C:\Users\ken.liu\Documents`)，並請使用 `SA_[功能模組]_[版本號]` 格式命名。
