import os, random

import requests

AHREFS_API_KEY = os.getenv("AHREFS_API_KEY", "")
DEMO_MODE = os.getenv("DEMO_MODE", "TRUE").upper() == "TRUE"

def get_metrics(domain: str) -> dict:
    """Return DR & UR for a domain.
    In DEMO_MODE, returns mocked stable pseudo-random values per domain."""
    if DEMO_MODE or not AHREFS_API_KEY:
        seed = sum(ord(c) for c in domain) % 997
        random.seed(seed)
        dr = random.randint(20, 95)
        ur = random.randint(10, 90)
        return {"dr": dr, "ur": ur, "source": "mock"}

    # Example Ahrefs API call placeholder (pseudo; adapt to your plan/endpoint)
    # url = "https://apiv2.ahrefs.com?from=domain_rating&target=%s&mode=domain&token=%s" % (domain, AHREFS_API_KEY)
    # resp = requests.get(url, timeout=20)
    # data = resp.json()
    # return {"dr": data.get("dr", 0), "ur": data.get("ur", 0), "source": "ahrefs"}
    raise NotImplementedError("Implement Ahrefs API call based on your subscription endpoints.")
