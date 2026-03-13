import pandas as pd
import numpy as np
from src.data_cleaning import clean_data

def calculate_regression_coefficients(df):
    """
    Calculate linear regression coefficients using mathematical formulas.
    Model: Burnout = a + b1*sleep + b2*study + b3*screen + b4*stress
    Using the normal equation method.
    """
    # Create burnout target variable
    # BurnoutScore = 0.35 * stress + 0.25 * screen_time + 0.20 * study_hours - 0.30 * sleep_hours
    burnout = (
        0.35 * df['stress_level'] +
        0.25 * df['screen_time'] +
        0.20 * df['study_hours'] -
        0.30 * df['sleep_hours']
    )
    
    # Normalize burnout to 0-10 scale
    min_burnout = burnout.min()
    max_burnout = burnout.max()
    if max_burnout > min_burnout:
        burnout = 10 * (burnout - min_burnout) / (max_burnout - min_burnout)
    else:
        burnout = 5  # Default middle value if all same
    
    # Prepare feature variables
    X = df[['sleep_hours', 'study_hours', 'screen_time', 'stress_level']].values
    y = burnout.values
    
    # Add column of ones for intercept
    X_with_intercept = np.column_stack([np.ones(len(X)), X])
    
    # Calculate coefficients using normal equation: β = (X^T X)^-1 X^T y
    try:
        coefficients = np.linalg.lstsq(X_with_intercept, y, rcond=None)[0]
    except np.linalg.LinAlgError:
        # Fallback if matrix is singular
        coefficients = np.zeros(5)
    
    # Extract results
    intercept = coefficients[0]
    coeff_sleep = coefficients[1]
    coeff_study = coefficients[2]
    coeff_screen = coefficients[3]
    coeff_stress = coefficients[4]
    
    # Calculate R-squared
    y_pred = X_with_intercept @ coefficients
    ss_res = np.sum((y - y_pred) ** 2)
    ss_tot = np.sum((y - np.mean(y)) ** 2)
    r_squared = 1 - (ss_res / ss_tot) if ss_tot != 0 else 0
    
    return {
        'intercept': float(intercept),
        'sleep_hours_coeff': float(coeff_sleep),
        'study_hours_coeff': float(coeff_study),
        'screen_time_coeff': float(coeff_screen),
        'stress_level_coeff': float(coeff_stress),
        'r_squared': float(r_squared),
        'equation': f"Burnout = {intercept:.4f} + ({coeff_sleep:.4f})*sleep + ({coeff_study:.4f})*study + ({coeff_screen:.4f})*screen + ({coeff_stress:.4f})*stress"
    }

def predict_burnout_regression(sleep, study, screen, stress):
    """Predict burnout using regression coefficients."""
    df = clean_data('data/student_data.csv')
    coeffs = calculate_regression_coefficients(df)
    
    burnout = (
        coeffs['intercept'] +
        coeffs['sleep_hours_coeff'] * sleep +
        coeffs['study_hours_coeff'] * study +
        coeffs['screen_time_coeff'] * screen +
        coeffs['stress_level_coeff'] * stress
    )
    
    # Ensure output is in 0-10 range
    burnout = max(0, min(10, burnout))
    return burnout

def get_regression_data(filepath):
    """Get regression coefficients."""
    df = clean_data(filepath)
    return calculate_regression_coefficients(df)

if __name__ == "__main__":
    coeffs = get_regression_data('data/student_data.csv')
    print("Regression Coefficients:")
    for param, value in coeffs.items():
        print(f"{param}: {value}")
