from notion_client import Client
from config import NOTION_API_KEY, NOTION_DATABASE_ID
from datetime import datetime

notion = Client(auth=NOTION_API_KEY)

def add_to_notion_database(seed_paper: str, citing_title: str, summary: str, tldr: str = "", gmail_msg_id: str = "",
                          citing_url: str = "", authors: str = ""):
    """Add entry to Notion database with the new structure.

    Database fields:
    - page (title): The name of the new paper (citing_title)
    - seed_paper: The original paper being cited
    - TLDR: One-sentence summary
    - url: Link to the arXiv paper
    - Gmail Msg ID: Email message ID
    - date_received: When the email was received
    - summary: Full summary (stored as child block content, plain text, ~1200 tokens)
    """
    try:
        # Truncate fields to Notion's limits
        page_title = citing_title[:100] if citing_title else ""
        seed_paper_truncated = seed_paper[:100] if seed_paper else ""
        tldr_truncated = tldr[:500] if tldr else ""

        properties = {
            "title": {
                "title": [
                    {
                        "text": {
                            "content": page_title
                        }
                    }
                ]
            },
            "seed_paper": {
                "rich_text": [
                    {
                        "text": {
                            "content": seed_paper_truncated
                        }
                    }
                ]
            },
            "TLDR": {
                "rich_text": [
                    {
                        "text": {
                            "content": tldr_truncated
                        }
                    }
                ]
            },
            "Gmail Msg ID": {
                "rich_text": [
                    {
                        "text": {
                            "content": gmail_msg_id
                        }
                    }
                ]
            },
            "date_received": {
                "date": {
                    "start": datetime.now().isoformat()
                }
            }
        }

        # Add URL if provided
        if citing_url:
            properties["url"] = {
                "url": citing_url
            }

        # Create the main page
        page = notion.pages.create(
            parent={"database_id": NOTION_DATABASE_ID},
            properties=properties
        )

        page_id = page['id']

        # Add the summary as child block content (plain text, no markdown)
        # Notion has a 2000 character limit per text block, so split into multiple blocks
        summary_text = summary if summary else ""

        if summary_text:
            # Split summary into chunks of max 1900 characters
            chunk_size = 1900
            chunks = [summary_text[i:i+chunk_size] for i in range(0, len(summary_text), chunk_size)]

            children = []
            for chunk in chunks:
                children.append({
                    "object": "block",
                    "type": "paragraph",
                    "paragraph": {
                        "rich_text": [
                            {
                                "type": "text",
                                "text": {
                                    "content": chunk
                                }
                            }
                        ]
                    }
                })

            notion.blocks.children.append(
                block_id=page_id,
                children=children
            )

        print(f"Successfully added to Notion: {citing_title}")
        return True
    except Exception as e:
        print(f"Error adding to Notion: {e}")
        return False
