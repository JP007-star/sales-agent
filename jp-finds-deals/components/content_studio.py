"""
Content Studio component for JP Finds Deals - AI Content Generation.
"""

import streamlit as st
import json
from datetime import datetime
from utils.helpers import format_date
from utils.gemini_client import generate_content, parse_gemini_content_response as parse_gemini_response


def render_content_studio():
    """Render the Content Studio tab."""

    st.header("✍️ Content Studio")

    products = st.session_state.get('products', [])
    content_drafts = st.session_state.get('content_drafts', [])

    if not products:
        st.warning("No products available. Please add products first in Product Manager.")
        if st.button("📦 Go to Product Manager", type="primary"):
            st.session_state.current_page = "Product Manager"
            st.rerun()
        return

    # Tabs for different content functions
    content_tabs = st.tabs(["🎯 Generate Content", "📝 Manage Drafts", "🎬 Video Prompts", "📋 Templates"])

    with content_tabs[0]:
        render_content_generator(products)

    with content_tabs[1]:
        render_drafts_manager(content_drafts)

    with content_tabs[2]:
        render_video_prompts(content_drafts)

    with content_tabs[3]:
        render_templates()


def render_content_generator(products):
    """Render the AI content generator."""

    st.subheader("🤖 AI Content Generation")

    # Product selection
    col1, col2 = st.columns([2, 1])

    with col1:
        product_options = {f"{p['name']} ({p['marketplace']})": p['id'] for p in products}

        # Check for preselected product
        default_index = 0
        if st.session_state.get('selected_product_for_content'):
            preselected_id = st.session_state.selected_product_for_content
            for i, (label, pid) in enumerate(product_options.items()):
                if pid == preselected_id:
                    default_index = i
                    break
            st.session_state.selected_product_for_content = None

        selected_label = st.selectbox(
            "Select Product",
            options=list(product_options.keys()),
            index=default_index,
            key="content_product_select"
        )
        product_id = product_options.get(selected_label)
        product = next((p for p in products if p['id'] == product_id), None)

    with col2:
        # Content type selection
        content_type = st.selectbox(
            "Content Type",
            ["Instagram Reel (15-30s)", "Instagram Story", "Carousel Post", "Weekly Roundup"],
            key="content_type_select"
        )

        languages = st.multiselect(
            "Languages",
            ["English", "Tamil", "English + Tamil (Mixed)"],
            default=["English", "Tamil", "English + Tamil (Mixed)"],
            key="content_languages"
        )

    if not product:
        st.info("Select a product to generate content")
        return

    # Display product info
    with st.expander("📦 Product Details", expanded=True):
        col1, col2, col3 = st.columns(3)
        with col1:
            st.write(f"**{product['name']}**")
            st.caption(f"₹{product.get('price', 0):,.0f}" + (f" (was ₹{product.get('original_price', 0):,.0f})" if product.get('original_price') else ""))
        with col2:
            st.write(f"Marketplace: {product.get('marketplace', 'Unknown')}")
            st.write(f"Category: {product.get('category', 'Uncategorized')}")
        with col3:
            if product.get('discount_pct'):
                st.write(f"Discount: {product['discount_pct']}%")
            if product.get('affiliate_url'):
                st.write("✅ Affiliate link available")

    # Generation options
    st.divider()
    st.subheader("⚙️ Generation Options")

    col1, col2 = st.columns(2)

    with col1:
        hook_style = st.selectbox(
            "Hook Style",
            ["Curiosity", "Problem/Solution", "Budget Saving", "Visual Demo", "Shocking Fact", "Relatable Story"],
            key="hook_style"
        )

        tone = st.selectbox(
            "Tone",
            ["Friendly & Casual", "Expert & Authoritative", "Excited & Energetic", "Trustworthy & Honest", "Fun & Playful"],
            key="content_tone"
        )

    with col2:
        include_price = st.checkbox("Include Price/Discount", value=True, key="include_price")
        include_cta = st.checkbox("Include Call-to-Action", value=True, key="include_cta")
        include_disclosure = st.checkbox("Include Affiliate Disclosure", value=True, key="include_disclosure")
        custom_instructions = st.text_area(
            "Custom Instructions",
            placeholder="Any specific requirements, brand voice notes, or constraints...",
            key="custom_instructions"
        )

    # Generate button
    if st.button("🚀 Generate Content", type="primary", use_container_width=True):
        with st.spinner("Generating content with Gemini AI..."):
            try:
                result = generate_content(product, {
                    'content_type': content_type,
                    'languages': languages,
                    'hook_style': hook_style,
                    'tone': tone,
                    'include_price': include_price,
                    'include_cta': include_cta,
                    'include_disclosure': include_disclosure,
                    'custom_instructions': custom_instructions
                })

                if result:
                    # Save draft
                    draft = {
                        'id': f"draft_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                        'product_id': product_id,
                        'product_name': product['name'],
                        'content_type': content_type,
                        'generated_content': result,
                        'created_at': datetime.now().isoformat(),
                        'status': 'draft'
                    }

                    if 'content_drafts' not in st.session_state:
                        st.session_state.content_drafts = []
                    st.session_state.content_drafts.append(draft)

                    st.session_state.current_draft = draft
                    st.success("Content generated successfully!")
                    st.rerun()
                else:
                    st.error("Failed to generate content. Please check your Gemini API configuration.")
            except Exception as e:
                st.error(f"Error generating content: {str(e)}")

    # Display current draft
    if st.session_state.get('current_draft'):
        render_draft_editor(st.session_state.current_draft)


