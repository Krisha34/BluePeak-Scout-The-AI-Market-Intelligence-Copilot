"""
Reports API endpoints
"""
from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from app.models.schemas import ReportCreate, ReportResponse
from database.supabase_client import supabase_client
from agents.synthesis_reporting import SynthesisReportingAgent
from app.core.logger import app_logger
from datetime import datetime
import uuid

router = APIRouter()
reporting_agent = SynthesisReportingAgent()


@router.get("/", response_model=List[ReportResponse])
async def get_reports(limit: int = Query(50, le=100)):
    """Get all generated reports"""
    try:
        reports = await supabase_client.get_reports(limit)
        return reports
    except Exception as e:
        app_logger.error(f"Error fetching reports: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{report_id}", response_model=ReportResponse)
async def get_report(report_id: str):
    """Get a specific report by ID"""
    try:
        reports = await supabase_client.get_reports(1000)
        report = next((r for r in reports if r["id"] == report_id), None)

        if not report:
            raise HTTPException(status_code=404, detail="Report not found")

        return report
    except HTTPException:
        raise
    except Exception as e:
        app_logger.error(f"Error fetching report: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/", response_model=ReportResponse, status_code=201)
async def create_report(report: ReportCreate):
    """Create a new report"""
    try:
        report_data = report.model_dump()
        report_data["id"] = str(uuid.uuid4())
        report_data["created_at"] = datetime.utcnow().isoformat()

        created = await supabase_client.create_report(report_data)
        if not created:
            raise HTTPException(status_code=400, detail="Failed to create report")

        return created
    except Exception as e:
        app_logger.error(f"Error creating report: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/generate")
async def generate_report(
    report_type: str = "comprehensive",
    competitor_ids: Optional[List[str]] = None,
    trend_ids: Optional[List[str]] = None,
    industry: Optional[str] = None
):
    """Generate a new report using AI"""
    try:
        # Gather data sources
        data_sources = []

        if competitor_ids:
            for cid in competitor_ids:
                competitor = await supabase_client.get_competitor_by_id(cid)
                if competitor:
                    data_sources.append({"type": "competitor", "data": competitor})

        if trend_ids:
            trends = await supabase_client.get_trends()
            for trend in trends:
                if trend.get("id") in trend_ids:
                    data_sources.append({"type": "trend", "data": trend})

        # Generate report with AI agent
        result = await reporting_agent.execute({
            "report_type": report_type,
            "data_sources": data_sources,
            "format": "markdown"
        })

        # Create summary
        summary = await reporting_agent.generate_executive_summary(result["content"])

        # Save report
        report_data = {
            "id": str(uuid.uuid4()),
            "title": f"{report_type.replace('_', ' ').title()} Report",
            "report_type": report_type,
            "content": result["content"],
            "summary": summary,
            "competitor_ids": competitor_ids or [],
            "trend_ids": trend_ids or [],
            "generated_by": "ai_agent",
            "created_at": datetime.utcnow().isoformat()
        }

        created = await supabase_client.create_report(report_data)

        return {
            "report_id": created.get("id") if created else report_data["id"],
            "report": created or report_data,
            "message": "Report generated successfully"
        }
    except Exception as e:
        app_logger.error(f"Error generating report: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{report_id}/export")
async def export_report(report_id: str, format: str = "pdf"):
    """Export report in different formats"""
    try:
        reports = await supabase_client.get_reports(1000)
        report = next((r for r in reports if r["id"] == report_id), None)

        if not report:
            raise HTTPException(status_code=404, detail="Report not found")

        # Format report for export
        formatted = await reporting_agent.format_for_distribution(
            report.get("content", ""),
            format
        )

        return {
            "report_id": report_id,
            "format": format,
            "content": formatted,
            "download_url": f"/api/v1/reports/{report_id}/download?format={format}"
        }
    except HTTPException:
        raise
    except Exception as e:
        app_logger.error(f"Error exporting report: {e}")
        raise HTTPException(status_code=500, detail=str(e))
