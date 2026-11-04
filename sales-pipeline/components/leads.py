"""
Leads management component for Sales Agent.
"""

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from utils.helpers import (
    format_currency, format_date, get_stage_color, get_lead_score_label,
    generate_lead_score, validate_email, truncate_text
)


def render_leads_tab():
    """Render the Leads management tab."""

    st.header("👥 Leads Management")

    # Action bar
    col1, col2, col3, col4 = st.columns([2, 1, 1, 1])

    with col1:
        search = st.text_input("🔍 Search leads...", placeholder="Name, email, company...", key="leads_search")

    with col2:
        stage_filter = st.selectbox("Stage", ["All"] + [
            "New", "Contacted", "Qualified", "Proposal",
            "Negotiation", "Closed Won", "Closed Lost"
        ], key="leads_stage_filter")

    with col3:
        source_filter = st.selectbox("Source", ["All"] + [
            "Website", "Referral", "Cold Call", "Email Campaign",
            "Social Media", "Event", "Partner", "Other"
        ], key="leads_source_filter")

    with col4:
        if st.button("➕ Add Lead", type="primary", use_container_width=True, key="leads_add_btn"):
            st.session_state.show_lead_modal = True
            st.rerun()

    # Get and filter leads
    leads = st.session_state.data_manager.get_leads()

    # Apply filters
    filtered_leads = leads
    if search:
        search_lower = search.lower()
        filtered_leads = [
            l for l in filtered_leads
            if search_lower in l['name'].lower() or
               search_lower in l['email'].lower() or
               search_lower in l.get('company', '').lower()
        ]
    if stage_filter != "All":
        filtered_leads = [l for l in filtered_leads if l['stage'] == stage_filter]
    if source_filter != "All":
        filtered_leads = [l for l in filtered_leads if l['source'] == source_filter]

    # Sort by stage order then by updated date
    stage_order = {
        'New': 0, 'Contacted': 1, 'Qualified': 2, 'Proposal': 3,
        'Negotiation': 4, 'Closed Won': 5, 'Closed Lost': 6
    }
    filtered_leads.sort(key=lambda x: (stage_order.get(x['stage'], 99), -datetime.fromisoformat(x['updated_at']).timestamp()))

    st.caption(f"Showing {len(filtered_leads)} of {len(leads)} leads")

    # Display leads as cards
    if filtered_leads:
        render_leads_cards(filtered_leads)
    else:
        st.info("No leads found matching your criteria. Click 'Add Lead' to create your first lead!")

    # Lead detail modal
    if st.session_state.get('selected_lead_id'):
        render_lead_detail_modal(st.session_state.selected_lead_id)

    # Add lead modal
    if st.session_state.get('show_lead_modal', False):
        render_add_lead_modal()


