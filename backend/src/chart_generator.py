import matplotlib.pyplot as plt
import seaborn as sns
import os

os.makedirs("static/charts", exist_ok=True)

# Pie Chart
plt.figure()
df["Risk_Level"].value_counts().plot.pie(autopct='%1.1f%%')
plt.title("Burnout Risk Category Distribution")
plt.savefig("static/charts/risk_distribution.png")
plt.close()

# Bar Chart
plt.figure()
sns.countplot(x="Risk_Level", data=df)
plt.title("Count of Students by Risk Level")
plt.savefig("static/charts/risk_bar_chart.png")
plt.close()

# Histogram
plt.figure()
sns.histplot(df["Burnout_Score"], bins=10, kde=True)
plt.title("Burnout Score Histogram")
plt.savefig("static/charts/burnout_histogram.png")
plt.close()

# Scatter Plot
plt.figure()
sns.scatterplot(x="Sleep_Hours", y="Burnout_Score", data=df)
plt.title("Sleep vs Burnout Score")
plt.savefig("static/charts/sleep_vs_burnout.png")
plt.close()
        'ytick.labelsize': 10,
        'legend.fontsize': 10,
        'figure.titlesize': 16
    })


def generate_risk_distribution_pie_chart(df, output_path):
    """Generate Burnout Risk Category Distribution Pie Chart."""
    plt.figure(figsize=(10, 8))
    
    # Count risk levels
    risk_counts = df['risk_level'].value_counts()
    
    # Create pie chart
    colors = ['#2ecc71', '#f39c12', '#e74c3c']  # Green, Orange, Red
    wedges, texts, autotexts = plt.pie(
        risk_counts.values,
        labels=risk_counts.index,
        autopct='%1.1f%%',
        colors=colors,
        startangle=90,
        explode=(0.05, 0.05, 0.05)  # Slightly separate slices
    )
    
    # Style the text
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontweight('bold')
        autotext.set_fontsize(12)
    
    for text in texts:
        text.set_fontweight('bold')
        text.set_fontsize(12)
    
    plt.title('Burnout Risk Category Distribution', fontsize=16, fontweight='bold', pad=20)
    plt.axis('equal')
    
    # Add legend
    plt.legend(
        title='Risk Levels',
        loc='center left',
        bbox_to_anchor=(1, 0, 0.5, 1),
        fontsize=12
    )
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    
    print(f"✓ Risk Distribution Pie Chart: {output_path}")


def generate_risk_bar_chart(df, output_path):
    """Generate Count of Students by Risk Level Bar Chart."""
    plt.figure(figsize=(12, 8))
    
    # Count risk levels
    risk_counts = df['risk_level'].value_counts()
    
    # Create bar chart
    colors = ['#2ecc71', '#f39c12', '#e74c3c']  # Green, Orange, Red
    
    bars = plt.bar(
        risk_counts.index,
        risk_counts.values,
        color=colors,
        alpha=0.8,
        edgecolor='black',
        linewidth=2
    )
    
    # Add value labels on top of bars
    for bar in bars:
        height = bar.get_height()
        plt.text(
            bar.get_x() + bar.get_width()/2.,
            height + 1,
            f'{int(height)}',
            ha='center',
            va='bottom',
            fontweight='bold',
            fontsize=14
        )
    
    plt.title('Count of Students by Risk Level', fontsize=16, fontweight='bold', pad=20)
    plt.xlabel('Risk Level', fontsize=14, fontweight='bold')
    plt.ylabel('Number of Students', fontsize=14, fontweight='bold')
    
    # Customize grid
    plt.grid(axis='y', alpha=0.3, linestyle='--')
    plt.gca().set_axisbelow(True)
    
    # Set y-axis to start from 0
    plt.ylim(0, max(risk_counts.values) * 1.2)
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    
    print(f"✓ Risk Bar Chart: {output_path}")


def generate_burnout_histogram(df, output_path):
    """Generate Burnout Score Histogram."""
    plt.figure(figsize=(12, 8))
    
    # Create histogram with KDE
    sns.histplot(
        data=df,
        x='burnout_score',
        bins=20,
        kde=True,
        color='#3498db',
        alpha=0.7,
        edgecolor='black',
        linewidth=1
    )
    
    # Add vertical lines for risk thresholds
    plt.axvline(x=4, color='#f39c12', linestyle='--', linewidth=2, label='Moderate Risk Threshold')
    plt.axvline(x=7, color='#e74c3c', linestyle='--', linewidth=2, label='High Risk Threshold')
    
    plt.title('Burnout Score Distribution', fontsize=16, fontweight='bold', pad=20)
    plt.xlabel('Burnout Score (0-10)', fontsize=14, fontweight='bold')
    plt.ylabel('Number of Students', fontsize=14, fontweight='bold')
    
    # Add legend
    plt.legend(fontsize=12)
    
    # Customize grid
    plt.grid(axis='y', alpha=0.3, linestyle='--')
    plt.gca().set_axisbelow(True)
    
    # Add statistics text
    mean_score = df['burnout_score'].mean()
    std_score = df['burnout_score'].std()
    plt.text(
        0.95, 0.95,
        f'Mean: {mean_score:.2f}\nStd: {std_score:.2f}',
        transform=plt.gca().transAxes,
        ha='right',
        va='top',
        bbox=dict(boxstyle='round', facecolor='white', alpha=0.8),
        fontsize=12,
        fontweight='bold'
    )
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    
    print(f"✓ Burnout Histogram: {output_path}")


