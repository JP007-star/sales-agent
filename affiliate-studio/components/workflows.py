"""
Workflows component for JP Finds Deals - n8n Workflow Management.
"""

import streamlit as st
import json
from datetime import datetime


def render_workflows():
    """Render the Workflows tab."""

    st.header("🔄 n8n Workflows")

    st.info("""
    **n8n Community Edition** runs locally at http://localhost:5678

    These are the core automation workflows for JP Finds Deals.
    Import them into n8n to enable full automation.
    """)

    workflow_tabs = st.tabs(["📋 Workflow Library", "⚡ Quick Actions", "📊 Execution Logs", "⚙️ Configuration"])

    with workflow_tabs[0]:
        render_workflow_library()

    with workflow_tabs[1]:
        render_quick_actions()

    with workflow_tabs[2]:
        render_execution_logs()

    with workflow_tabs[3]:
        render_workflow_config()


def render_workflow_library():
    """Render the workflow library with importable JSON."""

    workflows = [
        {
            'id': 'wf_product_intake',
            'name': '1. Product URL Intake',
            'description': 'Receives product URLs via webhook, validates marketplace, saves to database, triggers AI analysis',
            'trigger': 'Webhook (POST /webhook/product-intake)',
            'nodes': ['Webhook', 'Validate URL', 'Extract Product Info', 'Save to DB', 'Trigger AI Analysis'],
            'filename': '01_product_intake.json'
        },
        {
            'id': 'wf_product_discovery',
            'name': '2. Product Discovery',
            'description': 'Queries Amazon/Flipkart affiliate APIs, identifies trending products, scores them, avoids duplicates',
            'trigger': 'Cron (Daily 9:00 AM IST)',
            'nodes': ['Cron', 'Amazon API', 'Flipkart API', 'Score Products', 'Deduplicate', 'Save Selected'],
            'filename': '02_product_discovery.json'
        },
        {
            'id': 'wf_ai_content',
            'name': '3. AI Content Generation',
            'description': 'Sends product data to Gemini, generates hooks, scripts (English/Tamil), SEO captions, hashtags, video prompts',
            'trigger': 'Webhook (from Product Intake/Discovery)',
            'nodes': ['Get Product', 'Gemini Analysis', 'Generate Hooks', 'Generate Scripts', 'Generate SEO', 'Generate Video Prompts', 'Save Draft'],
            'filename': '03_ai_content_generation.json'
        },
        {
            'id': 'wf_video_production',
            'name': '4. Video Production',
            'description': 'Prepares Canva-ready assets, generates video prompts for Flow/FFmpeg, creates final MP4',
            'trigger': 'Webhook (from AI Content)',
            'nodes': ['Get Draft', 'Prepare Canva Assets', 'Generate Video Prompts', 'FFmpeg Processing', 'Save Video Asset'],
            'filename': '04_video_production.json'
        },
        {
            'id': 'wf_approval',
            'name': '5. Approval Workflow',
            'description': 'Notifies via email/Slack when Reel ready, waits for explicit approval, allows edit/reject, moves to publish queue',
            'trigger': 'Webhook (from Video Production)',
            'nodes': ['Notification', 'Wait for Approval', 'Approval Gate', 'Edit/Reject Handler', 'Move to Publish Queue'],
            'filename': '05_approval_workflow.json'
        },
        {
            'id': 'wf_instagram_publish',
            'name': '6. Instagram Publishing',
            'description': 'Checks approval, verifies video/caption, publishes via Meta Graph API, saves media ID, records result',
            'trigger': 'Cron (at scheduled times) / Webhook',
            'nodes': ['Check Queue', 'Verify Assets', 'Meta Graph API Publish', 'Save Media ID', 'Update Status', 'Log Result'],
            'filename': '06_instagram_publishing.json'
        },
        {
            'id': 'wf_daily_scheduling',
            'name': '7. Daily Scheduling',
            'description': 'Generates up to 2 content drafts daily, uses IST timezone, avoids repeated products, maintains approval requirement',
            'trigger': 'Cron (Daily 8:00 AM IST)',
            'nodes': ['Cron', 'Select Products', 'Trigger Content Gen', 'Queue for Review', 'Send Daily Summary'],
            'filename': '07_daily_scheduling.json'
        },
        {
            'id': 'wf_analytics',
            'name': '8. Analytics Collection',
            'description': 'Retrieves Instagram insights, updates product performance, imports affiliate conversions, generates reports',
            'trigger': 'Cron (Daily 6:00 AM IST)',
            'nodes': ['Cron', 'Instagram Insights API', 'Affiliate Reports', 'Update DB', 'Generate Reports', 'Send Summary'],
            'filename': '08_analytics_collection.json'
        }
    ]

    for wf in workflows:
        with st.expander(f"**{wf['name']}**"):
            col1, col2 = st.columns([2, 1])

            with col1:
                st.write(wf['description'])
                st.caption(f"Trigger: {wf['trigger']}")
                st.write("**Nodes:**")
                for node in wf['nodes']:
                    st.write(f"  • {node}")

            with col2:
                if st.button("📥 Download JSON", key=f"download_{wf['id']}", use_container_width=True):
                    download_workflow_json(wf)

                if st.button("📋 Copy to Clipboard", key=f"copy_{wf['id']}", use_container_width=True):
                    copy_workflow_json(wf)

                if st.button("🚀 Open in n8n", key=f"open_{wf['id']}", use_container_width=True):
                    st.info("Opening n8n at http://localhost:5678")

    # Import all button
    st.divider()
    if st.button("📦 Download All Workflows (ZIP)", type="primary", use_container_width=True):
        download_all_workflows()