def render_leads_cards(leads: list):
    """Render leads as cards in a grid."""

    # Display as table for better usability
    st.subheader("Leads List")

    # Prepare data for dataframe
    leads_data = []
    for lead in leads:
        score = generate_lead_score(lead)
        leads_data.append({
            'Name': lead['name'],
            'Company': lead.get('company', '-'),
            'Email': lead['email'],
            'Stage': lead['stage'],
            'Value': format_currency(lead['value']),
            'Source': lead['source'],
            'Assigned': lead['assigned_to'],
            'Score': f"{score} {get_lead_score_label(score)}",
            'Last Contact': format_date(lead['last_contacted']) if lead.get('last_contacted') else 'Never',
            'Next Follow-up': format_date(lead['next_followup']) if lead.get('next_followup') else 'Not scheduled',
            'ID': lead['id']
        })

    df = pd.DataFrame(leads_data)

    # Configure column display
    column_config = {
        'Name': st.column_config.TextColumn('Name', width='medium'),
        'Company': st.column_config.TextColumn('Company', width='medium'),
        'Email': st.column_config.TextColumn('Email', width='medium'),
        'Stage': st.column_config.SelectboxColumn(
            'Stage',
            options=["New", "Contacted", "Qualified", "Proposal", "Negotiation", "Closed Won", "Closed Lost"],
            width='medium'
        ),
        'Value': st.column_config.TextColumn('Value', width='small'),
        'Source': st.column_config.TextColumn('Source', width='small'),
        'Assigned': st.column_config.TextColumn('Assigned To', width='small'),
        'Score': st.column_config.TextColumn('Score', width='medium'),
        'Last Contact': st.column_config.TextColumn('Last Contact', width='small'),
        'Next Follow-up': st.column_config.TextColumn('Next Follow-up', width='small'),
        'ID': st.column_config.TextColumn('ID', width='small')
    }

    # Display editable dataframe
    edited_df = st.data_editor(
        df,
        column_config=column_config,
        hide_index=True,
        use_container_width=True,
        disabled=['ID'],
        key="leads_editor"
    )

    # Handle stage changes
    if not edited_df.equals(df):
        for idx, row in edited_df.iterrows():
            original = df.iloc[idx]
            if row['Stage'] != original['Stage']:
                lead_id = row['ID']
                st.session_state.data_manager.update_lead(lead_id, {'stage': row['Stage']})
                st.success(f"Updated {row['Name']} to {row['Stage']}")
                st.rerun()

    # Bulk actions
    st.divider()
    st.subheader("Bulk Actions")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        if st.button("📧 Email Selected", use_container_width=True):
            st.info("Email composer would open here")

    with col2:
        if st.button("📞 Call Selected", use_container_width=True):
            st.info("Call logger would open here")

    with col3:
        if st.button("🏷️ Tag Selected", use_container_width=True):
            st.info("Tagging interface would open here")

    with col4:
        if st.button("🗑️ Delete Selected", use_container_width=True):
            st.warning("Delete confirmation would appear here")


