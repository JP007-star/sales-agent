"""
Sidebar component for JP Finds Deals navigation.
"""

import streamlit as st
from datetime import datetime


def render_sidebar():
    """Render the sidebar navigation and return selected page."""

    with st.sidebar:
        # Logo/Brand
        st.markdown("""
        <div style="text-align: center; padding: 1rem 0;">
            <h1 style="margin: 0; color: #FF6B35;">🛍️ JP Finds Deals</h1>
            <p style="margin: 0.5rem 0 0; color: #888; font-size: 0.85rem;">AI Sales Agent</p>
            <p style="margin: 0.25rem 0 0; color: #666; font-size: 0.75rem;">@jp.finds.deals</p>
        </div>
        """, unsafe_allow_html=True)

        st.divider()

        # Navigation Menu
        st.subheader("📋 Navigation")

        pages = {
            "Dashboard": "🏠 Dashboard",
            "Product Manager": "📦 Product Manager",
            "Content Studio": "✍️ Content Studio",
            "Approval Queue": "✅ Approval Queue",
            "Analytics": "📊 Analytics",
            "Workflows": "🔄 Workflows",
            "Settings": "⚙️ Settings"
        }

        # Initialize current page in session state if not exists
        if 'current_page' not in st.session_state:
            st.session_state.current_page = "Dashboard"

        # Create navigation buttons
        for page_key, page_label in pages.items():
            is_active = st.session_state.current_page == page_key
            button_type = "primary" if is_active else "secondary"

            if st.button(
                page_label,
                key=f"nav_{page_key}",
                use_container_width=True,
                type=button_type
            ):
                st.session_state.current_page = page_key
                st.rerun()

        st.divider()

        # Quick Stats in Sidebar
        st.subheader("📊 Quick Stats")

        # Products by status
        products = st.session_state.get('products', [])
        if products:
            status_counts = {}
            for product in products:
                status = product.get('status', 'discovered')
                status_counts[status] = status_counts.get(status, 0) + 1

            for status, count in status_counts.items():
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.caption(status.replace('_', ' ').title())
                with col2:
                    st.caption(f"**{count}**")

        # Approval queue count
        approval_queue = st.session_state.get('approval_queue', [])
        pending = len([p for p in approval_queue if p.get('status') == 'pending'])
        approved = len([p for p in approval_queue if p.get('status') == 'approved'])
        published = len(st.session_state.get('published_posts', []))

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Pending", pending)
        with col2:
            st.metric("Approved", approved)
        with col3:
            st.metric("Published", published)

        st.divider()

        # Quick Actions in Sidebar
        st.subheader("⚡ Quick Actions")

        if st.button("➕ Add Product", use_container_width=True, key="sidebar_add_product"):
            st.session_state.current_page = "Product Manager"
            st.session_state.show_add_product = True
            st.rerun()

        if st.button("🎬 Generate Content", use_container_width=True, key="sidebar_generate_content"):
            st.session_state.current_page = "Content Studio"
            st.rerun()

        if st.button("📤 Publish Approved", use_container_width=True, key="sidebar_publish"):
            st.session_state.current_page = "Approval Queue"
            st.rerun()

        st.divider()

        # Publishing Schedule
        st.subheader("📅 Schedule")
        schedule = st.session_state.settings.get('publishing_schedule', ['12:00', '19:00'])
        for i, time_slot in enumerate(schedule):
            st.caption(f"🕐 Slot {i+1}: {time_slot} IST")

        st.divider()

        # User Profile Section
        st.subheader("👤 Account")

        col1, col2 = st.columns([1, 3])
        with col1:
            st.image("https://api.dicebear.com/7.x/avataaars/svg?seed=jpfindsdeals", width=40)
        with col2:
            st.write("**JP Finds Deals**")
            st.caption("Digital Creator | Affiliate")

        st.divider()

        # Settings/Info
        st.subheader("ℹ️ About")
        st.caption("JP Finds Deals AI Agent v1.0.0")
        st.caption("Built with Streamlit")
        st.caption(f"Session: {datetime.now().strftime('%Y-%m-%d %H:%M')}")

        # Theme toggle (visual only)
        st.divider()
        theme = st.selectbox(
            "🎨 Theme",
            ["System Default", "Light", "Dark"],
            index=0,
            key="theme_selector"
        )

        return st.session_state.current_page