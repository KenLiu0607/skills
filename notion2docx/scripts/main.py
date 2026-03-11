import os
import sys
import argparse
import shutil
import traceback

# 確保系統可以從 components 目錄匯入模組
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

def main():
    parser = argparse.ArgumentParser(description="Notion TO DOCX")
    parser.add_argument("id", help="Notion Page ID 或 Block ID (32 bit string)")
    parser.add_argument("-o", "--output-dir", required=True, help="Specify the output directory (required). A folder named block_id will be created in this directory.")
    
    args = parser.parse_args()
    
    # 延遲匯入，避免在執行 --help 時因為缺少 API Key 而崩潰
    from components.notion_api import search_notion_targets
    from components.page2html import parse_page
    from components.html2docx import convert_html_to_docx
    from components.math_injector import process_equations
    block_id = args.id  # 不移除 '-' 符號，這樣才能跟 Notion Search 取得的原生 ID (8-4-4-4-12) 比對
    
    # 在使用者指定的目錄下，建立以短版 block_id (去除-) 命名的資料夾
    clean_id = block_id.replace("-", "")
    output_dir = os.path.join(os.path.abspath(args.output_dir), clean_id)
    
    # 建立必要的目錄 (output_dir/{block_id}/)
    os.makedirs(output_dir, exist_ok=True)

    # --- 自動取得檔名邏輯 ---
    print(f"🔍 Searching for title for ID: {block_id}...")
    targets = search_notion_targets()
    # 支援帶橫線或不帶橫線的 ID 比對
    found_target = targets.get(block_id)
    if not found_target:
        # 嘗試去除橫線比對
        for tid, info in targets.items():
            if tid.replace("-", "") == clean_id:
                found_target = info
                break
    
    if found_target:
        output_filename = found_target.get("title", clean_id)
        print(f"✅ Found title: {output_filename}")
    else:
        output_filename = clean_id
        print(f"⚠️ Title not found in search results, fallback to ID: {output_filename}")

    # 稍微清理檔名，避免非法字元 (簡單處理)
    for c in '<>:"/\\|?*':
        output_filename = output_filename.replace(c, "_")
    
    # 中間產生的 docx 路徑 (暫存)
    target_docx = os.path.join(output_dir, f"{clean_id}_temp.docx")
    
    try:
        print(f"📦 Start processing Notion ID: {block_id}")
        
        # 步驟 1: 從 Notion 抓取內容並轉換為 HTML (存於 output_dir)
        print("=== Step 1: Generate HTML ===")
        # 從我們修改過的 parse_page 取得產生好的 html 絕對路徑
        output_html_path, math_html_path = parse_page(block_id, output_dir=output_dir)

        if not output_html_path or not os.path.exists(output_html_path):
            print("❌ Error: Unable to generate HTML file. Program aborted.")
            sys.exit(1)
            
        print(f"✅ HTML generation complete: {output_html_path}")
        
        # 步驟 2: 把暫存 HTML 交由 Word 轉換成 DOCX (存於 output_dir)
        print("\n=== Step 2: Use Word to convert HTML to DOCX ===")
        success = convert_html_to_docx(output_html_path, target_docx)
        
        if success:
            # 步驟 3: 方程式縫合
            print("\n=== Step 3: Extract and replace the original mathematical equations ===")
            final_docx = os.path.join(output_dir, f"{output_filename}.docx")
            inj_success = process_equations(math_html_path, target_docx, final_docx)
            
            if inj_success:
                print(f"\n🎉 Conversion successful! File location \n=> {final_docx}")
            else:
                print(f"\n⚠️ Word generation successful, but equation stitching skipped or failed：\n=> {target_docx}")
        else:
            print("\n❌ Error: DOCX conversion failed.")
            sys.exit(1)

    except ValueError as ve:
        # 特別處理缺少 API KEY 的例外
        print(f"\n❌ Setting error: {ve}")
        sys.exit(1)
    except Exception as e:
        print("\n❌ Unexpected system error:")
        traceback.print_exc()
        sys.exit(1)
        
    finally:
        # ====== 最終清理作業 ======
        # 依據最新需求，檔案保留在 doc/{block_id} 內，但只保留最終成果檔案，其餘刪除
        if 'output_dir' in locals() and os.path.exists(output_dir):
            # 確定最終要保留的檔名 (以免誤刪)
            final_name = os.path.basename(final_docx) if 'final_docx' in locals() else None
            for filename in os.listdir(output_dir):
                if filename != final_name:
                    file_path = os.path.join(output_dir, filename)
                    try:
                        if os.path.isfile(file_path):
                            os.remove(file_path)
                    except Exception as e:
                        print(f"Cleaning up discarded files failed: {file_path}, Error: {e}")

if __name__ == "__main__":
    main()
