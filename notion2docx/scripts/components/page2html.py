import json
import os
import requests
import sys
import latex2mathml.converter
from settings import TEXT_COLORS, BG_COLORS, DEFAULT_HTML_STYLE
from components import notion_api

# 儲存本次轉換過程中遇到的所有方程式
_math_blocks = []

def reset_math_blocks():
    global _math_blocks
    _math_blocks = []

def add_math_block(mathml):
    global _math_blocks
    math_id = f"MATH_{len(_math_blocks):03d}"
    _math_blocks.append({"id": math_id, "mathml": mathml})
    return math_id


def parse_rich_text(rich_text_array):
    """
    負責解析 Notion 返回的「文本」(含有樣式裝飾的文字群組) 陣列，把它變成 HTML 字串。
    舉例：Notion 文字常常是一段話裡面有粗體、有斜體，它會切成陣列分開標示，這個函式會負責組合回去。
    """
    if not rich_text_array:
        return ""
    
    html_content = ""
    # 針對陣列中的每一段文句進行處理
    for rt in rich_text_array:
        # 判斷是普通文字還是行內公式 (inline equation)
        if rt.get('type') == 'equation':
            expression = rt.get('equation', {}).get('expression', '')
            try:
                # 處理 notion API 拿到的雙反斜線問題
                clean_expr = expression.replace("\\\\", "\\")
                mathml = latex2mathml.converter.convert(clean_expr)
                math_id = add_math_block(mathml)
                text = f"[MATH_PLACEHOLDER: {math_id}]"
            except Exception as e:
                print(f"Math convert error: {e}")
                text = f"\\({expression}\\)"
        else:
            # 讀出文字內容，順便將換行字元 \n 取代為 HTML <br> 標籤
            text = rt.get('text', {}).get('content', '').replace('\n', '<br>')
            
        # 讀出這段文字含有哪些排版標籤 (粗斜體、底線等)
        annotations = rt.get('annotations', {})
        
        # 套用 HTML 的加粗標籤 (Strong) 與斜體標籤 (em) 等
        if annotations.get('bold'):
            text = f"<strong>{text}</strong>"
        if annotations.get('italic'):
            text = f"<em>{text}</em>"
        if annotations.get('strikethrough'):
            text = f"<s>{text}</s>"
        if annotations.get('underline'):
            text = f"<u>{text}</u>"
            
        # ==========================================
        # 處理文字顏色與背景顏色 (包含 Code 樣式覆蓋邏輯)
        # ==========================================
        is_code = annotations.get('code', False)
        color_prop = annotations.get('color', 'default')
        
        # 1. 先決定最終要使用的文字色與背景色
        final_text_color = ""
        final_bg_color = ""
        
        if is_code:
            # Code 的基底配色
            final_text_color = TEXT_COLORS.get('code')
            final_bg_color = BG_COLORS.get('code')
            
            # 使用者若有替 Code 額外設定顏色，則覆蓋它
            if color_prop != 'default':
                if color_prop.endswith('_background'):
                    base_color = color_prop.replace('_background', '')
                    final_bg_color = BG_COLORS.get(base_color, BG_COLORS['default'])
                else:
                    final_text_color = TEXT_COLORS.get(color_prop, TEXT_COLORS['default'])
        else:
            # 一般文字的配色 (不是 Code)
            if color_prop != 'default':
                if color_prop.endswith('_background'):
                    base_color = color_prop.replace('_background', '')
                    final_bg_color = BG_COLORS.get(base_color, BG_COLORS['default'])
                else:
                    final_text_color = TEXT_COLORS.get(color_prop, TEXT_COLORS['default'])

        # 2. 開始組合 CSS Style 字串
        style_parts = []
        if final_text_color:
            style_parts.append(f"color: {final_text_color};")
        if final_bg_color:
            style_parts.append(f"background-color: {final_bg_color};")
            
        # 3. 根據是 Code 還是普通文字，套用不同的 padding 與標籤
        if style_parts or is_code:
            style_str = " ".join(style_parts)
            if is_code:
                # Code 專屬的額外排版
                style_str += " padding: 0.2em 0.4em; border-radius: 3px; font-family: monospace;"
                text = f'<code style="{style_str}">{text}</code>'
            else:
                # 一般裝飾顏色的排版
                if final_bg_color: 
                    style_str += " padding: 2px;"
                text = f'<span style="{style_str}">{text}</span>'
                
        # ==========================================

        # 如果這段文字是一個超連結網址，幫它加上被點擊的 HTML <a> 標籤
        link = rt.get('text', {}).get('link')
        if link:
            url = link.get('url', '#')
            text = f'<a href="{url}">{text}</a>'
            
        html_content += text
        
    return html_content

