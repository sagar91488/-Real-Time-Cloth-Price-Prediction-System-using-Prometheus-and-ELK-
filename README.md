🎯 Real-Time Cloth Price Prediction System using Prometheus and ELK
This project is a real-time cloth/stock price prediction system that combines Machine Learning, Prometheus, and the ELK Stack (Elasticsearch + Kibana).
It fetches the latest price from the internet, predicts the future value, stores everything in Elasticsearch, and shows live dashboards in Kibana and Prometheus.

📌 Features
🔹 Real-Time Cloth/Stock Price Fetching
Fetches latest market price (e.g., Vardhman Textiles – VTL.NS) automatically at fixed intervals.

🔹 Machine Learning Prediction
Uses a lightweight regression model to predict the upcoming cloth price.

🔹 Elasticsearch Storage
Stores both actual & predicted prices with exact timestamps:

price

predicted_price

symbol

company

timestamp

🔹 Live Kibana Dashboard
Visualizes:

price trend

predicted vs actual values

time-series chart

instant updates

🔹 Prometheus Metrics Monitoring
Exports real-time metrics via /metrics:

nginx
Copy code
cloth_price_current  
cloth_price_predicted  
cloth_last_update_timestamp
Prometheus displays continuously updated graphs of both current and predicted prices.

🔹 Docker Automated Deployment
Runs the entire system (ELK + Prometheus + Exporter + Predictor) using:

css
Copy code
docker compose up --build
🛠️ Technologies Used
Python – Core logic

Machine Learning (Linear Regression) – Prediction

Yahoo Finance API / Public Data – Live price source

Elasticsearch – Time-series storage

Kibana – Visualization dashboard

Prometheus – Monitoring & metrics scraping

Docker & Docker Compose – Deployment

Pandas, NumPy, Requests – Data handling

🧠 How It Works
👉 1. Live Price Fetching
A Python exporter retrieves the cloth/stock price from Yahoo Finance or a dataset URL.

👉 2. Prediction Engine
Another Python service fetches recent values from Elasticsearch → predicts next price → stores prediction.

👉 3. Exporter for Prometheus
A custom /metrics endpoint exposes:

latest price

latest predicted price

last update timestamp

Prometheus scrapes and graphs these values every few seconds.

👉 4. Data Visualization (Kibana)
Kibana reads indexed data from Elasticsearch and displays:

Real-time price charts

Predicted vs actual

Time-based trend analytics

📁 Outputs
📊 Elasticsearch
Two indices:

cloth_prices

cloth_predictions

Each record includes:

price

predicted_price

timestamp

symbol

company name

📈 Prometheus Metrics Example
nginx
Copy code
cloth_price_current 438.25
cloth_price_predicted 440.58
cloth_last_update_timestamp 1730589120
🖥️ Kibana Dashboards
Line chart of live prices

Prediction trend visualization

Auto-refresh every second

🐳 How to Run the Full Project
1️⃣ Clone the Repository
sql
Copy code
git clone https://github.com/yourusername/Real-Time-Cloth-Price-Prediction-System-using-Prometheus-and-ELK.git
cd Real-Time-Cloth-Price-Prediction-System-using-Prometheus-and-ELK
2️⃣ Start All Services
css
Copy code
docker compose up --build
3️⃣ Open Dashboards
Service	URL
Kibana	http://localhost:5601
Elasticsearch	http://localhost:9200
Prometheus	http://localhost:9090
Metrics Exporter	http://localhost:8000/metrics

📌 Use Cases
This system is ideal for:

Cloth market price monitoring

Textile industry analytics

Supply chain & procurement planning

Business forecasting

Research & academic projects

Any application requiring real-time prediction + visualization

