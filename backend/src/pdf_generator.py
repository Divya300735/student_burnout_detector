"""
PDF Report Generator for Academic Burnout Detection System.

Generates professional PDF reports using ReportLab with statistics, graphs, and recommendations.
"""

import os
from datetime import datetime
from io import BytesIO

from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, 
    PageBreak, Image, KeepTogether
)
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT

from src.data_cleaning import clean_data
from src.burnout_model import calculate_burnout_score, get_risk_category
from src.correlation_analysis import get_correlation_data


def generate_burnout_report_pdf(filepath='data/student_data.csv', output_path='reports/burnout_report.pdf'):
    """
    Generate a comprehensive PDF report with burnout analysis.
    
    Args:
        filepath: Path to the student data CSV
        output_path: Where to save the PDF report
    
    Returns:
        bytes: PDF content if successful, None otherwise
    """
    try:
        # Ensure output directory exists
        output_dir = os.path.dirname(output_path)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # Load and analyze data
        df = clean_data(filepath)
        
        # Calculate burnout scores and risk levels
        df['burnout_score'] = df.apply(
            lambda row: calculate_burnout_score(
                row['sleep_hours'], row['study_hours'], row['screen_time'],
                row['stress_level'], row['physical_activity'], row['assignment_load']
            ),
            axis=1
        )
        df['risk_level'] = df['burnout_score'].apply(get_risk_category)
        
        # Get statistics
        risk_counts = df['risk_level'].value_counts().to_dict()
        corr_data = get_correlation_data(filepath)
        
        # Create PDF
        doc = SimpleDocTemplate(
            output_path,
            pagesize=letter,
            rightMargin=0.75*inch,
            leftMargin=0.75*inch,
            topMargin=0.75*inch,
            bottomMargin=0.75*inch
        )
        
        # Container for the 'Flowable' objects
        elements = []
        
        # Define styles
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1f4788'),
            spaceAfter=6,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=14,
            textColor=colors.HexColor('#2c5aa0'),
            spaceAfter=12,
            spaceBefore=12,
            fontName='Helvetica-Bold'
        )
        
        # ===== TITLE PAGE =====
        elements.append(Spacer(1, 0.5*inch))
        elements.append(Paragraph("Academic Burnout Risk Analysis Report", title_style))
        elements.append(Spacer(1, 0.2*inch))
        
        subtitle = ParagraphStyle(
            'Subtitle',
            parent=styles['Normal'],
            fontSize=12,
            alignment=TA_CENTER,
            textColor=colors.HexColor('#555555')
        )
        elements.append(Paragraph(
            f"Generated on {datetime.now().strftime('%B %d, %Y at %H:%M:%S')}", 
            subtitle
        ))
        elements.append(Spacer(1, 0.1*inch))
        elements.append(Paragraph(
            f"Total Students Analyzed: {len(df)}", 
            subtitle
        ))
        elements.append(Spacer(1, 0.5*inch))
        
        # ===== SECTION 1: DATASET SUMMARY =====
        elements.append(Paragraph("1. Dataset Summary", heading_style))
        
        summary_data = [
            ['Metric', 'Value'],
            ['Total Students Analyzed', str(len(df))],
            ['Average Sleep Hours', f"{df['sleep_hours'].mean():.2f}"],
            ['Average Study Hours', f"{df['study_hours'].mean():.2f}"],
            ['Average Screen Time (hours)', f"{df['screen_time'].mean():.2f}"],
            ['Average Stress Level (0-10)', f"{df['stress_level'].mean():.2f}"],
            ['Average Physical Activity (0-10)', f"{df['physical_activity'].mean():.2f}"],
            ['Average Assignment Load (0-10)', f"{df['assignment_load'].mean():.2f}"],
        ]
        
        summary_table = Table(summary_data, colWidths=[3*inch, 2.5*inch])
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2c5aa0')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f0f0f0')]),
        ]))
        elements.append(summary_table)
        elements.append(Spacer(1, 0.3*inch))
        
        # ===== SECTION 2: RISK DISTRIBUTION =====
        elements.append(Paragraph("2. Risk Level Distribution", heading_style))
        
        low_risk = risk_counts.get('Low Risk', 0)
        mod_risk = risk_counts.get('Moderate Risk', 0)
        high_risk = risk_counts.get('High Risk', 0)
        total = len(df)
        
        risk_data = [
            ['Risk Level', 'Student Count', 'Percentage'],
            ['Low Risk (0-4)', str(low_risk), f"{(low_risk/total*100):.1f}%"],
            ['Moderate Risk (4-7)', str(mod_risk), f"{(mod_risk/total*100):.1f}%"],
            ['High Risk (7-10)', str(high_risk), f"{(high_risk/total*100):.1f}%"],
            ['Total', str(total), '100.0%'],
        ]
        
        risk_table = Table(risk_data, colWidths=[2.5*inch, 2*inch, 2*inch])
        risk_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2c5aa0')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#ffcccc')),
            ('ROWBACKGROUNDS', (0, 1), (-1, -2), [colors.white, colors.HexColor('#f0f0f0')]),
        ]))
        elements.append(risk_table)
        elements.append(Spacer(1, 0.3*inch))
        
        # ===== SECTION 3: STRONGEST BURNOUT INDICATORS =====
        elements.append(Paragraph("3. Strongest Burnout Indicators", heading_style))
        
        indicators = corr_data.get('burnout_indicators', {})
        sorted_indicators = sorted(
            indicators.items(), 
            key=lambda x: abs(x[1]), 
            reverse=True
        )
        
        indicator_text = "The following factors have the strongest correlation with burnout risk, ranked by impact strength:\n\n"
        
        for i, (factor, corr_value) in enumerate(sorted_indicators, 1):
            direction = "↑ increases" if corr_value > 0 else "↓ decreases"
            factor_name = factor.replace('_', ' ').title()
            indicator_text += f"{i}. <b>{factor_name}</b>: {corr_value:+.2f} {direction} burnout\n"
        
        elements.append(Paragraph(indicator_text, styles['Normal']))
        elements.append(Spacer(1, 0.3*inch))
        
        # ===== SECTION 4: RISK CATEGORY EXPLANATIONS =====
        elements.append(Paragraph("4. Risk Category Explanations", heading_style))
        
        risk_explanations = [
            ("Low Risk (0–4)", "Healthy lifestyle balance maintained", 
             "Students in this category maintain excellent work-life balance with adequate sleep, "
             "moderate stress levels, and regular physical activity."),
            ("Moderate Risk (4–7)", "Some burnout indicators present", 
             "Students showing early signs of burnout with moderate stress levels and lifestyle imbalances. "
             "Intervention recommended."),
            ("High Risk (7–10)", "Significant burnout risk detected", 
             "Students at critical risk requiring immediate intervention with severe lifestyle imbalances "
             "and high stress levels."),
        ]
        
        for risk_cat, title, desc in risk_explanations:
            p = Paragraph(f"<b>{title}</b> - {risk_cat}", styles['Normal'])
            elements.append(p)
            elements.append(Paragraph(desc, styles['Normal']))
            elements.append(Spacer(1, 0.15*inch))
        
        elements.append(Spacer(1, 0.2*inch))
        
        # ===== SECTION 5: GRAPHS =====
        elements.append(PageBreak())
        elements.append(Paragraph("5. Statistical Visualizations", heading_style))
        
        graph_files = [
            ('static/graphs/risk_analysis/risk_pie_chart.png', 'Risk Distribution - Pie Chart'),
            ('static/graphs/risk_analysis/risk_bar_chart.png', 'Risk Distribution - Bar Chart'),
            ('static/graphs/risk_analysis/burnout_histogram.png', 'Burnout Score Distribution'),
        ]
        
        for graph_file, graph_title in graph_files:
            if os.path.exists(graph_file):
                try:
                    img = Image(graph_file, width=5.5*inch, height=3.5*inch)
                    elements.append(Paragraph(f"<i>{graph_title}</i>", styles['Normal']))
                    elements.append(img)
                    elements.append(Spacer(1, 0.25*inch))
                except Exception as e:
                    elements.append(Paragraph(f"[Graph: {graph_title} - Image load failed]", styles['Normal']))
                    elements.append(Spacer(1, 0.25*inch))
        
        # ===== SECTION 6: STATISTICAL OBSERVATIONS =====
        elements.append(PageBreak())
        elements.append(Paragraph("6. Statistical Observations", heading_style))
        
        observations = generate_observations(df, indicators)
        elements.append(Paragraph(observations, styles['Normal']))
        elements.append(Spacer(1, 0.3*inch))
        
        # ===== SECTION 7: RECOMMENDATIONS =====
        elements.append(Paragraph("7. Recommendations for Intervention", heading_style))
        
        recommendations_text = generate_recommendations(df)
        elements.append(Paragraph(recommendations_text, styles['Normal']))
        
        # Build PDF
        doc.build(elements)
        
        print(f"✓ PDF report generated: {output_path}")
        return output_path
        
    except Exception as e:
        print(f"✗ Error generating PDF report: {e}")
        return None


