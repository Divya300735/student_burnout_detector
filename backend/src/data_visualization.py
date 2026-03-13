"""
Data-driven visualization module for generating graphs from the student dataset.
Generates 10 different statistical visualizations for burnout analysis.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from src.data_cleaning import clean_data
from src.burnout_model import calculate_burnout_score, get_risk_category
import os

# Set style for all plots
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 7)
plt.rcParams['figure.dpi'] = 100

def create_graphs_directory():
    """Ensure graphs directory exists."""
    if not os.path.exists('static/graphs'):
        os.makedirs('static/graphs')

def generate_sleep_distribution(df):
    """Generate 1. Sleep Hours Distribution Histogram."""
    plt.figure(figsize=(11, 6))
    plt.hist(df['sleep_hours'], bins=25, color='#3498db', edgecolor='black', alpha=0.8)
    plt.xlabel('Sleep Hours', fontsize=12, fontweight='bold')
    plt.ylabel('Number of Students', fontsize=12, fontweight='bold')
    plt.title('Distribution of Sleep Hours Among Students', fontsize=14, fontweight='bold')
    plt.grid(axis='y', alpha=0.3, linestyle='--')
    plt.tight_layout()
    plt.savefig('static/graphs/01_sleep_distribution.png', dpi=100, bbox_inches='tight')
    plt.close()
    return "01_sleep_distribution.png"

def generate_stress_distribution(df):
    """Generate 2. Stress Level Distribution Histogram."""
    plt.figure(figsize=(11, 6))
    plt.hist(df['stress_level'], bins=20, color='#e74c3c', edgecolor='black', alpha=0.8)
    plt.xlabel('Stress Level (0-10)', fontsize=12, fontweight='bold')
    plt.ylabel('Number of Students', fontsize=12, fontweight='bold')
    plt.title('Distribution of Stress Levels Among Students', fontsize=14, fontweight='bold')
    plt.grid(axis='y', alpha=0.3, linestyle='--')
    plt.tight_layout()
    plt.savefig('static/graphs/02_stress_distribution.png', dpi=100, bbox_inches='tight')
    plt.close()
    return "02_stress_distribution.png"

def generate_study_hours_boxplot(df):
    """Generate 3. Study Hours Boxplot by Risk Category."""
    df_temp = df.copy()
    df_temp['burnout_score'] = df_temp.apply(
        lambda row: calculate_burnout_score(
            row['sleep_hours'], row['study_hours'], row['screen_time'],
            row['stress_level'], row['physical_activity'], row['assignment_load']
        ), axis=1
    )
    df_temp['risk_category'] = df_temp['burnout_score'].apply(get_risk_category)
    
    plt.figure(figsize=(11, 6))
    # Define risk order and colors
    risk_order = ['Low Risk', 'Moderate Risk', 'High Risk']
    colors = ['#2ecc71', '#f39c12', '#e74c3c']
    
    bp = plt.boxplot([df_temp[df_temp['risk_category'] == cat]['study_hours'].values 
                       for cat in risk_order],
                      labels=risk_order,
                      patch_artist=True,
                      widths=0.6)
    
    for patch, color in zip(bp['boxes'], colors):
        patch.set_facecolor(color)
        patch.set_alpha(0.7)
    
    plt.ylabel('Study Hours per Day', fontsize=12, fontweight='bold')
    plt.xlabel('Risk Category', fontsize=12, fontweight='bold')
    plt.title('Study Hours Distribution by Risk Category', fontsize=14, fontweight='bold')
    plt.grid(axis='y', alpha=0.3, linestyle='--')
    plt.tight_layout()
    plt.savefig('static/graphs/03_study_hours_boxplot.png', dpi=100, bbox_inches='tight')
    plt.close()
    return "03_study_hours_boxplot.png"

def generate_screen_time_distribution(df):
    """Generate 4. Screen Time Distribution Histogram."""
    plt.figure(figsize=(11, 6))
    plt.hist(df['screen_time'], bins=25, color='#9b59b6', edgecolor='black', alpha=0.8)
    plt.xlabel('Screen Time (hours)', fontsize=12, fontweight='bold')
    plt.ylabel('Number of Students', fontsize=12, fontweight='bold')
    plt.title('Distribution of Daily Screen Time', fontsize=14, fontweight='bold')
    plt.grid(axis='y', alpha=0.3, linestyle='--')
    plt.tight_layout()
    plt.savefig('static/graphs/04_screen_time_distribution.png', dpi=100, bbox_inches='tight')
    plt.close()
    return "04_screen_time_distribution.png"

def generate_burnout_distribution(df):
    """Generate 5. Burnout Score Distribution Histogram."""
    df_temp = df.copy()
    df_temp['burnout_score'] = df_temp.apply(
        lambda row: calculate_burnout_score(
            row['sleep_hours'], row['study_hours'], row['screen_time'],
            row['stress_level'], row['physical_activity'], row['assignment_load']
        ), axis=1
    )
    
    plt.figure(figsize=(11, 6))
    counts, bins, patches = plt.hist(df_temp['burnout_score'], bins=25, edgecolor='black', alpha=0.8)
    
    # Color code based on risk level
    for i, patch in enumerate(patches):
        if bins[i] < 4:
            patch.set_facecolor('#2ecc71')
        elif bins[i] < 7:
            patch.set_facecolor('#f39c12')
        else:
            patch.set_facecolor('#e74c3c')
    
    plt.xlabel('Burnout Score (0-10)', fontsize=12, fontweight='bold')
    plt.ylabel('Number of Students', fontsize=12, fontweight='bold')
    plt.title('Distribution of Burnout Scores', fontsize=14, fontweight='bold')
    plt.axvline(4, color='red', linestyle='--', linewidth=2, label='Risk Threshold')
    plt.axvline(7, color='darkred', linestyle='--', linewidth=2, label='High Risk Threshold')
    plt.legend()
    plt.grid(axis='y', alpha=0.3, linestyle='--')
    plt.tight_layout()
    plt.savefig('static/graphs/05_burnout_distribution.png', dpi=100, bbox_inches='tight')
    plt.close()
    return "05_burnout_distribution.png"

def generate_sleep_vs_burnout_scatter(df):
    """Generate 6. Scatter Plot: Sleep vs Burnout Score."""
    df_temp = df.copy()
    df_temp['burnout_score'] = df_temp.apply(
        lambda row: calculate_burnout_score(
            row['sleep_hours'], row['study_hours'], row['screen_time'],
            row['stress_level'], row['physical_activity'], row['assignment_load']
        ), axis=1
    )
    
    plt.figure(figsize=(11, 6))
    plt.scatter(df_temp['sleep_hours'], df_temp['burnout_score'], 
               alpha=0.6, s=80, color='#3498db', edgecolors='black', linewidth=0.5)
    
    # Add trend line
    z = np.polyfit(df_temp['sleep_hours'], df_temp['burnout_score'], 2)
    p = np.poly1d(z)
    x_trend = np.linspace(df_temp['sleep_hours'].min(), df_temp['sleep_hours'].max(), 100)
    plt.plot(x_trend, p(x_trend), "r-", linewidth=2.5, label='Trend Line')
    
    plt.xlabel('Sleep Hours', fontsize=12, fontweight='bold')
    plt.ylabel('Burnout Score', fontsize=12, fontweight='bold')
    plt.title('Sleep Duration vs Burnout Score (Negative Correlation)', fontsize=14, fontweight='bold')
    plt.legend(fontsize=10)
    plt.grid(True, alpha=0.3, linestyle='--')
    plt.tight_layout()
    plt.savefig('static/graphs/06_sleep_vs_burnout.png', dpi=100, bbox_inches='tight')
    plt.close()
    return "06_sleep_vs_burnout.png"

def generate_stress_vs_burnout_scatter(df):
    """Generate 7. Scatter Plot: Stress vs Burnout Score."""
    df_temp = df.copy()
    df_temp['burnout_score'] = df_temp.apply(
        lambda row: calculate_burnout_score(
            row['sleep_hours'], row['study_hours'], row['screen_time'],
            row['stress_level'], row['physical_activity'], row['assignment_load']
        ), axis=1
    )
    
    plt.figure(figsize=(11, 6))
    plt.scatter(df_temp['stress_level'], df_temp['burnout_score'], 
               alpha=0.6, s=80, color='#e74c3c', edgecolors='black', linewidth=0.5)
    
    # Add trend line
    z = np.polyfit(df_temp['stress_level'], df_temp['burnout_score'], 2)
    p = np.poly1d(z)
    x_trend = np.linspace(df_temp['stress_level'].min(), df_temp['stress_level'].max(), 100)
    plt.plot(x_trend, p(x_trend), "b-", linewidth=2.5, label='Trend Line')
    
    plt.xlabel('Stress Level (0-10)', fontsize=12, fontweight='bold')
    plt.ylabel('Burnout Score', fontsize=12, fontweight='bold')
    plt.title('Stress Level vs Burnout Score (Strong Positive Correlation)', fontsize=14, fontweight='bold')
    plt.legend(fontsize=10)
    plt.grid(True, alpha=0.3, linestyle='--')
    plt.tight_layout()
    plt.savefig('static/graphs/07_stress_vs_burnout.png', dpi=100, bbox_inches='tight')
    plt.close()
    return "07_stress_vs_burnout.png"

def generate_screen_time_vs_burnout_scatter(df):
    """Generate 8. Scatter Plot: Screen Time vs Burnout Score."""
    df_temp = df.copy()
    df_temp['burnout_score'] = df_temp.apply(
        lambda row: calculate_burnout_score(
            row['sleep_hours'], row['study_hours'], row['screen_time'],
            row['stress_level'], row['physical_activity'], row['assignment_load']
        ), axis=1
    )
    
    plt.figure(figsize=(11, 6))
    plt.scatter(df_temp['screen_time'], df_temp['burnout_score'], 
               alpha=0.6, s=80, color='#9b59b6', edgecolors='black', linewidth=0.5)
    
    # Add trend line
    z = np.polyfit(df_temp['screen_time'], df_temp['burnout_score'], 2)
    p = np.poly1d(z)
    x_trend = np.linspace(df_temp['screen_time'].min(), df_temp['screen_time'].max(), 100)
    plt.plot(x_trend, p(x_trend), "orange", linewidth=2.5, linestyle='-', label='Trend Line')
    
    plt.xlabel('Screen Time (hours)', fontsize=12, fontweight='bold')
    plt.ylabel('Burnout Score', fontsize=12, fontweight='bold')
    plt.title('Daily Screen Time vs Burnout Score (Positive Correlation)', fontsize=14, fontweight='bold')
    plt.legend(fontsize=10)
    plt.grid(True, alpha=0.3, linestyle='--')
    plt.tight_layout()
    plt.savefig('static/graphs/08_screen_time_vs_burnout.png', dpi=100, bbox_inches='tight')
    plt.close()
    return "08_screen_time_vs_burnout.png"

def generate_correlation_heatmap(df):
    """Generate 9. Correlation Heatmap."""
    plt.figure(figsize=(12, 9))
    correlation = df.corr()
    
    sns.heatmap(correlation, 
               annot=True, 
               fmt='.2f', 
               cmap='RdYlGn', 
               center=0,
               square=True, 
               linewidths=1.5,
               cbar_kws={"shrink": 0.8},
               vmin=-1, vmax=1)
    
    plt.title('Correlation Matrix: Lifestyle Factors and Relationships', fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig('static/graphs/09_correlation_heatmap.png', dpi=100, bbox_inches='tight')
    plt.close()
    return "09_correlation_heatmap.png"

def generate_risk_pie_chart(df):
    """Generate 10. Risk Category Pie Chart."""
    df_temp = df.copy()
    df_temp['burnout_score'] = df_temp.apply(
        lambda row: calculate_burnout_score(
            row['sleep_hours'], row['study_hours'], row['screen_time'],
            row['stress_level'], row['physical_activity'], row['assignment_load']
        ), axis=1
    )
    df_temp['risk_category'] = df_temp['burnout_score'].apply(get_risk_category)
    
    risk_counts = df_temp['risk_category'].value_counts()
    
    # Ensure all categories are present
    risk_order = ['Low Risk', 'Moderate Risk', 'High Risk']
    risk_counts = risk_counts.reindex(risk_order, fill_value=0)
    
    plt.figure(figsize=(10, 8))
    colors = ['#2ecc71', '#f39c12', '#e74c3c']
    explode = (0.05, 0.05, 0.05)
    
    wedges, texts, autotexts = plt.pie(risk_counts.values, 
                                        labels=risk_counts.index, 
                                        autopct='%1.1f%%',
                                        colors=colors, 
                                        explode=explode, 
                                        startangle=90,
                                        textprops={'fontsize': 11, 'fontweight': 'bold'})
    
    # Enhance text
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontweight('bold')
        autotext.set_fontsize(12)
    
    plt.title('Distribution of Students by Burnout Risk Category', fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig('static/graphs/10_risk_pie_chart.png', dpi=100, bbox_inches='tight')
    plt.close()
    return "10_risk_pie_chart.png"

def generate_all_dataset_graphs(filepath='data/student_data.csv'):
    """Generate all 10 graphs from dataset."""
    print("\nGenerating Dataset Graphs...")
    create_graphs_directory()
    
    df = clean_data(filepath)
    
    graphs = []
    
    graphs.append(generate_sleep_distribution(df))
    print("  ✓ Graph 1: Sleep Hours Distribution")
    
    graphs.append(generate_stress_distribution(df))
    print("  ✓ Graph 2: Stress Level Distribution")
    
    graphs.append(generate_study_hours_boxplot(df))
    print("  ✓ Graph 3: Study Hours Boxplot")
    
    graphs.append(generate_screen_time_distribution(df))
    print("  ✓ Graph 4: Screen Time Distribution")
    
    graphs.append(generate_burnout_distribution(df))
    print("  ✓ Graph 5: Burnout Score Distribution")
    
    graphs.append(generate_sleep_vs_burnout_scatter(df))
    print("  ✓ Graph 6: Sleep vs Burnout Scatter")
    
    graphs.append(generate_stress_vs_burnout_scatter(df))
    print("  ✓ Graph 7: Stress vs Burnout Scatter")
    
    graphs.append(generate_screen_time_vs_burnout_scatter(df))
    print("  ✓ Graph 8: Screen Time vs Burnout Scatter")
    
    graphs.append(generate_correlation_heatmap(df))
    print("  ✓ Graph 9: Correlation Heatmap")
    
    graphs.append(generate_risk_pie_chart(df))
    print("  ✓ Graph 10: Risk Category Pie Chart")
    
    print("\nAll dataset graphs generated successfully!\n")
    
    return graphs

if __name__ == "__main__":
    generate_all_dataset_graphs()
