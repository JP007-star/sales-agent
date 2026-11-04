"""
Gemini AI client for JP Finds Deals content generation.
"""

import os
import json
import streamlit as st
from typing import Dict, Any, Optional


def generate_content(product: dict, options: dict) -> Optional[dict]:
    """
    Generate promotional content using Gemini AI.

    Args:
        product: Product dictionary with details
        options: Generation options (languages, tone, content_type, etc.)

    Returns:
        Structured content dictionary or None if failed
    """

    api_key = st.session_state.settings.get('gemini_api_key', '')
    if not api_key:
        st.error("Gemini API key not configured. Please add it in Settings.")
        return None

    try:
        import google.generativeai as genai
        genai.configure(api_key=api_key)

        # Use Gemini 1.5 Flash for cost efficiency
        model = genai.GenerativeModel('gemini-1.5-flash')

        # Build the prompt
        prompt = build_generation_prompt(product, options)

        # Generate content
        response = model.generate_content(
            prompt,
            generation_config={
                'temperature': 0.7,
                'top_p': 0.9,
                'top_k': 40,
                'max_output_tokens': 8192,
            }
        )

        # Parse the response
        content = parse_gemini_content_response(response.text, options)
        return content

    except Exception as e:
        st.error(f"Gemini API error: {str(e)}")
        return None


def build_generation_prompt(product: dict, options: dict) -> str:
    """Build the prompt for Gemini content generation."""

    languages = options.get('languages', ['English', 'Tamil'])
    content_type = options.get('content_type', 'Instagram Reel (15-30s)')
    hook_style = options.get('hook_style', 'Curiosity')
    tone = options.get('tone', 'Friendly & Casual')
    include_price = options.get('include_price', True)
    include_cta = options.get('include_cta', True)
    include_disclosure = options.get('include_disclosure', True)
    custom_instructions = options.get('custom_instructions', '')

    # Product details
    name = product.get('name', 'Product')
    price = product.get('price', 0)
    original_price = product.get('original_price')
    discount = product.get('discount_pct', 0)
    category = product.get('category', 'General')
    features = product.get('features', [])
    description = product.get('description', '')
    marketplace = product.get('marketplace', 'Unknown')

    price_info = ""
    if include_price and price > 0:
        price_info = f"Current Price: ₹{price:,}"
        if original_price and original_price > price:
            price_info += f" (Was ₹{original_price:,}, {discount}% OFF)"

    features_text = "\n".join([f"• {f}" for f in features]) if features else "Not specified"

    # Language-specific instructions
    lang_instructions = []
    for lang in languages:
        if lang == 'English':
            lang_instructions.append("""
ENGLISH VERSION:
- Natural, conversational Indian English
- Use Hinglish where natural (e.g., "bahut accha hai", "paisa vasool")
- Keep it relatable for Indian audience
""")
        elif lang == 'Tamil':
            lang_instructions.append("""
TAMIL VERSION:
- Pure Tamil (தமிழ்) - not Tanglish
- Use colloquial Tamil expressions
- Cultural references familiar to Tamil Nadu audience
""")
        elif lang == 'English + Tamil (Mixed)':
            lang_instructions.append("""
ENGLISH + TAMIL MIXED (Tanglish):
- Mix English and Tamil naturally
- Example: "Idhu romba nalla product, must buy!"
- Use common Tamil words in English sentences
""")

    prompt = f"""
You are an expert Instagram content creator for @jp.finds.deals - a deal discovery account by Divya.
Create HIGH-CONVERTING promotional content for this product:

PRODUCT DETAILS:
- Name: {name}
- Category: {category}
- Marketplace: {marketplace}
- {price_info}
- Features:
{features_text}
- Description: {description}

CONTENT REQUIREMENTS:
- Type: {content_type}
- Hook Style: {hook_style}
- Tone: {tone}
- Include Price: {include_price}
- Include CTA: {include_cta}
- Include Affiliate Disclosure: {include_disclosure}
- Custom Instructions: {custom_instructions}

LANGUAGES TO GENERATE:
{chr(10).join(lang_instructions)}

OUTPUT FORMAT (JSON):
{{
  "scripts": {{
    "English": {{
      "hook": "Opening 3-second visual hook text",
      "introduction": "Scene 2 - Product introduction (3-8s)",
      "benefits": "Scene 3 - Benefits & use cases (8-20s)",
      "cta": "Scene 4 - Call to action (20-30s)"
    }},
    "Tamil": {{
      "hook": "ஹக் ടெக்ஸ்ட்",
      "introduction": "தொடர்பு Seen 2",
      "benefits": "பெனெஃபிட்ஸ்",
      "cta": "சிடிவை"
    }},
    "English + Tamil (Mixed)": {{
      "hook": "Mixed hook text",
      "introduction": "Mixed intro",
      "benefits": "Mixed benefits",
      "cta": "Mixed CTA"
    }}
  }},
  "seo": {{
    "caption": "Full Instagram caption with line breaks",
    "hashtags": ["tag1", "tag2", "tag3", "..."],
    "keywords": ["keyword1", "keyword2", "..."],
    "product_title": "Catchy product title for post",
    "cta": "Link in bio! 👆",
    "disclosure": "#ad #affiliate #jpfindsdeals"
  }},
  "video_prompts": {{
    "hook_visual": "Detailed visual prompt for hook scene (0-3s)",
    "hook_visual_camera": "Camera movement for hook",
    "hook_visual_music": "Music style for hook",
    "product_intro": "Visual prompt for product intro (3-8s)",
    "product_intro_camera": "Camera movement for intro",
    "product_intro_music": "Music style for intro",
    "benefits_demo": "Visual prompt for benefits demo (8-20s)",
    "benefits_demo_camera": "Camera movement for benefits",
    "benefits_demo_music": "Music style for benefits",
    "cta_visual": "Visual prompt for CTA (20-30s)",
    "cta_visual_camera": "Camera movement for CTA",
    "cta_visual_music": "Music style for CTA",
    "duration": 25,
    "resolution": "1080x1920",
    "format": "MP4"
  }}
}}

GUIDELINES:
1. Hook MUST grab attention in first 3 seconds
2. Scripts should be 15-30 seconds total
3. Tamil should be natural, not translated word-for-word
4. Hashtags: 20-30 relevant tags including #jpfindsdeals
5. Video prompts should be specific for AI video generation (Canva/Flow/FFmpeg)
6. Include affiliate disclosure naturally
7. CTA should drive to "Link in bio" or specific action
8. NO fake discounts, ratings, or claims
9. Focus on genuine value and usefulness
10. Keep brand voice: friendly, helpful, trustworthy shopping bestie

Generate the complete JSON response now.
"""
    return prompt


