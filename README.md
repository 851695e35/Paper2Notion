# Paper2Notion - Gmail to Notion Paper Citation Pipeline

Automatically fetch paper citations from Google Scholar emails, extract all citing papers, generate AI-powered summaries with intelligent TLDRs, and add them to your Notion database.

## Features

- 📧 **Gmail Integration**: Automatically polls Google Scholar Alert emails
- 📚 **Multi-Paper Extraction**: Extracts all citing papers from each email (not just one)
- 🤖 **AI Summarization**: Uses Claude to generate comprehensive paper summaries
- 💡 **Intelligent TLDR**: Generates proper one-sentence summaries (not naive truncation)
- 📝 **Notion Database**: Automatically adds papers with metadata to your Notion workspace
- ⏰ **Scheduled Processing**: Runs every 6 hours automatically

## Prerequisites

- Python 3.8+
- Google Account with Gmail
- Notion Account
- Anthropic API Key (Claude)

## Installation

### Step 1: Clone the Repository

```bash
git clone https://github.com/851695e35/Paper2Notion.git
cd Paper2Notion
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

## Configuration

### Step 1: Gmail Setup (OAuth 2.0)

1. **Create a Google Cloud Project**
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Click "Select a Project" → "New Project"
   - Enter project name: `Paper2Notion`
   - Click "Create"

2. **Enable Gmail API**
   - In the Google Cloud Console, go to "APIs & Services" → "Library"
   - Search for "Gmail API"
   - Click on it and press "Enable"

3. **Create OAuth 2.0 Credentials**
   - Go to "APIs & Services" → "Credentials"
   - Click "Create Credentials" → "OAuth client ID"
   - If prompted, configure the OAuth consent screen first:
     - User Type: External
     - Add required scopes: `https://www.googleapis.com/auth/gmail.modify`
   - Application type: Desktop application
   - Click "Create"

4. **Download Credentials**
   - Click the download icon next to your created credential
   - Save the JSON file as `gmail_credentials.json` in the project root

### Step 2: Notion Setup

