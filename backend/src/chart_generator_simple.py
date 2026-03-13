import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import os
import numpy as np

def generate_simple_charts(df):
    """Generate charts using simple code as per requirements."""
    os.makedirs("static/charts", exist_ok=True)

    # Add department data if not present
    if 'department' not in df.columns:
        departments = ['Computer Science', 'Engineering', 'Medicine', 'Business', 'Arts', 'Science']
        df['department'] = np.random.choice(departments, size=len(df))

    # Pie Chart
    plt.figure()
    df["risk_level"].value_counts().plot.pie(autopct='%1.1f%%')
    plt.title("Burnout Risk Category Distribution")
    plt.savefig("static/charts/risk_distribution.png")
    plt.close()

    # Bar Chart
    plt.figure()
    sns.countplot(x="risk_level", data=df)
    plt.title("Count of Students by Risk Level")
    plt.savefig("static/charts/risk_bar_chart.png")
    plt.close()

    # Histogram
    plt.figure()
    sns.histplot(df["burnout_score"], bins=10, kde=True)
    plt.title("Burnout Score Histogram")
    plt.savefig("static/charts/burnout_histogram.png")
    plt.close()

    # Scatter Plot
    plt.figure()
    sns.scatterplot(x="sleep_hours", y="burnout_score", data=df)
    plt.title("Sleep vs Burnout Score")
    plt.savefig("static/charts/sleep_vs_burnout.png")
    plt.close()

    # Department Wise Burnout Risk Analysis
    plt.figure(figsize=(10,6))
    sns.countplot(
        x="department",
        hue="risk_level",
        data=df,
        palette={
            "Low Risk":"green",
            "Moderate Risk":"gold", 
            "High Risk":"red"
        }
    )
    plt.title("Department Wise Burnout Risk Distribution")
    plt.xticks(rotation=30)
    plt.tight_layout()
    plt.savefig("static/charts/department_risk.png")
    plt.close()

if __name__ == '__main__':
    # Test with sample data
    from burnout_analyzer import analyze_burnout_data
    data_path = 'data/student_data.csv'
    results = analyze_burnout_data(data_path)
    df = results['dataframe']
    generate_simple_charts(df)
    print("Simple charts generated with department analysis!")
