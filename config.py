import os
from dotenv import load_dotenv

load_dotenv()

# Gmail API
GMAIL_CREDENTIALS_FILE = os.getenv("GMAIL_CREDENTIALS_FILE", "gmail_credentials.json")
GMAIL_TOKEN_FILE = os.getenv("GMAIL_TOKEN_FILE", "gmail_token.json")

# Notion API
NOTION_API_KEY = os.getenv("NOTION_API_KEY")
NOTION_DATABASE_ID = "2f0ed936-f4f7-80fb-a285-f9c8a0e89a1f"  # GS Citation Inbox

# Anthropic API
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

# Gmail polling interval (in seconds)
POLL_INTERVAL = 1 * 60  # 1 minute for testing

# Google Scholar sender email
GOOGLE_SCHOLAR_SENDER = "scholaralerts-noreply@google.com"

# Summarization prompt
SUMMARY_PROMPT = """Please read this paper and provide a structured summary that details the **core motivation** (what problem it solves and why existing methods fail), the **key methodology** (briefly explaining the technical approach, architecture, or loss function), and the **main contributions**. Summarize the **quantitative results**, specifically comparing them to previous baseline methods and highlighting the margin of improvement on key datasets. If available, explicitly analyze the **computational cost** (training vs. inference time, memory usage) and summarize the key takeaways from the **ablation studies** to identify which components contributed most to the performance gain. Finally, list any stated **limitations or assumptions** made by the authors. Also, noting the incorporation of guidance(CFG, how, what scale value.)"""
