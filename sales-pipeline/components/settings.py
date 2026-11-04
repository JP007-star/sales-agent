"""
Settings component for Sales Agent - Configuration, integrations, and preferences.
"""

import streamlit as st
import json
from datetime import datetime
from pathlib import Path


def render_settings_tab():
    """Render the Settings tab."""

    st.header("⚙️ Settings")

    settings_tabs = st.tabs([
        "👤 Profile",
        "🔔 Notifications",
        "🔗 Integrations",
        "📊 Pipeline Stages",
        "👥 Team",
        "💾 Data Management"
    ])

    with settings_tabs[0]:
        render_profile_settings()

    with settings_tabs[1]:
        render_notification_settings()

    with settings_tabs[2]:
        render_integration_settings()

    with settings_tabs[3]:
        render_pipeline_settings()

    with settings_tabs[4]:
        render_team_settings()

    with settings_tabs[5]:
        render_data_settings()


def render_profile_settings():
    """Render profile settings."""

    st.subheader("👤 Profile Settings")

    col1, col2 = st.columns([1, 2])

    with col1:
        # Profile picture placeholder
        st.image("https://api.dicebear.com/7.x/avataaars/svg?seed=salesagent", width=150)
        if st.button("Change Photo", use_container_width=True):
            st.info("Photo upload would be implemented here")

    with col2:
        with st.form("profile_form"):
            name = st.text_input("Full Name", value="Sales Agent User", placeholder="John Doe")
            email = st.text_input("Email", value="user@company.com", placeholder="john@company.com")
            title = st.text_input("Title", value="Account Executive", placeholder="Account Executive")
            phone = st.text_input("Phone", value="+1 (555) 123-4567", placeholder="+1 (555) 123-4567")

            company = st.text_input("Company", value="Sales Agent Inc", placeholder="Company Name")
            website = st.text_input("Website", value="https://company.com", placeholder="https://company.com")

            timezone = st.selectbox("Timezone", [
                "America/New_York (EST)",
                "America/Chicago (CST)",
                "America/Denver (MST)",
                "America/Los_Angeles (PST)",
                "Europe/London (GMT)",
                "Europe/Paris (CET)",
                "Asia/Tokyo (JST)",
                "Australia/Sydney (AEST)"
            ], index=0)

            language = st.selectbox("Language", ["English", "Spanish", "French", "German", "Japanese"])

            if st.form_submit_button("Save Profile", type="primary", use_container_width=True):
                st.success("Profile saved successfully!")

    st.divider()

    # Signature
    st.subheader("✍️ Email Signature")

    with st.form("signature_form"):
        signature = st.text_area(
            "Signature",
            value="""Best regards,
Sales Agent User
Account Executive | Sales Agent Inc
📞 +1 (555) 123-4567 | 📧 user@company.com
🌐 https://company.com""",
            height=150
        )

        if st.form_submit_button("Save Signature", type="primary", use_container_width=True):
            st.success("Signature saved!")


def render_notification_settings():
    """Render notification settings."""

    st.subheader("🔔 Notification Preferences")

    st.write("**Email Notifications**")

    col1, col2 = st.columns(2)

    with col1:
        st.checkbox("New lead assigned", value=True)
        st.checkbox("Lead stage changed", value=True)
        st.checkbox("Task due today", value=True)
        st.checkbox("Task overdue", value=True)
        st.checkbox("Email opened", value=False)
        st.checkbox("Email clicked", value=False)
        st.checkbox("Email replied", value=True)

    with col2:
        st.checkbox("Meeting scheduled", value=True)
        st.checkbox("Meeting reminder (1 hour)", value=True)
        st.checkbox("Meeting reminder (1 day)", value=True)
        st.checkbox("Campaign completed", value=True)
        st.checkbox("Weekly pipeline summary", value=True)
        st.checkbox("Monthly performance report", value=True)
        st.checkbox("Deal won/lost", value=True)

    st.divider()

    st.write("**In-App Notifications**")

    col1, col2 = st.columns(2)
    with col1:
        st.checkbox("Show notification badge", value=True)
        st.checkbox("Play notification sound", value=False)
        st.checkbox("Desktop notifications", value=True)
    with col2:
        st.checkbox("Auto-mark as read", value=False)
        st.checkbox("Group similar notifications", value=True)

    st.divider()

    st.write("**Notification Frequency**")

    freq = st.radio(
        "Digest Email",
        ["Real-time", "Hourly digest", "Daily digest (8 AM)", "Weekly digest (Monday)"],
        index=2,
        horizontal=True
    )

    if st.button("Save Notification Settings", type="primary"):
        st.success("Notification settings saved!")


