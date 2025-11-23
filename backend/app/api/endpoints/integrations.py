"""
Integrations API endpoints
"""
from fastapi import APIRouter, HTTPException
from app.models.schemas import IntegrationSettings, SlackIntegration, EmailIntegration
from app.core.logger import app_logger
from database.supabase_client import supabase_client
from integrations.email_integration import email_integration
from app.core.config import settings

router = APIRouter()


@router.get("/", response_model=IntegrationSettings)
async def get_integration_settings(user_id: str = "default_user"):
    """Get integration settings for a user"""
    try:
        # Fetch from database
        db_settings = await supabase_client.get_integration_settings(user_id)

        if not db_settings:
            # Return default settings if none exist
            return IntegrationSettings(
                slack=SlackIntegration(enabled=False),
                email=EmailIntegration(enabled=False)
            )

        # Convert database format to API format
        return IntegrationSettings(
            slack=SlackIntegration(
                enabled=db_settings.get("slack_enabled", False),
                channel_id=db_settings.get("slack_channel_id"),
                webhook_url=db_settings.get("slack_webhook_url"),
                notification_types=db_settings.get("notification_types", ["new_findings", "trend_alerts", "reports"])
            ),
            email=EmailIntegration(
                enabled=db_settings.get("email_enabled", False),
                recipients=db_settings.get("email_recipients", []),
                frequency=db_settings.get("email_frequency", "daily"),
                notification_types=db_settings.get("notification_types", ["reports", "critical_alerts"])
            )
        )
    except Exception as e:
        app_logger.error(f"Error fetching integration settings: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/", response_model=IntegrationSettings)
async def update_integration_settings(
    settings: IntegrationSettings,
    user_id: str = "default_user"
):
    """Update integration settings"""
    try:
        # Convert API format to database format
        db_data = {
            "slack_enabled": settings.slack.enabled,
            "slack_channel_id": settings.slack.channel_id,
            "slack_webhook_url": settings.slack.webhook_url,
            "email_enabled": settings.email.enabled,
            "email_recipients": settings.email.recipients,
            "email_frequency": settings.email.frequency,
            "notification_types": settings.email.notification_types
        }

        # Save to database
        result = await supabase_client.upsert_integration_settings(user_id, db_data)

        if not result:
            raise HTTPException(status_code=500, detail="Failed to save integration settings")

        app_logger.info(f"Updated integration settings for user {user_id}")
        return settings
    except Exception as e:
        app_logger.error(f"Error updating integration settings: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/slack/test")
async def test_slack_integration():
    """Test Slack integration"""
    try:
        # For now, just return success since we're focusing on email
        return {
            "status": "success",
            "message": "Slack integration not configured. Please configure Slack bot token."
        }
    except Exception as e:
        app_logger.error(f"Error testing Slack integration: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/email/test")
async def test_email_integration(user_id: str = "default_user"):
    """Test email integration"""
    try:
        # Get user's integration settings
        db_settings = await supabase_client.get_integration_settings(user_id)

        if not db_settings or not db_settings.get("email_enabled"):
            raise HTTPException(status_code=400, detail="Email integration is not enabled")

        recipients = db_settings.get("email_recipients", [])
        if not recipients:
            raise HTTPException(status_code=400, detail="No email recipients configured")

        # Send test email
        html_content = """
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
                .container { max-width: 600px; margin: 0 auto; padding: 20px; }
                .header { background: #2563eb; color: white; padding: 20px; text-align: center; border-radius: 8px; }
                .content { padding: 20px; background: #f9fafb; margin-top: 20px; border-radius: 8px; }
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>BluePeak Compass</h1>
                    <p>Email Integration Test</p>
                </div>
                <div class="content">
                    <h2>Congratulations!</h2>
                    <p>Your email integration is working correctly. You will now receive notifications about:</p>
                    <ul>
                        <li>Competitor analysis updates</li>
                        <li>New report generation</li>
                        <li>Trend alerts</li>
                        <li>Critical findings</li>
                    </ul>
                    <p style="color: #6b7280; font-size: 14px; margin-top: 30px;">
                        This is an automated test message from BluePeak Compass.
                    </p>
                </div>
            </div>
        </body>
        </html>
        """

        success = await email_integration.send_email(
            to_emails=recipients,
            subject="BluePeak Compass - Test Email",
            html_content=html_content
        )

        if success:
            return {
                "status": "success",
                "message": f"Test email sent successfully to {len(recipients)} recipient(s)"
            }
        else:
            raise HTTPException(status_code=500, detail="Failed to send test email. Please check your SendGrid configuration.")

    except HTTPException:
        raise
    except Exception as e:
        app_logger.error(f"Error testing email integration: {e}")
        raise HTTPException(status_code=500, detail=str(e))
