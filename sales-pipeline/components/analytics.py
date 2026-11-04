"""
Analytics component for Sales Agent - Dashboards, charts, and reports.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from utils.helpers import format_currency, format_date


def render_analytics_tab():
    """Render the Analytics dashboard."""

    st.header("📈 Analytics Dashboard")

    # Time period selector
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        period = st.selectbox(
            "Time Period",
            ["Last 7 days", "Last 30 days", "Last 90 days", "This Quarter", "This Year", "All Time"],
            index=1,
            key="analytics_period"
        )
    with col2:
        if st.button("📥 Export Report", use_container_width=True):
            st.info("Report export functionality would be here")
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
        "This Year": 365,
        "All Time": 3650
    }
    days = period_days.get(period, 30)
    start_date = now - timedelta(days=days)

    # Get data
    leads = st.session_state.data_manager.get_leads()
    activities = st.session_state.data_manager.get_recent_activities(1000)

    # Filter by date
    filtered_leads = [
        l for l in leads
        if datetime.fromisoformat(l['created_at']) >= start_date
    ]
    filtered_activities = [
        a for a in activities
        if datetime.fromisoformat(a['timestamp']) >= start_date
    ]

    # KPI Cards
    render_kpi_cards(filtered_leads, filtered_activities, leads)

    st.divider()

    # Charts row 1
    col1, col2 = st.columns(2)

    with col1:
        render_leads_by_source_chart(filtered_leads)
        render_conversion_funnel_chart(leads)

    with col2:
        render_revenue_trend_chart(leads, start_date)
        render_activity_heatmap(filtered_activities)

    st.divider()

    # Charts row 2
    col1, col2 = st.columns(2)

    with col1:
        render_lead_velocity_chart(leads, start_date)
        render_team_performance_chart(filtered_leads)

    with col2:
        render_pipeline_aging_chart(leads)
        render_lead_score_distribution(leads)

    st.divider()

    # Detailed tables
    render_detailed_tables(leads, activities, start_date)


def render_kpi_cards(filtered_leads, filtered_activities, all_leads):
    """Render KPI metric cards."""

    # Calculate metrics
    new_leads = len(filtered_leads)
    qualified_leads = len([l for l in filtered_leads if l['stage'] in ['Qualified', 'Proposal', 'Negotiation']])
    won_deals = len([l for l in filtered_leads if l['stage'] == 'Closed Won'])
    lost_deals = len([l for l in filtered_leads if l['stage'] == 'Closed Lost'])

    won_value = sum(l['value'] for l in filtered_leads if l['stage'] == 'Closed Won')
    pipeline_value = sum(l['value'] for l in all_leads if l['stage'] not in ['Closed Won', 'Closed Lost'])

    # Activity metrics
    emails_sent = len([a for a in filtered_activities if a['type'] == 'Email Sent'])
    calls_made = len([a for a in filtered_activities if a['type'] == 'Call'])
    meetings_held = len([a for a in filtered_activities if a['type'] == 'Meeting'])

    # Conversion rate
    closed_total = won_deals + lost_deals
    conversion_rate = (won_deals / closed_total * 100) if closed_total > 0 else 0

    # Average deal size
    avg_deal_size = won_value / won_deals if won_deals > 0 else 0

    # Row 1: Lead metrics
    st.subheader("📊 Lead Metrics")
    cols = st.columns(5)
    metrics = [
        ("New Leads", new_leads, "👥"),
        ("Qualified", qualified_leads, "✅"),
        ("Won", won_deals, "🏆"),
        ("Lost", lost_deals, "❌"),
        ("Conversion", f"{conversion_rate:.1f}%", "📈")
    ]
    for i, (label, value, icon) in enumerate(metrics):
        with cols[i]:
            st.metric(label, value)

    # Row 2: Revenue & Activity metrics
    st.subheader("💰 Revenue & Activity")
    cols = st.columns(5)
    metrics = [
        ("Revenue Won", format_currency(won_value), "💵"),
        ("Pipeline Value", format_currency(pipeline_value), "📊"),
        ("Avg Deal Size", format_currency(avg_deal_size), "📏"),
        ("Emails Sent", emails_sent, "📧"),
        ("Calls Made", calls_made, "📞")
    ]
    for i, (label, value, icon) in enumerate(metrics):
        with cols[i]:
            st.metric(label, value)


def render_leads_by_source_chart(leads):
    """Render leads by source chart."""

    st.subheader("📍 Leads by Source")

    if not leads:
        st.info("No leads in selected period")
        return

    source_counts = {}
    for lead in leads:
        source = lead.get('source', 'Unknown')
        source_counts[source] = source_counts.get(source, 0) + 1

    df = pd.DataFrame(list(source_counts.items()), columns=['Source', 'Count'])
    df = df.sort_values('Count', ascending=True)

    fig = px.bar(
        df, x='Count', y='Source', orientation='h',
        color='Count', color_continuous_scale='Viridis',
        text='Count'
    )
    fig.update_traces(textposition='outside')
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#FAFAFA'),
        showlegend=False,
        margin=dict(l=0, r=0, t=20, b=0),
        height=300,
        xaxis_title="Number of Leads",
        yaxis_title=""
    )
    st.plotly_chart(fig, use_container_width=True)


def render_conversion_funnel_chart(leads):
    """Render conversion funnel."""

    st.subheader("🔄 Conversion Funnel")

    stages = ['New', 'Contacted', 'Qualified', 'Proposal', 'Negotiation', 'Closed Won']
    stage_counts = {}
    for stage in stages:
        stage_counts[stage] = len([l for l in leads if l['stage'] == stage])

    fig = go.Figure(go.Funnel(
        y=list(stage_counts.keys()),
        x=list(stage_counts.values()),
        textinfo="value+percent initial",
        marker={"color": px.colors.qualitative.Set3},
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


def render_revenue_trend_chart(leads, start_date):
    """Render revenue trend chart."""

    st.subheader("💰 Revenue Trend")

    # Group won deals by month
    won_deals = [l for l in leads if l['stage'] == 'Closed Won' and datetime.fromisoformat(l['updated_at']) >= start_date]

    if not won_deals:
        st.info("No closed deals in selected period")
        return

    # Group by month
    monthly_revenue = {}
    for deal in won_deals:
        month_key = datetime.fromisoformat(deal['updated_at']).strftime('%Y-%m')
        monthly_revenue[month_key] = monthly_revenue.get(month_key, 0) + deal['value']

    # Ensure all months in range are present
    current = start_date.replace(day=1)
    while current <= datetime.now():
        month_key = current.strftime('%Y-%m')
        if month_key not in monthly_revenue:
            monthly_revenue[month_key] = 0
        # Move to next month
        if current.month == 12:
            current = current.replace(year=current.year + 1, month=1)
        else:
            current = current.replace(month=current.month + 1)

    df = pd.DataFrame(sorted(monthly_revenue.items()), columns=['Month', 'Revenue'])
    df['Month_Label'] = pd.to_datetime(df['Month']).dt.strftime('%b %Y')

    fig = px.line(
        df, x='Month_Label', y='Revenue',
        markers=True, text='Revenue'
    )
    fig.update_traces(line_color='#00D4AA', line_width=3, texttemplate='$%{y:,.0f}', textposition='top center')
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#FAFAFA'),
        margin=dict(l=0, r=0, t=20, b=0),
        height=300,
        xaxis_title="",
        yaxis_title="Revenue ($)"
    )
    st.plotly_chart(fig, use_container_width=True)


def render_activity_heatmap(activities):
    """Render activity heatmap by day/hour."""

    st.subheader("🔥 Activity Heatmap")

    if not activities:
        st.info("No activity data")
        return

    # Create heatmap data
    days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    hours = list(range(8, 19))  # 8am - 6pm

    heatmap_data = []
    for day_idx, day in enumerate(days):
        for hour in hours:
            count = len([
                a for a in activities
                if datetime.fromisoformat(a['timestamp']).weekday() == day_idx and
                datetime.fromisoformat(a['timestamp']).hour == hour
            ])
            heatmap_data.append({'Day': day, 'Hour': f"{hour}:00", 'Count': count})

    df = pd.DataFrame(heatmap_data)
    df_pivot = df.pivot(index='Hour', columns='Day', values='Count')
    df_pivot = df_pivot[days]  # Ensure correct order

    fig = px.imshow(
        df_pivot,
        color_continuous_scale='Blues',
        aspect='auto',
        text_auto=True
    )
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#FAFAFA'),
        margin=dict(l=0, r=0, t=20, b=0),
        height=300,
        xaxis_title="Day of Week",
        yaxis_title="Hour"
    )
    st.plotly_chart(fig, use_container_width=True)


def render_lead_velocity_chart(leads, start_date):
    """Render lead velocity - new leads over time."""

    st.subheader("⚡ Lead Velocity")

    # Group new leads by week
    weekly_leads = {}
    for lead in leads:
        created = datetime.fromisoformat(lead['created_at'])
        if created >= start_date:
            week_key = created.strftime('%Y-W%U')
            weekly_leads[week_key] = weekly_leads.get(week_key, 0) + 1

    if not weekly_leads:
        st.info("No new leads in selected period")
        return

    df = pd.DataFrame(sorted(weekly_leads.items()), columns=['Week', 'New Leads'])
    df['Week_Label'] = df['Week'].apply(lambda x: f"Week {x.split('W')[1]}")

    fig = px.bar(
        df, x='Week_Label', y='New Leads',
        color='New Leads', color_continuous_scale='Viridis'
    )
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#FAFAFA'),
        margin=dict(l=0, r=0, t=20, b=0),
        height=300,
        showlegend=False,
        xaxis_title="",
        yaxis_title="New Leads"
    )
    st.plotly_chart(fig, use_container_width=True)


def render_team_performance_chart(leads):
    """Render team performance by assignee."""

    st.subheader("👥 Team Performance")

    assignee_stats = {}
    for lead in leads:
        assignee = lead.get('assigned_to', 'Unassigned')
        if assignee not in assignee_stats:
            assignee_stats[assignee] = {'total': 0, 'won': 0, 'value': 0, 'pipeline': 0}

        assignee_stats[assignee]['total'] += 1
        if lead['stage'] == 'Closed Won':
            assignee_stats[assignee]['won'] += 1
            assignee_stats[assignee]['value'] += lead['value']
        if lead['stage'] not in ['Closed Won', 'Closed Lost']:
            assignee_stats[assignee]['pipeline'] += lead['value']

    if not assignee_stats:
        st.info("No team data")
        return

    df = pd.DataFrame([
        {
            'Assignee': k,
            'Total Leads': v['total'],
            'Won': v['won'],
            'Revenue': v['value'],
            'Pipeline': v['pipeline'],
            'Win Rate': f"{(v['won']/v['total']*100):.1f}%" if v['total'] > 0 else "0%"
        }
        for k, v in assignee_stats.items()
    ])

    # Bar chart for revenue by assignee
    fig = px.bar(
        df, x='Assignee', y='Revenue',
        color='Assignee', text='Revenue'
    )
    fig.update_traces(texttemplate='$%{y:,.0f}', textposition='outside')
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#FAFAFA'),
        margin=dict(l=0, r=0, t=20, b=0),
        height=300,
        showlegend=False,
        xaxis_title="",
        yaxis_title="Revenue ($)"
    )
    st.plotly_chart(fig, use_container_width=True)

    # Table
    st.dataframe(df[['Assignee', 'Total Leads', 'Won', 'Revenue', 'Pipeline', 'Win Rate']], hide_index=True, use_container_width=True)


def render_pipeline_aging_chart(leads):
    """Render pipeline aging - how long deals stay in each stage."""

    st.subheader("⏳ Pipeline Aging")

    active_leads = [l for l in leads if l['stage'] not in ['Closed Won', 'Closed Lost']]

    if not active_leads:
        st.info("No active deals")
        return

    # Calculate days in current stage (simplified - using updated_at)
    aging_data = []
    for lead in active_leads:
        updated = datetime.fromisoformat(lead['updated_at'])
        days_in_stage = (datetime.now() - updated).days
        aging_data.append({
            'Lead': lead['name'][:20] + '...' if len(lead['name']) > 20 else lead['name'],
            'Stage': lead['stage'],
            'Value': lead['value'],
            'Days in Stage': days_in_stage,
            'Risk': '🔴 High' if days_in_stage > 30 else '🟡 Medium' if days_in_stage > 14 else '🟢 Low'
        })

    df = pd.DataFrame(aging_data)
    df = df.sort_values('Days in Stage', ascending=False)

    # Color-coded bar chart
    fig = px.bar(
        df.head(15), x='Days in Stage', y='Lead',
        color='Risk', orientation='h',
        color_discrete_map={'🔴 High': '#EF4444', '🟡 Medium': '#F59E0B', '🟢 Low': '#10B981'},
        text='Days in Stage'
    )
    fig.update_traces(textposition='outside')
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#FAFAFA'),
        margin=dict(l=0, r=0, t=20, b=0),
        height=300,
        xaxis_title="Days in Current Stage"
    )
    st.plotly_chart(fig, use_container_width=True)


def render_lead_score_distribution(leads):
    """Render lead score distribution."""

    st.subheader("🎯 Lead Score Distribution")

    from utils.helpers import generate_lead_score

    scores = [generate_lead_score(l) for l in leads]

    if not scores:
        st.info("No leads to score")
        return

    # Histogram
    fig = px.histogram(
        x=scores, nbins=20,
        labels={'x': 'Lead Score', 'y': 'Number of Leads'},
        color_discrete_sequence=['#00D4AA']
    )
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#FAFAFA'),
        margin=dict(l=0, r=0, t=20, b=0),
        height=300,
        xaxis_title="Lead Score",
        yaxis_title="Count"
    )
    # Add vertical lines for thresholds
    fig.add_vline(x=40, line_dash="dash", line_color="#F59E0B", annotation_text="Cool")
    fig.add_vline(x=60, line_dash="dash", line_color="#06B6D4", annotation_text="Warm")
    fig.add_vline(x=80, line_dash="dash", line_color="#10B981", annotation_text="Hot")

    st.plotly_chart(fig, use_container_width=True)

    # Summary stats
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Hot (≥80)", len([s for s in scores if s >= 80]))
    with col2:
        st.metric("Warm (60-79)", len([s for s in scores if 60 <= s < 80]))
    with col3:
        st.metric("Cool (40-59)", len([s for s in scores if 40 <= s < 60]))
    with col4:
        st.metric("Cold (<40)", len([s for s in scores if s < 40]))


def render_detailed_tables(leads, activities, start_date):
    """Render detailed data tables."""

    tab1, tab2, tab3 = st.tabs(["📋 All Leads", "📝 Recent Activity", "🎯 Top Opportunities"])

    with tab1:
        st.subheader("All Leads")

        if leads:
            import pandas as pd
            from utils.helpers import format_date, generate_lead_score, get_lead_score_label

            data = []
            for lead in leads:
                score = generate_lead_score(lead)
                data.append({
                    'Name': lead['name'],
                    'Company': lead.get('company', '-'),
                    'Email': lead['email'],
                    'Stage': lead['stage'],
                    'Value': lead['value'],
                    'Source': lead['source'],
                    'Assigned': lead['assigned_to'],
                    'Score': score,
                    'Grade': get_lead_score_label(score),
                    'Created': format_date(lead['created_at']),
                    'Updated': format_date(lead['updated_at'])
                })

            df = pd.DataFrame(data)
            df = df.sort_values('Score', ascending=False)

            st.dataframe(
                df,
                hide_index=True,
                use_container_width=True,
                column_config={
                    'Value': st.column_config.NumberColumn('Value', format='$%,.0f'),
                    'Score': st.column_config.ProgressColumn('Score', min_value=0, max_value=100, format='%d')
                }
            )
        else:
            st.info("No leads found")

    with tab2:
        st.subheader("Recent Activity")

        if activities:
            data = []
            for act in activities[:50]:
                data.append({
                    'Time': format_date(act['timestamp']),
                    'Type': act['type'],
                    'Description': act['description'],
                    'Lead': act.get('lead_name', '-'),
                    'User': act.get('user', '-')
                })

            df = pd.DataFrame(data)
            st.dataframe(df, hide_index=True, use_container_width=True)
        else:
            st.info("No activity recorded")

    with tab3:
        st.subheader("Top Opportunities")

        # High-value active deals
        opportunities = [
            l for l in leads
            if l['stage'] not in ['Closed Won', 'Closed Lost'] and l['value'] > 0
        ]
        opportunities.sort(key=lambda x: x['value'], reverse=True)

        if opportunities:
            data = []
            for opp in opportunities[:20]:
                from utils.helpers import generate_lead_score, get_lead_score_label, format_date
                data.append({
                    'Lead': opp['name'],
                    'Company': opp.get('company', '-'),
                    'Stage': opp['stage'],
                    'Value': opp['value'],
                    'Score': generate_lead_score(opp),
                    'Grade': get_lead_score_label(generate_lead_score(opp)),
                    'Next Follow-up': format_date(opp['next_followup']) if opp.get('next_followup') else 'Not scheduled',
                    'Assigned': opp['assigned_to']
                })

            df = pd.DataFrame(data)
            st.dataframe(
                df,
                hide_index=True,
                use_container_width=True,
                column_config={
                    'Value': st.column_config.NumberColumn('Value', format='$%,.0f'),
                    'Score': st.column_config.ProgressColumn('Score', min_value=0, max_value=100, format='%d')
                }
            )
        else:
            st.info("No active opportunities")