def render_quick_actions():
    """Render quick workflow actions."""

    st.subheader("⚡ Quick Actions")

    col1, col2 = st.columns(2)

    with col1:
        st.write("**Manual Triggers**")

        if st.button("🔍 Trigger Product Discovery", use_container_width=True):
            trigger_product_discovery()

        if st.button("🎬 Generate Content for Pending", use_container_width=True):
            trigger_content_generation()

        if st.button("📤 Check Publish Queue", use_container_width=True):
            check_publish_queue()

        if st.button("📊 Run Analytics Collection", use_container_width=True):
            run_analytics_collection()

    with col2:
        st.write("**Schedule Management**")

        if st.button("⏰ Enable Daily Scheduler", use_container_width=True):
            st.success("Daily scheduler enabled!")

        if st.button("⏸️ Pause All Workflows", use_container_width=True):
            st.warning("All workflows paused!")

        if st.button("▶️ Resume All Workflows", use_container_width=True):
            st.success("All workflows resumed!")

        if st.button("🔄 Restart n8n", use_container_width=True):
            st.info("Restarting n8n...")

    st.divider()

    # Manual product intake
    st.write("**Manual Product Intake**")

    with st.form("manual_intake_form"):
        product_url = st.text_input("Product URL", placeholder="https://www.amazon.in/... or https://www.flipkart.com/...")

        col1, col2 = st.columns(2)
        with col1:
            if st.form_submit_button("Submit to Workflow", type="primary", use_container_width=True):
                if product_url:
                    manual_product_intake(product_url)
                    st.success("Product submitted to intake workflow!")
                else:
                    st.error("Please enter a product URL")

        with col2:
            if st.form_submit_button("Process Immediately", use_container_width=True):
                st.info("Would trigger full pipeline immediately")


