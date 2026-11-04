"""
Approval Queue component for JP Finds Deals.
"""

import streamlit as st
from datetime import datetime
from utils.helpers import format_date, get_relative_time


def render_approval_queue():
    """Render the Approval Queue tab."""

    st.header("✅ Approval Queue")

    approval_queue = st.session_state.get('approval_queue', [])
    published_posts = st.session_state.get('published_posts', [])

    # Tabs for different queues
    queue_tabs = st.tabs(["⏳ Pending Review", "✅ Approved", "📤 Published", "❌ Rejected"])

    with queue_tabs[0]:
        render_pending_queue(approval_queue)

    with queue_tabs[1]:
        render_approved_queue(approval_queue)

    with queue_tabs[2]:
        render_published_posts(published_posts)

    with queue_tabs[3]:
        render_rejected_queue(approval_queue)


def render_pending_queue(approval_queue):
    """Render pending approval items."""

    pending_items = [item for item in approval_queue if item.get('status') == 'pending']

    st.subheader(f"⏳ Pending Review ({len(pending_items)})")

    if not pending_items:
        st.info("No items pending approval. Great job! 🎉")
        return

    for item in pending_items:
        render_approval_card(item, 'pending')


def render_approved_queue(approval_queue):
    """Render approved items ready for publishing."""

    approved_items = [item for item in approval_queue if item.get('status') == 'approved']

    st.subheader(f"✅ Approved & Ready to Publish ({len(approved_items)})")

    if not approved_items:
        st.info("No approved items ready for publishing.")
        return

    for item in approved_items:
        render_approval_card(item, 'approved')


def render_approval_card(item, queue_type):
    """Render an approval queue card."""

    content = item.get('generated_content', {})
    scripts = content.get('scripts', {})
    seo = content.get('seo', {})
    video_prompts = content.get('video_prompts', {})

    with st.container():
        # Header
        col1, col2, col3 = st.columns([3, 1, 1])

        with col1:
            st.write(f"**{item.get('product_name', 'Unknown Product')}**")
            st.caption(f"{item.get('content_type', 'Reel')} • {format_date(item.get('created_at', ''))}")

        with col2:
            if queue_type == 'pending':
                st.markdown("""
                <span style="background: #F59E0B20; color: #F59E0B; padding: 4px 12px; border-radius: 16px; font-size: 0.75rem; font-weight: 600;">
                    ⏳ Pending
                </span>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <span style="background: #10B98120; color: #10B981; padding: 4px 12px; border-radius: 16px; font-size: 0.75rem; font-weight: 600;">
                    ✅ Approved
                </span>
                """, unsafe_allow_html=True)

        with col3:
            if st.button("👁️ Preview", key=f"preview_{item['id']}", use_container_width=True):
                st.session_state.preview_item = item
                st.rerun()

        # Content preview (collapsible)
        with st.expander("📝 View Content"):
            # Scripts
            for lang, script in scripts.items():
                st.write(f"**{lang} Script**")
                st.write(f"🎯 **Hook:** {script.get('hook', 'N/A')}")
                st.write(f"📦 **Intro:** {script.get('introduction', 'N/A')[:100]}...")
                st.write(f"✨ **Benefits:** {script.get('benefits', 'N/A')[:100]}...")
                st.write(f"👆 **CTA:** {script.get('cta', 'N/A')}")
                st.divider()

            # Caption & Hashtags
            st.write("**📱 Instagram Caption**")
            st.write(seo.get('caption', 'No caption generated'))

            hashtags = seo.get('hashtags', [])
            if hashtags:
                st.write("**#️⃣ Hashtags**")
                tags_html = " ".join([f'<span style="background: #3B82F620; color: #3B82F6; padding: 2px 6px; border-radius: 8px; font-size: 0.7rem; margin-right: 4px;">#{tag}</span>' for tag in hashtags[:15]])
                st.markdown(tags_html, unsafe_allow_html=True)
                if len(hashtags) > 15:
                    st.caption(f"+ {len(hashtags) - 15} more hashtags")

            # Video prompts summary
            if video_prompts:
                st.write("**🎬 Video Prompts**")
                scenes = ['hook_visual', 'product_intro', 'benefits_demo', 'cta_visual']
                for scene in scenes:
                    prompt = video_prompts.get(scene, '')
                    if prompt:
                        st.caption(f"• {scene.replace('_', ' ').title()}: {prompt[:80]}...")

        # Actions
        st.write("**Actions**")
        action_cols = st.columns(4)

        with action_cols[0]:
            if queue_type == 'pending':
                if st.button("✅ Approve", key=f"approve_{item['id']}", type="primary", use_container_width=True):
                    approve_item(item['id'])
                    st.success("Approved! Moved to publishing queue.")
                    st.rerun()
            else:
                if st.button("📤 Publish Now", key=f"publish_{item['id']}", type="primary", use_container_width=True):
                    publish_to_instagram(item)
                    st.rerun()

        with action_cols[1]:
            if queue_type == 'pending':
                if st.button("✏️ Edit", key=f"edit_approval_{item['id']}", use_container_width=True):
                    # Send back to content studio
                    draft = {
                        'id': f"draft_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                        'product_id': item['product_id'],
                        'product_name': item['product_name'],
                        'content_type': item['content_type'],
                        'generated_content': content,
                        'created_at': datetime.now().isoformat(),
                        'status': 'draft'
                    }
                    if 'content_drafts' not in st.session_state:
                        st.session_state.content_drafts = []
                    st.session_state.content_drafts.append(draft)
                    st.session_state.current_draft = draft
                    st.session_state.current_page = "Content Studio"
                    st.rerun()
            else:
                if st.button("📅 Schedule", key=f"schedule_{item['id']}", use_container_width=True):
                    st.session_state.scheduling_item = item
                    st.rerun()

        with action_cols[2]:
            if st.button("📥 Export", key=f"export_approval_{item['id']}", use_container_width=True):
                export_approval_package(item)

        with action_cols[3]:
            if queue_type == 'pending':
                if st.button("❌ Reject", key=f"reject_{item['id']}", type="secondary", use_container_width=True):
                    reject_item(item['id'])
                    st.warning("Item rejected.")
                    st.rerun()
            else:
                if st.button("↩️ Send Back", key=f"sendback_{item['id']}", type="secondary", use_container_width=True):
                    send_back_to_pending(item['id'])
                    st.info("Sent back for revision.")
                    st.rerun()

        # Scheduling modal
        if st.session_state.get('scheduling_item') and st.session_state.scheduling_item.get('id') == item['id']:
            render_scheduling_modal(item)

        st.divider()