def generate_observations(df, indicators):
    """Generate statistical observations text."""
    obs = []
    
    # Stress observation
    if 'stress_level' in indicators:
        stress_corr = indicators['stress_level']
        obs.append(f"<b>Stress Impact:</b> Stress level shows a correlation of {stress_corr:+.2f} with burnout, "
                   "indicating that higher stress strongly correlates with increased burnout risk.")
    
    # Sleep observation
    if 'sleep_hours' in indicators:
        sleep_corr = indicators['sleep_hours']
        obs.append(f"<b>Sleep Protection:</b> Sleep hours show a correlation of {sleep_corr:+.2f}, "
                   "indicating that adequate sleep is protective against burnout.")
    
    # Screen time observation
    if 'screen_time' in indicators:
        screen_corr = indicators['screen_time']
        obs.append(f"<b>Screen Time Impact:</b> Screen time correlation of {screen_corr:+.2f} suggests that "
                   "excessive digital exposure increases burnout risk.")
    
    # Physical activity observation
    if 'physical_activity' in indicators:
        phys_corr = indicators['physical_activity']
        obs.append(f"<b>Physical Activity Benefits:</b> Physical activity shows a correlation of {phys_corr:+.2f}, "
                   "demonstrating its protective effect against burnout.")
    
    # Average burnout observation
    avg_burnout = df['burnout_score'].mean()
    med_burnout = df['burnout_score'].median()
    obs.append(f"<b>Average Burnout Level:</b> The mean burnout score is {avg_burnout:.2f}/10 with a median of "
               f"{med_burnout:.2f}, indicating {'moderate' if 4 <= avg_burnout < 7 else 'low' if avg_burnout < 4 else 'high'} "
               "burnout levels across the student population.")
    
    return "<br/><br/>".join(obs)


