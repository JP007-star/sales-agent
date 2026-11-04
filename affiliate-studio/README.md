# JP Finds Deals - AI Sales Agent

> **@jp.finds.deals** - Automated AI-powered Instagram Affiliate Marketing System

A complete Streamlit application for managing product discovery, AI content generation (English/Tamil), approval workflows, Instagram publishing, and affiliate revenue tracking.

## 🎯 Overview

Transform your Instagram account **@jp.finds.deals** into an automated AI-powered affiliate marketing business:

- **Product Discovery**: Add products from Amazon, Flipkart, and other marketplaces
- **AI Content Generation**: Gemini AI creates Reel scripts in English, Tamil, and mixed (Tanglish)
- **Video Prompts**: Detailed scene-by-scene prompts for Canva, Google Flow, or FFmpeg
- **Approval Workflow**: Review and approve content before publishing
- **Instagram Publishing**: Publish via Meta Graph API (when configured)
- **Affiliate Tracking**: Track clicks, conversions, and commission earnings
- **Analytics Dashboard**: Views, engagement, revenue by category/marketplace

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- Git
- Google Gemini API key (free tier available)

### Installation

```bash
# Clone or navigate to the project
cd jp-finds-deals-ai-agent

# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Copy environment template
copy .env.example .env  # Windows
# cp .env.example .env  # Linux/Mac

# Edit .env with your API keys
notepad .env  # Windows
# nano .env   # Linux/Mac
```

### Configuration

Edit `.env` with your credentials:

```env
# Required for AI content generation
GEMINI_API_KEY=your_gemini_api_key_here

# Required for Instagram publishing (optional for local testing)
INSTAGRAM_APP_ID=your_app_id
INSTAGRAM_APP_SECRET=your_app_secret
INSTAGRAM_ACCESS_TOKEN=your_access_token
INSTAGRAM_BUSINESS_ACCOUNT_ID=your_business_account_id

# Required for affiliate link generation
AMAZON_ASSOCIATE_TAG=yourtag-21
AMAZON_ACCESS_KEY=your_access_key
AMAZON_SECRET_KEY=your_secret_key
```

### Run the App

```bash
streamlit run app.py
```

Open **http://localhost:8501** in your browser.

## 📁 Project Structure

```
jp-finds-deals-ai-agent/
├── app.py                 # Main Streamlit entry point
├── requirements.txt       # Python dependencies
├── .env.example          # Environment template
├── README.md             # This file
├── components/           # Streamlit UI components
│   ├── __init__.py
│   ├── sidebar.py        # Navigation sidebar
│   ├── dashboard.py      # Overview dashboard
│   ├── product_manager.py # Product CRUD & management
│   ├── content_studio.py # AI content generation
│   ├── approval_queue.py # Approval workflow
│   ├── analytics.py      # Analytics & reports
│   ├── settings.py       # Configuration
│   └── workflows.py      # n8n workflow management
├── utils/                # Utility modules
│   ├── __init__.py
│   ├── helpers.py        # Formatters, validators, scoring
│   └── gemini_client.py  # Gemini AI integration
├── assets/               # Static assets
│   └── style.css         # Custom dark theme
└── data/                 # Local JSON storage (auto-created)
    ├── products.json
    ├── content_drafts.json
    ├── approval_queue.json
    └── published_posts.json
```

## 🎨 Features Walkthrough

### 1. Dashboard
- Real-time KPIs: Products, pending approvals, published Reels, commission
- Visual pipeline funnel
- Category distribution
- Top performing products

### 2. Product Manager
- Add products via URL (Amazon/Flipkart auto-detection)
- Manual product entry with all details
- Affiliate link management
- Product scoring algorithm (0-100)
- Status tracking: discovered → analyzed → content_generated → video_ready → approved → published
- Bulk actions & CSV export

### 3. Content Studio (AI Powered)
- **Gemini AI Integration**: Generates complete promotional content
- **Multi-language**: English, Tamil, English+Tamil (Tanglish)
- **Reel Scripts**: 4 scenes (Hook → Intro → Benefits → CTA)
- **SEO Package**: Caption, 20-30 hashtags, keywords, disclosure
- **Video Prompts**: Scene-by-scene for Canva/Flow/FFmpeg
- **Canva Templates**: 6 branded template types
- **Draft Management**: Save, edit, duplicate, export

### 4. Approval Queue
- **Pending Review**: Items awaiting your approval
- **Approved**: Ready to publish
- **Published**: Live posts with performance
- **Rejected**: Archive with restore option
- **Scheduling**: Set date/time for future publishing
- **Export Packages**: Download for manual publishing

### 5. Analytics
- **Content Metrics**: Views, engagement rate, CTR
- **Affiliate Revenue**: Clicks, conversions, commission
- **Category Performance**: Views & revenue by product category
- **Posting Frequency**: Best days/times
- **Conversion Funnel**: Views → Clicks → Conversions
- **Top Posts**: Ranked by views/engagement/commission
- **Export Reports**: JSON/CSV download

### 6. Settings
- **API Keys**: Gemini, Canva
- **Instagram**: Meta Graph API configuration
- **Marketplaces**: Amazon Associates, Flipkart Affiliate
- **Brand Identity**: Colors, fonts, logo, watermark, default hashtags
- **Publishing**: Schedule slots, auto-publish toggle, daily targets
- **Workflows**: n8n connection, variables, rate limits
- **Data**: Export/import, retention, backup

### 7. Workflows (n8n)
- 8 pre-built automation workflows
- Downloadable JSON for n8n import
- Manual trigger buttons
- Execution logs
- Configuration management

