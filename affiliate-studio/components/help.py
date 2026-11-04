"""
Help & Documentation component for Affiliate Studio.
Comprehensive guide on all features and how to use them for Instagram affiliate marketing.
"""

import streamlit as st


def render_help_tab():
    """Render the Help & Documentation page."""

    st.header("📚 Help & Documentation")
    st.caption("Complete guide to using Affiliate Studio for @jp.finds.deals")

    # Create tabs for different help sections
    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
        "🚀 Getting Started",
        "📦 Product Manager",
        "✍️ Content Studio",
        "✅ Approval Queue",
        "📊 Analytics",
        "🔄 Workflows",
        "⚙️ Settings & Tips"
    ])

    # ========== TAB 1: GETTING STARTED ==========
    with tab1:
        render_getting_started()

    # ========== TAB 2: PRODUCT MANAGER ==========
    with tab2:
        render_product_manager_help()

    # ========== TAB 3: CONTENT STUDIO ==========
    with tab3:
        render_content_studio_help()

    # ========== TAB 4: APPROVAL QUEUE ==========
    with tab4:
        render_approval_queue_help()

    # ========== TAB 5: ANALYTICS ==========
    with tab5:
        render_analytics_help()

    # ========== TAB 6: WORKFLOWS ==========
    with tab6:
        render_workflows_help()

    # ========== TAB 7: SETTINGS ==========
    with tab7:
        render_settings_help()


def render_getting_started():
    """Getting Started guide."""

    st.subheader("🚀 Welcome to Affiliate Studio")

    st.markdown("""
    **Affiliate Studio** is an AI-powered Instagram affiliate marketing automation system for **@jp.finds.deals**.
    It streamlines the entire workflow from product discovery to published content with AI-generated scripts,
    SEO captions, video prompts, and approval workflows.

    ### 🎯 Key Features at a Glance
    | Feature | Description |
    |---------|-------------|
    | **Dashboard** | Real-time overview of products, pending approvals, and performance |
    | **Product Manager** | Add, score, and manage affiliate products from Amazon/Flipkart |
    | **Content Studio** | AI generates Reel scripts, captions, hashtags, video prompts in 3 languages |
    | **Approval Queue** | Review, approve/reject content before publishing |
    | **Analytics** | Track views, engagement, clicks, conversions, and commissions |
    | **Workflows** | n8n integration for automated scheduling and publishing |
    | **Settings** | API keys, publishing schedule, brand configuration |

    ### 🏁 Quick Start Checklist
    1. **Configure API Keys** — Settings → Add Gemini API, Instagram, Amazon Associate, Flipkart
    2. **Add Your First Product** — Product Manager → Paste Amazon/Flipkart URL → Auto-extract details
    3. **Generate Content** — Content Studio → Select product → Choose Reel/Story/Carousel → Generate
    4. **Review & Approve** — Approval Queue → Review AI content → Approve or request changes
    5. **Publish & Track** — Workflows → Schedule or auto-publish → Analytics for performance

    ### 💡 Pro Tips for New Users
    - **Product Scoring**: Every product gets 0-100 score (discount, rating, price, category, features, affiliate link)
    - **Multi-Language**: Generate content in English, Tamil, or English+Tamil (Tanglish) simultaneously
    - **Video Prompts**: Export prompts for Google Flow, FFmpeg, or Canva templates
    - **Hashtags**: Auto-generated with marketplace, category, price, and brand tags (max 30 for Instagram)
    - **Data Persistence**: All data saved locally as JSON — no database needed

    ### 🔄 Typical Daily Workflow
    ```
    Morning → Check Dashboard → Review Pending Approvals
    → Product Manager → Add 3-5 new trending products
    → Content Studio → Generate Reels + Stories for top products
    → Approval Queue → Review, tweak, approve
    → Workflows → Schedule for 12:00 & 19:00 IST
    → Evening → Analytics → Check engagement, commissions
    ```
    """)

    with st.expander("📖 Understanding the UI Layout"):
        st.markdown("""
        **Header Bar**: Shows @jp.finds.deals branding, product count, pending approvals

        **Sidebar Navigation**:
        - 🏠 **Dashboard** — Executive overview with product pipeline, recent activity, quick stats
        - 📦 **Product Manager** — Product database with scoring, filtering, bulk actions
        - ✍️ **Content Studio** — AI content generation with 4 content types, 3 languages, 6 hook styles
        - ✅ **Approval Queue** — Content review workflow (Pending → Approved → Published/Rejected)
        - 📊 **Analytics** — Performance dashboards, conversion funnels, category breakdowns
        - 🔄 **Workflows** — n8n integration, automation status, scheduling
        - ⚙️ **Settings** — All API keys, publishing schedule, brand config, export/import

        **Quick Actions** (Sidebar): One-click to add product, generate content, publish approved
        """)

    with st.expander("⌨️ Keyboard Shortcuts"):
        st.markdown("""
        | Shortcut | Action |
        |----------|--------|
        `Ctrl/Cmd + N` | New Product |
        `Ctrl/Cmd + G` | Generate Content |
        `Ctrl/Cmd + /` | Show this Help |
        `Esc` | Close Modal |
        `Enter` | Submit Form |
        """)


