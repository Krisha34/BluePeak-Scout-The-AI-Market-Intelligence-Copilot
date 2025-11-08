"""
Competitive Intelligence Agent - Analyzes competitors and their strategies
"""
from typing import Dict, Any, List
from agents.base_agent import BaseAgent
from app.core.logger import app_logger
import json


class CompetitiveIntelligenceAgent(BaseAgent):
    """
    Specialized agent for competitive intelligence gathering and analysis
    """

    def __init__(self):
        super().__init__(
            name="Competitive Intelligence Agent",
            description="Analyzes competitor strategies, products, pricing, and market positioning"
        )

    async def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute competitive intelligence analysis

        Args:
            task: Contains competitor_data, analysis_type

        Returns:
            Comprehensive competitive intelligence findings
        """
        competitor_data = task.get("competitor_data", {})
        analysis_type = task.get("analysis_type", "comprehensive")

        app_logger.info(f"Analyzing competitor: {competitor_data.get('name', 'Unknown')}")

        # Perform analysis
        analysis = await self.analyze_competitor(competitor_data, analysis_type)

        return self.format_response(
            content=analysis,
            metadata={
                "competitor": competitor_data.get("name"),
                "analysis_type": analysis_type
            }
        )

    async def analyze_competitor(self, competitor_data: Dict[str, Any], analysis_type: str) -> str:
        """Perform detailed competitor analysis"""

        prompt = f"""You are a competitive intelligence analyst. Analyze the following competitor:

Competitor Information:
{json.dumps(competitor_data, indent=2)}

Analysis Type: {analysis_type}

Provide a comprehensive analysis including:
1. Market Position & Strategy
2. Strengths & Weaknesses (SWOT)
3. Product/Service Portfolio
4. Pricing Strategy
5. Target Market & Customer Segments
6. Recent Developments & News
7. Threat Level Assessment
8. Recommended Monitoring Areas

Format your response as structured JSON with clear sections."""

        analysis = await self.invoke_llm(prompt)
        return analysis

    async def identify_competitive_advantages(self, competitor_data: Dict[str, Any]) -> List[str]:
        """Identify key competitive advantages"""

        prompt = f"""Based on this competitor data:
{json.dumps(competitor_data, indent=2)}

List their top 5 competitive advantages in bullet points."""

        response = await self.invoke_llm(prompt)
        return response.split('\n')

    async def assess_threat_level(self, competitor_data: Dict[str, Any]) -> Dict[str, Any]:
        """Assess the threat level posed by a competitor"""

        prompt = f"""Assess the competitive threat level of:
{json.dumps(competitor_data, indent=2)}

Provide:
1. Threat Score (0-10)
2. Threat Category (Low/Medium/High/Critical)
3. Key Risk Factors
4. Mitigation Recommendations

Format as JSON."""

        response = await self.invoke_llm(prompt)

        return {
            "raw_assessment": response,
            "timestamp": "now"
        }

    async def monitor_competitor_changes(self, competitor_id: str, historical_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Monitor and identify significant changes in competitor activities"""

        prompt = f"""Analyze historical data for competitor {competitor_id}:
{json.dumps(historical_data, indent=2)}

Identify:
1. Significant changes or shifts
2. Emerging patterns
3. Strategic pivots
4. Areas requiring immediate attention

Format as structured analysis."""

        analysis = await self.invoke_llm(prompt)

        return {
            "changes_detected": analysis,
            "competitor_id": competitor_id,
            "data_points_analyzed": len(historical_data)
        }
