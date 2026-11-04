"""
Pipeline visualization component for Sales Agent.
Kanban-style board with drag-and-drop simulation.
"""

import streamlit as st
from utils.helpers import format_currency, get_stage_color, generate_lead_score, get_lead_score_label


def render_pipeline_tab():
    """Render the Pipeline Kanban board."""

    st.header("📊 Sales Pipeline")

    # Pipeline summary metrics
    leads = st.session_state.data_manager.get_leads()
    pipeline_data = st.session_state.data_manager.get_pipeline_by_stage()

    # Summary row
    cols = st.columns(len(pipeline_data) + 1)
    with cols[0]:
        total_value = sum(p['value'] for p in pipeline_data if p['stage'] not in ['Closed Won', 'Closed Lost'])
        st.metric("Total Pipeline", format_currency(total_value))

    for i, stage_data in enumerate(pipeline_data):
        if stage_data['stage'] not in ['Closed Won', 'Closed Lost']:
            with cols[i + 1]:
                st.metric(
                    stage_data['stage'],
                    format_currency(stage_data['value']),
                    delta=f"{stage_data['count']} deals"
                )

    st.divider()

    # Kanban Board
    stages = [
        ("New", "🆕"),
        ("Contacted", "📞"),
        ("Qualified", "✅"),
        ("Proposal", "📄"),
        ("Negotiation", "🤝"),
        ("Closed Won", "🏆"),
        ("Closed Lost", "❌")
    ]

    # Create columns for each stage
    kanban_cols = st.columns(len(stages))

    for idx, (stage_name, stage_icon) in enumerate(stages):
        with kanban_cols[idx]:
            render_pipeline_column(stage_name, stage_icon, leads)

    st.divider()

    # Pipeline insights
    render_pipeline_insights(pipeline_data)