def render_product_manager_help():
    """Product Manager guide."""

    st.subheader("📦 Product Manager")

    st.markdown("""
    Central hub for managing all affiliate products from discovery to publication.

    ### ➕ Adding Products
    **Method 1: URL Paste (Recommended)**
    1. Copy Amazon.in or Flipkart.com product URL
    2. Click **Add Product** → Paste URL
    3. System auto-extracts: Product ID, Title, Price, Images, Rating, Reviews
    4. Review and add missing details (category, features, affiliate link)

    **Method 2: Manual Entry**
    - Fill all fields manually for custom products or other marketplaces

    ### 🔗 Supported Marketplaces
    | Marketplace | URL Pattern | Affiliate Format |
    |-------------|-------------|------------------|
    | **Amazon.in** | `amazon.in/dp/ASIN` | `amazon.in/dp/ASIN?tag=YOUR_TAG` |
    | **Flipkart** | `flipkart.com/p/PID` | `dl.flipkart.com/dl/PID` |
    | **Myntra** | `myntra.com/product/ID` | Manual |
    | **Nykaa** | `nykaa.com/product/ID` | Manual |
    | **Meesho** | `meesho.com/product/ID` | Manual |

    ### 🎯 Product Scoring Algorithm (0-100)
    Products are automatically scored on 6 factors:

    | Factor | Weight | Max Points | Details |
    |--------|--------|------------|---------|
    | **Discount %** | High | 30 | ≥50% = 30, 30-49% = 20, 15-29% = 10, >0 = 5 |
    | **Rating + Reviews** | High | 20 | ≥4.5 & 1000+ = 20, ≥4.0 & 500+ = 15, ≥4.0 = 10, ≥3.5 = 5 |
    | **Price Attractiveness** | Medium | 15 | ≤₹500 = 15, ≤₹1000 = 12, ≤₹2000 = 8, ≤₹5000 = 5 |
    | **Category Relevance** | Medium | 15 | Trending (Electronics, Mobile) = 15, Home/Beauty = 10, Other = 5 |
    | **Features Richness** | Low | 10 | 5+ features = 10, 3-4 = 7, 1-2 = 3 |
    | **Affiliate Link** | Low | 10 | Has valid link = 10, Missing = 0 |

    **Score Labels:**
    - 🔥 **Hot** (80-100): Prioritize for content creation
    - 🌡️ **Warm** (60-79): Good candidates
    - ❄️ **Cool** (40-59): Needs improvement
    - 🧊 **Cold** (0-39): Low priority

    ### 📋 Product Status Lifecycle
    ```
    Discovered → Analyzed → Content Generated → Video Ready → Approved → Published
                                              ↓
                                          Rejected (at any stage)
    ```

    ### 🔍 Filtering & Search
    - **Search**: Product name, marketplace, category
    - **Status Filter**: All 7 lifecycle stages
    - **Marketplace**: Amazon, Flipkart, Myntra, Nykaa, Meesho
    - **Score Range**: Slider for Hot/Warm/Cool/Cold
    - **Date Range**: Discovery date filter

    ### ⚡ Bulk Actions
    Select multiple products to:
    - Recalculate scores
    - Generate content in batch
    - Export to CSV/JSON
    - Update status in bulk
    - Delete selected

    ### 💰 Indian Currency Formatting
    All prices displayed in Indian format:
    - ₹500 → `₹500`
    - ₹5,000 → `₹5.0K`
    - ₹1,50,000 → `₹1.50 L` (Lakh)
    - ₹1,50,00,000 → `₹1.50 Cr` (Crore)
    """)


