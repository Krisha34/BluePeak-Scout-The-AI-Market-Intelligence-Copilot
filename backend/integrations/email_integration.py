"""
Email integration module using SendGrid
"""
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Email, To, Content
from app.core.config import settings
from app.core.logger import app_logger
from typing import List, Dict, Any


class EmailIntegration:
    """Email integration for notifications and reports"""

    def __init__(self):
        self.client = None
        if settings.SENDGRID_API_KEY:
            self.client = SendGridAPIClient(settings.SENDGRID_API_KEY)
            app_logger.info("Email integration initialized")

    async def send_email(
        self,
        to_emails: List[str],
        subject: str,
        html_content: str,
        from_email: str = None
    ) -> bool:
        """Send an email"""
        if not self.client:
            app_logger.warning("SendGrid client not initialized")
            return False

        try:
            message = Mail(
                from_email=from_email or settings.FROM_EMAIL,
                to_emails=to_emails,
                subject=subject,
                html_content=html_content
            )

            response = self.client.send(message)
            app_logger.info(f"Email sent to {len(to_emails)} recipients")
            return response.status_code == 202
        except Exception as e:
            app_logger.error(f"Error sending email: {e}")
            return False

    async def send_daily_digest(self, to_emails: List[str], digest_data: Dict[str, Any]) -> bool:
        """Send daily digest email"""
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background: #2563eb; color: white; padding: 20px; text-align: center; }}
                .section {{ margin: 20px 0; padding: 15px; background: #f9fafb; border-left: 4px solid #2563eb; }}
                .metric {{ display: inline-block; margin: 10px 20px 10px 0; }}
                .metric-value {{ font-size: 24px; font-weight: bold; color: #2563eb; }}
                .metric-label {{ font-size: 12px; color: #6b7280; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>BluePeak Compass Daily Digest</h1>
                </div>

                <div class="section">
                    <h2>📊 Today's Overview</h2>
                    <div class="metric">
                        <div class="metric-value">{digest_data.get('new_findings', 0)}</div>
                        <div class="metric-label">New Findings</div>
                    </div>
                    <div class="metric">
                        <div class="metric-value">{digest_data.get('new_trends', 0)}</div>
                        <div class="metric-label">New Trends</div>
                    </div>
                    <div class="metric">
                        <div class="metric-value">{digest_data.get('reports_generated', 0)}</div>
                        <div class="metric-label">Reports Generated</div>
                    </div>
                </div>

                <div class="section">
                    <h2>🎯 Key Highlights</h2>
                    <ul>
                        {self._format_highlights(digest_data.get('highlights', []))}
                    </ul>
                </div>

                <div class="section">
                    <h2>📈 Trending Topics</h2>
                    <ul>
                        {self._format_trends(digest_data.get('trends', []))}
                    </ul>
                </div>

                <p style="text-align: center; color: #6b7280; font-size: 12px; margin-top: 40px;">
                    © 2024 BluePeak Compass. All rights reserved.
                </p>
            </div>
        </body>
        </html>
        """

        return await self.send_email(
            to_emails=to_emails,
            subject="BluePeak Compass - Daily Intelligence Digest",
            html_content=html_content
        )

    def _format_highlights(self, highlights: List[str]) -> str:
        """Format highlights for email"""
        return "\n".join([f"<li>{h}</li>" for h in highlights])

    def _format_trends(self, trends: List[Dict[str, Any]]) -> str:
        """Format trends for email"""
        return "\n".join([
            f"<li><strong>{t.get('title', 'Unknown')}</strong> - {t.get('description', 'N/A')[:100]}...</li>"
            for t in trends
        ])

    async def send_report_email(
        self,
        to_emails: List[str],
        report_data: Dict[str, Any]
    ) -> bool:
        """Send report via email"""
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 800px; margin: 0 auto; padding: 20px; }}
                .header {{ background: #2563eb; color: white; padding: 20px; text-align: center; }}
                .content {{ padding: 20px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>{report_data.get('title', 'Intelligence Report')}</h1>
                </div>
                <div class="content">
                    <h2>Executive Summary</h2>
                    <p>{report_data.get('summary', 'No summary available')}</p>

                    <h2>Full Report</h2>
                    <div style="white-space: pre-wrap;">
                        {report_data.get('content', 'No content available')[:5000]}
                    </div>
                </div>
            </div>
        </body>
        </html>
        """

        return await self.send_email(
            to_emails=to_emails,
            subject=f"BluePeak Compass Report: {report_data.get('title')}",
            html_content=html_content
        )


# Global instance
email_integration = EmailIntegration()
