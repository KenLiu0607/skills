import requests
import sys
import os

# 確保可以讀取到專案根目錄的 settings
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import settings
from settings import NOTION_API_KEY

# 如果系統中沒有設定 NOTION_API_KEY，強制拋出例外，交由最外層的 main.py 去捕捉處理
if not NOTION_API_KEY:
    raise ValueError("Error: NOTION_API_KEY not found. Please provide a valid Notion API key in the environment variables.")

HEADERS = {
    "Authorization": f"Bearer {NOTION_API_KEY}",
    "Notion-Version": "2022-06-28",
}

def fetch_children(block_id, target_dict=None):
    """
    向 Notion API 請求，抓取指定區塊 (block_id) 底下的所有「子區塊 (children)」。
    """

    url = f"https://api.notion.com/v1/blocks/{block_id}/children"

    try:
        response = requests.get(url, headers=HEADERS)

        if response.status_code != 200:
            print(f"❌ Notion API request failed. (Status: {response.status_code}): {url}")
            if response.status_code == 404:
                print("👉 提示：ID not found. Please check if the ID is correct.")
            elif response.status_code == 403:
                print("👉 提示：Permission denied. Please check if the Notion Integration has been shared with the page.")
        response.raise_for_status()

        return response.json().get('results', [])
    except Exception as e:
        print(f"Error fetching children for block {block_id}: {e}")
        return []

def retrieve_database(database_id, target_dict=None):
    """
    拿這個資料庫「本身的設定」(如資料庫標題、欄位定義、是否有 data_sources 等)。
    """
    
    url = f"https://api.notion.com/v1/databases/{database_id}"
    try:
        response = requests.get(url, headers=HEADERS)
        if response.status_code != 200:
            print(f"==ID is not identified as a database. Proceeding to fetch as a Page ID.==")
        response.raise_for_status()
        return response.json()
    except Exception as e:
        # print(f"Error retrieving database {database_id}: {e}")
        return {}

def query_database(database_id, target_dict=None):
    """
    查詢一般的 Notion 資料庫 (Database) 中的所有記錄 (Row 行資料)。
    """

    url = f"https://api.notion.com/v1/databases/{database_id}/query"
    try:
        response = requests.post(url, headers=HEADERS)
        if response.status_code != 200:
            print(f"❌ Notion API request failed. (Status: {response.status_code}): {url}")
        response.raise_for_status()
        return response.json().get('results', [])
    except Exception as e:
        print(f"Error querying database {database_id}: {e}")
        return []

def query_data_source(data_source_id, target_dict=None):
    """
    查詢 Notion Linked Database (Data Source) 中的所有記錄。
    主要用於 child_database 回傳只含有 data_sources 且沒有實體內容的狀況。
    注意：在較新的 Notion API 版本中，部分關聯資料庫可能需要直接打這個 endpoint。
    """
    url = f"https://api.notion.com/v1/databases/{data_source_id}/query" 
    # ^ 註：官方文件上仍是打 databases/{id}/query。即使它是 data_source，也當作 db 來 query。
    try:
        response = requests.post(url, headers=HEADERS)
        response.raise_for_status()
        return response.json().get('results', [])
    except Exception as e:
        print(f"Error querying data source {data_source_id}: {e}")
        return []


def search_notion_targets():
    """
    呼叫 Notion Search API，自動化找出所有已授權的 Root 節點和核心 Database，
    回傳一個整理過的字典結構供後續主程式應用與防呆使用：
    {
        "id": {
            "type": "page" 或 "database",
            "id": "xxxx",
            "title": "節點標題"
        }
    }
    """
    url = "https://api.notion.com/v1/search"
    # 用空的 payload ，預設會找所有 page 與 database
    payload = {}

    try:
        response = requests.post(url, headers=HEADERS, json=payload)
        response.raise_for_status()
        results = response.json().get('results', [])
        
        targets = {}
        for item in results:
            obj_type = item.get("object", "")
            item_id = item.get("id", "")
            parent = item.get("parent", {})

            # 1. 忽略根節點 (Workspace) 
            if parent.get("type") == "workspace":
                continue

            # 2. 忽略一般資料庫儲存的資料列項目 (Database child)
            #    注意：只有當本身是 page (例如 row item) 且 parent 是 database_id 時才忽略
            if obj_type == "page" and parent.get("type") in ["database_id", "data_source_id"]:
                continue

            # 3. 取得標題
            title_text = "Unknown_Title"
            if obj_type == "page":
                properties = item.get("properties", {})
                title_prop = properties.get("title", {})
                print(title_prop)

                
                if title_prop and "title" in title_prop:
                    title_arr = title_prop.get("title", [])
                    if title_arr:
                         title_text = "".join([t.get("plain_text", "") for t in title_arr])
            elif obj_type in ["database", "data_source"]:
                title_arr = item.get("title", [])
                if title_arr:
                    title_text = "".join([t.get("plain_text", "") for t in title_arr])
            
            # 4. 統一歸類為 page 或 database
            unified_type = "page" if obj_type == "page" else "database"
            
            if not title_text or title_text == "Unknown_Title":
                title_text = f"Unknown_{unified_type}_{item_id[-6:]}"

            targets[item_id] = {
                "type": unified_type,
                "id": item_id,
                "title": title_text
            }
            
        return targets
        
    except Exception as e:
        print(f"❌ Error searching notion targets: {e}")
        return {}

