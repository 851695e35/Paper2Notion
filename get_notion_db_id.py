#!/usr/bin/env python
"""Get Notion database ID"""
from notion_client import Client
from config import NOTION_API_KEY

notion = Client(auth=NOTION_API_KEY)

try:
    # Search for databases
    response = notion.search(query="GS Citation Inbox", filter={"value": "database", "property": "object"})

    print("Found databases:")
    for result in response.get("results", []):
        if result["object"] == "database":
            db_id = result["id"]
            title = result.get("title", [{}])[0].get("plain_text", "Untitled")
            print(f"  - {title}: {db_id}")

except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
