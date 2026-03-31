"""
Simple RSS Feed Reader
"""

import feedparser
import re
from urllib.parse import urlparse

def validate_url(url):
    """Basic URL validation"""
    if not url.startswith(('http://', 'https://')):
        return False
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False

def fetch_feed(url):
    """Fetch and parse RSS feed"""
    try:
        feed = feedparser.parse(url)
        if feed.bozo:  # Parse error
            return None, f"Parse error: {feed.bozo_exception}"
        if not feed.entries:
            return None, "No entries found in feed"
        return feed, None
    except Exception as e:
        return None, f"Error fetching feed: {str(e)}"

def clean_html(text):
    """Basic HTML tag stripping"""
    if not text:
        return ""
    # Remove HTML tags
    clean = re.sub(r'<[^>]+>', '', text)
    # Decode common HTML entities
    clean = clean.replace('&amp;', '&')
    clean = clean.replace('&lt;', '<')
    clean = clean.replace('&gt;', '>')
    clean = clean.replace('&quot;', '"')
    clean = clean.replace('&#39;', "'")
    return clean.strip()

def display_entries(feed, max_items=10, show_full=True):
    """Display feed entries"""
    entries = feed.entries[:max_items]
    
    for i, entry in enumerate(entries, 1):
        print(f"\n{i}. {entry.title}")
        
        # Get description/summary
        description = ""
        if hasattr(entry, 'summary') and entry.summary:
            description = entry.summary
        elif hasattr(entry, 'description') and entry.description:
            description = entry.description
        
        if description:
            description = clean_html(description)
            if not show_full and len(description) > 200:
                description = description[:200] + "..."
            print(f"   Description: {description}")
        
        if hasattr(entry, 'link') and entry.link:
            print(f"   Link: {entry.link}")

def main():
    print("RSS Feed Reader")
    print("===============")
    
    # Get URL
    while True:
        url = input("Enter RSS feed URL: ").strip()
        if validate_url(url):
            break
        print("Invalid URL. Must start with http:// or https://")
    
    # Get options
    try:
        max_items_input = input("How many items to show? (default 10): ").strip()
        max_items = int(max_items_input) if max_items_input else 10
    except ValueError:
        print("Invalid number, using default of 10")
        max_items = 10
    
    show_full_input = input("Show full descriptions? (y/n): ").strip().lower()
    show_full = show_full_input in ('y', 'yes')
    
    print("\nFetching feed...")
    
    # Fetch and display
    feed, error = fetch_feed(url)
    if error:
        print(f"Error: {error}")
        return
    
    display_entries(feed, max_items, show_full)

if __name__ == "__main__":

    main()
