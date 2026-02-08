import requests
import arxiv
from typing import Optional, Tuple

def search_paper_content(title: str) -> Tuple[Optional[str], str, str]:
    """Search for paper content using arXiv API. Returns (content, url, authors)."""
    try:
        # Search arXiv
        client = arxiv.Client()
        search = arxiv.Search(
            query=f'ti:"{title}"',
            max_results=1,
            sort_by=arxiv.SortCriterion.SubmittedDate,
            sort_order=arxiv.SortOrder.Descending
        )

        for result in search.results():
            # Get the PDF URL and metadata
            pdf_url = result.pdf_url
            paper_url = result.entry_id
            authors = ", ".join([author.name for author in result.authors])

            if pdf_url:
                content = fetch_paper_text(pdf_url)
                return content, paper_url, authors

            return None, paper_url, authors

        return None, "", ""
    except Exception as e:
        print(f"Error searching arXiv: {e}")
        return None, "", ""

def fetch_paper_text(pdf_url: str) -> Optional[str]:
    """Fetch and extract text from PDF."""
    try:
        import PyPDF2
        import io

        response = requests.get(pdf_url, timeout=30)
        response.raise_for_status()

        pdf_file = io.BytesIO(response.content)
        pdf_reader = PyPDF2.PdfReader(pdf_file)

        text = ""
        # Extract text from first 10 pages (to avoid token limits)
        for page_num in range(min(10, len(pdf_reader.pages))):
            page = pdf_reader.pages[page_num]
            text += page.extract_text()

        return text if text.strip() else None
    except Exception as e:
        print(f"Error fetching paper text: {e}")
        return None

def search_paper_abstract(title: str) -> Tuple[Optional[str], str, str]:
    """Fallback: search for paper abstract using arXiv API. Returns (abstract, url, authors)."""
    try:
        client = arxiv.Client()
        search = arxiv.Search(
            query=f'ti:"{title}"',
            max_results=1,
            sort_by=arxiv.SortCriterion.SubmittedDate,
            sort_order=arxiv.SortOrder.Descending
        )

        for result in search.results():
            paper_url = result.entry_id
            authors = ", ".join([author.name for author in result.authors])
            return result.summary, paper_url, authors

        return None, "", ""
    except Exception as e:
        print(f"Error searching paper abstract: {e}")
        return None, "", ""

