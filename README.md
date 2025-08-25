# ⚽ MATCH_PREDICTOR
A data pipeline project that fetches football (soccer) match data from API-Football, 
preprocesses it with Python, and uploads it to Supabase.  
The project is fully automated using **Docker + AWS Lambda + EventBridge**.

## 🚀 Features
- Fetch EPL 2023/24 fixtures, team stats, player stats from [API-Football](https://www.api-football.com/)
- Preprocess raw JSON into clean DataFrames with Pandas
- Upload structured tables into **Supabase** (PostgreSQL)
- Automated daily updates with **AWS Lambda + EventBridge**
- Containerized with **Docker** and deployed to **AWS ECR**

## 📂 Project Structure
- `api/` → API calls (fixtures, teams, players)
- `processing/` → Data preprocessing
- `pipeline/` → Uploading to Supabase
- `main.py` → Full ETL pipeline
- `Dockerfile` → Containerization for AWS Lambda

## 🛠️ Tech Stack
- **Python** (Pandas, Requests)
- **Supabase** (PostgreSQL backend)
- **Docker**
- **AWS (Lambda, EventBridge, CloudWatch, ECR)**

## ⚡ Automation
The pipeline runs **daily at midnight (CST)** using AWS EventBridge and automatically updates Supabase.

## 📊 Example Workflow
1. Fetch fixtures from API-Football
2. Preprocess into DataFrames
3. Upload to Supabase
4. Logs and errors tracked with AWS CloudWatch

## 🔒 Environment Variables
Store my credentials in `.env` file:
