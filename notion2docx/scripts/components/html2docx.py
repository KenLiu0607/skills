import os
import sys

try:
    import win32com.client
except ImportError:
    print("錯誤：找不到 win32com 模組。請執行 'pip install pywin32' 來安裝。")
    sys.exit(1)

def convert_html_to_docx(html_path, docx_path):
    """
    使用 Microsoft Word (透過 win32com) 將 HTML 檔案轉換為 DOCX 格式。
    這可以在最大程度上保留 HTML 內的表格結構與樣式。
    """
    # win32com 必須使用絕對路徑，否則 Word 可能找不到檔案
    html_abspath = os.path.abspath(html_path)
    docx_abspath = os.path.abspath(docx_path)
    
    if not os.path.exists(html_abspath):
        print(f"Error: The specified HTML file could not be found.'{html_path}'")
        return False

    # 若輸出檔案已存在，嘗試先刪除避免 Word 另存新檔時被擋（如前次轉換失敗造成）
    if os.path.exists(docx_abspath):
        try:
            os.remove(docx_abspath)
        except Exception as e:
            print(f"Error: Unable to overwrite or delete the existing file '{docx_path}'. It's possible that another program (such as Word itself) is using it.")
            return False

    # 建立或連接到 Word 應用程式
    try:
        word = win32com.client.Dispatch('Word.Application')
        word.Visible = False # 在背景安靜執行，不跳出 Word 視窗
    except Exception as e:
        print(f"Error: Unable to start Microsoft Word. Please ensure that Office Word is installed on your computer. Detailed error: {e}")
        return False

    try:
        print(f"[1/3] Opening HTML via Word: {html_path} ...")
        # 讓 Word 開啟 HTML 檔案
        doc = word.Documents.Open(html_abspath)
        
        print(f"[2/3] Saving file as DOCX: {docx_path} ...")
        
        # 套用來自 settings 的版面與邊界設定
        try:
            # 確保 Python 認識根目錄
            sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            import settings
            
            doc.PageSetup.Orientation = settings.WORD_ORIENTATION
            doc.PageSetup.TopMargin = settings.WORD_MARGIN_TOP
            doc.PageSetup.BottomMargin = settings.WORD_MARGIN_BOTTOM
            doc.PageSetup.LeftMargin = settings.WORD_MARGIN_LEFT
            doc.PageSetup.RightMargin = settings.WORD_MARGIN_RIGHT
        except ImportError:
            print("[WARNING] Unable to load components.settings layout settings. Word defaults will be used instead.")
        except Exception as e:
            print(f"[WARNING] Error applying layout settings: {e}. Word defaults will be used instead.")
        # 將文件另存為 Word 格式 (wdFormatXMLDocument = 16)
        # 參數 FileFormat=16 代表 .docx
        doc.SaveAs2(docx_abspath, FileFormat=16)
        
        # 關閉目前文件
        doc.Close()
        print("[3/3] Conversion successful!")
        return True
        
    except Exception as e:
        print(f"Error during conversion process: {e}")
        return False
        
    finally:
        # 無論成功或失敗，最後一定要確保把背景的 Word 應用程式關閉，避免佔用記憶體
        try:
            word.Quit()
        except:
            pass

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python html2docx.py <input_html_path> [output_docx_path]")
        print("Example: python html2docx.py doc/31aa.html")
        sys.exit(1)
        
    input_html = sys.argv[1]
    
    # 如果使用者沒有指定輸出的檔名，自動以相同的檔名替換副檔名為 .docx
    if len(sys.argv) >= 3:
        output_docx = sys.argv[2]
    else:
        # 分離檔名與副檔名，把 .html 改成 .docx
        base_name = os.path.splitext(input_html)[0]
        output_docx = f"{base_name}.docx"
        
    convert_html_to_docx(input_html, output_docx)
