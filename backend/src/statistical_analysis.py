import pandas as pd
import numpy as np
from src.data_cleaning import clean_data

def calculate_descriptive_statistics(df):
    """Calculate descriptive statistics for all variables."""
    stats = {}
    
    for column in df.columns:
        stats[column] = {
            'mean': float(df[column].mean()),
            'median': float(df[column].median()),
            'variance': float(df[column].var()),
            'std_dev': float(df[column].std()),
            'min': float(df[column].min()),
            'max': float(df[column].max()),
            'count': int(df[column].count())
        }
    
    return stats

def get_statistics_json(filepath):
    """Get statistics as JSON-compatible format."""
    df = clean_data(filepath)
    stats = calculate_descriptive_statistics(df)
    return stats

if __name__ == "__main__":
    stats = get_statistics_json('data/student_data.csv')
    print("Descriptive Statistics:")
    for variable, values in stats.items():
        print(f"\n{variable}:")
        for metric, value in values.items():
            print(f"  {metric}: {value:.4f}" if isinstance(value, float) else f"  {metric}: {value}")