def render_draft_editor(draft):
    """Render the draft editor with generated content."""

    st.divider()
    st.subheader("📝 Generated Content")

    content = draft.get('generated_content', {})

    # Tabs for different content pieces
    edit_tabs = st.tabs(["🎬 Reel Scripts", "📱 Captions & Hashtags", "🎥 Video Prompts", "💾 Save & Export"])

    with edit_tabs[0]:
        render_script_editor(content)

    with edit_tabs[1]:
        render_caption_editor(content)

    with edit_tabs[2]:
        render_video_prompt_editor(content)

    with edit_tabs[3]:
        render_draft_actions(draft)


def render_script_editor(content):
    """Render reel script editor."""

    scripts = content.get('scripts', {})

    for lang, script in scripts.items():
        st.write(f"**{lang} Script**")

        # Scene 1: Hook
        hook = st.text_area(
            f"Scene 1 - Hook ({lang})",
            value=script.get('hook', ''),
            height=80,
            key=f"hook_{lang}"
        )

        # Scene 2: Introduction
        intro = st.text_area(
            f"Scene 2 - Product Introduction ({lang})",
            value=script.get('introduction', ''),
            height=100,
            key=f"intro_{lang}"
        )

        # Scene 3: Benefits
        benefits = st.text_area(
            f"Scene 3 - Benefits & Use Cases ({lang})",
            value=script.get('benefits', ''),
            height=100,
            key=f"benefits_{lang}"
        )

        # Scene 4: CTA
        cta = st.text_area(
            f"Scene 4 - Call to Action ({lang})",
            value=script.get('cta', ''),
            height=80,
            key=f"cta_{lang}"
        )

        # Update content
        if 'scripts' not in content:
            content['scripts'] = {}
        content['scripts'][lang] = {
            'hook': hook,
            'introduction': intro,
            'benefits': benefits,
            'cta': cta
        }

        st.divider()


def render_caption_editor(content):
    """Render caption and hashtag editor."""

    seo = content.get('seo', {})

    # Instagram Caption
    caption = st.text_area(
        "Instagram Caption",
        value=seo.get('caption', ''),
        height=150,
        key="caption_editor"
    )

    col1, col2 = st.columns(2)
    with col1:
        hashtags = st.text_area(
            "Hashtags (one per line)",
            value='\n'.join(seo.get('hashtags', [])),
            height=100,
            key="hashtags_editor"
        )

    with col2:
        keywords = st.text_area(
            "Search Keywords (comma-separated)",
            value=', '.join(seo.get('keywords', [])),
            height=100,
            key="keywords_editor"
        )

    # Product title
    title = st.text_input(
        "Product Title for Post",
        value=seo.get('product_title', ''),
        key="product_title_editor"
    )

    # CTA
    cta_text = st.text_input(
        "Call to Action Text",
        value=seo.get('cta', 'Link in bio! 👆'),
        key="cta_text_editor"
    )

    # Affiliate disclosure
    disclosure = st.text_input(
        "Affiliate Disclosure",
        value=seo.get('disclosure', '#ad #affiliate'),
        key="disclosure_editor"
    )

    # Update content
    content['seo'] = {
        'caption': caption,
        'hashtags': [h.strip() for h in hashtags.split('\n') if h.strip()],
        'keywords': [k.strip() for k in keywords.split(',') if k.strip()],
        'product_title': title,
        'cta': cta_text,
        'disclosure': disclosure
    }


