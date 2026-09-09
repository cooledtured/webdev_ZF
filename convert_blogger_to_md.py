"""
Requirements: requests beautifulsoup4 html2text pyyaml
"""

import os
import re
import math
import json
import urllib.request
import urllib.parse
from datetime import datetime

# Try importing HTML to Markdown converter, fall back to BeautifulSoup parser if needed
try:
    import html2text
    HAVE_HTML2TEXT = True
except ImportError:
    HAVE_HTML2TEXT = False

from bs4 import BeautifulSoup

SITE_URL = "https://www.zealedfujoshi.xyz"
OUTPUT_DIR = "./src/content/posts/"
MAX_RESULTS_PER_PAGE = 300

def clean_slug(text):
    """Generate a clean URL-friendly slug from title."""
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s-]', '', text)
    text = re.sub(r'\s+', '-', text)
    return text.strip('-')[:80] or "post"

def calculate_reading_time(html_content):
    """Calculate estimated reading time in minutes (approx 200 wpm)."""
    soup = BeautifulSoup(html_content, "html.parser")
    text = soup.get_text(separator=' ')
    words = len(re.findall(r'\w+', text))
    minutes = math.ceil(words / 200)
    return max(1, minutes)

def extract_summary(html_content, max_length=160):
    """Extract clean plain-text summary from HTML body."""
    soup = BeautifulSoup(html_content, "html.parser")
    # Remove script and style elements
    for script in soup(["script", "style"]):
        script.extract()
    text = soup.get_text(separator=' ')
    clean_text = ' '.join(text.split())
    if len(clean_text) > max_length:
        clean_text = clean_text[:max_length].rsplit(' ', 1)[0] + "..."
    return clean_text or "No summary available."

def extract_cover_image(entry, html_content):
    """Extract cover image URL from entry or post content."""
    # 1. Check media$thumbnail
    if "media$thumbnail" in entry:
        thumb_url = entry["media$thumbnail"].get("url", "")
        # Upgrade blogger thumbnail resolution from /s72-c/ or /w72-h72/ to original /s1600/
        high_res = re.sub(r'/s72-c/|/s\d+/|/w\d+-h\d+/', '/s1600/', thumb_url)
        if high_res:
            return high_res

    # 2. Extract first img tag from HTML
    soup = BeautifulSoup(html_content, "html.parser")
    first_img = soup.find("img")
    if first_img and first_img.get("src"):
        return first_img["src"]

    return "/images/default-cover.jpg"

def determine_category(tags):
    """Map post tags to an uppercase Category constant."""
    if not tags:
        return "GENERAL"
    
    first_tag = tags[0].upper().replace(" ", "_")
    
    # Custom mappings
    if any("INTERVIEW" in t.upper() for t in tags):
        return "INTERVIEW"
    elif any("REVIEW" in t.upper() for t in tags):
        return "MANHWA_REVIEW"
    elif any("PODCAST" in t.upper() for t in tags):
        return "PODCAST"
    elif any("CONVENTION" in t.upper() or "EVENT" in t.upper() for t in tags):
        return "CONVENTION_RECAP"
    
    return first_tag

def html_to_markdown(html_content):
    """Convert HTML content to clean Markdown."""
    if HAVE_HTML2TEXT:
        h = html2text.HTML2Text()
        h.body_width = 0  # Disable line wrapping
        h.ignore_links = False
        h.ignore_images = False
        h.ignore_emphasis = False
        markdown = h.handle(html_content)
    else:
        # Basic BeautifulSoup fallback conversion
        soup = BeautifulSoup(html_content, "html.parser")
        
        # Replace headings
        for i in range(1, 7):
            for h in soup.find_all(f"h{i}"):
                h.replace_with(f"\n\n{'#' * i} {h.get_text().strip()}\n\n")
        
        # Replace paragraphs
        for p in soup.find_all("p"):
            p.replace_with(f"\n\n{p.get_text().strip()}\n\n")

        # Replace links
        for a in soup.find_all("a"):
            if a.get("href"):
                a.replace_with(f"[{a.get_text().strip()}]({a['href']})")

        markdown = soup.get_text()

    # Clean up excess blank lines
    markdown = re.sub(r'\n{3,}', '\n\n', markdown)
    return markdown.strip()

