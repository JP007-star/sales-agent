# Sales Agent - Streamlit Application

A comprehensive sales management tool built with Streamlit, featuring lead tracking, pipeline visualization, outreach automation, and analytics dashboard.

## Features

### 📊 Dashboard
- Real-time KPI metrics (leads, deals, pipeline value, conversion rate)
- Pipeline funnel visualization
- Revenue trend charts
- Recent activity feed
- Upcoming tasks

### 👥 Leads Management
- Add, edit, delete leads with full details
- Filter and search leads
- Lead scoring algorithm
- Activity history per lead
- Task management per lead
- Bulk actions support

### 📈 Pipeline (Kanban Board)
- Visual Kanban board with 7 stages
- Drag-and-drop simulation for stage changes
- Pipeline value by stage
- Stage aging analysis
- Conversion funnel

### 📧 Outreach Center
- Email composer with variable substitution
- Campaign management
- Template library with categories
- Outreach analytics (open rates, click rates, reply rates)

### 📈 Analytics Dashboard
- Lead velocity charts
- Revenue trends
- Team performance
- Lead score distribution
- Activity heatmap
- Pipeline aging
- Detailed data tables with export

### ⚙️ Settings
- Profile management
- Notification preferences
- Integrations (Gmail, Outlook, HubSpot, Salesforce, LinkedIn, Zoom, Calendly, Slack, Zapier)
- Pipeline stage customization
- Team management
- Data export/import
- Data retention policies

## Installation

```bash
# Navigate to the project directory
cd sales-agent

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

## Project Structure

```
sales-agent/
├── app.py                 # Main application entry point
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── components/           # UI components
│   ├── __init__.py
│   ├── sidebar.py        # Navigation sidebar
│   ├── leads.py          # Leads management
│   ├── pipeline.py       # Pipeline Kanban board
│   ├── outreach.py       # Email outreach & campaigns
│   ├── analytics.py      # Analytics dashboard
│   └── settings.py       # Settings & configuration
├── utils/                # Utility modules
│   ├── __init__.py
│   ├── data_manager.py   # Data persistence layer
│   └── helpers.py        # Helper functions
├── styles/               # Custom CSS
│   └── main.css          # Main stylesheet
└── data/                 # JSON data files (auto-created)
    ├── leads.json
    ├── activities.json
    ├── tasks.json
    ├── campaigns.json
    └── templates.json
```

## Data Persistence

Data is stored locally in JSON files in the `data/` directory:
- `leads.json` - Lead information
- `activities.json` - Activity log
- `tasks.json` - Task management
- `campaigns.json` - Email campaigns
- `templates.json` - Email templates

## Lead Scoring Algorithm

Leads are automatically scored (0-100) based on:
- **Stage** (10-100 points): New=10, Contacted=20, Qualified=40, Proposal=60, Negotiation=80, Closed Won=100
- **Deal Value** (0-30 points): $100K+=30, $50K+=20, $10K+=10, >$0=5
- **Source** (0-15 points): Referral/Partner=15, Event=10, Website/Email/Social=5
- **Engagement** (0-15 points): Last contacted=10, Next follow-up scheduled=5

Score Labels:
- 🔥 Hot (≥80)
- 🌡️ Warm (60-79)
- ❄️ Cool (40-59)
- 🧊 Cold (<40)

## Customization

### Adding Pipeline Stages
Go to Settings → Pipeline Stages to add, remove, or reorder stages with custom colors and win probabilities.

### Email Templates
Pre-built templates included:
- Initial Cold Outreach
- Follow-up After No Response
- Proposal Follow-up
- Referral Request
- Meeting Confirmation

Variables available: `{name}`, `{company}`, `{sender_name}`, `{sender_email}`, `{sender_title}`

### Integrations
Configure integrations in Settings → Integrations:
- Gmail/Google Workspace
- Outlook/Office 365
- HubSpot CRM
- Salesforce
- LinkedIn Sales Navigator
- Zoom
- Calendly
- Slack
- Zapier

## Keyboard Shortcuts

- `N` - New Lead (when not in input field)
- `C` - New Campaign
- `T` - New Task
- `Escape` - Close modals

## Browser Support

- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

## License

MIT License - Feel free to use and modify for your sales team.