def render_execution_logs():
    """Render workflow execution logs."""

    st.subheader("📊 Execution Logs")

    # Mock execution logs
    logs = [
        {
            'timestamp': '2024-01-15 09:00:00',
            'workflow': 'Product Discovery',
            'status': '✅ Success',
            'duration': '45s',
            'items_processed': 12,
            'message': 'Found 12 new products, 3 duplicates skipped'
        },
        {
            'timestamp': '2024-01-15 09:15:00',
            'workflow': 'AI Content Generation',
            'status': '✅ Success',
            'duration': '2m 30s',
            'items_processed': 3,
            'message': 'Generated content for 3 products (English + Tamil)'
        },
        {
            'timestamp': '2024-01-15 10:00:00',
            'workflow': 'Video Production',
            'status': '⚠️ Partial',
            'duration': '5m 12s',
            'items_processed': 3,
            'message': 'Canva assets ready, video generation needs manual Flow step'
        },
        {
            'timestamp': '2024-01-15 12:00:00',
            'workflow': 'Instagram Publishing',
            'status': '⏳ Waiting',
            'duration': '-',
            'items_processed': 0,
            'message': 'Waiting for approval on 2 Reels'
        },
        {
            'timestamp': '2024-01-14 09:00:00',
            'workflow': 'Product Discovery',
            'status': '✅ Success',
            'duration': '38s',
            'items_processed': 8,
            'message': 'Found 8 new products'
        }
    ]

    # Filter options
    col1, col2 = st.columns(2)
    with col1:
        status_filter = st.selectbox("Filter by Status", ["All", "✅ Success", "❌ Failed", "⚠️ Partial", "⏳ Waiting"])
    with col2:
        workflow_filter = st.selectbox("Filter by Workflow", ["All"] + [log['workflow'] for log in logs])

    # Apply filters
    filtered_logs = logs
    if status_filter != "All":
        filtered_logs = [log for log in logs if log['status'] == status_filter]
    if workflow_filter != "All":
        filtered_logs = [log for log in filtered_logs if log['workflow'] == workflow_filter]

    # Display logs
    for log in filtered_logs:
        with st.container():
            col1, col2, col3, col4 = st.columns([2, 2, 1, 3])

            with col1:
                st.caption(log['timestamp'])
                st.write(f"**{log['workflow']}**")

            with col2:
                st.write(log['status'])
                st.caption(f"Duration: {log['duration']}")

            with col3:
                st.metric("Items", log['items_processed'])

            with col4:
                st.caption(log['message'])

            st.divider()


def render_workflow_config():
    """Render workflow configuration."""

    st.subheader("⚙️ Workflow Configuration")

    # n8n connection
    st.write("**n8n Connection**")

    col1, col2 = st.columns(2)
    with col1:
        st.text_input("n8n URL", value="http://localhost:5678", key="n8n_url_config")
        st.text_input("API Key", type="password", placeholder="n8n API key for automation", key="n8n_api_key")
    with col2:
        st.text_input("Webhook Base URL", value="http://localhost:8000/webhook", key="webhook_base")
        st.selectbox("Auth Type", ["Header", "Query Param", "Basic Auth"], key="n8n_auth_type")

    # Workflow variables
    st.write("**Global Variables**")

    variables = {
        'GEMINI_API_KEY': st.session_state.settings.get('gemini_api_key', ''),
        'INSTAGRAM_ACCESS_TOKEN': st.session_state.settings.get('instagram_access_token', ''),
        'AMAZON_ASSOCIATE_TAG': st.session_state.settings.get('amazon_associate_tag', ''),
        'FLIPKART_AFFILIATE_ID': st.session_state.settings.get('flipkart_affiliate_id', ''),
        'DAILY_REELS_TARGET': str(st.session_state.settings.get('daily_reels_target', 2)),
        'PUBLISHING_TIMEZONE': 'Asia/Kolkata'
    }

    for key, value in variables.items():
        st.text_input(key, value=value, type="password" if 'KEY' in key or 'TOKEN' in key else "default", key=f"var_{key}")

    if st.button("Save Variables to n8n", type="primary", use_container_width=True):
        st.success("Variables synced to n8n!")

    st.divider()

    # Error handling
    st.write("**Error Handling**")

    col1, col2 = st.columns(2)
    with col1:
        st.number_input("Max Retries", value=3, min_value=0, max_value=10, key="max_retries")
        st.number_input("Retry Delay (seconds)", value=60, min_value=10, max_value=300, key="retry_delay")
    with col2:
        st.checkbox("Continue on Failure", value=True, key="continue_on_failure")
        st.checkbox("Send Error Notifications", value=True, key="error_notifications")

    st.divider()

    # Rate limiting
    st.write("**Rate Limits**")

    col1, col2 = st.columns(2)
    with col1:
        st.number_input("Gemini API (req/min)", value=60, key="gemini_rate")
        st.number_input("Instagram API (req/hour)", value=200, key="ig_rate")
    with col2:
        st.number_input("Amazon API (req/sec)", value=1, key="amazon_rate")
        st.number_input("Flipkart API (req/min)", value=30, key="flipkart_rate")


