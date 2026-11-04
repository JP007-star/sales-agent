"""
Product Manager component for JP Finds Deals.
"""

import streamlit as st
import pandas as pd
from datetime import datetime
from utils.helpers import format_currency, format_date, validate_url, extract_product_info


def render_product_manager():
    """Render the Product Manager tab."""

    st.header("📦 Product Manager")

    # Action bar
    col1, col2, col3, col4 = st.columns([2, 1, 1, 1])

    with col1:
        search = st.text_input("🔍 Search products...", placeholder="Name, marketplace, category...", key="product_search")

    with col2:
        status_filter = st.selectbox("Status", ["All"] + [
            "discovered", "analyzed", "content_generated", "video_ready",
            "approved", "published", "rejected"
        ], key="product_status_filter")

    with col3:
        marketplace_filter = st.selectbox("Marketplace", ["All"] + [
            "Amazon", "Flipkart", "Other"
        ], key="product_marketplace_filter")

    with col4:
        if st.button("➕ Add Product", type="primary", use_container_width=True, key="add_product_btn"):
            st.session_state.show_add_product = True
            st.rerun()

    # Get and filter products
    products = st.session_state.get('products', [])

    # Apply filters
    filtered_products = products
    if search:
        search_lower = search.lower()
        filtered_products = [
            p for p in filtered_products
            if search_lower in p.get('name', '').lower() or
               search_lower in p.get('marketplace', '').lower() or
               search_lower in p.get('category', '').lower()
        ]
    if status_filter != "All":
        filtered_products = [p for p in filtered_products if p.get('status') == status_filter]
    if marketplace_filter != "All":
        filtered_products = [p for p in filtered_products if p.get('marketplace') == marketplace_filter]

    # Sort by created date descending
    filtered_products.sort(key=lambda x: x.get('created_at', ''), reverse=True)

    st.caption(f"Showing {len(filtered_products)} of {len(products)} products")

    # Display products
    if filtered_products:
        render_products_table(filtered_products)
    else:
        st.info("No products found matching your criteria. Click 'Add Product' to get started!")

    # Add product modal
    if st.session_state.get('show_add_product', False):
        render_add_product_modal()

    # Product detail modal
    if st.session_state.get('selected_product_id'):
        render_product_detail_modal(st.session_state.selected_product_id)


def render_products_table(products):
    """Render products as an interactive table."""

    # Prepare data for dataframe
    products_data = []
    for product in products:
        products_data.append({
            'Name': product.get('name', 'Unknown'),
            'Marketplace': product.get('marketplace', 'Unknown'),
            'Category': product.get('category', 'Uncategorized'),
            'Price': format_currency(product.get('price', 0)),
            'Original Price': format_currency(product.get('original_price', 0)) if product.get('original_price') else '-',
            'Discount': f"{product.get('discount_pct', 0)}%" if product.get('discount_pct') else '-',
            'Status': product.get('status', 'discovered').replace('_', ' ').title(),
            'Score': product.get('score', 0),
            'Created': format_date(product.get('created_at', '')),
            'ID': product.get('id', '')
        })

    df = pd.DataFrame(products_data)

    # Configure column display
    column_config = {
        'Name': st.column_config.TextColumn('Product Name', width='medium'),
        'Marketplace': st.column_config.SelectboxColumn(
            'Marketplace',
            options=["Amazon", "Flipkart", "Other"],
            width='small'
        ),
        'Category': st.column_config.TextColumn('Category', width='small'),
        'Price': st.column_config.TextColumn('Current Price', width='small'),
        'Original Price': st.column_config.TextColumn('Original Price', width='small'),
        'Discount': st.column_config.TextColumn('Discount', width='small'),
        'Status': st.column_config.SelectboxColumn(
            'Status',
            options=["Discovered", "Analyzed", "Content Generated", "Video Ready", "Approved", "Published", "Rejected"],
            width='medium'
        ),
        'Score': st.column_config.ProgressColumn(
            'Score',
            min_value=0,
            max_value=100,
            format='%d',
            width='small'
        ),
        'Created': st.column_config.TextColumn('Date Added', width='small'),
        'ID': st.column_config.TextColumn('ID', width='small')
    }

    # Display editable dataframe
    edited_df = st.data_editor(
        df,
        column_config=column_config,
        hide_index=True,
        use_container_width=True,
        disabled=['ID', 'Created'],
        key="products_editor"
    )

    # Handle status changes
    if not edited_df.equals(df):
        for idx, row in edited_df.iterrows():
            original = df.iloc[idx]
            if row['Status'] != original['Status']:
                product_id = row['ID']
                new_status = row['Status'].lower().replace(' ', '_')
                update_product_status(product_id, new_status)
                st.success(f"Updated {row['Name']} to {row['Status']}")
                st.rerun()

    # Bulk actions
    st.divider()
    st.subheader("Bulk Actions")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        if st.button("🎬 Generate Content", use_container_width=True):
            st.info("Select products first, then use Content Studio")

    with col2:
        if st.button("📤 Export CSV", use_container_width=True):
            export_products_csv(products)

    with col3:
        if st.button("🔄 Re-analyze", use_container_width=True):
            st.info("Re-analysis would trigger Gemini AI")

    with col4:
        if st.button("🗑️ Delete Selected", use_container_width=True):
            st.warning("Select products to delete")


