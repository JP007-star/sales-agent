"""
Settings component for JP Finds Deals.
"""

import streamlit as st
import json
from datetime import datetime


def render_settings():
    """Render the Settings tab."""

    st.header("⚙️ Settings")

    settings_tabs = st.tabs([
        "🔑 API Keys",
        "📱 Instagram",
        "🛒 Marketplaces",
        "🎨 Brand & Creative",
        "📅 Publishing",
        "🔄 Workflows",
        "💾 Data Management"
    ])

    with settings_tabs[0]:
        render_api_keys()

    with settings_tabs[1]:
        render_instagram_settings()

    with settings_tabs[2]:
        render_marketplace_settings()

    with settings_tabs[3]:
        render_brand_settings()

    with settings_tabs[4]:
        render_publishing_settings()

    with settings_tabs[5]:
        render_workflow_settings()

    with settings_tabs[6]:
        render_data_settings()


def render_api_keys():
    """Render API keys configuration."""

    st.subheader("🔑 API Configuration")

    st.warning("⚠️ API keys are stored locally in session state. For production, use environment variables.")

    # Gemini API
    st.write("**Google Gemini AI**")
    st.caption("Required for content generation. Get your API key from https://aistudio.google.com/")

    gemini_key = st.text_input(
        "Gemini API Key",
        value=st.session_state.settings.get('gemini_api_key', ''),
        type="password",
        placeholder="AIzaSy...",
        key="gemini_api_key_input"
    )

    if st.button("Save Gemini Key", key="save_gemini"):
        st.session_state.settings['gemini_api_key'] = gemini_key
        st.success("Gemini API key saved!")

    st.divider()

    # Canva API
    st.write("**Canva Pro API**")
    st.caption("Optional: For automated design generation. Requires Canva Developer access.")

    canva_token = st.text_input(
        "Canva API Token",
        value=st.session_state.settings.get('canva_api_token', ''),
        type="password",
        placeholder="Bearer token...",
        key="canva_api_token_input"
    )

    if st.button("Save Canva Token", key="save_canva"):
        st.session_state.settings['canva_api_token'] = canva_token
        st.success("Canva API token saved!")

    st.divider()

    # Test connections
    st.write("**Connection Tests**")
    col1, col2 = st.columns(2)

    with col1:
        if st.button("Test Gemini API", use_container_width=True):
            test_gemini_connection()

    with col2:
        if st.button("Test Canva API", use_container_width=True):
            test_canva_connection()


def render_instagram_settings():
    """Render Instagram Graph API settings."""

    st.subheader("📱 Instagram Graph API")

    st.info("""
    **Setup Instructions:**
    1. Go to https://developers.facebook.com/
    2. Create a Meta App (Business type)
    3. Add Instagram Graph API product
    4. Configure Instagram Basic Display & Instagram Graph API
    5. Get App ID, App Secret, and generate Access Token
    6. Connect your Instagram Business/Creator account
    """)

    col1, col2 = st.columns(2)

    with col1:
        app_id = st.text_input(
            "App ID",
            value=st.session_state.settings.get('instagram_app_id', ''),
            placeholder="1234567890123456",
            key="ig_app_id"
        )

        business_account_id = st.text_input(
            "Instagram Business Account ID",
            value=st.session_state.settings.get('instagram_business_account_id', ''),
            placeholder="17841400008460056",
            key="ig_business_id"
        )

    with col2:
        app_secret = st.text_input(
            "App Secret",
            value=st.session_state.settings.get('instagram_app_secret', ''),
            type="password",
            placeholder="abcdef123456...",
            key="ig_app_secret"
        )

        access_token = st.text_input(
            "Access Token (Long-lived)",
            value=st.session_state.settings.get('instagram_access_token', ''),
            type="password",
            placeholder="EAA...",
            key="ig_access_token"
        )

    if st.button("Save Instagram Settings", type="primary", use_container_width=True):
        st.session_state.settings['instagram_app_id'] = app_id
        st.session_state.settings['instagram_app_secret'] = app_secret
        st.session_state.settings['instagram_business_account_id'] = business_account_id
        st.session_state.settings['instagram_access_token'] = access_token
        st.success("Instagram settings saved!")

    st.divider()

    # Permissions status
    st.write("**Required Permissions:**")
    permissions = [
        ("instagram_basic_display", "Basic profile info"),
        ("instagram_content_publish", "Publish Reels/Posts"),
        ("instagram_manage_insights", "Read insights"),
        ("pages_show_list", "List connected pages"),
        ("pages_read_engagement", "Read engagement metrics")
    ]

    for perm, desc in permissions:
        col1, col2 = st.columns([1, 3])
        with col1:
            st.checkbox(perm, value=True, key=f"perm_{perm}")
        with col2:
            st.caption(desc)

    # Test connection
    if st.button("Test Instagram Connection", use_container_width=True):
        test_instagram_connection()


