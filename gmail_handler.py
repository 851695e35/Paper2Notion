import base64
import re
import time
from gmail_auth import get_gmail_service
from config import GOOGLE_SCHOLAR_SENDER

def get_unread_scholar_emails(retries=10):
    """Fetch unread emails from Google Scholar with retry logic."""
    service = get_gmail_service()

    for attempt in range(retries):
        try:
            # Query for unread emails from Google Scholar
            print(f"Querying Gmail for unread emails from {GOOGLE_SCHOLAR_SENDER}... (attempt {attempt + 1}/{retries})")
            results = service.users().messages().list(
                userId='me',
                q=f'from:{GOOGLE_SCHOLAR_SENDER} is:unread',
                maxResults=10
            ).execute()

            messages = results.get('messages', [])
            print(f"Found {len(messages)} unread emails")
            return messages
        except Exception as e:
            print(f"Error fetching emails (attempt {attempt + 1}): {e}")
            if attempt < retries - 1:
                wait_time = 10  # Fixed 10 second wait
                print(f"Retrying in {wait_time} seconds...")
                time.sleep(wait_time)
            else:
                print("Max retries reached")
                return []

def get_email_details(message_id):
    """Get full email details including body."""
    service = get_gmail_service()

    try:
        message = service.users().messages().get(
            userId='me',
            id=message_id,
            format='full'
        ).execute()

        headers = message['payload']['headers']
        subject = next((h['value'] for h in headers if h['name'] == 'Subject'), '')
        sender = next((h['value'] for h in headers if h['name'] == 'From'), '')

        # Extract body
        body = ''
        if 'parts' in message['payload']:
            for part in message['payload']['parts']:
                if part['mimeType'] == 'text/plain':
                    data = part['body'].get('data', '')
                    if data:
                        body = base64.urlsafe_b64decode(data).decode('utf-8')
                    break
        else:
            data = message['payload']['body'].get('data', '')
            if data:
                body = base64.urlsafe_b64decode(data).decode('utf-8')

        return {
            'id': message_id,
            'subject': subject,
            'sender': sender,
            'body': body
        }
    except Exception as e:
        print(f"Error getting email details: {e}")
        return None

def extract_paper_titles(email_body):
    """Extract both seed paper and citing papers from Google Scholar email.

    Returns: (seed_paper, citing_papers) tuple
    - seed_paper: The original paper being cited
    - citing_papers: List of new papers that cite the seed paper
    """
    import html
    import re

    # Decode HTML entities
    email_body = html.unescape(email_body)

    seed_paper = None
    citing_papers = []

    # Extract all citing papers (the ones with [PDF] link)
    # Pattern: [PDF]</span> <a ...>Title</a>
    matches = re.finditer(r'\[PDF\].*?<a[^>]*>([^<]+)</a>', email_body, re.DOTALL)
    for match in matches:
        title = match.group(1).strip()
        cleaned_title = clean_paper_title(title)
        if cleaned_title:
            citing_papers.append(cleaned_title)

    # Extract seed paper - try multiple patterns
    # Pattern 1: <b>「Title」- 新的引用</b>
    match = re.search(r'<b>「([^」]+)」', email_body)
    if match:
        title = match.group(1).strip()
        seed_paper = clean_paper_title(title)

    # Pattern 2: 〈<a ...>Title</a>〉 (Chinese angle brackets)
    if not seed_paper:
        match = re.search(r'〈<a[^>]*>([^<]+)</a>〉', email_body)
        if match:
            title = match.group(1).strip()
            seed_paper = clean_paper_title(title)

    # Pattern 3: Look for text in first <a> tag (fallback)
    if not seed_paper:
        match = re.search(r'<a[^>]*>([^<]+)</a>', email_body)
        if match:
            title = match.group(1).strip()
            seed_paper = clean_paper_title(title)

    return seed_paper, citing_papers

def extract_paper_title(email_body):
    """Extract paper title from Google Scholar email (legacy function)."""
    seed_paper, citing_paper = extract_paper_titles(email_body)
    return citing_paper or seed_paper

def clean_paper_title(title):
    """Clean paper title by removing special characters and non-ASCII text."""
    # Remove HTML entities and special characters
    title = re.sub(r'&[a-z]+;', '', title)  # Remove HTML entities like &nbsp;
    title = re.sub(r'[\u4e00-\u9fff]+', '', title)  # Remove Chinese characters
    title = re.sub(r'[\u3040-\u309f]+', '', title)  # Remove Japanese hiragana
    title = re.sub(r'[\u30a0-\u30ff]+', '', title)  # Remove Japanese katakana
    title = re.sub(r'[\u0600-\u06ff]+', '', title)  # Remove Arabic characters
    title = re.sub(r'[\xa0]+', ' ', title)  # Replace non-breaking spaces with regular spaces
    title = re.sub(r'[\s]+', ' ', title)  # Collapse multiple spaces
    title = title.strip()

    # Remove leading/trailing special characters
    title = re.sub(r'^[\W_]+|[\W_]+$', '', title)

    # Only return if title has meaningful content (at least 5 characters)
    return title if len(title) >= 5 else None

def mark_email_as_read(message_id):
    """Mark email as read."""
    service = get_gmail_service()

    try:
        service.users().messages().modify(
            userId='me',
            id=message_id,
            body={'removeLabelIds': ['UNREAD']}
        ).execute()
    except Exception as e:
        print(f"Error marking email as read: {e}")

