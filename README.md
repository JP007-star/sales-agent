# JP Sales Agent Suite

A unified repository containing two Streamlit applications for B2B sales management and Instagram affiliate marketing automation.

## 🏗️ Architecture

```
sales-agent/
├── crm-core/                    # Shared modules
│   ├── utils/
│   │   ├── data_manager.py      # JSON persistence (leads, activities, tasks, campaigns, templates)
│   │   └── helpers.py           # Formatters, validators, lead scoring
│   └── styles/
│       └── main.css             # Teal theme for Sales Pipeline
├── sales-pipeline/              # B2B Sales Management (renamed from Sales Agent)
│   ├── app.py
│   ├── components/              # sidebar, dashboard, leads, pipeline, outreach, analytics, settings, help
│   ├── utils/ (imports from crm-core)
│   └── styles/ (imports from crm-core)
├── affiliate-studio/            # Instagram Affiliate Marketing (renamed from JP Finds Deals)
│   ├── app.py
│   ├── components/              # sidebar, dashboard, product_manager, content_studio, approval_queue, analytics, settings, workflows, help
│   ├── utils/ (project-specific: Indian currency, marketplace extraction, product scoring, hashtags, Gemini)
│   └── assets/style.css         # Orange theme
├── launcher/                    # Unified launch scripts
│   ├── run_all.py
│   ├── run_all.bat
│   ├── run_all.ps1
│   └── run_all.sh
├── test_business_cases.py       # 72 comprehensive tests
└── README.md
```

## 🚀 Applications

### 1. Sales Pipeline (Port 8501)
**B2B Sales Management Tool**
- Lead tracking with scoring (0-100)
- 7-stage pipeline visualization (Kanban + Funnel)
- Outreach automation (templates, campaigns, sequences)
- Analytics dashboard (conversion funnels, team performance, activity heatmaps)
- JSON file-based persistence

### 2. Affiliate Studio (Port 8502) 
**AI-Powered Instagram Affiliate Marketing for @jp.finds.deals**
- Product Manager: Add Amazon/Flipkart products, auto-scoring (0-100)
- Content Studio: AI generates Reels/Stories/Carousels in English, Tamil, Tanglish
- Approval Queue: Review workflow (Pending → Approved → Published/Rejected)
- Analytics: Conversion funnel, category performance, commission tracking
- Workflows: 8 n8n automation workflows for scheduling/publishing
- Video prompts export for Google Flow, FFmpeg, Canva

---

## 🛠️ Local Development

### Prerequisites
- Python 3.10+
- pip

### Quick Start

```bash
# Clone repository
git clone https://github.com/yourusername/sales-agent.git
cd sales-agent

# Install dependencies for both apps
pip install -r sales-pipeline/requirements.txt
pip install -r affiliate-studio/requirements.txt

# Option 1: Run both apps with unified launcher (recommended)
python launcher/run_all.py

# Option 2: Run individually
# Terminal 1 - Sales Pipeline
streamlit run sales-pipeline/app.py --server.port 8501

# Terminal 2 - Affiliate Studio
streamlit run affiliate-studio/app.py --server.port 8502
```

### Platform-Specific Launchers
```bash
# Windows Batch
launcher\run_all.bat

# Windows PowerShell
launcher\run_all.ps1

# Linux/macOS
./launcher/run_all.sh
```

**Access URLs:**
- Sales Pipeline: http://localhost:8501
- Affiliate Studio: http://localhost:8502

---

## 🧪 Testing

```bash
# Run all 72 business case tests
python -m pytest test_business_cases.py -v

# Run with coverage
python -m pytest test_business_cases.py --cov=sales-pipeline --cov=affiliate-studio
```

**Test Coverage:**
- Sales Pipeline: DataManager CRUD, lead scoring, pipeline metrics, helpers
- Affiliate Studio: Product scoring, Indian currency formatting, hashtag generation, Gemini parsing
- Integration: End-to-end workflows, edge cases, performance

---

## ☁️ Deployment Guide

### 1. Streamlit Community Cloud (Free, Easiest)

Best for public repositories. Auto-deploys from GitHub.

**Steps:**
1. Push this repo to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Click "New app" → Select your repo
4. **For Sales Pipeline:** Main file path: `sales-pipeline/app.py`
5. **For Affiliate Studio:** Main file path: `affiliate-studio/app.py`
6. Add secrets in Settings → Secrets (see format below)

**Secrets format (`.streamlit/secrets.toml`):**
```toml
# Sales Pipeline
GEMINI_API_KEY = "your-gemini-key"

# Affiliate Studio  
GEMINI_API_KEY = "your-gemini-key"
INSTAGRAM_APP_ID = "xxx"
INSTAGRAM_APP_SECRET = "xxx"
INSTAGRAM_ACCESS_TOKEN = "xxx"
INSTAGRAM_BUSINESS_ACCOUNT_ID = "xxx"
AMAZON_ASSOCIATE_TAG = "your-tag"
# ... other API keys
```