def render_content_studio_help():
    """Content Studio guide."""

    st.subheader("✍️ Content Studio")

    st.markdown("""
    AI-powered content generation for Instagram Reels, Stories, Carousels, and Roundups.

    ### 🎬 Content Types
    | Type | Duration | Best For | Scenes |
    |------|----------|----------|--------|
    | **Instagram Reel** | 15-30s | Product demos, viral reach | 4 (Hook, Intro, Benefits, CTA) |
    | **Instagram Story** | 5-15s | Quick deals, swipe-up links | 3 (Hook, Product, CTA) |
    | **Carousel Post** | Static | Multi-product, comparisons | 5-10 slides |
    | **Weekly Roundup** | 30-60s | Top 5-10 deals of the week | 6+ scenes |

    ### 🌍 Language Options
    Generate all 3 simultaneously:
    1. **English** — Natural Indian English with Hinglish touches
    2. **Tamil** — Pure Tamil script for Tamil audience
    3. **English + Tamil (Mixed)** — Tanglish for broader reach

    ### 🎭 Hook Styles (Choose One)
    | Style | Best For | Example |
    |-------|----------|---------|
    | **Curiosity** | Mystery products | "You won't believe what this ₹299 gadget does..." |
    | **Problem/Solution** | Pain-point products | "Tired of tangled cables? This ₹199 fix..." |
    | **Budget Saving** | High discount | "Save ₹3000 on this premium headphone..." |
    | **Visual Demo** | Visual products | "Watch this phone case survive a 10ft drop..." |
    | **Shocking Fact** | Stats-driven | "90% of people overpay for this — here's why..." |
    | **Relatable Story** | Lifestyle products | "My mom called me crazy for buying this, but..." |

    ### 🎭 Tone Options
    | Tone | Vibe | Use Case |
    |------|------|----------|
    | **Friendly & Casual** | Conversational | Daily deals, relatable |
    | **Expert & Authoritative** | Trustworthy | Tech, high-value |
    | **Excited & Energetic** | Hype-building | Flash sales, limited stock |
    | **Trustworthy & Honest** | Transparent | Reviews, comparisons |
    | **Fun & Playful** | Light-hearted | Lifestyle, accessories |

    ### 📝 Generated Content Structure

    #### For Reels (4-Scene Script):
    ```json
    {
      "scripts": {
        "English": {
          "hook": "0-3s: Visual + verbal hook",
          "introduction": "3-8s: Product reveal + price",
          "benefits": "8-22s: 3 key benefits demo",
          "cta": "22-30s: Link in bio + urgency"
        },
        "Tamil": { ... },
        "English + Tamil (Mixed)": { ... }
      },
      "seo": {
        "caption": "Engaging caption with emojis",
        "hashtags": ["#tag1", "#tag2", ...],
        "product_title": "SEO-optimized title",
        "cta": "Call to action",
        "disclosure": "#ad #affiliate"
      },
      "video_prompts": {
        "hook_visual": "AI video generation prompt",
        "product_intro": "AI video generation prompt",
        "benefits_demo": "AI video generation prompt",
        "cta_visual": "AI video generation prompt",
        "duration": 25,
        "resolution": "1080x1920",
        "format": "MP4"
      }
    }
    ```

    ### 🏷️ Hashtag Generation (Auto, Max 30)
    **Auto-included:**
    - Marketplace: `#amazonfinds`, `#amazondeals`, `#flipkartdeals`
    - Category: `#electronics`, `#gadgets`, `#homekitchen`, `#beauty`
    - Price: `#under500`, `#under1000`, `#under2000`
    - Discount: `#50off`, `#30off`
    - Brand: `#jpfindsdeals`, `#discountdeals`, `#smartshopping`, `#indianshopping`

    ### 🎨 Canva Template Recommendations
    Based on content type, system suggests:
    - **Product Promotion** — Single product focus
    - **Today's Best Deals** — Daily deal highlight
    - **Top 5 Gadgets** — Multi-product carousel
    - **Budget Shopping Finds** — Under ₹500/₹1000
    - **Product Comparison** — Side-by-side
    - **Festival Deals** — Seasonal campaigns

    ### 📤 Export Options
    - **Canva JSON** — Import into Canva for design
    - **Google Flow JSON** — 4-scene video generation prompts
    - **FFmpeg Script** — Command-line video assembly
    - **Raw JSON** — Full content for custom workflows
    """)


