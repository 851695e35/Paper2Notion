# GS2Notion - Google Scholar to Notion Automation

Automate the process of tracking paper citations from Google Scholar and summarizing them to your Notion database.

## Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Set Up Environment Variables

Create a `.env` file in the project root:

```
GMAIL_CREDENTIALS_FILE=gmail_credentials.json
GMAIL_TOKEN_FILE=gmail_token.pickle
NOTION_API_KEY=your_notion_api_key
NOTION_DATABASE_ID=your_notion_database_id
ANTHROPIC_API_KEY=your_anthropic_api_key
```

### 3. Gmail Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project
3. Enable the Gmail API
4. Create OAuth 2.0 credentials (Desktop application)
5. Download the credentials JSON and save as `gmail_credentials.json`

### 4. Notion Setup

1. Go to [Notion Integrations](https://www.notion.so/my-integrations)
2. Create a new integration and get your API key
3. Share your "GS Citation Inbox" database with the integration
4. Get the database ID from the database URL

### 5. Anthropic API

Get your API key from [Anthropic Console](https://console.anthropic.com/)

## Running

```bash
python main.py
```

The script will:
- Poll Gmail every 6 hours for unread emails from Google Scholar
- Extract the paper title from each email
- Search for the paper content on arXiv
- Summarize it using Claude with your custom prompt
- Add the summary to your Notion database

Logs are saved to `gs2notion.log`

## Database Schema

Your Notion database should have these properties:
- **seed_paper** (Title): The original paper being cited
- **citing_title** (Text): The title of the new citing paper
- **summary** (Text): The AI-generated summary
- **gmail_msg_id** (Text): Gmail message ID for tracking