---

### 2. Docker Deployment (Production Ready)

**Dockerfile (project root):**
```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY sales-pipeline/requirements.txt sales-pipeline/
COPY affiliate-studio/requirements.txt affiliate-studio/
RUN pip install -r sales-pipeline/requirements.txt && pip install -r affiliate-studio/requirements.txt
COPY . .
EXPOSE 8501 8502
CMD ["python", "launcher/run_all.py"]
```

**Build & Run:**
```bash
docker build -t sales-agent-suite .
docker run -d -p 8501:8501 -p 8502:8502 sales-agent-suite
```

**Docker Compose (`docker-compose.yml`):**
```yaml
version: '3.8'
services:
  sales-pipeline:
    build: .
    command: python -m streamlit run sales-pipeline/app.py --server.port 8501 --server.address 0.0.0.0
    ports:
      - "8501:8501"
    volumes:
      - ./sales-pipeline/data:/app/sales-pipeline/data
      - ./crm-core:/app/crm-core
    environment:
      - GEMINI_API_KEY=${GEMINI_API_KEY}
  
  affiliate-studio:
    build: .
    command: python -m streamlit run affiliate-studio/app.py --server.port 8502 --server.address 0.0.0.0
    ports:
      - "8502:8502"
    volumes:
      - ./affiliate-studio/data:/app/affiliate-studio/data
    environment:
      - GEMINI_API_KEY=${GEMINI_API_KEY}
      - INSTAGRAM_APP_ID=${INSTAGRAM_APP_ID}
      - INSTAGRAM_APP_SECRET=${INSTAGRAM_APP_SECRET}
      - INSTAGRAM_ACCESS_TOKEN=${INSTAGRAM_ACCESS_TOKEN}
      - INSTAGRAM_BUSINESS_ACCOUNT_ID=${INSTAGRAM_BUSINESS_ACCOUNT_ID}
      - AMAZON_ASSOCIATE_TAG=${AMAZON_ASSOCIATE_TAG}
      - FLIPKART_AFFILIATE_ID=${FLIPKART_AFFILIATE_ID}
      - FLIPKART_AFFILIATE_TOKEN=${FLIPKART_AFFILIATE_TOKEN}
```

**Run with Compose:**
```bash
docker-compose up -d
```

---

### 3. Cloud VM (AWS EC2, DigitalOcean, GCP, Azure)

**Ubuntu 22.04 Setup:**
```bash
# On server
sudo apt update && sudo apt install -y python3 python3-pip nginx git

# Clone repo
git clone https://github.com/yourusername/sales-agent.git
cd sales-agent

# Install dependencies
pip3 install -r sales-pipeline/requirements.txt
pip3 install -r affiliate-studio/requirements.txt

# Create systemd services
sudo tee /etc/systemd/system/sales-pipeline.service > /dev/null <<EOF
[Unit]
Description=Sales Pipeline Streamlit
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/sales-agent
ExecStart=/usr/local/bin/python -m streamlit run sales-pipeline/app.py --server.port 8501 --server.address 0.0.0.0
Restart=always
Environment=GEMINI_API_KEY=your-key

[Install]
WantedBy=multi-user.target
EOF

sudo tee /etc/systemd/system/affiliate-studio.service > /dev/null <<EOF
[Unit]
Description=Affiliate Studio Streamlit
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/sales-agent
ExecStart=/usr/local/bin/python -m streamlit run affiliate-studio/app.py --server.port 8502 --server.address 0.0.0.0
Restart=always
Environment=GEMINI_API_KEY=your-key
Environment=INSTAGRAM_APP_ID=xxx
Environment=INSTAGRAM_APP_SECRET=xxx
Environment=INSTAGRAM_ACCESS_TOKEN=xxx
Environment=INSTAGRAM_BUSINESS_ACCOUNT_ID=xxx
Environment=AMAZON_ASSOCIATE_TAG=xxx

[Install]
WantedBy=multi-user.target
EOF

# Start services
sudo systemctl daemon-reload
sudo systemctl enable --now sales-pipeline affiliate-studio

# Nginx reverse proxy (optional - for custom domains)
sudo tee /etc/nginx/sites-available/sales-agent <<EOF
server {
    listen 80;
    server_name your-domain.com;

    location /pipeline/ {
        proxy_pass http://localhost:8501/;
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection "upgrade";
    }

    location /studio/ {
        proxy_pass http://localhost:8502/;
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
EOF
sudo ln -s /etc/nginx/sites-available/sales-agent /etc/nginx/sites-enabled/
sudo nginx -t && sudo systemctl reload nginx
```

