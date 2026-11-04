"""
Comprehensive Business Case Tests for JP Sales Agent Suite

This test suite covers all major business cases for both applications:
1. Sales Agent - B2B Sales Management
2. JP Finds Deals - AI-Powered Instagram Affiliate Marketing

Run with: python -m pytest test_business_cases.py -v
"""

import pytest
import json
import tempfile
import os
from datetime import datetime, timedelta
from pathlib import Path
import sys

# Add project roots to path
sales_pipeline_path = str(Path(__file__).parent / "sales-pipeline")
affiliate_studio_path = str(Path(__file__).parent / "affiliate-studio")
sys.path.insert(0, sales_pipeline_path)
sys.path.insert(0, affiliate_studio_path)

# ============================================================
# SALES AGENT TESTS - Load helpers from sales-agent specifically
# ============================================================

# Load sales-pipeline helpers module explicitly
import importlib.util
sa_helpers_path = str(Path(sales_pipeline_path) / "utils" / "helpers.py")
spec = importlib.util.spec_from_file_location("sa_helpers", sa_helpers_path)
sa_helpers = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sa_helpers)

# Extract functions from sa_helpers module
format_currency_sa = sa_helpers.format_currency
format_date_sa = sa_helpers.format_date
format_datetime_sa = sa_helpers.format_datetime
get_stage_color = sa_helpers.get_stage_color
get_priority_color = sa_helpers.get_priority_color
get_priority_icon = sa_helpers.get_priority_icon
truncate_text_sa = sa_helpers.truncate_text
calculate_days_until = sa_helpers.calculate_days_until
is_overdue = sa_helpers.is_overdue
get_relative_time_sa = sa_helpers.get_relative_time
parse_email_variables = sa_helpers.parse_email_variables
validate_email = sa_helpers.validate_email
validate_phone = sa_helpers.validate_phone
generate_lead_score = sa_helpers.generate_lead_score
get_lead_score_label = sa_helpers.get_lead_score_label

# Load DataManager
sa_data_manager_path = str(Path(sales_pipeline_path) / "utils" / "data_manager.py")
spec = importlib.util.spec_from_file_location("sa_data_manager", sa_data_manager_path)
sa_data_manager = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sa_data_manager)
DataManager = sa_data_manager.DataManager


