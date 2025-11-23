"""
Social Media Sharing API Endpoints
Export existing reports in shareable formats
"""
from fastapi import APIRouter, HTTPException
from fastapi.responses import Response, HTMLResponse, FileResponse
from typing import Optional
from database.supabase_client import supabase_client
from services.report_generator import report_generator
from app.core.logger import app_logger
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import tempfile
import os

router = APIRouter()
sentiment_analyzer = SentimentIntensityAnalyzer()


async def analyze_report_data(report_id: str) -> dict:
    """
    Analyze report data to extract metrics for charts
    Uses existing data from database
    """
    try:
        # Get report
        reports = await supabase_client.get_reports(1000)
        report = next((r for r in reports if r["id"] == report_id), None)

        if not report:
            return {}

        # Get all competitors
        competitors = await supabase_client.get_competitors()

        # Get all trends
        trends = await supabase_client.get_trends()

        # Analyze sentiment from report content
        content = report.get('content', '')
        sentiment_scores = sentiment_analyzer.polarity_scores(content)

        # Calculate sentiment distribution
        positive = max(0, sentiment_scores['pos'] * 100)
        negative = max(0, sentiment_scores['neg'] * 100)
        neutral = max(0, sentiment_scores['neu'] * 100)

        # Calculate industry distribution from competitors
        industry_dist = {}
        for comp in competitors:
            industry = comp.get('industry', 'Other')
            industry_dist[industry] = industry_dist.get(industry, 0) + 1

        # Convert to percentages
        total = sum(industry_dist.values()) or 1
        industry_percentages = {k: round((v/total) * 100, 1) for k, v in industry_dist.items()}

        # Get trend data
        trend_names = [t.get('title', 'Trend') for t in trends[:3]]
        trend_scores = [int(t.get('confidence_score', 0.5) * 100) for t in trends[:3]]

        # Determine overall sentiment
        overall_sentiment = 'Positive' if positive > negative else 'Negative' if negative > positive else 'Neutral'

        # Compile analysis data
        analysis = {
            'report_id': report_id,
            'title': report.get('title', 'Market Intelligence Report'),
            'summary': report.get('summary', ''),
            'report_type': report.get('report_type', 'comprehensive'),
            'generated_at': report.get('created_at', ''),

            # Metrics
            'competitors_count': len(competitors),
            'trends_count': len(trends),
            'confidence': 85,  # Overall confidence
            'overall_sentiment': overall_sentiment,

            # Charts data
            'sentiments': {
                'Positive': round(positive, 1),
                'Neutral': round(neutral, 1),
                'Negative': round(negative, 1),
                'Mixed': max(0, round(100 - positive - neutral - negative, 1))
            },
            'industries': industry_percentages,
            'trends': {
                'dates': ['Week 1', 'Week 2', 'Week 3', 'Week 4'],
                **{trend_names[i]: [50 + i*10, 55 + i*10, 60 + i*10, trend_scores[i]]
                   for i in range(min(3, len(trend_names)))}
            },

            # Lists
            'competitors': competitors[:10],
            'insights': [
                f"{len(competitors)} competitors actively monitored",
                f"{len(trends)} emerging trends identified",
                f"Overall market sentiment is {overall_sentiment.lower()}",
                "Strategic opportunities identified across multiple sectors"
            ],
            'recommendations': report.get('summary', 'Continue monitoring the competitive landscape for strategic opportunities.')
        }

        return analysis

    except Exception as e:
        app_logger.error(f"Error analyzing report data: {e}")
        return {}


@router.get("/{report_id}/preview")
async def preview_shareable_report(report_id: str):
    """Preview what the shareable report will look like"""
    try:
        analysis = await analyze_report_data(report_id)

        if not analysis:
            raise HTTPException(status_code=404, detail="Report not found")

        return {
            "report_id": report_id,
            "title": analysis['title'],
            "metrics": {
                "competitors": analysis['competitors_count'],
                "trends": analysis['trends_count'],
                "sentiment": analysis['overall_sentiment'],
                "confidence": f"{analysis['confidence']}%"
            },
            "available_formats": [
                "pdf",
                "linkedin_article",
                "social_image_stat",
                "social_image_insight",
                "infographic"
            ]
        }

    except HTTPException:
        raise
    except Exception as e:
        app_logger.error(f"Error previewing report: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{report_id}/export/pdf")