---

### 4. Platform-Specific Quick Deploy

| Platform | Command |
|----------|---------|
| **Render** | Connect repo → New Web Service → Build: `pip install -r sales-pipeline/requirements.txt && pip install -r affiliate-studio/requirements.txt`, Start: `python launcher/run_all.py` |
| **Railway** | `railway init` → `railway up` |
| **Fly.io** | `fly launch` → edit `fly.toml` for dual ports |
| **Heroku** | `heroku create` → `git push heroku main` (needs `Procfile`) |

**Heroku `Procfile`:**
```
web: python launcher/run_all.py
```

---

### 5. Production Configuration

**In both `app.py` files, add before `st.set_page_config()`:**
```python
import os

# Allow external access
os.environ["STREAMLIT_SERVER_ADDRESS"] = "0.0.0.0"
os.environ["STREAMLIT_SERVER_HEADLESS"] = "true"

# Disable usage stats
os.environ["STREAMLIT_BROWSER_GATHER_USAGE_STATS"] = "false"

# For reverse proxy subpaths
# os.environ["STREAMLIT_SERVER_BASE_URL_PATH"] = "/pipeline"  # or "/studio"
```

**File permissions for JSON data:**
```bash
chmod 755 sales-pipeline/data affiliate-studio/data
chmod 644 sales-pipeline/data/*.json affiliate-studio/data/*.json
```

---

### 6. Environment Variables

Create `.env` file (add to `.gitignore`):
```bash
# Shared
GEMINI_API_KEY=your-gemini-key

# Affiliate Studio
INSTAGRAM_APP_ID=xxx
INSTAGRAM_APP_SECRET=xxx
INSTAGRAM_ACCESS_TOKEN=xxx
INSTAGRAM_BUSINESS_ACCOUNT_ID=xxx
AMAZON_ASSOCIATE_TAG=xxx
AMAZON_ACCESS_KEY=xxx
AMAZON_SECRET_KEY=xxx
FLIPKART_AFFILIATE_ID=xxx
FLIPKART_AFFILIATE_TOKEN=xxx
CANVA_API_TOKEN=xxx
```

**Load in app.py:**
```python
from dotenv import load_dotenv
load_dotenv()  # Add python-dotenv to requirements.txt
```

---

## 📋 Quick Reference

| Use Case | Best Deployment Option |
|----------|------------------------|
| Demo/Portfolio | Streamlit Community Cloud (free) |
| Team Internal Tool | Docker + VPS (DigitalOcean $6/mo) |
| Production SaaS | Docker + AWS ECS / GCP Cloud Run / Kubernetes |
| Client Delivery | Docker Compose on their server |

---

## 🔑 API Keys Required

### Sales Pipeline
| Key | Purpose |
|-----|---------|
| `GEMINI_API_KEY` | AI content generation (optional) |

### Affiliate Studio
| Key | Source | Required |
|-----|--------|----------|
| `GEMINI_API_KEY` | Google AI Studio | ✅ Yes |
| `INSTAGRAM_APP_ID` | Meta Developers | ✅ Yes |
| `INSTAGRAM_APP_SECRET` | Meta Developers | ✅ Yes |
| `INSTAGRAM_ACCESS_TOKEN` | Meta Graph API | ✅ Yes |
| `INSTAGRAM_BUSINESS_ACCOUNT_ID` | Meta Business Suite | ✅ Yes |
| `AMAZON_ASSOCIATE_TAG` | Amazon Associates | ✅ Yes |
| `AMAZON_ACCESS_KEY` | AWS IAM (PA-API) | Optional |
| `AMAZON_SECRET_KEY` | AWS IAM (PA-API) | Optional |
| `FLIPKART_AFFILIATE_ID` | Flipkart Affiliate | Optional |
| `FLIPKART_AFFILIATE_TOKEN` | Flipkart Affiliate | Optional |
| `CANVA_API_TOKEN` | Canva Developers | Optional |

---

## 📚 Help & Documentation

Both apps include comprehensive in-app help:
- **Sales Pipeline**: Help tab covers Getting Started, Leads, Pipeline, Outreach, Analytics, Settings
- **Affiliate Studio**: Help tab covers Getting Started, Product Manager, Content Studio, Approval Queue, Analytics, Workflows, Settings

**Keyboard Shortcut:** `Ctrl/Cmd + /` opens help in both apps.

---

## 📄 License

MIT License - Feel free to use and modify for your team.

---

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Run tests (`python -m pytest test_business_cases.py -v`)
4. Commit changes (`git commit -m 'Add amazing feature'`)
5. Push to branch (`git push origin feature/amazing-feature`)
6. Open Pull Request