def render_approval_queue_help():
    """Approval Queue guide."""

    st.subheader("✅ Approval Queue")

    st.markdown("""
    Review and quality-control all AI-generated content before publishing.

    ### 🔄 Approval Workflow States
    | Status | Meaning | Actions Available |
    |--------|---------|-------------------|
    | **Pending** | Awaiting review | Approve, Reject, View Details |
    | **Approved** | Ready to publish | Publish Now, Schedule, Send Back |
    | **Published** | Live on Instagram | View Metrics, Archive |
    | **Rejected** | Needs revision | Restore to Pending, Delete |
    | **Scheduled** | Queued for auto-publish | Cancel Schedule, Reschedule |

    ### 👀 Review Checklist
    Before approving, verify:
    - [ ] **Hook** grabs attention in first 3 seconds
    - [ ] **Price/Discount** accurate and current
    - [ ] **Affiliate Link** works and tracked
    - [ ] **Disclosure** includes `#ad #affiliate`
    - [ ] **Language** matches target audience
    - [ ] **Hashtags** relevant and under 30
    - [ ] **Video Prompts** feasible for production
    - [ ] **Brand Voice** consistent with @jp.finds.deals

    ### ⚡ Quick Actions
    - **Approve** → Moves to Approved, ready for publishing
    - **Reject** → Opens feedback modal, returns to Content Studio
    - **Edit** → Opens Content Studio with pre-filled content for tweaks
    - **Preview** → Full-screen view of formatted caption + hashtags
    - **Bulk Approve** → Select multiple → Approve all

    ### 📝 Giving Feedback on Rejection
    When rejecting, provide specific feedback:
    ```
    ✅ Good: "Hook is weak - change to Problem/Solution style, mention ₹299 price upfront"
    ❌ Bad: "Don't like it"
    ```

    ### 📅 Scheduling Approved Content
    From Approved tab:
    1. Click **Schedule** on individual item
    2. Choose date/time (respects IST timezone)
    3. Or use **Bulk Schedule** for multiple items
    4. Scheduled items move to **Scheduled** tab
    5. n8n workflow picks up at scheduled time

    ### 🔍 Filtering & Search
    - **Status Tabs**: Pending / Approved / Published / Rejected / Scheduled
    - **Content Type**: Reel, Story, Carousel, Roundup
    - **Language**: English, Tamil, Mixed
    - **Date Range**: Created, Approved, Published
    - **Product**: Search by product name
    """)