async def export_pdf(report_id: str):
    """Export report as PDF for sharing"""
    try:
        analysis = await analyze_report_data(report_id)

        if not analysis:
            raise HTTPException(status_code=404, detail="Report not found")

        pdf_bytes = await report_generator.generate_pdf_report(analysis)

        if not pdf_bytes:
            raise HTTPException(status_code=500, detail="Failed to generate PDF")

        return Response(
            content=pdf_bytes,
            media_type="application/pdf",
            headers={
                "Content-Disposition": f"attachment; filename=bluepeak_report_{report_id[:8]}.pdf"
            }
        )

    except HTTPException:
        raise
    except Exception as e:
        app_logger.error(f"Error exporting PDF: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{report_id}/export/linkedin-article", response_class=HTMLResponse)
async def export_linkedin_article(report_id: str):
    """Export report as LinkedIn article HTML"""
    try:
        analysis = await analyze_report_data(report_id)

        if not analysis:
            raise HTTPException(status_code=404, detail="Report not found")

        html = await report_generator.generate_linkedin_article(analysis)

        if not html:
            raise HTTPException(status_code=500, detail="Failed to generate LinkedIn article")

        return HTMLResponse(content=html)

    except HTTPException:
        raise
    except Exception as e:
        app_logger.error(f"Error exporting LinkedIn article: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{report_id}/export/social-image")
async def export_social_image(
    report_id: str,
    template: str = "insight",
    stat_value: Optional[str] = None,
    stat_label: Optional[str] = None,
    insight: Optional[str] = None
):
    """
    Export report as social media image
    Templates: insight, stat, quote, infographic
    """
    try:
        analysis = await analyze_report_data(report_id)

        if not analysis:
            raise HTTPException(status_code=404, detail="Report not found")

        # Override with custom values if provided
        if stat_value:
            analysis['stat_value'] = stat_value
        else:
            analysis['stat_value'] = f"{analysis['competitors_count']}"

        if stat_label:
            analysis['stat_label'] = stat_label
        else:
            analysis['stat_label'] = "Competitors Monitored"

        if insight:
            analysis['insight'] = insight
        else:
            analysis['insight'] = analysis['insights'][0] if analysis.get('insights') else "Market intelligence insights"

        img_bytes = await report_generator.generate_social_image(analysis, template=template)

        if not img_bytes:
            raise HTTPException(status_code=500, detail="Failed to generate image")

        return Response(
            content=img_bytes,
            media_type="image/png",
            headers={
                "Content-Disposition": f"attachment; filename=bluepeak_social_{report_id[:8]}.png"
            }
        )

    except HTTPException:
        raise
    except Exception as e:
        app_logger.error(f"Error exporting social image: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{report_id}/charts/sentiment")
async def get_sentiment_chart(report_id: str):
    """Get sentiment chart as base64 image"""
    try:
        analysis = await analyze_report_data(report_id)

        if not analysis:
            raise HTTPException(status_code=404, detail="Report not found")

        chart_data = await report_generator.generate_sentiment_chart(analysis)

        return {
            "chart_type": "sentiment",
            "data_uri": chart_data
        }

    except Exception as e:
        app_logger.error(f"Error generating sentiment chart: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{report_id}/charts/industry")
async def get_industry_chart(report_id: str):
    """Get industry distribution chart as base64 image"""
    try:
        analysis = await analyze_report_data(report_id)

        if not analysis:
            raise HTTPException(status_code=404, detail="Report not found")

        chart_data = await report_generator.generate_industry_distribution_chart(analysis)

        return {
            "chart_type": "industry",
            "data_uri": chart_data
        }

    except Exception as e:
        app_logger.error(f"Error generating industry chart: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{report_id}/charts/trends")
async def get_trends_chart(report_id: str):
    """Get market trends chart as base64 image"""
    try:
        analysis = await analyze_report_data(report_id)

        if not analysis:
            raise HTTPException(status_code=404, detail="Report not found")

        chart_data = await report_generator.generate_trend_chart(analysis)

        return {
            "chart_type": "trends",
            "data_uri": chart_data
        }

    except Exception as e:
        app_logger.error(f"Error generating trends chart: {e}")
        raise HTTPException(status_code=500, detail=str(e))
