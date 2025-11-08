"""
Generate comprehensive dummy data for BluePeak Compass
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

import asyncio
from datetime import datetime, timedelta
import random
import uuid
from database.supabase_client import supabase_client
from app.services.vector_store import vector_store


# Competitor Data
COMPETITORS = [
    {
        "name": "TechVision AI",
        "website": "https://techvision-ai.com",
        "description": "Leading AI-powered analytics platform for enterprise businesses",
        "industry": "Technology",
        "founded_year": 2018,
        "headquarters": "San Francisco, CA",
        "employee_count": 450,
        "status": "active"
    },
    {
        "name": "DataFlow Systems",
        "website": "https://dataflow-systems.com",
        "description": "Real-time data processing and analytics solutions",
        "industry": "Technology",
        "founded_year": 2016,
        "headquarters": "Austin, TX",
        "employee_count": 320,
        "status": "monitoring"
    },
    {
        "name": "CloudMetrics Inc",
        "website": "https://cloudmetrics.io",
        "description": "Cloud-native business intelligence and reporting platform",
        "industry": "Technology",
        "founded_year": 2019,
        "headquarters": "Seattle, WA",
        "employee_count": 280,
        "status": "active"
    },
    {
        "name": "InsightHub Pro",
        "website": "https://insighthub-pro.com",
        "description": "Customer analytics and market intelligence platform",
        "industry": "Technology",
        "founded_year": 2017,
        "headquarters": "New York, NY",
        "employee_count": 500,
        "status": "active"
    },
    {
        "name": "MarketPulse Analytics",
        "website": "https://marketpulse.com",
        "description": "AI-driven market research and competitive intelligence",
        "industry": "Technology",
        "founded_year": 2020,
        "headquarters": "Boston, MA",
        "employee_count": 180,
        "status": "monitoring"
    },
    {
        "name": "VisionTech Solutions",
        "website": "https://visiontech.io",
        "description": "Computer vision and image recognition technology",
        "industry": "Technology",
        "founded_year": 2015,
        "headquarters": "Palo Alto, CA",
        "employee_count": 600,
        "status": "active"
    },
    {
        "name": "NeuralWorks Corp",
        "website": "https://neuralworks.ai",
        "description": "Deep learning infrastructure and model optimization",
        "industry": "Technology",
        "founded_year": 2019,
        "headquarters": "Mountain View, CA",
        "employee_count": 220,
        "status": "active"
    },
    {
        "name": "QuantumData Labs",
        "website": "https://quantumdata.com",
        "description": "Quantum computing applications for data analysis",
        "industry": "Technology",
        "founded_year": 2021,
        "headquarters": "Cambridge, MA",
        "employee_count": 95,
        "status": "monitoring"
    },
    {
        "name": "EdgeAI Technologies",
        "website": "https://edgeai.tech",
        "description": "Edge computing and IoT analytics platform",
        "industry": "Technology",
        "founded_year": 2018,
        "headquarters": "San Jose, CA",
        "employee_count": 340,
        "status": "active"
    },
    {
        "name": "StreamAnalyze Pro",
        "website": "https://streamanalyze.com",
        "description": "Real-time streaming analytics and data visualization",
        "industry": "Technology",
        "founded_year": 2017,
        "headquarters": "Denver, CO",
        "employee_count": 260,
        "status": "active"
    }
]

# Trends Data
TRENDS = [
    {
        "title": "Generative AI in Enterprise Software",
        "description": "Rapid adoption of generative AI capabilities across enterprise software platforms, enabling automated content creation, code generation, and decision support",
        "industry": "Technology",
        "status": "growing",
        "confidence_score": 0.92,
        "keywords": ["generative ai", "llm", "enterprise", "automation", "gpt"],
        "mention_count": 1247,
        "growth_rate": 156.3
    },
    {
        "title": "Edge Computing for Real-Time Analytics",
        "description": "Shift towards processing data at the edge for reduced latency and improved real-time decision making in IoT and industrial applications",
        "industry": "Technology",
        "status": "emerging",
        "confidence_score": 0.87,
        "keywords": ["edge computing", "iot", "real-time", "latency", "5g"],
        "mention_count": 892,
        "growth_rate": 89.4
    },
    {
        "title": "Privacy-First Data Analytics",
        "description": "Growing emphasis on privacy-preserving analytics techniques including differential privacy and federated learning",
        "industry": "Technology",
        "status": "growing",
        "confidence_score": 0.84,
        "keywords": ["privacy", "gdpr", "data protection", "differential privacy"],
        "mention_count": 678,
        "growth_rate": 67.2
    },
    {
        "title": "Natural Language Interfaces for BI",
        "description": "Business intelligence tools incorporating natural language processing to enable conversational analytics and query interfaces",
        "industry": "Technology",
        "status": "emerging",
        "confidence_score": 0.79,
        "keywords": ["nlp", "conversational ai", "business intelligence", "query"],
        "mention_count": 543,
        "growth_rate": 45.8
    },
    {
        "title": "AutoML and No-Code ML Platforms",
        "description": "Democratization of machine learning through automated model selection, training, and deployment platforms",
        "industry": "Technology",
        "status": "stable",
        "confidence_score": 0.88,
        "keywords": ["automl", "no-code", "democratization", "citizen data scientist"],
        "mention_count": 1034,
        "growth_rate": 23.5
    },
    {
        "title": "Graph Analytics for Complex Relationships",
        "description": "Increased use of graph databases and analytics for understanding complex relationships in social networks, supply chains, and fraud detection",
        "industry": "Technology",
        "status": "growing",
        "confidence_score": 0.81,
        "keywords": ["graph database", "network analysis", "relationships", "neo4j"],
        "mention_count": 456,
        "growth_rate": 52.1
    },
    {
        "title": "Sustainable AI Computing",
        "description": "Focus on energy-efficient AI models and green computing practices to reduce carbon footprint of machine learning operations",
        "industry": "Technology",
        "status": "emerging",
        "confidence_score": 0.76,
        "keywords": ["sustainable ai", "green computing", "energy efficient", "carbon footprint"],
        "mention_count": 389,
        "growth_rate": 78.9
    },
    {
        "title": "Augmented Analytics with AI",
        "description": "Integration of AI-powered insights, automated pattern detection, and predictive analytics into traditional BI workflows",
        "industry": "Technology",
        "status": "growing",
        "confidence_score": 0.90,
        "keywords": ["augmented analytics", "ai insights", "predictive", "pattern detection"],
        "mention_count": 812,
        "growth_rate": 94.3
    }
]

# Research Findings Templates
FINDING_TYPES = ["product_launch", "pricing_change", "partnership", "funding", "acquisition", "market_expansion"]
SENTIMENTS = ["positive", "neutral", "negative"]

FINDING_TEMPLATES = [
    {
        "type": "product_launch",
        "titles": [
            "New AI-powered analytics module announced",
            "Launch of next-generation data platform",
            "Unveiling of advanced reporting capabilities"
        ],
        "contents": [
            "Company has announced a major product update featuring enhanced AI capabilities, real-time processing, and improved user experience.",
            "The new platform includes automated insights, predictive analytics, and seamless integrations with major cloud providers.",
            "Latest release introduces breakthrough features in data visualization and collaborative analytics workflows."
        ]
    },
    {
        "type": "pricing_change",
        "titles": [
            "Competitive pricing strategy update",
            "New pricing tier introduced",
            "Enterprise plan restructuring announced"
        ],
        "contents": [
            "Significant changes to pricing structure with new usage-based model and expanded enterprise features.",
            "Introduction of flexible pricing tiers aimed at capturing mid-market segment with enhanced value proposition.",
            "Price adjustments reflect market positioning shift and increased feature set in premium offerings."
        ]
    },
    {
        "type": "partnership",
        "titles": [
            "Strategic partnership with major cloud provider",
            "Integration partnership announced",
            "Joint go-to-market initiative launched"
        ],
        "contents": [
            "New partnership enables deeper integration with enterprise ecosystems and expands market reach significantly.",
            "Collaborative initiative brings together complementary technologies to deliver enhanced customer value.",
            "Strategic alliance positions company for accelerated growth in key market segments."
        ]
    }
]


async def generate_competitors():
    """Generate competitor data"""
    print("Generating competitor data...")
    competitor_ids = []

    for comp in COMPETITORS:
        comp_data = {
            **comp,
            "id": str(uuid.uuid4()),
            "monitoring_score": round(random.uniform(0.6, 0.95), 2),
            "last_analyzed": (datetime.utcnow() - timedelta(days=random.randint(0, 30))).isoformat(),
            "created_at": (datetime.utcnow() - timedelta(days=random.randint(30, 365))).isoformat(),
            "updated_at": datetime.utcnow().isoformat()
        }

        created = await supabase_client.create_competitor(comp_data)
        if created:
            competitor_ids.append(comp_data["id"])
            # Add to vector store
            await vector_store.add_competitor(comp_data)
            print(f"  ✓ Created: {comp['name']}")

    return competitor_ids


async def generate_trends():
    """Generate trend data"""
    print("\nGenerating trend data...")
    trend_ids = []

    for trend in TRENDS:
        trend_data = {
            **trend,
            "id": str(uuid.uuid4()),
            "created_at": (datetime.utcnow() - timedelta(days=random.randint(1, 90))).isoformat(),
            "updated_at": datetime.utcnow().isoformat()
        }

        created = await supabase_client.create_trend(trend_data)
        if created:
            trend_ids.append(trend_data["id"])
            # Add to vector store
            await vector_store.add_trend(trend_data)
            print(f"  ✓ Created: {trend['title']}")

    return trend_ids


async def generate_findings(competitor_ids):
    """Generate research findings"""
    print("\nGenerating research findings...")

    for competitor_id in competitor_ids:
        # Generate 3-5 findings per competitor
        num_findings = random.randint(3, 5)

        for _ in range(num_findings):
            finding_type = random.choice(FINDING_TYPES)
            template = next((t for t in FINDING_TEMPLATES if t["type"] == finding_type), FINDING_TEMPLATES[0])

            finding_data = {
                "id": str(uuid.uuid4()),
                "competitor_id": competitor_id,
                "finding_type": finding_type,
                "title": random.choice(template["titles"]),
                "content": random.choice(template["contents"]),
                "source_url": f"https://example.com/article/{uuid.uuid4().hex[:8]}",
                "sentiment": random.choice(SENTIMENTS),
                "importance_score": round(random.uniform(0.5, 1.0), 2),
                "metadata": {
                    "source": random.choice(["press_release", "news_article", "blog_post", "social_media"]),
                    "author": f"Author {random.randint(1, 100)}"
                },
                "created_at": (datetime.utcnow() - timedelta(days=random.randint(0, 60))).isoformat()
            }

            created = await supabase_client.create_finding(finding_data)
            if created:
                # Add to vector store
                await vector_store.add_finding(finding_data)

    print(f"  ✓ Created {len(competitor_ids) * 4} research findings")


async def generate_reports(competitor_ids, trend_ids):
    """Generate sample reports"""
    print("\nGenerating reports...")

    report_types = ["competitive_analysis", "market_trends", "industry_overview", "quarterly_review"]

    for i, report_type in enumerate(report_types):
        report_data = {
            "id": str(uuid.uuid4()),
            "title": f"{report_type.replace('_', ' ').title()} - Q{random.randint(1,4)} 2024",
            "report_type": report_type,
            "content": f"""# {report_type.replace('_', ' ').title()}

