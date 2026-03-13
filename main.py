#!/usr/bin/env python3
"""Entry point for running analysis and report generation.

This script can be run from the project root using `python main.py`.  It
initializes the backend path and then executes the report generator (and can
be extended later to trigger additional analysis steps).
"""
import os
import sys

# ensure backend folder is on sys.path so we can import modules
root = os.path.dirname(os.path.abspath(__file__))
backend_dir = os.path.join(root, 'backend')
sys.path.insert(0, backend_dir)

from src.report_generator import generate_report


def main():
    print("Starting analysis and report generation...")
    data_path = os.path.join('backend', 'data', 'student_data.csv')
    try:
        report_text = generate_report(filepath=data_path)
        print("Report generation complete. Check 'reports/analysis_report.txt'.")
    except Exception as e:
        print(f"Error during report generation: {e}")


if __name__ == '__main__':
    main()
