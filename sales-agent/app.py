"""
Sales Agent - Streamlit Application
A comprehensive sales management tool with lead tracking, pipeline visualization,
outreach automation, and analytics dashboard.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json
import os
from pathlib import Path

# Page configuration
st.set_page_config(
    page_title="Sales Agent",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Import custom components
from components.sidebar import render_sidebar
from components.leads import render_leads_tab
from components.pipeline import render_pipeline_tab
from components.outreach import render_outreach_tab
from components.analytics import render_analytics_tab
from components.settings import render_settings_tab
from utils.data_manager import DataManager
from utils.helpers import format_currency, format_date

# Initialize session state
if 'data_manager' not in st.session_state:
    st.session_state.data_manager = DataManager()

if 'current_page' not in st.session_state:
    st.session_state.current_page = 'Dashboard'

# Load custom CSS
def load_css():
    css_path = Path(__file__).parent / "styles" / "main.css"
    if css_path.exists():
        with open(css_path) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()

# Main App
def main():
    # Render sidebar and get selected page
    selected_page = render_sidebar()
    st.session_state.current_page = selected_page

    # Header
    col1, col2, col3 = st.columns([3, 1, 1])
    with col1:
        st.title("📈 Sales Agent")
        st.caption(f"Welcome back! Today is {datetime.now().strftime('%B %d, %Y')}")

    with col2:
        # Quick stats
        leads_count = len(st.session_state.data_manager.get_leads())
        st.metric("Total Leads", leads_count)

    with col3:
        pipeline_value = st.session_state.data_manager.get_pipeline_value()
        st.metric("Pipeline Value", format_currency(pipeline_value))

    st.divider()

    # Render selected page
    if selected_page == "Dashboard":
        render_dashboard()
    elif selected_page == "Leads":
        render_leads_tab()
    elif selected_page == "Pipeline":
        render_pipeline_tab()
    elif selected_page == "Outreach":
        render_outreach_tab()
    elif selected_page == "Analytics":
        render_analytics_tab()
    elif selected_page == "Settings":
        render_settings_tab()

def render_dashboard():
    """Render the main dashboard with overview metrics and charts."""

    # Key Metrics Row
    st.subheader("📊 Overview")

    metrics = st.session_state.data_manager.get_dashboard_metrics()

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.metric(
            "Total Leads",
            metrics['total_leads'],
            delta=metrics['leads_change'],
            delta_color="normal"
        )

    with col2:
        st.metric(
            "Active Deals",
            metrics['active_deals'],
            delta=metrics['deals_change'],
            delta_color="normal"
        )

    with col3:
        st.metric(
            "Pipeline Value",
            format_currency(metrics['pipeline_value']),
            delta=format_currency(metrics['pipeline_change']),
            delta_color="normal"
        )

    with col4:
        st.metric(
            "Won This Month",
            format_currency(metrics['won_this_month']),
            delta=format_currency(metrics['won_change']),
            delta_color="normal"
        )

    with col4:
        st.metric(
            "Conversion Rate",
            f"{metrics['conversion_rate']:.1f}%",
            delta=f"{metrics['conversion_change']:.1f}%",
            delta_color="normal"
        )

    st.divider()

    # Charts Row
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📈 Pipeline by Stage")
        pipeline_data = st.session_state.data_manager.get_pipeline_by_stage()
        if pipeline_data:
            fig = px.funnel(
                pipeline_data,
                x='value',
                y='stage',
                title="Sales Pipeline Funnel",
                color='stage',
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#FAFAFA'),
                showlegend=False
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No pipeline data available. Add leads to see the funnel.")

    with col2:
        st.subheader("💰 Revenue Trend")
        revenue_data = st.session_state.data_manager.get_revenue_trend()
        if revenue_data:
            fig = px.line(
                revenue_data,
                x='date',
                y='value',
                title="Monthly Revenue Trend",
                markers=True
            )
            fig.update_traces(line_color='#00D4AA', line_width=3)
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#FAFAFA'),
                xaxis_title="",
                yaxis_title="Revenue ($)"
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No revenue data available yet.")

    # Recent Activity & Upcoming Tasks
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🔔 Recent Activity")
        activities = st.session_state.data_manager.get_recent_activities(limit=10)
        if activities:
            for activity in activities:
                with st.container():
                    cols = st.columns([1, 4, 1])
                    with cols[0]:
                        st.caption(activity['time'])
                    with cols[1]:
                        st.write(f"**{activity['type']}** - {activity['description']}")
                    with cols[2]:
                        if activity['lead']:
                            st.caption(activity['lead'])
        else:
            st.info("No recent activity.")

    with col2:
        st.subheader("📅 Upcoming Tasks")
        tasks = st.session_state.data_manager.get_upcoming_tasks(limit=10)
        if tasks:
            for task in tasks:
                with st.container():
                    cols = st.columns([1, 4, 1])
                    with cols[0]:
                        due_color = "🔴" if task['overdue'] else "🟢"
                        st.write(due_color)
                    with cols[1]:
                        st.write(f"**{task['title']}**")
                        st.caption(f"Due: {format_date(task['due_date'])} | {task['lead_name']}")
                    with cols[2]:
                        if st.button("✓", key=f"complete_{task['id']}"):
                            st.session_state.data_manager.complete_task(task['id'])
                            st.rerun()
        else:
            st.info("No upcoming tasks.")

    # Quick Actions
    st.divider()
    st.subheader("⚡ Quick Actions")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        if st.button("➕ Add New Lead", use_container_width=True, type="primary"):
            st.session_state.show_lead_modal = True

    with col2:
        if st.button("📧 Send Outreach", use_container_width=True):
            st.session_state.current_page = "Outreach"
            st.rerun()

    with col3:
        if st.button("📞 Log Call", use_container_width=True):
            st.session_state.show_call_modal = True

    with col4:
        if st.button("📊 View Analytics", use_container_width=True):
            st.session_state.current_page = "Analytics"
            st.rerun()

    # Modal for adding lead
    if st.session_state.get('show_lead_modal', False):
        render_add_lead_modal()

def render_add_lead_modal():
    """Render modal for adding a new lead."""
    with st.form("add_lead_form", clear_on_submit=True):
        st.subheader("Add New Lead")

        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Full Name*", placeholder="John Doe")
            email = st.text_input("Email*", placeholder="john@company.com")
            phone = st.text_input("Phone", placeholder="+1 (555) 123-4567")
            company = st.text_input("Company", placeholder="Acme Corp")

        with col2:
            source = st.selectbox("Source*", [
                "Website", "Referral", "Cold Call", "Email Campaign",
                "Social Media", "Event", "Partner", "Other"
            ])
            stage = st.selectbox("Stage*", [
                "New", "Contacted", "Qualified", "Proposal",
                "Negotiation", "Closed Won", "Closed Lost"
            ])
            value = st.number_input("Estimated Value ($)", min_value=0, value=0, step=1000)
            assigned_to = st.selectbox("Assigned To", [
                "Me", "Sarah Johnson", "Mike Chen", "Emily Davis"
            ])

        notes = st.text_area("Notes", placeholder="Initial notes about this lead...")

        col1, col2 = st.columns(2)
        with col1:
            submitted = st.form_submit_button("Create Lead", type="primary", use_container_width=True)
        with col2:
            cancelled = st.form_submit_button("Cancel", use_container_width=True)

        if cancelled:
            st.session_state.show_lead_modal = False
            st.rerun()

        if submitted:
            if name and email:
                lead_data = {
                    'name': name,
                    'email': email,
                    'phone': phone,
                    'company': company,
                    'source': source,
                    'stage': stage,
                    'value': value,
                    'assigned_to': assigned_to,
                    'notes': notes,
                    'created_at': datetime.now().isoformat(),
                    'updated_at': datetime.now().isoformat()
                }
                st.session_state.data_manager.add_lead(lead_data)
                st.session_state.show_lead_modal = False
                st.success(f"Lead '{name}' created successfully!")
                st.rerun()
            else:
                st.error("Please fill in required fields (Name, Email)")

if __name__ == "__main__":
    main()