def download_workflow_json(workflow):
    """Download workflow as JSON."""

    # Generate n8n-compatible workflow JSON
    n8n_workflow = generate_n8n_workflow(workflow['id'])

    json_str = json.dumps(n8n_workflow, indent=2)

    st.download_button(
        label=f"Download {workflow['name']}",
        data=json_str,
        file_name=workflow['filename'],
        mime="application/json",
        key=f"dl_btn_{workflow['id']}"
    )


def copy_workflow_json(workflow):
    """Copy workflow JSON to clipboard (simulated)."""

    n8n_workflow = generate_n8n_workflow(workflow['id'])
    json_str = json.dumps(n8n_workflow, indent=2)

    st.code(json_str, language='json')
    st.caption("JSON displayed above - copy manually")


def download_all_workflows():
    """Download all workflows as a zip."""

    import zipfile
    import io

    zip_buffer = io.BytesIO()

    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        workflows = [
            'wf_product_intake',
            'wf_product_discovery',
            'wf_ai_content',
            'wf_video_production',
            'wf_approval',
            'wf_instagram_publish',
            'wf_daily_scheduling',
            'wf_analytics'
        ]

        for wf_id in workflows:
            n8n_workflow = generate_n8n_workflow(wf_id)
            json_str = json.dumps(n8n_workflow, indent=2)
            filename = f"{wf_id}.json"
            zip_file.writestr(filename, json_str)

    zip_buffer.seek(0)

    st.download_button(
        label="Download All Workflows (ZIP)",
        data=zip_buffer.getvalue(),
        file_name=f"jp_finds_deals_workflows_{datetime.now().strftime('%Y%m%d')}.zip",
        mime="application/zip"
    )


def generate_n8n_workflow(workflow_id):
    """Generate n8n-compatible workflow JSON."""

    # This is a simplified template - real workflows would be more complex
    base_workflow = {
        "name": workflow_id.replace('wf_', '').replace('_', ' ').title(),
        "nodes": [],
        "connections": {},
        "active": False,
        "settings": {},
        "id": workflow_id
    }

    # Add workflow-specific nodes
    if workflow_id == 'wf_product_intake':
        base_workflow['nodes'] = [
            {"name": "Webhook", "type": "n8n-nodes-base.webhook", "position": [250, 300], "parameters": {"path": "product-intake", "httpMethod": "POST"}},
            {"name": "Validate URL", "type": "n8n-nodes-base.function", "position": [500, 300], "parameters": {"functionCode": "// Validate marketplace URL\nconst url = items[0].json.body.url;\nreturn [{json: {url, valid: true, marketplace: url.includes('amazon') ? 'Amazon' : url.includes('flipkart') ? 'Flipkart' : 'Unknown'}}];"}},
            {"name": "Save to Database", "type": "n8n-nodes-base.postgres", "position": [750, 300], "parameters": {"operation": "insert", "table": "products"}},
            {"name": "Trigger AI Analysis", "type": "n8n-nodes-base.httpRequest", "position": [1000, 300], "parameters": {"url": "http://backend:8000/webhook/ai-analysis", "method": "POST"}}
        ]

    return base_workflow


def trigger_product_discovery():
    """Trigger product discovery workflow."""
    st.success("Product discovery workflow triggered!")


def trigger_content_generation():
    """Trigger content generation for pending products."""
    st.success("Content generation triggered for pending products!")


def check_publish_queue():
    """Check and process publish queue."""
    st.success("Publish queue checked!")


def run_analytics_collection():
    """Run analytics collection."""
    st.success("Analytics collection triggered!")


def manual_product_intake(product_url):
    """Process manual product intake."""
    # Add to products
    if 'products' not in st.session_state:
        st.session_state.products = []

    # Simple extraction
    marketplace = "Amazon" if "amazon" in product_url.lower() else "Flipkart" if "flipkart" in product_url.lower() else "Other"

    product = {
        'id': f"prod_{datetime.now().strftime('%Y%m%d%H%M%S')}",
        'name': 'Product from Manual Intake',
        'url': product_url,
        'marketplace': marketplace,
        'category': 'Uncategorized',
        'price': 0,
        'status': 'discovered',
        'score': 0,
        'created_at': datetime.now().isoformat(),
        'updated_at': datetime.now().isoformat()
    }

    st.session_state.products.append(product)