"""
Reports API endpoints
"""
from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import PlainTextResponse
from typing import List, Optional
from app.models.schemas import ReportCreate, ReportResponse
from database.supabase_client import supabase_client
from agents.synthesis_reporting import SynthesisReportingAgent
from app.core.logger import app_logger
from integrations.email_integration import email_integration
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
    report_type: str = "full_market",
    focus_areas: Optional[List[str]] = None,
    date_range: str = "last_30_days",
    competitor_ids: Optional[List[str]] = None,
    trend_ids: Optional[List[str]] = None,
    industry: Optional[str] = None
):
    """Generate a comprehensive AI-powered market intelligence report"""
    try:
        from agents.rag_assistant import RAGQueryAssistantAgent

        # Gather all competitors and trends
        competitors = await supabase_client.get_competitors()
        trends = await supabase_client.get_trends()
        findings = await supabase_client.get_findings()

        # Map report types to titles
        report_titles = {
            "weekly_digest": "Weekly Competitive Digest",
            "full_market": "Full Market Analysis",
            "competitor_deep_dive": "Competitor Deep Dive",
            "custom_query": "Custom Research Report"
        }

        # Map focus areas to readable names
        focus_area_names = {
            "ai_features": "AI Features",
            "pricing_strategies": "Pricing Strategies",
            "content_marketing": "Content Marketing",
            "product_launches": "Product Launches"
        }

        # Create focus areas text
        focus_text = ""
        if focus_areas and len(focus_areas) > 0:
            focus_names = [focus_area_names.get(fa, fa) for fa in focus_areas]
            focus_text = f" - Focus: {', '.join(focus_names)}"

        # Generate report title
        title = f"{report_titles.get(report_type, 'Intelligence Report')} - {datetime.utcnow().strftime('%b %d, %Y')}{focus_text}"

        # Build comprehensive report content
        rag_agent = RAGQueryAssistantAgent()

        # Generate executive summary
        summary_query = f"Provide an executive summary of the competitive landscape, focusing on {', '.join(focus_areas) if focus_areas else 'all areas'} over the {date_range.replace('_', ' ')}."
        summary_response = await rag_agent.execute({
            "query": summary_query,
            "conversation_history": [],
            "context_ids": []
        })

        # Generate detailed content sections
        content_sections = []

        # Executive Summary Section
        content_sections.append(f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
         BLUEPEAK COMPASS
    Market Intelligence Report
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Generated: {datetime.utcnow().strftime('%B %d, %Y')}
Report Type: {report_titles.get(report_type, 'Intelligence Report')}
Date Range: {date_range.replace('_', ' ').title()}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

EXECUTIVE SUMMARY

{summary_response['content']}

KEY FINDINGS:
- {len(competitors)} competitors monitored
- {len(trends)} active market trends identified
- {len(findings)} research findings analyzed
- Focus areas: {', '.join([focus_area_names.get(fa, fa) for fa in focus_areas]) if focus_areas else 'All areas'}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
""")

        # Competitive Landscape Section
        content_sections.append("\nCOMPETITIVE LANDSCAPE\n")
        for i, competitor in enumerate(competitors[:5]):  # Top 5 competitors
            comp_query = f"Provide a brief competitive analysis of {competitor.get('name', 'Unknown')}, focusing on their recent activities and market position."
            comp_response = await rag_agent.execute({
                "query": comp_query,
                "conversation_history": [],
                "context_ids": [competitor.get("id")]
            })

            content_sections.append(f"""
{competitor.get('name', 'Unknown')}
{'─' * 60}
Industry: {competitor.get('industry', 'N/A')}
Status: {competitor.get('status', 'N/A').upper()}
Monitoring Score: {(competitor.get('monitoring_score', 0) * 100):.0f}%

Analysis:
{comp_response['content']}

""")

        # Trends and Market Dynamics
        if len(trends) > 0:
            content_sections.append(f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

MARKET TRENDS & DYNAMICS

""")
            for trend in trends[:5]:
                content_sections.append(f"""
{trend.get('title', 'Unnamed Trend')}
Status: {trend.get('status', 'N/A').upper()} | Confidence: {(trend.get('confidence_score', 0) * 100):.0f}%

{trend.get('description', 'No description available')}

""")

        # Strategic Recommendations
        rec_query = f"Based on the current competitive landscape, provide 3 strategic recommendations for the {date_range.replace('_', ' ')}."
        rec_response = await rag_agent.execute({
            "query": rec_query,
            "conversation_history": [],
            "context_ids": []
        })

        content_sections.append(f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

STRATEGIC RECOMMENDATIONS

{rec_response['content']}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

APPENDIX: DATA SOURCES

{len(competitors)} competitor profiles analyzed
{len(trends)} market trends tracked
{len(findings)} research findings reviewed
Report generated in ~60 seconds using AI

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
""")

        full_content = "\n".join(content_sections)

        # Save report
        report_data = {
            "id": str(uuid.uuid4()),
            "title": title,
            "report_type": report_type,
            "content": full_content,
            "summary": summary_response['content'],
            "competitor_ids": competitor_ids or [],
            "trend_ids": trend_ids or [],
            "generated_by": "ai_agent",
            "created_at": datetime.utcnow().isoformat()
        }

        created = await supabase_client.create_report(report_data)

        # Send email notification if integration is enabled
        try:
            integration_settings = await supabase_client.get_integration_settings("default_user")
            if integration_settings and integration_settings.get("email_enabled"):
                recipients = integration_settings.get("email_recipients", [])
                notification_types = integration_settings.get("notification_types", [])

                # Check if report notifications are enabled
                if recipients and ("reports" in notification_types or "report_ready" in notification_types):
                    await email_integration.send_report_email(
                        to_emails=recipients,
                        report_data={
                            "title": title,
                            "summary": summary_response['content'],
                            "content": full_content
                        }
                    )
                    app_logger.info(f"Report notification email sent to {len(recipients)} recipient(s)")
        except Exception as email_error:
            # Don't fail the report generation if email fails
            app_logger.error(f"Failed to send report notification email: {email_error}")

        return {
            "report_id": created.get("id") if created else report_data["id"],
            "report": created or report_data,
            "message": "Report generated successfully"
        }
    except Exception as e:
        app_logger.error(f"Error generating report: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{report_id}/export", response_class=PlainTextResponse)
async def export_report(report_id: str, format: str = "pdf"):
    """Export report as downloadable text file"""
    try:
        reports = await supabase_client.get_reports(1000)
        report = next((r for r in reports if r["id"] == report_id), None)

        if not report:
            raise HTTPException(status_code=404, detail="Report not found")

        # Get report content
        content = report.get("content", "")

        # Add header information
        header = f"""
╔═══════════════════════════════════════════════════════════════════════════╗
║                           BLUEPEAK COMPASS                                ║
║                      Market Intelligence Report                           ║
╚═══════════════════════════════════════════════════════════════════════════╝

Report: {report.get('title', 'Untitled Report')}
Generated: {report.get('created_at', 'Unknown date')}
Type: {report.get('report_type', 'N/A').replace('_', ' ').title()}

═══════════════════════════════════════════════════════════════════════════

"""

        full_content = header + content

        return PlainTextResponse(content=full_content, media_type="text/plain")
    except HTTPException:
        raise
    except Exception as e:
        app_logger.error(f"Error exporting report: {e}")
        raise HTTPException(status_code=500, detail=str(e))
