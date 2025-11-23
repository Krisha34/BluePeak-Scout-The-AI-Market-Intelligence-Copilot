"""
Social Media Shareable Report Generation Service
Generates reports in multiple formats: PDF, Images, LinkedIn Articles, Infographics
"""
import io
import base64
from datetime import datetime
from typing import Dict, List, Any, Optional
import matplotlib
matplotlib.use('Agg')  # Use non-GUI backend
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px
from PIL import Image, ImageDraw, ImageFont
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image as RLImage
from reportlab.lib.units import inch
from app.core.logger import app_logger


class ReportGenerator:
    """Generate shareable reports for social media"""

    def __init__(self):
        self.brand_color = "#2563eb"  # BluePeak blue
        self.secondary_color = "#10b981"  # Green for positive
        self.negative_color = "#ef4444"  # Red for negative

    async def generate_sentiment_chart(self, data: Dict[str, Any], format: str = "plotly") -> str:
        """
        Generate sentiment analysis chart
        Returns: base64 encoded image or plotly JSON
        """
        try:
            sentiments = data.get('sentiments', {
                'positive': 45,
                'neutral': 35,
                'negative': 15,
                'mixed': 5
            })

            if format == "plotly":
                # Create interactive plotly chart
                fig = go.Figure(data=[go.Pie(
                    labels=list(sentiments.keys()),
                    values=list(sentiments.values()),
                    marker=dict(colors=['#10b981', '#6b7280', '#ef4444', '#f59e0b']),
                    textinfo='label+percent',
                    textfont=dict(size=14, color='white'),
                    hole=0.4
                )])

                fig.update_layout(
                    title=dict(
                        text='Sentiment Distribution',
                        font=dict(size=20, color=self.brand_color, family='Arial')
                    ),
                    showlegend=True,
                    height=400,
                    margin=dict(t=50, b=50, l=50, r=50)
                )

                # Convert to base64 image
                img_bytes = fig.to_image(format="png", width=800, height=400)
                img_base64 = base64.b64encode(img_bytes).decode()
                return f"data:image/png;base64,{img_base64}"

            else:  # matplotlib
                fig, ax = plt.subplots(figsize=(10, 6))
                colors_list = ['#10b981', '#6b7280', '#ef4444', '#f59e0b']
                wedges, texts, autotexts = ax.pie(
                    sentiments.values(),
                    labels=sentiments.keys(),
                    autopct='%1.1f%%',
                    colors=colors_list,
                    startangle=90
                )
                ax.set_title('Sentiment Distribution', fontsize=16, color=self.brand_color, pad=20)

                # Save to bytes
                buf = io.BytesIO()
                plt.savefig(buf, format='png', dpi=150, bbox_inches='tight')
                buf.seek(0)
                img_base64 = base64.b64encode(buf.getvalue()).decode()
                plt.close()

                return f"data:image/png;base64,{img_base64}"

        except Exception as e:
            app_logger.error(f"Error generating sentiment chart: {e}")
            return ""

    async def generate_industry_distribution_chart(self, data: Dict[str, Any]) -> str:
        """Generate industry distribution bar chart"""
        try:
            industries = data.get('industries', {
                'Technology': 35,
                'Healthcare': 25,
                'Finance': 20,
                'Retail': 12,
                'Manufacturing': 8
            })

            fig = go.Figure(data=[go.Bar(
                x=list(industries.keys()),
                y=list(industries.values()),
                marker=dict(color=self.brand_color),
                text=list(industries.values()),
                textposition='outside'
            )])

            fig.update_layout(
                title=dict(
                    text='Industry Distribution',
                    font=dict(size=20, color=self.brand_color, family='Arial')
                ),
                xaxis_title='Industry',
                yaxis_title='Percentage (%)',
                height=400,
                margin=dict(t=50, b=50, l=50, r=50),
                showlegend=False
            )

            img_bytes = fig.to_image(format="png", width=800, height=400)
            img_base64 = base64.b64encode(img_bytes).decode()
            return f"data:image/png;base64,{img_base64}"

        except Exception as e:
            app_logger.error(f"Error generating industry chart: {e}")
            return ""

    async def generate_trend_chart(self, data: Dict[str, Any]) -> str:
        """Generate market trends line chart"""
        try:
            trends = data.get('trends', {
                'dates': ['Week 1', 'Week 2', 'Week 3', 'Week 4'],
                'ai_adoption': [45, 52, 58, 65],
                'cloud_migration': [30, 35, 38, 42],
                'automation': [25, 28, 32, 38]
            })

            fig = go.Figure()

            for trend_name, values in trends.items():
                if trend_name != 'dates':
                    fig.add_trace(go.Scatter(
                        x=trends['dates'],
                        y=values,
                        mode='lines+markers',
                        name=trend_name.replace('_', ' ').title(),
                        line=dict(width=3)
                    ))

            fig.update_layout(
                title=dict(
                    text='Market Trends Over Time',
                    font=dict(size=20, color=self.brand_color, family='Arial')
                ),
                xaxis_title='Time Period',
                yaxis_title='Trend Score',
                height=400,
                margin=dict(t=50, b=50, l=50, r=50),
                hovermode='x unified'
            )

            img_bytes = fig.to_image(format="png", width=800, height=400)
            img_base64 = base64.b64encode(img_bytes).decode()
            return f"data:image/png;base64,{img_base64}"

        except Exception as e:
            app_logger.error(f"Error generating trend chart: {e}")
            return ""

    async def generate_pdf_report(self, data: Dict[str, Any]) -> bytes:
        """Generate professional PDF report"""
        try:
            buffer = io.BytesIO()
            doc = SimpleDocTemplate(buffer, pagesize=letter)
            story = []
            styles = getSampleStyleSheet()

            # Custom styles
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=24,
                textColor=colors.HexColor(self.brand_color),
                spaceAfter=30,
                alignment=1  # Center
            )

            heading_style = ParagraphStyle(
                'CustomHeading',
                parent=styles['Heading2'],
                fontSize=16,
                textColor=colors.HexColor(self.brand_color),
                spaceBefore=20,
                spaceAfter=12
            )

            # Title
            title = Paragraph("BluePeak Compass<br/>Market Intelligence Report", title_style)
            story.append(title)
            story.append(Spacer(1, 0.3*inch))

            # Metadata
            meta_data = [
                ['Generated:', datetime.now().strftime('%B %d, %Y at %I:%M %p')],
                ['Report Type:', data.get('report_type', 'Comprehensive Analysis')],
                ['Period:', data.get('period', 'Last 30 Days')]
            ]

            meta_table = Table(meta_data, colWidths=[2*inch, 4*inch])
            meta_table.setStyle(TableStyle([
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('TEXTCOLOR', (0, 0), (0, -1), colors.grey),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ]))
            story.append(meta_table)
            story.append(Spacer(1, 0.5*inch))

            # Executive Summary
            story.append(Paragraph("Executive Summary", heading_style))
            summary_text = data.get('summary', 'Comprehensive market intelligence analysis covering competitive landscape, emerging trends, and strategic insights.')
            story.append(Paragraph(summary_text, styles['BodyText']))
            story.append(Spacer(1, 0.3*inch))

            # Key Metrics
            story.append(Paragraph("Key Metrics", heading_style))
            metrics = data.get('metrics', {
                'Competitors Monitored': data.get('competitors_count', 12),
                'Trends Identified': data.get('trends_count', 8),
                'Market Sentiment': data.get('overall_sentiment', 'Positive'),
                'Confidence Score': f"{data.get('confidence', 85)}%"
            })

            metrics_data = [[k, str(v)] for k, v in metrics.items()]
            metrics_table = Table(metrics_data, colWidths=[3*inch, 3*inch])
            metrics_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f9fafb')),
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 12),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('PADDING', (0, 0), (-1, -1), 12),
                ('GRID', (0, 0), (-1, -1), 1, colors.HexColor(self.brand_color)),
            ]))
            story.append(metrics_table)
            story.append(PageBreak())

            # Competitor Analysis
            story.append(Paragraph("Competitor Analysis", heading_style))
            competitors = data.get('competitors', [])
            if competitors:
                for comp in competitors[:5]:  # Top 5
                    comp_text = f"""<b>{comp.get('name', 'Unknown')}</b><br/>
                    Industry: {comp.get('industry', 'N/A')}<br/>
                    Status: {comp.get('status', 'N/A')}<br/>
                    Monitoring Score: {int(comp.get('monitoring_score', 0.5) * 100)}%<br/>
                    """
                    story.append(Paragraph(comp_text, styles['BodyText']))
                    story.append(Spacer(1, 0.2*inch))

            # Build PDF
            doc.build(story)
            buffer.seek(0)
            return buffer.getvalue()

        except Exception as e:
            app_logger.error(f"Error generating PDF: {e}")
            return b""

    async def generate_social_image(self, data: Dict[str, Any], template: str = "insight") -> bytes:
        """
        Generate shareable social media image post
        Templates: 'insight', 'stat', 'quote', 'infographic'
        """
        try:
            # Create base image (LinkedIn optimal size: 1200x627)
            img = Image.new('RGB', (1200, 627), color='#ffffff')
            draw = ImageDraw.Draw(img)

            # Try to load fonts, fallback to default
            try:
                title_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 48)
                body_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 32)
                small_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 24)
            except:
                title_font = ImageFont.load_default()
                body_font = ImageFont.load_default()
                small_font = ImageFont.load_default()

            # Draw brand header
            draw.rectangle([(0, 0), (1200, 100)], fill=self.brand_color)
            draw.text((60, 35), "BluePeak Compass", fill='#ffffff', font=title_font)

            if template == "stat":
                # Big number stat
                stat_value = str(data.get('stat_value', '85%'))
                stat_label = data.get('stat_label', 'Market Growth')

                # Draw big stat
                draw.text((600, 280), stat_value, fill=self.brand_color, font=title_font, anchor="mm")
                draw.text((600, 380), stat_label, fill='#6b7280', font=body_font, anchor="mm")

            elif template == "insight":
                # Key insight text
                insight = data.get('insight', 'AI adoption is accelerating across industries')
                # Word wrap the insight
                words = insight.split()
                lines = []
                current_line = []
                for word in words:
                    current_line.append(word)
                    if len(' '.join(current_line)) > 50:
                        lines.append(' '.join(current_line[:-1]))
                        current_line = [word]
                if current_line:
                    lines.append(' '.join(current_line))

                y_position = 200
                for line in lines:
                    draw.text((600, y_position), line, fill='#1f2937', font=body_font, anchor="mm")
                    y_position += 50

            # Footer
            draw.rectangle([(0, 557), (1200, 627)], fill='#f9fafb')
            draw.text((60, 580), f"Generated {datetime.now().strftime('%B %d, %Y')}",
                     fill='#6b7280', font=small_font)
            draw.text((1140, 580), "bluepeak.ai", fill=self.brand_color, font=small_font, anchor="rm")

            # Convert to bytes
            buffer = io.BytesIO()
            img.save(buffer, format='PNG', quality=95)
            buffer.seek(0)
            return buffer.getvalue()

        except Exception as e:
            app_logger.error(f"Error generating social image: {e}")
            return b""

    async def generate_linkedin_article(self, data: Dict[str, Any]) -> str:
        """Generate LinkedIn article HTML format"""
        try:
            # Generate charts as base64
            sentiment_chart = await self.generate_sentiment_chart(data)
            industry_chart = await self.generate_industry_distribution_chart(data)
            trend_chart = await self.generate_trend_chart(data)

            html = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>{data.get('title', 'Market Intelligence Report')}</title>
                <style>
                    body {{
                        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
                        line-height: 1.6;
                        color: #1f2937;
                        max-width: 680px;
                        margin: 0 auto;
                        padding: 20px;
                    }}
                    h1 {{
                        color: {self.brand_color};
                        font-size: 2.5em;
                        margin-bottom: 0.5em;
                    }}
                    h2 {{
                        color: {self.brand_color};
                        font-size: 1.8em;
                        margin-top: 1.5em;
                        border-bottom: 3px solid {self.brand_color};
                        padding-bottom: 0.3em;
                    }}
                    .meta {{
                        color: #6b7280;
                        font-size: 0.9em;
                        margin-bottom: 2em;
                    }}
                    .highlight {{
                        background: #eff6ff;
                        border-left: 4px solid {self.brand_color};
                        padding: 1em;
                        margin: 1.5em 0;
                    }}
                    .metric-grid {{
                        display: grid;
                        grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
                        gap: 1em;
                        margin: 1.5em 0;
                    }}
                    .metric-card {{
                        background: #f9fafb;
                        padding: 1em;
                        border-radius: 8px;
                        text-align: center;
                    }}
                    .metric-value {{
                        font-size: 2em;
                        font-weight: bold;
                        color: {self.brand_color};
                    }}
                    .metric-label {{
                        font-size: 0.9em;
                        color: #6b7280;
                        margin-top: 0.5em;
                    }}
                    .chart {{
                        margin: 2em 0;
                        text-align: center;
                    }}
                    .chart img {{
                        max-width: 100%;
                        height: auto;
                        border-radius: 8px;
                        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
                    }}
                    .footer {{
                        margin-top: 3em;
                        padding-top: 2em;
                        border-top: 1px solid #e5e7eb;
                        text-align: center;
                        color: #6b7280;
                        font-size: 0.9em;
                    }}
                </style>
            </head>
            <body>
                <h1>{data.get('title', 'Market Intelligence Report')}</h1>
                <div class="meta">
                    Published on {datetime.now().strftime('%B %d, %Y')} | BluePeak Compass
                </div>

                <div class="highlight">
                    <strong>Executive Summary:</strong>
                    {data.get('summary', 'Comprehensive analysis of market trends, competitive landscape, and strategic insights.')}
                </div>

                <h2>Key Metrics</h2>
                <div class="metric-grid">
                    <div class="metric-card">
                        <div class="metric-value">{data.get('competitors_count', 12)}</div>
                        <div class="metric-label">Competitors Monitored</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-value">{data.get('trends_count', 8)}</div>
                        <div class="metric-label">Trends Identified</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-value">{data.get('confidence', 85)}%</div>
                        <div class="metric-label">Confidence Score</div>
                    </div>
                </div>

                <h2>Sentiment Analysis</h2>
                <div class="chart">
                    <img src="{sentiment_chart}" alt="Sentiment Distribution" />
                </div>

                <h2>Industry Distribution</h2>
                <div class="chart">
                    <img src="{industry_chart}" alt="Industry Distribution" />
                </div>

                <h2>Market Trends</h2>
                <div class="chart">
                    <img src="{trend_chart}" alt="Market Trends" />
                </div>

                <h2>Key Insights</h2>
                <ul>
                    {self._format_insights_list(data.get('insights', []))}
                </ul>

                <h2>Strategic Recommendations</h2>
                <p>{data.get('recommendations', 'Continue monitoring competitive landscape and emerging trends for strategic opportunities.')}</p>

                <div class="footer">
                    <p><strong>BluePeak Compass</strong> - AI-Powered Competitive Intelligence</p>
                    <p>Generated with advanced AI analysis | Visit bluepeak.ai for more insights</p>
                </div>
            </body>
            </html>
            """

            return html

        except Exception as e:
            app_logger.error(f"Error generating LinkedIn article: {e}")
            return ""

    def _format_insights_list(self, insights: List[str]) -> str:
        """Format insights as HTML list items"""
        if not insights:
            insights = [
                "AI adoption accelerating across key industries",
                "Sentiment trending positive for emerging technologies",
                "Competitive landscape shows increased innovation",
                "Market opportunities in automation and cloud services"
            ]
        return '\n'.join([f"<li>{insight}</li>" for insight in insights])


# Global instance
report_generator = ReportGenerator()
