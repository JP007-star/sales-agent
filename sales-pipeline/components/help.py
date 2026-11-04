"""
Help & Documentation component for Sales Pipeline.
Comprehensive guide on all features and how to use them.
"""

import streamlit as st


def render_help_tab():
    """Render the Help & Documentation page."""

    st.header("📚 Help & Documentation")
    st.caption("Complete guide to using Sales Pipeline effectively")

    # Create tabs for different help sections
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "🚀 Getting Started",
        "👥 Leads Management",
        "📊 Pipeline & Deals",
        "📧 Outreach & Campaigns",
        "📈 Analytics & Reports",
        "⚙️ Settings & Tips"
    ])

    # ========== TAB 1: GETTING STARTED ==========
    with tab1:
        render_getting_started()

    # ========== TAB 2: LEADS MANAGEMENT ==========
    with tab2:
        render_leads_help()

    # ========== TAB 3: PIPELINE ==========
    with tab3:
        render_pipeline_help()

    # ========== TAB 4: OUTREACH ==========
    with tab4:
        render_outreach_help()

    # ========== TAB 5: ANALYTICS ==========
    with tab5:
        render_analytics_help()

    # ========== TAB 6: SETTINGS ==========
    with tab6:
        render_settings_help()


def render_getting_started():
    """Getting Started guide."""

    st.subheader("🚀 Welcome to Sales Pipeline")

    st.markdown("""
    **Sales Pipeline** is a comprehensive B2B sales management tool designed to help you track leads,
    manage your sales pipeline, automate outreach, and analyze performance — all in one place.

    ### 🎯 Key Features at a Glance
    | Feature | Description |
    |---------|-------------|
    | **Dashboard** | Real-time overview of leads, pipeline value, and activities |
    | **Leads** | Full CRUD operations, filtering, scoring, and segmentation |
    | **Pipeline** | Visual funnel, drag-and-drop stage management |
    | **Outreach** | Email templates, campaigns, activity logging |
    | **Analytics** | Conversion funnels, team performance, revenue trends |
    | **Settings** | User preferences, integrations, data management |

    ### 🏁 Quick Start Checklist
    1. **Add your first lead** — Click ➕ *New Lead* in sidebar or Dashboard
    2. **Set up pipeline stages** — Go to Settings → Pipeline Stages
    3. **Create email templates** — Settings → Templates for consistent outreach
    4. **Log your first activity** — Call, meeting, or email from any lead
    5. **Review Analytics** — Check conversion rates and pipeline health weekly

    ### 💡 Pro Tips for New Users
    - **Use Lead Scoring**: Every lead gets an automatic score (0-100) based on stage, value, source, and engagement
    - **Keyboard Shortcuts**: Press `?` anywhere to see available shortcuts
    - **Data Persistence**: All data is saved locally as JSON — no database setup required
    - **Multi-user Ready**: Assign leads to team members (Me, Sarah, Mike, Emily)

    ### 🔄 Typical Daily Workflow
    ```
    Morning → Check Dashboard → Review Upcoming Tasks → Follow up on Hot leads
    → Log Activities → Update Pipeline Stages → End of Day → Review Analytics
    ```
    """)

    with st.expander("📖 Understanding the UI Layout"):
        st.markdown("""
        **Header Bar**: Shows today's date, total leads count, and pipeline value

        **Sidebar Navigation**:
        - 🏠 **Dashboard** — Executive overview with metrics, charts, and quick actions
        - 👥 **Leads** — Complete lead database with filters, search, and bulk actions
        - 📊 **Pipeline** — Visual funnel view, stage management, deal tracking
        - 📧 **Outreach** — Email campaigns, templates, sequence builder
        - 📈 **Analytics** — Deep-dive reports, conversion funnels, team performance
        - ⚙️ **Settings** — User config, integrations, data import/export

        **Quick Actions** (Dashboard): One-click buttons for common tasks
        """)

    with st.expander("⌨️ Keyboard Shortcuts"):
        st.markdown("""
        | Shortcut | Action |
        |----------|--------|
        `Ctrl/Cmd + N` | New Lead |
        `Ctrl/Cmd + K` | Search Leads |
        `Ctrl/Cmd + /` | Show this Help |
        `Esc` | Close Modal |
        `Enter` | Submit Form |
        """)


