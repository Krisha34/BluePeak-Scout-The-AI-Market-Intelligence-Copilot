"""
Trends API endpoints
"""
from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from app.models.schemas import TrendCreate, TrendResponse, TrendStatus
from database.supabase_client import supabase_client
from agents.market_trend_analyst import MarketTrendAnalystAgent
from app.core.logger import app_logger
from datetime import datetime
import uuid

router = APIRouter()
trend_agent = MarketTrendAnalystAgent()


@router.get("/", response_model=List[TrendResponse])
async def get_trends(
    status: Optional[TrendStatus] = None,
    industry: Optional[str] = None,
    limit: int = Query(50, le=100)
):
    """Get all trends with optional filters"""
    try:
        filters = {}
        if status:
            filters["status"] = status.value
        if industry:
            filters["industry"] = industry

        trends = await supabase_client.get_trends(filters)
        return trends[:limit]
    except Exception as e:
        app_logger.error(f"Error fetching trends: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/", response_model=TrendResponse, status_code=201)
async def create_trend(trend: TrendCreate):
    """Create a new trend"""
    try:
        trend_data = trend.model_dump()
        trend_data["id"] = str(uuid.uuid4())
        trend_data["created_at"] = datetime.utcnow().isoformat()
        trend_data["updated_at"] = datetime.utcnow().isoformat()

        created = await supabase_client.create_trend(trend_data)
        if not created:
            raise HTTPException(status_code=400, detail="Failed to create trend")

        return created
    except Exception as e:
        app_logger.error(f"Error creating trend: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/discover")
async def discover_trends(industry: str, timeframe: str = "30_days"):
    """Discover new trends using AI agent"""
    try:
        analysis = await trend_agent.execute({
            "industry": industry,
            "timeframe": timeframe,
            "data_points": []  # Would be populated with real data
        })

        return {
            "industry": industry,
            "timeframe": timeframe,
            "analysis": analysis,
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        app_logger.error(f"Error discovering trends: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{trend_id}/trajectory")
async def predict_trend_trajectory(trend_id: str):
    """Predict the future trajectory of a trend"""
    try:
        trends = await supabase_client.get_trends({"id": trend_id})
        if not trends:
            raise HTTPException(status_code=404, detail="Trend not found")

        trend = trends[0]
        prediction = await trend_agent.predict_trend_trajectory(trend)

        return {
            "trend_id": trend_id,
            "prediction": prediction,
            "timestamp": datetime.utcnow().isoformat()
        }
    except HTTPException:
        raise
    except Exception as e:
        app_logger.error(f"Error predicting trajectory: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/industries")
async def get_industries():
    """Get list of available industries"""
    return {
        "industries": [
            "Technology",
            "Healthcare",
            "Finance",
            "E-commerce",
            "Manufacturing",
            "Education",
            "Entertainment",
            "Automotive",
            "Energy",
            "Telecommunications"
        ]
    }
