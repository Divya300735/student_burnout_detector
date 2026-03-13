import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from src.data_cleaning import clean_data
from src.burnout_model import calculate_burnout_score, get_risk_category
import os

# Set style for all plots
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (10, 6)

def create_graphs_directory():
    """Ensure graphs directory exists."""
    if not os.path.exists('static/graphs'):
        os.makedirs('static/graphs')

def generate_sleep_distribution(df):
    """Generate sleep hours distribution histogram."""
    plt.figure(figsize=(10, 6))
    plt.hist(df['sleep_hours'], bins=20, color='skyblue', edgecolor='black', alpha=0.7)
    plt.xlabel('Sleep Hours', fontsize=12)
    plt.ylabel('Frequency', fontsize=12)
    plt.title('Distribution of Sleep Hours', fontsize=14, fontweight='bold')
    plt.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    plt.savefig('static/graphs/sleep_distribution.png', dpi=100, bbox_inches='tight')
    plt.close()

def generate_stress_distribution(df):
    """Generate stress level distribution histogram."""
    plt.figure(figsize=(10, 6))
    plt.hist(df['stress_level'], bins=20, color='coral', edgecolor='black', alpha=0.7)
    plt.xlabel('Stress Level', fontsize=12)
    plt.ylabel('Frequency', fontsize=12)
    plt.title('Distribution of Stress Levels', fontsize=14, fontweight='bold')
    plt.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    plt.savefig('static/graphs/stress_distribution.png', dpi=100, bbox_inches='tight')
    plt.close()

def generate_burnout_distribution(df):
    """Generate burnout score distribution histogram."""
    df_temp = df.copy()
    df_temp['burnout_score'] = df_temp.apply(
        lambda row: calculate_burnout_score(
            row['sleep_hours'], row['study_hours'], row['screen_time'],
            row['stress_level'], row['physical_activity'], row['assignment_load']
        ), axis=1
    )
    
    plt.figure(figsize=(10, 6))
    plt.hist(df_temp['burnout_score'], bins=20, color='lightcoral', edgecolor='black', alpha=0.7)
    plt.xlabel('Burnout Score (0-10)', fontsize=12)
    plt.ylabel('Frequency', fontsize=12)
    plt.title('Distribution of Burnout Scores', fontsize=14, fontweight='bold')
    plt.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    plt.savefig('static/graphs/burnout_distribution.png', dpi=100, bbox_inches='tight')
    plt.close()

def generate_sleep_vs_burnout(df):
    """Generate scatter plot of sleep vs burnout score."""
    df_temp = df.copy()
    df_temp['burnout_score'] = df_temp.apply(
        lambda row: calculate_burnout_score(
            row['sleep_hours'], row['study_hours'], row['screen_time'],
            row['stress_level'], row['physical_activity'], row['assignment_load']
        ), axis=1
    )
    
    plt.figure(figsize=(10, 6))
    plt.scatter(df_temp['sleep_hours'], df_temp['burnout_score'], alpha=0.6, s=100, color='steelblue')
    
    # Add trend line
    z = np.polyfit(df_temp['sleep_hours'], df_temp['burnout_score'], 1)
    p = np.poly1d(z)
    x_trend = np.linspace(df_temp['sleep_hours'].min(), df_temp['sleep_hours'].max(), 100)
    plt.plot(x_trend, p(x_trend), "r--", linewidth=2, label='Trend')
    
    plt.xlabel('Sleep Hours', fontsize=12)
    plt.ylabel('Burnout Score', fontsize=12)
    plt.title('Sleep Hours vs Burnout Score', fontsize=14, fontweight='bold')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('static/graphs/sleep_vs_burnout.png', dpi=100, bbox_inches='tight')
    plt.close()

def generate_stress_vs_burnout(df):
    """Generate scatter plot of stress vs burnout score."""
    df_temp = df.copy()
    df_temp['burnout_score'] = df_temp.apply(
        lambda row: calculate_burnout_score(
            row['sleep_hours'], row['study_hours'], row['screen_time'],
            row['stress_level'], row['physical_activity'], row['assignment_load']
        ), axis=1
    )
    
    plt.figure(figsize=(10, 6))
    plt.scatter(df_temp['stress_level'], df_temp['burnout_score'], alpha=0.6, s=100, color='darkred')
    
    # Add trend line
    z = np.polyfit(df_temp['stress_level'], df_temp['burnout_score'], 1)
    p = np.poly1d(z)
    x_trend = np.linspace(df_temp['stress_level'].min(), df_temp['stress_level'].max(), 100)
    plt.plot(x_trend, p(x_trend), "b--", linewidth=2, label='Trend')
    
    plt.xlabel('Stress Level', fontsize=12)
    plt.ylabel('Burnout Score', fontsize=12)
    plt.title('Stress Level vs Burnout Score', fontsize=14, fontweight='bold')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('static/graphs/stress_vs_burnout.png', dpi=100, bbox_inches='tight')
    plt.close()

