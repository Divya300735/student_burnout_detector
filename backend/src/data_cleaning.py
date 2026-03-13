import pandas as pd
import numpy as np

def load_data(filepath):
    """Load dataset from CSV file."""
    df = pd.read_csv(filepath)
    return df

def remove_missing_values(df):
    """Remove rows with missing values."""
    df_cleaned = df.dropna()
    return df_cleaned

def check_valid_ranges(df):
    """Check and validate data ranges."""
    # Define valid ranges for each variable
    valid_ranges = {
        'sleep_hours': (0, 12),
        'study_hours': (0, 12),
        'screen_time': (0, 14),
        'stress_level': (0, 10),
        'physical_activity': (0, 10),
        'assignment_load': (0, 10)
    }
    
    # Filter data within valid ranges
    for column, (min_val, max_val) in valid_ranges.items():
        if column in df.columns:
            df = df[(df[column] >= min_val) & (df[column] <= max_val)]
    
    return df

def remove_outliers(df):
    """Remove outliers using IQR method."""
    Q1 = df.quantile(0.25)
    Q3 = df.quantile(0.75)
    IQR = Q3 - Q1
    
    # Define bounds
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    
    # Filter data
    df_cleaned = df[~((df < lower_bound) | (df > upper_bound)).any(axis=1)]
    
    return df_cleaned

def clean_data(filepath):
    """Complete data cleaning pipeline."""
    df = load_data(filepath)
    print(f"Original data shape: {df.shape}")
    
    df = remove_missing_values(df)
    print(f"After removing missing values: {df.shape}")
    
    df = check_valid_ranges(df)
    print(f"After checking valid ranges: {df.shape}")
    
    df = remove_outliers(df)
    print(f"After removing outliers: {df.shape}")
    
    return df

if __name__ == "__main__":
    cleaned_df = clean_data('data/student_data.csv')
    print("\nCleaned dataset:")
    print(cleaned_df.head())
    print(f"\nFinal shape: {cleaned_df.shape}")