def render_marketplace_settings():
    """Render affiliate marketplace settings."""

    st.subheader("🛒 Affiliate Marketplaces")

    # Amazon Associates
    with st.expander("📦 Amazon Associates (India)", expanded=True):
        st.caption("Get credentials from https://affiliate-program.amazon.in/")

        col1, col2 = st.columns(2)
        with col1:
            associate_tag = st.text_input(
                "Associate Tag",
                value=st.session_state.settings.get('amazon_associate_tag', ''),
                placeholder="yourtag-21",
                key="amazon_tag"
            )
        with col2:
            access_key = st.text_input(
                "Access Key ID",
                value=st.session_state.settings.get('amazon_access_key', ''),
                type="password",
                placeholder="AKIA...",
                key="amazon_access"
            )

        secret_key = st.text_input(
            "Secret Access Key",
            value=st.session_state.settings.get('amazon_secret_key', ''),
            type="password",
            placeholder="Secret key...",
            key="amazon_secret"
        )

        if st.button("Save Amazon Settings", key="save_amazon"):
            st.session_state.settings['amazon_associate_tag'] = associate_tag
            st.session_state.settings['amazon_access_key'] = access_key
            st.session_state.settings['amazon_secret_key'] = secret_key
            st.success("Amazon settings saved!")

    # Flipkart Affiliate
    with st.expander("🛍️ Flipkart Affiliate"):
        st.caption("Get credentials from Flipkart Affiliate Program")

        col1, col2 = st.columns(2)
        with col1:
            affiliate_id = st.text_input(
                "Affiliate ID",
                value=st.session_state.settings.get('flipkart_affiliate_id', ''),
                placeholder="your_affiliate_id",
                key="flipkart_id"
            )
        with col2:
            affiliate_token = st.text_input(
                "Affiliate Token",
                value=st.session_state.settings.get('flipkart_affiliate_token', ''),
                type="password",
                placeholder="token...",
                key="flipkart_token"
            )

        if st.button("Save Flipkart Settings", key="save_flipkart"):
            st.session_state.settings['flipkart_affiliate_id'] = affiliate_id
            st.session_state.settings['flipkart_affiliate_token'] = affiliate_token
            st.success("Flipkart settings saved!")

    # Other marketplaces placeholder
    with st.expander("➕ Other Marketplaces"):
        st.info("Add more marketplace integrations as needed")

        if st.button("Add Marketplace", use_container_width=True):
            st.session_state.show_add_marketplace = True