def render_video_prompt_editor(content):
    """Render video generation prompts editor."""

    video_prompts = content.get('video_prompts', {})

    st.write("**Scene-by-Scene Video Prompts**")

    scenes = [
        ('hook_visual', 'Hook Visual (0-3s)'),
        ('product_intro', 'Product Introduction (3-8s)'),
        ('benefits_demo', 'Benefits Demo (8-20s)'),
        ('cta_visual', 'CTA Visual (20-30s)')
    ]

    for key, label in scenes:
        with st.expander(f"🎬 {label}"):
            prompt = st.text_area(
                f"Prompt for {label}",
                value=video_prompts.get(key, ''),
                height=100,
                key=f"video_prompt_{key}"
            )

            col1, col2 = st.columns(2)
            with col1:
                camera = st.text_input(
                    "Camera Movement",
                    value=video_prompts.get(f'{key}_camera', ''),
                    key=f"camera_{key}"
                )
            with col2:
                music = st.text_input(
                    "Background Music",
                    value=video_prompts.get(f'{key}_music', ''),
                    key=f"music_{key}"
                )

            # Update
            if 'video_prompts' not in content:
                content['video_prompts'] = {}
            content['video_prompts'][key] = prompt
            content['video_prompts'][f'{key}_camera'] = camera
            content['video_prompts'][f'{key}_music'] = music

    # Overall settings
    st.write("**Video Settings**")
    col1, col2, col3 = st.columns(3)
    with col1:
        duration = st.number_input("Target Duration (seconds)", value=video_prompts.get('duration', 25), min_value=15, max_value=60, key="video_duration")
    with col2:
        resolution = st.selectbox("Resolution", ["1080x1920 (Reel)", "1080x1350 (Post)", "1080x1080 (Square)"], index=0, key="video_resolution")
    with col3:
        format_type = st.selectbox("Format", ["MP4", "MOV"], index=0, key="video_format")

    content['video_prompts']['duration'] = duration
    content['video_prompts']['resolution'] = resolution
    content['video_prompts']['format'] = format_type


def render_draft_actions(draft):
    """Render draft save/export actions."""

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        if st.button("💾 Save Draft", type="primary", use_container_width=True):
            # Update draft in session
            drafts = st.session_state.get('content_drafts', [])
            for i, d in enumerate(drafts):
                if d['id'] == draft['id']:
                    drafts[i] = draft
                    break
            st.success("Draft saved!")

    with col2:
        if st.button("✅ Send to Approval", use_container_width=True):
            # Move to approval queue
            approval_item = {
                'id': f"approval_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                'draft_id': draft['id'],
                'product_id': draft['product_id'],
                'product_name': draft['product_name'],
                'content_type': draft['content_type'],
                'generated_content': draft['generated_content'],
                'status': 'pending',
                'created_at': datetime.now().isoformat(),
                'updated_at': datetime.now().isoformat()
            }

            if 'approval_queue' not in st.session_state:
                st.session_state.approval_queue = []
            st.session_state.approval_queue.append(approval_item)

            # Update draft status
            draft['status'] = 'pending_approval'
            st.success("Sent to approval queue!")
            st.session_state.current_page = "Approval Queue"
            st.rerun()

    with col3:
        if st.button("📥 Export JSON", use_container_width=True):
            export_draft_json(draft)

    with col4:
        if st.button("🗑️ Discard", use_container_width=True):
            st.session_state.current_draft = None
            st.rerun()


def render_drafts_manager(drafts):
    """Render the drafts management view."""

    st.subheader("📝 Content Drafts")

    if not drafts:
        st.info("No drafts yet. Generate content to create drafts.")
        return

    # Filter options
    col1, col2 = st.columns(2)
    with col1:
        status_filter = st.selectbox("Filter by Status", ["All", "draft", "pending_approval", "approved", "rejected"])
    with col2:
        sort_by = st.selectbox("Sort by", ["Newest First", "Oldest First", "Product Name"])

    # Filter and sort
    filtered_drafts = drafts
    if status_filter != "All":
        filtered_drafts = [d for d in drafts if d.get('status') == status_filter]

    if sort_by == "Newest First":
        filtered_drafts.sort(key=lambda x: x.get('created_at', ''), reverse=True)
    elif sort_by == "Oldest First":
        filtered_drafts.sort(key=lambda x: x.get('created_at', ''))
    else:
        filtered_drafts.sort(key=lambda x: x.get('product_name', ''))

    # Display drafts
    for draft in filtered_drafts:
        with st.container():
            col1, col2, col3, col4, col5 = st.columns([3, 1, 1, 1, 1])

            with col1:
                st.write(f"**{draft.get('product_name', 'Unknown')}**")
                st.caption(f"{draft.get('content_type', 'Reel')} • {format_date(draft.get('created_at', ''))}")

            with col2:
                status = draft.get('status', 'draft')
                status_colors = {
                    'draft': '#6B7280',
                    'pending_approval': '#F59E0B',
                    'approved': '#10B981',
                    'rejected': '#EF4444'
                }
                color = status_colors.get(status, '#6B7280')
                st.markdown(f"""
                <span style="background: {color}20; color: {color}; padding: 2px 8px; border-radius: 12px; font-size: 0.7rem;">
                    {status.replace('_', ' ').title()}
                </span>
                """, unsafe_allow_html=True)

            with col3:
                if st.button("✏️ Edit", key=f"edit_draft_{draft['id']}", use_container_width=True):
                    st.session_state.current_draft = draft
                    st.rerun()

            with col4:
                if st.button("📋 Duplicate", key=f"dup_draft_{draft['id']}", use_container_width=True):
                    new_draft = draft.copy()
                    new_draft['id'] = f"draft_{datetime.now().strftime('%Y%m%d%H%M%S')}"
                    new_draft['status'] = 'draft'
                    new_draft['created_at'] = datetime.now().isoformat()
                    st.session_state.content_drafts.append(new_draft)
                    st.success("Draft duplicated!")
                    st.rerun()

            with col5:
                if st.button("🗑️", key=f"del_draft_{draft['id']}", use_container_width=True):
                    st.session_state.content_drafts = [d for d in drafts if d['id'] != draft['id']]
                    st.success("Draft deleted!")
                    st.rerun()

            st.divider()