## Executive Summary
This comprehensive analysis provides insights into the current competitive landscape and market dynamics.

## Key Findings
- Market consolidation trends indicate increased competition
- Emerging technologies driving innovation
- Customer preferences shifting towards cloud-native solutions
- Price competition intensifying in mid-market segment

## Competitive Landscape
Analysis of {len(competitor_ids)} key competitors reveals diverse strategies and market positioning.

## Market Trends
{len(trend_ids)} significant trends identified with high confidence scores.

## Strategic Recommendations
1. Focus on differentiation through advanced AI capabilities
2. Expand partnerships to strengthen market position
3. Invest in emerging technologies for future growth
4. Optimize pricing strategy for target segments

## Conclusion
The market presents significant opportunities for growth despite increasing competition.
""",
            "summary": f"Comprehensive {report_type.replace('_', ' ')} covering key competitive insights and market dynamics.",
            "competitor_ids": random.sample(competitor_ids, min(3, len(competitor_ids))),
            "trend_ids": random.sample(trend_ids, min(3, len(trend_ids))),
            "generated_by": "ai_agent",
            "created_at": (datetime.utcnow() - timedelta(days=random.randint(0, 30))).isoformat()
        }

        created = await supabase_client.create_report(report_data)
        if created:
            # Add to vector store
            await vector_store.add_report(report_data)
            print(f"  ✓ Created: {report_data['title']}")


async def generate_conversations():
    """Generate sample conversations"""
    print("\nGenerating sample conversations...")

    conversations = [
        {
            "title": "Competitor pricing analysis",
            "messages": [
                {"role": "user", "content": "What's the average pricing for our competitors?", "timestamp": datetime.utcnow().isoformat()},
                {"role": "assistant", "content": "Based on current data, competitor pricing ranges from $49/month for basic plans to $499/month for enterprise plans. The median price point is around $199/month.", "timestamp": datetime.utcnow().isoformat()}
            ]
        },
        {
            "title": "Market trends discussion",
            "messages": [
                {"role": "user", "content": "What are the top emerging trends in our industry?", "timestamp": datetime.utcnow().isoformat()},
                {"role": "assistant", "content": "The top emerging trends include: 1) Generative AI adoption (92% confidence), 2) Edge computing for real-time analytics (87% confidence), and 3) Privacy-first data analytics (84% confidence).", "timestamp": datetime.utcnow().isoformat()}
            ]
        }
    ]

    for conv in conversations:
        conv_data = {
            "id": str(uuid.uuid4()),
            "user_id": "default_user",
            "title": conv["title"],
            "messages": conv["messages"],
            "context_ids": [],
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat()
        }

        await supabase_client.create_conversation(conv_data)
        print(f"  ✓ Created conversation: {conv['title']}")


async def main():
    """Main function to generate all dummy data"""
    print("=" * 60)
    print("BluePeak Compass - Dummy Data Generator")
    print("=" * 60)

    try:
        # Generate data
        competitor_ids = await generate_competitors()
        trend_ids = await generate_trends()
        await generate_findings(competitor_ids)
        await generate_reports(competitor_ids, trend_ids)
        await generate_conversations()

        print("\n" + "=" * 60)
        print("✓ Dummy data generation completed successfully!")
        print("=" * 60)
        print(f"\nGenerated:")
        print(f"  - {len(competitor_ids)} competitors")
        print(f"  - {len(trend_ids)} trends")
        print(f"  - {len(competitor_ids) * 4} research findings")
        print(f"  - 4 reports")
        print(f"  - 2 sample conversations")
        print("\n")

    except Exception as e:
        print(f"\n❌ Error generating dummy data: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
