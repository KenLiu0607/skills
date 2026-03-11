---
name: communication-integration
description: 通訊與整合節點（Communication & Integration Nodes）是 n8n 工作流連接外部世界的核心。
---

## 1. HTTP Request 節點 (萬能 API 連接器)

這是 n8n 中最強大的節點之一，幾乎可以與任何提供 REST API 的服務通訊。

- **請求設定**：
    - **Method**：支援 GET, POST, PUT, PATCH, DELETE 等。
    - **URL**：支援動態表達式，例如 `https://api.service.com/users/{{ $json.userId }}`。
    - **Authentication**：內建多種認證方式，包括 Header Auth, Query Auth, Basic Auth, OAuth2 等。
- **進階功能**：
    - **Response Format**：可選擇 JSON、String 或 File（處理圖片/PDF 等二進位檔案）。
    - **Pagination**：支援處理分頁 API，自動循環獲取所有頁面的資料。
    - **Batching**：當需要對大量資料進行 API 請求時，可開啟批次處理模式以避免觸發速率限制。

## 2. Webhook 節點 (接收外部事件)

讓您的工作流能夠被外部系統（如 GitHub, Stripe, Typeform）觸發。

- **HTTP Method**：定義 Webhook 接收哪種類型的請求（通常為 POST）。
- **路徑與安全性**：
    - **Path**：自定義 Webhook 的 URL 路徑。
    - **Authentication**：可為 Webhook 加上認證，確保只有授權的請求能觸發工作流。
- **測試與生產環境**：
    - **Test URL**：用於開發調試，每次請求後會自動顯示資料。
    - **Production URL**：用於實際運行，必須手動「Activate」工作流後才生效。

## 3. Send Email 節點 (通知與通訊)

透過 SMTP 或特定服務（如 Gmail, Outlook）發送電子郵件。

- **內容設定**：
    - **HTML 支援**：可發送格式豐富的 HTML 郵件。
    - **附件 (Attachments)**：支援將上游節點產生的二進位檔案（如生成的 PDF 報告）作為附件發送。
- **動態收件人**：收件人、主旨和內容均可使用 `{{ $json.field }}` 動態填入。

## 4. Respond to Webhook 節點 (自定義響應)

當您使用 Webhook 觸發工作流時，可以使用此節點來回傳自定義的 HTTP 響應給發送方。

- **響應代碼**：自定義 HTTP 狀態碼（如 200 OK, 201 Created, 400 Bad Request）。
- **響應內容**：回傳 JSON、HTML 或純文字。這對於構建自定義 API 接口非常有用。

## 5. RSS Read / Feed Trigger 節點

監控與獲取網站更新。

- **RSS Read**：主動拉取特定 RSS Feed 的內容。
- **RSS Feed Trigger**：當 RSS Feed 有新內容更新時，自動觸發工作流。

## 6. 第三方整合節點 (Integration Nodes)

n8n 內建了數百個針對特定服務的節點，如：

- **Google Sheets**：讀寫試算表資料。
- **Slack**：發送訊息至頻道或使用者。
- **GitHub**：管理 Repo、Issue 或 Pull Request。
- **Discord**：透過 Webhook 或 Bot 發送訊息。

---

📖 **最佳實踐**：

- **憑證管理**：始終使用 n8n 的「Credentials」系統來管理 API Key 和密碼，切勿直接寫死在 URL 或 Header 中。
- **錯誤處理**：對於外部 API 請求，建議開啟「Retry On Failure」功能，以應對暫時性的網路波動。
- **安全性**：在公開 Webhook 時，務必加上認證機制或驗證請求來源的簽名（Signature）。
