# vardhman_predictor.py
import time
import logging
import sys
import os
from datetime import datetime
from elasticsearch import Elasticsearch
from sklearn.linear_model import LinearRegression
import numpy as np
import urllib3

# --- Logging setup ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    stream=sys.stdout,
    force=True
)
sys.stdout.reconfigure(line_buffering=True)

# --- Disable SSL warnings (for local ES) ---
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# --- Environment setup ---
ES_HOST = os.environ.get("ELASTICSEARCH_HOST", "http://elasticsearch:9200")
PRICE_INDEX = "vardhman_prices"
PRED_INDEX = "vardhman_predictions"
LOOKBACK = int(os.environ.get("LOOKBACK", 200))
INTERVAL = int(os.environ.get("PRED_INTERVAL", 30))

# --- Connect to Elasticsearch with retries ---
es = None
max_retries = 15
for attempt in range(max_retries):
    try:
        es = Elasticsearch([ES_HOST], verify_certs=False, request_timeout=30)
        if es.ping():
            logging.info(f"✅ Connected to Elasticsearch successfully at {ES_HOST}")
            break
        else:
            raise Exception("Ping failed.")
    except Exception as e:
        logging.warning(f"⚠️ Elasticsearch not ready (attempt {attempt+1}/{max_retries}): {e}")
        time.sleep(5)
else:
    logging.error("❌ Could not connect to Elasticsearch after retries. Exiting.")
    raise SystemExit(1)


# --- Fetch prices from ES ---
def fetch_prices(limit=LOOKBACK):
    try:
        q = {
            "size": limit,
            "sort": [{"timestamp": {"order": "asc"}}],
            "query": {"match_all": {}}
        }
        res = es.search(index=PRICE_INDEX, body=q)
        hits = res.get("hits", {}).get("hits", [])
        prices = [
            float(h["_source"]["price"])
            for h in hits
            if "_source" in h and "price" in h["_source"]
        ]
        return prices
    except Exception as e:
        logging.warning(f"⚠️ Error fetching prices: {e}")
        return []


# --- Train and predict ---
def train_and_predict(prices):
    if len(prices) < 3:
        return None
    y = np.array(prices)
    X = np.arange(len(y)).reshape(-1, 1)
    model = LinearRegression().fit(X, y)
    pred = model.predict([[len(y)]])[0]
    return float(pred)


# --- Write prediction to ES ---
def write_prediction(pred):
    doc = {
        "timestamp": datetime.utcnow().isoformat(),
        "symbol": "VTL.NS",
        "company": "Vardhman Textiles Ltd",
        "predicted_price": round(float(pred), 2),
    }
    try:
        es.index(index=PRED_INDEX, document=doc)
        logging.info(f"📤 Wrote prediction ₹{doc['predicted_price']} at {doc['timestamp']}")
    except Exception as e:
        logging.warning(f"⚠️ Error writing prediction: {e}")


# --- Main loop ---
if __name__ == "__main__":
    while True:
        try:
            prices = fetch_prices()
            if prices:
                pred = train_and_predict(prices)
                if pred is not None:
                    write_prediction(pred)
                else:
                    logging.info("⚠️ Not enough data to predict yet.")
            else:
                logging.info("⚠️ No price data found.")
        except Exception as e:
            logging.error(f"❌ Predictor error: {e}")
        time.sleep(INTERVAL)
