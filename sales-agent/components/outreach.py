"""
Outreach component for Sales Agent - Email campaigns, templates, and sequencing.
"""

import streamlit as st
from datetime import datetime
from utils.helpers import format_date, parse_email_variables, validate_email


def render_outreach_tab():
    """Render the Outreach tab with campaigns, templates, and composer."""

    st.header("📧 Outreach Center")

    # Tabs for different outreach functions
    outreach_tabs = st.tabs(["📝 Composer", "📋 Campaigns", "📚 Templates", "📊 Analytics"])

    with outreach_tabs[0]:
        render_email_composer()

    with outreach_tabs[1]:
        render_campaigns()

    with outreach_tabs[2]:
        render_templates()

    with outreach_tabs[3]:
        render_outreach_analytics()


def render_email_composer():
    """Render the email composer interface."""

    st.subheader("✍️ Compose Email")

    # Recipient selection
    col1, col2 = st.columns([2, 1])

    with col1:
        # Get leads for recipient dropdown
        leads = st.session_state.data_manager.get_leads()
        lead_options = {f"{l['name']} ({l['email']})": l['id'] for l in leads}

        # Check for preselected lead
        default_index = 0
        if st.session_state.get('preselect_lead'):
            preselected = st.session_state.preselect_lead
            for i, (label, lid) in enumerate(lead_options.items()):
                if lid == preselected:
                    default_index = i
                    break
            st.session_state.preselect_lead = None

        recipient_label = st.selectbox(
            "To (Lead)",
            options=list(lead_options.keys()),
            index=default_index,
            key="email_recipient"
        )
        recipient_id = lead_options.get(recipient_label)
        recipient = st.session_state.data_manager.get_lead(recipient_id) if recipient_id else None

    with col2:
        # Template selection
        templates = st.session_state.data_manager.get_templates()
        template_options = {"Custom / Blank": None}
        template_options.update({t['name']: t['id'] for t in templates})

        selected_template_name = st.selectbox(
            "Template",
            options=list(template_options.keys()),
            key="email_template"
        )
        template_id = template_options[selected_template_name]

    # Load template if selected
    if template_id and 'email_subject' not in st.session_state:
        template = next((t for t in templates if t['id'] == template_id), None)
        if template:
            st.session_state.email_subject = template['subject']
            st.session_state.email_body = template['body']

    # Email form
    with st.form("email_composer_form"):
        # Subject line
        subject = st.text_input(
            "Subject",
            value=st.session_state.get('email_subject', ''),
            placeholder="Subject line...",
            key="email_subject_input"
        )

        # Body
        body = st.text_area(
            "Body",
            value=st.session_state.get('email_body', ''),
            height=300,
            placeholder="Write your email here... Use {name}, {company}, {sender_name} for personalization.",
            key="email_body_input"
        )

        # Preview variables
        if recipient:
            with st.expander("🔍 Preview Variables"):
                variables = {
                    'name': recipient['name'],
                    'company': recipient.get('company', ''),
                    'sender_name': 'Sales Agent User',
                    'sender_email': 'user@company.com',
                    'sender_title': 'Account Executive'
                }
                for key, value in variables.items():
                    st.caption(f"{{{key}}} → {value or '(empty)'}")

        # Send options
        col1, col2, col3 = st.columns(3)
        with col1:
            send_now = st.form_submit_button("📤 Send Now", type="primary", use_container_width=True)
        with col2:
            schedule = st.form_submit_button("⏰ Schedule", use_container_width=True)
        with col3:
            save_draft = st.form_submit_button("💾 Save Draft", use_container_width=True)

        if send_now or schedule or save_draft:
            if not recipient:
                st.error("Please select a recipient")
            elif not subject:
                st.error("Subject is required")
            elif not body:
                st.error("Body is required")
            else:
                # Parse variables
                variables = {
                    'name': recipient['name'],
                    'company': recipient.get('company', ''),
                    'sender_name': 'Sales Agent User',
                    'sender_email': 'user@company.com',
                    'sender_title': 'Account Executive'
                }

                parsed_subject = parse_email_variables(subject, variables)
                parsed_body = parse_email_variables(body, variables)

                # Log activity
                st.session_state.data_manager.add_activity({
                    'type': 'Email Sent' if send_now else 'Email Scheduled' if schedule else 'Draft Saved',
                    'description': f"Email to {recipient['name']}: {parsed_subject}",
                    'lead_id': recipient['id'],
                    'lead_name': recipient['name']
                })

                # Add task for follow-up if sending
                if send_now:
                    st.session_state.data_manager.add_task({
                        'title': f"Follow up on email: {parsed_subject}",
                        'description': f"Follow up with {recipient['name']} regarding sent email",
                        'lead_id': recipient['id'],
                        'lead_name': recipient['name'],
                        'due_date': (datetime.now() + timedelta(days=3)).isoformat(),
                        'priority': 'Medium',
                        'type': 'Email'
                    })

                action = "sent" if send_now else "scheduled" if schedule else "saved as draft"
                st.success(f"Email {action} successfully!")

                # Clear form state
                if 'email_subject' in st.session_state:
                    del st.session_state.email_subject
                if 'email_body' in st.session_state:
                    del st.session_state.email_body
                st.rerun()