def render_add_product_modal():
    """Render modal for adding a new product."""

    with st.form("add_product_form", clear_on_submit=True):
        st.subheader("Add New Product")

        # URL input
        product_url = st.text_input(
            "Product URL *",
            placeholder="https://www.amazon.in/... or https://www.flipkart.com/...",
            help="Paste the product URL from Amazon, Flipkart, or other supported marketplace"
        )

        # Auto-detect marketplace
        marketplace = "Unknown"
        if "amazon" in product_url.lower():
            marketplace = "Amazon"
        elif "flipkart" in product_url.lower():
            marketplace = "Flipkart"

        col1, col2 = st.columns(2)
        with col1:
            st.text_input("Marketplace", value=marketplace, disabled=True)
            name = st.text_input("Product Name *", placeholder="Product name")
            category = st.selectbox("Category *", [
                "Electronics & Gadgets",
                "Mobile Accessories",
                "Home & Kitchen",
                "Fashion & Clothing",
                "Beauty & Skincare",
                "Lifestyle Products",
                "Travel Accessories",
                "Everyday Essentials",
                "Trending Products",
                "Budget-Friendly"
            ])

        with col2:
            price = st.number_input("Current Price (₹)", min_value=0, value=0, step=1)
            original_price = st.number_input("Original Price (₹)", min_value=0, value=0, step=1, help="Leave 0 if not on discount")
            discount_pct = st.number_input("Discount %", min_value=0, max_value=100, value=0, step=1, help="Calculated automatically if prices provided")
            rating = st.number_input("Rating", min_value=0.0, max_value=5.0, value=0.0, step=0.1)
            review_count = st.number_input("Review Count", min_value=0, value=0, step=1)

        # Affiliate link
        st.write("**Affiliate Tracking**")
        affiliate_url = st.text_input(
            "Affiliate URL",
            placeholder="Your affiliate tracking URL (auto-generated if using API)",
            help="The URL with your affiliate tracking parameters"
        )

        # Product image
        image_url = st.text_input(
            "Product Image URL",
            placeholder="https://... (main product image)"
        )

        # Features and description
        features = st.text_area(
            "Key Features (one per line)",
            placeholder="Feature 1\nFeature 2\nFeature 3"
        )

        description = st.text_area(
            "Product Description",
            placeholder="Brief description of the product..."
        )

        # Tags
        tags = st.text_input(
            "Tags (comma-separated)",
            placeholder="bestseller, limited-time, budget-friendly, trending"
        )

        col1, col2 = st.columns(2)
        with col1:
            submitted = st.form_submit_button("Add Product", type="primary", use_container_width=True)
        with col2:
            cancelled = st.form_submit_button("Cancel", use_container_width=True)

        if cancelled:
            st.session_state.show_add_product = False
            st.rerun()

        if submitted:
            errors = []
            if not product_url:
                errors.append("Product URL is required")
            elif not validate_url(product_url):
                errors.append("Invalid URL format")
            if not name:
                errors.append("Product name is required")

            if errors:
                for error in errors:
                    st.error(error)
            else:
                # Calculate discount if prices provided
                if original_price > 0 and price > 0:
                    discount_pct = round(((original_price - price) / original_price) * 100)

                product_data = {
                    'id': f"prod_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                    'name': name,
                    'url': product_url,
                    'marketplace': marketplace,
                    'category': category,
                    'price': price,
                    'original_price': original_price if original_price > 0 else None,
                    'discount_pct': discount_pct if discount_pct > 0 else None,
                    'rating': rating if rating > 0 else None,
                    'review_count': review_count if review_count > 0 else None,
                    'affiliate_url': affiliate_url,
                    'image_url': image_url,
                    'features': [f.strip() for f in features.split('\n') if f.strip()],
                    'description': description,
                    'tags': [t.strip() for t in tags.split(',') if t.strip()],
                    'status': 'discovered',
                    'score': 0,
                    'created_at': datetime.now().isoformat(),
                    'updated_at': datetime.now().isoformat()
                }

                # Add to products
                if 'products' not in st.session_state:
                    st.session_state.products = []
                st.session_state.products.append(product_data)

                st.session_state.show_add_product = False
                st.success(f"Product '{name}' added successfully!")
                st.rerun()


