import os

# Notion API Key
NOTION_API_KEY = os.getenv('NOTION_API_KEY', '')

# Notion 對應的設定
DEFAULT_HTML_STYLE = """
        /* 基礎字體與版面設定 / Basic typography & layout */
        body { font-family: 'Microsoft JhengHei', '微軟正黑體', -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, "Apple Color Emoji", Arial, sans-serif, "Segoe UI Emoji", "Segoe UI Symbol"; padding: 2em; line-height: 1.5; color: #37352f; max-width: 900px; margin: 0 auto; }
        h1, h2, h3 { font-weight: 600; }
        .notion-h1 { font-size: 2em; margin-top: 1em; margin-bottom: 0.5em; }
        .notion-h2 { font-size: 1.5em; margin-top: 1em; margin-bottom: 0.5em; }
        .notion-h3 { font-size: 1.25em; margin-top: 1em; margin-bottom: 0.5em; }
        .notion-p { margin-top: 0.2em; margin-bottom: 0.2em; min-height: 1.5em; }
"""

# 字體顏色與背景顏色
TEXT_COLORS = {
    "default": "#373530",
    "gray": "#787774",
    "brown": "#976D57",
    "orange": "#CC782F",
    "yellow": "#C29343",
    "green": "#548164",
    "blue": "#487CA5",
    "purple": "#8A67AB",
    "pink": "#B35488",
    "red": "#C4554D",
    "code": "#C4554D",
}

BG_COLORS = {
    "default": "#FFFFFF",
    "gray": "#F1F1EF",
    "brown": "#F3EEEE",
    "orange": "#F8ECDF",
    "yellow": "#FAF3DD",
    "green": "#EEF3ED",
    "blue": "#E9F3F7",
    "purple": "#F6F3F8",
    "pink": "#F9F2F5",
    "red": "#FAECEC",
    "code": "#EDEDEB",
}

# Word 版面方向: 0 代表直式 (Portrait), 1 代表橫式 (Landscape)
WORD_ORIENTATION = 1

# Word 邊界設定 (單位為「磅」 Points, 1 公分約等於 28.35 磅) 常見值: 72 磅 = 1 英吋 = 2.54 公分
WORD_MARGIN_TOP = 72
WORD_MARGIN_BOTTOM = 72
WORD_MARGIN_LEFT = 72
WORD_MARGIN_RIGHT = 72



