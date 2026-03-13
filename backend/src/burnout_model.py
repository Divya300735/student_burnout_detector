import pandas as pd
import numpy as np
from src.data_cleaning import clean_data
from scipy.stats import norm

def calculate_burnout_score(sleep_hours, study_hours, screen_time, stress_level, 
                           physical_activity=5, assignment_load=5):
    """
    Calculate burnout score using statistical weighted formula:
    
    burnout_score = (
        0.25 * stress_level +
        0.20 * screen_time +
        0.20 * study_hours +
        0.15 * assignment_load -
        0.10 * sleep_hours -
        0.10 * physical_activity
    )
    
    Normalize to 0-10 scale.
    """
    # Apply weighted formula as per specification
    burnout_raw = (
        0.25 * stress_level +
        0.20 * screen_time +
        0.20 * study_hours +
        0.15 * assignment_load -
        0.10 * sleep_hours -
        0.10 * physical_activity
    )
    
    # Normalize to 0-10 scale using min-max normalization
    # Raw score can range from approximately -1.2 to 8.8, normalize to 0-10
    min_raw = -1.2
    max_raw = 8.8
    
    if max_raw > min_raw:
        burnout_score = 10 * (burnout_raw - min_raw) / (max_raw - min_raw)
    else:
        burnout_score = 5
    
    # Clamp to 0-10 range
    burnout_score = max(0, min(10, burnout_score))
    
    return burnout_score

def get_risk_category(burnout_score):
    """Determine risk category based on burnout score."""
    if burnout_score < 4:
        return "Low Risk"
    elif burnout_score < 7:
        return "Moderate Risk"
    else:
        return "High Risk"

def calculate_burnout_probability(burnout_score):
    """
    Calculate probability of actual burnout using normal distribution.
    Uses statistics from the dataset to estimate probability.
    """
    # Assuming burnout follows normal distribution with mean 5 and std dev 2
    mean = 5
    std_dev = 2
    
    # Probability of burnout = P(X >= burnout_score)
    probability = 1 - norm.cdf(burnout_score, loc=mean, scale=std_dev)
    
    return float(probability)

def get_recommendations(sleep_hours, study_hours, screen_time, stress_level, 
                       physical_activity, assignment_load, burnout_score):
    """Generate personalized recommendations based on student data."""
    recommendations = []
    
    # Sleep recommendations
    if sleep_hours < 6:
        recommendations.append({
            'category': 'Sleep',
            'message': f'Increase sleep to at least 7-8 hours. Currently getting {sleep_hours:.1f} hours.',
            'impact': 'Improving sleep quality is crucial for burnout prevention.'
        })
    
    # Screen time recommendations
    if screen_time > 8:
        recommendations.append({
            'category': 'Screen Time',
            'message': f'Reduce screen time below 8 hours. Currently {screen_time:.1f} hours daily.',
            'impact': 'Excessive screen time increases stress and fatigue.'
        })
    
    # Stress management
    if stress_level > 6:
        recommendations.append({
            'category': 'Stress Management',
            'message': f'Your stress level is {stress_level:.1f}/10. Practice relaxation techniques.',
            'impact': 'Implement meditation, breathing exercises, or counseling services.'
        })
    
    # Study load
    if study_hours > 6:
        recommendations.append({
            'category': 'Study Load',
            'message': f'Current study hours: {study_hours:.1f}. Consider spreading work over more days.',
            'impact': 'Balanced study schedule improves retention and reduces exhaustion.'
        })
    
    # Physical activity
    if physical_activity < 3:
        recommendations.append({
            'category': 'Physical Activity',
            'message': f'Increase physical activity. Current level: {physical_activity:.1f}/10.',
            'impact': 'Regular exercise reduces stress and improves overall wellbeing.'
        })
    
    # Assignment load
    if assignment_load > 7:
        recommendations.append({
            'category': 'Assignment Management',
            'message': f'Assignment load is high ({assignment_load:.1f}/10). Prioritize tasks effectively.',
            'impact': 'Better time management and task prioritization reduce overwhelm.'
        })
    
    # If low risk, provide maintenance tips
    if burnout_score < 4:
        recommendations.append({
            'category': 'Wellbeing',
            'message': 'You are maintaining good wellbeing habits!',
            'impact': 'Continue your current practices and maintain this healthy balance.'
        })
    
    return recommendations

def analyze_student_burnout(sleep_hours, study_hours, screen_time, stress_level, 
                           physical_activity=5, assignment_load=5):
    """Complete burnout analysis for a student."""
    burnout_score = calculate_burnout_score(
        sleep_hours, study_hours, screen_time, stress_level, 
        physical_activity, assignment_load
    )
    
    risk_category = get_risk_category(burnout_score)
    probability = calculate_burnout_probability(burnout_score)
    recommendations = get_recommendations(
        sleep_hours, study_hours, screen_time, stress_level,
        physical_activity, assignment_load, burnout_score
    )
    
    return {
        'burnout_score': round(burnout_score, 2),
        'risk_category': risk_category,
        'burnout_probability': round(probability * 100, 2),
        'recommendations': recommendations
    }

if __name__ == "__main__":
    # Test example
    result = analyze_student_burnout(
        sleep_hours=5.5,
        study_hours=7.5,
        screen_time=9.0,
        stress_level=7.5,
        physical_activity=2,
        assignment_load=8
    )
    print("Burnout Analysis:")
    print(f"Score: {result['burnout_score']}/10")
    print(f"Risk Category: {result['risk_category']}")
    print(f"Burnout Probability: {result['burnout_probability']}%")
    print("\nRecommendations:")
    for rec in result['recommendations']:
        print(f"  - {rec['message']}")
