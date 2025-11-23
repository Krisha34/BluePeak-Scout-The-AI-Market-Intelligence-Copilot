"""
Synthesis & Reporting Agent - Generates comprehensive reports
"""
from typing import Dict, Any, List
from agents.base_agent import BaseAgent
from app.core.logger import app_logger
import json
from datetime import datetime


class SynthesisReportingAgent(BaseAgent):
    """
    Specialized agent for synthesizing information and generating reports
    """

    def __init__(self):
        super().__init__(
            name="Synthesis & Reporting Agent",
            description="Synthesizes data from multiple sources and generates comprehensive analytical reports"
        )

    async def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute report generation

        Args:
            task: Contains report_type, data_sources, format

        Returns:
            Generated report
        """
        report_type = task.get("report_type", "comprehensive")
        data_sources = task.get("data_sources", [])
        report_format = task.get("format", "markdown")

        app_logger.info(f"Generating {report_type} report from {len(data_sources)} sources")

        report = await self.generate_report(report_type, data_sources, report_format)

        return self.format_response(
            content=report,
            metadata={
                "report_type": report_type,
                "sources_count": len(data_sources),
                "format": report_format
            }
        )

    async def generate_report(self, report_type: str, data_sources: List[Dict[str, Any]], format_type: str) -> str:
        """Generate a comprehensive report"""

        prompt = f"""You are an expert business analyst. Generate a {report_type} report.

Data Sources ({len(data_sources)}):
{json.dumps(data_sources[:3], indent=2)}

Report Type: {report_type}
Format: {format_type}

Create a professional report with:

# Executive Summary
Brief overview of key findings and recommendations

# Market Overview
Current market landscape and dynamics

# Competitive Analysis
Detailed competitor insights and positioning

# Trend Analysis
Emerging and existing market trends

# Key Findings
Critical insights and discoveries

# Strategic Recommendations
Actionable recommendations based on analysis

# Risk Assessment
Potential challenges and mitigation strategies

# Conclusion
Summary and next steps

Use clear headings, bullet points, and data-driven insights."""

        report = await self.invoke_llm(prompt)
        return report

    async def synthesize_agent_outputs(self, agent_outputs: List[Dict[str, Any]]) -> str:
        """Synthesize outputs from multiple agents"""

        prompt = f"""Synthesize insights from these specialized agents:

{json.dumps(agent_outputs, indent=2)}

Create a cohesive narrative that:
1. Integrates all findings
2. Identifies patterns across sources
3. Resolves any contradictions
4. Highlights most important insights
5. Provides unified recommendations

Format as comprehensive synthesis."""

        synthesis = await self.invoke_llm(prompt)
        return synthesis

    async def generate_executive_summary(self, full_report: str) -> str:
        """Generate executive summary from full report"""

        prompt = f"""Create a concise executive summary from this report:

{full_report[:3000]}

Executive summary should:
- Be 250-300 words
- Highlight key findings
- Present critical recommendations
- Be accessible to C-level executives
- Focus on business impact"""

        summary = await self.invoke_llm(prompt)
        return summary

    async def create_competitor_report(self, competitor_data: Dict[str, Any], findings: List[Dict[str, Any]]) -> str:
        """Create a detailed competitor report"""

        prompt = f"""Generate a comprehensive competitor report for:

Competitor: {competitor_data.get('name', 'Unknown')}
Industry: {competitor_data.get('industry', 'Unknown')}

Recent Findings ({len(findings)}):
{json.dumps(findings[:5], indent=2)}

Include:
1. Company Overview
2. Market Position
3. Product/Service Analysis
4. Pricing Strategy
5. Recent Developments
6. SWOT Analysis
7. Threat Assessment
8. Monitoring Recommendations

Format as professional intelligence report."""

        report = await self.invoke_llm(prompt)
        return report

    async def create_trend_report(self, trends: List[Dict[str, Any]], industry: str) -> str:
        """Create a market trends report"""

        prompt = f"""Generate a market trends report for {industry}:

Identified Trends ({len(trends)}):
{json.dumps(trends, indent=2)}

Include:
1. Trend Overview
2. Detailed Analysis of Each Trend
3. Market Impact Assessment
4. Adoption Predictions
5. Strategic Opportunities
6. Risk Considerations
7. Recommendations

Format as professional market analysis report."""

        report = await self.invoke_llm(prompt)
        return report

    async def create_periodic_digest(self, period: str, data: Dict[str, Any]) -> str:
        """Create a periodic digest (daily/weekly/monthly)"""

        prompt = f"""Create a {period} digest report:

Data Summary:
{json.dumps(data, indent=2)}

Include:
- **Period Highlights**: Key events and developments
- **New Competitors**: Recently added or discovered
- **Trending Topics**: Most discussed themes
- **Important Findings**: Critical intelligence
- **Metrics Dashboard**: Key performance indicators
- **Action Items**: Recommended follow-ups

Format as engaging digest suitable for email distribution."""

        digest = await self.invoke_llm(prompt)
        return digest

    async def format_for_distribution(self, content: str, channel: str) -> str:
        """Format report for different distribution channels"""

        format_specs = {
            "email": "HTML email format with clear sections",
            "slack": "Slack message format with markdown",
            "pdf": "PDF-ready format with proper structure",
            "dashboard": "Dashboard widget format, concise"
        }

        prompt = f"""Reformat this content for {channel} distribution:

{content[:2000]}

Target Format: {format_specs.get(channel, 'standard')}

Optimize for readability and engagement on {channel}."""

        formatted = await self.invoke_llm(prompt)
        return formatted
