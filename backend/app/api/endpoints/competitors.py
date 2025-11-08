"""
Competitors API endpoints
"""
from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from app.models.schemas import (
    CompetitorCreate,
    CompetitorUpdate,
    CompetitorResponse,
    CompetitorStatus
)
from database.supabase_client import supabase_client
from agents.competitive_intelligence import CompetitiveIntelligenceAgent
from app.core.logger import app_logger
from datetime import datetime
import uuid

router = APIRouter()
ci_agent = CompetitiveIntelligenceAgent()


@router.get("/", response_model=List[CompetitorResponse])
async def get_competitors(
    status: Optional[CompetitorStatus] = None,
    industry: Optional[str] = None,
    limit: int = Query(50, le=100)
):
    """Get all competitors with optional filters"""
    try:
        filters = {}
        if status:
            filters["status"] = status.value
        if industry:
            filters["industry"] = industry

        competitors = await supabase_client.get_competitors(filters)
        return competitors[:limit]
    except Exception as e:
        app_logger.error(f"Error fetching competitors: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{competitor_id}", response_model=CompetitorResponse)
async def get_competitor(competitor_id: str):
    """Get a specific competitor by ID"""
    try:
        competitor = await supabase_client.get_competitor_by_id(competitor_id)
        if not competitor:
            raise HTTPException(status_code=404, detail="Competitor not found")
        return competitor
    except HTTPException:
        raise
    except Exception as e:
        app_logger.error(f"Error fetching competitor: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/", response_model=CompetitorResponse, status_code=201)
async def create_competitor(competitor: CompetitorCreate):
    """Create a new competitor"""
    try:
        competitor_data = competitor.model_dump()
        competitor_data["id"] = str(uuid.uuid4())
        competitor_data["created_at"] = datetime.utcnow().isoformat()
        competitor_data["updated_at"] = datetime.utcnow().isoformat()

        created = await supabase_client.create_competitor(competitor_data)
        if not created:
            raise HTTPException(status_code=400, detail="Failed to create competitor")

        return created
    except Exception as e:
        app_logger.error(f"Error creating competitor: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{competitor_id}", response_model=CompetitorResponse)
async def update_competitor(competitor_id: str, competitor: CompetitorUpdate):
    """Update an existing competitor"""
    try:
        update_data = competitor.model_dump(exclude_unset=True)
        if not update_data:
            raise HTTPException(status_code=400, detail="No fields to update")

        updated = await supabase_client.update_competitor(competitor_id, update_data)
        if not updated:
            raise HTTPException(status_code=404, detail="Competitor not found")

        return updated
    except HTTPException:
        raise
    except Exception as e:
        app_logger.error(f"Error updating competitor: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{competitor_id}/analyze")
async def analyze_competitor(competitor_id: str, analysis_type: str = "comprehensive"):
    """Trigger AI analysis of a competitor"""
    try:
        competitor = await supabase_client.get_competitor_by_id(competitor_id)
        if not competitor:
            raise HTTPException(status_code=404, detail="Competitor not found")

        # Run competitive intelligence agent
        analysis = await ci_agent.execute({
            "competitor_data": competitor,
            "analysis_type": analysis_type
        })

        # Update last_analyzed timestamp
        await supabase_client.update_competitor(
            competitor_id,
            {"last_analyzed": datetime.utcnow().isoformat()}
        )

        return {
            "competitor_id": competitor_id,
            "analysis": analysis,
            "timestamp": datetime.utcnow().isoformat()
        }
    except HTTPException:
        raise
    except Exception as e:
        app_logger.error(f"Error analyzing competitor: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{competitor_id}/findings")
async def get_competitor_findings(competitor_id: str, limit: int = 20):
    """Get research findings for a specific competitor"""
    try:
        findings = await supabase_client.get_findings(competitor_id)
        return findings[:limit]
    except Exception as e:
        app_logger.error(f"Error fetching findings: {e}")
        raise HTTPException(status_code=500, detail=str(e))