def render_leads_help():
    """Leads Management guide."""

    st.subheader("👥 Leads Management")

    st.markdown("""
    The Leads page is your central database for all prospects and customers.

    ### 📋 Lead Fields Explained
    | Field | Purpose | Required |
    |-------|---------|----------|
    | **Name** | Contact's full name | ✅ Yes |
    | **Email** | Primary contact email | ✅ Yes |
    | **Phone** | Direct line or mobile | Optional |
    | **Company** | Organization name | Optional |
    | **Source** | How they found you (Referral, Website, etc.) | ✅ Yes |
    | **Stage** | Current pipeline stage | ✅ Yes |
    | **Value** | Estimated deal size in USD | Optional |
    | **Assigned To** | Team member responsible | Optional |
    | **Notes** | Free-form context | Optional |

    ### 🔍 Filtering & Search
    - **Search Bar**: Type any name, email, company, or note content
    - **Stage Filter**: Click pipeline stages to filter instantly
    - **Assignee Filter**: View leads by team member
    - **Date Range**: Filter by creation or last updated date

    ### 🎯 Lead Scoring System
    Every lead receives an automatic score (0-100):

    | Score Range | Label | Meaning |
    |-------------|-------|---------|
    | 80-100 | 🔥 **Hot** | Ready to close, high engagement |
    | 60-79 | 🌡️ **Warm** | Qualified, needs nurturing |
    | 40-59 | ❄️ **Cool** | Early stage, more discovery needed |
    | 0-39 | 🧊 **Cold** | Low priority, long-term nurture |

    **Scoring Factors:**
    - Pipeline Stage (max 30 pts): Won=100, Negotiation=80, Proposal=60, etc.
    - Deal Value (max 30 pts): $100K+=30, $50K+=20, $10K+=10
    - Source (max 15 pts): Referral=15, Partner=15, Event=10, Website=5
    - Engagement (max 15 pts): Recent contact=10, Follow-up scheduled=5

    ### ⚡ Bulk Actions
    Select multiple leads with checkboxes to:
    - Change stage in bulk
    - Reassign to different team member
    - Export to CSV
    - Add to outreach campaign

    ### 📝 Lead Lifecycle Example
    ```
    New Lead Created (Score: 15)
        ↓ First Contact Made (Score: 25)
        ↓ Discovery Call (Score: 40) → Qualified
        ↓ Proposal Sent (Score: 60)
        ↓ Negotiation (Score: 80) → Hot
        ↓ Closed Won (Score: 100) 🎉
    ```
    """)


def render_pipeline_help():
    """Pipeline & Deals guide."""

    st.subheader("📊 Pipeline Management")

    st.markdown("""
    The Pipeline page gives you a visual funnel view of all active deals.

    ### 🔄 Default Pipeline Stages
    | Stage | Description | Typical Duration | Probability |
    |-------|-------------|------------------|-------------|
    | **New** | Fresh lead, no contact yet | 1-2 days | 10% |
    | **Contacted** | Initial outreach made | 3-5 days | 20% |
    | **Qualified** | Budget, authority, need confirmed | 1-2 weeks | 40% |
    | **Proposal** | Formal quote/proposal sent | 1-3 weeks | 60% |
    | **Negotiation** | Terms discussion, objections | 1-2 weeks | 80% |
    | **Closed Won** | Contract signed 🎉 | — | 100% |
    | **Closed Lost** | Deal dead, reason logged | — | 0% |

    ### 📈 Funnel Chart Interpretation
    - **Width** = Total deal value at that stage
    - **Count** = Number of deals
    - **Conversion** = Percentage moving to next stage
    - **Bottlenecks** = Stages with low conversion or high aging

    ### ⏳ Pipeline Aging (Critical Metric)
    Deals that stay too long in one stage risk going cold:
    - 🟢 **Low Risk**: < 14 days in stage
    - 🟡 **Medium Risk**: 14-30 days
    - 🔴 **High Risk**: > 30 days — **Action Required!**

    **Best Practices:**
    - Review aging weekly in Analytics → Pipeline Aging chart
    - Set follow-up tasks for every stage transition
    - Move stale deals to "Closed Lost" with reason to keep pipeline clean

    ### 💰 Pipeline Value Calculation
    ```
    Pipeline Value = Sum of all deals NOT in Closed Won/Lost
    Weighted Pipeline = Sum(Value × Stage Probability)
    ```

    ### 🎯 Stage Management Tips
    1. **Advance stages promptly** — Don't let deals stagnate
    2. **Log every interaction** — Activities auto-update `updated_at`
    3. **Use "Closed Lost" reasons** — Enables loss analysis in Analytics
    4. **Customize stages** — Settings → Pipeline Stages to match your process
    """)