def render_campaigns():
    """Render campaign management."""

    st.subheader("📋 Email Campaigns")

    # Action buttons
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        search = st.text_input("🔍 Search campaigns...", key="campaign_search")
    with col2:
        if st.button("➕ New Campaign", type="primary", use_container_width=True, key="new_campaign_btn"):
            st.session_state.show_campaign_modal = True
            st.rerun()
    with col3:
        st.caption(f"{len(st.session_state.data_manager.get_campaigns())} campaigns")

    campaigns = st.session_state.data_manager.get_campaigns()

    if campaigns:
        for campaign in campaigns:
            render_campaign_card(campaign)
    else:
        st.info("No campaigns yet. Create your first campaign!")

    # Campaign modal
    if st.session_state.get('show_campaign_modal', False):
        render_campaign_modal()


def render_campaign_card(campaign: dict):
    """Render a campaign card."""

    status_colors = {
        'Draft': '#6B7280',
        'Scheduled': '#3B82F6',
        'Sending': '#F59E0B',
        'Sent': '#10B981',
        'Paused': '#EF4444'
    }
    status_color = status_colors.get(campaign['status'], '#6B7280')

    with st.container():
        col1, col2, col3, col4 = st.columns([3, 1, 1, 1])

        with col1:
            st.markdown(f"**{campaign['name']}**")
            st.caption(f"Subject: {campaign['subject'][:60]}..." if len(campaign['subject']) > 60 else f"Subject: {campaign['subject']}")

        with col2:
            st.markdown(f"""
            <span style="
                background: {status_color}20;
                color: {status_color};
                padding: 4px 12px;
                border-radius: 16px;
                font-size: 0.75rem;
                font-weight: 600;
            ">
                {campaign['status']}
            </span>
            """, unsafe_allow_html=True)

        with col3:
            if campaign['sent_count'] > 0:
                open_rate = (campaign['open_count'] / campaign['sent_count'] * 100) if campaign['sent_count'] > 0 else 0
                st.metric("Open Rate", f"{open_rate:.1f}%")
            else:
                st.metric("Recipients", len(campaign.get('recipients', [])))

        with col4:
            if st.button("👁️ View", key=f"view_campaign_{campaign['id']}", use_container_width=True):
                st.session_state.selected_campaign = campaign['id']
                st.rerun()

        # Progress bar for sent campaigns
        if campaign['status'] in ['Sending', 'Sent'] and campaign.get('recipients'):
            progress = campaign['sent_count'] / len(campaign['recipients']) if campaign['recipients'] else 0
            st.progress(progress, text=f"Sent: {campaign['sent_count']}/{len(campaign['recipients'])}")

        st.divider()


