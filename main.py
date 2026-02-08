import schedule
import time
import logging
import sys
import io
from datetime import datetime
from gmail_handler import get_unread_scholar_emails, get_email_details, extract_paper_titles, mark_email_as_read, clean_paper_title
from paper_fetcher import search_paper_content, search_paper_abstract
from summarizer import summarize_paper, generate_tldr
from notion_handler import add_to_notion_database
from config import POLL_INTERVAL

# Setup logging with UTF-8 encoding
import sys
import io

# Force UTF-8 encoding for console output
if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('gs2notion.log', encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

def process_scholar_emails():
    """Main function to process Google Scholar emails."""
    logger.info("Starting email processing...")

    try:
        emails = get_unread_scholar_emails()
    except Exception as e:
        logger.error(f"Error fetching emails: {e}", exc_info=True)
        return

    if not emails:
        logger.info("No unread emails from Google Scholar")
        return

    logger.info(f"Found {len(emails)} unread emails")

    for email in emails:
        message_id = email['id']
        logger.info(f"Processing email: {message_id}")

        # Get email details
        email_details = get_email_details(message_id)
        if not email_details:
            logger.error(f"Failed to get email details for {message_id}")
            continue

        logger.info(f"Subject: {email_details['subject']}")

        # Extract both seed paper and citing papers (now returns a list)
        seed_paper, citing_papers = extract_paper_titles(email_details['body'])

        if not seed_paper:
            logger.warning(f"Could not extract seed paper from email {message_id}")
            mark_email_as_read(message_id)
            continue

        if not citing_papers:
            logger.warning(f"Could not extract citing papers from email {message_id}")
            mark_email_as_read(message_id)
            continue

        logger.info(f"Seed paper: {seed_paper}")
        logger.info(f"Found {len(citing_papers)} citing papers")

        # Process each citing paper
        for citing_title in citing_papers:
            logger.info(f"Processing citing paper: {citing_title}")

            # Search for the CITING paper content (the new paper)
            logger.info("Searching for citing paper content...")
            paper_content, paper_url, authors = search_paper_content(citing_title)

            # Fallback to abstract if full text not available
            if not paper_content:
                logger.info("Full text not found, trying abstract...")
                paper_content, paper_url, authors = search_paper_abstract(citing_title)

            if not paper_content:
                logger.warning(f"Could not find paper content for {citing_title}")
                continue

            logger.info("Summarizing citing paper...")
            summary = summarize_paper(paper_content)

            if not summary:
                logger.error(f"Failed to summarize paper {citing_title}")
                continue

            # Generate proper one-sentence TLDR
            logger.info("Generating TLDR...")
            tldr = generate_tldr(paper_content, summary)
            if not tldr:
                # Fallback: use first sentence if TLDR generation fails
                sentences = summary.split('.')
                tldr = sentences[0].strip() if sentences and sentences[0].strip() else summary[:150]
                if tldr and not tldr.endswith('.'):
                    tldr = tldr + '.'

            # Truncate summary to 1200 tokens (approximately 4800 characters for plain text)
            summary_truncated = summary[:4800]

            logger.info("Adding to Notion database...")
            success = add_to_notion_database(
                seed_paper=seed_paper,
                citing_title=citing_title,
                summary=summary_truncated,
                tldr=tldr,
                gmail_msg_id=message_id,
                citing_url=paper_url,
                authors=authors
            )

            if success:
                logger.info(f"Successfully added to Notion: {citing_title}")
            else:
                logger.error(f"Failed to add to Notion for {citing_title}")

        # Mark email as read after processing all papers
        mark_email_as_read(message_id)
        logger.info(f"Successfully processed email {message_id}")

    logger.info("Email processing completed")

def schedule_jobs():
    """Schedule the email processing job."""
    schedule.every(6).hours.do(process_scholar_emails)
    logger.info(f"Scheduled email processing every 6 hours")

    # Run immediately on startup
    process_scholar_emails()

    # Keep scheduler running
    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == "__main__":
    logger.info("Starting GS2Notion automation...")
    try:
        schedule_jobs()
    except KeyboardInterrupt:
        logger.info("Shutting down...")
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