def parse_property(prop):
    """
    將 Notion "資料庫 (Database)” 裡的一格一格儲存格 (Property) 轉換為 HTML 內容。
    由於每個儲存格可以設定成標籤 (Select)、文字區塊、核取方塊等，所以這裡用 if/elif 來分門別類處理。
    """
    prop_type = prop.get('type')
    
    # Title 型別通常是表格中最重要的一欄(名稱)
    if prop_type == 'title':
        return parse_rich_text(prop.get('title', []))
    
    # Rich Text 型別是表格中的文本欄位
    elif prop_type == 'rich_text':
        return parse_rich_text(prop.get('rich_text', []))
        
    # Status 是如 Todo、In Progress 這種系統狀態標籤
    elif prop_type == 'status':
        status = prop.get('status', {})
        name = status.get('name', '')
        color = status.get('color', 'default') # 抓取顏色
        hex_bg = BG_COLORS.get(color, BG_COLORS['default'])
        hex_text = TEXT_COLORS.get(color, TEXT_COLORS['default']) if color != 'default' else '#FFFFFF'
        return f'<span class="notion-status" style="border-radius: 3px; padding: 2px 6px; background-color: {hex_bg}; color: {hex_text}; font-size: 0.9em;">{name}</span>'
        
    # Select 是一個自訂義的單選標籤
    elif prop_type == 'select':
        select = prop.get('select', {})
        name = select.get('name', '')
        return f'<span class="notion-select">{name}</span>'
        
    # Multi-select 則是支援多選標籤的陣列，並繪製每一個標籤外框
    elif prop_type == 'multi_select':
        selects = prop.get('multi_select', [])
        res = []
        for s in selects:
            color = s.get('color', 'default')
            hex_bg = BG_COLORS.get(color, BG_COLORS['default'])
            hex_text = TEXT_COLORS.get(color, TEXT_COLORS['default']) if color != 'default' else '#333333'
            res.append(f'<span class="notion-multi-select" style="margin-right: 4px; border-radius: 3px; padding: 2px 6px; background-color: {hex_bg}; color: {hex_text}; border: 1px solid #ccc; font-size: 0.85em;">{s.get("name", "")}</span>')
        return "".join(res)
        
    # 純數字顯示
    elif prop_type == 'number':
        return str(prop.get('number', ''))
        
    # 日期屬性解析
    elif prop_type == 'date':
        date_obj = prop.get('date', {})
        start = date_obj.get('start', '')
        end = date_obj.get('end', '')
        if end:
            return f"{start} → {end}"
        return start
        
    # 核取方塊 Checkbox (用 Emoji 取代 HTML 以達相容性)
    elif prop_type == 'checkbox':
        checked = prop.get('checkbox', False)
        return "☑️" if checked else "🔲"
        
    # 單純網址
    elif prop_type == 'url':
        url = prop.get('url', '')
        return f'<a href="{url}">{url}</a>'
        
    # 遇到尚未支援解析的屬性，預設會留下空白
    return ""

