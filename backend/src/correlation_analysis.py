import pandas as pd
import numpy as np
from src.data_cleaning import clean_data

def calculate_correlation_matrix(df):
    """Calculate Pearson correlation matrix."""
    correlation = df.corr(method='pearson')
    return correlation

def identify_burnout_indicators(df):
    """Identify strongest burnout indicators."""
    # Create a temporary burnout score for correlation analysis
    # BurnoutScore = 0.35 * stress + 0.25 * screen_time + 0.20 * study_hours - 0.30 * sleep_hours
    df_temp = df.copy()
    df_temp['burnout_indicator'] = (
        0.35 * df['stress_level'] +
        0.25 * df['screen_time'] +
        0.20 * df['study_hours'] -
        0.30 * df['sleep_hours']
    )
    
    # Calculate correlations with burnout indicator
    correlations_with_burnout = {}
    for column in df.columns:
        if column != 'burnout_indicator':
            corr = df_temp[column].corr(df_temp['burnout_indicator'])
            correlations_with_burnout[column] = float(corr)
    
    # Sort by absolute correlation value
    sorted_indicators = sorted(
        correlations_with_burnout.items(),
        key=lambda x: abs(x[1]),
        reverse=True
    )
    
    return dict(sorted_indicators)

def get_correlation_data(filepath):
    """Get correlation matrix and indicators as JSON."""
    df = clean_data(filepath)
    
    correlation_matrix = calculate_correlation_matrix(df)
    indicators = identify_burnout_indicators(df)
    
    return {
        'correlation_matrix': correlation_matrix.to_dict(),
        'burnout_indicators': indicators
    }

if __name__ == "__main__":
    result = get_correlation_data('data/student_data.csv')
    print("Correlation Matrix:")
    for var, corrs in result['correlation_matrix'].items():
        print(f"\n{var}:")
        for other_var, corr_value in corrs.items():
            print(f"  {other_var}: {corr_value:.4f}")
    
    print("\n\nBurnout Indicators (sorted by correlation strength):")
    for indicator, value in result['burnout_indicators'].items():
        print(f"  {indicator}: {value:.4f}")
