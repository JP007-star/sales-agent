"""
Sidebar component for Sales Pipeline navigation.
"""

import streamlit as st
from datetime import datetime


def render_sidebar():
    """Render the sidebar navigation and return selected page."""

    with st.sidebar:
        # Logo/Brand
        st.markdown("""
        <div style="text-align: center; padding: 1rem 0;">
            <h1 style="margin: 0; color: #00D4AA;">📈 Sales Pipeline</h1>
            <p style="margin: 0.5rem 0 0; color: #888; font-size: 0.85rem;">B2B Sales Management Suite</p>
        </div>
        """, unsafe_allow_html=True)

        st.divider()

        # Navigation Menu
        st.subheader("📋 Navigation")

        pages = {
            "Dashboard": "🏠 Dashboard",
            "Leads": "👥 Leads",
            "Pipeline": "📊 Pipeline",
            "Outreach": "📧 Outreach",
            "Analytics": "📈 Analytics",
            "Settings": "⚙️ Settings",
            "Help": "📚 Help"
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

        if 'data_manager' in st.session_state:
            dm = st.session_state.data_manager
            leads = dm.get_leads()

            # Count leads by stage
            stage_counts = {}
            for lead in leads:
                stage = lead.get('stage', 'New')
                stage_counts[stage] = stage_counts.get(stage, 0) + 1

            for stage, count in stage_counts.items():
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.caption(stage)
                with col2:
                    st.caption(f"**{count}**")

        st.divider()

        # User Profile Section
        st.subheader("👤 Profile")

        col1, col2 = st.columns([1, 3])
        with col1:
            st.image("https://api.dicebear.com/7.x/avataaars/svg?seed=salesagent", width=40)
        with col2:
            st.write("**Sales Agent User**")
            st.caption("Account Executive")

        # Quick Actions in Sidebar
        st.divider()
        st.subheader("⚡ Quick Actions")

        if st.button("➕ New Lead", use_container_width=True, key="sidebar_new_lead"):
            st.session_state.show_lead_modal = True
            st.rerun()

        if st.button("📧 New Campaign", use_container_width=True, key="sidebar_new_campaign"):
            st.session_state.current_page = "Outreach"
            st.session_state.show_campaign_modal = True
            st.rerun()

        if st.button("📞 Log Activity", use_container_width=True, key="sidebar_log_activity"):
            st.session_state.show_activity_modal = True
            st.rerun()

        st.divider()

        # Settings/Info
        st.subheader("ℹ️ About")
        st.caption("Sales Agent v1.0.0")
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