def render_outreach_help():
    """Outreach & Campaigns guide."""

    st.subheader("📧 Outreach & Campaigns")

    st.markdown("""
    Automate and track all your prospect communication.

    ### ✉️ Email Templates
    Create reusable templates with dynamic variables:

    **Available Variables:**
    - `{name}` → Lead's full name
    - `{company}` → Company name
    - `{email}` → Lead's email
    - `{value}` → Deal value (formatted)
    - `{stage}` → Current pipeline stage

    **Example Template:**
    ```
    Subject: Quick question for {company}

    Hi {name},

    I noticed {company} is growing rapidly. I'd love to share
    how we helped similar companies increase revenue by 23%.

    Worth a 15-min call this week?

    Best,
    [Your Name]
    ```

    ### 📧 Campaign Builder
    1. **Create Campaign** — Name, subject, template, recipient list
    2. **Select Recipients** — Filter by stage, source, assignee, or manual select
    3. **Schedule or Send Now** — Immediate or future date/time
    4. **Track Results** — Opens, clicks, replies, bounces

    ### 📋 Activity Logging
    Every interaction should be logged:

    | Activity Type | When to Use | Auto-updates |
    |---------------|-------------|--------------|
    | **Email Sent** | Any outbound email | Lead `updated_at`, last_contacted |
    | **Call** | Phone conversations | Lead `updated_at`, last_contacted |
    | **Meeting** | Demos, discovery, negotiations | Lead `updated_at`, last_contacted |
    | **Note** | Internal context | Lead `updated_at` only |

    ### 🔄 Outreach Sequences (Best Practice)
    ```
    Day 1:  Initial Email (Template: "Introduction")
    Day 3:  Follow-up Email (Template: "Value Add")
    Day 7:  LinkedIn Connection + Message
    Day 10: Call Attempt + Voicemail
    Day 14: Breakup Email (Template: "Permission to Close")
    ```

    ### 📊 Campaign Analytics
    Track in Analytics → Campaign Performance:
    - **Sent** → **Delivered** → **Opened** → **Clicked** → **Replied**
    - Benchmark: 20%+ open rate, 3%+ click rate, 5%+ reply rate
    """)


def render_analytics_help():
    """Analytics & Reports guide."""

    st.subheader("📈 Analytics & Reports")

    st.markdown("""
    Data-driven insights to optimize your sales process.

    ### 📊 Dashboard Overview (Executive Summary)
    **Top Row KPIs:**
    - **Total Leads** — All-time count with period-over-period change
    - **Active Deals** — Currently in pipeline (not Won/Lost)
    - **Pipeline Value** — Sum of all active deal values
    - **Won This Month** — Revenue closed in current month
    - **Conversion Rate** — Won / (Won + Lost) × 100

    **Charts:**
    - **Pipeline Funnel** — Visual stage conversion
    - **Revenue Trend** — Monthly closed revenue over time

    ### 📋 Detailed Analytics Tabs

    #### 1. Lead Metrics
    - Leads by Source (bar chart)
    - Conversion Funnel (stage-by-stage)
    - Lead Velocity (new leads per week)

    #### 2. Revenue & Activity
    - Revenue Trend (monthly line chart)
    - Activity Heatmap (day × hour matrix)
    - Team Performance (revenue by assignee)

    #### 3. Pipeline Health
    - Pipeline Aging (days in current stage)
    - Lead Score Distribution (histogram with Hot/Warm/Cool/Cold thresholds)

    ### 🔍 Key Metrics to Monitor Weekly

    | Metric | Target | Action if Below |
    |--------|--------|-----------------|
    | **New Leads/Week** | > 10 | Increase prospecting |
    | **Conversion Rate** | > 20% | Improve qualification |
    | **Avg Days in Stage** | < 14 | Review stuck deals |
    | **Pipeline Coverage** | 3× Quota | Add more deals |
    | **Activity/Lead** | > 5/week | Increase outreach |

    ### 📤 Exporting Reports
    - Click **Export Report** on any Analytics page
    - Formats: CSV (data), PDF (charts + summary)
    - Schedule automated weekly emails in Settings

    ### 🎯 Conversion by Source Analysis
    Identify your best channels:
    ```
    Referral:     45% conversion ← Invest more here
    Website:      22% conversion
    Events:       18% conversion
    Cold Call:    8% conversion  ← Needs improvement
    ```
    """)