def render_product_detail_modal(product_id):
    """Render detailed view of a product."""

    products = st.session_state.get('products', [])
    product = next((p for p in products if p.get('id') == product_id), None)

    if not product:
        st.session_state.selected_product_id = None
        return

    with st.container():
        st.markdown("---")
        st.subheader(f"📦 Product Details: {product.get('name', 'Unknown')}")

        # Close button
        if st.button("✕ Close", key="close_product_detail"):
            st.session_state.selected_product_id = None
            st.rerun()

        # Main info row
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Marketplace", product.get('marketplace', 'Unknown'))
            st.caption(f"Category: {product.get('category', 'Uncategorized')}")

        with col2:
            st.metric("Price", format_currency(product.get('price', 0)))
            if product.get('original_price'):
                st.caption(f"Was: {format_currency(product['original_price'])}")

        with col3:
            discount = product.get('discount_pct', 0)
            st.metric("Discount", f"{discount}%" if discount else "No discount")
            st.caption(f"Rating: {product.get('rating', 'N/A')}/5 ({product.get('review_count', 0)} reviews)")

        with col4:
            score = product.get('score', 0)
            st.metric("AI Score", f"{score}/100")
            st.caption(f"Status: {product.get('status', 'discovered').replace('_', ' ').title()}")

        # Product image
        if product.get('image_url'):
            st.image(product['image_url'], width=300)

        # Links
        st.write("**Links**")
        col1, col2 = st.columns(2)
        with col1:
            st.link_button("🔗 Original Product", product.get('url', '#'))
        with col2:
            if product.get('affiliate_url'):
                st.link_button("💰 Affiliate Link", product['affiliate_url'])

        # Features
        if product.get('features'):
            st.write("**Key Features**")
            for feature in product['features']:
                st.write(f"• {feature}")

        # Description
        if product.get('description'):
            st.write("**Description**")
            st.write(product['description'])

        # Tags
        if product.get('tags'):
            st.write("**Tags**")
            tags_html = " ".join([f'<span style="background: #FF6B3520; color: #FF6B35; padding: 2px 8px; border-radius: 12px; font-size: 0.75rem; margin-right: 4px;">{tag}</span>' for tag in product['tags']])
            st.markdown(tags_html, unsafe_allow_html=True)

        st.divider()

        # Actions
        st.write("**Actions**")
        action_cols = st.columns(5)

        with action_cols[0]:
            new_status = st.selectbox(
                "Change Status",
                ["discovered", "analyzed", "content_generated", "video_ready", "approved", "published", "rejected"],
                index=["discovered", "analyzed", "content_generated", "video_ready", "approved", "published", "rejected"].index(product.get('status', 'discovered')),
                key=f"status_change_{product_id}"
            )
            if new_status != product.get('status'):
                if st.button("Update Status", key=f"update_status_{product_id}"):
                    update_product_status(product_id, new_status)
                    st.success(f"Status updated to {new_status.replace('_', ' ').title()}")
                    st.rerun()

        with action_cols[1]:
            if st.button("🎬 Generate Content", key=f"gen_content_{product_id}", use_container_width=True):
                st.session_state.current_page = "Content Studio"
                st.session_state.selected_product_for_content = product_id
                st.rerun()

        with action_cols[2]:
            if st.button("📝 Edit Details", key=f"edit_{product_id}", use_container_width=True):
                st.session_state.editing_product = product_id
                st.rerun()

        with action_cols[3]:
            if st.button("📊 View Analytics", key=f"analytics_{product_id}", use_container_width=True):
                st.session_state.current_page = "Analytics"
                st.rerun()

        with action_cols[4]:
            if st.button("🗑️ Delete", key=f"delete_{product_id}", type="secondary", use_container_width=True):
                st.session_state.confirm_delete_product = product_id
                st.rerun()

        # Delete confirmation
        if st.session_state.get('confirm_delete_product') == product_id:
            st.error("⚠️ Are you sure you want to delete this product? This action cannot be undone.")
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Yes, Delete", type="primary", key=f"confirm_delete_yes_{product_id}"):
                    st.session_state.products = [p for p in products if p.get('id') != product_id]
                    st.session_state.selected_product_id = None
                    st.session_state.confirm_delete_product = None
                    st.success("Product deleted")
                    st.rerun()
            with col2:
                if st.button("Cancel", key=f"confirm_delete_no_{product_id}"):
                    st.session_state.confirm_delete_product = None
                    st.rerun()


