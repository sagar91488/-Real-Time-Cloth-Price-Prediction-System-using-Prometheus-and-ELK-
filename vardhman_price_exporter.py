# vardhman_price_exporter.py
from http.server import BaseHTTPRequestHandler, HTTPServer
from elasticsearch import Elasticsearch
from datetime import datetime
import requests
import threading
import time
import urllib3
import os
import json

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Config
ES_HOST = os.environ.get("ELASTICSEARCH_HOST", "http://elasticsearch:9200")
INDEX_NAME = "vardhman_prices"
PRED_INDEX = "vardhman_predictions"
SYMBOL = "VTL.NS"   # Vardhman Textiles (NSE / Yahoo)
COMPANY = "Vardhman Textiles Ltd"
PORT = int(os.environ.get("EXPORTER_PORT", 8000))
FETCH_INTERVAL = int(os.environ.get("FETCH_INTERVAL", 15))  # seconds

# Elasticsearch connection with retry
es = None
for attempt in range(20):
    try:
        es = Elasticsearch([ES_HOST], verify_certs=False, request_timeout=30)
        if es.ping():
            print(f"✅ Connected to Elasticsearch at {ES_HOST}")
            break
    except Exception as e:
        print(f"⚠️ Elasticsearch not ready (attempt {attempt+1}/20): {e}")
    time.sleep(3)
else:
    print("❌ Could not connect to Elasticsearch after retries. Exporter will still start and try later.")
    es = None

latest_price = None
latest_ts = None

def fetch_and_index_price():
    global latest_price, latest_ts, es
    while True:
        try:
            url = f"https://query1.finance.yahoo.com/v8/finance/chart/{SYMBOL}?interval=1m&range=1d"
            r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
            r.raise_for_status()
            data = r.json()
            result = data.get("chart", {}).get("result", [None])[0]
            price = None
            if result:
                price = result.get("meta", {}).get("regularMarketPrice")
                if price is None:
                    # fallback to latest close in indicators
                    q = result.get("indicators", {}).get("quote", [None])[0]
                    if q:
                        closes = q.get("close", [])
                        for v in reversed(closes):
                            if v is not None:
                                price = v
                                break

            if price is not None:
                latest_price = float(price)
                latest_ts = datetime.utcnow().isoformat()
                doc = {
                    "timestamp": latest_ts,
                    "company": COMPANY,
                    "symbol": SYMBOL,
                    "price": round(latest_price, 2),
                    "source": "yahoo_finance"
                }
                try:
                    if es is None:
                        es = Elasticsearch([ES_HOST], verify_certs=False, request_timeout=30)
                    es.index(index=INDEX_NAME, document=doc)
                except Exception as e:
                    print("⚠️ ES index failed (exporter):", e)
                print(f"📥 Indexed {SYMBOL} price ₹{latest_price} at {latest_ts}")
            else:
                print("⚠️ No price in Yahoo response")

        except Exception as exc:
            print("❌ Exporter fetch error:", exc)

        time.sleep(FETCH_INTERVAL)

class MetricsHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/metrics":
            lines = []
            lines.append("# HELP vardhman_stock_price Current Vardhman stock price (INR)")
            lines.append("# TYPE vardhman_stock_price gauge")
            if latest_price is not None:
                lines.append(f"vardhman_stock_price {latest_price}")
            else:
                lines.append("vardhman_stock_price NaN")

            # latest prediction
            pred_val = "NaN"
            try:
                if es is None:
                    raise Exception("ES not connected")
                q = {"size": 1, "sort": [{"timestamp": {"order": "desc"}}], "query": {"match_all": {}}}
                res = es.search(index=PRED_INDEX, body=q)
                hits = res.get("hits", {}).get("hits", [])
                if hits:
                    pred_val = hits[0]["_source"].get("predicted_price", "NaN")
            except Exception:
                pred_val = "NaN"

            lines.append("# HELP vardhman_predicted_price Predicted Vardhman stock price (INR)")
            lines.append("# TYPE vardhman_predicted_price gauge")
            lines.append(f"vardhman_predicted_price {pred_val}")

            payload = "\n".join(lines) + "\n"
            self.send_response(200)
            self.send_header("Content-Type", "text/plain; version=0.0.4")
            self.end_headers()
            self.wfile.write(payload.encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()

if __name__ == "__main__":
    t = threading.Thread(target=fetch_and_index_price, daemon=True)
    t.start()
    print(f"🚀 Vardhman exporter serving metrics on http://0.0.0.0:{PORT}/metrics")
    server = HTTPServer(("0.0.0.0", PORT), MetricsHandler)
    server.serve_forever()
