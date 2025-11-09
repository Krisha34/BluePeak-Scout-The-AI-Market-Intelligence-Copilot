#!/usr/bin/env python3
"""
Quick SendGrid test script
"""
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

api_key = os.environ.get('SENDGRID_API_KEY')
if not api_key:
    raise ValueError("SENDGRID_API_KEY environment variable not set")

from_email = 'moneshrallapalli@gmail.com'
to_email = 'moneshrallapalli@gmail.com'

message = Mail(
    from_email=from_email,
    to_emails=to_email,
    subject='SendGrid Test - BluePeak Compass',
    html_content='''
    <html>
    <body style="font-family: Arial, sans-serif;">
        <h1 style="color: #2563eb;">SendGrid Test Email</h1>
        <p>If you receive this, SendGrid is working correctly!</p>
        <p><strong>From:</strong> ''' + from_email + '''</p>
        <p><strong>To:</strong> ''' + to_email + '''</p>
        <p><strong>Time:</strong> Just now</p>
    </body>
    </html>
    '''
)

try:
    sg = SendGridAPIClient(api_key)
    response = sg.send(message)

    print(f"✓ Email sent successfully!")
    print(f"  Status Code: {response.status_code}")
    print(f"  Response Body: {response.body}")
    print(f"  Response Headers: {response.headers}")

    if response.status_code == 202:
        print("\n✓ SendGrid accepted the email (202 Accepted)")
        print("  The email should arrive within 1-5 minutes")
        print("  Check your inbox and spam folder")
    else:
        print(f"\n⚠ Unexpected status code: {response.status_code}")

except Exception as e:
    print(f"✗ Error sending email: {e}")
    import traceback
    traceback.print_exc()
