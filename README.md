# JP Sales Agent Suite

A unified repository containing two Streamlit applications for sales and affiliate marketing automation.

## 📦 Projects

### 1. Sales Agent (`/sales-agent`)
**B2B Sales Management Dashboard**
- Lead management with Kanban pipeline
- Deal tracking & pipeline visualization
- Email outreach & campaign management
- Analytics dashboard with revenue trends
- Team performance tracking

**Run:** `cd sales-agent && streamlit run app.py`

---

### 2. JP Finds Deals (`/jp-finds-deals`)
**AI-Powered Instagram Affiliate Marketing** `@jp.finds.deals`
- Product discovery (Amazon, Flipkart)
- Gemini AI content generation (English/Tamil/Tanglish)
- Reel scripts, SEO captions, video prompts
- Approval workflow for publishing
- Affiliate click & commission tracking
- n8n workflow automation (8 workflows)

**Run:** `cd jp-finds-deals && streamlit run app.py`

---

## 🚀 Quick Start

```bash
# Clone the repo
git clone <repo-url>
cd jp-sales-agent-combined

# Install dependencies for both projects
cd sales-agent && pip install -r requirements.txt
cd ../jp-finds-deals && pip install -r requirements.txt

# Configure environment
cd jp-finds-deals
cp .env.example .env
# Edit .env with your API keys (Gemini required)

# Run either app
cd ../sales-agent && streamlit run app.py      # Port 8501
# OR
cd ../jp-finds-deals && streamlit run app.py   # Port 8502
```

---

## 📁 Repository Structure

```
jp-sales-agent-combined/
├── README.md                    # This file
├── sales-agent/                 # B2B Sales Dashboard
│   ├── app.py
│   ├── requirements.txt
│   ├── README.md
│   ├── components/
│   │   ├── sidebar.py
│   │   ├── dashboard.py
│   │   ├── leads.py
│   │   ├── pipeline.py
│   │   ├── outreach.py
│   │   ├── analytics.py
│   │   └── settings.py
│   ├── utils/
│   │   ├── data_manager.py
│   │   └── helpers.py
│   └── styles/
│       └── main.css
│
└── jp-finds-deals/              # AI Affiliate Marketing
    ├── app.py
    ├── requirements.txt
    ├── .env.example
    ├── README.md
    ├── components/
    │   ├── sidebar.py
    │   ├── dashboard.py
    │   ├── product_manager.py
    │   ├── content_studio.py
    │   ├── approval_queue.py
    │   ├── analytics.py
    │   ├── settings.py
    │   └── workflows.py
    ├── utils/
    │   ├── helpers.py
    │   └── gemini_client.py
    ├── assets/
    │   └── style.css
    └── workflows/               # n8n workflow JSONs (exported)
```

---

## 🔧 Shared Utilities

Both projects use similar patterns:
- **Streamlit** for UI
- **Plotly** for charts
- **Pandas** for data processing
- **Session state** for data persistence
- **Custom CSS** for dark theme

---

## 🔑 Required API Keys (JP Finds Deals)

| Service | Purpose | Free Tier |
|---------|---------|-----------|
| Google Gemini | AI content generation | 15 RPM, 1M tokens/day |
| Instagram Graph API | Publishing Reels | Requires Meta App approval |
| Amazon Associates | Affiliate links | Standard program |
| Flipkart Affiliate | Affiliate links | Standard program |
| Canva API | Design automation | Developer access required |

---

## 📊 Features Comparison

| Feature | Sales Agent | JP Finds Deals |
|---------|-------------|----------------|
| Lead/Deal Management | ✅ Full CRM | ❌ |
| Pipeline Kanban | ✅ 7 stages | ❌ |
| Email Campaigns | ✅ Templates | ❌ |
| AI Content Gen | ❌ | ✅ Gemini (3 languages) |
| Video Prompts | ❌ | ✅ Canva/Flow/FFmpeg |
| Approval Workflow | ❌ | ✅ Multi-stage |
| Affiliate Tracking | ❌ | ✅ Clicks/Commission |
| Instagram Publishing | ❌ | ✅ Graph API |
| n8n Automation | ❌ | ✅ 8 workflows |
| Analytics | ✅ Revenue/Team | ✅ Content/Affiliate |

---

## 🛠️ Development

Both apps are independent Streamlit applications. To modify:

1. Navigate to the project directory
2. Edit components in `components/`
3. Shared utilities in `utils/`
4. Styles in `styles/` or `assets/`

---

## 📄 License

MIT License - Free to use and modify.

---

## 🤝 Contributing

1. Fork the repository
2. Create feature branch
3. Make changes to either project
4. Test locally
5. Submit PR

---

**Built for sales automation & affiliate marketing success!** 🚀