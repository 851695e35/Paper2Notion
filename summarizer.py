import os
import sys

# Completely disable any proxy configuration
for key in list(os.environ.keys()):
    if 'proxy' in key.lower():
        del os.environ[key]

# Patch httpx before importing anthropic
import httpx
original_client_init = httpx.Client.__init__

def patched_init(self, *args, **kwargs):
    kwargs.pop('proxies', None)
    return original_client_init(self, *args, **kwargs)

httpx.Client.__init__ = patched_init

from anthropic import Anthropic
from config import SUMMARY_PROMPT, ANTHROPIC_API_KEY

def summarize_paper(paper_content: str) -> str:
    """Summarize paper using Claude."""
    try:
        client = Anthropic(api_key=ANTHROPIC_API_KEY)
        message = client.messages.create(
            model="claude-opus-4-5-20251101",
            max_tokens=2000,
            messages=[
                {
                    "role": "user",
                    "content": f"{SUMMARY_PROMPT}\n\n---\n\nPaper Content:\n\n{paper_content}"
                }
            ]
        )

        return message.content[0].text
    except Exception as e:
        print(f"Error summarizing paper: {e}")
        import traceback
        traceback.print_exc()
        return ""

def generate_tldr(paper_content: str, full_summary: str) -> str:
    """Generate a one-sentence TLDR using Claude."""
    try:
        client = Anthropic(api_key=ANTHROPIC_API_KEY)
        message = client.messages.create(
            model="claude-opus-4-5-20251101",
            max_tokens=150,
            messages=[
                {
                    "role": "user",
                    "content": f"""Based on this paper summary, generate a single, complete sentence that captures the main contribution or finding. The sentence should be grammatically complete and end with a period.

Summary:
{full_summary}

Generate only the one-sentence TLDR, nothing else."""
                }
            ]
        )

        tldr = message.content[0].text.strip()
        # Ensure it ends with a period
        if tldr and not tldr.endswith('.'):
            tldr = tldr + '.'
        return tldr
    except Exception as e:
        print(f"Error generating TLDR: {e}")
        import traceback
        traceback.print_exc()
        return ""