def fetch_all_blogger_posts(base_url):
    """Fetch all posts using Blogger JSON feed API."""
    posts = []
    start_index = 1
    
    print(f"Fetching posts from {base_url}...")

    while True:
        feed_url = f"{base_url.rstrip('/')}/feeds/posts/default?alt=json&max-results={MAX_RESULTS_PER_PAGE}&start-index={start_index}"
        req = urllib.request.Request(feed_url, headers={'User-Agent': 'Mozilla/5.0'})
        
        try:
            with urllib.request.urlopen(req) as response:
                data = json.loads(response.read().decode('utf-8'))
        except Exception as e:
            print(f"Error fetching {feed_url}: {e}")
            break

        feed = data.get("feed", {})
        entries = feed.get("entry", [])

        if not entries:
            break

        posts.extend(entries)

        total_results = int(feed.get("openSearch$totalResults", {}).get("$t", 0))
        print(f"Fetched {len(posts)} / {total_results} posts...")

        if start_index + len(entries) > total_results:
            break

        start_index += MAX_RESULTS_PER_PAGE

    return posts

def convert_entry_to_astro_md(entry):
    """Transform Blogger entry dict into Astro Markdown file string."""
    title = entry.get("title", {}).get("$t", "Untitled Post").strip()
    
    # Extract Publication Date (YYYY-MM-DD)
    raw_pub_date = entry.get("published", {}).get("$t", "")
    if raw_pub_date:
        pub_date = raw_pub_date.split("T")[0]
    else:
        pub_date = datetime.now().strftime("%Y-%m-%d")

    # Author
    author_list = entry.get("author", [])
    author = author_list[0].get("name", {}).get("$t", "Zealed Fujoshi") if author_list else "Zealed Fujoshi"

    # Tags / Categories
    categories_data = entry.get("category", [])
    tags = [cat.get("term") for cat in categories_data if cat.get("term")]

    # Category determination
    category = determine_category(tags)

    # HTML Body Content
    content_html = entry.get("content", {}).get("$t", "") or entry.get("summary", {}).get("$t", "")

    # Cover Image
    cover_image = extract_cover_image(entry, content_html)

    # Summary
    summary = extract_summary(content_html)

    # Reading Time
    reading_time = calculate_reading_time(content_html)

    # Featured flag (e.g., if tagged as 'featured' or post is an interview)
    featured = "INTERVIEW" in category or "featured" in [t.lower() for t in tags]

    # Convert HTML body to Markdown
    markdown_body = html_to_markdown(content_html)

    # Format YAML Frontmatter according to schema
    frontmatter_tags = json.dumps(tags, ensure_ascii=False) if tags else "[]"
    
    # Escape quotes in title & summary for safe YAML syntax
    safe_title = title.replace('"', '\\"')
    safe_summary = summary.replace('"', '\\"')

    md_content = f"""---
title: "{safe_title}"
summary: "{safe_summary}"
pubDate: {pub_date}
author: "{author}"
category: {category}
coverImage: "{cover_image}"
featured: {str(featured).lower()}
readingTime: {reading_time}
tags: {frontmatter_tags}
---

## {title}

{markdown_body}
"""
    return title, pub_date, md_content

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    posts = fetch_all_blogger_posts(SITE_URL)
    
    if not posts:
        print("No posts found or failed to retrieve feed.")
        return

    print(f"Converting {len(posts)} posts into Astro Markdown (.md)...")

    for entry in posts:
        title, pub_date, md_content = convert_entry_to_astro_md(entry)
        slug = clean_slug(title)
        filename = f"{pub_date}-{slug}.md"
        filepath = os.path.join(OUTPUT_DIR, filename)

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(md_content)

        print(f"Created: {filepath}")

    print(f"\nAll done! Output files saved to '{OUTPUT_DIR}'.")

if __name__ == "__main__":
    main()
