---
name: n8n-nodes
description: n8n 核心節點與常用整合節點的快速參考指南。用於：查找 n8n 節點功能、了解參數設定、學習常用資料處理模式以及參考核心邏輯節點用法。
---

# n8n Nodes Quick Reference

使用此技能來快速獲取 n8n 核心節點的詳細說明與使用模式。

## 核心邏輯節點

| 節點                    | 功能描述                              | 關鍵參數 / 模式                                                           |
| :---------------------- | :------------------------------------ | :------------------------------------------------------------------------ |
| **If**                  | 根據布林條件將工作流分為兩路。        | `Conditions`: 支援多種比較運算（String, Number, Boolean）。               |
| **Switch**              | 根據多個條件或表達式將工作流分流。    | `Routing Rules`: 支援數值範圍、正則表達式或精確匹配。                     |
| **Loop Over Items**     | 將輸入項目拆分為批次（Batches）處理。 | `Batch Size`: 每次循環處理的項目數量。                                    |
| **Merge**               | 合併來自兩個輸入源的資料。            | `Mode`: Append（追加）, Merge By Key（按鍵合併）, Multiplex（笛卡爾積）。 |
| **Wait**                | 暫停工作流執行。                      | `Wait Amount`: 秒、分、小時；`Resume`: 支                                 |
| 援 Webhook 或特定時間。 |

## 資料處理節點 (Data Transformation)

- **Edit Fields (Set)**: 用於新增、更新或刪除欄位。
    - _模式_：使用 `{{ $json.field }}` 表達式來引用上游資料。
- **Code**: 執行 JavaScript 或 Python 程式碼。
    - _JavaScript_: 使用 `items.map(item => { ... return item; })` 處理資料。
    - _Python_: 使用 `return [item for item in items]`。
- **Aggregate**: 將多個項目聚合為一個。
    - _功能_：加總 (Sum)、平均 (Average)、合併為陣列 (Array)。
- **Filter**: 根據條件保留或移除項目。
- **Sort**: 根據一個或多個欄位對項目進行排序。

## 通訊與整合 (Communication & Integration)

- **HTTP Request**: 與外部 API 互動。
    - _設定_：Method (GET, POST, etc.), URL, Headers, Body (JSON/Form-Data)。
    - _認證_：支援 Header Auth, Query Auth, OAuth2 等。
- **Send Email**: 發送電子郵件。
    - _設定_：SMTP 伺服器、收件人、主旨、內容（支援 HTML）。
- **Webhook**: 接收外部請求。
    - _注意_：生產環境使用 `/webhook/`，測試環境使用 `/webhook-test/`。

## 檔案處理 (File Handling)

- **Read/Write Files from Disk**: 直接操作主機檔案。
- **Convert to File**: 將 JSON 資料轉換為檔案（如 CSV, XLSX）。
- **Extract From File**: 從二進位檔案中提取內容（如 PDF 文字, 圖片資訊）。

## 最佳實踐

1. **節點命名**：始終為節點取一個描述性的名稱（例如：`Filter Active Users` 而非 `Filter`）。
2. **錯誤處理**：在重要節點上配置 `On Error -> Continue` 或 `On Error -> Error Trigger` 以增強穩定性。
3. **表達式優化**：儘量在節點設置中使用表達式而非在 Code 節點中寫死，以提高可維護性。

## 各節點詳細用法

- 核心邏輯節點 : core-logic.md
- 資料處理節點 : data-transformation.md
- 通訊與整合 : communication-integration.md
- 檔案處理 : file-handling.md

## 節點使用方式

- workflow-example.json

---

📖 **需要更深入的資訊？** 請訪問 [n8n 官方文檔](https://docs.n8n.io/integrations/builtin/node-types/)。
