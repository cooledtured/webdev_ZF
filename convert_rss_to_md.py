"""
Requirements: beautifulsoup4 html2text
"""

import os
import re
import math
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime
from email.utils import parsedate_to_datetime

try:
    import html2text
    HAVE_HTML2TEXT = True
except ImportError:
    HAVE_HTML2TEXT = False

from bs4 import BeautifulSoup

# Configuration
RSS_URL = "https://anchor.fm/s/32ea8fa8/podcast/rss"
OUTPUT_DIR = "./src/content/posts/"

# XML Namespaces used in Podcast RSS feeds
NAMESPACES = {
    "itunes": "http://www.itunes.com/dtds/podcast-1.0.dtd",
    "content": "http://purl.org/rss/1.0/modules/content/"
}

def clean_slug(text):
    """Generate a clean URL-friendly slug from title."""
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s-]', '', text)
    text = re.sub(r'\s+', '-', text)
    return text.strip('-')[:80] or "podcast-episode"

def extract_summary(html_or_text, max_length=160):
    """Extract clean plain-text summary."""
    soup = BeautifulSoup(html_or_text, "html.parser")
    text = ' '.join(soup.get_text(separator=' ').split())
    if len(text) > max_length:
        text = text[:max_length].rsplit(' ', 1)[0] + "..."
    return text or "New podcast episode from Zealed Fujoshi."

def html_to_markdown(html_content):
    """Convert HTML description to Markdown."""
    if HAVE_HTML2TEXT:
        h = html2text.HTML2Text()
        h.body_width = 0
        h.ignore_links = False
        return h.handle(html_content).strip()
    
    soup = BeautifulSoup(html_content, "html.parser")
    return soup.get_text().strip()

def fetch_rss_feed(url):
    """Fetch and parse RSS XML feed."""
    print(f"Fetching RSS feed from: {url}")
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req) as response:
        xml_data = response.read()
    return ET.fromstring(xml_data)

def sync_podcast_episodes():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    root = fetch_rss_feed(RSS_URL)
    channel = root.find("channel")

    if channel is None:
        print("Invalid RSS feed structure.")
        return

    # Fallback channel cover image
    channel_image_elem = channel.find("itunes:image", NAMESPACES)
    default_cover = channel_image_elem.get("href") if channel_image_elem is not None else "/images/default-podcast.jpg"

    items = channel.findall("item")
    print(f"Found {len(items)} episodes in RSS feed. Processing...")

    created_count = 0
    skipped_count = 0

    for item in items:
        title_elem = item.find("title")
        title = title_elem.text.strip() if title_elem is not None else "Untitled Episode"

        # Publication Date
        pub_date_elem = item.find("pubDate")
        if pub_date_elem is not None and pub_date_elem.text:
            dt = parsedate_to_datetime(pub_date_elem.text)
            pub_date = dt.strftime("%Y-%m-%d")
        else:
            pub_date = datetime.now().strftime("%Y-%m-%d")

        slug = clean_slug(title)
        filepath = os.path.join(OUTPUT_DIR, f"{pub_date}-{slug}.md")

        # Skip existing files to preserve manual edits
        if os.path.exists(filepath):
            skipped_count += 1
            continue

        # Audio Enclosure URL
        enclosure = item.find("enclosure")
        audio_url = enclosure.get("url", "") if enclosure is not None else ""

        # Cover Image
        image_elem = item.find("itunes:image", NAMESPACES)
        cover_image = image_elem.get("href") if image_elem is not None else default_cover

        # Episode Description / Body
        content_elem = item.find("content:encoded", NAMESPACES)
        desc_elem = item.find("description")
        
        raw_body = ""
        if content_elem is not None and content_elem.text:
            raw_body = content_elem.text
        elif desc_elem is not None and desc_elem.text:
            raw_body = desc_elem.text

        summary = extract_summary(raw_body)
        markdown_body = html_to_markdown(raw_body)

        safe_title = title.replace('"', '\\"')
        safe_summary = summary.replace('"', '\\"')

        # Frontmatter + HTML5 Audio Embed
        md_content = f"""---
title: "{safe_title}"
summary: "{safe_summary}"
pubDate: {pub_date}
author: "Zealed Fujoshi"
category: PODCAST
coverImage: "{cover_image}"
featured: false
readingTime: 3
tags: ["Podcast", "Episode", "Yaoi", "BL"]
audioUrl: "{audio_url}"
---

## {title}

{markdown_body}

### Listen to Episode

<audio controls class="w-full my-6 rounded-lg bg-white/5 border border-white/10 p-2">
  <source src="{audio_url}" type="audio/mpeg" />
  Your browser does not support the audio element.
</audio>
"""

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(md_content)

        print(f"Created: {filepath}")
        created_count += 1

    print(f"\nSync Complete: Created {created_count} new posts ({skipped_count} skipped/already existed).")

if __name__ == "__main__":
    sync_podcast_episodes()