def render_analytics_help():
    """Analytics guide."""

    st.subheader("📊 Analytics & Performance")

    st.markdown("""
    Track, analyze, and optimize your affiliate marketing performance.

    ### 📈 Dashboard Overview (Executive Summary)
    **Top Row KPIs:**
    - **Total Products** — All-time count with status breakdown
    - **Published Posts** — Live content count
    - **Total Views** — Aggregate reach
    - **Total Commission** — Earnings estimate
    - **Avg Engagement Rate** — (Likes + Comments + Shares + Saves) / Views × 100

    ### 📋 Detailed Analytics Sections

    #### 1. Content Performance
    - **Engagement Rate by Content Type** — Reel vs Story vs Carousel vs Roundup
    - **Top Performing Posts** — Sortable by views, engagement, clicks, conversions
    - **Posting Frequency** — Posts per week trend

    #### 2. Conversion Funnel
    ```
    Views → Clicks → Conversions → Commission
    100%     5%        1%           ₹X
    ```
    - **CTR** (Click-Through Rate) = Clicks / Views × 100
    - **Conversion Rate** = Conversions / Clicks × 100
    - **Revenue Per View** = Commission / Views

    #### 3. Category Performance
    | Category | Posts | Views | Engagement | CTR | Conv. Rate | Commission |
    |----------|-------|-------|------------|-----|------------|------------|
    | Electronics | 15 | 50K | 4.2% | 3.1% | 2.5% | ₹12,500 |
    | Home & Kitchen | 10 | 30K | 3.8% | 2.5% | 3.0% | ₹8,200 |

    #### 4. Marketplace Comparison
    - Amazon vs Flipkart vs Others
    - Commission rates, conversion rates, avg order value

    #### 5. Language Performance
    - English vs Tamil vs Mixed engagement comparison
    - Audience demographic insights

    #### 6. Time-Based Analysis
    - **Best Posting Times** — Heatmap of engagement by hour/day
    - **Day of Week** — Which days perform best
    - **Monthly Trends** — Growth over time

    ### 🎯 Key Metrics to Monitor Weekly

    | Metric | Target | Action if Below |
    |--------|--------|-----------------|
    | **Posts/Week** | ≥ 7 (1 Reel/day) | Increase content generation |
    | **Engagement Rate** | > 3% | Improve hooks, visuals |
    | **CTR** | > 2% | Better CTAs, link placement |
    | **Conversion Rate** | > 2% | Review product selection |
    | **Commission/Week** | Growing | Scale winning categories |

    ### 📤 Export & Reporting
    - **Weekly Report** — Auto-generated every Monday
    - **Monthly Deep-Dive** — Category, marketplace, language breakdowns
    - **Custom Date Range** — CSV export for spreadsheet analysis
    - **n8n Integration** — Push metrics to external dashboards
    """)