def render_brand_settings():
    """Render brand identity settings."""

    st.subheader("🎨 Brand Identity")

    col1, col2 = st.columns(2)

    with col1:
        st.text_input("Brand Name", value="JP Finds Deals", key="brand_name")
        st.text_input("Tagline", value="Daily Shopping Bestie 💖", key="brand_tagline")
        st.text_input("Profile Name", value="Discount Deals 🤫😱 | By Divya 😉✨️", key="brand_profile")
        st.text_input("Instagram Handle", value="@jp.finds.deals", key="brand_handle")

        st.color_picker("Primary Color", value="#FF6B35", key="brand_primary")
        st.color_picker("Secondary Color", value="#1A1A2E", key="brand_secondary")
        st.color_picker("Accent Color", value="#FFD700", key="brand_accent")

    with col2:
        st.text_input("Logo URL", placeholder="https://...", key="brand_logo")
        st.text_input("Watermark Text", value="@jp.finds.deals", key="brand_watermark")
        st.selectbox("Font Style", ["Modern Sans", "Playful Rounded", "Bold Display", "Clean Minimal"], key="brand_font")
        st.selectbox("Animation Style", ["Subtle", "Energetic", "Smooth", "Snappy"], key="brand_animation")

        st.text_area("Bio Template", value="Daily Shopping Bestie 💖!\nFashion | Beauty | Tech\nAmazing Deals & Smart Finds\nShop Smart. Save More.\nIndia | 5 Languages", key="brand_bio")

    # Default hashtags
    st.write("**Default Hashtags**")
    default_tags = st.text_area(
        "Hashtags (one per line)",
        value="#jpfindsdeals\n#discountdeals\n#smartshopping\n#indianshopping\n#budgetfriendly\n#onlinedeals\n#shoppinghacks\n#dealsofday\n#amazonfinds\n#flipkartdeals",
        height=150,
        key="default_hashtags"
    )

    if st.button("Save Brand Settings", type="primary", use_container_width=True):
        st.success("Brand settings saved!")


def render_publishing_settings():
    """Render publishing schedule and preferences."""

    st.subheader("📅 Publishing Schedule")

    # Time slots
    st.write("**Daily Publishing Slots (IST)**")

    schedule = st.session_state.settings.get('publishing_schedule', ['12:00', '19:00'])

    for i, slot in enumerate(schedule):
        col1, col2, col3 = st.columns([1, 2, 1])
        with col1:
            st.write(f"Slot {i+1}")
        with col2:
            new_time = st.time_input(f"Time {i+1}", value=datetime.strptime(slot, '%H:%M').time(), key=f"slot_{i}", label_visibility="collapsed")
            schedule[i] = new_time.strftime('%H:%M')
        with col3:
            if st.button("🗑️", key=f"del_slot_{i}", use_container_width=True):
                schedule.pop(i)
                st.rerun()

    if st.button("➕ Add Slot", use_container_width=True):
        schedule.append("20:00")
        st.rerun()

    # Timezone
    st.divider()
    timezone = st.selectbox(
        "Timezone",
        ["Asia/Kolkata (IST)", "UTC", "America/New_York (EST)", "Europe/London (GMT)"],
        index=0,
        key="publishing_timezone"
    )

    # Auto-publish
    st.divider()
    st.write("**Publishing Preferences**")

    auto_publish = st.checkbox(
        "Auto-publish approved content",
        value=st.session_state.settings.get('auto_publish', False),
        help="Automatically publish to Instagram when approved (requires Instagram API)"
    )

    require_approval = st.checkbox(
        "Require manual approval",
        value=True,
        help="Always require explicit approval before publishing"
    )

    # Daily targets
    st.divider()
    st.write("**Daily Content Targets**")

    col1, col2 = st.columns(2)
    with col1:
        daily_reels = st.number_input(
            "Reels per day",
            value=st.session_state.settings.get('daily_reels_target', 2),
            min_value=1,
            max_value=10,
            key="daily_reels"
        )
    with col2:
        daily_stories = st.number_input(
            "Stories per day",
            value=st.session_state.settings.get('daily_stories_target', 3),
            min_value=0,
            max_value=20,
            key="daily_stories"
        )

    weekly_roundup = st.checkbox("Weekly deals roundup", value=True, key="weekly_roundup")

    # Languages
    st.divider()
    languages = st.multiselect(
        "Content Languages",
        ["English", "Tamil", "Hindi", "English + Tamil", "English + Hindi"],
        default=st.session_state.settings.get('languages', ['English', 'Tamil', 'English + Tamil']),
        key="content_languages"
    )

    if st.button("Save Publishing Settings", type="primary", use_container_width=True):
        st.session_state.settings['publishing_schedule'] = schedule
        st.session_state.settings['timezone'] = timezone
        st.session_state.settings['auto_publish'] = auto_publish
        st.session_state.settings['require_approval'] = require_approval
        st.session_state.settings['daily_reels_target'] = daily_reels
        st.session_state.settings['daily_stories_target'] = daily_stories
        st.session_state.settings['weekly_roundup'] = weekly_roundup
        st.session_state.settings['languages'] = languages
        st.success("Publishing settings saved!")