def render_settings_help():
    """Settings & Tips guide."""

    st.subheader("⚙️ Settings & Advanced Tips")

    st.markdown("""
    Configure the app to match your workflow.

    ### 👤 User Profile
    - **Name & Role** — Appears in activity logs and assignments
    - **Avatar** — Auto-generated from name (DiceBear)
    - **Timezone** — Affects date/time displays and scheduling

    ### 🔗 Pipeline Configuration
    - **Custom Stages** — Add/remove/reorder stages to match your sales process
    - **Stage Probabilities** — Set win probability % per stage for weighted pipeline
    - **Default Values** — Set default stage, source, assignee for new leads

    ### 📧 Email Integration
    - **SMTP Settings** — Connect Gmail, Outlook, or custom SMTP
    - **Signature** — Auto-append to all sent emails
    - **Tracking** — Enable open/click tracking pixels

    ### 📊 Data Management
    | Action | Description |
    |--------|-------------|
    | **Export All Data** | Download complete JSON backup |
    | **Import Leads** | CSV upload with column mapping |
    | **Clear Sample Data** | Reset to empty state |
    | **Backup Schedule** | Auto-backup to local folder |

    ### 🔐 Privacy & Security
    - All data stored locally in `sales-pipeline/data/` as JSON files
    - No cloud sync unless you configure it
    - API keys stored in session only (not persisted)

    ### 💡 Power User Tips

    #### 1. **Keyboard-Driven Workflow**
    ```
    N → New Lead
    / → Search
    1-6 → Jump to Dashboard/Leads/Pipeline/Outreach/Analytics/Settings
    Escape → Close any modal
    ```

    #### 2. **Weekly Review Routine (15 mins)**
    1. Dashboard → Check KPI trends
    2. Analytics → Pipeline Aging → Action on 🔴 High Risk
    3. Leads → Filter "No Activity > 7 days" → Log follow-ups
    4. Analytics → Conversion by Source → Adjust prospecting mix

    #### 3. **Team Collaboration**
    - Assign leads to specific reps
    - Use @mentions in Notes for handoffs
    - Filter Analytics by assignee for 1:1 coaching

    #### 4. **Data Hygiene Habits**
    - **Daily**: Log all activities, update next_followup dates
    - **Weekly**: Review and close stale deals, update stages
    - **Monthly**: Export backup, analyze source performance
    - **Quarterly**: Clean duplicate leads, archive old campaigns

    ### 🐛 Troubleshooting

    | Issue | Solution |
    |-------|----------|
    | Data not saving | Check `sales-pipeline/data/` folder permissions |
    | Charts not loading | Refresh page, check browser console |
    | Import fails | Verify CSV headers match template |
    | Slow with 1000+ leads | Use filters, consider archiving old leads |

    ### 📞 Getting Help
    - **In-App**: This Help page (always accessible from sidebar)
    - **Documentation**: Check README.md in project root
    - **Issues**: Report bugs via GitHub Issues
    """)

    # Quick Reference Card
    st.divider()
    st.subheader("📋 Quick Reference Card")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        **Pipeline Stages & Probabilities**
        - New (10%)
        - Contacted (20%)
        - Qualified (40%)
        - Proposal (60%)
        - Negotiation (80%)
        - Closed Won (100%)
        - Closed Lost (0%)
        """)

        st.markdown("""
        **Lead Score Thresholds**
        - 🔥 Hot: 80-100
        - 🌡️ Warm: 60-79
        - ❄️ Cool: 40-59
        - 🧊 Cold: 0-39
        """)

    with col2:
        st.markdown("""
        **Source Quality Ranking**
        1. Referral (15 pts)
        2. Partner (15 pts)
        3. Event (10 pts)
        4. Website (5 pts)
        5. Email Campaign (5 pts)
        6. Social Media (5 pts)
        7. Cold Call (0 pts)
        """)

        st.markdown("""
        **Activity Types**
        - 📧 Email Sent
        - 📞 Call
        - 🤝 Meeting
        - 📝 Note
        """)

    st.info("💡 **Tip**: Bookmark this page! Press `Ctrl/Cmd + /` anytime to return here.")


if __name__ == "__main__":
    render_help_tab()