def render_video_prompts(drafts):
    """Render video prompts for Canva/Flow."""

    st.subheader("🎬 Video Generation Prompts")

    # Get drafts with video prompts
    drafts_with_video = [d for d in drafts if d.get('generated_content', {}).get('video_prompts')]

    if not drafts_with_video:
        st.info("No video prompts available. Generate content with video prompts enabled.")
        return

    for draft in drafts_with_video:
        with st.expander(f"🎥 {draft.get('product_name', 'Unknown')} - {draft.get('content_type', 'Reel')}"):
            prompts = draft['generated_content'].get('video_prompts', {})

            # Canva template suggestion
            st.write("**📋 Canva Template Recommendation**")
            template_type = _get_canva_template_type(draft.get('content_type', ''))
            st.info(f"Use Canva template: **{template_type}**")

            # Video prompts for each scene
            scenes = [
                ('hook_visual', 'Hook (0-3s)', '🎯'),
                ('product_intro', 'Product Intro (3-8s)', '📦'),
                ('benefits_demo', 'Benefits Demo (8-20s)', '✨'),
                ('cta_visual', 'CTA (20-30s)', '👆')
            ]

            for key, label, icon in scenes:
                st.write(f"**{icon} {label}**")
                st.code(prompts.get(key, 'No prompt generated'), language='text')

                col1, col2 = st.columns(2)
                with col1:
                    st.caption(f"Camera: {prompts.get(f'{key}_camera', 'Not specified')}")
                with col2:
                    st.caption(f"Music: {prompts.get(f'{key}_music', 'Not specified')}")

            # Export for video generation tools
            st.divider()
            col1, col2 = st.columns(2)
            with col1:
                if st.button(f"📥 Export for Canva", key=f"export_canva_{draft['id']}", use_container_width=True):
                    export_canva_assets(draft)
            with col2:
                if st.button(f"📥 Export for Flow", key=f"export_flow_{draft['id']}", use_container_width=True):
                    export_flow_prompts(draft)