def generate_recommendations(df):
    """Generate personalized recommendations based on data."""
    recs = []
    
    # Sleep recommendation
    low_sleep = df[df['sleep_hours'] < 6]
    if len(low_sleep) / len(df) > 0.2:
        pct = len(low_sleep) / len(df) * 100
        recs.append(f"<b>1. Promote Adequate Sleep:</b> {pct:.0f}% of students sleep less than 6 hours. "
                   "Encourage a consistent sleep schedule of 7-8 hours nightly.")
    
    # Screen time recommendation
    high_screen = df[df['screen_time'] > 8]
    if len(high_screen) / len(df) > 0.2:
        pct = len(high_screen) / len(df) * 100
        recs.append(f"<b>2. Reduce Screen Time:</b> {pct:.0f}% of students exceed 8 hours of daily screen time. "
                   "Implement digital wellness programs and encourage screen-free breaks.")
    
    # Stress management recommendation
    high_stress = df[df['stress_level'] > 7]
    if len(high_stress) / len(df) > 0.15:
        recs.append("<b>3. Implement Stress Management Programs:</b> Provide access to counseling services, "
                   "meditation workshops, and stress-relief activities.")
    
    # Physical activity recommendation
    low_activity = df[df['physical_activity'] < 3]
    if len(low_activity) / len(df) > 0.25:
        recs.append("<b>4. Encourage Physical Activity:</b> Promote regular exercise through campus fitness programs, "
                   "clubs, and wellness initiatives.")
    
    # Study load recommendation
    high_study = df[df['study_hours'] > 8]
    if len(high_study) / len(df) > 0.2:
        recs.append("<b>5. Balance Academic Load:</b> Review course loads and assignment deadlines to prevent "
                   "excessive daily study requirements.")
    
    # Default recommendations
    if not recs:
        recs = [
            "<b>1. Encourage Proper Sleep Schedules:</b> Maintain consistent sleep-wake cycles with 7-8 hours nightly.",
            "<b>2. Promote Physical Activity:</b> Implement regular exercise and wellness programs.",
            "<b>3. Reduce Excessive Screen Time:</b> Set healthy digital usage limits.",
            "<b>4. Stress Management Services:</b> Provide counseling and mental health support.",
            "<b>5. Monitor Student Wellbeing:</b> Conduct regular burnout assessments.",
        ]
    
    return "<br/><br/>".join(recs)
