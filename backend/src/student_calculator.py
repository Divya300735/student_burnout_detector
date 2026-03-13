#!/usr/bin/env python3
"""
Student Burnout Calculator and Data Saver

This module calculates burnout scores for individual students
and saves the results to a CSV file for tracking purposes.
"""

import pandas as pd
import numpy as np
from datetime import datetime
import os


def calculate_student_burnout(sleep_hours, study_hours, screen_time, 
                              stress_level, physical_activity, assignment_load):
    """
    Calculate burnout score for a single student using the weighted formula.
    
    Args:
        sleep_hours: Daily sleep hours (1-10 scale)
        study_hours: Daily study hours (1-10 scale) 
        screen_time: Daily screen time hours (1-10 scale)
        stress_level: Stress level (1-10 scale)
        physical_activity: Physical activity hours per day (1-10 scale)
        assignment_load: Assignment load (1-10 scale)
        
    Returns:
        Dictionary with burnout analysis results
    """
    # Calculate raw burnout score using weighted formula
    burnout_score_raw = (
        0.25 * stress_level +
        0.20 * screen_time +
        0.20 * study_hours +
        0.15 * assignment_load -
        0.10 * sleep_hours -
        0.10 * physical_activity
    )
    
    # Normalize to 0-10 scale (using typical ranges)
    # Assuming typical raw score range of -2 to +8
    min_score, max_score = -2, 8
    if burnout_score_raw <= min_score:
        normalized_score = 0
    elif burnout_score_raw >= max_score:
        normalized_score = 10
    else:
        normalized_score = ((burnout_score_raw - min_score) / (max_score - min_score)) * 10
    
    # Round to 2 decimal places
    burnout_score = round(normalized_score, 2)
    
    # Determine risk level
    if burnout_score <= 4:
        risk_level = 'Low Risk'
    elif burnout_score <= 7:
        risk_level = 'Moderate Risk'
    else:
        risk_level = 'High Risk'
    
    return {
        'burnout_score': burnout_score,
        'risk_level': risk_level,
        'raw_score': round(burnout_score_raw, 3)
    }


def save_student_data(student_data, data_file='data/student_results.csv'):
    """
    Save student burnout data to CSV file.
    
    Args:
        student_data: Dictionary with student information and results
        data_file: Path to save the CSV file
    """
    # Ensure data directory exists
    os.makedirs(os.path.dirname(data_file), exist_ok=True)
    
    # Prepare data row
    row_data = {
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'student_id': student_data.get('student_id', 'Unknown'),
        'sleep_hours': student_data['sleep_hours'],
        'study_hours': student_data['study_hours'],
        'screen_time': student_data['screen_time'],
        'stress_level': student_data['stress_level'],
        'physical_activity': student_data['physical_activity'],
        'assignment_load': student_data['assignment_load'],
        'burnout_score': student_data['burnout_score'],
        'risk_level': student_data['risk_level']
    }
    
    # Check if file exists
    if os.path.exists(data_file):
        # Append to existing file
        df_existing = pd.read_csv(data_file)
        df_new = pd.DataFrame([row_data])
        df_combined = pd.concat([df_existing, df_new], ignore_index=True)
        df_combined.to_csv(data_file, index=False)
    else:
        # Create new file
        df = pd.DataFrame([row_data])
        df.to_csv(data_file, index=False)
    
    print(f"Student data saved to {data_file}")
    return data_file