def generate_screen_time_vs_burnout(df):
    """Generate scatter plot of screen time vs burnout score."""
    df_temp = df.copy()
    df_temp['burnout_score'] = df_temp.apply(
        lambda row: calculate_burnout_score(
            row['sleep_hours'], row['study_hours'], row['screen_time'],
            row['stress_level'], row['physical_activity'], row['assignment_load']
        ), axis=1
    )
    
    plt.figure(figsize=(10, 6))
    plt.scatter(df_temp['screen_time'], df_temp['burnout_score'], alpha=0.6, s=100, color='purple')
    
    # Add trend line
    z = np.polyfit(df_temp['screen_time'], df_temp['burnout_score'], 1)
    p = np.poly1d(z)
    x_trend = np.linspace(df_temp['screen_time'].min(), df_temp['screen_time'].max(), 100)
    plt.plot(x_trend, p(x_trend), "orange", linewidth=2, linestyle='--', label='Trend')
    
    plt.xlabel('Screen Time (hours)', fontsize=12)
    plt.ylabel('Burnout Score', fontsize=12)
    plt.title('Screen Time vs Burnout Score', fontsize=14, fontweight='bold')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('static/graphs/screen_vs_burnout.png', dpi=100, bbox_inches='tight')
    plt.close()

def generate_correlation_heatmap(df):
    """Generate correlation heatmap."""
    plt.figure(figsize=(10, 8))
    correlation = df.corr()
    sns.heatmap(correlation, annot=True, fmt='.2f', cmap='coolwarm', center=0,
                square=True, linewidths=1, cbar_kws={"shrink": 0.8})
    plt.title('Correlation Matrix Heatmap', fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig('static/graphs/correlation_heatmap.png', dpi=100, bbox_inches='tight')
    plt.close()

def generate_risk_pie_chart(df):
    """Generate pie chart of risk categories."""
    df_temp = df.copy()
    df_temp['burnout_score'] = df_temp.apply(
        lambda row: calculate_burnout_score(
            row['sleep_hours'], row['study_hours'], row['screen_time'],
            row['stress_level'], row['physical_activity'], row['assignment_load']
        ), axis=1
    )
    df_temp['risk_category'] = df_temp['burnout_score'].apply(get_risk_category)
    
    risk_counts = df_temp['risk_category'].value_counts()
    
    plt.figure(figsize=(10, 7))
    colors = ['#90EE90', '#FFD700', '#FF6B6B']  # Light green, gold, light red
    explode = (0.05, 0.05, 0.05)
    
    plt.pie(risk_counts.values, labels=risk_counts.index, autopct='%1.1f%%',
            colors=colors, explode=explode, startangle=90, textprops={'fontsize': 12})
    plt.title('Distribution of Burnout Risk Categories', fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig('static/graphs/risk_pie_chart.png', dpi=100, bbox_inches='tight')
    plt.close()

def generate_study_hours_boxplot(df):
    """Generate boxplot for study hours."""
    df_temp = df.copy()
    df_temp['burnout_score'] = df_temp.apply(
        lambda row: calculate_burnout_score(
            row['sleep_hours'], row['study_hours'], row['screen_time'],
            row['stress_level'], row['physical_activity'], row['assignment_load']
        ), axis=1
    )
    df_temp['risk_category'] = df_temp['burnout_score'].apply(get_risk_category)
    
    plt.figure(figsize=(10, 6))
    sns.boxplot(data=df_temp, x='risk_category', y='study_hours', 
                palette=['#90EE90', '#FFD700', '#FF6B6B'])
    plt.xlabel('Risk Category', fontsize=12)
    plt.ylabel('Study Hours', fontsize=12)
    plt.title('Study Hours Distribution by Risk Category', fontsize=14, fontweight='bold')
    plt.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    plt.savefig('static/graphs/study_hours_boxplot.png', dpi=100, bbox_inches='tight')
    plt.close()

def generate_all_graphs(filepath='data/student_data.csv'):
    """Generate all graphs."""
    print("Generating graphs...")
    create_graphs_directory()
    
    df = clean_data(filepath)
    
    generate_sleep_distribution(df)
    print("  ✓ Sleep distribution graph")
    
    generate_stress_distribution(df)
    print("  ✓ Stress distribution graph")
    
    generate_burnout_distribution(df)
    print("  ✓ Burnout distribution graph")
    
    generate_sleep_vs_burnout(df)
    print("  ✓ Sleep vs burnout scatter plot")
    
    generate_stress_vs_burnout(df)
    print("  ✓ Stress vs burnout scatter plot")
    
    generate_screen_time_vs_burnout(df)
    print("  ✓ Screen time vs burnout scatter plot")
    
    generate_correlation_heatmap(df)
    print("  ✓ Correlation heatmap")
    
    generate_risk_pie_chart(df)
    print("  ✓ Risk category pie chart")
    
    generate_study_hours_boxplot(df)
    print("  ✓ Study hours boxplot")
    
    print("\nAll graphs generated successfully and saved to static/graphs/")

if __name__ == "__main__":
    generate_all_graphs()