def render_campaign_modal():
    """Render modal for creating/editing a campaign."""

    with st.form("campaign_form", clear_on_submit=True):
        st.subheader("Create New Campaign")

        name = st.text_input("Campaign Name*", placeholder="Q4 Enterprise Outreach")

        # Template selection
        templates = st.session_state.data_manager.get_templates()
        template_options = {"Custom": None}
        template_options.update({t['name']: t['id'] for t in templates})

        selected_template = st.selectbox("Email Template", options=list(template_options.keys()))
        template_id = template_options[selected_template]

        # Load template preview
        if template_id:
            template = next((t for t in templates if t['id'] == template_id), None)
            if template:
                st.text_input("Subject", value=template['subject'], disabled=True, key="campaign_subject_preview")
                st.text_area("Body Preview", value=template['body'][:200] + "...", disabled=True, height=100, key="campaign_body_preview")
        else:
            subject = st.text_input("Subject*", placeholder="Subject line...")
            body = st.text_area("Body*", height=200, placeholder="Email body with {name}, {company} variables...")

        # Recipient selection
        st.write("**Recipients**")
        leads = st.session_state.data_manager.get_leads()

        # Filter options
        col1, col2 = st.columns(2)
        with col1:
            stage_filter = st.multiselect("Filter by Stage",
                ["New", "Contacted", "Qualified", "Proposal", "Negotiation"],
                default=["New", "Contacted", "Qualified"])
        with col2:
            max_recipients = st.number_input("Max Recipients", min_value=1, max_value=1000, value=50)

        # Show filtered leads
        filtered_leads = [l for l in leads if l['stage'] in stage_filter][:max_recipients]
        st.caption(f"{len(filtered_leads)} leads match criteria")

        with st.expander("View Recipients"):
            for lead in filtered_leads:
                st.caption(f"• {lead['name']} ({lead['email']}) - {lead['company']}")

        # Schedule options
        st.write("**Schedule**")
        send_now = st.checkbox("Send immediately", value=True)

        if not send_now:
            scheduled_date = st.date_input("Schedule Date")
            scheduled_time = st.time_input("Schedule Time")

        col1, col2 = st.columns(2)
        with col1:
            submitted = st.form_submit_button("Create Campaign", type="primary", use_container_width=True)
        with col2:
            cancelled = st.form_submit_button("Cancel", use_container_width=True)

        if cancelled:
            st.session_state.show_campaign_modal = False
            st.rerun()

        if submitted:
            if not name:
                st.error("Campaign name is required")
            else:
                campaign_data = {
                    'name': name,
                    'subject': template['subject'] if template_id else subject,
                    'body': template['body'] if template_id else body,
                    'recipients': [l['id'] for l in filtered_leads],
                    'status': 'Draft'
                }
                st.session_state.data_manager.add_campaign(campaign_data)
                st.session_state.show_campaign_modal = False
                st.success(f"Campaign '{name}' created with {len(filtered_leads)} recipients!")
                st.rerun()


def render_templates():
    """Render email template management."""

    st.subheader("📚 Email Templates")

    col1, col2 = st.columns([3, 1])
    with col1:
        search = st.text_input("🔍 Search templates...", key="template_search")
    with col2:
        if st.button("➕ New Template", type="primary", use_container_width=True, key="new_template_btn"):
            st.session_state.show_template_modal = True
            st.rerun()

    templates = st.session_state.data_manager.get_templates()

    # Filter by category
    categories = list(set(t.get('category', 'General') for t in templates))
    selected_category = st.selectbox("Category", ["All"] + categories, key="template_category")

    filtered_templates = templates
    if selected_category != "All":
        filtered_templates = [t for t in templates if t.get('category', 'General') == selected_category]

    if search:
        filtered_templates = [t for t in filtered_templates if search.lower() in t['name'].lower() or search.lower() in t['subject'].lower()]

    if filtered_templates:
        for template in filtered_templates:
            render_template_card(template)
    else:
        st.info("No templates found. Create your first template!")

    # Template modal
    if st.session_state.get('show_template_modal', False):
        render_template_modal()


def render_template_card(template: dict):
    """Render a template card."""

    category_colors = {
        'Cold Outreach': '#3B82F6',
        'Follow-up': '#F59E0B',
        'Proposal': '#8B5CF6',
        'Referral': '#06B6D4',
        'Meeting': '#10B981',
        'General': '#6B7280'
    }
    cat_color = category_colors.get(template.get('category', 'General'), '#6B7280')

    with st.container():
        col1, col2, col3 = st.columns([3, 1, 1])

        with col1:
            st.markdown(f"**{template['name']}**")
            st.caption(f"Subject: {template['subject']}")

        with col2:
            st.markdown(f"""
            <span style="
                background: {cat_color}20;
                color: {cat_color};
                padding: 2px 8px;
                border-radius: 12px;
                font-size: 0.7rem;
                font-weight: 600;
            ">
                {template.get('category', 'General')}
            </span>
            """, unsafe_allow_html=True)

        with col3:
            btn_col1, btn_col2 = st.columns(2)
            with btn_col1:
                if st.button("📝 Use", key=f"use_tpl_{template['id']}", use_container_width=True):
                    st.session_state.email_subject = template['subject']
                    st.session_state.email_body = template['body']
                    st.session_state.current_page = "Outreach"
                    # Switch to composer tab would need session state
                    st.success("Template loaded in composer!")
                    st.rerun()
            with btn_col2:
                if st.button("✏️ Edit", key=f"edit_tpl_{template['id']}", use_container_width=True):
                    st.session_state.editing_template = template['id']
                    st.session_state.show_template_modal = True
                    st.rerun()

        # Preview
        with st.expander("Preview"):
            st.text(template['body'][:500] + ("..." if len(template['body']) > 500 else ""))

        st.divider()


