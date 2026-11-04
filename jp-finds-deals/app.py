"""
JP Finds Deals - AI Sales Agent
Streamlit Application for Instagram Affiliate Marketing Automation

@jp.finds.deals - Automated AI-powered affiliate marketing system
"""

import streamlit as st
import os
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Page configuration
st.set_page_config(
    page_title="JP Finds Deals - AI Sales Agent",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load custom CSS
def load_css():
    css_path = project_root / "assets" / "style.css"
    if css_path.exists():
        with open(css_path) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()

# Initialize session state
def init_session_state():
    defaults = {
        'current_page': 'Dashboard',
        'products': [],
        'content_drafts': [],
        'approval_queue': [],
        'published_posts': [],
        'affiliate_data': {},
        'settings': {
            'gemini_api_key': '',
            'instagram_app_id': '',
            'instagram_app_secret': '',
            'instagram_access_token': '',
            'instagram_business_account_id': '',
            'amazon_associate_tag': '',
            'amazon_access_key': '',
            'amazon_secret_key': '',
            'flipkart_affiliate_id': '',
            'flipkart_affiliate_token': '',
            'canva_api_token': '',
            'publishing_schedule': ['12:00', '19:00'],
            'timezone': 'Asia/Kolkata',
            'auto_publish': False,
            'languages': ['English', 'Tamil', 'English+Tamil'],
            'daily_reels_target': 2,
            'daily_stories_target': 3,
        }
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

init_session_state()

# Import components
from components.sidebar import render_sidebar
from components.dashboard import render_dashboard
from components.product_manager import render_product_manager
from components.content_studio import render_content_studio
from components.approval_queue import render_approval_queue
from components.analytics import render_analytics
from components.settings import render_settings

def main():
    # Render sidebar and get selected page
    selected_page = render_sidebar()
    st.session_state.current_page = selected_page

    # Header
    col1, col2, col3 = st.columns([3, 1, 1])
    with col1:
        st.title("🛍️ JP Finds Deals")
        st.caption("AI-Powered Instagram Affiliate Marketing Automation")

    with col2:
        products_count = len(st.session_state.products)
        st.metric("Products", products_count)

    with col3:
        pending_approval = len([p for p in st.session_state.approval_queue if p.get('status') == 'pending'])
        st.metric("Pending Approval", pending_approval)

    st.divider()

    # Render selected page
    if selected_page == "Dashboard":
        render_dashboard()
    elif selected_page == "Product Manager":
        render_product_manager()
    elif selected_page == "Content Studio":
        render_content_studio()
    elif selected_page == "Approval Queue":
        render_approval_queue()
    elif selected_page == "Analytics":
        render_analytics()
    elif selected_page == "Settings":
        render_settings()
    elif selected_page == "Workflows":
        render_workflows()

if __name__ == "__main__":
    main()