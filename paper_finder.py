import feedparser
import urllib.parse


def search_arxiv_papers(query, max_results=5):
    encoded_query = urllib.parse.quote(query)

    url = (
        "http://export.arxiv.org/api/query?"
        f"search_query=all:{encoded_query}"
        f"&start=0"
        f"&max_results={max_results}"
        f"&sortBy=relevance"
        f"&sortOrder=descending"
    )

    feed = feedparser.parse(url)

    papers = []

    for entry in feed.entries:
        paper_id = entry.id.split("/abs/")[-1]
        pdf_link = f"https://arxiv.org/pdf/{paper_id}.pdf"

        authors = [author.name for author in entry.authors]

        papers.append({
            "title": entry.title.replace("\n", " ").strip(),
            "authors": ", ".join(authors),
            "published": entry.published[:10],
            "summary": entry.summary.replace("\n", " ").strip(),
            "paper_link": entry.id,
            "pdf_link": pdf_link
        })

    return papers