def render_lead_detail_modal(lead_id: str):
    """Render detailed view of a lead in a modal-like container."""

    lead = st.session_state.data_manager.get_lead(lead_id)
    if not lead:
        st.session_state.selected_lead_id = None
        return

    with st.container():
        st.markdown("---")
        st.subheader(f"📋 Lead Details: {lead['name']}")

        # Close button
        if st.button("✕ Close", key="close_lead_detail"):
            st.session_state.selected_lead_id = None
            st.rerun()

        # Main info row
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Stage", lead['stage'])
            st.caption(f"Source: {lead['source']}")

        with col2:
            st.metric("Value", format_currency(lead['value']))
            st.caption(f"Assigned: {lead['assigned_to']}")

        with col3:
            score = generate_lead_score(lead)
            st.metric("Lead Score", f"{score}/100")
            st.caption(get_lead_score_label(score))

        with col4:
            st.metric("Created", format_date(lead['created_at']))
            st.caption(f"Updated: {format_date(lead['updated_at'])}")

        # Contact info
        col1, col2 = st.columns(2)
        with col1:
            st.write("**Contact Information**")
            st.write(f"📧 {lead['email']}")
            if lead.get('phone'):
                st.write(f"📞 {lead['phone']}")
            if lead.get('company'):
                st.write(f"🏢 {lead['company']}")

        with col2:
            st.write("**Timeline**")
            if lead.get('last_contacted'):
                st.write(f"Last contact: {format_date(lead['last_contacted'])}")
            if lead.get('next_followup'):
                st.write(f"Next follow-up: {format_date(lead['next_followup'])}")

        # Notes
        if lead.get('notes'):
            st.write("**Notes**")
            st.write(lead['notes'])

        # Tags
        if lead.get('tags'):
            st.write("**Tags**")
            tags_html = " ".join([f'<span style="background: #00D4AA20; color: #00D4AA; padding: 2px 8px; border-radius: 12px; font-size: 0.75rem; margin-right: 4px;">{tag}</span>' for tag in lead['tags']])
            st.markdown(tags_html, unsafe_allow_html=True)

        st.divider()

        # Actions
        st.write("**Actions**")
        action_cols = st.columns(5)

        with action_cols[0]:
            new_stage = st.selectbox(
                "Change Stage",
                ["New", "Contacted", "Qualified", "Proposal", "Negotiation", "Closed Won", "Closed Lost"],
                index=["New", "Contacted", "Qualified", "Proposal", "Negotiation", "Closed Won", "Closed Lost"].index(lead['stage']),
                key=f"stage_change_{lead_id}"
            )
            if new_stage != lead['stage']:
                if st.button("Update Stage", key=f"update_stage_{lead_id}"):
                    st.session_state.data_manager.update_lead(lead_id, {'stage': new_stage})
                    st.success(f"Stage updated to {new_stage}")
                    st.rerun()

        with action_cols[1]:
            if st.button("📧 Send Email", key=f"email_{lead_id}", use_container_width=True):
                st.session_state.current_page = "Outreach"
                st.session_state.preselect_lead = lead_id
                st.rerun()

        with action_cols[2]:
            if st.button("📞 Log Call", key=f"call_{lead_id}", use_container_width=True):
                st.session_state.show_call_modal = True
                st.session_state.call_lead_id = lead_id
                st.rerun()

        with action_cols[3]:
            if st.button("➕ Add Task", key=f"task_{lead_id}", use_container_width=True):
                st.session_state.show_task_modal = True
                st.session_state.task_lead_id = lead_id
                st.rerun()

        with action_cols[4]:
            if st.button("🗑️ Delete", key=f"delete_{lead_id}", type="secondary", use_container_width=True):
                st.session_state.confirm_delete_lead = lead_id
                st.rerun()

        # Delete confirmation
        if st.session_state.get('confirm_delete_lead') == lead_id:
            st.error("⚠️ Are you sure you want to delete this lead? This action cannot be undone.")
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Yes, Delete", type="primary", key=f"confirm_delete_yes_{lead_id}"):
                    st.session_state.data_manager.delete_lead(lead_id)
                    st.session_state.selected_lead_id = None
                    st.session_state.confirm_delete_lead = None
                    st.success("Lead deleted")
                    st.rerun()
            with col2:
                if st.button("Cancel", key=f"confirm_delete_no_{lead_id}"):
                    st.session_state.confirm_delete_lead = None
                    st.rerun()

        st.divider()

        # Activity history
        st.write("**Activity History**")
        activities = st.session_state.data_manager.get_lead_activities(lead_id)
        if activities:
            for act in activities[:20]:
                from utils.helpers import get_relative_time
                cols = st.columns([1, 4, 1])
                with cols[0]:
                    st.caption(get_relative_time(act['timestamp']))
                with cols[1]:
                    st.write(f"**{act['type']}** - {act['description']}")
                with cols[2]:
                    st.caption(act['user'])
        else:
            st.info("No activity recorded for this lead yet.")

        # Tasks for this lead
        st.write("**Tasks**")
        tasks = st.session_state.data_manager.get_tasks(lead_id)
        if tasks:
            for task in tasks:
                from utils.helpers import get_priority_icon, is_overdue, format_date
                cols = st.columns([1, 4, 1, 1])
                with cols[0]:
                    st.write(get_priority_icon(task['priority']))
                with cols[1]:
                    st.write(f"**{task['title']}**")
                    if task.get('description'):
                        st.caption(task['description'])
                with cols[2]:
                    due_color = "🔴" if is_overdue(task['due_date']) and not task['completed'] else "🟢"
                    st.caption(f"{due_color} {format_date(task['due_date'])}")
                with cols[3]:
                    if not task['completed']:
                        if st.button("✓", key=f"complete_task_{task['id']}"):
                            st.session_state.data_manager.complete_task(task['id'])
                            st.rerun()
                    else:
                        st.caption("✅ Done")
        else:
            st.info("No tasks for this lead.")


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

        tags = st.text_input("Tags (comma-separated)", placeholder="enterprise, decision-maker, urgent")
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
            errors = []
            if not name:
                errors.append("Name is required")
            if not email:
                errors.append("Email is required")
            elif not validate_email(email):
                errors.append("Invalid email format")

            if errors:
                for error in errors:
                    st.error(error)
            else:
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
                    'tags': [t.strip() for t in tags.split(',') if t.strip()],
                    'created_at': datetime.now().isoformat(),
                    'updated_at': datetime.now().isoformat()
                }
                st.session_state.data_manager.add_lead(lead_data)
                st.session_state.show_lead_modal = False
                st.success(f"Lead '{name}' created successfully!")
                st.rerun()