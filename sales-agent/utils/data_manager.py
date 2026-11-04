"""
Data Manager for Sales Agent - Handles all data operations.
Uses JSON files for persistence (can be replaced with database).
"""

import json
import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Any, Optional
import uuid


class DataManager:
    """Manages all data operations for the Sales Agent app."""

    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)

        # Data file paths
        self.leads_file = self.data_dir / "leads.json"
        self.activities_file = self.data_dir / "activities.json"
        self.tasks_file = self.data_dir / "tasks.json"
        self.campaigns_file = self.data_dir / "campaigns.json"
        self.templates_file = self.data_dir / "templates.json"

        # Initialize data files if they don't exist
        self._init_data_files()

        # Load data
        self.leads = self._load_json(self.leads_file, [])
        self.activities = self._load_json(self.activities_file, [])
        self.tasks = self._load_json(self.tasks_file, [])
        self.campaigns = self._load_json(self.campaigns_file, [])
        self.templates = self._load_json(self.templates_file, self._get_default_templates())

    def _init_data_files(self):
        """Initialize data files with sample data if empty."""
        if not self.leads_file.exists():
            self._save_json(self.leads_file, self._get_sample_leads())
        if not self.activities_file.exists():
            self._save_json(self.activities_file, self._get_sample_activities())
        if not self.tasks_file.exists():
            self._save_json(self.tasks_file, self._get_sample_tasks())
        if not self.campaigns_file.exists():
            self._save_json(self.campaigns_file, [])
        if not self.templates_file.exists():
            self._save_json(self.templates_file, self._get_default_templates())

    def _load_json(self, filepath: Path, default: Any) -> Any:
        """Load JSON data from file."""
        try:
            with open(filepath, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return default

    def _save_json(self, filepath: Path, data: Any):
        """Save JSON data to file."""
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2, default=str)

    def _generate_id(self) -> str:
        """Generate unique ID."""
        return str(uuid.uuid4())[:8]

    # ==================== LEADS ====================

    def get_leads(self) -> List[Dict]:
        """Get all leads."""
        return self.leads

    def get_lead(self, lead_id: str) -> Optional[Dict]:
        """Get a specific lead by ID."""
        for lead in self.leads:
            if lead['id'] == lead_id:
                return lead
        return None

    def add_lead(self, lead_data: Dict) -> Dict:
        """Add a new lead."""
        lead = {
            'id': self._generate_id(),
            'name': lead_data.get('name', ''),
            'email': lead_data.get('email', ''),
            'phone': lead_data.get('phone', ''),
            'company': lead_data.get('company', ''),
            'source': lead_data.get('source', 'Website'),
            'stage': lead_data.get('stage', 'New'),
            'value': lead_data.get('value', 0),
            'assigned_to': lead_data.get('assigned_to', 'Me'),
            'notes': lead_data.get('notes', ''),
            'tags': lead_data.get('tags', []),
            'created_at': lead_data.get('created_at', datetime.now().isoformat()),
            'updated_at': datetime.now().isoformat(),
            'last_contacted': None,
            'next_followup': None
        }
        self.leads.append(lead)
        self._save_json(self.leads_file, self.leads)
        self._add_activity({
            'type': 'Lead Created',
            'description': f"New lead added: {lead['name']}",
            'lead_id': lead['id'],
            'lead_name': lead['name']
        })
        return lead

    def update_lead(self, lead_id: str, updates: Dict) -> Optional[Dict]:
        """Update a lead."""
        for i, lead in enumerate(self.leads):
            if lead['id'] == lead_id:
                self.leads[i].update(updates)
                self.leads[i]['updated_at'] = datetime.now().isoformat()
                self._save_json(self.leads_file, self.leads)
                self._add_activity({
                    'type': 'Lead Updated',
                    'description': f"Lead updated: {self.leads[i]['name']}",
                    'lead_id': lead_id,
                    'lead_name': self.leads[i]['name']
                })
                return self.leads[i]
        return None

    def delete_lead(self, lead_id: str) -> bool:
        """Delete a lead."""
        for i, lead in enumerate(self.leads):
            if lead['id'] == lead_id:
                name = lead['name']
                self.leads.pop(i)
                self._save_json(self.leads_file, self.leads)
                self._add_activity({
                    'type': 'Lead Deleted',
                    'description': f"Lead deleted: {name}",
                    'lead_id': lead_id,
                    'lead_name': name
                })
                return True
        return False

    def get_leads_by_stage(self, stage: str) -> List[Dict]:
        """Get leads filtered by stage."""
        return [lead for lead in self.leads if lead['stage'] == stage]

    def get_leads_by_assignee(self, assignee: str) -> List[Dict]:
        """Get leads filtered by assignee."""
        return [lead for lead in self.leads if lead['assigned_to'] == assignee]

    # ==================== ACTIVITIES ====================

    def _add_activity(self, activity_data: Dict):
        """Add an activity record."""
        activity = {
            'id': self._generate_id(),
            'type': activity_data.get('type', 'Note'),
            'description': activity_data.get('description', ''),
            'lead_id': activity_data.get('lead_id'),
            'lead_name': activity_data.get('lead_name'),
            'user': activity_data.get('user', 'Current User'),
            'timestamp': datetime.now().isoformat()
        }
        self.activities.insert(0, activity)
        # Keep only last 1000 activities
        self.activities = self.activities[:1000]
        self._save_json(self.activities_file, self.activities)

    def get_recent_activities(self, limit: int = 20) -> List[Dict]:
        """Get recent activities."""
        activities = self.activities[:limit]
        for act in activities:
            act['time'] = datetime.fromisoformat(act['timestamp']).strftime('%H:%M')
            act['date'] = datetime.fromisoformat(act['timestamp']).strftime('%b %d')
        return activities

    def get_lead_activities(self, lead_id: str) -> List[Dict]:
        """Get activities for a specific lead."""
        return [a for a in self.activities if a.get('lead_id') == lead_id]

    def add_activity(self, activity_data: Dict):
        """Public method to add activity."""
        self._add_activity(activity_data)

    # ==================== TASKS ====================

    def get_tasks(self, lead_id: str = None) -> List[Dict]:
        """Get all tasks, optionally filtered by lead."""
        if lead_id:
            return [t for t in self.tasks if t.get('lead_id') == lead_id]
        return self.tasks

    def get_upcoming_tasks(self, limit: int = 10) -> List[Dict]:
        """Get upcoming tasks sorted by due date."""
        now = datetime.now()
        upcoming = []
        for task in self.tasks:
            if not task.get('completed', False):
                due = datetime.fromisoformat(task['due_date'])
                task_copy = task.copy()
                task_copy['overdue'] = due < now
                task_copy['due_date_formatted'] = due.strftime('%b %d, %Y')
                upcoming.append(task_copy)

        upcoming.sort(key=lambda x: datetime.fromisoformat(x['due_date']))
        return upcoming[:limit]

    def add_task(self, task_data: Dict) -> Dict:
        """Add a new task."""
        task = {
            'id': self._generate_id(),
            'title': task_data.get('title', ''),
            'description': task_data.get('description', ''),
            'lead_id': task_data.get('lead_id'),
            'lead_name': task_data.get('lead_name', ''),
            'due_date': task_data.get('due_date', (datetime.now() + timedelta(days=1)).isoformat()),
            'priority': task_data.get('priority', 'Medium'),
            'type': task_data.get('type', 'Call'),
            'completed': False,
            'created_at': datetime.now().isoformat()
        }
        self.tasks.append(task)
        self._save_json(self.tasks_file, self.tasks)
        return task

    def complete_task(self, task_id: str) -> bool:
        """Mark a task as complete."""
        for task in self.tasks:
            if task['id'] == task_id:
                task['completed'] = True
                task['completed_at'] = datetime.now().isoformat()
                self._save_json(self.tasks_file, self.tasks)
                return True
        return False

    def update_task(self, task_id: str, updates: Dict) -> Optional[Dict]:
        """Update a task."""
        for task in self.tasks:
            if task['id'] == task_id:
                task.update(updates)
                self._save_json(self.tasks_file, self.tasks)
                return task
        return None

    # ==================== CAMPAIGNS ====================

    def get_campaigns(self) -> List[Dict]:
        """Get all campaigns."""
        return self.campaigns

    def add_campaign(self, campaign_data: Dict) -> Dict:
        """Add a new campaign."""
        campaign = {
            'id': self._generate_id(),
            'name': campaign_data.get('name', ''),
            'subject': campaign_data.get('subject', ''),
            'body': campaign_data.get('body', ''),
            'status': 'Draft',
            'recipients': campaign_data.get('recipients', []),
            'sent_count': 0,
            'open_count': 0,
            'click_count': 0,
            'reply_count': 0,
            'created_at': datetime.now().isoformat(),
            'sent_at': None
        }
        self.campaigns.append(campaign)
        self._save_json(self.campaigns_file, self.campaigns)
        return campaign

    def update_campaign(self, campaign_id: str, updates: Dict) -> Optional[Dict]:
        """Update a campaign."""
        for campaign in self.campaigns:
            if campaign['id'] == campaign_id:
                campaign.update(updates)
                self._save_json(self.campaigns_file, self.campaigns)
                return campaign
        return None

    # ==================== TEMPLATES ====================

    def get_templates(self) -> List[Dict]:
        """Get all email templates."""
        return self.templates

    def add_template(self, template_data: Dict) -> Dict:
        """Add a new template."""
        template = {
            'id': self._generate_id(),
            'name': template_data.get('name', ''),
            'subject': template_data.get('subject', ''),
            'body': template_data.get('body', ''),
            'category': template_data.get('category', 'General'),
            'created_at': datetime.now().isoformat()
        }
        self.templates.append(template)
        self._save_json(self.templates_file, self.templates)
        return template

    def _get_default_templates(self) -> List[Dict]:
        """Get default email templates."""
        return [
            {
                'id': 'tpl_001',
                'name': 'Initial Cold Outreach',
                'category': 'Cold Outreach',
                'subject': 'Quick question for {company}',
                'body': '''Hi {name},

I noticed {company} has been {trigger_event} and thought you might be interested in how we helped {similar_company} achieve {result}.

We specialize in helping companies like yours {value_prop}. Would you be open to a brief 15-minute call to see if there's a fit?

Best regards,
{sender_name}''',
                'created_at': datetime.now().isoformat()
            },
            {
                'id': 'tpl_002',
                'name': 'Follow-up After No Response',
                'category': 'Follow-up',
                'subject': 'Re: Quick question for {company}',
                'body': '''Hi {name},

Just floating this to the top of your inbox in case you missed my previous note.

I genuinely believe we could help {company} with {value_prop}. Even if it's not the right time, I'd love to stay in touch for the future.

No pressure either way!

Best,
{sender_name}''',
                'created_at': datetime.now().isoformat()
            },
            {
                'id': 'tpl_003',
                'name': 'Proposal Follow-up',
                'category': 'Proposal',
                'subject': 'Proposal for {company} - {proposal_name}',
                'body': ''''Hi {name},

I wanted to follow up on the proposal I sent over for {proposal_name}.

I know you're evaluating options, and I'm happy to walk through any questions or concerns you might have. I've also attached a brief case study showing how {similar_company} achieved {result} with our solution.

Would Thursday or Friday work for a quick 15-min call?

Best,
{sender_name}''',
                'created_at': datetime.now().isoformat()
            },
            {
                'id': 'tpl_004',
                'name': 'Referral Request',
                'category': 'Referral',
                'subject': 'Introduction to {target_person}?',
                'body': '''Hi {name},

I hope you're doing well! I'm reaching out because I'm trying to connect with {target_person} at {target_company} regarding {reason}.

Given your relationship, would you be comfortable making an introduction? I'd really appreciate it, and I'm happy to draft a brief blurb to make it easy.

Thanks in advance!
{sender_name}''',
                'created_at': datetime.now().isoformat()
            },
            {
                'id': 'tpl_005',
                'name': 'Meeting Confirmation',
                'category': 'Meeting',
                'subject': 'Confirmed: {meeting_topic} on {date}',
                'body': '''Hi {name},

Just confirming our {meeting_type} for {date} at {time} ({timezone}).

**Agenda:**
{agenda}

**Meeting Link:** {meeting_link}

Looking forward to our conversation!

Best,
{sender_name}''',
                'created_at': datetime.now().isoformat()
            }
        ]

    # ==================== ANALYTICS ====================

    def get_dashboard_metrics(self) -> Dict:
        """Get dashboard metrics."""
        now = datetime.now()
        month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        last_month_start = (month_start - timedelta(days=1)).replace(day=1)

        total_leads = len(self.leads)
        active_deals = len([l for l in self.leads if l['stage'] not in ['Closed Won', 'Closed Lost', 'New']])
        pipeline_value = sum(l['value'] for l in self.leads if l['stage'] not in ['Closed Won', 'Closed Lost'])

        won_this_month = sum(
            l['value'] for l in self.leads
            if l['stage'] == 'Closed Won' and
            datetime.fromisoformat(l['updated_at']) >= month_start
        )

        # Calculate changes (simplified)
        last_month_leads = len([l for l in self.leads if datetime.fromisoformat(l['created_at']) < month_start])
        last_month_won = sum(
            l['value'] for l in self.leads
            if l['stage'] == 'Closed Won' and
            last_month_start <= datetime.fromisoformat(l['updated_at']) < month_start
        )

        conversion_rate = 0
        closed_leads = [l for l in self.leads if l['stage'] in ['Closed Won', 'Closed Lost']]
        if closed_leads:
            won_leads = [l for l in closed_leads if l['stage'] == 'Closed Won']
            conversion_rate = (len(won_leads) / len(closed_leads)) * 100

        return {
            'total_leads': total_leads,
            'leads_change': total_leads - last_month_leads,
            'active_deals': active_deals,
            'deals_change': 0,  # Simplified
            'pipeline_value': pipeline_value,
            'pipeline_change': 0,
            'won_this_month': won_this_month,
            'won_change': won_this_month - last_month_won,
            'conversion_rate': conversion_rate,
            'conversion_change': 0
        }

    def get_pipeline_by_stage(self) -> List[Dict]:
        """Get pipeline value grouped by stage."""
        stages = ['New', 'Contacted', 'Qualified', 'Proposal', 'Negotiation', 'Closed Won', 'Closed Lost']
        result = []
        for stage in stages:
            value = sum(l['value'] for l in self.leads if l['stage'] == stage)
            count = len([l for l in self.leads if l['stage'] == stage])
            result.append({
                'stage': stage,
                'value': value,
                'count': count
            })
        return result

    def get_revenue_trend(self, months: int = 12) -> List[Dict]:
        """Get revenue trend for the last N months."""
        result = []
        now = datetime.now()

        for i in range(months):
            month_start = (now.replace(day=1) - timedelta(days=30*i)).replace(day=1)
            month_end = (month_start + timedelta(days=32)).replace(day=1) - timedelta(days=1)

            won_value = sum(
                l['value'] for l in self.leads
                if l['stage'] == 'Closed Won' and
                month_start <= datetime.fromisoformat(l['updated_at']) <= month_end
            )

            result.append({
                'date': month_start.strftime('%b %Y'),
                'value': won_value
            })

        return list(reversed(result))

    def get_pipeline_value(self) -> float:
        """Get total pipeline value."""
        return sum(l['value'] for l in self.leads if l['stage'] not in ['Closed Won', 'Closed Lost'])

    def get_conversion_by_source(self) -> List[Dict]:
        """Get conversion rates by lead source."""
        sources = {}
        for lead in self.leads:
            source = lead.get('source', 'Unknown')
            if source not in sources:
                sources[source] = {'total': 0, 'won': 0}
            sources[source]['total'] += 1
            if lead['stage'] == 'Closed Won':
                sources[source]['won'] += 1

        result = []
        for source, data in sources.items():
            rate = (data['won'] / data['total'] * 100) if data['total'] > 0 else 0
            result.append({
                'source': source,
                'total': data['total'],
                'won': data['won'],
                'rate': rate
            })

        return sorted(result, key=lambda x: x['rate'], reverse=True)

    def get_activity_heatmap(self) -> List[Dict]:
        """Get activity data for heatmap."""
        # Simplified - return activity counts by day of week and hour
        days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        hours = list(range(8, 19))  # 8am to 6pm

        result = []
        for day_idx, day in enumerate(days):
            for hour in hours:
                count = len([
                    a for a in self.activities
                    if datetime.fromisoformat(a['timestamp']).weekday() == day_idx and
                    datetime.fromisoformat(a['timestamp']).hour == hour
                ])
                result.append({
                    'day': day,
                    'hour': hour,
                    'count': count
                })
        return result

    # ==================== SAMPLE DATA ====================

    def _get_sample_leads(self) -> List[Dict]:
        """Generate sample leads."""
        sample_leads = [
            {
                'id': 'lead_001',
                'name': 'Sarah Johnson',
                'email': 'sarah.johnson@techcorp.com',
                'phone': '+1 (555) 123-4567',
                'company': 'TechCorp Inc',
                'source': 'Website',
                'stage': 'Qualified',
                'value': 50000,
                'assigned_to': 'Me',
                'notes': 'Interested in enterprise plan. Decision maker. Budget approved.',
                'tags': ['enterprise', 'decision-maker'],
                'created_at': (datetime.now() - timedelta(days=15)).isoformat(),
                'updated_at': (datetime.now() - timedelta(days=2)).isoformat(),
                'last_contacted': (datetime.now() - timedelta(days=2)).isoformat(),
                'next_followup': (datetime.now() + timedelta(days=3)).isoformat()
            },
            {
                'id': 'lead_002',
                'name': 'Michael Chen',
                'email': 'mchen@startupxyz.com',
                'phone': '+1 (555) 234-5678',
                'company': 'StartupXYZ',
                'source': 'Referral',
                'stage': 'Proposal',
                'value': 25000,
                'assigned_to': 'Me',
                'notes': 'Referred by Sarah Johnson. Sent proposal last week. Waiting for feedback.',
                'tags': ['referral', 'proposal-sent'],
                'created_at': (datetime.now() - timedelta(days=30)).isoformat(),
                'updated_at': (datetime.now() - timedelta(days=5)).isoformat(),
                'last_contacted': (datetime.now() - timedelta(days=5)).isoformat(),
                'next_followup': (datetime.now() + timedelta(days=2)).isoformat()
            },
            {
                'id': 'lead_003',
                'name': 'Emily Davis',
                'email': 'emily.davis@globaltech.com',
                'phone': '+1 (555) 345-6789',
                'company': 'GlobalTech Solutions',
                'source': 'Cold Call',
                'stage': 'Negotiation',
                'value': 75000,
                'assigned_to': 'Me',
                'notes': 'Negotiating contract terms. Legal review in progress. Close by end of quarter.',
                'tags': ['negotiation', 'high-value'],
                'created_at': (datetime.now() - timedelta(days=45)).isoformat(),
                'updated_at': (datetime.now() - timedelta(days=1)).isoformat(),
                'last_contacted': (datetime.now() - timedelta(days=1)).isoformat(),
                'next_followup': (datetime.now() + timedelta(days=1)).isoformat()
            },
            {
                'id': 'lead_004',
                'name': 'James Wilson',
                'email': 'jwilson@innovate.io',
                'phone': '+1 (555) 456-7890',
                'company': 'Innovate.io',
                'source': 'Event',
                'stage': 'Contacted',
                'value': 15000,
                'assigned_to': 'Me',
                'notes': 'Met at SaaS Conference. Sent follow-up email. Need to schedule demo.',
                'tags': ['event', 'needs-demo'],
                'created_at': (datetime.now() - timedelta(days=10)).isoformat(),
                'updated_at': (datetime.now() - timedelta(days=8)).isoformat(),
                'last_contacted': (datetime.now() - timedelta(days=8)).isoformat(),
                'next_followup': (datetime.now() + timedelta(days=1)).isoformat()
            },
            {
                'id': 'lead_005',
                'name': 'Lisa Anderson',
                'email': 'landerson@meridian.com',
                'phone': '+1 (555) 567-8901',
                'company': 'Meridian Systems',
                'source': 'Email Campaign',
                'stage': 'New',
                'value': 30000,
                'assigned_to': 'Me',
                'notes': 'Downloaded whitepaper. Opened emails 3x. Not yet contacted.',
                'tags': ['engaged', 'marketing-qualified'],
                'created_at': (datetime.now() - timedelta(days=3)).isoformat(),
                'updated_at': (datetime.now() - timedelta(days=3)).isoformat(),
                'last_contacted': None,
                'next_followup': (datetime.now() + timedelta(days=1)).isoformat()
            },
            {
                'id': 'lead_006',
                'name': 'Robert Kim',
                'email': 'rkim@apexcorp.com',
                'phone': '+1 (555) 678-9012',
                'company': 'Apex Corporation',
                'source': 'Partner',
                'stage': 'Closed Won',
                'value': 100000,
                'assigned_to': 'Me',
                'notes': 'Closed deal! Annual contract signed. Onboarding starts next week.',
                'tags': ['closed-won', 'annual-contract'],
                'created_at': (datetime.now() - timedelta(days=60)).isoformat(),
                'updated_at': (datetime.now() - timedelta(days=10)).isoformat(),
                'last_contacted': (datetime.now() - timedelta(days=10)).isoformat(),
                'next_followup': None
            },
            {
                'id': 'lead_007',
                'name': 'Jennifer Martinez',
                'email': 'jmartinez@velocity.co',
                'phone': '+1 (555) 789-0123',
                'company': 'Velocity Co',
                'source': 'Social Media',
                'stage': 'Closed Lost',
                'value': 20000,
                'assigned_to': 'Me',
                'notes': 'Lost to competitor. Budget constraints. Keep in nurture for next year.',
                'tags': ['lost', 'competitor', 'nurture'],
                'created_at': (datetime.now() - timedelta(days=90)).isoformat(),
                'updated_at': (datetime.now() - timedelta(days=20)).isoformat(),
                'last_contacted': (datetime.now() - timedelta(days=20)).isoformat(),
                'next_followup': None
            },
            {
                'id': 'lead_008',
                'name': 'David Thompson',
                'email': 'dthompson@nexgen.com',
                'phone': '+1 (555) 890-1234',
                'company': 'NexGen Industries',
                'source': 'Website',
                'stage': 'Qualified',
                'value': 40000,
                'assigned_to': 'Sarah Johnson',
                'notes': 'Technical evaluation in progress. Need to connect with CTO.',
                'tags': ['technical-eval', 'cto-involved'],
                'created_at': (datetime.now() - timedelta(days=20)).isoformat(),
                'updated_at': (datetime.now() - timedelta(days=4)).isoformat(),
                'last_contacted': (datetime.now() - timedelta(days=4)).isoformat(),
                'next_followup': (datetime.now() + timedelta(days=5)).isoformat()
            }
        ]
        return sample_leads

    def _get_sample_activities(self) -> List[Dict]:
        """Generate sample activities."""
        activities = []
        base_time = datetime.now() - timedelta(days=7)

        sample_activities = [
            {'type': 'Call', 'description': 'Discovery call with Sarah Johnson - discussed requirements', 'lead_id': 'lead_001', 'lead_name': 'Sarah Johnson', 'hours_ago': 2},
            {'type': 'Email', 'description': 'Sent proposal to Michael Chen', 'lead_id': 'lead_002', 'lead_name': 'Michael Chen', 'hours_ago': 5},
            {'type': 'Meeting', 'description': 'Negotiation meeting with Emily Davis - legal review', 'lead_id': 'lead_003', 'lead_name': 'Emily Davis', 'hours_ago': 24},
            {'type': 'Email', 'description': 'Follow-up email to James Wilson with demo recording', 'lead_id': 'lead_004', 'lead_name': 'James Wilson', 'hours_ago': 48},
            {'type': 'Task', 'description': 'Scheduled demo for Lisa Anderson', 'lead_id': 'lead_005', 'lead_name': 'Lisa Anderson', 'hours_ago': 72},
            {'type': 'Note', 'description': 'Contract signed by Robert Kim - $100k annual', 'lead_id': 'lead_006', 'lead_name': 'Robert Kim', 'hours_ago': 240},
            {'type': 'Call', 'description': 'Technical discovery call with David Thompson', 'lead_id': 'lead_008', 'lead_name': 'David Thompson', 'hours_ago': 96},
        ]

        for act in sample_activities:
            timestamp = base_time + timedelta(hours=act['hours_ago'])
            activities.append({
                'id': f"act_{act['hours_ago']}",
                'type': act['type'],
                'description': act['description'],
                'lead_id': act['lead_id'],
                'lead_name': act['lead_name'],
                'user': 'Current User',
                'timestamp': timestamp.isoformat()
            })

        return activities

    def _get_sample_tasks(self) -> List[Dict]:
        """Generate sample tasks."""
        now = datetime.now()
        return [
            {
                'id': 'task_001',
                'title': 'Follow up with Sarah Johnson',
                'description': 'Send case study and pricing details',
                'lead_id': 'lead_001',
                'lead_name': 'Sarah Johnson',
                'due_date': (now + timedelta(days=1)).isoformat(),
                'priority': 'High',
                'type': 'Email',
                'completed': False,
                'created_at': (now - timedelta(days=2)).isoformat()
            },
            {
                'id': 'task_002',
                'title': 'Schedule demo for Lisa Anderson',
                'description': 'Book 30-min product demo',
                'lead_id': 'lead_005',
                'lead_name': 'Lisa Anderson',
                'due_date': (now + timedelta(days=2)).isoformat(),
                'priority': 'High',
                'type': 'Meeting',
                'completed': False,
                'created_at': (now - timedelta(days=1)).isoformat()
            },
            {
                'id': 'task_003',
                'title': 'Review contract with Emily Davis',
                'description': 'Legal team review - finalize terms',
                'lead_id': 'lead_003',
                'lead_name': 'Emily Davis',
                'due_date': (now + timedelta(days=3)).isoformat(),
                'priority': 'Critical',
                'type': 'Call',
                'completed': False,
                'created_at': (now - timedelta(days=1)).isoformat()
            },
            {
                'id': 'task_004',
                'title': 'Send proposal to Michael Chen',
                'description': 'Custom enterprise proposal',
                'lead_id': 'lead_002',
                'lead_name': 'Michael Chen',
                'due_date': (now - timedelta(days=1)).isoformat(),
                'priority': 'Medium',
                'type': 'Email',
                'completed': False,
                'created_at': (now - timedelta(days=5)).isoformat()
            },
            {
                'id': 'task_005',
                'title': 'Connect with CTO at NexGen',
                'description': 'Technical deep-dive session',
                'lead_id': 'lead_008',
                'lead_name': 'David Thompson',
                'due_date': (now + timedelta(days=5)).isoformat(),
                'priority': 'Medium',
                'type': 'Call',
                'completed': False,
                'created_at': (now - timedelta(days=3)).isoformat()
            }
        ]