def update_product_status(product_id, new_status):
    """Update product status."""
    products = st.session_state.get('products', [])
    for product in products:
        if product.get('id') == product_id:
            product['status'] = new_status
            product['updated_at'] = datetime.now().isoformat()
            break


def export_products_csv(products):
    """Export products as CSV."""
    import pandas as pd
    from utils.helpers import format_date

    data = []
    for product in products:
        data.append({
            'ID': product.get('id', ''),
            'Name': product.get('name', ''),
            'URL': product.get('url', ''),
            'Marketplace': product.get('marketplace', ''),
            'Category': product.get('category', ''),
            'Price': product.get('price', 0),
            'Original Price': product.get('original_price', 0) or 0,
            'Discount %': product.get('discount_pct', 0) or 0,
            'Rating': product.get('rating', 0) or 0,
            'Review Count': product.get('review_count', 0) or 0,
            'Affiliate URL': product.get('affiliate_url', ''),
            'Image URL': product.get('image_url', ''),
            'Features': '; '.join(product.get('features', [])),
            'Description': product.get('description', ''),
            'Tags': ', '.join(product.get('tags', [])),
            'Status': product.get('status', ''),
            'Score': product.get('score', 0),
            'Created At': format_date(product.get('created_at', '')),
            'Updated At': format_date(product.get('updated_at', ''))
        })

    df = pd.DataFrame(data)
    csv = df.to_csv(index=False)

    st.download_button(
        label="Download Products CSV",
        data=csv,
        file_name=f"products_export_{datetime.now().strftime('%Y%m%d')}.csv",
        mime="text/csv"
    )