def render_published_posts(published_posts):
    """Render published posts with performance."""

    st.subheader(f"📤 Published Posts ({len(published_posts)})")

    if not published_posts:
        st.info("No posts published yet.")
        return

    # Sort by publish date descending
    published_posts.sort(key=lambda x: x.get('published_at', ''), reverse=True)

    for post in published_posts:
        with st.container():
            col1, col2, col3, col4, col5 = st.columns([2, 1, 1, 1, 1])

            with col1:
                st.write(f"**{post.get('product_name', 'Unknown')}**")
                st.caption(f"Published: {format_date(post.get('published_at', ''))}")
                if post.get('instagram_url'):
                    st.link_button("🔗 View on Instagram", post['instagram_url'])

            with col2:
                st.metric("Views", post.get('views', 0))
                st.metric("Likes", post.get('likes', 0))

            with col3:
                st.metric("Comments", post.get('comments', 0))
                st.metric("Shares", post.get('shares', 0))

            with col4:
                st.metric("Saves", post.get('saves', 0))
                st.metric("Clicks", post.get('affiliate_clicks', 0))

            with col5:
                st.metric("Commission", f"₹{post.get('commission', 0):,.0f}")
                if post.get('conversions', 0) > 0:
                    st.caption(f"{post['conversions']} conversions")

            st.divider()


def render_rejected_queue(approval_queue):
    """Render rejected items."""

    rejected_items = [item for item in approval_queue if item.get('status') == 'rejected']

    st.subheader(f"❌ Rejected ({len(rejected_items)})")

    if not rejected_items:
        st.info("No rejected items.")
        return

    for item in rejected_items:
        with st.container():
            col1, col2, col3 = st.columns([3, 1, 1])

            with col1:
                st.write(f"**{item.get('product_name', 'Unknown')}**")
                st.caption(f"Rejected: {format_date(item.get('updated_at', ''))}")
                if item.get('rejection_reason'):
                    st.caption(f"Reason: {item['rejection_reason']}")

            with col2:
                if st.button("♻️ Restore", key=f"restore_{item['id']}", use_container_width=True):
                    restore_item(item['id'])
                    st.success("Restored to pending!")
                    st.rerun()

            with col3:
                if st.button("🗑️ Delete", key=f"del_rejected_{item['id']}", use_container_width=True):
                    delete_item(item['id'])
                    st.success("Permanently deleted!")
                    st.rerun()

            st.divider()


def approve_item(item_id):
    """Approve an item."""
    approval_queue = st.session_state.get('approval_queue', [])
    for item in approval_queue:
        if item['id'] == item_id:
            item['status'] = 'approved'
            item['updated_at'] = datetime.now().isoformat()
            break