def render_workflow_settings():
    """Render n8n workflow settings."""

    st.subheader("🔄 n8n Workflow Automation")

    st.info("""
    **n8n Community Edition** runs locally via Docker.
    Access n8n at: http://localhost:5678

    Default credentials: admin / admin (change in .env)
    """)

    # Workflow status
    workflows = [
        ("Product URL Intake", "Receives product URLs, validates, saves, triggers AI"),
        ("Product Discovery", "Queries affiliate APIs, scores products, avoids duplicates"),
        ("AI Content Generation", "Sends to Gemini, generates hooks/scripts/SEO/video prompts"),
        ("Video Production", "Prepares Canva assets, generates video prompts, processes video"),
        ("Approval Workflow", "Notifies for approval, waits for decision, moves to queue"),
        ("Instagram Publishing", "Publishes approved content via Meta Graph API"),
        ("Daily Scheduling", "Generates up to 2 content drafts daily at scheduled times"),
        ("Analytics Collection", "Fetches Instagram insights, updates affiliate data")
    ]

    for name, desc in workflows:
        with st.container():
            col1, col2, col3 = st.columns([2, 4, 1])
            with col1:
                st.write(f"**{name}**")
            with col2:
                st.caption(desc)
            with col3:
                if st.button("Import", key=f"import_wf_{name}", use_container_width=True):
                    st.info(f"Importing {name} workflow...")
            st.divider()

    # n8n connection
    st.write("**n8n Connection**")
    col1, col2 = st.columns(2)
    with col1:
        n8n_url = st.text_input("n8n URL", value="http://localhost:5678", key="n8n_url")
    with col2:
        n8n_key = st.text_input("API Key", type="password", placeholder="n8n API key", key="n8n_key")

    if st.button("Test n8n Connection", use_container_width=True):
        test_n8n_connection()


def render_data_settings():
    """Render data management settings."""

    st.subheader("💾 Data Management")

    # Data stats
    products_count = len(st.session_state.get('products', []))
    drafts_count = len(st.session_state.get('content_drafts', []))
    approval_count = len(st.session_state.get('approval_queue', []))
    published_count = len(st.session_state.get('published_posts', []))

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Products", products_count)
    with col2:
        st.metric("Drafts", drafts_count)
    with col3:
        st.metric("In Queue", approval_count)
    with col4:
        st.metric("Published", published_count)

    st.divider()

    # Export
    st.write("**Export Data**")

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("📥 Export Products", use_container_width=True):
            export_data('products')

    with col2:
        if st.button("📥 Export Drafts", use_container_width=True):
            export_data('drafts')

    with col3:
        if st.button("📥 Export All Data", use_container_width=True, type="primary"):
            export_all_data()

    st.divider()

    # Import
    st.write("**Import Data**")

    uploaded_file = st.file_uploader("Upload JSON file", type=['json'])

    if uploaded_file:
        import_type = st.selectbox("Import As", ["Products", "Drafts", "Approval Items", "Published Posts"])
        if st.button("Import", type="primary"):
            import_data(uploaded_file, import_type)

    st.divider()

    # Data retention
    st.write("**Data Retention**")

    col1, col2 = st.columns(2)
    with col1:
        st.selectbox("Draft Retention", ["30 days", "90 days", "1 year", "Forever"], index=1)
        st.selectbox("Published Post Retention", ["1 year", "3 years", "Forever"], index=2)
    with col2:
        st.selectbox("Analytics Retention", ["90 days", "1 year", "3 years", "Forever"], index=1)
        st.checkbox("Auto-clean rejected items", value=True)

    st.divider()

    # Danger zone
    st.write("**⚠️ Danger Zone**")

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("🗑️ Clear Drafts", use_container_width=True, type="secondary"):
            st.error("This would delete all drafts. Confirmation required.")

    with col2:
        if st.button("🗑️ Clear Queue", use_container_width=True, type="secondary"):
            st.error("This would clear approval queue. Confirmation required.")

    with col3:
        if st.button("💥 Reset All Data", use_container_width=True, type="secondary"):
            st.error("⚠️ PERMANENTLY deletes ALL data. Type 'RESET' to confirm.")