def generate_student_report(student_data, output_dir='reports'):
    """
    Generate a detailed report for a single student.
    
    Args:
        student_data: Dictionary with student information and results
        output_dir: Directory to save the report
        
    Returns:
        Path to the generated report file
    """
    os.makedirs(output_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    report_file = os.path.join(output_dir, f'student_report_{student_data.get("student_id", "unknown")}_{timestamp}.txt')
    
    report_content = f"""
{'='*60}
ACADEMIC BURNOUT ANALYSIS REPORT
{'='*60}

Student ID: {student_data.get('student_id', 'Unknown')}
Analysis Date: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}

{'='*60}
INPUT DATA
{'='*60}
Sleep Hours: {student_data['sleep_hours']}/10
Study Hours: {student_data['study_hours']}/10
Screen Time: {student_data['screen_time']}/10
Stress Level: {student_data['stress_level']}/10
Physical Activity: {student_data['physical_activity']}/10
Assignment Load: {student_data['assignment_load']}/10

{'='*60}
RESULTS
{'='*60}
Burnout Score: {student_data['burnout_score']}/10
Risk Level: {student_data['risk_level']}
Raw Calculation Score: {student_data['raw_score']}

{'='*60}
RISK LEVEL EXPLANATION
{'='*60}
"""
    
    if student_data['risk_level'] == 'Low Risk':
        report_content += """
🟢 LOW RISK (0-4)
Your burnout score indicates a healthy lifestyle balance.
Continue maintaining good sleep habits, regular physical activity,
and balanced study schedules.
"""
    elif student_data['risk_level'] == 'Moderate Risk':
        report_content += f"""
🟡 MODERATE RISK (4-7)
Your burnout score suggests some burnout indicators are present.

RECOMMENDATIONS:
• Focus on improving sleep quality and duration
• Incorporate regular physical activity breaks
• Practice stress management techniques
• Consider reducing screen time, especially before bed
• Seek academic support if feeling overwhelmed
"""
    else:
        report_content += f"""
🔴 HIGH RISK (7-10)
Your burnout score indicates significant burnout risk.

IMMEDIATE RECOMMENDATIONS:
• Prioritize getting 7-9 hours of quality sleep
• Schedule regular physical activity (30+ minutes daily)
• Practice stress reduction techniques (meditation, deep breathing)
• Consider speaking with a counselor or academic advisor
• Reduce excessive screen time, especially before bedtime
• Take regular breaks from studying
• Evaluate and potentially reduce assignment load
"""
    
    report_content += f"""

{'='*60}
DETAILED FACTOR ANALYSIS
{'='*60}

Positive Contributors to Burnout:
• Stress Level: {student_data['stress_level']}/10 (Weight: 25%)
• Screen Time: {student_data['screen_time']}/10 (Weight: 20%)
• Study Hours: {student_data['study_hours']}/10 (Weight: 20%)
• Assignment Load: {student_data['assignment_load']}/10 (Weight: 15%)

Protective Factors (Negative Contributors):
• Sleep Hours: {student_data['sleep_hours']}/10 (Weight: -10%)
• Physical Activity: {student_data['physical_activity']}/10 (Weight: -10%)

{'='*60}
CALCULATION FORMULA
{'='*60}
Burnout Score = (0.25 × Stress) + (0.20 × Screen) + (0.20 × Study) + 
               (0.15 × Assignment) - (0.10 × Sleep) - (0.10 × Activity)

Raw Score: {student_data['raw_score']}
Normalized Score (0-10): {student_data['burnout_score']}

{'='*60}
Generated by Academic Burnout Detection System
For questions, contact academic counseling services.
{'='*60}
"""
    
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(report_content)
    
    print(f"Student report generated: {report_file}")
    return report_file


def analyze_and_save_student(student_id, sleep_hours, study_hours, screen_time,
                           stress_level, physical_activity, assignment_load):
    """
    Complete pipeline: calculate burnout, save data, and generate report.
    
    Args:
        student_id: Student identifier
        sleep_hours: Daily sleep hours (1-10)
        study_hours: Daily study hours (1-10)
        screen_time: Daily screen time hours (1-10)
        stress_level: Stress level (1-10)
        physical_activity: Physical activity hours per day (1-10)
        assignment_load: Assignment load (1-10)
        
    Returns:
        Dictionary with all results and file paths
    """
    # Calculate burnout
    results = calculate_student_burnout(
        sleep_hours, study_hours, screen_time,
        stress_level, physical_activity, assignment_load
    )
    
    # Prepare student data
    student_data = {
        'student_id': student_id,
        'sleep_hours': sleep_hours,
        'study_hours': study_hours,
        'screen_time': screen_time,
        'stress_level': stress_level,
        'physical_activity': physical_activity,
        'assignment_load': assignment_load,
        **results
    }
    
    # Save data to CSV
    data_file = save_student_data(student_data)
    
    # Generate detailed report
    report_file = generate_student_report(student_data)
    
    return {
        'student_data': student_data,
        'data_file': data_file,
        'report_file': report_file
    }


if __name__ == '__main__':
    # Example usage
    print("Student Burnout Calculator")
    print("=" * 40)
    
    # Test with sample data
    result = analyze_and_save_student(
        student_id="TEST001",
        sleep_hours=6.5,
        study_hours=7.2,
        screen_time=8.1,
        stress_level=6.8,
        physical_activity=3.5,
        assignment_load=7.0
    )
    
    print(f"\nResults for {result['student_data']['student_id']}:")
    print(f"Burnout Score: {result['student_data']['burnout_score']}/10")
    print(f"Risk Level: {result['student_data']['risk_level']}")
    print(f"Data saved to: {result['data_file']}")
    print(f"Report generated: {result['report_file']}")
