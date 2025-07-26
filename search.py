import arxiv
client = arxiv.Client()
def search_arxiv(query : str ) :
    search = arxiv.Search(
        query = query,
        max_results = 5,
        sort_by = arxiv.SortCriterion.Relevance
    )
    results = []
    for r in client.results(search):
        paper = {
            "title": r.title,
            "id": r.entry_id,
            "authors": [author.name for author in r.authors],
            "summary": r.summary,
            "pdf_url": getattr(r, "pdf_url", None),
            "published": r.published.strftime("%Y-%m-%d")
        }
        results.append(paper)
    return {
        "papers": results
    }
        