def render_workflows_help():
    """Workflows & Automation guide."""

    st.subheader("🔄 Workflows & n8n Integration")

    st.markdown("""
    Automate content scheduling, publishing, and cross-platform distribution.

    ### 🤖 n8n Community Edition Workflows
    Affiliate Studio includes 8 pre-built n8n workflows:

    | Workflow | Trigger | Actions |
    |----------|---------|---------|
    | **Daily Product Discovery** | Cron (6 AM) | Scrape deals → Score → Add to Product Manager |
    | **Content Generation** | Webhook (new product) | Call Gemini → Create drafts → Queue for approval |
    | **Auto-Approval** | Cron (10 AM) | Auto-approve Hot score > 85 content |
    | **Scheduled Publishing** | Cron (12 PM, 7 PM) | Publish approved → Instagram Graph API → Log metrics |
    | **Story Sequence** | Cron (9 AM, 2 PM, 9 PM) | Post Stories → Add link stickers → Track swipe-ups |
    | **Weekly Roundup** | Cron (Sunday 10 AM) | Compile top 10 → Generate carousel → Schedule |
    | **Metrics Collection** | Cron (Hourly) | Fetch Instagram Insights → Update Analytics |
    | **Commission Tracking** | Webhook (sale) | Parse affiliate reports → Update product commissions |

    ### 🔧 n8n Setup
    1. **Install n8n**: `npm install n8n -g` or Docker
    2. **Import Workflows**: Settings → Workflows → Import JSON
    3. **Configure Credentials**: Instagram Graph API, Gemini, Amazon, Flipkart
    4. **Activate Workflows**: Toggle active in n8n dashboard
    5. **Test**: Manual trigger each workflow once

    ### 📅 Publishing Schedule
    Configure in Settings:
    - **Reel Slots**: 12:00 IST, 19:00 IST (prime time)
    - **Story Slots**: 09:00, 14:00, 21:00 IST
    - **Timezone**: Asia/Kolkata (IST)
    - **Auto-Publish**: Toggle for hands-free operation

    ### 🔗 Instagram Graph API Setup
    1. **Meta Developer Account** → Create App → Instagram Business
    2. **App ID & Secret** → Settings → Instagram
    3. **Access Token** → Long-lived token (60 days)
    4. **Business Account ID** → From Meta Business Suite
    5. **Permissions**: `instagram_content_publish`, `instagram_manage_insights`

    ### 🎬 Video Generation Pipeline
    For automated video creation:
    1. **Google Flow** (Recommended) — Import Flow JSON from Content Studio
    2. **FFmpeg** — Run generated script for programmatic assembly
    3. **Manual** — Use Canva templates with exported assets

    ### ⚙️ Workflow Monitoring
    In Workflows tab:
    - **Status**: Active/Inactive/Error
    - **Last Run**: Timestamp + success/failure
    - **Next Run**: Scheduled time
    - **Logs**: Expand for detailed execution log
    - **Manual Trigger**: Run any workflow on-demand

    ### 🔒 Security Notes
    - Store API keys in n8n credentials (encrypted)
    - Never commit credentials to git
    - Rotate tokens every 60 days
    - Use webhook secrets for n8n ↔ Studio communication
    """)


