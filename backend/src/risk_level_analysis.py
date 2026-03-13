"""
Risk level analysis and visualization module.

Uses the burnout score calculated for each student to classify them into
Low/Medium/High risk categories and generate analytical graphs.

Advanced features include trend analysis (if weekly data provided),
department-wise comparison (if department column exists) and lifestyle
impact scatter plots.

Graphs are saved under static/graphs/risk_analysis/ and filenames are
standardized.
"""

import os
from datetime import datetime

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from src.data_cleaning import clean_data
from src.burnout_model import calculate_burnout_score, get_risk_category

# Configure plotting defaults
sns.set_style("whitegrid")
plt.rcParams['figure.dpi'] = 100
plt.rcParams['figure.figsize'] = (12, 7)


def create_risk_directory():
    """Ensure the directory for risk analysis graphs exists."""
    path = os.path.join('static', 'graphs', 'risk_analysis')
    if not os.path.exists(path):
        os.makedirs(path)
    return path


def classify_risk(df: pd.DataFrame) -> pd.DataFrame:
    """Return a copy of ``df`` with burnout_score and risk_level columns added."""
    df_copy = df.copy()
    # calculate burnout score for each row
    df_copy['burnout_score'] = df_copy.apply(
        lambda row: calculate_burnout_score(
            row['sleep_hours'], row['study_hours'], row['screen_time'],
            row['stress_level'], row['physical_activity'], row['assignment_load']
        ),
        axis=1
    )
    df_copy['risk_level'] = df_copy['burnout_score'].apply(get_risk_category)
    return df_copy


def get_risk_counts(df: pd.DataFrame) -> dict:
    """Return a dictionary mapping risk levels to student counts."""
    return df['risk_level'].value_counts().to_dict()


def generate_risk_bar_chart(risk_counts: dict) -> str:
    """Create and save a bar chart of risk level counts.

    Returns the relative filename of the saved chart.
    """
    path = create_risk_directory()
    labels = list(risk_counts.keys())
    counts = [risk_counts[label] for label in labels]
    colors = ['#90EE90', '#FFD700', '#FF6B6B']  # low, medium, high
    plt.figure()
    sns.barplot(x=labels, y=counts, palette=colors)
    plt.title('Burnout Risk Distribution')
    plt.xlabel('Risk Level')
    plt.ylabel('Number of Students')
    for i, v in enumerate(counts):
        plt.text(i, v + 0.5, str(v), ha='center', fontsize=10)
    filename = os.path.join(path, 'risk_bar_chart.png')
    plt.savefig(filename, bbox_inches='tight')
    plt.close()
    return filename


def generate_risk_pie_chart(risk_counts: dict) -> str:
    """Create and save a pie chart showing percentage of each risk level."""
    path = create_risk_directory()
    labels = list(risk_counts.keys())
    counts = [risk_counts[label] for label in labels]
    colors = ['#90EE90', '#FFD700', '#FF6B6B']
    plt.figure()
    plt.pie(counts, labels=labels, autopct='%1.1f%%', colors=colors, startangle=140)
    plt.axis('equal')
    plt.title('Burnout Risk Category Distribution')
    filename = os.path.join(path, 'risk_pie_chart.png')
    plt.savefig(filename, bbox_inches='tight')
    plt.close()
    return filename


def generate_burnout_histogram(df: pd.DataFrame) -> str:
    """Create and save a histogram of burnout scores across students."""
    path = create_risk_directory()
    plt.figure()
    plt.hist(df['burnout_score'], bins=20, color='#3498db', edgecolor='black', alpha=0.7)
    plt.xlabel('Burnout Score')
    plt.ylabel('Number of Students')
    plt.title('Distribution of Burnout Scores')
    filename = os.path.join(path, 'burnout_histogram.png')
    plt.savefig(filename, bbox_inches='tight')
    plt.close()
    return filename


# -------------------- Advanced/Optional Features --------------------

def generate_risk_trend_graph(weekly_df: pd.DataFrame) -> str | None:
    """Produce a trend line of high‑risk student counts if weekly data is given.

    weekly_df should contain at least columns ``Week`` and
    ``HighRiskStudents``. Returns filename or ``None`` if generation skipped.
    """
    if weekly_df is None or weekly_df.empty:
        return None
    if 'Week' not in weekly_df.columns or 'HighRiskStudents' not in weekly_df.columns:
        return None
    path = create_risk_directory()
    plt.figure()
    sns.lineplot(data=weekly_df, x='Week', y='HighRiskStudents', marker='o')
    plt.title('High Risk Students Trend Over Time')
    plt.xlabel('Week')
    plt.ylabel('Number of High Risk Students')
    filename = os.path.join(path, 'risk_trend.png')
    plt.savefig(filename, bbox_inches='tight')
    plt.close()
    return filename


def generate_department_comparison(df: pd.DataFrame) -> str | None:
    """Create a bar chart comparing high‑risk counts by department.

    Returns filename or ``None`` if department data is unavailable.
    """
    if 'department' not in df.columns:
        return None
    high_risk = df[df['risk_level'] == 'High Risk']
    dept_counts = high_risk['department'].value_counts()
    if dept_counts.empty:
        return None
    path = create_risk_directory()
    plt.figure()
    sns.barplot(x=dept_counts.index, y=dept_counts.values, palette='rocket')
    plt.title('High Risk Students by Department')
    plt.xlabel('Department')
    plt.ylabel('Number of High Risk Students')
    plt.xticks(rotation=45)
    filename = os.path.join(path, 'department_highrisk_bar.png')
    plt.savefig(filename, bbox_inches='tight')
    plt.close()
    return filename


def generate_lifestyle_impact_graph(df: pd.DataFrame) -> str | None:
    """Scatter plot showing relationship between sleep hours and burnout.

    Returns filename or ``None`` if necessary columns are missing.
    """
    if 'sleep_hours' not in df.columns or 'burnout_score' not in df.columns:
        return None
    path = create_risk_directory()
    plt.figure()
    sns.scatterplot(data=df, x='sleep_hours', y='burnout_score', hue='risk_level',
                    palette=['#90EE90', '#FFD700', '#FF6B6B'])
    plt.title('Sleep Hours vs Burnout Score')
    plt.xlabel('Sleep Hours')
    plt.ylabel('Burnout Score')
    filename = os.path.join(path, 'sleep_vs_burnout_scatter.png')
    plt.savefig(filename, bbox_inches='tight')
    plt.close()
    return filename


def generate_all_risk_graphs() -> dict:
    """Run full risk analysis pipeline and save all graphs.

    Returns a dictionary of generated filenames for each chart. Missing
    or optional graphs will have value ``None``.
    """
    df = clean_data('data/student_data.csv')
    df = classify_risk(df)
    counts = get_risk_counts(df)

    bar = generate_risk_bar_chart(counts)
    pie = generate_risk_pie_chart(counts)
    hist = generate_burnout_histogram(df)

    # optional advanced outputs
    trend_file = None
    dept_file = None
    lifestyle_file = generate_lifestyle_impact_graph(df)

    # look for weekly data CSV if present
    weekly_path = os.path.join('data', 'weekly_risk.csv')
    if os.path.exists(weekly_path):
        try:
            weekly_df = pd.read_csv(weekly_path)
            trend_file = generate_risk_trend_graph(weekly_df)
        except Exception:
            trend_file = None

    dept_file = generate_department_comparison(df)

    return {
        'bar': bar,
        'pie': pie,
        'histogram': hist,
        'trend': trend_file,
        'department': dept_file,
        'lifestyle': lifestyle_file
    }
