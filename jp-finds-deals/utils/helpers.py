"""
Helper functions for JP Finds Deals.
"""

import re
from datetime import datetime
from typing import Union, Optional
from urllib.parse import urlparse


def format_currency(value: Union[int, float]) -> str:
    """Format number as Indian currency string."""
    if value >= 1_00_00_000:  # 1 Crore
        return f"₹{value/1_00_00_000:.2f} Cr"
    elif value >= 1_00_000:  # 1 Lakh
        return f"₹{value/1_00_000:.2f} L"
    elif value >= 1_000:
        return f"₹{value/1_000:.1f}K"
    else:
        return f"₹{value:,.0f}"


def format_date(date_input: Union[str, datetime]) -> str:
    """Format date as readable string."""
    if isinstance(date_input, str):
        try:
            dt = datetime.fromisoformat(date_input.replace('Z', '+00:00'))
        except ValueError:
            return date_input
    else:
        dt = date_input
    return dt.strftime('%b %d, %Y')


def format_datetime(date_input: Union[str, datetime]) -> str:
    """Format datetime as readable string."""
    if isinstance(date_input, str):
        try:
            dt = datetime.fromisoformat(date_input.replace('Z', '+00:00'))
        except ValueError:
            return date_input
    else:
        dt = date_input
    return dt.strftime('%b %d, %Y %I:%M %p')


def get_relative_time(date_input: Union[str, datetime]) -> str:
    """Get relative time string (e.g., '2 hours ago')."""
    if isinstance(date_input, str):
        try:
            dt = datetime.fromisoformat(date_input.replace('Z', '+00:00'))
        except ValueError:
            return "Unknown"
    else:
        dt = date_input

    now = datetime.now()
    diff = now - dt

    if diff.days > 0:
        return f"{diff.days} day{'s' if diff.days != 1 else ''} ago"
    elif diff.seconds >= 3600:
        hours = diff.seconds // 3600
        return f"{hours} hour{'s' if hours != 1 else ''} ago"
    elif diff.seconds >= 60:
        minutes = diff.seconds // 60
        return f"{minutes} minute{'s' if minutes != 1 else ''} ago"
    else:
        return "Just now"


def validate_url(url: str) -> bool:
    """Validate URL format."""
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False


def extract_marketplace(url: str) -> str:
    """Extract marketplace from URL."""
    url_lower = url.lower()
    if 'amazon' in url_lower:
        return 'Amazon'
    elif 'flipkart' in url_lower:
        return 'Flipkart'
    elif 'myntra' in url_lower:
        return 'Myntra'
    elif 'nykaa' in url_lower:
        return 'Nykaa'
    elif 'meesho' in url_lower:
        return 'Meesho'
    else:
        return 'Unknown'


def extract_product_info(url: str) -> dict:
    """Extract basic product info from URL."""
    info = {
        'marketplace': extract_marketplace(url),
        'product_id': None,
        'clean_url': url
    }

    # Amazon product ID extraction
    if 'amazon' in url.lower():
        patterns = [
            r'/dp/([A-Z0-9]{10})',
            r'/gp/product/([A-Z0-9]{10})',
            r'/product/([A-Z0-9]{10})',
            r'/([A-Z0-9]{10})(?:/|\?|$)'
        ]
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                info['product_id'] = match.group(1)
                break

    # Flipkart product ID extraction
    elif 'flipkart' in url.lower():
        patterns = [
            r'/p/([a-zA-Z0-9]+)',
            r'pid=([a-zA-Z0-9]+)',
            r'productId=([a-zA-Z0-9]+)'
        ]
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                info['product_id'] = match.group(1)
                break

    return info


def calculate_product_score(product: dict) -> int:
    """Calculate product score based on various factors (0-100)."""
    score = 0

    # Discount score (0-30 points)
    discount = product.get('discount_pct', 0) or 0
    if discount >= 50:
        score += 30
    elif discount >= 30:
        score += 20
    elif discount >= 15:
        score += 10
    elif discount > 0:
        score += 5

    # Rating score (0-20 points)
    rating = product.get('rating', 0) or 0
    review_count = product.get('review_count', 0) or 0
    if rating >= 4.5 and review_count >= 1000:
        score += 20
    elif rating >= 4.0 and review_count >= 500:
        score += 15
    elif rating >= 4.0:
        score += 10
    elif rating >= 3.5:
        score += 5

    # Price attractiveness (0-15 points)
    price = product.get('price', 0) or 0
    if price <= 500:
        score += 15
    elif price <= 1000:
        score += 12
    elif price <= 2000:
        score += 8
    elif price <= 5000:
        score += 5

    # Category relevance (0-15 points)
    trending_categories = [
        'Electronics & Gadgets',
        'Mobile Accessories',
        'Trending Products',
        'Budget-Friendly'
    ]
    category = product.get('category', '')
    if category in trending_categories:
        score += 15
    elif category in ['Home & Kitchen', 'Beauty & Skincare']:
        score += 10
    elif category:
        score += 5

    # Features richness (0-10 points)
    features = product.get('features', [])
    if len(features) >= 5:
        score += 10
    elif len(features) >= 3:
        score += 7
    elif len(features) >= 1:
        score += 3

    # Affiliate link availability (0-10 points)
    if product.get('affiliate_url'):
        score += 10

    return min(score, 100)