def parse_database_to_html(database_id, default_title):
    """
    負責把整個資料庫 (Database) 的結構轉出為一個精美的 HTML `<table>`。
    因為 Notion 裡面的資料庫常常是以網格 (Grid) 出現的。
    """
    # 1. 拿資料庫標題與結構設定
    db_info = notion_api.retrieve_database(database_id)
    title_arr = db_info.get('title', [])
    db_title = parse_rich_text(title_arr) if title_arr else default_title
    
    # 2. 判斷是否有 data_sources (例如它是個 Linked Database)
    data_sources = db_info.get("data_sources", [])
    if data_sources and len(data_sources) > 0:
        # 有時候它是個關聯資料庫視圖，拿第一組 data_source_id 出來取代原本的查詢 ID
        query_id = data_sources[0].get("id")
        print(f"  -> Detected data_source! Original DB ID: {database_id}, Querying Data Source ID: {query_id}")
        records = notion_api.query_data_source(query_id)
    else:
        # 原本一般的資料庫查詢
        records = notion_api.query_database(database_id)
        
    if not records:
        return f'<div class="notion-database" id="{database_id}"><strong>🗃️ Database: {db_title}</strong> (No data)</div>'
    
    # 3. 提取所有欄位名稱 (Columns)，透過第一筆資料的 Key 值建立
    first_props = records[0].get('properties', {})
    columns = list(first_props.keys())
    
    # 小技巧：如果這張表有標題欄 (Title) 的話，主動把它排到最左邊(第一個)
    title_col = next((col for col, val in first_props.items() if val.get('type') == 'title'), None)
    if title_col and title_col in columns:
        columns.remove(title_col)
        columns.insert(0, title_col)
        
    # 4. 開始組合 Table 結構
    html = f'<div class="notion-database" id="{database_id}" style="margin-bottom: 1em;">'
    html += f'<h4 style="margin-bottom: 0.5em;">🗃️ {db_title}</h4>'
    html += '<table style="width: 100%; border-collapse: collapse; border: 1px solid #ddd;">'
    
    # 加入表頭 (Header Row)
    html += '<thead style="background-color: #f7f7f7;"><tr>'
    for col in columns:
        html += f'<th style="border: 1px solid #ddd; padding: 8px; text-align: left;">{col}</th>'
    html += '</tr></thead>'
    
    # 加入表身資料 (Body Rows)
    html += '<tbody>'
    for record in records: # 跑過每一行
        html += '<tr>'
        props = record.get('properties', {})
        for col in columns: # 對每一行的每個對應欄位去 Parse，填入 <td>
            prop_data = props.get(col, {})
            cell_html = parse_property(prop_data)
            html += f'<td style="border: 1px solid #ddd; padding: 8px;">{cell_html}</td>'
        html += '</tr>'
    html += '</tbody></table></div>'
    
    return html


# ============================================================
# Block Handler 函式區
# 每個 handler 負責將特定類型的 Notion Block 轉為對應 HTML。
# 簽名統一為：(block, block_data, html_content, children_html) -> str
# ============================================================

def _handle_paragraph(block, block_data, html_content, children_html):
    """一小段普通的文字"""
    block_id = block.get('id')
    return f'<p class="notion-p" id="{block_id}">{html_content}{children_html}</p>'


def _handle_heading_1(block, block_data, html_content, children_html):
    """最大號黑色粗體大寫標題"""
    block_id = block.get('id')
    return f'<h1 class="notion-h1" id="{block_id}">{html_content}{children_html}</h1>'


def _handle_heading_2(block, block_data, html_content, children_html):
    """中號標題"""
    block_id = block.get('id')
    return f'<h2 class="notion-h2" id="{block_id}">{html_content}{children_html}</h2>'


def _handle_heading_3(block, block_data, html_content, children_html):
    """小號標題"""
    block_id = block.get('id')
    return f'<h3 class="notion-h3" id="{block_id}">{html_content}{children_html}</h3>'


