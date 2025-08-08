import os
from flask import Flask, render_template, request, jsonify, send_file
from dotenv import load_dotenv
import pandas as pd

from utils.ahrefs_client import get_metrics as ahrefs_metrics
from utils.moz_client import get_metrics as moz_metrics
from utils.discovery import discover_candidates

load_dotenv()

app = Flask(__name__)

DATA_PATH = os.path.join("data", "starter_list.csv")

DEFAULTS = {
    "MIN_DR": int(os.getenv("MIN_DR", 40)),
    "MIN_UR": int(os.getenv("MIN_UR", 20)),
    "MIN_DA": int(os.getenv("MIN_DA", 35)),
    "MIN_PA": int(os.getenv("MIN_PA", 20)),
    "MAX_SPAM_SCORE": int(os.getenv("MAX_SPAM_SCORE", 3)),
    "TOP_N": int(os.getenv("TOP_N", 100)),
}

def load_seed() -> list[str]:
    try:
        df = pd.read_csv(DATA_PATH)
        return df["domain"].dropna().tolist()
    except Exception:
        return []

@app.get("/")
def index():
    return render_template("index.html", defaults=DEFAULTS)

@app.post("/scan")
def scan():
    payload = request.get_json(force=True)
    keyword = payload.get("keyword", "").strip()
    target_url = payload.get("target_url", "").strip()

    min_dr = int(payload.get("min_dr", DEFAULTS["MIN_DR"]))
    min_ur = int(payload.get("min_ur", DEFAULTS["MIN_UR"]))
    min_da = int(payload.get("min_da", DEFAULTS["MIN_DA"]))
    min_pa = int(payload.get("min_pa", DEFAULTS["MIN_PA"]))
    max_spam = int(payload.get("max_spam", DEFAULTS["MAX_SPAM_SCORE"]))
    top_n = int(payload.get("top_n", DEFAULTS["TOP_N"]))

    use_serpapi = bool(payload.get("use_serpapi", False))

    seeds = load_seed()
    candidates = discover_candidates(keyword, seed_domains=seeds, use_serpapi=use_serpapi, per_pattern=10)

    rows = []
    for domain in candidates:
        a = ahrefs_metrics(domain)
        m = moz_metrics(domain)
        row = {
            "domain": domain,
            "dr": a.get("dr", 0),
            "ur": a.get("ur", 0),
            "da": m.get("da", 0),
            "pa": m.get("pa", 0),
            "spam_score": m.get("spam_score", 0),
        }
        rows.append(row)

    df = pd.DataFrame(rows)
    # Filter
    filtered = df[
        (df["dr"] >= min_dr) &
        (df["ur"] >= min_ur) &
        (df["da"] >= min_da) &
        (df["pa"] >= min_pa) &
        (df["spam_score"] <= max_spam)
    ].copy()

    # Rank (simple average of normalized scores; customize as needed)
    if not filtered.empty:
        filtered["score"] = (
            filtered["dr"].rank(pct=True) +
            filtered["ur"].rank(pct=True) +
            filtered["da"].rank(pct=True) +
            filtered["pa"].rank(pct=True) -
            filtered["spam_score"].rank(pct=True)
        )
        filtered = filtered.sort_values("score", ascending=False).head(top_n)

    # Save to temp csv for download
    out_path = os.path.join("data", "last_result.csv")
    os.makedirs("data", exist_ok=True)
    filtered.to_csv(out_path, index=False)

    return jsonify({
        "count": int(filtered.shape[0]),
        "items": filtered.to_dict(orient="records"),
        "download": "/export"
    })

@app.get("/export")
def export_csv():
    path = os.path.join("data", "last_result.csv")
    if not os.path.exists(path):
        return jsonify({"error": "No result yet"}), 400
    return send_file(path, as_attachment=True, download_name="backlink_top100.csv", mimetype="text/csv")

if __name__ == "__main__":
    app.run(debug=True)