def parse_gemini_content_response(response_text: str, options: dict) -> dict:
    """Parse Gemini response into structured content."""

    try:
        # Try to extract JSON
        import re
        json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
        if json_match:
            content = json.loads(json_match.group())

            # Ensure all required languages present
            languages = options.get('languages', ['English', 'Tamil'])
            for lang in languages:
                if lang not in content.get('scripts', {}):
                    content['scripts'][lang] = {
                        'hook': '',
                        'introduction': '',
                        'benefits': '',
                        'cta': ''
                    }

            # Ensure SEO structure
            if 'seo' not in content:
                content['seo'] = {}
            seo_defaults = {
                'caption': '',
                'hashtags': ['#jpfindsdeals', '#discountdeals', '#smartshopping'],
                'keywords': [],
                'product_title': '',
                'cta': 'Link in bio! 👆',
                'disclosure': '#ad #affiliate #jpfindsdeals'
            }
            for key, default in seo_defaults.items():
                if key not in content['seo']:
                    content['seo'][key] = default

            # Ensure video prompts
            if 'video_prompts' not in content:
                content['video_prompts'] = {}
            video_defaults = {
                'hook_visual': '',
                'hook_visual_camera': 'Static, close-up',
                'hook_visual_music': 'Upbeat, attention-grabbing',
                'product_intro': '',
                'product_intro_camera': 'Slow zoom in',
                'product_intro_music': 'Friendly, upbeat',
                'benefits_demo': '',
                'benefits_demo_camera': 'Multiple angles',
                'benefits_demo_music': 'Energetic, demonstrative',
                'cta_visual': '',
                'cta_visual_camera': 'Point to caption/bio',
                'cta_visual_music': 'Clear, decisive',
                'duration': 25,
                'resolution': '1080x1920',
                'format': 'MP4'
            }
            for key, default in video_defaults.items():
                if key not in content['video_prompts']:
                    content['video_prompts'][key] = default

            return content
    except Exception as e:
        pass

    # Fallback: generate basic structure from text
    return generate_fallback_content(response_text, options)


def generate_fallback_content(response_text: str, options: dict) -> dict:
    """Generate fallback content structure when parsing fails."""

    languages = options.get('languages', ['English', 'Tamil'])

    scripts = {}
    for lang in languages:
        scripts[lang] = {
            'hook': 'Check out this amazing deal! 🔥',
            'introduction': 'I found this incredible product that you need to see.',
            'benefits': 'It solves [problem] and gives you [benefit]. Perfect for [use case].',
            'cta': 'Link in bio to grab this deal! 👆'
        }

    return {
        'scripts': scripts,
        'seo': {
            'caption': 'Found an amazing deal! Check it out 👇\n\n#jpfindsdeals #discountdeals #smartshopping',
            'hashtags': ['#jpfindsdeals', '#discountdeals', '#smartshopping', '#indianshopping', '#budgetfriendly'],
            'keywords': ['deal', 'discount', 'shopping', 'save money'],
            'product_title': 'Amazing Deal Alert!',
            'cta': 'Link in bio! 👆',
            'disclosure': '#ad #affiliate #jpfindsdeals'
        },
        'video_prompts': {
            'hook_visual': 'Close up of product with "WAIT FOR IT" text overlay',
            'hook_visual_camera': 'Static, close-up',
            'hook_visual_music': 'Upbeat, attention-grabbing',
            'product_intro': 'Product rotating, showing key features',
            'product_intro_camera': 'Slow 360 rotation',
            'product_intro_music': 'Friendly, upbeat',
            'benefits_demo': 'Person using product in real life',
            'benefits_demo_camera': 'Multiple angles, lifestyle shots',
            'benefits_demo_music': 'Energetic, demonstrative',
            'cta_visual': 'Pointing to caption with "LINK IN BIO" animation',
            'cta_visual_camera': 'Point to caption',
            'cta_visual_music': 'Clear, decisive',
            'duration': 25,
            'resolution': '1080x1920',
            'format': 'MP4'
        }
    }


def test_gemini_connection(api_key: str) -> bool:
    """Test if Gemini API key is valid."""
    try:
        import google.generativeai as genai
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content("Say 'Connection successful'")
        return "successful" in response.text.lower()
    except:
        return False


def estimate_tokens(text: str) -> int:
    """Rough token estimation (4 chars ≈ 1 token)."""
    return len(text) // 4


def calculate_generation_cost(input_tokens: int, output_tokens: int) -> float:
    """Estimate Gemini API cost (Gemini 1.5 Flash pricing)."""
    # Gemini 1.5 Flash: $0.075/1M input tokens, $0.30/1M output tokens
    input_cost = (input_tokens / 1_000_000) * 0.075
    output_cost = (output_tokens / 1_000_000) * 0.30
    return input_cost + output_cost