def _handle_callout(block, block_data, html_content, children_html):
    """醒目提示區塊 (附帶 Emoji 及白灰色背景)"""
    block_id = block.get('id')
    icon = block_data.get('icon', {})
    icon_html = ""
    # 特殊處理裡頭包含的 Icon Emoji
    if icon.get('type') == 'emoji':
        icon_html = f'<span class="notion-callout-icon" style="font-size: 1.2em; margin-right: 0.5em;">{icon.get("emoji")}</span>'
    elif icon.get('type') == 'external':
        icon_url = icon.get('external', {}).get('url')
        icon_html = f'<img class="notion-callout-icon" src="{icon_url}" alt="icon" style="width: 24px; height: 24px; margin-right: 0.5em;">'

    return f'<div class="notion-callout" id="{block_id}" style="padding: 1em; border-radius: 4px; background-color: #f1f1f1; display: flex; align-items: flex-start; margin-bottom: 1em;">\n{icon_html}\n<div style="flex-grow: 1;">{html_content}{children_html}</div>\n</div>'


def _handle_child_database(block, block_data, html_content, children_html):
    """如果是插入到頁面的整包關聯資料庫，block ID 就是 Notion API 上的 Database_ID"""
    block_id = block.get('id')
    title = block_data.get('title', 'Database')
    print(f"Parsing database {block_id}...")
    return parse_database_to_html(block_id, title)


def _handle_bulleted_list_item(block, block_data, html_content, children_html):
    """帶黑點的列表項目"""
    block_id = block.get('id')
    return f'<li class="notion-li" id="{block_id}">{html_content}{children_html}</li>'


def _handle_numbered_list_item(block, block_data, html_content, children_html):
    """有編碼的列表項目 (1. 2. 3.)"""
    block_id = block.get('id')
    return f'<li class="notion-li" id="{block_id}">{html_content}{children_html}</li>'


def _handle_code(block, block_data, html_content, children_html):
    """程式碼區塊"""
    block_id = block.get('id')
    bg_color = BG_COLORS.get('code')
    text_color = TEXT_COLORS.get('code')
    return f'<div class="notion-code" id="{block_id}" style="background-color: {bg_color}; color: {text_color}; padding: 1em; border-radius: 4px; font-family: monospace; white-space: pre-wrap; margin-bottom: 1em;">{html_content}</div>'


def _handle_table(block, block_data, html_content, children_html):
    """普通的繪整表格 (Table) 外層，自行管理子結構（不使用通用 children 遞迴）"""
    block_id = block.get('id')
    print(f"Fetching rows for table ({block_id})...")
    rows = notion_api.fetch_children(block_id)
    has_col_header = block_data.get('has_column_header', False)
    has_row_header = block_data.get('has_row_header', False)

    # 標記特殊行(標題) (如果有開啟標題設定的話)
    table_content = ""
    for i, row in enumerate(rows):
        if row.get('type') == 'table_row':
            row_data = row.get('table_row', {})
            cells = row_data.get('cells', [])
            cells_html = ""
            for j, cell_rich_text in enumerate(cells):
                cell_content = parse_rich_text(cell_rich_text)
                is_header = (has_col_header and i == 0) or (has_row_header and j == 0)
                tag = "th" if is_header else "td"
                bg_color = "#f7f7f7" if is_header else "transparent"
                cells_html += f'<{tag} class="notion-{tag}" style="border: 1px solid #ccc; padding: 0.5em; min-width: 100px; background-color: {bg_color}; text-align: left;">{cell_content}</{tag}>'
            table_content += f'<tr class="notion-tr" id="{row.get("id")}">\n{cells_html}\n</tr>\n'

    # 表格外層加上 overflow wrapper 以及 table 專屬標籤
    return f'<div style="overflow-x: auto; margin-bottom: 1em;"><table class="notion-table" id="{block_id}" style="border-collapse: collapse; min-width: 100%; border: 1px solid #ccc;">\n<tbody>\n{table_content}</tbody>\n</table></div>'


