---
name: file-handling
description: 檔案處理節點（File Handling Nodes）負責管理 n8n 工作流中的二進位資料（Binary Data）。無論是處理圖片、PDF 報告，還是進行 CSV 與 JSON 之間的轉換，這些節點都是不可或缺的工具。
---

## 1. Read/Write Files from Disk 節點

直接與運行 n8n 的主機檔案系統進行互動。

- **Read From Disk**：從指定路徑讀取檔案並將其轉換為 n8n 的二進位屬性。
- **Write To Disk**：將上游的二進位資料儲存到主機的特定目錄。
- **注意**：在使用 Docker 部署時，務必確保已正確掛載（Mount）磁碟卷，否則工作流將無法存取主機路徑。

## 2. Convert to File 節點

將結構化的 JSON 資料轉換為可下載或發送的檔案格式。

- **支援格式**：CSV, XLSX (Excel), HTML, JSON, PDF (透過特定組件)。
- **應用場景**：將資料庫查詢結果轉換為 Excel 報表，並透過 Email 發送給團隊。
- **二進位屬性 (Binary Property)**：您可以自定義生成的檔案在工作流中的屬性名稱（預設為 `data`）。

## 3. Extract From File 節點

從二進位檔案中提取內容，將其轉換回可處理的 JSON 資料。

- **支援操作**：
    - **CSV/XLSX**：將試算表行轉換為 n8n 項目。
    - **PDF**：提取 PDF 中的文字內容。
    - **Images**：提取圖片的元數據（Metadata）。
- **編碼設定**：支援自定義檔案編碼（如 UTF-8, Big5），確保中文字元不會出現亂碼。

## 4. Compression 節點 (壓縮與解壓縮)

處理 ZIP 或 TAR 檔案。

- **Compress**：將多個二進位檔案打包成一個壓縮檔。
- **Decompress**：解放壓縮檔內容，將其中的每個檔案作為獨立的二進位項目輸出。
- **應用場景**：批次下載多張圖片後，打包成 ZIP 檔上傳至雲端硬碟。

## 5. FTP / SFTP 節點

與遠端伺服器進行檔案傳輸。

- **功能**：支援 Upload (上傳), Download (下載), List (列出檔案), Delete (刪除), Rename (重命名)。
- **安全性**：建議使用 SFTP (SSH File Transfer Protocol) 以確保傳輸過程的加密安全。

## 6. Edit Image 節點

對圖片進行基本的處理操作。

- **操作**：Resize (調整大小), Crop (裁剪), Rotate (旋轉), Watermark (加浮水印)。
- **格式轉換**：支援在 JPEG, PNG, WEBP 等格式間轉換。

---

📖 **進階技巧：處理二進位資料**

- **記憶體管理**：處理大型檔案（如 100MB 以上的影片）時，請注意 n8n 伺服器的記憶體限制。
- **二進位與 JSON 的切換**：在 n8n 中，資料分為 `JSON`（結構化文字）和 `Binary`（檔案）。大多數檔案處理流程都涉及這兩者之間的轉換。
- **多檔案處理**：若一個項目包含多個二進位檔案，可使用 `Split Out` 節點將其拆分為多個獨立項目分別處理。