def get_score_label(score: int) -> str:
    """Get label for product score."""
    if score >= 80:
        return "🔥 Hot"
    elif score >= 60:
        return "🌡️ Warm"
    elif score >= 40:
        return "❄️ Cool"
    else:
        return "🧊 Cold"


def get_score_color(score: int) -> str:
    """Get color for score."""
    if score >= 80:
        return "#EF4444"
    elif score >= 60:
        return "#F59E0B"
    elif score >= 40:
        return "#06B6D4"
    else:
        return "#6B7280"


def truncate_text(text: str, max_length: int = 100) -> str:
    """Truncate text to max length with ellipsis."""
    if not text:
        return ""
    if len(text) <= max_length:
        return text
    return text[:max_length-3] + "..."


def generate_hashtags(product: dict, base_tags: list = None) -> list:
    """Generate relevant hashtags for a product."""
    tags = set(base_tags or [])

    # Add marketplace tags
    marketplace = product.get('marketplace', '').lower()
    if marketplace == 'amazon':
        tags.add('#amazonfinds')
        tags.add('#amazondeals')
    elif marketplace == 'flipkart':
        tags.add('#flipkartdeals')
        tags.add('#flipkartfinds')

    # Add category tags
    category = product.get('category', '').lower()
    category_tags = {
        'electronics & gadgets': ['#electronics', '#gadgets', '#techdeals'],
        'mobile accessories': ['#mobileaccessories', '#phoneaccessories', '#techaccessories'],
        'home & kitchen': ['#homekitchen', '#homedeals', '#kitchenfinds'],
        'fashion & clothing': ['#fashion', '#clothing', '#styledeals'],
        'beauty & skincare': ['#beauty', '#skincare', '#beautydeals'],
        'lifestyle products': ['#lifestyle', '#lifestyleproducts'],
        'travel accessories': ['#travel', '#travelaccessories', '#travelgear'],
        'everyday essentials': ['#essentials', '#dailyessentials'],
        'trending products': ['#trending', '#viral', '#trendingnow'],
        'budget-friendly': ['#budgetfriendly', '#affordable', '#under500', '#under1000']
    }

    for cat_key, cat_tags in category_tags.items():
        if cat_key in category:
            tags.update(cat_tags)
            break

    # Add price-based tags
    price = product.get('price', 0) or 0
    if price <= 299:
        tags.add('#under300')
    elif price <= 499:
        tags.add('#under500')
    elif price <= 999:
        tags.add('#under1000')
    elif price <= 1999:
        tags.add('#under2000')

    # Add discount tag
    discount = product.get('discount_pct', 0) or 0
    if discount >= 50:
        tags.add('#50off')
    elif discount >= 30:
        tags.add('#30off')

    # Brand tags
    tags.update(['#jpfindsdeals', '#discountdeals', '#smartshopping', '#indianshopping', '#shoppinghacks', '#dealsofday'])

    return list(tags)[:30]  # Instagram limit


def parse_gemini_response(response_text: str) -> dict:
    """Parse Gemini AI response into structured data."""
    try:
        # Try to extract JSON from response
        json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
        if json_match:
            return json.loads(json_match.group())
    except:
        pass

    # Fallback: parse as text sections
    return {
        'raw_response': response_text,
        'parsed': False
    }


def sanitize_filename(filename: str) -> str:
    """Sanitize filename for safe file system usage."""
    # Remove invalid characters
    sanitized = re.sub(r'[<>:"/\\|?*]', '_', filename)
    # Remove extra spaces and limit length
    sanitized = re.sub(r'\s+', '_', sanitized.strip())
    return sanitized[:100]


def generate_affiliate_url(marketplace: str, product_id: str, associate_tag: str = None) -> str:
    """Generate affiliate tracking URL."""
    if marketplace.lower() == 'amazon' and associate_tag:
        return f"https://www.amazon.in/dp/{product_id}?tag={associate_tag}"
    elif marketplace.lower() == 'flipkart':
        # Flipkart affiliate URL format would go here
        return f"https://dl.flipkart.com/dl/{product_id}"

    return ""


# Import json at module level for parse_gemini_response
import json