def render_integration_settings():
    """Render integration settings."""

    st.subheader("🔗 Integrations")

    integrations = [
        {
            'name': 'Gmail / Google Workspace',
            'description': 'Sync emails, contacts, and calendar',
            'status': 'connected',
            'icon': '📧'
        },
        {
            'name': 'Outlook / Office 365',
            'description': 'Sync emails, contacts, and calendar',
            'status': 'disconnected',
            'icon': '📧'
        },
        {
            'name': 'HubSpot CRM',
            'description': 'Two-way sync with HubSpot',
            'status': 'disconnected',
            'icon': '🔄'
        },
        {
            'name': 'Salesforce',
            'description': 'Enterprise CRM integration',
            'status': 'disconnected',
            'icon': '☁️'
        },
        {
            'name': 'LinkedIn Sales Navigator',
            'description': 'Import leads and insights',
            'status': 'disconnected',
            'icon': '💼'
        },
        {
            'name': 'Zoom',
            'description': 'Auto-create meeting links',
            'status': 'connected',
            'icon': '📹'
        },
        {
            'name': 'Calendly',
            'description': 'Schedule meetings seamlessly',
            'status': 'disconnected',
            'icon': '📅'
        },
        {
            'name': 'Slack',
            'description': 'Get notifications in Slack',
            'status': 'connected',
            'icon': '💬'
        },
        {
            'name': 'Zapier',
            'description': 'Connect 5000+ apps',
            'status': 'disconnected',
            'icon': '⚡'
        }
    ]

    for integration in integrations:
        with st.container():
            col1, col2, col3 = st.columns([1, 4, 1])

            with col1:
                st.write(f"# {integration['icon']}")

            with col2:
                st.write(f"**{integration['name']}**")
                st.caption(integration['description'])

            with col3:
                if integration['status'] == 'connected':
                    st.success("✅ Connected")
                    if st.button("Disconnect", key=f"disconnect_{integration['name']}", use_container_width=True):
                        st.warning(f"{integration['name']} disconnected")
                else:
                    st.info("⚪ Not Connected")
                    if st.button("Connect", key=f"connect_{integration['name']}", type="primary", use_container_width=True):
                        st.info(f"OAuth flow for {integration['name']} would start here")

            st.divider()

    # API Settings
    st.subheader("🔑 API Access")

    with st.expander("API Keys"):
        st.write("Generate API keys for custom integrations")

        col1, col2 = st.columns([3, 1])
        with col1:
            st.code("sk_live_abc123...xyz789", language="text")
        with col2:
            if st.button("Regenerate", use_container_width=True):
                st.success("New API key generated!")

        st.caption("⚠️ Keep your API keys secure. They provide full access to your account.")

        if st.button("Create New Key", type="primary"):
            st.info("New key creation form would appear here")


def render_pipeline_settings():
    """Render pipeline stage settings."""

    st.subheader("📊 Pipeline Stages")

    st.write("Customize your sales pipeline stages. Drag to reorder (functionality would be implemented with drag-and-drop).")

    # Default stages
    default_stages = [
        {'name': 'New', 'order': 1, 'color': '#6B7280', 'probability': 10, 'default': True},
        {'name': 'Contacted', 'order': 2, 'color': '#3B82F6', 'probability': 20, 'default': True},
        {'name': 'Qualified', 'order': 3, 'color': '#06B6D4', 'probability': 40, 'default': True},
        {'name': 'Proposal', 'order': 4, 'color': '#F59E0B', 'probability': 60, 'default': True},
        {'name': 'Negotiation', 'order': 5, 'color': '#EF4444', 'probability': 80, 'default': True},
        {'name': 'Closed Won', 'order': 6, 'color': '#10B981', 'probability': 100, 'default': True},
        {'name': 'Closed Lost', 'order': 7, 'color': '#EF4444', 'probability': 0, 'default': True}
    ]

    # Load custom stages from session state or use defaults
    if 'custom_stages' not in st.session_state:
        st.session_state.custom_stages = default_stages

    for i, stage in enumerate(st.session_state.custom_stages):
        with st.container():
            col1, col2, col3, col4, col5 = st.columns([1, 3, 1, 1, 1])

            with col1:
                st.write(f"**{stage['order']}**")

            with col2:
                new_name = st.text_input("Stage Name", value=stage['name'], key=f"stage_name_{i}", label_visibility="collapsed")
                stage['name'] = new_name

            with col3:
                new_color = st.color_picker("Color", value=stage['color'], key=f"stage_color_{i}", label_visibility="collapsed")
                stage['color'] = new_color

            with col4:
                new_prob = st.number_input("Win %", value=stage['probability'], min_value=0, max_value=100, step=5, key=f"stage_prob_{i}", label_visibility="collapsed")
                stage['probability'] = new_prob

            with col5:
                if not stage.get('default', False):
                    if st.button("🗑️", key=f"delete_stage_{i}", use_container_width=True):
                        st.session_state.custom_stages.pop(i)
                        st.rerun()
                else:
                    st.caption("Default")

            st.divider()

    # Add new stage
    with st.form("add_stage_form"):
        st.write("**Add New Stage**")
        col1, col2, col3 = st.columns([3, 1, 1])
        with col1:
            new_stage_name = st.text_input("Stage Name", placeholder="e.g., Demo Scheduled")
        with col2:
            new_stage_color = st.color_picker("Color", value="#8B5CF6")
        with col3:
            new_stage_prob = st.number_input("Win %", value=50, min_value=0, max_value=100, step=5)

        if st.form_submit_button("Add Stage", type="primary", use_container_width=True):
            if new_stage_name:
                new_order = len(st.session_state.custom_stages) + 1
                st.session_state.custom_stages.append({
                    'name': new_stage_name,
                    'order': new_order,
                    'color': new_stage_color,
                    'probability': new_stage_prob,
                    'default': False
                })
                st.success(f"Stage '{new_stage_name}' added!")
                st.rerun()

    if st.button("Save Pipeline Configuration", type="primary"):
        st.success("Pipeline configuration saved!")