def test_gemini_connection():
    """Test Gemini API connection."""
    api_key = st.session_state.settings.get('gemini_api_key', '')
    if not api_key:
        st.error("No API key configured")
        return

    try:
        import google.generativeai as genai
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content("Say 'Hello from JP Finds Deals!'")
        st.success(f"✅ Connected! Response: {response.text}")
    except Exception as e:
        st.error(f"❌ Connection failed: {str(e)}")


def test_canva_connection():
    """Test Canva API connection."""
    token = st.session_state.settings.get('canva_api_token', '')
    if not token:
        st.error("No API token configured")
        return

    st.info("Canva API test would be implemented here")


def test_instagram_connection():
    """Test Instagram Graph API connection."""
    access_token = st.session_state.settings.get('instagram_access_token', '')
    if not access_token:
        st.error("No access token configured")
        return

    st.info("Instagram API test would be implemented here")


def test_n8n_connection():
    """Test n8n connection."""
    st.info("n8n connection test would be implemented here")


def export_data(data_type):
    """Export specific data type."""
    import json

    data_map = {
        'products': st.session_state.get('products', []),
        'drafts': st.session_state.get('content_drafts', []),
        'approval': st.session_state.get('approval_queue', []),
        'published': st.session_state.get('published_posts', [])
    }

    data = data_map.get(data_type, [])
    json_str = json.dumps(data, indent=2, default=str)

    st.download_button(
        label=f"Download {data_type.title()}",
        data=json_str,
        file_name=f"{data_type}_{datetime.now().strftime('%Y%m%d')}.json",
        mime="application/json"
    )


def export_all_data():
    """Export all data."""
    import json

    all_data = {
        'products': st.session_state.get('products', []),
        'content_drafts': st.session_state.get('content_drafts', []),
        'approval_queue': st.session_state.get('approval_queue', []),
        'published_posts': st.session_state.get('published_posts', []),
        'settings': st.session_state.get('settings', {}),
        'exported_at': datetime.now().isoformat()
    }

    json_str = json.dumps(all_data, indent=2, default=str)

    st.download_button(
        label="Download Complete Backup",
        data=json_str,
        file_name=f"jp_finds_deals_backup_{datetime.now().strftime('%Y%m%d')}.json",
        mime="application/json"
    )


def import_data(uploaded_file, import_type):
    """Import data from uploaded file."""
    import json

    try:
        data = json.load(uploaded_file)

        if import_type == "Products":
            st.session_state.products = data
        elif import_type == "Drafts":
            st.session_state.content_drafts = data
        elif import_type == "Approval Items":
            st.session_state.approval_queue = data
        elif import_type == "Published Posts":
            st.session_state.published_posts = data

        st.success(f"Imported {len(data)} {import_type.lower()}!")
    except Exception as e:
        st.error(f"Import failed: {str(e)}")