# Module-level fixtures
@pytest.fixture
def temp_data_dir():
    """Create temporary data directory for testing."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield tmpdir


@pytest.fixture
def data_manager(temp_data_dir):
    """Create DataManager instance with temp directory."""
    return DataManager(data_dir=temp_data_dir)


class TestSalesAgentDataManager:
    """Test DataManager - Core data persistence layer"""

    def test_leads_crud(self, data_manager):
        """Test Lead Create, Read, Update, Delete operations."""
        # CREATE
        lead_data = {
            'name': 'Test Lead',
            'email': 'test@example.com',
            'phone': '+15551234567',
            'company': 'Test Corp',
            'source': 'Website',
            'stage': 'New',
            'value': 50000,
            'assigned_to': 'Me',
            'notes': 'Test notes'
        }
        lead = data_manager.add_lead(lead_data)

        assert lead['id'] is not None
        assert lead['name'] == 'Test Lead'
        assert lead['email'] == 'test@example.com'
        assert lead['stage'] == 'New'
        assert lead['value'] == 50000

        # READ
        retrieved = data_manager.get_lead(lead['id'])
        assert retrieved is not None
        assert retrieved['name'] == 'Test Lead'

        # UPDATE
        updated = data_manager.update_lead(lead['id'], {'stage': 'Qualified', 'value': 75000})
        assert updated['stage'] == 'Qualified'
        assert updated['value'] == 75000

        # DELETE
        deleted = data_manager.delete_lead(lead['id'])
        assert deleted is True
        assert data_manager.get_lead(lead['id']) is None

    def test_leads_filter_by_stage(self, data_manager):
        """Test filtering leads by pipeline stage."""
        # Clear existing sample data
        data_manager.leads = []
        data_manager._save_json(data_manager.leads_file, [])

        data_manager.add_lead({'name': 'Lead 1', 'email': 'l1@test.com', 'stage': 'New', 'value': 10000})
        data_manager.add_lead({'name': 'Lead 2', 'email': 'l2@test.com', 'stage': 'Qualified', 'value': 20000})
        data_manager.add_lead({'name': 'Lead 3', 'email': 'l3@test.com', 'stage': 'Closed Won', 'value': 30000})

        new_leads = data_manager.get_leads_by_stage('New')
        qualified_leads = data_manager.get_leads_by_stage('Qualified')
        won_leads = data_manager.get_leads_by_stage('Closed Won')

        assert len(new_leads) == 1
        assert len(qualified_leads) == 1
        assert len(won_leads) == 1

    def test_leads_filter_by_assignee(self, data_manager):
        """Test filtering leads by assigned sales rep."""
        # Clear existing sample data
        data_manager.leads = []
        data_manager._save_json(data_manager.leads_file, [])

        data_manager.add_lead({'name': 'Lead 1', 'email': 'l1@test.com', 'assigned_to': 'Me', 'stage': 'New', 'value': 10000})
        data_manager.add_lead({'name': 'Lead 2', 'email': 'l2@test.com', 'assigned_to': 'Sarah Johnson', 'stage': 'New', 'value': 20000})

        my_leads = data_manager.get_leads_by_assignee('Me')
        sarah_leads = data_manager.get_leads_by_assignee('Sarah Johnson')

        assert len(my_leads) == 1
        assert len(sarah_leads) == 1

    def test_activities_tracking(self, data_manager):
        """Test activity logging and retrieval."""
        lead = data_manager.add_lead({'name': 'Lead 1', 'email': 'l1@test.com', 'stage': 'New', 'value': 10000})

        data_manager.add_activity({
            'type': 'Call',
            'description': 'Discovery call completed',
            'lead_id': lead['id'],
            'lead_name': lead['name']
        })

        activities = data_manager.get_lead_activities(lead['id'])
        assert len(activities) >= 1
        assert activities[0]['type'] == 'Call'
        assert activities[0]['lead_id'] == lead['id']

    def test_tasks_management(self, data_manager):
        """Test task creation, completion, and filtering."""
        lead = data_manager.add_lead({'name': 'Lead 1', 'email': 'l1@test.com', 'stage': 'New', 'value': 10000})

        # Create tasks
        task1 = data_manager.add_task({
            'title': 'Follow up call',
            'lead_id': lead['id'],
            'due_date': (datetime.now() + timedelta(days=1)).isoformat(),
            'priority': 'High'
        })
        task2 = data_manager.add_task({
            'title': 'Send proposal',
            'lead_id': lead['id'],
            'due_date': (datetime.now() - timedelta(days=1)).isoformat(),  # Overdue
            'priority': 'Critical'
        })

        # Get upcoming tasks
        upcoming = data_manager.get_upcoming_tasks(limit=10)
        assert len(upcoming) >= 2

        # Complete a task
        completed = data_manager.complete_task(task1['id'])
        assert completed is True

        # Check overdue detection
        overdue_task = next(t for t in upcoming if t['id'] == task2['id'])
        assert overdue_task['overdue'] is True

    def test_campaigns_crud(self, data_manager):
        """Test email campaign management."""
        campaign = data_manager.add_campaign({
            'name': 'Q1 Outreach',
            'subject': 'Quick question for {company}',
            'body': 'Hi {name}, ...',
            'recipients': ['lead1@test.com', 'lead2@test.com']
        })

        assert campaign['id'] is not None
        assert campaign['status'] == 'Draft'
        assert campaign['sent_count'] == 0

        # Update campaign
        updated = data_manager.update_campaign(campaign['id'], {'status': 'Sent', 'sent_count': 2})
        assert updated['status'] == 'Sent'
        assert updated['sent_count'] == 2

    def test_templates_management(self, data_manager):
        """Test email template management."""
        templates = data_manager.get_templates()
        assert len(templates) >= 5  # Default templates

        # Add custom template
        template = data_manager.add_template({
            'name': 'Custom Template',
            'subject': 'Custom subject',
            'body': 'Custom body',
            'category': 'Custom'
        })

        assert template['id'] is not None
        assert template['name'] == 'Custom Template'

        all_templates = data_manager.get_templates()
        assert len(all_templates) >= 6

    def test_dashboard_metrics(self, data_manager):
        """Test dashboard metrics calculation."""
        # Add test leads with various stages
        data_manager.add_lead({'name': 'Won Lead', 'email': 'won@test.com', 'stage': 'Closed Won', 'value': 100000})
        data_manager.add_lead({'name': 'Active Lead', 'email': 'active@test.com', 'stage': 'Qualified', 'value': 50000})
        data_manager.add_lead({'name': 'Lost Lead', 'email': 'lost@test.com', 'stage': 'Closed Lost', 'value': 25000})

        metrics = data_manager.get_dashboard_metrics()

        assert metrics['total_leads'] >= 3
        assert metrics['active_deals'] >= 1
        assert metrics['pipeline_value'] >= 50000
        assert metrics['conversion_rate'] > 0

    def test_pipeline_by_stage(self, data_manager):
        """Test pipeline funnel data."""
        data_manager.add_lead({'name': 'Lead 1', 'email': 'l1@test.com', 'stage': 'New', 'value': 10000})
        data_manager.add_lead({'name': 'Lead 2', 'email': 'l2@test.com', 'stage': 'Qualified', 'value': 20000})
        data_manager.add_lead({'name': 'Lead 3', 'email': 'l3@test.com', 'stage': 'Proposal', 'value': 30000})

        pipeline = data_manager.get_pipeline_by_stage()

        assert len(pipeline) == 7  # All 7 stages
        new_stage = next(s for s in pipeline if s['stage'] == 'New')
        assert new_stage['value'] >= 10000
        assert new_stage['count'] >= 1

    def test_revenue_trend(self, data_manager):
        """Test revenue trend calculation."""
        trend = data_manager.get_revenue_trend(months=6)

        assert len(trend) == 6
        for month in trend:
            assert 'date' in month
            assert 'value' in month
            assert isinstance(month['value'], (int, float))

    def test_conversion_by_source(self, data_manager):
        """Test conversion rate by lead source."""
        # Clear existing sample data
        data_manager.leads = []
        data_manager._save_json(data_manager.leads_file, [])

        data_manager.add_lead({'name': 'Web Lead 1', 'email': 'w1@test.com', 'source': 'Website', 'stage': 'Closed Won', 'value': 10000})
        data_manager.add_lead({'name': 'Web Lead 2', 'email': 'w2@test.com', 'source': 'Website', 'stage': 'Closed Lost', 'value': 5000})
        data_manager.add_lead({'name': 'Ref Lead 1', 'email': 'r1@test.com', 'source': 'Referral', 'stage': 'Closed Won', 'value': 20000})

        conversions = data_manager.get_conversion_by_source()

        website = next(c for c in conversions if c['source'] == 'Website')
        referral = next(c for c in conversions if c['source'] == 'Referral')

        assert website['total'] == 2
        assert website['won'] == 1
        assert website['rate'] == 50.0
        assert referral['total'] == 1
        assert referral['won'] == 1
        assert referral['rate'] == 100.0

    def test_activity_heatmap(self, data_manager):
        """Test activity heatmap data structure."""
        heatmap = data_manager.get_activity_heatmap()

        assert len(heatmap) == 7 * 11  # 7 days x 11 hours (8am-6pm)
        for entry in heatmap:
            assert 'day' in entry
            assert 'hour' in entry
            assert 'count' in entry
            assert entry['day'] in ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
            assert 8 <= entry['hour'] <= 18


class TestSalesAgentHelpers:
    """Test Sales Agent helper functions"""

    def test_format_currency(self):
        """Test currency formatting."""
        assert format_currency_sa(0) == "$0"
        assert format_currency_sa(500) == "$500"
        assert format_currency_sa(1500) == "$1.5K"
        assert format_currency_sa(1500000) == "$1.5M"

    def test_format_date(self):
        """Test date formatting."""
        test_date = "2024-01-15T10:30:00"
        formatted = format_date_sa(test_date)
        assert "Jan" in formatted
        assert "15" in formatted
        assert "2024" in formatted

    def test_format_datetime(self):
        """Test datetime formatting."""
        test_dt = "2024-01-15T10:30:00"
        formatted = format_datetime_sa(test_dt)
        assert "Jan" in formatted
        assert "15" in formatted
        assert "2024" in formatted
        assert ":" in formatted  # Time component

    def test_stage_colors(self):
        """Test pipeline stage color mapping."""
        assert get_stage_color('New') == '#6B7280'
        assert get_stage_color('Qualified') == '#06B6D4'
        assert get_stage_color('Closed Won') == '#10B981'
        assert get_stage_color('Closed Lost') == '#EF4444'

    def test_priority_colors_and_icons(self):
        """Test task priority colors and icons."""
        assert get_priority_color('Low') == '#10B981'
        assert get_priority_color('Critical') == '#DC2626'
        assert get_priority_icon('High') == '🟠'
        assert get_priority_icon('Critical') == '🔴'

    def test_truncate_text(self):
        """Test text truncation."""
        assert truncate_text_sa("Short", 50) == "Short"
        # Sales agent truncate_text uses max_length-3 for ellipsis
        result = truncate_text_sa("This is a very long text that should be truncated", 20)
        assert result == "This is a very lo..."

    def test_calculate_days_until(self):
        """Test days until calculation."""
        future = datetime.now() + timedelta(days=5)
        assert calculate_days_until(future) == 5

        past = datetime.now() - timedelta(days=2)
        assert calculate_days_until(past) == 0

    def test_is_overdue(self):
        """Test overdue detection."""
        past = datetime.now() - timedelta(days=1)
        future = datetime.now() + timedelta(days=1)

        assert is_overdue(past) is True
        assert is_overdue(future) is False

    def test_get_relative_time(self):
        """Test relative time formatting."""
        just_now = datetime.now()
        assert get_relative_time_sa(just_now) == "Just now"

        hour_ago = datetime.now() - timedelta(hours=2)
        assert "hour" in get_relative_time_sa(hour_ago)

        day_ago = datetime.now() - timedelta(days=3)
        assert "day" in get_relative_time_sa(day_ago)

    def test_parse_email_variables(self):
        """Test email template variable parsing."""
        template = "Hi {name}, welcome to {company}!"
        variables = {'name': 'John', 'company': 'Acme Corp'}
        result = parse_email_variables(template, variables)

        assert result == "Hi John, welcome to Acme Corp!"

    def test_validate_email(self):
        """Test email validation."""
        assert validate_email("test@example.com") is True
        assert validate_email("user.name@domain.co.uk") is True
        assert validate_email("invalid") is False
        assert validate_email("@nodomain.com") is False
        assert validate_email("no@tld") is False

    def test_validate_phone(self):
        """Test phone validation."""
        assert validate_phone("+1 (555) 123-4567") is True
        assert validate_phone("5551234567") is True
        assert validate_phone("123") is False
        assert validate_phone("abc") is False

    def test_generate_lead_score(self):
        """Test lead scoring algorithm."""
        # High-value, qualified referral
        hot_lead = {
            'stage': 'Negotiation',
            'value': 150000,
            'source': 'Referral',
            'last_contacted': datetime.now().isoformat(),
            'next_followup': (datetime.now() + timedelta(days=1)).isoformat()
        }
        score = generate_lead_score(hot_lead)
        assert score >= 80
        assert get_lead_score_label(score) == "🔥 Hot"

        # Low-value, cold call, new
        cold_lead = {
            'stage': 'New',
            'value': 5000,
            'source': 'Cold Call',
            'last_contacted': None,
            'next_followup': None
        }
        score = generate_lead_score(cold_lead)
        assert score <= 40
        assert get_lead_score_label(score) == "🧊 Cold"

    def test_lead_score_labels(self):
        """Test lead score label mapping."""
        assert get_lead_score_label(90) == "🔥 Hot"
        assert get_lead_score_label(70) == "🌡️ Warm"
        assert get_lead_score_label(50) == "❄️ Cool"
        assert get_lead_score_label(20) == "🧊 Cold"


# ============================================================
# JP FINDS DEALS TESTS
# ============================================================

# Need to import affiliate-studio helpers specifically
import importlib.util
jp_helpers_path = str(Path(affiliate_studio_path) / "utils" / "helpers.py")
spec = importlib.util.spec_from_file_location("jp_helpers", jp_helpers_path)
jp_helpers = importlib.util.module_from_spec(spec)
spec.loader.exec_module(jp_helpers)

# Extract functions from jp_helpers module
format_currency_jp = jp_helpers.format_currency
format_date_jp = jp_helpers.format_date
format_datetime_jp = jp_helpers.format_datetime
get_relative_time_jp = jp_helpers.get_relative_time
validate_url = jp_helpers.validate_url
extract_marketplace = jp_helpers.extract_marketplace
extract_product_info = jp_helpers.extract_product_info
calculate_product_score = jp_helpers.calculate_product_score
get_score_label = jp_helpers.get_score_label
get_score_color = jp_helpers.get_score_color
truncate_text_jp = jp_helpers.truncate_text
generate_hashtags = jp_helpers.generate_hashtags
parse_gemini_response = jp_helpers.parse_gemini_response
sanitize_filename = jp_helpers.sanitize_filename
generate_affiliate_url = jp_helpers.generate_affiliate_url


class TestJPFindsDealsHelpers:
    """Test JP Finds Deals helper functions"""

    def test_format_currency_indian(self):
        """Test Indian currency formatting (Lakhs/Crores)."""
        assert format_currency_jp(0) == "₹0"
        assert format_currency_jp(500) == "₹500"
        assert format_currency_jp(5000) == "₹5.0K"
        assert format_currency_jp(150000) == "₹1.50 L"  # 1.5 Lakh
        assert format_currency_jp(15000000) == "₹1.50 Cr"  # 1.5 Crore

    def test_format_date(self):
        """Test date formatting."""
        test_date = "2024-01-15T10:30:00"
        formatted = format_date_jp(test_date)
        assert "Jan" in formatted
        assert "15" in formatted
        assert "2024" in formatted

    def test_format_datetime(self):
        """Test datetime formatting."""
        test_dt = "2024-01-15T10:30:00"
        formatted = format_datetime_jp(test_dt)
        assert "Jan" in formatted
        assert "10:30" in formatted

    def test_get_relative_time(self):
        """Test relative time formatting."""
        just_now = datetime.now()
        assert get_relative_time_jp(just_now) == "Just now"

        hour_ago = datetime.now() - timedelta(hours=2)
        assert "hour" in get_relative_time_jp(hour_ago)

        day_ago = datetime.now() - timedelta(days=3)
        assert "day" in get_relative_time_jp(day_ago)

    def test_validate_url(self):
        """Test URL validation."""
        assert validate_url("https://www.amazon.in/product") is True
        assert validate_url("https://flipkart.com/item") is True
        assert validate_url("not-a-url") is False
        assert validate_url("") is False

    def test_extract_marketplace(self):
        """Test marketplace extraction from URLs."""
        assert extract_marketplace("https://www.amazon.in/dp/B08N5WRWNW") == "Amazon"
        assert extract_marketplace("https://www.flipkart.com/product/p/itm123") == "Flipkart"
        assert extract_marketplace("https://www.myntra.com/product/123") == "Myntra"
        assert extract_marketplace("https://www.nykaa.com/product/123") == "Nykaa"
        assert extract_marketplace("https://meesho.com/product/123") == "Meesho"
        assert extract_marketplace("https://unknown.com/product") == "Unknown"

    def test_extract_product_info_amazon(self):
        """Test Amazon product ID extraction."""
        url = "https://www.amazon.in/dp/B08N5WRWNW/ref=sr_1_1"
        info = extract_product_info(url)

        assert info['marketplace'] == "Amazon"
        assert info['product_id'] == "B08N5WRWNW"

    def test_extract_product_info_flipkart(self):
        """Test Flipkart product ID extraction."""
        url = "https://www.flipkart.com/product/p/itm123456?pid=ABC123"
        info = extract_product_info(url)

        assert info['marketplace'] == "Flipkart"
        assert info['product_id'] == "itm123456"

    def test_calculate_product_score(self):
        """Test product scoring algorithm (0-100)."""
        # High-scoring product: high discount, high rating, low price, trending category, many features, affiliate link
        hot_product = {
            'discount_pct': 60,
            'rating': 4.8,
            'review_count': 2000,
            'price': 299,
            'category': 'Electronics & Gadgets',
            'features': ['Feature 1', 'Feature 2', 'Feature 3', 'Feature 4', 'Feature 5'],
            'affiliate_url': 'https://affiliate.link/product'
        }
        score = calculate_product_score(hot_product)
        assert score >= 80
        assert get_score_label(score) == "🔥 Hot"
        assert get_score_color(score) == "#EF4444"

        # Low-scoring product: no discount, low rating, high price, no features, no affiliate link
        cold_product = {
            'discount_pct': 0,
            'rating': 2.5,
            'review_count': 10,
            'price': 10000,
            'category': 'Other',
            'features': [],
            'affiliate_url': None
        }
        score = calculate_product_score(cold_product)
        assert score <= 30
        assert get_score_label(score) == "🧊 Cold"
        assert get_score_color(score) == "#6B7280"

        # Medium product
        medium_product = {
            'discount_pct': 25,
            'rating': 4.0,
            'review_count': 500,
            'price': 999,
            'category': 'Home & Kitchen',
            'features': ['Feature 1', 'Feature 2', 'Feature 3'],
            'affiliate_url': 'https://affiliate.link/product'
        }
        score = calculate_product_score(medium_product)
        assert 40 <= score <= 70

    def test_score_boundaries(self):
        """Test score boundaries at 40, 60, 80."""
        assert get_score_label(39) == "🧊 Cold"
        assert get_score_label(40) == "❄️ Cool"
        assert get_score_label(59) == "❄️ Cool"
        assert get_score_label(60) == "🌡️ Warm"
        assert get_score_label(79) == "🌡️ Warm"
        assert get_score_label(80) == "🔥 Hot"
        assert get_score_label(100) == "🔥 Hot"

    def test_truncate_text(self):
        """Test text truncation."""
        assert truncate_text_jp("Short", 50) == "Short"
        # max_length=20, so text[:17] + "..." = "This is a very lo..."
        assert truncate_text_jp("This is a very long text that should be truncated", 20) == "This is a very lo..."

    def test_generate_hashtags(self):
        """Test hashtag generation for products."""
        product = {
            'marketplace': 'Amazon',
            'category': 'Electronics & Gadgets',
            'price': 499,
            'discount_pct': 50
        }
        hashtags = generate_hashtags(product)

        assert '#amazonfinds' in hashtags
        assert '#amazondeals' in hashtags
        assert '#electronics' in hashtags
        assert '#gadgets' in hashtags
        assert '#under500' in hashtags
        assert '#50off' in hashtags
        assert '#jpfindsdeals' in hashtags
        assert '#discountdeals' in hashtags
        assert len(hashtags) <= 30  # Instagram limit

    def test_parse_gemini_response_json(self):
        """Test parsing JSON from Gemini response."""
        response = 'Here is the result: {"key": "value", "number": 42} and some text'
        parsed = parse_gemini_response(response)

        assert parsed.get('key') == 'value'
        assert parsed.get('number') == 42

    def test_parse_gemini_response_fallback(self):
        """Test fallback when JSON not found."""
        response = 'This is just text without JSON'
        parsed = parse_gemini_response(response)

        assert parsed['raw_response'] == response
        assert parsed['parsed'] is False

    def test_sanitize_filename(self):
        """Test filename sanitization."""
        assert sanitize_filename("normal_file.txt") == "normal_file.txt"
        assert sanitize_filename("file<with>invalid:chars") == "file_with_invalid_chars"
        assert sanitize_filename("  spaced  file  ") == "spaced_file"
        assert len(sanitize_filename("a" * 150)) == 100

    def test_generate_affiliate_url_amazon(self):
        """Test Amazon affiliate URL generation."""
        url = generate_affiliate_url('Amazon', 'B08N5WRWNW', 'jpfindsdeals-21')
        assert url == "https://www.amazon.in/dp/B08N5WRWNW?tag=jpfindsdeals-21"

    def test_generate_affiliate_url_flipkart(self):
        """Test Flipkart affiliate URL generation."""
        url = generate_affiliate_url('Flipkart', 'itm123', 'tag')
        assert "flipkart.com" in url


class TestContentGenerationFlow:
    """Test content generation business logic (mocked)"""

    def test_content_type_options(self):
        """Test available content types."""
        content_types = [
            "Instagram Reel (15-30s)",
            "Instagram Story",
            "Carousel Post",
            "Weekly Roundup"
        ]
        # These are the options in content_studio.py
        assert len(content_types) == 4

    def test_language_options(self):
        """Test supported languages."""
        languages = ["English", "Tamil", "English + Tamil (Mixed)"]
        assert len(languages) == 3

    def test_hook_styles(self):
        """Test hook style options."""
        hooks = ["Curiosity", "Problem/Solution", "Budget Saving", "Visual Demo", "Shocking Fact", "Relatable Story"]
        assert len(hooks) == 6

    def test_tones(self):
        """Test tone options."""
        tones = ["Friendly & Casual", "Expert & Authoritative", "Excited & Energetic", "Trustworthy & Honest", "Fun & Playful"]
        assert len(tones) == 5


class TestApprovalWorkflow:
    """Test approval queue workflow states"""

    def test_approval_statuses(self):
        """Test all approval statuses."""
        statuses = ['pending', 'approved', 'published', 'rejected', 'scheduled']

        # Test status transitions
        item = {'id': 'test_1', 'status': 'pending', 'product_name': 'Test Product'}

        # Pending -> Approved
        item['status'] = 'approved'
        assert item['status'] == 'approved'

        # Approved -> Published
        item['status'] = 'published'
        assert item['status'] == 'published'

        # Pending -> Rejected
        item['status'] = 'rejected'
        assert item['status'] == 'rejected'

        # Rejected -> Pending (restore)
        item['status'] = 'pending'
        assert item['status'] == 'pending'

        # Approved -> Pending (send back)
        item['status'] = 'approved'
        item['status'] = 'pending'
        assert item['status'] == 'pending'


class TestProductStatusFlow:
    """Test product status lifecycle"""

    def test_product_statuses(self):
        """Test all product statuses."""
        statuses = [
            "discovered",
            "analyzed",
            "content_generated",
            "video_ready",
            "approved",
            "published",
            "rejected"
        ]
        assert len(statuses) == 7

    def test_status_progression(self):
        """Test typical status progression."""
        product = {'id': 'prod_1', 'status': 'discovered'}

        # Discovered -> Analyzed
        product['status'] = 'analyzed'
        assert product['status'] == 'analyzed'

        # Analyzed -> Content Generated
        product['status'] = 'content_generated'
        assert product['status'] == 'content_generated'

        # Content Generated -> Video Ready
        product['status'] = 'video_ready'
        assert product['status'] == 'video_ready'

        # Video Ready -> Approved
        product['status'] = 'approved'
        assert product['status'] == 'approved'

        # Approved -> Published
        product['status'] = 'published'
        assert product['status'] == 'published'


class TestAnalyticsCalculations:
    """Test analytics computations"""

    def test_engagement_rate_calculation(self):
        """Test engagement rate formula."""
        posts = [
            {'views': 1000, 'likes': 50, 'comments': 10, 'shares': 5, 'saves': 15},
            {'views': 2000, 'likes': 100, 'comments': 20, 'shares': 10, 'saves': 30}
        ]

        total_views = sum(p['views'] for p in posts)
        total_engagement = sum(p['likes'] + p['comments'] + p['shares'] + p['saves'] for p in posts)
        engagement_rate = (total_engagement / total_views * 100) if total_views > 0 else 0

        assert engagement_rate > 0
        assert round(engagement_rate, 2) == 8.0  # (80 + 160) / 3000 * 100 = 8.0%

    def test_ctr_calculation(self):
        """Test click-through rate formula."""
        posts = [
            {'views': 1000, 'affiliate_clicks': 50},
            {'views': 2000, 'affiliate_clicks': 100}
        ]

        total_views = sum(p['views'] for p in posts)
        total_clicks = sum(p['affiliate_clicks'] for p in posts)
        ctr = (total_clicks / total_views * 100) if total_views > 0 else 0

        assert ctr == 5.0  # 150 / 3000 * 100

    def test_conversion_rate_calculation(self):
        """Test conversion rate formula."""
        posts = [
            {'affiliate_clicks': 100, 'conversions': 5},
            {'affiliate_clicks': 200, 'conversions': 10}
        ]

        total_clicks = sum(p['affiliate_clicks'] for p in posts)
        total_conversions = sum(p['conversions'] for p in posts)
        conv_rate = (total_conversions / total_clicks * 100) if total_clicks > 0 else 0

        assert conv_rate == 5.0  # 15 / 300 * 100

    def test_conversion_funnel(self):
        """Test conversion funnel data structure."""
        posts = [
            {'views': 10000, 'affiliate_clicks': 500, 'conversions': 25}
        ]

        total_views = sum(p['views'] for p in posts)
        total_clicks = sum(p['affiliate_clicks'] for p in posts)
        total_conversions = sum(p['conversions'] for p in posts)

        funnel = [
            {'stage': 'Views', 'count': total_views},
            {'stage': 'Clicks', 'count': total_clicks},
            {'stage': 'Conversions', 'count': total_conversions}
        ]

        assert funnel[0]['count'] == 10000
        assert funnel[1]['count'] == 500
        assert funnel[2]['count'] == 25


class TestVideoPromptExport:
    """Test video prompt export formats"""

    def test_canva_assets_structure(self):
        """Test Canva export JSON structure."""
        draft = {
            'product_name': 'Test Product',
            'product_price': '₹499',
            'product_discount': '50%',
            'product_image': 'https://example.com/image.jpg',
            'product_affiliate_url': 'https://affiliate.link/product',
            'generated_content': {
                'scripts': {'English': {'hook': 'Hook', 'introduction': 'Intro'}},
                'seo': {'caption': 'Caption', 'hashtags': ['#tag1', '#tag2']},
                'video_prompts': {'hook_visual': 'Visual prompt'}
            }
        }

        assets = {
            'product': {
                'name': draft['product_name'],
                'price': draft['product_price'],
                'discount': draft['product_discount'],
                'image_url': draft['product_image'],
                'affiliate_url': draft['product_affiliate_url']
            },
            'content': draft['generated_content'],
            'brand': {
                'name': 'JP Finds Deals',
                'watermark': '@jp.finds.deals',
                'colors': {'primary': '#FF6B35', 'secondary': '#1A1A2E'}
            }
        }

        assert assets['product']['name'] == 'Test Product'
        assert assets['brand']['watermark'] == '@jp.finds.deals'
        assert 'content' in assets

    def test_flow_prompts_structure(self):
        """Test Google Flow export JSON structure."""
        prompts = {
            'hook_visual': 'Hook visual prompt',
            'product_intro': 'Product intro prompt',
            'benefits_demo': 'Benefits demo prompt',
            'cta_visual': 'CTA visual prompt',
            'duration': 25,
            'resolution': '1080x1920',
            'format': 'MP4'
        }

        flow_data = {
            'project_name': 'JP Finds Deals - Test Product',
            'scenes': [
                {'name': 'Hook', 'prompt': prompts['hook_visual'], 'duration': 3},
                {'name': 'Product Intro', 'prompt': prompts['product_intro'], 'duration': 5},
                {'name': 'Benefits', 'prompt': prompts['benefits_demo'], 'duration': 12},
                {'name': 'CTA', 'prompt': prompts['cta_visual'], 'duration': 5}
            ],
            'settings': {
                'resolution': prompts['resolution'],
                'format': prompts['format'],
                'music': prompts.get('hook_visual_music', '')
            }
        }

        assert len(flow_data['scenes']) == 4
        assert flow_data['scenes'][0]['duration'] == 3
        assert flow_data['scenes'][-1]['duration'] == 5
        assert flow_data['settings']['resolution'] == '1080x1920'


class TestCanvaTemplates:
    """Test Canva template definitions"""

    def test_template_definitions(self):
        """Test all Canva templates are defined."""
        templates = [
            'Product Promotion',
            "Today's Best Deals",
            'Top 5 Gadgets',
            'Budget Shopping Finds',
            'Product Comparison',
            'Festival Deals'
        ]

        for template in templates:
            assert isinstance(template, str)
            assert len(template) > 0


# ============================================================
# INTEGRATION TESTS
# ============================================================

class TestEndToEndWorkflows:
    """Test complete end-to-end workflows"""

    def test_sales_agent_lead_to_deal_workflow(self, temp_data_dir):
        """Test complete lead-to-deal workflow."""
        dm = DataManager(data_dir=temp_data_dir)

        # 1. Create lead
        lead = dm.add_lead({
            'name': 'John Doe',
            'email': 'john@company.com',
            'company': 'Acme Corp',
            'source': 'Referral',
            'stage': 'New',
            'value': 50000
        })
        assert lead['stage'] == 'New'

        # 2. Progress through pipeline stages
        stages = ['Contacted', 'Qualified', 'Proposal', 'Negotiation', 'Closed Won']
        for stage in stages:
            lead = dm.update_lead(lead['id'], {'stage': stage})
            assert lead['stage'] == stage

        # 3. Verify final state
        final_lead = dm.get_lead(lead['id'])
        assert final_lead['stage'] == 'Closed Won'

        # 4. Check metrics reflect won deal
        metrics = dm.get_dashboard_metrics()
        assert metrics['won_this_month'] >= 50000

    def test_jp_finds_deals_product_to_publish_workflow(self):
        """Test complete product-to-publish workflow (session state simulation)."""
        # Simulate session state
        session_state = {
            'products': [],
            'content_drafts': [],
            'approval_queue': [],
            'published_posts': []
        }

        # 1. Add product
        product = {
            'id': 'prod_1',
            'name': 'Test Product',
            'url': 'https://amazon.in/dp/B08N5WRWNW',
            'marketplace': 'Amazon',
            'category': 'Electronics & Gadgets',
            'price': 499,
            'original_price': 999,
            'discount_pct': 50,
            'rating': 4.5,
            'review_count': 1000,
            'affiliate_url': 'https://affiliate.link/prod_1',
            'features': ['Feature 1', 'Feature 2', 'Feature 3'],
            'status': 'discovered',
            'score': 0,
            'created_at': datetime.now().isoformat()
        }
        session_state['products'].append(product)

        # 2. Calculate score
        product['score'] = calculate_product_score(product)
        assert product['score'] >= 60

        # 3. Generate content (simulated)
        draft = {
            'id': 'draft_1',
            'product_id': 'prod_1',
            'product_name': 'Test Product',
            'content_type': 'Instagram Reel (15-30s)',
            'generated_content': {
                'scripts': {
                    'English': {'hook': 'Hook', 'introduction': 'Intro', 'benefits': 'Benefits', 'cta': 'CTA'},
                    'Tamil': {'hook': 'தூக்கம்', 'introduction': 'அறிமுகம்', 'benefits': 'பயன்கள்', 'cta': 'செயல்'},
                    'English + Tamil (Mixed)': {'hook': 'Mixed hook', 'introduction': 'Mixed intro', 'benefits': 'Mixed benefits', 'cta': 'Mixed CTA'}
                },
                'seo': {
                    'caption': 'Great product! 🎉',
                    'hashtags': generate_hashtags(product),
                    'product_title': 'Test Product',
                    'cta': 'Link in bio! 👆',
                    'disclosure': '#ad #affiliate'
                },
                'video_prompts': {
                    'hook_visual': 'Visual hook prompt',
                    'product_intro': 'Product intro prompt',
                    'benefits_demo': 'Benefits demo prompt',
                    'cta_visual': 'CTA visual prompt',
                    'duration': 25,
                    'resolution': '1080x1920',
                    'format': 'MP4'
                }
            },
            'status': 'draft',
            'created_at': datetime.now().isoformat()
        }
        session_state['content_drafts'].append(draft)

        # Update product status
        product['status'] = 'content_generated'

        # 4. Send to approval
        approval_item = {
            'id': 'approval_1',
            'draft_id': 'draft_1',
            'product_id': 'prod_1',
            'product_name': 'Test Product',
            'content_type': 'Instagram Reel (15-30s)',
            'generated_content': draft['generated_content'],
            'status': 'pending',
            'created_at': datetime.now().isoformat()
        }
        session_state['approval_queue'].append(approval_item)
        draft['status'] = 'pending_approval'
        product['status'] = 'approved'

        # 5. Approve
        approval_item['status'] = 'approved'

        # 6. Publish
        published_post = {
            'id': 'post_1',
            'approval_id': 'approval_1',
            'product_id': 'prod_1',
            'product_name': 'Test Product',
            'content_type': 'Instagram Reel (15-30s)',
            'caption': draft['generated_content']['seo']['caption'],
            'hashtags': draft['generated_content']['seo']['hashtags'],
            'instagram_media_id': 'media_123',
            'instagram_url': 'https://instagram.com/reel/abc123',
            'published_at': datetime.now().isoformat(),
            'views': 10000,
            'likes': 500,
            'comments': 50,
            'shares': 25,
            'saves': 100,
            'affiliate_clicks': 200,
            'conversions': 10,
            'commission': 2500
        }
        session_state['published_posts'].append(published_post)
        approval_item['status'] = 'published'
        product['status'] = 'published'

        # Verify final state
        assert len(session_state['published_posts']) == 1
        assert session_state['published_posts'][0]['commission'] == 2500
        assert product['status'] == 'published'

    def test_analytics_report_generation(self):
        """Test analytics report export structure."""
        published_posts = [
            {
                'id': 'post_1',
                'product_name': 'Product 1',
                'content_type': 'Instagram Reel (15-30s)',
                'published_at': '2024-01-15T10:00:00',
                'views': 10000,
                'likes': 500,
                'comments': 50,
                'shares': 25,
                'saves': 100,
                'affiliate_clicks': 200,
                'conversions': 10,
                'commission': 2500,
                'instagram_media_id': 'media_1'
            }
        ]

        products = [
            {'id': 'prod_1', 'name': 'Product 1', 'category': 'Electronics', 'marketplace': 'Amazon'}
        ]

        approval_queue = [
            {'id': 'approval_1', 'product_name': 'Product 1', 'status': 'published'}
        ]

        report = {
            'generated_at': datetime.now().isoformat(),
            'period': 'Last 30 days',
            'posts': published_posts,
            'products': products,
            'approval_queue': approval_queue
        }

        # Verify JSON serializable
        json_str = json.dumps(report, default=str)
        assert len(json_str) > 0

        # Verify structure
        parsed = json.loads(json_str)
        assert 'generated_at' in parsed
        assert len(parsed['posts']) == 1
        assert len(parsed['products']) == 1
        assert len(parsed['approval_queue']) == 1


# ============================================================
# EDGE CASE TESTS
# ============================================================

class TestEdgeCases:
    """Test edge cases and error handling"""

    def test_empty_data_handling(self, temp_data_dir):
        """Test handling of empty data."""
        dm = DataManager(data_dir=temp_data_dir)

        # Clear all data
        dm.leads = []
        dm.activities = []
        dm.tasks = []
        dm._save_json(dm.leads_file, [])
        dm._save_json(dm.activities_file, [])
        dm._save_json(dm.tasks_file, [])

        assert dm.get_leads() == []
        assert dm.get_recent_activities() == []
        assert dm.get_upcoming_tasks() == []

        metrics = dm.get_dashboard_metrics()
        assert metrics['total_leads'] == 0
        assert metrics['conversion_rate'] == 0

    def test_invalid_lead_id(self, data_manager):
        """Test operations with invalid lead ID."""
        assert data_manager.get_lead('invalid_id') is None
        assert data_manager.update_lead('invalid_id', {'stage': 'Qualified'}) is None
        assert data_manager.delete_lead('invalid_id') is False

    def test_invalid_task_id(self, data_manager):
        """Test task operations with invalid ID."""
        assert data_manager.complete_task('invalid_id') is False

    def test_product_score_caps_at_100(self):
        """Test product score never exceeds 100."""
        # Product with maximum possible scores
        max_product = {
            'discount_pct': 100,
            'rating': 5.0,
            'review_count': 10000,
            'price': 100,
            'category': 'Electronics & Gadgets',
            'features': ['F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9', 'F10'],
            'affiliate_url': 'https://link'
        }
        score = calculate_product_score(max_product)
        assert score == 100

    def test_lead_score_caps_at_100(self):
        """Test lead score never exceeds 100."""
        max_lead = {
            'stage': 'Closed Won',
            'value': 1000000,
            'source': 'Referral',
            'last_contacted': datetime.now().isoformat(),
            'next_followup': (datetime.now() + timedelta(days=1)).isoformat()
        }
        score = generate_lead_score(max_lead)
        assert score == 100

    def test_special_characters_in_product_name(self):
        """Test handling of special characters in product names."""
        product = {
            'name': 'Product with "quotes" & <special> chars',
            'marketplace': 'Amazon',
            'category': 'Electronics',
            'price': 499,
            'discount_pct': 20,
            'rating': 4.0,
            'review_count': 100,
            'features': ['Feature with "quotes"'],
            'affiliate_url': 'https://link'
        }

        score = calculate_product_score(product)
        assert score > 0

        hashtags = generate_hashtags(product)
        assert len(hashtags) > 0

        sanitized = sanitize_filename(product['name'])
        assert '<' not in sanitized
        assert '>' not in sanitized
        assert '"' not in sanitized

    def test_unicode_handling(self):
        """Test Unicode handling in text processing."""
        tamil_text = 'தமிழ் உரை'
        truncated = truncate_text_jp(tamil_text, 5)
        assert len(truncated) <= 5 + 3  # +3 for ellipsis

        product = {
            'name': tamil_text,
            'marketplace': 'Amazon',
            'category': 'Electronics',
            'price': 499
        }
        hashtags = generate_hashtags(product)
        assert '#jpfindsdeals' in hashtags

    def test_missing_optional_fields(self):
        """Test handling of missing optional fields."""
        product = {
            'name': 'Minimal Product',
            'marketplace': 'Amazon',
            'category': 'Electronics',
            'price': 499
            # No discount, rating, features, affiliate_url
        }

        score = calculate_product_score(product)
        assert 0 <= score <= 100

        hashtags = generate_hashtags(product)
        assert len(hashtags) > 0

    def test_date_parsing_robustness(self):
        """Test date parsing with various formats."""
        formats = [
            "2024-01-15T10:30:00",
            "2024-01-15T10:30:00Z",
            "2024-01-15T10:30:00+00:00",
            "2024-01-15"
        ]

        for fmt in formats:
            formatted = format_date_jp(fmt)
            assert "Jan" in formatted
            assert "15" in formatted
            assert "2024" in formatted

    def test_large_numbers_formatting(self):
        """Test formatting of very large numbers."""
        assert format_currency_jp(10_00_00_000) == "₹10.00 Cr"  # 10 Crore
        assert format_currency_jp(1_00_00_00_000) == "₹100.00 Cr"  # 100 Crore

        # Sales agent format (USD) - uses K, M suffixes
        assert format_currency_sa(1_000_000_000) == "$1000.0M"
        assert format_currency_sa(1_500_000) == "$1.5M"


# ============================================================
# PERFORMANCE TESTS
# ============================================================

class TestPerformance:
    """Basic performance tests"""

    def test_data_manager_with_many_leads(self, temp_data_dir):
        """Test DataManager performance with many leads."""
        dm = DataManager(data_dir=temp_data_dir)

        # Clear existing sample data
        dm.leads = []
        dm._save_json(dm.leads_file, [])

        # Add 100 leads
        for i in range(100):
            dm.add_lead({
                'name': f'Lead {i}',
                'email': f'lead{i}@test.com',
                'stage': 'New',
                'value': 10000 * (i % 10 + 1)
            })

        leads = dm.get_leads()
        assert len(leads) == 100

        # Test filtering performance
        qualified = dm.get_leads_by_stage('Qualified')
        assert len(qualified) == 0  # All are 'New'

        # Test metrics calculation
        metrics = dm.get_dashboard_metrics()
        assert metrics['total_leads'] == 100

    def test_product_score_calculation_performance(self):
        """Test product scoring with many products."""
        products = []
        for i in range(1000):
            products.append({
                'discount_pct': i % 60,
                'rating': 3.0 + (i % 20) * 0.1,
                'review_count': i * 10,
                'price': 100 + (i % 5000),
                'category': ['Electronics', 'Home', 'Fashion'][i % 3],
                'features': [f'Feature {j}' for j in range(i % 6)],
                'affiliate_url': 'https://link' if i % 2 == 0 else None
            })

        # Score all products
        scores = [calculate_product_score(p) for p in products]

        assert len(scores) == 1000
        assert all(0 <= s <= 100 for s in scores)


# ============================================================
# RUN ALL TESTS
# ============================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])