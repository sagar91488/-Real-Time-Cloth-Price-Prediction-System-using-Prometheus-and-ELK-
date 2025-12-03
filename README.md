🎯 AI-Based Cloth Price Prediction System using Machine Learning
This project is a real-time cloth price prediction system that uses machine learning, Yahoo Finance API, Elasticsearch, Kibana, and Prometheus.
It fetches live stock/cloth prices, analyzes them, predicts the next expected price, and visualizes everything in dashboards.

📌 Features
🔹 Live Price Fetching
Fetches the latest market/cloth price (e.g., Vardhman Textiles – VTL.NS) in real time.

🔹 Automatic Prediction
Applies machine-learning (Linear Regression) to calculate next predicted price.

🔹 Stores Data in Elasticsearch
Saves live + predicted prices with exact timestamps.

🔹 Live Dashboards (Kibana)
Beautiful charts showing

price variations

predicted values

time-wise trends

🔹 Prometheus Monitoring
Live metrics for:

current price

predicted price

last update timestamp
Using /metrics endpoint.

🔹 Docker Support
Full stack (Elasticsearch + Kibana + Prometheus + Exporter + Predictor) runs with one command:

css
Copy code
docker compose up --build
🛠️ Technologies Used
Python – core logic

Machine Learning (Linear Regression) – prediction

Elasticsearch – data storage

Kibana – live visualization

Prometheus – monitoring + graphing

Yahoo Finance API – stock/cloth price source

Docker & Docker Compose – deployment

Requests, Pandas, NumPy – data handling

🧠 How It Works
👉 1. Live Price Fetching
Uses Yahoo Finance API to get latest cloth/stock price.

👉 2. Prediction Engine
Reads historical prices from Elasticsearch
→ Applies regression
→ Predicts next price
→ Saves prediction back to Elasticsearch.

👉 3. Metrics Exporter
Custom Python exporter exposes metrics to Prometheus:

nginx
Copy code
vardhman_stock_price  
vardhman_predicted_price  
vardhman_last_update_timestamp
👉 4. Data Visualization (Kibana)
Shows:

real-time price

predicted price

continuous trend graphs

live changes every few seconds/minutes

👉 5. Real-Time Monitoring (Prometheus)
Shows:

live updated metrics

accurate time-aligned graphs

supports alerts & dashboards

📁 Output
📄 Data Stored in Elasticsearch
Live price document

Predicted price document

Timestamp, company name, symbol

📊 Kibana Dashboard
Line graphs of price vs prediction

Time-based filters

Real-time updates

📡 Prometheus Metrics
Example:

nginx
Copy code
vardhman_stock_price 438.25
vardhman_predicted_price 440.12
vardhman_last_update_timestamp 1730589120
📌 Use Case
A practical tool for:

textile industries

stock-based cloth pricing analysis

price prediction dashboards

monitoring cloth price trends

decision-making for procurement, sourcing, and forecasting

Helps users visualize current vs predicted cloth prices with both ML and monitoring tools.
