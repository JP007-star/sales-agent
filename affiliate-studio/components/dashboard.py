"""
Dashboard component for JP Finds Deals.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from utils.helpers import format_currency, format_date, get_relative_time


def render_dashboard():
    """Render the main dashboard with overview metrics and charts."""

    st.header("🏠 Dashboard")

    # Key Metrics Row
    st.subheader("📊 Overview")

    products = st.session_state.get('products', [])
    approval_queue = st.session_state.get('approval_queue', [])
    published_posts = st.session_state.get('published_posts', [])
    content_drafts = st.session_state.get('content_drafts', [])

    # Calculate metrics
    total_products = len(products)
    products_today = len([p for p in products if _is_today(p.get('created_at'))])
    pending_approval = len([p for p in approval_queue if p.get('status') == 'pending'])
    approved_ready = len([p for p in approval_queue if p.get('status') == 'approved'])
    published_count = len(published_posts)
    drafts_count = len(content_drafts)

    # Affiliate metrics
    total_clicks = sum(p.get('affiliate_clicks', 0) for p in published_posts)
    total_commission = sum(p.get('commission', 0) for p in published_posts)

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.metric(
            "Total Products",
            total_products,
            delta=products_today,
            delta_color="normal"
        )

    with col2:
        st.metric(
            "Pending Approval",
            pending_approval,
            delta=None
        )

    with col3:
        st.metric(
            "Ready to Publish",
            approved_ready,
            delta=None
        )

    with col4:
        st.metric(
            "Published Reels",
            published_count,
            delta=None
        )

    with col5:
        st.metric(
            "Est. Commission",
            format_currency(total_commission),
            delta=f"{total_clicks} clicks"
        )

    st.divider()

    # Charts Row
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📦 Products by Category")
        category_data = _get_category_distribution(products)
        if category_data:
            fig = px.pie(
                category_data,
                values='count',
                names='category',
                title="Product Distribution by Category",
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#FAFAFA'),
                showlegend=True,
                height=300
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No products yet. Add products to see distribution.")

    with col2:
        st.subheader("📈 Publishing Pipeline")
        pipeline_data = [
            {'stage': 'Discovered', 'count': len([p for p in products if p.get('status') == 'discovered'])},
            {'stage': 'Content Generated', 'count': len(content_drafts)},
            {'stage': 'Video Ready', 'count': len([p for p in approval_queue if p.get('status') in ['pending', 'approved']])},
            {'stage': 'Published', 'count': published_count},
        ]

        fig = go.Figure(go.Funnel(
            y=[p['stage'] for p in pipeline_data],
            x=[p['count'] for p in pipeline_data],
            textinfo="value+percent initial",
            marker={"color": ["#6B7280", "#3B82F6", "#F59E0B", "#10B981"]},
            connector={"line": {"color": "#333", "dash": "dot", "width": 1}}
        ))
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#FAFAFA'),
            margin=dict(l=0, r=0, t=20, b=0),
            height=300
        )
        st.plotly_chart(fig, use_container_width=True)

    # Recent Activity & Quick Actions
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🔔 Recent Activity")
        activities = _get_recent_activities()
        if activities:
            for activity in activities[:8]:
                with st.container():
                    cols = st.columns([1, 4, 1])
                    with cols[0]:
                        st.caption(activity['time'])
                    with cols[1]:
                        st.write(f"**{activity['type']}** - {activity['description']}")
                    with cols[2]:
                        if activity.get('product'):
                            st.caption(activity['product'][:20])
        else:
            st.info("No recent activity. Start by adding a product!")

    with col2:
        st.subheader("📅 Upcoming Schedule")
        schedule = st.session_state.settings.get('publishing_schedule', ['12:00', '19:00'])
        for i, time_slot in enumerate(schedule):
            st.write(f"🕐 **Slot {i+1}**: {time_slot} IST")

        st.divider()

        # Daily targets
        st.write("**Daily Targets**")
        st.write(f"🎬 Reels: {st.session_state.settings.get('daily_reels_target', 2)}/day")
        st.write(f"📱 Stories: {st.session_state.settings.get('daily_stories_target', 3)}/day")
        st.write("📊 Weekly Roundup: 1/week")

    # Quick Actions
    st.divider()
    st.subheader("⚡ Quick Actions")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        if st.button("➕ Add Product", use_container_width=True, type="primary"):
            st.session_state.current_page = "Product Manager"
            st.session_state.show_add_product = True
            st.rerun()

    with col2:
        if st.button("🎬 Generate Content", use_container_width=True):
            st.session_state.current_page = "Content Studio"
            st.rerun()

    with col3:
        if st.button("✅ Review Queue", use_container_width=True):
            st.session_state.current_page = "Approval Queue"
            st.rerun()

    with col4:
        if st.button("📊 View Analytics", use_container_width=True):
            st.session_state.current_page = "Analytics"
            st.rerun()

    # Affiliate Performance Summary
    st.divider()
    st.subheader("💰 Affiliate Performance")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total Clicks", total_clicks)

    with col2:
        st.metric("Total Commission", format_currency(total_commission))

    with col3:
        avg_commission = total_commission / published_count if published_count > 0 else 0
        st.metric("Avg/Reel", format_currency(avg_commission))

    with col4:
        conversion_rate = (sum(p.get('conversions', 0) for p in published_posts) / total_clicks * 100) if total_clicks > 0 else 0
        st.metric("Conversion Rate", f"{conversion_rate:.2f}%")

    # Top performing products
    if published_posts:
        st.write("**Top Performing Products**")
        top_products = sorted(published_posts, key=lambda x: x.get('commission', 0), reverse=True)[:5]

        for i, product in enumerate(top_products):
            cols = st.columns([1, 3, 1, 1, 1])
            with cols[0]:
                st.write(f"#{i+1}")
            with cols[1]:
                st.write(f"**{product.get('product_name', 'Unknown')}**")
                st.caption(f"via {product.get('marketplace', 'Unknown')}")
            with cols[2]:
                st.write(f"👁️ {product.get('views', 0)}")
            with cols[3]:
                st.write(f"🖱️ {product.get('affiliate_clicks', 0)}")
            with cols[4]:
                st.write(f"💰 {format_currency(product.get('commission', 0))}")


def _is_today(date_str):
    """Check if date string is today."""
    if not date_str:
        return False
    try:
        dt = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
        return dt.date() == datetime.now().date()
    except:
        return False


def _get_category_distribution(products):
    """Get product count by category."""
    categories = {}
    for product in products:
        cat = product.get('category', 'Uncategorized')
        categories[cat] = categories.get(cat, 0) + 1

    return [{'category': k, 'count': v} for k, v in categories.items()]


def _get_recent_activities():
    """Get recent activities from products and approval queue."""
    activities = []

    # Product activities
    products = st.session_state.get('products', [])
    for product in products[-5:]:
        activities.append({
            'time': get_relative_time(product.get('created_at', '')),
            'type': 'Product Added',
            'description': f"Added {product.get('name', 'product')} from {product.get('marketplace', 'unknown')}",
            'product': product.get('name', ''),
            'timestamp': product.get('created_at', '')
        })

    # Approval activities
    approval_queue = st.session_state.get('approval_queue', [])
    for item in approval_queue[-5:]:
        if item.get('updated_at'):
            activities.append({
                'time': get_relative_time(item.get('updated_at', '')),
                'type': f"{item.get('status', '').title()}",
                'description': f"{item.get('product_name', 'Product')} moved to {item.get('status', 'pending')}",
                'product': item.get('product_name', ''),
                'timestamp': item.get('updated_at', '')
            })

    # Sort by timestamp
    activities.sort(key=lambda x: x.get('timestamp', ''), reverse=True)
    return activities[:10]