def render_templates():
    """Render Canva template management."""

    st.subheader("📋 Canva Templates")

    templates = [
        {
            'name': 'Product Promotion',
            'type': 'Reel',
            'description': 'Single product showcase with hook, demo, and CTA',
            'elements': ['Product image', 'Hook text', 'Price badge', 'Benefits list', 'CTA button', 'Affiliate disclosure']
        },
        {
            'name': 'Today\'s Best Deals',
            'type': 'Reel',
            'description': 'Multiple products in a quick-fire format',
            'elements': ['3-5 product cards', 'Countdown timer', 'Swipe up CTA', 'Category tags']
        },
        {
            'name': 'Top 5 Gadgets',
            'type': 'Reel',
            'description': 'Countdown style gadget roundup',
            'elements': ['Numbered list', 'Quick specs', 'Price comparison', 'Best pick badge']
        },
        {
            'name': 'Budget Shopping Finds',
            'type': 'Reel',
            'description': 'Affordable products under budget',
            'elements': ['Budget banner', 'Price highlights', 'Value indicators', 'Save amount']
        },
        {
            'name': 'Product Comparison',
            'type': 'Reel',
            'description': 'Side-by-side comparison',
            'elements': ['Split screen', 'Specs table', 'Winner highlight', 'Recommendation']
        },
        {
            'name': 'Festival Deals',
            'type': 'Reel',
            'description': 'Seasonal/festival promotional template',
            'elements': ['Festival theme', 'Limited time badge', 'Bundle offers', 'Code display']
        }
    ]

    for template in templates:
        with st.container():
            col1, col2, col3 = st.columns([3, 2, 1])

            with col1:
                st.write(f"**{template['name']}**")
                st.caption(template['description'])

            with col2:
                st.caption(f"Type: {template['type']}")
                elements_str = ', '.join(template['elements'][:3]) + f" +{len(template['elements'])-3} more"
                st.caption(f"Elements: {elements_str}")

            with col3:
                if st.button("Use Template", key=f"use_tpl_{template['name']}", use_container_width=True):
                    st.info(f"Template '{template['name']}' selected for next content generation")

            st.divider()

    # Brand settings
    st.subheader("🎨 Brand Identity")

    col1, col2 = st.columns(2)
    with col1:
        st.text_input("Brand Name", value="JP Finds Deals", key="brand_name")
        st.text_input("Tagline", value="Daily Shopping Bestie 💖", key="brand_tagline")
        st.color_picker("Primary Color", value="#FF6B35", key="brand_primary")
        st.color_picker("Secondary Color", value="#1A1A2E", key="brand_secondary")

    with col2:
        st.text_input("Logo URL", placeholder="https://...", key="brand_logo")
        st.text_input("Watermark Text", value="@jp.finds.deals", key="brand_watermark")
        st.selectbox("Font Style", ["Modern Sans", "Playful Rounded", "Bold Display", "Clean Minimal"], key="brand_font")
        st.selectbox("Animation Style", ["Subtle", "Energetic", "Smooth", "Snappy"], key="brand_animation")


def _get_canva_template_type(content_type):
    """Get recommended Canva template type."""
    mapping = {
        'Instagram Reel (15-30s)': 'Product Promotion',
        'Instagram Story': 'Today\'s Best Deals',
        'Carousel Post': 'Top 5 Gadgets',
        'Weekly Roundup': 'Budget Shopping Finds'
    }
    return mapping.get(content_type, 'Product Promotion')


def export_draft_json(draft):
    """Export draft as JSON."""
    import json

    json_str = json.dumps(draft, indent=2, default=str)

    st.download_button(
        label="Download Draft JSON",
        data=json_str,
        file_name=f"draft_{draft['product_name']}_{datetime.now().strftime('%Y%m%d')}.json",
        mime="application/json"
    )


def export_canva_assets(draft):
    """Export assets for Canva."""
    import json

    assets = {
        'product': {
            'name': draft['product_name'],
            'price': draft.get('product_price', ''),
            'discount': draft.get('product_discount', ''),
            'image_url': draft.get('product_image', ''),
            'affiliate_url': draft.get('product_affiliate_url', '')
        },
        'content': draft['generated_content'],
        'brand': {
            'name': 'JP Finds Deals',
            'watermark': '@jp.finds.deals',
            'colors': {'primary': '#FF6B35', 'secondary': '#1A1A2E'}
        }
    }

    json_str = json.dumps(assets, indent=2, default=str)

    st.download_button(
        label="Download Canva Assets",
        data=json_str,
        file_name=f"canva_assets_{draft['product_name']}_{datetime.now().strftime('%Y%m%d')}.json",
        mime="application/json"
    )


def export_flow_prompts(draft):
    """Export prompts for Google Flow."""
    import json

    prompts = draft['generated_content'].get('video_prompts', {})

    flow_data = {
        'project_name': f"JP Finds Deals - {draft['product_name']}",
        'scenes': [
            {'name': 'Hook', 'prompt': prompts.get('hook_visual', ''), 'duration': 3},
            {'name': 'Product Intro', 'prompt': prompts.get('product_intro', ''), 'duration': 5},
            {'name': 'Benefits', 'prompt': prompts.get('benefits_demo', ''), 'duration': 12},
            {'name': 'CTA', 'prompt': prompts.get('cta_visual', ''), 'duration': 5}
        ],
        'settings': {
            'resolution': prompts.get('resolution', '1080x1920'),
            'format': prompts.get('format', 'MP4'),
            'music': prompts.get('hook_visual_music', '')
        }
    }

    json_str = json.dumps(flow_data, indent=2, default=str)

    st.download_button(
        label="Download Flow Prompts",
        data=json_str,
        file_name=f"flow_prompts_{draft['product_name']}_{datetime.now().strftime('%Y%m%d')}.json",
        mime="application/json"
    )