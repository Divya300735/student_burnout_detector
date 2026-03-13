#!/usr/bin/env python3
"""
Enhanced PDF Report Generator for Academic Burnout Analysis

This module generates comprehensive PDF reports using ReportLab with:
- Dataset Summary
- Risk Level Distribution  
- Strongest Burnout Indicators
- Embedded Graphs
- Statistical Observations
- Recommendations
"""

from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
import pandas as pd
import os
from datetime import datetime


class BurnoutPDFReport:
    def __init__(self, output_path):
        self.output_path = output_path
        self.doc = SimpleDocTemplate(output_path, pagesize=A4, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=18)
        self.styles = getSampleStyleSheet()
        self.story = []
        
        # Custom styles
        self.title_style = ParagraphStyle(
            'CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            spaceAfter=30,
            alignment=TA_CENTER,
            textColor=colors.HexColor('#2c3e50')
        )
        
        self.heading_style = ParagraphStyle(
            'CustomHeading',
            parent=self.styles['Heading2'],
            fontSize=18,
            spaceAfter=20,
            spaceBefore=20,
            textColor=colors.HexColor('#34495e')
        )
        
        self.subheading_style = ParagraphStyle(
            'CustomSubheading',
            parent=self.styles['Heading3'],
            fontSize=14,
            spaceAfter=12,
            spaceBefore=15,
            textColor=colors.HexColor('#3498db')
        )
        
        self.normal_style = ParagraphStyle(
            'CustomNormal',
            parent=self.styles['Normal'],
            fontSize=11,
            spaceAfter=12,
            alignment=TA_JUSTIFY
        )
        
        self.highlight_style = ParagraphStyle(
            'CustomHighlight',
            parent=self.styles['Normal'],
            fontSize=12,
            spaceAfter=10,
            textColor=colors.HexColor('#e74c3c'),
            fontName='Helvetica-Bold'
        )
    
    def add_title(self):
        """Add report title"""
        title = Paragraph("Academic Burnout Risk Analysis Report", self.title_style)
        self.story.append(title)
        
        # Add date and generation info
        date_str = datetime.now().strftime("%B %d, %Y")
        date_para = Paragraph(f"Generated on {date_str}", self.styles['Normal'])
        self.story.append(date_para)
        self.story.append(Spacer(1, 20))
    
    def add_dataset_summary(self, stats):
        """Add dataset summary section"""
        self.story.append(Paragraph("1️⃣ Dataset Summary", self.heading_style))
        
        data = [
            ['Metric', 'Value'],
            ['Total Students Analyzed', str(stats['total_students'])],
            ['Average Burnout Score', f"{stats['avg_burnout_score']}/10"],
            ['Minimum Burnout Score', f"{stats['min_burnout_score']}/10"],
            ['Maximum Burnout Score', f"{stats['max_burnout_score']}/10"],
            ['Standard Deviation', str(stats['std_burnout_score'])]
        ]
        
        table = Table(data, colWidths=[3*inch, 2*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3498db')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f8f9fa')),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#dee2e6'))
        ]))
        
        self.story.append(table)
        self.story.append(Spacer(1, 20))
    
    def add_risk_distribution(self, risk_dist):
        """Add risk level distribution section"""
        self.story.append(Paragraph("2️⃣ Risk Level Distribution", self.heading_style))
        
        data = [
            ['Risk Level', 'Number of Students', 'Percentage'],
            ['Low Risk (0-4)', str(risk_dist['Low Risk']['count']), f"{risk_dist['Low Risk']['percentage']}%"],
            ['Moderate Risk (4-7)', str(risk_dist['Moderate Risk']['count']), f"{risk_dist['Moderate Risk']['percentage']}%"],
            ['High Risk (7-10)', str(risk_dist['High Risk']['count']), f"{risk_dist['High Risk']['percentage']}%"]
        ]
        
        # Add color coding
        table = Table(data, colWidths=[2.5*inch, 2*inch, 1.5*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3498db')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (0, 1), colors.HexColor('#d5f4e6')),  # Low Risk - Green
            ('BACKGROUND', (0, 2), (0, 2), colors.HexColor('#fef9e7')),  # Moderate Risk - Yellow
            ('BACKGROUND', (0, 3), (0, 3), colors.HexColor('#fadbd8')),  # High Risk - Red
            ('BACKGROUND', (0, 1), (-1, 1), colors.HexColor('#f8f9fa')),
            ('BACKGROUND', (0, 2), (-1, 2), colors.HexColor('#f8f9fa')),
            ('BACKGROUND', (0, 3), (-1, 3), colors.HexColor('#f8f9fa')),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#dee2e6'))
        ]))
        
        self.story.append(table)
        self.story.append(Spacer(1, 20))
    
    def add_indicators(self, indicators):
        """Add strongest burnout indicators section"""
        self.story.append(Paragraph("3️⃣ Strongest Burnout Indicators", self.heading_style))
        
        data = [['Rank', 'Factor', 'Correlation', 'Direction']]
        for i, indicator in enumerate(indicators[:5], 1):
            factor_name = indicator['factor'].replace('_', ' ').title()
            direction = "Positive ↑" if indicator['direction'] == '↑' else "Negative ↓"
            data.append([str(i), factor_name, str(indicator['correlation']), direction])
        
        table = Table(data, colWidths=[0.8*inch, 2.5*inch, 1.2*inch, 1.5*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3498db')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f8f9fa')),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#dee2e6'))
        ]))
        
        self.story.append(table)
        self.story.append(Spacer(1, 20))
    
    def add_graphs(self, graphs_dir):
        """Add graphs section"""
        self.story.append(Paragraph("4️⃣ Risk Distribution Graphs", self.heading_style))
        
        graph_files = [
            ('Risk Pie Chart', 'risk_pie_chart.png'),
            ('Risk Bar Chart', 'risk_bar_chart.png'),
            ('Burnout Histogram', 'burnout_histogram.png')
        ]
        
        for title, filename in graph_files:
            graph_path = os.path.join(graphs_dir, filename)
            if os.path.exists(graph_path):
                self.story.append(Paragraph(title, self.subheading_style))
                
                # Add graph image
                img = Image(graph_path, width=5*inch, height=3.5*inch)
                self.story.append(img)
                self.story.append(Spacer(1, 15))
        
        self.story.append(Spacer(1, 20))
    
    def add_statistical_observations(self, indicators, stats):
        """Add statistical observations section"""
        self.story.append(Paragraph("5️⃣ Statistical Observations", self.heading_style))
        
        observations = []
        
        # Analyze top indicators
        top_positive = [ind for ind in indicators if ind['direction'] == '↑'][0] if indicators else None
        top_negative = [ind for ind in indicators if ind['direction'] == '↓'][0] if indicators else None
        
        if top_positive:
            observations.append(f"• {top_positive['factor'].replace('_', ' ').title()} shows the strongest positive correlation with burnout ({top_positive['correlation']}).")
        
        if top_negative:
            observations.append(f"• {top_negative['factor'].replace('_', ' ').title()} demonstrates negative correlation with burnout ({top_negative['correlation']}), indicating protective effects.")
        
        # Add general observations
        if stats['avg_burnout_score'] > 6:
            observations.append("• The average burnout score indicates moderate to high risk levels across the student population.")
        elif stats['avg_burnout_score'] > 4:
            observations.append("• The average burnout score suggests moderate risk levels requiring attention.")
        else:
            observations.append("• The average burnout score indicates relatively low risk levels overall.")
        
        observations.append("• Statistical analysis reveals significant variations in burnout scores across different student profiles.")
        
        for obs in observations:
            self.story.append(Paragraph(obs, self.normal_style))
        
        self.story.append(Spacer(1, 20))
    
    def add_recommendations(self, indicators, risk_dist):
        """Add recommendations section"""
        self.story.append(Paragraph("6️⃣ Recommendations", self.heading_style))
        
        recommendations = []
        
        # Analyze risk distribution
        high_risk_pct = risk_dist['High Risk']['percentage']
        moderate_risk_pct = risk_dist['Moderate Risk']['percentage']
        
        if high_risk_pct > 30:
            recommendations.append("🔴 **Urgent Intervention Required**: High percentage of students at high risk. Implement comprehensive wellness programs immediately.")
        
        if moderate_risk_pct > 40:
            recommendations.append("🟡 **Preventive Measures Needed**: Significant moderate-risk population. Focus on early intervention strategies.")
        
        # Factor-specific recommendations
        stress_indicator = next((ind for ind in indicators if ind['factor'] == 'stress_level'), None)
        sleep_indicator = next((ind for ind in indicators if ind['factor'] == 'sleep_hours'), None)
        screen_indicator = next((ind for ind in indicators if ind['factor'] == 'screen_time'), None)
        
        if stress_indicator and stress_indicator['correlation'] > 0.5:
            recommendations.append("🧘 **Stress Management**: Implement mindfulness programs, counseling services, and stress reduction workshops.")
        
        if sleep_indicator and sleep_indicator['direction'] == '↓':
            recommendations.append("😴 **Sleep Hygiene**: Promote healthy sleep schedules and create sleep-friendly campus environments.")
        
        if screen_indicator and screen_indicator['correlation'] > 0.4:
            recommendations.append("📱 **Digital Wellness**: Encourage digital detox periods and screen time management.")
        
        # General recommendations
        recommendations.extend([
            "🏃 **Physical Activity**: Promote regular exercise and sports participation.",
            "📚 **Academic Support**: Provide tutoring and study skills workshops.",
            "🤝 **Social Connection**: Foster community building and peer support programs.",
            "📊 **Regular Monitoring**: Implement periodic burnout assessments."
        ])
        
        for rec in recommendations:
            self.story.append(Paragraph(rec, self.normal_style))
        
        self.story.append(Spacer(1, 20))
    
    def add_footer(self):
        """Add report footer"""
        self.story.append(Spacer(1, 30))
        footer_text = "This report was generated using statistical analysis of student burnout data. " \
                     "For questions about this analysis, please contact the academic counseling services."
        self.story.append(Paragraph(footer_text, self.styles['Normal']))
    
    def generate_report(self, stats, risk_dist, indicators, graphs_dir):
        """Generate the complete PDF report"""
        self.add_title()
        self.add_dataset_summary(stats)
        self.add_risk_distribution(risk_dist)
        self.add_indicators(indicators)
        self.add_graphs(graphs_dir)
        self.add_statistical_observations(indicators, stats)
        self.add_recommendations(indicators, risk_dist)
        self.add_footer()
        
        # Build PDF
        self.doc.build(self.story)
        print(f"PDF report generated successfully: {self.output_path}")


def generate_burnout_report_pdf(stats, risk_dist, indicators, graphs_dir, output_path):
    """
    Generate comprehensive burnout analysis PDF report.
    
    Args:
        stats: Summary statistics dictionary
        risk_dist: Risk distribution dictionary
        indicators: List of burnout indicators
        graphs_dir: Directory containing graph images
        output_path: Path to save the PDF report
    """
    # Ensure reports directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Generate report
    report_generator = BurnoutPDFReport(output_path)
    report_generator.generate_report(stats, risk_dist, indicators, graphs_dir)
    
    return output_path


if __name__ == '__main__':
    # Test the PDF generator
    from burnout_analyzer import analyze_burnout_data
    
    data_path = os.path.join('..', 'data', 'student_data.csv')
    results = analyze_burnout_data(data_path)
    
    graphs_dir = os.path.join('..', 'static', 'graphs')
    output_path = os.path.join('..', 'reports', 'burnout_report.pdf')
    
    generate_burnout_report_pdf(
        results['summary_stats'],
        results['risk_distribution'],
        results['indicators'],
        graphs_dir,
        output_path
    )