## 🤖 AI Content Generation Details

### Prompt Engineering
The system uses carefully crafted prompts for Gemini 1.5 Flash that generate:

1. **Hooks** (4 styles): Curiosity, Problem/Solution, Budget Saving, Visual Demo
2. **Scripts** (4 scenes × 3 languages): 15-30 second Reels
3. **SEO**: Caption, hashtags, keywords, disclosure
4. **Video Prompts**: Detailed for AI video tools

### Language Support
- **English**: Natural Indian English with Hinglish
- **Tamil**: Pure Tamil (தமிழ்) with colloquial expressions
- **Tanglish**: English+Tamil mixed naturally

### Cost Optimization
- Uses Gemini 1.5 Flash (cheapest tier)
- Estimated cost: ~$0.001 per product content generation
- Free tier: 15 RPM, 1M tokens/day

## 🔗 Affiliate Integration

### Amazon Associates (India)
- Associate Tag for link generation
- Product Advertising API for automated discovery
- Commission tracking via Amazon reports

### Flipkart Affiliate
- Affiliate ID & Token
- API integration for product feeds
- Commission tracking

### Link Format
```
Amazon: https://www.amazon.in/dp/{PRODUCT_ID}?tag={ASSOCIATE_TAG}
Flipkart: https://dl.flipkart.com/dl/{PRODUCT_ID}
```

## 📊 n8n Workflow Automation

The system includes 8 n8n workflows for full automation:

| # | Workflow | Trigger | Description |
|---|----------|---------|-------------|
| 1 | Product Intake | Webhook | Receive URLs, validate, save, trigger AI |
| 2 | Product Discovery | Cron (9 AM) | Query APIs, score, deduplicate |
| 3 | AI Content Gen | Webhook | Gemini → scripts, SEO, video prompts |
| 4 | Video Production | Webhook | Canva assets, video prompts, FFmpeg |
| 5 | Approval | Webhook | Notify, wait for approval, move to queue |
| 6 | Instagram Publish | Cron/Webhook | Meta Graph API publish, save media ID |
| 7 | Daily Scheduling | Cron (8 AM) | Generate 2 drafts daily |
| 8 | Analytics | Cron (6 AM) | Instagram insights, affiliate reports |

### Running n8n Locally

```bash
# Using Docker (recommended)
docker run -it --rm \
  -p 5678:5678 \
  -v n8n_data:/home/node/.n8n \
  n8nio/n8n

# Or with docker-compose (includes PostgreSQL)
docker-compose up -d
```

Access n8n at **http://localhost:5678** (default: admin/admin)

## 💾 Data Persistence

Data is stored locally in JSON files (no database required for basic usage):

| File | Description |
|------|-------------|
| `products.json` | All discovered products |
| `content_drafts.json` | AI-generated content drafts |
| `approval_queue.json` | Approval workflow items |
| `published_posts.json` | Published posts with analytics |

For production, use PostgreSQL with the provided schema.

## 🔒 Security

- All API keys stored in `.env` (never committed)
- Session-based authentication (extend for multi-user)
- Input validation on all forms
- Rate limiting configuration for APIs
- Secure file handling for uploads

## 🚢 Deployment Options

### Local Development (Current)
```bash
streamlit run app.py
```

### Docker (Recommended for Production)
```dockerfile
# Dockerfile included in project
docker build -t jp-finds-deals .
docker run -p 8501:8501 --env-file .env jp-finds-deals
```

### Streamlit Cloud
1. Push to GitHub
2. Connect to Streamlit Cloud
3. Add secrets from `.env`
4. Deploy

### With n8n + PostgreSQL
```bash
docker-compose up -d
# Runs: Streamlit (3000), Backend (8000), n8n (5678), PostgreSQL (5432)
```

## 📈 Roadmap

### Phase 1 - Foundation ✅
- [x] Product management
- [x] AI content generation
- [x] Approval workflow
- [x] Basic analytics

### Phase 2 - Publishing
- [ ] Instagram Graph API integration
- [ ] Video generation pipeline (Canva/Flow/FFmpeg)
- [ ] Automated scheduling

### Phase 3 - Affiliate Business
- [ ] Amazon PA-API integration
- [ ] Flipkart API integration
- [ ] Automated commission import

### Phase 4 - Optimization
- [ ] A/B testing for hooks
- [ ] Performance-based product scoring
- [ ] Advanced analytics (cohort, LTV)

## 🛠️ Troubleshooting

### "Gemini API key not configured"
Add `GEMINI_API_KEY` to your `.env` file.

### "streamlit not recognized"
Use `python -m streamlit run app.py` instead.

### Port already in use
Change port: `streamlit run app.py --server.port 8502`

### n8n workflows not importing
Ensure n8n version compatibility. Workflows designed for n8n 1.0+

### Low content quality
- Adjust prompt in `utils/gemini_client.py`
- Provide more detailed custom instructions
- Check product data completeness

## 🤝 Contributing

1. Fork the repository
2. Create feature branch
3. Make changes
4. Test locally
5. Submit PR

## 📄 License

MIT License - Free to use and modify for your affiliate marketing business.

## 🙏 Acknowledgments

- **Google Gemini** for AI content generation
- **Streamlit** for the amazing framework
- **n8n** for workflow automation
- **Plotly** for beautiful charts
- **@jp.finds.deals** community for inspiration

---

**Built with ❤️ for the @jp.finds.deals community**

*Daily Shopping Bestie 💖 | Fashion | Beauty | Tech | Amazing Deals & Smart Finds*