def render_team_settings():
    """Render team management settings."""

    st.subheader("👥 Team Management")

    # Team members
    team_members = [
        {'name': 'Sales Agent User', 'role': 'Admin', 'email': 'user@company.com', 'status': 'Active'},
        {'name': 'Sarah Johnson', 'role': 'Manager', 'email': 'sarah@company.com', 'status': 'Active'},
        {'name': 'Mike Chen', 'role': 'Rep', 'email': 'mike@company.com', 'status': 'Active'},
        {'name': 'Emily Davis', 'role': 'Rep', 'email': 'emily@company.com', 'status': 'Invited'}
    ]

    for member in team_members:
        with st.container():
            col1, col2, col3, col4, col5 = st.columns([1, 3, 1, 1, 1])

            with col1:
                st.image(f"https://api.dicebear.com/7.x/avataaars/svg?seed={member['email']}", width=40)

            with col2:
                st.write(f"**{member['name']}**")
                st.caption(member['email'])

            with col3:
                role_options = ['Admin', 'Manager', 'Rep', 'Viewer']
                new_role = st.selectbox("Role", role_options, index=role_options.index(member['role']), key=f"role_{member['email']}", label_visibility="collapsed")

            with col4:
                status_color = "🟢" if member['status'] == 'Active' else "🟡"
                st.write(f"{status_color} {member['status']}")

            with col5:
                if member['status'] == 'Invited':
                    if st.button("Resend Invite", key=f"resend_{member['email']}", use_container_width=True):
                        st.success("Invitation resent!")
                else:
                    if st.button("Remove", key=f"remove_{member['email']}", use_container_width=True):
                        st.warning(f"{member['name']} removed")

            st.divider()

    # Invite new member
    with st.form("invite_member_form"):
        st.write("**Invite New Team Member**")

        col1, col2 = st.columns(2)
        with col1:
            invite_email = st.text_input("Email", placeholder="newmember@company.com")
            invite_name = st.text_input("Name", placeholder="Full Name")
        with col2:
            invite_role = st.selectbox("Role", ['Rep', 'Manager', 'Viewer'])
            invite_message = st.text_area("Personal Message (optional)", placeholder="Welcome to the team!")

        if st.form_submit_button("Send Invitation", type="primary", use_container_width=True):
            if invite_email and invite_name:
                st.success(f"Invitation sent to {invite_name} ({invite_email}) as {invite_role}")
            else:
                st.error("Please fill in all required fields")

    st.divider()

    # Team settings
    st.subheader("Team Settings")

    col1, col2 = st.columns(2)
    with col1:
        st.checkbox("Allow reps to see each other's leads", value=True)
        st.checkbox("Allow reps to export data", value=False)
        st.checkbox("Require 2FA for all members", value=True)
    with col2:
        st.checkbox("Auto-assign new leads", value=True)
        st.checkbox("Round-robin assignment", value=False)
        st.checkbox("Territory-based assignment", value=False)


