"""
Analytics component for JP Finds Deals.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from utils.helpers import format_currency, format_date


def render_analytics():
    """Render the Analytics dashboard."""

    st.header("📊 Analytics")

    published_posts = st.session_state.get('published_posts', [])
    products = st.session_state.get('products', [])
    approval_queue = st.session_state.get('approval_queue', [])

    # Time period selector
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        period = st.selectbox(
            "Time Period",
            ["Last 7 days", "Last 30 days", "Last 90 days", "This Quarter", "All Time"],
            index=1,
            key="analytics_period"
        )
    with col2:
        if st.button("📥 Export Report", use_container_width=True):
            export_analytics_report()
    with col3:
        if st.button("🔄 Refresh", use_container_width=True):
            st.rerun()

    # Calculate date range
    now = datetime.now()
    period_days = {
        "Last 7 days": 7,
        "Last 30 days": 30,
        "Last 90 days": 90,
        "This Quarter": 90,
        "All Time": 3650
    }
    days = period_days.get(period, 30)
    start_date = now - timedelta(days=days)

    # Filter posts by date
    filtered_posts = [
        p for p in published_posts
        if p.get('published_at') and datetime.fromisoformat(p['published_at'].replace('Z', '+00:00')) >= start_date
    ]

    # KPI Cards
    render_kpi_cards(filtered_posts, products, approval_queue)

    st.divider()

    # Charts row 1
    col1, col2 = st.columns(2)

    with col1:
        render_views_trend_chart(filtered_posts)
        render_engagement_breakdown(filtered_posts)

    with col2:
        render_platform_performance(filtered_posts)
        render_affiliate_performance(filtered_posts)

    st.divider()

    # Charts row 2
    col1, col2 = st.columns(2)

    with col1:
        render_category_performance(products, filtered_posts)
        render_posting_frequency(filtered_posts)

    with col2:
        render_top_performing_posts(filtered_posts)
        render_conversion_funnel(filtered_posts)

    st.divider()

    # Detailed tables
    render_detailed_tables(products, filtered_posts, approval_queue)


def render_kpi_cards(filtered_posts, products, approval_queue):
    """Render KPI metric cards."""

    # Calculate metrics
    total_posts = len(filtered_posts)
    total_views = sum(p.get('views', 0) for p in filtered_posts)
    total_likes = sum(p.get('likes', 0) for p in filtered_posts)
    total_comments = sum(p.get('comments', 0) for p in filtered_posts)
    total_shares = sum(p.get('shares', 0) for p in filtered_posts)
    total_saves = sum(p.get('saves', 0) for p in filtered_posts)
    total_clicks = sum(p.get('affiliate_clicks', 0) for p in filtered_posts)
    total_commission = sum(p.get('commission', 0) for p in filtered_posts)
    total_conversions = sum(p.get('conversions', 0) for p in filtered_posts)

    avg_views = total_views / total_posts if total_posts > 0 else 0
    engagement_rate = ((total_likes + total_comments + total_shares + total_saves) / total_views * 100) if total_views > 0 else 0
    ctr = (total_clicks / total_views * 100) if total_views > 0 else 0
    conversion_rate = (total_conversions / total_clicks * 100) if total_clicks > 0 else 0

    # Row 1: Content metrics
    st.subheader("📈 Content Performance")
    cols = st.columns(5)
    metrics = [
        ("Posts Published", total_posts, "📹"),
        ("Total Views", f"{total_views:,}", "👁️"),
        ("Avg Views/Post", f"{avg_views:,.0f}", "📊"),
        ("Engagement Rate", f"{engagement_rate:.2f}%", "💬"),
        ("Click-Through Rate", f"{ctr:.2f}%", "🖱️")
    ]
    for i, (label, value, icon) in enumerate(metrics):
        with cols[i]:
            st.metric(label, value)

    # Row 2: Affiliate metrics
    st.subheader("💰 Affiliate Revenue")
    cols = st.columns(5)
    metrics = [
        ("Total Clicks", total_clicks, "🖱️"),
        ("Conversions", total_conversions, "✅"),
        ("Conversion Rate", f"{conversion_rate:.2f}%", "📈"),
        ("Commission Earned", format_currency(total_commission), "💰"),
        ("Avg Commission/Post", format_currency(total_commission / total_posts if total_posts > 0 else 0), "📏")
    ]
    for i, (label, value, icon) in enumerate(metrics):
        with cols[i]:
            st.metric(label, value)


def render_views_trend_chart(posts):
    """Render views trend over time."""

    st.subheader("📈 Views Trend")

    if not posts:
        st.info("No published posts in selected period")
        return

    # Group by date
    daily_views = {}
    for post in posts:
        if post.get('published_at'):
            date_key = datetime.fromisoformat(post['published_at'].replace('Z', '+00:00')).strftime('%Y-%m-%d')
            daily_views[date_key] = daily_views.get(date_key, 0) + post.get('views', 0)

    if not daily_views:
        st.info("No view data available")
        return

    df = pd.DataFrame(sorted(daily_views.items()), columns=['Date', 'Views'])
    df['Date'] = pd.to_datetime(df['Date'])

    fig = px.line(
        df, x='Date', y='Views',
        markers=True,
        title="Daily Views"
    )
    fig.update_traces(line_color='#FF6B35', line_width=3)
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#FAFAFA'),
        margin=dict(l=0, r=0, t=30, b=0),
        height=300,
        xaxis_title="",
        yaxis_title="Views"
    )
    st.plotly_chart(fig, use_container_width=True)


def render_engagement_breakdown(posts):
    """Render engagement breakdown."""

    st.subheader("💬 Engagement Breakdown")

    if not posts:
        st.info("No engagement data")
        return

    engagement_data = {
        'Metric': ['Likes', 'Comments', 'Shares', 'Saves'],
        'Count': [
            sum(p.get('likes', 0) for p in posts),
            sum(p.get('comments', 0) for p in posts),
            sum(p.get('shares', 0) for p in posts),
            sum(p.get('saves', 0) for p in posts)
        ]
    }

    df = pd.DataFrame(engagement_data)

    fig = px.bar(
        df, x='Metric', y='Count',
        color='Count', color_continuous_scale='Oranges',
        text='Count'
    )
    fig.update_traces(textposition='outside')
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#FAFAFA'),
        margin=dict(l=0, r=0, t=20, b=0),
        height=300,
        showlegend=False
    )
    st.plotly_chart(fig, use_container_width=True)


def render_platform_performance(posts):
    """Render performance by content type."""

    st.subheader("📱 Performance by Content Type")

    if not posts:
        st.info("No content type data")
        return

    type_stats = {}
    for post in posts:
        ctype = post.get('content_type', 'Reel')
        if ctype not in type_stats:
            type_stats[ctype] = {'posts': 0, 'views': 0, 'engagement': 0, 'clicks': 0, 'commission': 0}

        type_stats[ctype]['posts'] += 1
        type_stats[ctype]['views'] += post.get('views', 0)
        type_stats[ctype]['engagement'] += post.get('likes', 0) + post.get('comments', 0) + post.get('shares', 0) + post.get('saves', 0)
        type_stats[ctype]['clicks'] += post.get('affiliate_clicks', 0)
        type_stats[ctype]['commission'] += post.get('commission', 0)

    df = pd.DataFrame([
        {
            'Content Type': k,
            'Posts': v['posts'],
            'Total Views': v['views'],
            'Avg Views': round(v['views'] / v['posts']) if v['posts'] > 0 else 0,
            'Engagement': v['engagement'],
            'Clicks': v['clicks'],
            'Commission': v['commission']
        }
        for k, v in type_stats.items()
    ])

    # Bar chart for avg views by type
    fig = px.bar(
        df, x='Content Type', y='Avg Views',
        color='Content Type', text='Avg Views'
    )
    fig.update_traces(texttemplate='%{y:,.0f}', textposition='outside')
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#FAFAFA'),
        margin=dict(l=0, r=0, t=20, b=0),
        height=300,
        showlegend=False
    )
    st.plotly_chart(fig, use_container_width=True)

    # Table
    st.dataframe(df, hide_index=True, use_container_width=True)


def render_affiliate_performance(posts):
    """Render affiliate performance by marketplace."""

    st.subheader("🛒 Affiliate by Marketplace")

    # This would need marketplace data on posts
    # For now, show overall affiliate metrics

    if not posts:
        st.info("No affiliate data")
        return

    # Simulate marketplace breakdown (would come from actual data)
    marketplace_data = {
        'Marketplace': ['Amazon', 'Flipkart', 'Other'],
        'Clicks': [sum(p.get('affiliate_clicks', 0) for p in posts) * 0.6,
                   sum(p.get('affiliate_clicks', 0) for p in posts) * 0.3,
                   sum(p.get('affiliate_clicks', 0) for p in posts) * 0.1],
        'Conversions': [sum(p.get('conversions', 0) for p in posts) * 0.5,
                        sum(p.get('conversions', 0) for p in posts) * 0.3,
                        sum(p.get('conversions', 0) for p in posts) * 0.2],
        'Commission': [sum(p.get('commission', 0) for p in posts) * 0.55,
                       sum(p.get('commission', 0) for p in posts) * 0.35,
                       sum(p.get('commission', 0) for p in posts) * 0.1]
    }

    df = pd.DataFrame(marketplace_data)
    df['Clicks'] = df['Clicks'].astype(int)
    df['Conversions'] = df['Conversions'].astype(int)
    df['Commission'] = df['Commission'].round(0)

    fig = px.pie(
        df, values='Commission', names='Marketplace',
        title="Commission by Marketplace",
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#FAFAFA'),
        margin=dict(l=0, r=0, t=30, b=0),
        height=300
    )
    st.plotly_chart(fig, use_container_width=True)


def render_category_performance(products, posts):
    """Render performance by product category."""

    st.subheader("📦 Performance by Category")

    if not products:
        st.info("No product data")
        return

    # Category stats
    category_stats = {}
    for product in products:
        cat = product.get('category', 'Uncategorized')
        if cat not in category_stats:
            category_stats[cat] = {'products': 0, 'published': 0, 'views': 0, 'commission': 0}
        category_stats[cat]['products'] += 1

    # Match with published posts
    for post in posts:
        # Find product category
        product = next((p for p in products if p.get('id') == post.get('product_id')), None)
        if product:
            cat = product.get('category', 'Uncategorized')
            if cat in category_stats:
                category_stats[cat]['published'] += 1
                category_stats[cat]['views'] += post.get('views', 0)
                category_stats[cat]['commission'] += post.get('commission', 0)

    df = pd.DataFrame([
        {
            'Category': k,
            'Total Products': v['products'],
            'Published': v['published'],
            'Publish Rate': f"{(v['published']/v['products']*100):.1f}%" if v['products'] > 0 else "0%",
            'Total Views': v['views'],
            'Commission': v['commission']
        }
        for k, v in category_stats.items()
    ])

    if not df.empty:
        fig = px.bar(
            df, x='Category', y='Commission',
            color='Commission', color_continuous_scale='Viridis',
            text='Commission'
        )
        fig.update_traces(texttemplate='₹%{y:,.0f}', textposition='outside')
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#FAFAFA'),
            margin=dict(l=0, r=0, t=20, b=0),
            height=300,
            showlegend=False,
            xaxis_tickangle=-45
        )
        st.plotly_chart(fig, use_container_width=True)

    st.dataframe(df, hide_index=True, use_container_width=True)


def render_posting_frequency(posts):
    """Render posting frequency analysis."""

    st.subheader("📅 Posting Frequency")

    if not posts:
        st.info("No posting data")
        return

    # Day of week analysis
    dow_stats = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0}
    dow_names = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']

    for post in posts:
        if post.get('published_at'):
            dow = datetime.fromisoformat(post['published_at'].replace('Z', '+00:00')).weekday()
            dow_stats[dow] += 1

    df = pd.DataFrame({
        'Day': [dow_names[i] for i in range(7)],
        'Posts': [dow_stats[i] for i in range(7)]
    })

    fig = px.bar(
        df, x='Day', y='Posts',
        color='Posts', color_continuous_scale='Blues'
    )
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#FAFAFA'),
        margin=dict(l=0, r=0, t=20, b=0),
        height=300,
        showlegend=False
    )
    st.plotly_chart(fig, use_container_width=True)


def render_top_performing_posts(posts):
    """Render top performing posts table."""

    st.subheader("🏆 Top Performing Posts")

    if not posts:
        st.info("No posts to rank")
        return

    # Sort by views
    top_posts = sorted(posts, key=lambda x: x.get('views', 0), reverse=True)[:10]

    data = []
    for i, post in enumerate(top_posts):
        engagement = post.get('likes', 0) + post.get('comments', 0) + post.get('shares', 0) + post.get('saves', 0)
        engagement_rate = (engagement / post.get('views', 1) * 100) if post.get('views', 0) > 0 else 0

        data.append({
            'Rank': i + 1,
            'Product': post.get('product_name', 'Unknown')[:30],
            'Type': post.get('content_type', 'Reel'),
            'Views': post.get('views', 0),
            'Engagement': engagement,
            'Eng. Rate': f"{engagement_rate:.2f}%",
            'Clicks': post.get('affiliate_clicks', 0),
            'Commission': f"₹{post.get('commission', 0):,.0f}",
            'Date': format_date(post.get('published_at', ''))
        })

    df = pd.DataFrame(data)
    st.dataframe(df, hide_index=True, use_container_width=True)


def render_conversion_funnel(posts):
    """Render conversion funnel."""

    st.subheader("🔄 Conversion Funnel")

    if not posts:
        st.info("No conversion data")
        return

    total_views = sum(p.get('views', 0) for p in posts)
    total_clicks = sum(p.get('affiliate_clicks', 0) for p in posts)
    total_conversions = sum(p.get('conversions', 0) for p in posts)

    funnel_data = [
        {'stage': 'Views', 'count': total_views},
        {'stage': 'Clicks', 'count': total_clicks},
        {'stage': 'Conversions', 'count': total_conversions}
    ]

    fig = go.Figure(go.Funnel(
        y=[d['stage'] for d in funnel_data],
        x=[d['count'] for d in funnel_data],
        textinfo="value+percent initial",
        marker={"color": ["#FF6B35", "#F59E0B", "#10B981"]}
    ))
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#FAFAFA'),
        margin=dict(l=0, r=0, t=30, b=0),
        height=300
    )
    st.plotly_chart(fig, use_container_width=True)


def render_detailed_tables(products, posts, approval_queue):
    """Render detailed data tables."""

    tab1, tab2, tab3, tab4 = st.tabs(["📊 All Posts", "📦 Products", "✅ Approval History", "💰 Affiliate Details"])

    with tab1:
        if posts:
            data = []
            for post in sorted(posts, key=lambda x: x.get('published_at', ''), reverse=True):
                engagement = post.get('likes', 0) + post.get('comments', 0) + post.get('shares', 0) + post.get('saves', 0)
                data.append({
                    'Date': format_date(post.get('published_at', '')),
                    'Product': post.get('product_name', 'Unknown'),
                    'Type': post.get('content_type', 'Reel'),
                    'Views': post.get('views', 0),
                    'Engagement': engagement,
                    'Clicks': post.get('affiliate_clicks', 0),
                    'Conversions': post.get('conversions', 0),
                    'Commission': f"₹{post.get('commission', 0):,.0f}",
                    'Media ID': post.get('instagram_media_id', 'N/A')
                })
            df = pd.DataFrame(data)
            st.dataframe(df, hide_index=True, use_container_width=True)
        else:
            st.info("No published posts")

    with tab2:
        if products:
            data = []
            for product in products:
                # Find published posts for this product
                product_posts = [p for p in posts if p.get('product_id') == product.get('id')]
                total_views = sum(p.get('views', 0) for p in product_posts)
                total_commission = sum(p.get('commission', 0) for p in product_posts)

                data.append({
                    'Product': product.get('name', 'Unknown'),
                    'Marketplace': product.get('marketplace', 'Unknown'),
                    'Category': product.get('category', 'Uncategorized'),
                    'Price': f"₹{product.get('price', 0):,.0f}",
                    'Status': product.get('status', 'discovered').replace('_', ' ').title(),
                    'Posts': len(product_posts),
                    'Total Views': total_views,
                    'Commission': f"₹{total_commission:,.0f}",
                    'AI Score': product.get('score', 0)
                })
            df = pd.DataFrame(data)
            st.dataframe(df, hide_index=True, use_container_width=True)
        else:
            st.info("No products")

    with tab3:
        if approval_queue:
            data = []
            for item in approval_queue:
                data.append({
                    'Date': format_date(item.get('created_at', '')),
                    'Product': item.get('product_name', 'Unknown'),
                    'Type': item.get('content_type', 'Reel'),
                    'Status': item.get('status', 'pending').replace('_', ' ').title(),
                    'Updated': format_date(item.get('updated_at', '')),
                    'Published': format_date(item.get('published_at', '')) if item.get('published_at') else '-'
                })
            df = pd.DataFrame(data)
            st.dataframe(df, hide_index=True, use_container_width=True)
        else:
            st.info("No approval history")

    with tab4:
        if posts:
            data = []
            for post in posts:
                data.append({
                    'Product': post.get('product_name', 'Unknown'),
                    'Date': format_date(post.get('published_at', '')),
                    'Clicks': post.get('affiliate_clicks', 0),
                    'Conversions': post.get('conversions', 0),
                    'Conv. Rate': f"{(post.get('conversions', 0)/post.get('affiliate_clicks', 1)*100):.2f}%" if post.get('affiliate_clicks', 0) > 0 else "0%",
                    'Commission': f"₹{post.get('commission', 0):,.0f}",
                    'Avg Order Value': f"₹{post.get('commission', 0)/post.get('conversions', 1):,.0f}" if post.get('conversions', 0) > 0 else "N/A"
                })
            df = pd.DataFrame(data)
            st.dataframe(df, hide_index=True, use_container_width=True)
        else:
            st.info("No affiliate data")


def export_analytics_report():
    """Export analytics report as JSON."""
    import json

    report = {
        'generated_at': datetime.now().isoformat(),
        'period': st.session_state.get('analytics_period', 'Last 30 days'),
        'posts': st.session_state.get('published_posts', []),
        'products': st.session_state.get('products', []),
        'approval_queue': st.session_state.get('approval_queue', [])
    }

    json_str = json.dumps(report, indent=2, default=str)

    st.download_button(
        label="Download Analytics Report",
        data=json_str,
        file_name=f"analytics_report_{datetime.now().strftime('%Y%m%d')}.json",
        mime="application/json"
    )