def generate_sleep_vs_burnout_scatter(df, output_path):
    """Generate Sleep vs Burnout Score Scatter Plot."""
    plt.figure(figsize=(12, 8))
    
    # Create scatter plot with color coding by risk level
    colors = {'Low Risk': '#2ecc71', 'Moderate Risk': '#f39c12', 'High Risk': '#e74c3c'}
    
    for risk_level, color in colors.items():
        subset = df[df['risk_level'] == risk_level]
        plt.scatter(
            subset['sleep_hours'],
            subset['burnout_score'],
            c=color,
            label=risk_level,
            alpha=0.7,
            s=60,
            edgecolors='black',
            linewidth=1
        )
    
    # Add trend line
    z = np.polyfit(df['sleep_hours'], df['burnout_score'], 1)
    p = np.poly1d(z)
    plt.plot(
        df['sleep_hours'],
        p(df['sleep_hours']),
        "r--",
        alpha=0.8,
        linewidth=2,
        label=f'Trend: y={z[0]:.2f}x+{z[1]:.2f}'
    )
    
    plt.title('Sleep Hours vs Burnout Score', fontsize=16, fontweight='bold', pad=20)
    plt.xlabel('Sleep Hours (1-10 scale)', fontsize=14, fontweight='bold')
    plt.ylabel('Burnout Score (0-10)', fontsize=14, fontweight='bold')
    
    # Add legend
    plt.legend(fontsize=12)
    
    # Customize grid
    plt.grid(True, alpha=0.3, linestyle='--')
    plt.gca().set_axisbelow(True)
    
    # Add correlation coefficient
    correlation = df['sleep_hours'].corr(df['burnout_score'])
    plt.text(
        0.95, 0.05,
        f'Correlation: {correlation:.3f}',
        transform=plt.gca().transAxes,
        ha='right',
        va='bottom',
        bbox=dict(boxstyle='round', facecolor='white', alpha=0.8),
        fontsize=12,
        fontweight='bold'
    )
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    
    print(f"✓ Sleep vs Burnout Scatter Plot: {output_path}")


def generate_all_dashboard_charts(df, charts_dir='static/charts'):
    """Generate all charts for the risk dashboard."""
    # Create charts directory
    Path(charts_dir).mkdir(parents=True, exist_ok=True)
    
    # Setup chart styling
    setup_chart_style()
    
    print("🔧 Generating Dashboard Charts...")
    print("=" * 50)
    
    try:
        # Generate all charts
        generate_risk_distribution_pie_chart(
            df, 
            os.path.join(charts_dir, 'risk_distribution.png')
        )
        
        generate_risk_bar_chart(
            df, 
            os.path.join(charts_dir, 'risk_bar_chart.png')
        )
        
        generate_burnout_histogram(
            df, 
            os.path.join(charts_dir, 'burnout_histogram.png')
        )
        
        generate_sleep_vs_burnout_scatter(
            df, 
            os.path.join(charts_dir, 'sleep_vs_burnout.png')
        )
        
        print("=" * 50)
        print("✅ All dashboard charts generated successfully!")
        
        return True
        
    except Exception as e:
        print(f"❌ Error generating charts: {e}")
        return False


def check_charts_exist(charts_dir='static/charts'):
    """Check if all required charts exist."""
    required_charts = [
        'risk_distribution.png',
        'risk_bar_chart.png', 
        'burnout_histogram.png',
        'sleep_vs_burnout.png'
    ]
    
    missing_charts = []
    for chart in required_charts:
        chart_path = os.path.join(charts_dir, chart)
        if not os.path.exists(chart_path):
            missing_charts.append(chart)
    
    return missing_charts


if __name__ == '__main__':
    # Test the chart generator
    from burnout_analyzer import analyze_burnout_data
    
    # Load sample data
    data_path = 'data/student_data.csv'
    results = analyze_burnout_data(data_path)
    df = results['data']
    
    # Generate charts
    success = generate_all_dashboard_charts(df)
    
    if success:
        print("\n📊 Charts generated in static/charts/")
        print("Files created:")
        charts = ['risk_distribution.png', 'risk_bar_chart.png', 'burnout_histogram.png', 'sleep_vs_burnout.png']
        for chart in charts:
            print(f"  - static/charts/{chart}")
    else:
        print("\n❌ Failed to generate charts")