def reject_item(item_id):
    """Reject an item."""
    approval_queue = st.session_state.get('approval_queue', [])
    for item in approval_queue:
        if item['id'] == item_id:
            item['status'] = 'rejected'
            item['updated_at'] = datetime.now().isoformat()
            item['rejection_reason'] = "Rejected by user"
            break


def send_back_to_pending(item_id):
    """Send approved item back to pending."""
    approval_queue = st.session_state.get('approval_queue', [])
    for item in approval_queue:
        if item['id'] == item_id:
            item['status'] = 'pending'
            item['updated_at'] = datetime.now().isoformat()
            break


def restore_item(item_id):
    """Restore rejected item to pending."""
    approval_queue = st.session_state.get('approval_queue', [])
    for item in approval_queue:
        if item['id'] == item_id:
            item['status'] = 'pending'
            item['updated_at'] = datetime.now().isoformat()
            item.pop('rejection_reason', None)
            break


def delete_item(item_id):
    """Permanently delete an item."""
    approval_queue = st.session_state.get('approval_queue', [])
    st.session_state.approval_queue = [item for item in approval_queue if item['id'] != item_id]


def publish_to_instagram(item):
    """Publish approved item to Instagram (simulated)."""

    # In real implementation, this would call Instagram Graph API
    # For now, simulate publishing

    published_post = {
        'id': f"post_{datetime.now().strftime('%Y%m%d%H%M%S')}",
        'approval_id': item['id'],
        'product_id': item['product_id'],
        'product_name': item['product_name'],
        'content_type': item['content_type'],
        'caption': item['generated_content'].get('seo', {}).get('caption', ''),
        'hashtags': item['generated_content'].get('seo', {}).get('hashtags', []),
        'instagram_media_id': f"media_{datetime.now().strftime('%Y%m%d%H%M%S')}",
        'instagram_url': f"https://instagram.com/reel/{datetime.now().strftime('%Y%m%d%H%M%S')}",
        'published_at': datetime.now().isoformat(),
        'views': 0,
        'likes': 0,
        'comments': 0,
        'shares': 0,
        'saves': 0,
        'affiliate_clicks': 0,
        'conversions': 0,
        'commission': 0
    }

    if 'published_posts' not in st.session_state:
        st.session_state.published_posts = []
    st.session_state.published_posts.append(published_post)

    # Update approval status
    item['status'] = 'published'
    item['published_at'] = datetime.now().isoformat()
    item['instagram_media_id'] = published_post['instagram_media_id']

    st.success(f"Published to Instagram! 🎉\nMedia ID: {published_post['instagram_media_id']}")


def render_scheduling_modal(item):
    """Render scheduling modal."""

    with st.form(f"schedule_form_{item['id']}"):
        st.subheader("📅 Schedule Post")

        col1, col2 = st.columns(2)
        with col1:
            schedule_date = st.date_input("Date", key=f"sched_date_{item['id']}")
        with col2:
            schedule_time = st.time_input("Time (IST)", key=f"sched_time_{item['id']}")

        # Recurring option
        recurring = st.checkbox("Recurring", key=f"sched_recurring_{item['id']}")
        if recurring:
            frequency = st.selectbox("Frequency", ["Daily", "Weekly", "Monthly"], key=f"sched_freq_{item['id']}")

        col1, col2 = st.columns(2)
        with col1:
            if st.form_submit_button("Schedule", type="primary", use_container_width=True):
                item['status'] = 'scheduled'
                item['scheduled_at'] = datetime.combine(schedule_date, schedule_time).isoformat()
                item['recurring'] = recurring
                if recurring:
                    item['frequency'] = frequency
                st.success(f"Scheduled for {schedule_date} at {schedule_time} IST")
                st.session_state.scheduling_item = None
                st.rerun()
        with col2:
            if st.form_submit_button("Cancel", use_container_width=True):
                st.session_state.scheduling_item = None
                st.rerun()


def export_approval_package(item):
    """Export approval package for manual publishing."""
    import json

    package = {
        'product': {
            'name': item['product_name'],
            'id': item['product_id']
        },
        'content': item['generated_content'],
        'instagram_ready': {
            'caption': item['generated_content'].get('seo', {}).get('caption', ''),
            'hashtags': item['generated_content'].get('seo', {}).get('hashtags', []),
            'disclosure': item['generated_content'].get('seo', {}).get('disclosure', '#ad #affiliate')
        },
        'video_prompts': item['generated_content'].get('video_prompts', {}),
        'exported_at': datetime.now().isoformat()
    }

    json_str = json.dumps(package, indent=2, default=str)

    st.download_button(
        label="Download Package",
        data=json_str,
        file_name=f"publish_package_{item['product_name']}_{datetime.now().strftime('%Y%m%d')}.json",
        mime="application/json",
        key=f"download_pkg_{item['id']}"
    )