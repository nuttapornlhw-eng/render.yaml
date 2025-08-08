import os, re, requests

SERPAPI_KEY = os.getenv("SERPAPI_KEY", "")

# Basic query patterns to find free-post / UGC opportunities.
PATTERNS = [
    "{kw} \"write for us\"",
    "{kw} \"guest post\"",
    "{kw} \"submit article\"",
    "{kw} \"add url\"",
    "{kw} \"submit site\"",
    "{kw} \"contribute\"",
    "{kw} \"community\"",
    "{kw} \"forum\"",
    "{kw} \"directory\"",
    "{kw} \"profile\"",
]

def serpapi_search(query: str, num: int = 10):
    if not SERPAPI_KEY:
        return []
    # Example placeholder; see SerpAPI docs for exact params.
    # url = "https://serpapi.com/search.json"
    # params = {"engine": "google", "q": query, "num": num, "api_key": SERPAPI_KEY}
    # r = requests.get(url, params=params, timeout=30)
    # data = r.json()
    # results = [item.get("link") for item in data.get("organic_results", []) if item.get("link")]
    # return results
    return []

def discover_candidates(keyword: str, seed_domains: list[str], use_serpapi: bool = False, per_pattern: int = 10) -> list[str]:
    found = set(seed_domains or [])
    for pat in PATTERNS:
        q = pat.format(kw=keyword)
        if use_serpapi:
            for link in serpapi_search(q, num=per_pattern) or []:
                found.add(link)
    # Normalize: keep domains only
    domains = set()
    for url in found:
        m = re.search(r"https?://([^/]+)", url) if url.startswith("http") else re.match(r"([^/]+)$", url)
        if m:
            domains.add(m.group(1).lower())
    return sorted(domains)
