"""
Slack integration module
"""
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from app.core.config import settings
from app.core.logger import app_logger
from typing import Dict, Any, Optional


class SlackIntegration:
    """Slack integration for notifications"""

    def __init__(self):
        self.client = None
        if settings.SLACK_BOT_TOKEN:
            self.client = WebClient(token=settings.SLACK_BOT_TOKEN)
            app_logger.info("Slack integration initialized")

    async def send_message(self, channel: str, text: str, blocks: Optional[list] = None) -> bool:
        """Send a message to a Slack channel"""
        if not self.client:
            app_logger.warning("Slack client not initialized")
            return False

        try:
            response = self.client.chat_postMessage(
                channel=channel,
                text=text,
                blocks=blocks
            )
            app_logger.info(f"Message sent to Slack channel {channel}")
            return True
        except SlackApiError as e:
            app_logger.error(f"Error sending Slack message: {e}")
            return False

    async def send_competitor_alert(self, competitor_data: Dict[str, Any], channel: str) -> bool:
        """Send competitor alert to Slack"""
        blocks = [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": f"🔔 New Competitor Alert: {competitor_data.get('name', 'Unknown')}"
                }
            },
            {
                "type": "section",
                "fields": [
                    {
                        "type": "mrkdwn",
                        "text": f"*Industry:*\n{competitor_data.get('industry', 'N/A')}"
                    },
                    {
                        "type": "mrkdwn",
                        "text": f"*Status:*\n{competitor_data.get('status', 'N/A')}"
                    }
                ]
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*Description:*\n{competitor_data.get('description', 'No description available')}"
                }
            }
        ]

        return await self.send_message(
            channel=channel,
            text=f"New competitor detected: {competitor_data.get('name')}",
            blocks=blocks
        )

    async def send_trend_alert(self, trend_data: Dict[str, Any], channel: str) -> bool:
        """Send trend alert to Slack"""
        status_emoji = {
            "emerging": "🌟",
            "growing": "📈",
            "declining": "📉",
            "stable": "➡️"
        }

        emoji = status_emoji.get(trend_data.get('status', 'stable'), "📊")

        blocks = [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": f"{emoji} Trend Alert: {trend_data.get('title', 'Unknown')}"
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*Description:*\n{trend_data.get('description', 'N/A')}"
                }
            },
            {
                "type": "section",
                "fields": [
                    {
                        "type": "mrkdwn",
                        "text": f"*Status:*\n{trend_data.get('status', 'N/A')}"
                    },
                    {
                        "type": "mrkdwn",
                        "text": f"*Confidence:*\n{int(trend_data.get('confidence_score', 0) * 100)}%"
                    }
                ]
            }
        ]

        return await self.send_message(
            channel=channel,
            text=f"New trend detected: {trend_data.get('title')}",
            blocks=blocks
        )

    async def send_report_notification(self, report_data: Dict[str, Any], channel: str) -> bool:
        """Send report generation notification to Slack"""
        blocks = [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": f"📄 New Report: {report_data.get('title', 'Unknown')}"
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*Summary:*\n{report_data.get('summary', 'No summary available')}"
                }
            },
            {
                "type": "section",
                "fields": [
                    {
                        "type": "mrkdwn",
                        "text": f"*Type:*\n{report_data.get('report_type', 'N/A')}"
                    },
                    {
                        "type": "mrkdwn",
                        "text": f"*Generated:*\n{report_data.get('created_at', 'N/A')}"
                    }
                ]
            }
        ]

        return await self.send_message(
            channel=channel,
            text=f"New report generated: {report_data.get('title')}",
            blocks=blocks
        )


# Global instance
slack_integration = SlackIntegration()
