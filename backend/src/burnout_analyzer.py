#!/usr/bin/env python3
"""
Burnout Score Calculator and Risk Level Classifier

This module implements the statistical weighted formula for burnout calculation
and risk level classification as specified in the requirements.
"""

import pandas as pd
import numpy as np
from pathlib import Path
import os


def calculate_burnout_score(df):
    """
    Calculate burnout score using the weighted formula:
    
    burnout_score = (
        0.25 * stress_level +
        0.20 * screen_time +
        0.20 * study_hours +
        0.15 * assignment_load -
        0.10 * sleep_hours -
        0.10 * physical_activity
    )
    
    Normalized to scale 0-10.
    
    Args:
        df: DataFrame containing the required columns
        
    Returns:
        DataFrame with burnout_score column added
    """
    # Make a copy to avoid modifying original
    df = df.copy()
    
    # Calculate raw burnout score using weighted formula
    df['burnout_score_raw'] = (
        0.25 * df['stress_level'] +
        0.20 * df['screen_time'] +
        0.20 * df['study_hours'] +
        0.15 * df['assignment_load'] -
        0.10 * df['sleep_hours'] -
        0.10 * df['physical_activity']
    )
    
    # Normalize to 0-10 scale
    min_score = df['burnout_score_raw'].min()
    max_score = df['burnout_score_raw'].max()
    
    if max_score != min_score:
        df['burnout_score'] = ((df['burnout_score_raw'] - min_score) / (max_score - min_score)) * 10
    else:
        df['burnout_score'] = 5.0  # Default to middle if all scores are same
    
    # Round to 2 decimal places
    df['burnout_score'] = df['burnout_score'].round(2)
    
    return df


def classify_risk_level(df):
    """
    Classify students into risk categories:
    
    0-4 → Low Risk
    4-7 → Moderate Risk  
    7-10 → High Risk
    
    Args:
        df: DataFrame containing burnout_score column
        
    Returns:
        DataFrame with risk_level column added
    """
    df = df.copy()
    
    # Define risk classification function
    def get_risk_level(score):
        if score <= 4:
            return 'Low Risk'
        elif score <= 7:
            return 'Moderate Risk'
        else:
            return 'High Risk'
    
    # Apply risk classification
    df['risk_level'] = df['burnout_score'].apply(get_risk_level)
    
    return df


def get_risk_distribution(df):
    """
    Get distribution of students across risk levels.
    
    Args:
        df: DataFrame with risk_level column
        
    Returns:
        Dictionary with risk distribution counts and percentages
    """
    risk_counts = df['risk_level'].value_counts()
    total_students = len(df)
    
    distribution = {
        'Low Risk': {
            'count': risk_counts.get('Low Risk', 0),
            'percentage': round((risk_counts.get('Low Risk', 0) / total_students) * 100, 1)
        },
        'Moderate Risk': {
            'count': risk_counts.get('Moderate Risk', 0),
            'percentage': round((risk_counts.get('Moderate Risk', 0) / total_students) * 100, 1)
        },
        'High Risk': {
            'count': risk_counts.get('High Risk', 0),
            'percentage': round((risk_counts.get('High Risk', 0) / total_students) * 100, 1)
        },
        'total_students': total_students
    }
    
    return distribution


def get_burnout_indicators_correlation(df):
    """
    Compute correlation between burnout_score and all factors.
    
    Args:
        df: DataFrame with burnout_score and factor columns
        
    Returns:
        Sorted list of indicators by correlation strength
    """
    # Columns to correlate with burnout_score
    factor_columns = [
        'sleep_hours', 'study_hours', 'stress_level', 
        'screen_time', 'assignment_load', 'physical_activity'
    ]
    
    # Calculate correlations
    correlations = []
    for factor in factor_columns:
        corr = df['burnout_score'].corr(df[factor])
        correlations.append({
            'factor': factor,
            'correlation': round(corr, 3),
            'direction': '↑' if corr > 0 else '↓'
        })
    
    # Sort by absolute correlation value (descending)
    correlations.sort(key=lambda x: abs(x['correlation']), reverse=True)
    
    return correlations


def analyze_burnout_data(data_path):
    """
    Complete burnout analysis pipeline.
    
    Args:
        data_path: Path to the CSV data file
        
    Returns:
        Dictionary with all analysis results
    """
    # Load data
    df = pd.read_csv(data_path)
    
    # Calculate burnout scores
    df = calculate_burnout_score(df)
    
    # Classify risk levels
    df = classify_risk_level(df)
    
    # Get risk distribution
    risk_distribution = get_risk_distribution(df)
    
    # Get correlation indicators
    indicators = get_burnout_indicators_correlation(df)
    
    # Get summary statistics
    summary_stats = {
        'total_students': len(df),
        'avg_burnout_score': round(df['burnout_score'].mean(), 2),
        'min_burnout_score': round(df['burnout_score'].min(), 2),
        'max_burnout_score': round(df['burnout_score'].max(), 2),
        'std_burnout_score': round(df['burnout_score'].std(), 2)
    }
    
    return {
        'dataframe': df,
        'risk_distribution': risk_distribution,
        'indicators': indicators,
        'summary_stats': summary_stats
    }


if __name__ == '__main__':
    # Test the analysis
    data_path = os.path.join('..', 'data', 'student_data.csv')
    results = analyze_burnout_data(data_path)
    
    print("Burnout Analysis Results:")
    print(f"Total Students: {results['summary_stats']['total_students']}")
    print(f"Average Burnout Score: {results['summary_stats']['avg_burnout_score']}")
    print("\nRisk Distribution:")
    for level, data in results['risk_distribution'].items():
        if isinstance(data, dict):
            print(f"  {level}: {data['count']} students ({data['percentage']}%)")
    
    print("\nTop Burnout Indicators:")
    for i, indicator in enumerate(results['indicators'][:3], 1):
        print(f"  {i}. {indicator['factor']} {indicator['correlation']} {indicator['direction']}")
