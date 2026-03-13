#!/usr/bin/env python3
"""
Student Report Downloader

This module handles downloading individual student reports.
"""

import os
from flask import send_file
from datetime import datetime
import glob


def get_student_report_file(student_id):
    """
    Find the latest report file for a given student ID.
    
    Args:
        student_id: Student identifier
        
    Returns:
        Path to the latest report file, or None if not found
    """
    reports_dir = 'reports'
    
    # Search for report files with this student ID
    pattern = os.path.join(reports_dir, f'student_report_{student_id}_*.txt')
    report_files = glob.glob(pattern)
    
    if not report_files:
        return None
    
    # Return the most recent file (sorted by modification time)
    latest_file = max(report_files, key=os.path.getmtime)
    return latest_file


def list_all_student_reports():
    """
    List all available student reports.
    
    Returns:
        List of dictionaries with report information
    """
    reports_dir = 'reports'
    
    if not os.path.exists(reports_dir):
        return []
    
    # Find all student report files
    pattern = os.path.join(reports_dir, 'student_report_*.txt')
    report_files = glob.glob(pattern)
    
    reports = []
    for file_path in report_files:
        try:
            # Extract student ID and timestamp from filename
            filename = os.path.basename(file_path)
            parts = filename.replace('student_report_', '').replace('.txt', '').split('_')
            
            if len(parts) >= 2:
                student_id = '_'.join(parts[:-1])  # Handle IDs with underscores
                timestamp_str = parts[-1]
                
                # Parse timestamp
                try:
                    timestamp = datetime.strptime(timestamp_str, '%Y%m%d_%H%M%S')
                    formatted_time = timestamp.strftime('%B %d, %Y at %I:%M %p')
                except ValueError:
                    formatted_time = 'Unknown'
                
                # Get file size
                file_size = os.path.getsize(file_path)
                
                reports.append({
                    'student_id': student_id,
                    'filename': filename,
                    'file_path': file_path,
                    'timestamp': formatted_time,
                    'file_size': file_size
                })
        except Exception as e:
            print(f"Error processing file {file_path}: {e}")
            continue
    
    # Sort by timestamp (most recent first)
    reports.sort(key=lambda x: x['timestamp'], reverse=True)
    
    return reports


def generate_report_summary(student_id):
    """
    Generate a summary of a student's latest report.
    
    Args:
        student_id: Student identifier
        
    Returns:
        Dictionary with report summary or None if not found
    """
    report_file = get_student_report_file(student_id)
    
    if not report_file:
        return None
    
    try:
        with open(report_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract key information from the report
        lines = content.split('\n')
        burnout_score = 'Unknown'
        risk_level = 'Unknown'
        
        for line in lines:
            if 'Burnout Score:' in line:
                burnout_score = line.split(':')[-1].strip()
            elif 'Risk Level:' in line:
                risk_level = line.split(':')[-1].strip()
        
        return {
            'student_id': student_id,
            'burnout_score': burnout_score,
            'risk_level': risk_level,
            'report_file': report_file,
            'file_size': os.path.getsize(report_file)
        }
        
    except Exception as e:
        print(f"Error reading report {report_file}: {e}")
        return None


if __name__ == '__main__':
    # Test the functions
    print("Testing Report Downloader...")
    print("=" * 40)
    
    # List all reports
    reports = list_all_student_reports()
    print(f"Found {len(reports)} student reports:")
    
    for report in reports[:5]:  # Show first 5
        print(f"  - {report['student_id']}: {report['timestamp']} ({report['file_size']} bytes)")
    
    # Test getting specific report
    if reports:
        summary = generate_report_summary(reports[0]['student_id'])
        if summary:
            print(f"\nLatest report summary:")
            print(f"  Student ID: {summary['student_id']}")
            print(f"  Burnout Score: {summary['burnout_score']}")
            print(f"  Risk Level: {summary['risk_level']}")
            print(f"  File: {summary['report_file']}")
