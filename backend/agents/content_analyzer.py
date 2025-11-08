"""
Content Analyzer Agent - Analyzes content, documents, and communications
"""
from typing import Dict, Any, List
from agents.base_agent import BaseAgent
from app.core.logger import app_logger
import json


class ContentAnalyzerAgent(BaseAgent):
    """
    Specialized agent for content analysis and extraction of insights
    """

    def __init__(self):
        super().__init__(
            name="Content Analyzer Agent",
            description="Analyzes content, extracts key insights, and identifies important information"
        )

    async def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute content analysis

        Args:
            task: Contains content, analysis_type, focus_areas

        Returns:
            Content analysis results
        """
        content = task.get("content", "")
        analysis_type = task.get("analysis_type", "comprehensive")
        focus_areas = task.get("focus_areas", [])

        app_logger.info(f"Analyzing content: {len(content)} characters")

        analysis = await self.analyze_content(content, analysis_type, focus_areas)

        return self.format_response(
            content=analysis,
            metadata={
                "content_length": len(content),
                "analysis_type": analysis_type
            }
        )

    async def analyze_content(self, content: str, analysis_type: str, focus_areas: List[str]) -> str:
        """Perform comprehensive content analysis"""

        prompt = f"""You are a content analysis expert. Analyze the following content:

Content:
{content[:2000]}...  # Truncated for brevity

Analysis Type: {analysis_type}
Focus Areas: {', '.join(focus_areas) if focus_areas else 'General'}

Provide:
1. **Key Themes** - Main topics and subjects
2. **Important Entities** - Companies, people, products mentioned
3. **Sentiment & Tone** - Overall emotional context
4. **Key Insights** - Critical takeaways
5. **Factual Claims** - Verifiable statements
6. **Strategic Implications** - Business impact
7. **Action Items** - Recommended responses
8. **Content Quality** - Assessment of reliability

Format as structured JSON analysis."""

        analysis = await self.invoke_llm(prompt)
        return analysis

    async def extract_entities(self, content: str) -> Dict[str, Any]:
        """Extract named entities from content"""

        prompt = f"""Extract named entities from this content:

{content[:1500]}

Identify and categorize:
- Companies/Organizations
- People
- Products/Services
- Locations
- Technologies
- Financial figures
- Dates/Events

Format as JSON with categories."""

        response = await self.invoke_llm(prompt)

        return {
            "entities": response,
            "content_analyzed": len(content)
        }

    async def summarize_content(self, content: str, length: str = "medium") -> str:
        """Generate content summary"""

        length_tokens = {
            "short": "2-3 sentences",
            "medium": "1 paragraph",
            "long": "multiple paragraphs with bullet points"
        }

        prompt = f"""Summarize this content in {length_tokens.get(length, 'medium')} format:

{content[:3000]}

Focus on the most important and actionable information."""

        summary = await self.invoke_llm(prompt)
        return summary

    async def compare_content(self, content_list: List[str]) -> Dict[str, Any]:
        """Compare multiple pieces of content"""

        prompt = f"""Compare these {len(content_list)} pieces of content and identify:

1. Common themes
2. Differences in messaging
3. Unique insights from each
4. Contradictions or conflicts
5. Overall narrative

Content samples:
{json.dumps([c[:500] for c in content_list[:5]], indent=2)}

Format as comparative analysis."""

        comparison = await self.invoke_llm(prompt)

        return {
            "comparison": comparison,
            "items_compared": len(content_list)
        }

    async def assess_content_quality(self, content: str) -> Dict[str, Any]:
        """Assess the quality and credibility of content"""

        prompt = f"""Assess the quality of this content:

{content[:2000]}

Evaluate:
1. Credibility (0-10)
2. Factual accuracy indicators
3. Bias detection
4. Source reliability
5. Content depth
6. Actionability

Format as JSON assessment."""

        assessment = await self.invoke_llm(prompt)

        return {
            "quality_assessment": assessment
        }

    async def extract_competitive_intelligence(self, content: str, competitor_name: str) -> Dict[str, Any]:
        """Extract competitive intelligence from content"""

        prompt = f"""Extract competitive intelligence about {competitor_name} from:

{content[:2000]}

Focus on:
- Product/service information
- Pricing details
- Strategy indicators
- Customer feedback
- Market positioning
- Partnerships/alliances
- Future plans

Format as structured intelligence report."""

        intelligence = await self.invoke_llm(prompt)

        return {
            "intelligence": intelligence,
            "competitor": competitor_name
        }
