"""
Helper functions for Sales Agent.
"""

from datetime import datetime
from typing import Union


def format_currency(value: Union[int, float]) -> str:
    """Format number as currency string."""
    if value >= 1_000_000:
        return f"${value/1_000_000:.1f}M"
    elif value >= 1_000:
        return f"${value/1_000:.1f}K"
    else:
        return f"${value:,.0f}"


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


def get_stage_color(stage: str) -> str:
    """Get color for a pipeline stage."""
    colors = {
        'New': '#6B7280',
        'Contacted': '#3B82F6',
        'Qualified': '#06B6D4',
        'Proposal': '#F59E0B',
        'Negotiation': '#EF4444',
        'Closed Won': '#10B981',
        'Closed Lost': '#EF4444'
    }
    return colors.get(stage, '#6B7280')


def get_priority_color(priority: str) -> str:
    """Get color for task priority."""
    colors = {
        'Low': '#10B981',
        'Medium': '#F59E0B',
        'High': '#EF4444',
        'Critical': '#DC2626'
    }
    return colors.get(priority, '#6B7280')


def get_priority_icon(priority: str) -> str:
    """Get icon for task priority."""
    icons = {
        'Low': '🟢',
        'Medium': '🟡',
        'High': '🟠',
        'Critical': '🔴'
    }
    return icons.get(priority, '⚪')


def truncate_text(text: str, max_length: int = 50) -> str:
    """Truncate text to max length with ellipsis."""
    if len(text) <= max_length:
        return text
    return text[:max_length-3] + "..."


def calculate_days_until(date_input: Union[str, datetime]) -> int:
    """Calculate days until a date."""
    if isinstance(date_input, str):
        try:
            target = datetime.fromisoformat(date_input.replace('Z', '+00:00'))
        except ValueError:
            return 0
    else:
        target = date_input

    now = datetime.now()
    delta = target - now
    return max(0, delta.days)


def is_overdue(date_input: Union[str, datetime]) -> bool:
    """Check if a date is overdue."""
    if isinstance(date_input, str):
        try:
            target = datetime.fromisoformat(date_input.replace('Z', '+00:00'))
        except ValueError:
            return False
    else:
        target = date_input
    return target < datetime.now()


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


def parse_email_variables(template: str, variables: dict) -> str:
    """Parse template variables in email."""
    result = template
    for key, value in variables.items():
        placeholder = f"{{{key}}}"
        result = result.replace(placeholder, str(value))
    return result


def validate_email(email: str) -> bool:
    """Simple email validation."""
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def validate_phone(phone: str) -> bool:
    """Simple phone validation."""
    import re
    # Remove all non-digits
    digits = re.sub(r'\D', '', phone)
    # Check if it's a valid length (10-15 digits)
    return 10 <= len(digits) <= 15


def generate_lead_score(lead: dict) -> int:
    """Calculate lead score based on various factors."""
    score = 0

    # Stage scoring
    stage_scores = {
        'New': 10,
        'Contacted': 20,
        'Qualified': 40,
        'Proposal': 60,
        'Negotiation': 80,
        'Closed Won': 100,
        'Closed Lost': 0
    }
    score += stage_scores.get(lead.get('stage', 'New'), 10)

    # Value scoring (capped at 30 points)
    value = lead.get('value', 0)
    if value >= 100000:
        score += 30
    elif value >= 50000:
        score += 20
    elif value >= 10000:
        score += 10
    elif value > 0:
        score += 5

    # Source scoring
    source_scores = {
        'Referral': 15,
        'Partner': 15,
        'Event': 10,
        'Website': 5,
        'Email Campaign': 5,
        'Social Media': 5,
        'Cold Call': 0
    }
    score += source_scores.get(lead.get('source', ''), 0)

    # Engagement scoring
    if lead.get('last_contacted'):
        score += 10
    if lead.get('next_followup'):
        score += 5

    return min(score, 100)


def get_lead_score_label(score: int) -> str:
    """Get label for lead score."""
    if score >= 80:
        return "🔥 Hot"
    elif score >= 60:
        return "🌡️ Warm"
    elif score >= 40:
        return "❄️ Cool"
    else:
        return "🧊 Cold"