def _handle_table_row(block, block_data, html_content, children_html):
    """如果因為某種原因單獨解析 table_row，保留備援機制"""
    return ""


def _handle_equation(block, block_data, html_content, children_html):
    """數學公式區塊"""
    block_id = block.get('id')
    expression = block_data.get('expression', '')
    try:
        # 處理 notion API 拿到的雙反斜線問題
        clean_expr = expression.replace("\\\\", "\\")
        mathml = latex2mathml.converter.convert(clean_expr)
        math_id = add_math_block(mathml)
        return f'<div class="notion-equation" id="{block_id}" style="padding: 1em; background-color: #f7f7f7; text-align: center; border-radius: 4px; overflow-x: auto; margin: 1em 0; font-family: KaTeX_Math, math, serif;">\n[MATH_PLACEHOLDER: {math_id}]\n</div>'
    except Exception as e:
        print(f"Math convert error: {e}")
        return f'<div class="notion-equation" id="{block_id}" style="padding: 1em; background-color: #f7f7f7; text-align: center; border-radius: 4px; overflow-x: auto; margin: 1em 0; font-family: KaTeX_Math, math, serif;">\\[ {expression} \\]</div>'


def _handle_quote(block, block_data, html_content, children_html):
    """引用區塊"""
    block_id = block.get('id')
    return f'<blockquote class="notion-quote" id="{block_id}" style="border-left: 3px solid currentColor; padding-left: 14px; margin: 1em 0;">{html_content}{children_html}</blockquote>'


def _handle_to_do(block, block_data, html_content, children_html):
    """待辦事項 (Checkboxes)"""
    block_id = block.get('id')
    checked = block_data.get('checked', False)
    # 簡單用 Emoji 呈現勾選狀態（也可換成 HTML input checkbox）
    check_symbol = "☑️" if checked else "🔲"
    # 為了美觀加一點刪除線樣式
    text_style = "text-decoration: line-through; opacity: 0.6;" if checked else ""
    return f'<div class="notion-todo" id="{block_id}" style="margin: 0.2em 0;"><span style="margin-right:0.5em;">{check_symbol}</span><span style="{text_style}">{html_content}</span>{children_html}</div>'


def _handle_divider(block, block_data, html_content, children_html):
    """分隔線"""
    block_id = block.get('id')
    return f'<hr class="notion-divider" id="{block_id}" style="border: none; border-top: 1px solid #ccc; margin: 1.5em 0;" />'


def _handle_toggle(block, block_data, html_content, children_html):
    """摺疊式清單 (用 HTML details/summary 原生支援)"""
    block_id = block.get('id')
    return f'<details class="notion-toggle" id="{block_id}" style="margin: 0.5em 0;"><summary style="cursor: pointer; font-weight: 500;">{html_content}</summary><div style="padding-left: 1.5em; margin-top: 0.5em;">{children_html}</div></details>'


def _handle_child_page(block, block_data, html_content, children_html):
    """子頁面連結，不支援遞迴下載整頁子頁面，只提供一個連結按鈕的樣式顯示它在那邊"""
    block_id = block.get('id')
    title = block_data.get('title', 'Child Page')
    return f'<div class="notion-child-page" id="{block_id}" style="padding: 0.5em 1em; border: 1px solid #ddd; border-radius: 4px; display: inline-block; margin-bottom: 0.5em;">📄 <strong>{title}</strong></div>'


# ============================================================
# Block Handler 註冊表
# 新增 Block 類型時，只需：1) 寫一個 _handle_xxx 函式  2) 加到這張表中
# ============================================================
_BLOCK_HANDLERS = {
    'paragraph':          _handle_paragraph,
    'heading_1':          _handle_heading_1,
    'heading_2':          _handle_heading_2,
    'heading_3':          _handle_heading_3,
    'callout':            _handle_callout,
    'child_database':     _handle_child_database,
    'bulleted_list_item': _handle_bulleted_list_item,
    'numbered_list_item': _handle_numbered_list_item,
    'code':               _handle_code,
    'table':              _handle_table,
    'table_row':          _handle_table_row,
    'equation':           _handle_equation,
    'quote':              _handle_quote,
    'to_do':              _handle_to_do,
    'divider':            _handle_divider,
    'toggle':             _handle_toggle,
    'child_page':         _handle_child_page,
}


