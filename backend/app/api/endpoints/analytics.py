"""
Analytics API endpoints
"""
from fastapi import APIRouter, HTTPException
from app.models.schemas import AnalyticsMetrics
from database.supabase_client import supabase_client
from app.core.logger import app_logger
from datetime import datetime, timedelta

router = APIRouter()


@router.get("/metrics", response_model=AnalyticsMetrics)
async def get_analytics_metrics():
    """Get overall analytics metrics"""
    try:
        # Fetch data from database
        competitors = await supabase_client.get_competitors()
        trends = await supabase_client.get_trends()
        reports = await supabase_client.get_reports(100)

        # Calculate findings this week
        week_ago = (datetime.utcnow() - timedelta(days=7)).isoformat()
        findings = await supabase_client.get_findings()
        findings_this_week = len([f for f in findings if f.get("created_at", "") > week_ago])

        # Sentiment breakdown
        sentiment_breakdown = {
            "positive": len([f for f in findings if f.get("sentiment") == "positive"]),
            "neutral": len([f for f in findings if f.get("sentiment") == "neutral"]),
            "negative": len([f for f in findings if f.get("sentiment") == "negative"])
        }

        # Top industries
        industry_counts = {}
        for comp in competitors:
            industry = comp.get("industry", "Unknown")
            industry_counts[industry] = industry_counts.get(industry, 0) + 1

        top_industries = [
            {"name": k, "count": v}
            for k, v in sorted(industry_counts.items(), key=lambda x: x[1], reverse=True)[:5]
        ]

        return AnalyticsMetrics(
            total_competitors=len(competitors),
            active_trends=len([t for t in trends if t.get("status") in ["emerging", "growing"]]),
            findings_this_week=findings_this_week,
            reports_generated=len(reports),
            sentiment_breakdown=sentiment_breakdown,
            top_industries=top_industries
        )
    except Exception as e:
        app_logger.error(f"Error fetching analytics metrics: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/dashboard")
async def get_dashboard_data():
    """Get dashboard overview data"""
    try:
        metrics = await get_analytics_metrics()
        competitors = await supabase_client.get_competitors()
        trends = await supabase_client.get_trends()
        recent_findings = await supabase_client.get_findings()

        return {
            "metrics": metrics,
            "recent_competitors": competitors[:5],
            "trending_topics": trends[:5],
            "recent_findings": recent_findings[:10],
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        app_logger.error(f"Error fetching dashboard data: {e}")
        raise HTTPException(status_code=500, detail=str(e))