def render_pipeline_column(stage_name: str, stage_icon: str, all_leads: list):
    """Render a single pipeline column."""

    # Filter leads for this stage
    stage_leads = [l for l in all_leads if l['stage'] == stage_name]
    stage_color = get_stage_color(stage_name)

    # Column header
    st.markdown(f"""
    <div style="
        background: {stage_color}20;
        border: 1px solid {stage_color}40;
        border-radius: 8px;
        padding: 12px;
        margin-bottom: 8px;
        text-align: center;
    ">
        <h4 style="margin: 0; color: {stage_color};">
            {stage_icon} {stage_name}
        </h4>
        <p style="margin: 4px 0 0; font-size: 0.85rem; color: #888;">
            {len(stage_leads)} deals • {format_currency(sum(l['value'] for l in stage_leads))}
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Lead cards
    if stage_leads:
        # Sort by value descending
        stage_leads.sort(key=lambda x: x['value'], reverse=True)

        for lead in stage_leads:
            render_lead_card(lead, stage_name, stage_color)
    else:
        # Drop zone indicator
        st.markdown(f"""
        <div style="
            border: 2px dashed {stage_color}40;
            border-radius: 8px;
            padding: 20px;
            text-align: center;
            color: #666;
            font-size: 0.85rem;
            min-height: 100px;
        ">
            Drop leads here
        </div>
        """, unsafe_allow_html=True)

    # Add lead button for this stage
    if st.button(f"➕ Add to {stage_name}", key=f"add_to_{stage_name}", use_container_width=True):
        st.session_state.show_lead_modal = True
        st.session_state.prefill_stage = stage_name
        st.rerun()


def render_lead_card(lead: dict, current_stage: str, stage_color: str):
    """Render a single lead card in the pipeline."""

    score = generate_lead_score(lead)
    score_label = get_lead_score_label(score)

    # Card container
    with st.container():
        # Card header with name and value
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f"**{lead['name']}**")
            if lead.get('company'):
                st.caption(f"🏢 {lead['company']}")
        with col2:
            st.markdown(f"<span style='color: {stage_color}; font-weight: 600;'>{format_currency(lead['value'])}</span>", unsafe_allow_html=True)

        # Lead info
        st.caption(f"📧 {lead['email']}")
        if lead.get('phone'):
            st.caption(f"📞 {lead['phone']}")

        # Score badge
        score_color = "#10B981" if score >= 60 else "#F59E0B" if score >= 40 else "#EF4444"
        st.markdown(f"""
        <span style="
            background: {score_color}20;
            color: {score_color};
            padding: 2px 8px;
            border-radius: 12px;
            font-size: 0.7rem;
            font-weight: 600;
        ">
            Score: {score} {score_label}
        </span>
        """, unsafe_allow_html=True)

        # Assigned to
        st.caption(f"👤 {lead['assigned_to']}")

        # Action buttons
        btn_col1, btn_col2 = st.columns(2)

        with btn_col1:
            if st.button("👁️ View", key=f"view_{lead['id']}", use_container_width=True):
                st.session_state.selected_lead_id = lead['id']
                st.rerun()

        with btn_col2:
            # Move to next/previous stage
            stages = ["New", "Contacted", "Qualified", "Proposal", "Negotiation", "Closed Won", "Closed Lost"]
            current_idx = stages.index(current_stage) if current_stage in stages else 0

            if current_idx < len(stages) - 1:
                next_stage = stages[current_idx + 1]
                if st.button(f"➡️ {next_stage[:3]}", key=f"move_{lead['id']}", use_container_width=True):
                    st.session_state.data_manager.update_lead(lead['id'], {'stage': next_stage})
                    st.success(f"Moved {lead['name']} to {next_stage}")
                    st.rerun()

        st.divider()


def render_pipeline_insights(pipeline_data: list):
    """Render pipeline insights and analytics."""

    st.subheader("📈 Pipeline Insights")

    col1, col2 = st.columns(2)

    with col1:
        # Stage conversion funnel
        st.write("**Stage Conversion Funnel**")

        funnel_data = [p for p in pipeline_data if p['stage'] not in ['Closed Won', 'Closed Lost']]
        if funnel_data:
            import plotly.graph_objects as go

            fig = go.Figure(go.Funnel(
                y=[p['stage'] for p in funnel_data],
                x=[p['count'] for p in funnel_data],
                textinfo="value+percent initial",
                marker={"color": [get_stage_color(p['stage']) for p in funnel_data]},
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
        else:
            st.info("No pipeline data for funnel")

    with col2:
        # Pipeline velocity metrics
        st.write("**Pipeline Velocity**")

        # Calculate average days in each stage (simplified)
        leads = st.session_state.data_manager.get_leads()
        active_leads = [l for l in leads if l['stage'] not in ['Closed Won', 'Closed Lost']]

        if active_leads:
            avg_value = sum(l['value'] for l in active_leads) / len(active_leads)
            total_value = sum(l['value'] for l in active_leads)

            st.metric("Active Deals", len(active_leads))
            st.metric("Total Pipeline Value", format_currency(total_value))
            st.metric("Average Deal Size", format_currency(avg_value))

            # Estimated close rate
            won_leads = [l for l in leads if l['stage'] == 'Closed Won']
            lost_leads = [l for l in leads if l['stage'] == 'Closed Lost']
            closed_total = len(won_leads) + len(lost_leads)

            if closed_total > 0:
                win_rate = len(won_leads) / closed_total * 100
                st.metric("Historical Win Rate", f"{win_rate:.1f}%")

                # Weighted pipeline
                weighted = total_value * (win_rate / 100)
                st.metric("Weighted Pipeline", format_currency(weighted))
        else:
            st.info("No active deals in pipeline")

    # Stage aging analysis
    st.divider()
    st.write("**Stage Aging Analysis**")

    aging_data = []
    for stage_data in pipeline_data:
        if stage_data['stage'] not in ['Closed Won', 'Closed Lost']:
            stage_leads = [l for l in leads if l['stage'] == stage_data['stage']]
            if stage_leads:
                avg_days = 0  # Simplified - would calculate from created/updated dates
                aging_data.append({
                    'Stage': stage_data['stage'],
                    'Deals': stage_data['count'],
                    'Value': format_currency(stage_data['value']),
                    'Avg Days': f"{avg_days}d",
                    'Risk': "🔴 High" if avg_days > 30 else "🟡 Medium" if avg_days > 14 else "🟢 Low"
                })

    if aging_data:
        import pandas as pd
        df = pd.DataFrame(aging_data)
        st.dataframe(df, hide_index=True, use_container_width=True)
    else:
        st.info("No aging data available")


def render_pipeline_list_view():
    """Alternative list view for pipeline."""

    st.subheader("📋 Pipeline List View")

    leads = st.session_state.data_manager.get_leads()
    active_leads = [l for l in leads if l['stage'] not in ['Closed Won', 'Closed Lost']]

    if not active_leads:
        st.info("No active deals in pipeline")
        return

    # Sort by stage order then value
    stage_order = {
        'New': 0, 'Contacted': 1, 'Qualified': 2, 'Proposal': 3,
        'Negotiation': 4, 'Closed Won': 5, 'Closed Lost': 6
    }
    active_leads.sort(key=lambda x: (stage_order.get(x['stage'], 99), -x['value']))

    # Display as table
    import pandas as pd
    from utils.helpers import format_date

    data = []
    for lead in active_leads:
        data.append({
            'Name': lead['name'],
            'Company': lead.get('company', '-'),
            'Stage': lead['stage'],
            'Value': format_currency(lead['value']),
            'Source': lead['source'],
            'Assigned': lead['assigned_to'],
            'Last Update': format_date(lead['updated_at']),
            'Next Action': format_date(lead['next_followup']) if lead.get('next_followup') else 'Not scheduled'
        })

    df = pd.DataFrame(data)
    st.dataframe(df, hide_index=True, use_container_width=True)