def parse_block(block):
    """
    核心遞迴函式。這個函式判斷傳入的每一個 Notion 結構區塊 (Block) 是什麼類型，然後轉為對應的 HTML 元素。
    如果這個區塊包含子項目 (has_children: true)，則會觸發對自己本身的「遞迴呼叫 (Recursion)」。
    透過 _BLOCK_HANDLERS 註冊表進行查表分派，新增類型只需加入 handler 函式與註冊表即可。
    """
    block_type = block.get('type')
    block_id = block.get('id')
    has_children = block.get('has_children', False)

    # 把實際包含資訊的部分拉出來
    block_data = block.get(block_type, {})

    # Notion 大部分區塊都有這段：獲取標題或是文本，先轉為 HTML 字串
    rich_text = block_data.get('rich_text', [])
    html_content = parse_rich_text(rich_text)

    # ==== 判斷遞迴 (核心難點) ==== #
    # 如果這個區塊底下有縮排了另外很多段落呢？這時候需要去透過網路請求，把下層段落要出來
    children_html = ""
    if has_children and block_type != 'table':  # 避開 table, 因為 table 要自訂子結構
        print(f"Fetching children for {block_type} ({block_id})...")
        children_blocks = notion_api.fetch_children(block_id)
        # 用遞迴方式，反覆地去組合所有下屬文字區塊
        children_html = "\n".join([parse_block(child) for child in children_blocks])

    # ==== 透過註冊表分派對應的 handler ==== #
    handler = _BLOCK_HANDLERS.get(block_type)
    if handler:
        return handler(block, block_data, html_content, children_html)

    # 當遇到 Notion 其他未來會出的怪異系統方塊或我們未編寫處理機制的項目
    # 如果裡面有文字的話，還是勉強把它用 <div> 包裝顯示出來避免資料遺失
    if html_content or children_html:
        return f'<div class="notion-unsupported" id="{block_id}">{html_content}{children_html}</div>'
    return ""

def parse_page(page_id, output_dir=None):
    """
    程式實際開始工作的起點函式：接收 Notion Page_ID 或 Database_ID，轉為 HTML。
    """
    if output_dir is None:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        output_dir = os.path.join(script_dir, "doc")

    reset_math_blocks()

    print(f"Starting fetch for Notion ID: {page_id}")
    
    # 嘗試判定這是不是一個資料庫 (直接向 Notion 請求 database info)
    is_database = False
    db_title = "Exported Database"
    
    try:
        # 直接拿這個 ID 當作 database 查詢看看
        # 如果不是 database，Notion API 會拋出 exception
        db_info = notion_api.retrieve_database(page_id)
        if db_info and db_info.get("object") == "database":
            is_database = True
            title_arr = db_info.get("title", [])
            if title_arr:
                db_title = "".join([t.get("plain_text", "") for t in title_arr])
    except Exception:
        # 發生錯誤代表他不是 Database 或者是權限不足，退回視為一般的 Page 處理
        pass
            
    if is_database:
        print(f"  -> Detected as Database. Parsing table structure directly...")
        # 建立一個假的 block 讓迴圈或結構能直接處理這個資料庫 HTML
        db_html = parse_database_to_html(page_id, db_title)
        blocks = [{"type": "_raw_html", "content": db_html}]
    else:
        # 不是資料庫，那就當作一般頁面，抓取底下的 blocks
        blocks = notion_api.fetch_children(page_id)
            

    # 如果真的連資料也沒有抓到
    if not blocks:
        print("No blocks found or fetched. Exiting.")
        return None, None

    # 計算存放位置並創造對應名詞的新 HTML 檔案位置
    output_file = os.path.join(output_dir, f"{page_id.replace('-', '')}.html")
    # Python 預防創建目的地資料夾不存在發生錯誤用，自動建立所需的子資料夾
    if not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)
        
    try:
        # 定義一張合格網頁檔案開頭必須寫的基本標籤 HTML + CSS Reset 結構樣式設定
        html_output = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Notion Block Export</title>
    <style>
{DEFAULT_HTML_STYLE}
    </style>