def render_data_settings():
    """Render data management settings."""

    st.subheader("💾 Data Management")

    # Data stats
    leads_count = len(st.session_state.data_manager.get_leads())
    activities_count = len(st.session_state.data_manager.get_recent_activities(10000))
    campaigns_count = len(st.session_state.data_manager.get_campaigns())
    templates_count = len(st.session_state.data_manager.get_templates())

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Leads", leads_count)
    with col2:
        st.metric("Activities", activities_count)
    with col3:
        st.metric("Campaigns", campaigns_count)
    with col4:
        st.metric("Templates", templates_count)

    st.divider()

    # Export data
    st.write("**Export Data**")

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("📥 Export Leads (CSV)", use_container_width=True):
            export_leads_csv()

    with col2:
        if st.button("📥 Export Activities (CSV)", use_container_width=True):
            export_activities_csv()

    with col3:
        if st.button("📥 Export All Data (JSON)", use_container_width=True):
            export_all_json()

    st.divider()

    # Import data
    st.write("**Import Data**")

    uploaded_file = st.file_uploader("Upload CSV or JSON file", type=['csv', 'json'])

    if uploaded_file:
        st.info(f"File uploaded: {uploaded_file.name} ({uploaded_file.size} bytes)")

        col1, col2 = st.columns(2)
        with col1:
            import_type = st.selectbox("Import As", ["Leads", "Activities", "Campaigns"])
        with col2:
            if st.button("Import", type="primary", use_container_width=True):
                st.success(f"{import_type} imported successfully!")

    st.divider()

    # Data retention
    st.write("**Data Retention**")

    col1, col2 = st.columns(2)
    with col1:
        st.selectbox("Activity Log Retention", ["90 days", "1 year", "3 years", "7 years", "Forever"], index=1)
        st.selectbox("Email Tracking Retention", ["30 days", "90 days", "1 year", "Forever"], index=1)
    with col2:
        st.selectbox("Deleted Data Retention", ["30 days", "90 days", "1 year", "Forever"], index=0)
        st.checkbox("Anonymize deleted leads", value=True)

    st.divider()

    # Danger zone
    st.write("**⚠️ Danger Zone**")

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("🗑️ Clear All Activities", use_container_width=True, type="secondary"):
            st.error("This would delete all activity history. Confirmation required.")

    with col2:
        if st.button("🗑️ Reset Pipeline", use_container_width=True, type="secondary"):
            st.error("This would reset all leads to 'New' stage. Confirmation required.")

    with col3:
        if st.button("💥 Delete All Data", use_container_width=True, type="secondary"):
            st.error("⚠️ This would PERMANENTLY delete ALL data. Type 'DELETE' to confirm.")


def export_leads_csv():
    """Export leads as CSV."""
    import pandas as pd
    from utils.helpers import format_date

    leads = st.session_state.data_manager.get_leads()

    data = []
    for lead in leads:
        data.append({
            'ID': lead['id'],
            'Name': lead['name'],
            'Email': lead['email'],
            'Phone': lead.get('phone', ''),
            'Company': lead.get('company', ''),
            'Source': lead['source'],
            'Stage': lead['stage'],
            'Value': lead['value'],
            'Assigned To': lead['assigned_to'],
            'Tags': ', '.join(lead.get('tags', [])),
            'Notes': lead.get('notes', ''),
            'Created At': format_date(lead['created_at']),
            'Updated At': format_date(lead['updated_at']),
            'Last Contacted': format_date(lead['last_contacted']) if lead.get('last_contacted') else '',
            'Next Follow-up': format_date(lead['next_followup']) if lead.get('next_followup') else ''
        })

    df = pd.DataFrame(data)
    csv = df.to_csv(index=False)

    st.download_button(
        label="Download Leads CSV",
        data=csv,
        file_name=f"leads_export_{datetime.now().strftime('%Y%m%d')}.csv",
        mime="text/csv"
    )


def export_activities_csv():
    """Export activities as CSV."""
    import pandas as pd
    from utils.helpers import format_date

    activities = st.session_state.data_manager.get_recent_activities(10000)

    data = []
    for act in activities:
        data.append({
            'ID': act['id'],
            'Type': act['type'],
            'Description': act['description'],
            'Lead ID': act.get('lead_id', ''),
            'Lead Name': act.get('lead_name', ''),
            'User': act.get('user', ''),
            'Timestamp': format_date(act['timestamp'])
        })

    df = pd.DataFrame(data)
    csv = df.to_csv(index=False)

    st.download_button(
        label="Download Activities CSV",
        data=csv,
        file_name=f"activities_export_{datetime.now().strftime('%Y%m%d')}.csv",
        mime="text/csv"
    )


def export_all_json():
    """Export all data as JSON."""

    data = {
        'leads': st.session_state.data_manager.get_leads(),
        'activities': st.session_state.data_manager.get_recent_activities(10000),
        'campaigns': st.session_state.data_manager.get_campaigns(),
        'templates': st.session_state.data_manager.get_templates(),
        'exported_at': datetime.now().isoformat(),
        'version': '1.0'
    }

    json_str = json.dumps(data, indent=2, default=str)

    st.download_button(
        label="Download All Data (JSON)",
        data=json_str,
        file_name=f"sales_agent_export_{datetime.now().strftime('%Y%m%d')}.json",
        mime="application/json"
    )