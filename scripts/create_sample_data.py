"""
Create sample data via API
"""
import requests
import json
from datetime import datetime, timedelta
import random

BASE_URL = "http://localhost:8000/api/v1"

# Sample competitors
competitors = [
    {
        "name": "HubSpot",
        "website": "https://hubspot.com",
        "description": "Marketing, sales, and service software that helps businesses grow",
        "industry": "Marketing Technology",
        "founded_year": 2006,
        "headquarters": "Cambridge, MA",
        "employee_count": 7000,
        "status": "active",
        "monitoring_score": 95
    },
    {
        "name": "Marketo",
        "website": "https://marketo.com",
        "description": "Marketing automation platform for B2B marketers",
        "industry": "Marketing Technology",
        "founded_year": 2006,
        "headquarters": "San Mateo, CA",
        "employee_count": 2000,
        "status": "active",
        "monitoring_score": 88
    },
    {
        "name": "Pardot",
        "website": "https://pardot.com",
        "description": "B2B marketing automation by Salesforce",
        "industry": "Marketing Technology",
        "founded_year": 2007,
        "headquarters": "Atlanta, GA",
        "employee_count": 500,
        "status": "active",
        "monitoring_score": 92
    },
    {
        "name": "ActiveCampaign",
        "website": "https://activecampaign.com",
        "description": "Customer experience automation platform",
        "industry": "Marketing Technology",
        "founded_year": 2003,
        "headquarters": "Chicago, IL",
        "employee_count": 850,
        "status": "active",
        "monitoring_score": 86
    },
    {
        "name": "Mailchimp",
        "website": "https://mailchimp.com",
        "description": "Email marketing and automation platform",
        "industry": "Marketing Technology",
        "founded_year": 2001,
        "headquarters": "Atlanta, GA",
        "employee_count": 1200,
        "status": "monitoring",
        "monitoring_score": 90
    }
]

# Sample trends
trends = [
    {
        "title": "AI-Powered Content Generation",
        "description": "Increasing adoption of AI tools for automated content creation and personalization",
        "industry": "Marketing Technology",
        "status": "growing",
        "confidence_score": 0.92,
        "keywords": ["AI", "content", "automation", "GPT", "copywriting"],
        "mention_count": 1250,
        "growth_rate": 45.5
    },
    {
        "title": "Privacy-First Marketing",
        "description": "Shift towards cookieless tracking and privacy-compliant marketing strategies",
        "industry": "Marketing Technology",
        "status": "emerging",
        "confidence_score": 0.88,
        "keywords": ["privacy", "GDPR", "cookies", "compliance", "data protection"],
        "mention_count": 890,
        "growth_rate": 38.2
    },
    {
        "title": "Predictive Analytics in Marketing",
        "description": "Using machine learning to predict customer behavior and optimize campaigns",
        "industry": "Marketing Technology",
        "status": "growing",
        "confidence_score": 0.85,
        "keywords": ["predictive", "analytics", "ML", "optimization", "ROI"],
        "mention_count": 720,
        "growth_rate": 32.7
    },
    {
        "title": "Conversational Marketing",
        "description": "Growth of chatbots and conversational AI for customer engagement",
        "industry": "Marketing Technology",
        "status": "stable",
        "confidence_score": 0.80,
        "keywords": ["chatbot", "conversational AI", "messaging", "automation"],
        "mention_count": 650,
        "growth_rate": 15.3
    },
    {
        "title": "Account-Based Marketing (ABM)",
        "description": "Targeted marketing approach focusing on key accounts",
        "industry": "Marketing Technology",
        "status": "growing",
        "confidence_score": 0.87,
        "keywords": ["ABM", "enterprise", "B2B", "personalization", "targeting"],
        "mention_count": 540,
        "growth_rate": 28.9
    }
]

def create_competitors():
    print("Creating competitors...")
    created_competitors = []
    for comp in competitors:
        try:
            response = requests.post(f"{BASE_URL}/competitors/", json=comp)
            if response.status_code in [200, 201]:
                created = response.json()
                created_competitors.append(created)
                print(f"[OK] Created competitor: {comp['name']}")
            else:
                print(f"[FAIL] Failed to create {comp['name']}: {response.status_code}")
        except Exception as e:
            print(f"[ERROR] Error creating {comp['name']}: {e}")
    return created_competitors

def create_trends():
    print("\nCreating trends...")
    created_trends = []
    for trend in trends:
        try:
            response = requests.post(f"{BASE_URL}/trends/", json=trend)
            if response.status_code in [200, 201]:
                created = response.json()
                created_trends.append(created)
                print(f"[OK] Created trend: {trend['title']}")
            else:
                print(f"[FAIL] Failed to create {trend['title']}: {response.status_code}")
        except Exception as e:
            print(f"[ERROR] Error creating {trend['title']}: {e}")
    return created_trends

if __name__ == "__main__":
    print("=" * 50)
    print("BluePeak Compass - Sample Data Generator")
    print("=" * 50)

    comps = create_competitors()
    trends_data = create_trends()

    print("\n" + "=" * 50)
    print(f"Summary:")
    print(f"  Competitors created: {len(comps)}")
    print(f"  Trends created: {len(trends_data)}")
    print("=" * 50)
    print("\n[OK] Sample data generation complete!")