</head>
<body>
"""
        
        # 這兩個布林值變數主要是去判定：這群文字是否一直連續是清單項目？
        in_bullet_list = False
        in_number_list = False
        
        # 把這頁最外層大陣列跑過一遍
        for block in blocks:
            b_type = block.get('type')
            
            # 如果是 Database 的特別注入 HTML (剛剛在上面產生的)
            if b_type == '_raw_html':
                html_output += block.get('content', '') + "\n"
                continue
                
            # --- 以下兩段處理在網頁中用 <ul> 與 <ol> 連續包覆清單項目 <li> 的切換邊界處理 ---
            if b_type == 'bulleted_list_item' and not in_bullet_list:
                html_output += "<ul>\n" # 第一項開始
                in_bullet_list = True
            elif b_type != 'bulleted_list_item' and in_bullet_list:
                html_output += "</ul>\n" # 後方被一般文字截斷了，關閉標籤
                in_bullet_list = False
                
            if b_type == 'numbered_list_item' and not in_number_list:
                html_output += "<ol>\n"
                in_number_list = True
            elif b_type != 'numbered_list_item' and in_number_list:
                html_output += "</ol>\n"
                in_number_list = False
                
            # 將上述遞迴寫好的字串吐入這個網頁骨幹中附著
            html_output += parse_block(block) + "\n"
            
        # 防止結束以前還沒被截除到下一個非清單物件時的漏網之魚正常關閉標籤
        if in_bullet_list: html_output += "</ul>\n"
        if in_number_list: html_output += "</ol>\n"
            
        html_output += "</body>\n</html>"
        
        # I/O 動作寫入硬體：執行真正的寫檔到系統資料夾中
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_output)
            
        print(f"✅ Successfully exported to {output_file}")
        
        # 產生 math_library.html 檔案，準備給 Pandoc 轉成原生公式
        math_file = os.path.join(output_dir, "math_library.html")
        math_html = '<!DOCTYPE html>\n<html>\n<head><meta charset="utf-8"></head>\n<body>\n'
        for mb in _math_blocks:
            math_html += f'<p>[ID: {mb["id"]}]</p>\n'
            math_html += f'<p>{mb["mathml"]}</p>\n'
        math_html += '</body>\n</html>'
        
        with open(math_file, 'w', encoding='utf-8') as f:
            f.write(math_html)
            
        print(f"✅ Math library exported to {math_file}")
        
        # 回傳包含兩個檔案路徑的 tuple
        return output_file, math_file
        
    except Exception as e:
        print(f"Error during export: {e}")
        raise e

# 程式設計中，這句能讓其他代碼只在 "純測試直接執行這支檔案時" 才去跑解析指令
# 若是被當作副程式引用的時候則不會自動呼叫
if __name__ == "__main__":
    # 將命令列支援模組引路進來
    import sys
    # sys.argv 內存使用者命令列輸入的值；小於 2 代表使用者只寫了 "python a.py"，少給了附帶參數
    if len(sys.argv) < 2:
        print("Usage: python parse_blocks_to_html.py <page_id>")
        sys.exit(1) # 跳錯給系統知道這有問題，強制終止程式
    
    # 使用者有填資料：把輸入第一順位當作指定的 Page_ID 塞進執行參數裡面並觸發。
    page_id = sys.argv[1]
    parse_page(page_id)