1. **Create a Notion Integration**
   - Go to [Notion Integrations](https://www.notion.so/my-integrations)
   - Click "New Integration"
   - Name: `Paper2Notion`
   - Click "Submit"
   - Copy the "Internal Integration Token" (you'll need this)

2. **Create a Notion Database**
   - In Notion, create a new database with the following properties:
     - **名称** (Title): Paper title
     - **seed_paper** (Text): The original paper being cited
     - **url** (URL): Link to the paper on arXiv
     - **TLDR** (Text): One-sentence summary
     - **date_received** (Date): When the email was received
     - **Gmail Msg ID** (Text): Gmail message ID for tracking

3. **Share Database with Integration**
   - Open your Paper2Notion database in Notion
   - Click "Share" → "Invite"
   - Select your `Paper2Notion` integration
   - Click "Invite"

4. **Get Database ID**
   - Open your database in Notion
   - Copy the URL: `https://www.notion.so/[DATABASE_ID]?v=[VIEW_ID]`
   - The `DATABASE_ID` is the long string before the `?`
   - Format it as: `[first 8 chars]-[next 4 chars]-[next 4 chars]-[next 4 chars]-[last 12 chars]`
   - Example: `a1b2c3d4-e5f6-g7h8-i9j0-k1l2m3n4o5p6`

### Step 3: Anthropic API Setup

1. **Get API Key**
   - Go to [Anthropic Console](https://console.anthropic.com/)
   - Sign up or log in
   - Go to "API Keys"
   - Click "Create Key"
   - Copy your API key

### Step 4: Environment Variables

Create a `.env` file in the project root with your credentials:

```env
GMAIL_CREDENTIALS_FILE=gmail_credentials.json
GMAIL_TOKEN_FILE=gmail_token.pickle
NOTION_API_KEY=your_notion_internal_integration_token
NOTION_DATABASE_ID=your_notion_database_id
ANTHROPIC_API_KEY=your_anthropic_api_key
GOOGLE_SCHOLAR_SENDER=scholaralerts-noreply@google.com
SUMMARY_PROMPT=Provide a comprehensive summary of this paper including: 1) Main contribution 2) Methodology 3) Key results 4) Significance
```

### Step 5: Gmail Authentication

Run the setup script to authenticate with Gmail:

```bash
python setup_gmail.py
```

This will:
1. Open a browser window for you to authorize the application
2. Save the OAuth token to `gmail_token.pickle`
3. You only need to do this once

## Running the Application

### Option 1: Run Once

```bash
python main.py
```

This will process all unread Google Scholar emails once and exit.

### Option 2: Run as Scheduled Service (Windows)

Use the provided batch file:

```bash
run_gs2notion.bat
```

This will run the application with automatic 6-hour polling.

### Option 3: Run as Background Service (Linux/Mac)

```bash
nohup python main.py > gs2notion.log 2>&1 &
```

## How It Works

1. **Email Polling**: Checks Gmail every 6 hours for unread emails from Google Scholar
2. **Paper Extraction**: Extracts all citing papers from each email
3. **Content Fetching**: Searches arXiv for each paper's full text or abstract
4. **Summarization**: Uses Claude to generate comprehensive summaries
5. **TLDR Generation**: Creates intelligent one-sentence summaries
6. **Notion Upload**: Adds papers to your Notion database with all metadata
7. **Email Marking**: Marks processed emails as read

## Notion Database Schema

Your Notion database should have these properties:

| Property | Type | Description |
|----------|------|-------------|
| 名称 | Title | Paper title (auto-filled) |
| seed_paper | Text | The original paper being cited |
| url | URL | Link to the paper on arXiv |
| TLDR | Text | One-sentence AI-generated summary |
| date_received | Date | When the email was received |
| Gmail Msg ID | Text | Gmail message ID for tracking |

## Troubleshooting

### Gmail Authentication Issues

- **"Gmail credentials not found"**: Run `python setup_gmail.py` again
- **"Invalid credentials"**: Delete `gmail_token.pickle` and run setup again
- **"Gmail API not enabled"**: Go to Google Cloud Console and enable Gmail API

### Notion Connection Issues

- **"Database not found"**: Check your `NOTION_DATABASE_ID` format
- **"Permission denied"**: Make sure you shared the database with the integration
- **"Invalid API key"**: Verify your `NOTION_API_KEY` is correct

### Paper Not Found

- Some papers may not be available on arXiv
- The application will skip papers that can't be found
- Check `gs2notion.log` for details

### Logs

All activity is logged to `gs2notion.log`. Check this file for debugging:

```bash
tail -f gs2notion.log
```

## Configuration Files

- `config.py`: Main configuration (API endpoints, prompts)
- `.env`: Sensitive credentials (not committed to git)
- `requirements.txt`: Python dependencies

## Project Structure

```
Paper2Notion/
├── main.py                 # Main application entry point
├── gmail_handler.py        # Gmail API integration
├── gmail_auth.py           # Gmail OAuth authentication
├── paper_fetcher.py        # arXiv paper fetching
├── summarizer.py           # Claude summarization
├── notion_handler.py       # Notion database integration
├── config.py               # Configuration settings
├── setup_gmail.py          # Gmail setup script
├── get_notion_db_id.py     # Notion database ID helper
├── requirements.txt        # Python dependencies
├── run_gs2notion.bat       # Windows batch runner
└── README.md               # This file
```

## API Costs

- **Gmail API**: Free (included with Google account)
- **Notion API**: Free (included with Notion account)
- **Anthropic API**: Paid (Claude usage) - ~$0.01-0.05 per paper summary

## License

See LICENSE file for details.

## Support

For issues or questions:
1. Check `TROUBLESHOOTING.md`
2. Review `gs2notion.log` for error messages
3. Check `SOLUTIONS.md` for common problems