def render_settings_help():
    """Settings & Advanced Tips guide."""

    st.subheader("⚙️ Settings & Advanced Tips")

    st.markdown("""
    Configure all integrations and customize for your workflow.

    ### 🔑 Required API Keys (Priority Order)

    | Key | Source | Purpose | Required |
    |-----|--------|---------|----------|
    | **Gemini API** | Google AI Studio | Content generation | ✅ Yes |
    | **Instagram App ID** | Meta Developers | Publishing | ✅ Yes |
    | **Instagram App Secret** | Meta Developers | Auth | ✅ Yes |
    | **Instagram Access Token** | Meta Graph API | Posting + Insights | ✅ Yes |
    | **Instagram Business ID** | Meta Business Suite | Account targeting | ✅ Yes |
    | **Amazon Associate Tag** | Amazon Associates | Affiliate links | ✅ Yes |
    | **Amazon Access Key** | AWS IAM | PA-API (optional) | Optional |
    | **Amazon Secret Key** | AWS IAM | PA-API (optional) | Optional |
    | **Flipkart Affiliate ID** | Flipkart Affiliate | Affiliate links | Optional |
    | **Flipkart Affiliate Token** | Flipkart Affiliate | Auth | Optional |
    | **Canva API Token** | Canva Developers | Template import | Optional |

    ### 📅 Publishing Configuration
    - **Reel Schedule**: 2x daily (12:00, 19:00 IST recommended)
    - **Story Schedule**: 3x daily (09:00, 14:00, 21:00 IST)
    - **Timezone**: Asia/Kolkata (change if different audience)
    - **Auto-Publish**: ON for hands-free, OFF for manual review

    ### 🌍 Language & Brand Settings
    - **Default Languages**: English, Tamil, English+Tamil
    - **Brand Name**: "JP Finds Deals"
    - **Watermark**: "@jp.finds.deals"
    - **Colors**: Primary `#FF6B35`, Secondary `#1A1A2E`
    - **Disclosure**: Default `#ad #affiliate` (FTC compliance)

    ### 📊 Data Management
    | Action | Description |
    |--------|-------------|
    | **Export All Data** | Complete JSON backup (products, drafts, approvals, posts, settings) |
    | **Import Data** | Restore from backup or migrate from another instance |
    | **Clear Sample Data** | Remove demo products/posts for fresh start |
    | **Reset Settings** | Factory defaults (keeps products/content) |

    ### 💡 Power User Tips

    #### 1. **Batch Content Generation**
    ```
    1. Product Manager → Filter "Hot" score products
    2. Select 5-10 → Bulk Generate Content
    3. Content Studio → Review all → Bulk Approve
    4. Workflows → Schedule full week in 10 minutes
    ```

    #### 2. **Category-Focused Days**
    ```
    Monday:    Electronics & Gadgets
    Tuesday:   Home & Kitchen
    Wednesday: Beauty & Skincare
    Thursday:  Fashion & Accessories
    Friday:    Budget Finds (< ₹500)
    Saturday:  Weekly Roundup
    Sunday:    Rest / Metrics Review
    ```

    #### 3. **A/B Testing Hooks**
    - Generate same product with 2 different hook styles
    - Publish at same time on different days
    - Compare engagement in Analytics → Optimize

    #### 4. **Seasonal Campaigns**
    - Pre-build festival templates (Diwali, Christmas, Sales)
    - Use "Festival Deals" Canva template
    - Schedule 2 weeks ahead for maximum reach

    ### 🐛 Troubleshooting

    | Issue | Solution |
    |-------|----------|
    | Gemini API error | Check API key, quota, billing enabled |
    | Instagram publish fails | Verify token not expired, permissions granted |
    | Product not scoring | Ensure all fields filled (price, rating, category) |
    | Hashtags > 30 | System auto-trims, check output |
    | Video prompts fail | Check Google Flow format, simplify prompts |
    | n8n workflow stuck | Check credentials, webhook URLs, logs |

    ### 📞 Getting Help
    - **In-App**: This Help page (always accessible from sidebar)
    - **Documentation**: Check README.md in project root
    - **n8n Docs**: docs.n8n.io for workflow troubleshooting
    - **Meta API**: developers.facebook.com/docs/instagram-api
    - **Gemini API**: ai.google.dev/docs

    ### 🔐 Privacy & Security
    - All data stored locally in `affiliate-studio/data/` as JSON
    - API keys in session state only (not persisted to disk)
    - Instagram tokens encrypted in n8n credentials
    - No data sent to third parties except configured APIs
    """)

    # Quick Reference Card
    st.divider()
    st.subheader("📋 Quick Reference Card")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        **Product Score Weights**
        - Discount %: 30 pts
        - Rating + Reviews: 20 pts
        - Price: 15 pts
        - Category: 15 pts
        - Features: 10 pts
        - Affiliate Link: 10 pts

        **Score Labels**
        - 🔥 Hot: 80-100
        - 🌡️ Warm: 60-79
        - ❄️ Cool: 40-59
        - 🧊 Cold: 0-39
        """)

        st.markdown("""
        **Content Types & Scenes**
        - Reel: 4 scenes (30s)
        - Story: 3 scenes (15s)
        - Carousel: 5-10 slides
        - Roundup: 6+ scenes (60s)
        """)

    with col2:
        st.markdown("""
        **Approval States**
        - Pending → Approved → Published
        - Pending → Rejected → Pending
        - Approved → Scheduled → Published
        """)

        st.markdown("""
        **Publishing Schedule (IST)**
        - Reels: 12:00, 19:00
        - Stories: 09:00, 14:00, 21:00
        - Timezone: Asia/Kolkata
        """)

        st.markdown("""
        **Languages**
        - English
        - Tamil
        - English + Tamil (Mixed)
        """)

    st.info("💡 **Tip**: Bookmark this page! Press `Ctrl/Cmd + /` anytime to return here.")


if __name__ == "__main__":
    render_help_tab()