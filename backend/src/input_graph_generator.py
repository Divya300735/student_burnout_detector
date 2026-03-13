"""
Input-based graph generator for visualizing user lifestyle data.
Creates dynamic visualizations based on user input from the burnout calculator.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import Polygon
import os
from datetime import datetime

# Set style for all plots
plt.rcParams['figure.figsize'] = (12, 7)
plt.rcParams['figure.dpi'] = 100

def create_user_graphs_directory():
    """Ensure user graphs directory exists."""
    if not os.path.exists('static/graphs/user_input_graphs'):
        os.makedirs('static/graphs/user_input_graphs')

def generate_lifestyle_bar_chart(sleep_hours, study_hours, screen_time, stress_level, 
                                 physical_activity, assignment_load):
    """Generate 1. Lifestyle Bar Chart showing all input values."""
    create_user_graphs_directory()
    
    categories = ['Sleep\nHours', 'Study\nHours', 'Screen\nTime', 'Stress\nLevel', 
                  'Physical\nActivity', 'Assignment\nLoad']
    values = [sleep_hours, study_hours, screen_time, stress_level, physical_activity, assignment_load]
    
    # Normalize values to 0-10 scale for comparison
    max_values = [12, 12, 14, 10, 10, 10]
    normalized = [v / m * 10 for v, m in zip(values, max_values)]
    
    # Define colors
    colors = ['#3498db', '#2ecc71', '#9b59b6', '#e74c3c', '#f39c12', '#1abc9c']
    
    plt.figure(figsize=(13, 7))
    bars = plt.bar(categories, normalized, color=colors, edgecolor='black', linewidth=1.5, alpha=0.85)
    
    # Add value labels on bars
    for i, (bar, actual_value, max_val) in enumerate(zip(bars, values, max_values)):
        height = bar.get_height()
        label = f'{actual_value:.1f}'
        if i == 3:  # Stress level
            label += '\n(/10)'
        elif i in [4, 5]:  # Physical activity, assignment load
            label += '\n(/10)'
        elif i == 0:  # Sleep
            label += '\n(hrs)'
        elif i in [1, 2]:  # Study, screen
            label += '\n(hrs)'
        
        plt.text(bar.get_x() + bar.get_width()/2, height + 0.2,
                label, ha='center', va='bottom', fontweight='bold', fontsize=10)
    
    plt.ylabel('Normalized Value (0-10 scale)', fontsize=12, fontweight='bold')
    plt.title('Your Lifestyle Factors - Normalized Comparison', fontsize=14, fontweight='bold')
    plt.ylim(0, 12)
    plt.grid(axis='y', alpha=0.3, linestyle='--')
    plt.tight_layout()
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f'user_input_graphs/lifestyle_bar_chart_{timestamp}.png'
    plt.savefig(f'static/graphs/{filename}', bbox_inches='tight')
    plt.close()
    return filename

def generate_radar_chart(sleep_hours, study_hours, screen_time, stress_level, 
                        physical_activity, assignment_load):
    """Generate 2. Radar Chart showing lifestyle balance."""
    create_user_graphs_directory()
    
    # Categories
    categories = ['Sleep', 'Study', 'Screen Time', 'Stress', 'Physical Activity', 'Assignment']
    N = len(categories)
    
    # Normalize all values to 0-10 scale (inverted some for better visualization)
    # Lower stress is better, so invert it
    values = [
        sleep_hours / 12 * 10,           # Sleep: 0-12 hrs -> 0-10
        study_hours / 12 * 10,           # Study: 0-12 hrs -> 0-10
        (14 - screen_time) / 14 * 10,    # Screen: inverted (less is better)
        (10 - stress_level),              # Stress: inverted (less is better)
        physical_activity,                # Activity: already 0-10
        (10 - assignment_load)            # Assignment: inverted (less is better)
    ]
    
    # Ensure values stay in 0-10 range
    values = [max(0, min(10, v)) for v in values]
    values += values[:1]  # Complete the loop
    
    # Calculate angles
    angles = [n / float(N) * 2 * np.pi for n in range(N)]
    angles += angles[:1]
    
    # Create figure
    fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(projection='polar'))
    
    # Plot data
    ax.plot(angles, values, 'o-', linewidth=2.5, color='#3498db', markersize=8)
    ax.fill(angles, values, alpha=0.25, color='#3498db')
    
    # Fix axis to go in the right order
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories, fontsize=11, fontweight='bold')
    ax.set_ylim(0, 10)
    ax.set_yticks([2, 4, 6, 8, 10])
    ax.set_yticklabels(['2', '4', '6', '8', '10'], fontsize=9)
    ax.grid(True, linestyle='--', alpha=0.7)
    
    plt.title('Your Lifestyle Balance - Radar Chart\n(Outer = Better Balance)', 
             fontsize=14, fontweight='bold', pad=20)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f'user_input_graphs/radar_chart_{timestamp}.png'
    plt.savefig(f'static/graphs/{filename}', bbox_inches='tight')
    plt.close()
    return filename

def generate_gauge_chart(burnout_score):
    """Generate 3. Burnout Score Gauge Chart."""
    create_user_graphs_directory()
    
    # Create figure
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Create gauge background
    theta = np.linspace(np.pi, 2*np.pi, 100)
    
    # Three color zones
    low_theta = np.linspace(np.pi, np.pi + np.pi/3, 50)
    moderate_theta = np.linspace(np.pi + np.pi/3, np.pi + 2*np.pi/3, 50)
    high_theta = np.linspace(np.pi + 2*np.pi/3, 2*np.pi, 50)
    
    # Draw gauge sections
    ax.fill_between(low_theta, 0, 1, color='#2ecc71', alpha=0.7)
    ax.fill_between(moderate_theta, 0, 1, color='#f39c12', alpha=0.7)
    ax.fill_between(high_theta, 0, 1, color='#e74c3c', alpha=0.7)
    
    # Add labels to zones
    ax.text(np.pi + np.pi/6, 0.7, 'LOW RISK', ha='center', fontsize=12, fontweight='bold')
    ax.text(np.pi + np.pi/2, 0.7, 'MODERATE RISK', ha='center', fontsize=12, fontweight='bold')
    ax.text(np.pi + 5*np.pi/6, 0.7, 'HIGH RISK', ha='center', fontsize=12, fontweight='bold')
    
    # Draw needle
    normalized_score = burnout_score / 10  # Normalize to 0-1
    needle_angle = np.pi + normalized_score * np.pi  # Map to pi -> 2pi
    
    neck_radius = 0.15
    needle_length = 0.9
    
    ax.arrow(0, 0, neck_radius * np.cos(needle_angle), neck_radius * np.sin(needle_angle),
            head_width=0.1, head_length=0.1, fc='black', ec='black')
    
    ax.plot([0, needle_length * np.cos(needle_angle)], 
           [0, needle_length * np.sin(needle_angle)],
           'k-', linewidth=3)
    
    # Draw center circle
    circle = plt.Circle((0, 0), 0.1, color='black')
    ax.add_patch(circle)
    
    # Add score text
    ax.text(0, -0.5, f'Your Burnout Score: {burnout_score:.1f}/10', 
           ha='center', fontsize=16, fontweight='bold')
    
    # Determine risk message
    if burnout_score < 4:
        risk_msg = "You're in GOOD SHAPE!"
        color = '#2ecc71'
    elif burnout_score < 7:
        risk_msg = "Moderate Risk - Take Action"
        color = '#f39c12'
    else:
        risk_msg = "High Risk - Seek Support"
        color = '#e74c3c'
    
    ax.text(0, -0.65, risk_msg, ha='center', fontsize=13, 
           fontweight='bold', color=color)
    
    # Set axis properties
    ax.set_xlim(-1.2, 1.2)
    ax.set_ylim(-0.8, 1.2)
    ax.set_aspect('equal')
    ax.axis('off')
    
    plt.title('Burnout Score Gauge', fontsize=14, fontweight='bold', pad=20)
    plt.tight_layout()
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f'user_input_graphs/gauge_chart_{timestamp}.png'
    plt.savefig(f'static/graphs/{filename}', bbox_inches='tight')
    plt.close()
    return filename

def generate_all_user_graphs(sleep_hours, study_hours, screen_time, stress_level,
                            physical_activity, assignment_load, burnout_score):
    """Generate all 3 user input graphs."""
    print("\nGenerating User Input Graphs...")
    
    graphs = []
    
    graphs.append(generate_lifestyle_bar_chart(
        sleep_hours, study_hours, screen_time, stress_level, 
        physical_activity, assignment_load
    ))
    print("  ✓ User Graph 1: Lifestyle Bar Chart")
    
    graphs.append(generate_radar_chart(
        sleep_hours, study_hours, screen_time, stress_level,
        physical_activity, assignment_load
    ))
    print("  ✓ User Graph 2: Radar Chart")
    
    graphs.append(generate_gauge_chart(burnout_score))
    print("  ✓ User Graph 3: Gauge Chart")
    
    print("\nUser input graphs generated successfully!\n")
    
    return graphs

if __name__ == "__main__":
    # Test
    graphs = generate_all_user_graphs(
        sleep_hours=6.5,
        study_hours=5.5,
        screen_time=7.0,
        stress_level=5.5,
        physical_activity=4.0,
        assignment_load=5.0,
        burnout_score=5.73
    )
    print("Graphs created:", graphs)
