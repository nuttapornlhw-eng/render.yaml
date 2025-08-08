import os, time, base64, hmac, hashlib, random, requests

MOZ_ACCESS_ID = os.getenv("MOZ_ACCESS_ID", "")
MOZ_SECRET_KEY = os.getenv("MOZ_SECRET_KEY", "")
DEMO_MODE = os.getenv("DEMO_MODE", "TRUE").upper() == "TRUE"

def _mock(domain: str):
    seed = (sum(ord(c) for c in domain) * 7) % 1009
    random.seed(seed)
    da = random.randint(15, 95)
    pa = random.randint(10, 90)
    spam = random.choice([0, 1, 2, 3, 4, 5])
    return {"da": da, "pa": pa, "spam_score": spam, "source": "mock"}

def get_metrics(domain: str) -> dict:
    """Return DA, PA, Spam Score for a domain. Uses Moz Links API v2 style signing (placeholder).
    In DEMO_MODE, returns mocked values."""
    if DEMO_MODE or not (MOZ_ACCESS_ID and MOZ_SECRET_KEY):
        return _mock(domain)

    # Example (placeholder). Refer to Moz official docs for exact endpoints & signing.
    # expires = int(time.time()) + 300
    # string_to_sign = f"{MOZ_ACCESS_ID}\n{expires}".encode("utf-8")
    # signature = base64.b64encode(hmac.new(MOZ_SECRET_KEY.encode("utf-8"), string_to_sign, hashlib.sha1).digest()).decode("utf-8")
    # params = {
    #     "AccessID": MOZ_ACCESS_ID,
    #     "Expires": expires,
    #     "Signature": signature,
    #     "target": domain,
    # }
    # resp = requests.get("https://lsapi.seomoz.com/v2/url_metrics", params=params, timeout=20)
    # data = resp.json()
    # return {"da": data.get("domain_authority", 0), "pa": data.get("page_authority", 0), "spam_score": data.get("spam_score", 0), "source": "moz"}
    raise NotImplementedError("Implement Moz API call based on your plan and endpoint.")