def render_template_modal():
    """Render modal for creating/editing a template."""

    editing_id = st.session_state.get('editing_template')
    template = None
    if editing_id:
        template = next((t for t in st.session_state.data_manager.get_templates() if t['id'] == editing_id), None)

    with st.form("template_form", clear_on_submit=True):
        st.subheader("Edit Template" if editing_id else "Create New Template")

        name = st.text_input("Template Name*", value=template['name'] if template else "", placeholder="Initial Cold Outreach")
        category = st.selectbox("Category*", [
            "Cold Outreach", "Follow-up", "Proposal", "Referral", "Meeting", "General"
        ], index=["Cold Outreach", "Follow-up", "Proposal", "Referral", "Meeting", "General"].index(template.get('category', 'General')) if template else 0)

        subject = st.text_input("Subject*", value=template['subject'] if template else "", placeholder="Quick question for {company}")
        body = st.text_area("Body*", value=template['body'] if template else "", height=300,
                           placeholder="Hi {name},\n\nI noticed {company}...\n\nBest,\n{sender_name}")

        # Variable helper
        with st.expander("Available Variables"):
            st.markdown("""
            - `{name}` - Lead's full name
            - `{company}` - Lead's company
            - `{sender_name}` - Your name
            - `{sender_email}` - Your email
            - `{sender_title}` - Your title
            """)

        col1, col2 = st.columns(2)
        with col1:
            submitted = st.form_submit_button("Save Template", type="primary", use_container_width=True)
        with col2:
            cancelled = st.form_submit_button("Cancel", use_container_width=True)

        if cancelled:
            st.session_state.show_template_modal = False
            st.session_state.editing_template = None
            st.rerun()

        if submitted:
            if not name or not subject or not body:
                st.error("All fields are required")
            else:
                template_data = {
                    'name': name,
                    'category': category,
                    'subject': subject,
                    'body': body
                }

                if editing_id:
                    st.session_state.data_manager.update_template(editing_id, template_data)
                    st.success(f"Template '{name}' updated!")
                else:
                    st.session_state.data_manager.add_template(template_data)
                    st.success(f"Template '{name}' created!")

                st.session_state.show_template_modal = False
                st.session_state.editing_template = None
                st.rerun()


def render_outreach_analytics():
    """Render outreach analytics."""

    st.subheader("📊 Outreach Analytics")

    campaigns = st.session_state.data_manager.get_campaigns()
    activities = st.session_state.data_manager.get_recent_activities(100)

    # Email activities
    email_activities = [a for a in activities if a['type'] in ['Email Sent', 'Email Scheduled']]

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Emails Sent (30d)", len([a for a in email_activities if a['type'] == 'Email Sent']))

    with col2:
        total_sent = sum(c['sent_count'] for c in campaigns)
        st.metric("Total Campaign Sends", total_sent)

    with col3:
        total_opens = sum(c['open_count'] for c in campaigns)
        avg_open_rate = (total_opens / total_sent * 100) if total_sent > 0 else 0
        st.metric("Avg Open Rate", f"{avg_open_rate:.1f}%")

    with col4:
        total_replies = sum(c['reply_count'] for c in campaigns)
        avg_reply_rate = (total_replies / total_sent * 100) if total_sent > 0 else 0
        st.metric("Avg Reply Rate", f"{avg_reply_rate:.1f}%")

    st.divider()

    # Campaign performance table
    if campaigns:
        st.write("**Campaign Performance**")

        import pandas as pd

        data = []
        for c in campaigns:
            open_rate = (c['open_count'] / c['sent_count'] * 100) if c['sent_count'] > 0 else 0
            click_rate = (c['click_count'] / c['sent_count'] * 100) if c['sent_count'] > 0 else 0
            reply_rate = (c['reply_count'] / c['sent_count'] * 100) if c['sent_count'] > 0 else 0

            data.append({
                'Campaign': c['name'],
                'Status': c['status'],
                'Sent': c['sent_count'],
                'Opens': c['open_count'],
                'Open Rate': f"{open_rate:.1f}%",
                'Clicks': c['click_count'],
                'Click Rate': f"{click_rate:.1f}%",
                'Replies': c['reply_count'],
                'Reply Rate': f"{reply_rate:.1f}%"
            })

        df = pd.DataFrame(data)
        st.dataframe(df, hide_index=True, use_container_width=True)
    else:
        st.info("No campaign data available yet.")

# Need to import timedelta for the composer
from datetime import timedelta