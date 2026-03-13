from flask import Flask, render_template, request, jsonify, send_file
import os
import sys
import pandas as pd
from datetime import datetime
from pathlib import Path

# Set working directory to backend folder
BACKEND_DIR = Path(__file__).parent
os.chdir(str(BACKEND_DIR))
sys.path.insert(0, str(BACKEND_DIR))

from src.data_cleaning import clean_data
from src.statistical_analysis import get_statistics_json
from src.correlation_analysis import get_correlation_data
from src.regression_model import get_regression_data
from src.data_visualization import generate_all_dataset_graphs
from src.input_graph_generator import generate_all_user_graphs
from src.risk_level_analysis import generate_all_risk_graphs
from src.burnout_model import analyze_student_burnout
from src.report_generator import generate_report
from src.pdf_generator import generate_burnout_report_pdf
from src.burnout_analyzer import analyze_burnout_data
from src.risk_graphs import generate_all_risk_graphs
from src.enhanced_pdf_generator import generate_burnout_report_pdf as generate_enhanced_pdf
from src.student_calculator import analyze_and_save_student
from src.report_downloader import get_student_report_file, list_all_student_reports, generate_report_summary
from src.chart_generator_simple import generate_simple_charts
from src.data_manager import export_student_data, export_student_results, create_system_backup, get_system_statistics

app = Flask(__name__)
app.config['SECRET_KEY'] = 'academic-burnout-detection-secret'

# Generate graphs and report on startup
print("=" * 70)
print("ACADEMIC BURNOUT DETECTION SYSTEM")
print("=" * 70)
print("\nInitializing application...")

print("\n[1/4] Generating dataset-based graphs (10 visualizations)...")
try:
    generate_all_dataset_graphs()
except Exception as e:
    print(f"  ✗ Error generating dataset graphs: {e}")

print("\n[2/4] Generating risk analysis graphs...")
try:
    generate_all_risk_graphs()
except Exception as e:
    print(f"  ✗ Error generating risk analysis graphs: {e}")

print("\n[3/4] Generating analysis report...")
try:
    data_path = os.path.join('data', 'student_data.csv')
    # generate_report writes to reports/analysis_report.txt relative to cwd
    report_text = generate_report(filepath=data_path)
    print("  ✓ Report text generated (also saved to disk)")
except Exception as e:
    print(f"  ✗ Error generating report: {e}")

print("\n[3/3] Application ready for requests!")
print("=" * 70)
print("\nAccess the application at: http://localhost:5000")
print("\n")

# ============================================================================
# ROUTES
# ============================================================================

@app.route('/')
def index():
    """Home dashboard."""
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    """Graph dashboard."""
    # prepare risk analysis graph URLs if they exist
    risk_folder = os.path.join('static', 'graphs')
    risk_files = {}
    if os.path.exists(risk_folder):
        for fname in os.listdir(risk_folder):
            if fname.lower().endswith('.png'):
                key = fname.rsplit('.', 1)[0]
                # Use forward slashes for web URLs
                risk_files[key] = os.path.join('graphs', fname).replace('\\', '/')
    return render_template('dashboard.html', risk_files=risk_files)

@app.route('/risk_dashboard')
def risk_dashboard():
    """Enhanced risk distribution dashboard."""
    try:
        data_path = os.path.join('data', 'student_data.csv')
        results = analyze_burnout_data(data_path)
        stats = results['summary_stats']
        risk_dist = results['risk_distribution']
        indicators = results['indicators']
        
        # Generate simple charts if they don't exist
        charts_dir = os.path.join('static', 'charts')
        if not os.path.exists(charts_dir):
            generate_simple_charts(results['dataframe'])
        
        return render_template('risk_dashboard.html', 
                             stats=stats, 
                             risk_distribution=risk_dist,
                             indicators=indicators)
    except Exception as e:
        return f"Error loading risk dashboard: {e}", 500

@app.route('/student_calculator')
def student_calculator():
    """Student burnout calculator page."""
    return render_template('student_calculator.html')

@app.route('/reports_center')
def reports_center():
    """Reports center page."""
    return render_template('reports_center.html')

@app.route('/part_dashboard')
def part_dashboard():
    """System parts dashboard page."""
    return render_template('part_dashboard.html')

@app.route('/api/export_student_data', methods=['POST'])
def api_export_student_data():
    """Export student data to CSV."""
    try:
        result = export_student_data()
        return jsonify(result)
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/export_student_results', methods=['POST'])
def api_export_student_results():
    """Export student results to CSV."""
    try:
        result = export_student_results()
        return jsonify(result)
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/create_backup', methods=['POST'])
def api_create_backup():
    """Create system backup."""
    try:
        result = create_system_backup()
        return jsonify(result)
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/system_statistics', methods=['GET'])
def api_system_statistics():
    """Get system statistics."""
    try:
        result = get_system_statistics()
        return jsonify(result)
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/download_export/<filename>')
def download_export(filename):
    """Download exported file."""
    try:
        export_path = os.path.join('exports', filename)
        if os.path.exists(export_path):
            return send_file(
                export_path,
                as_attachment=True,
                download_name=filename
            )
        else:
            return "File not found", 404
    except Exception as e:
        return f"Error downloading file: {e}", 500

@app.route('/api/student_reports', methods=['GET'])
def api_student_reports():
    """Get list of all student reports."""
    try:
        reports = list_all_student_reports()
        return jsonify({
            'success': True,
            'data': reports,
            'total': len(reports)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/report_summary/<student_id>', methods=['GET'])
def api_report_summary(student_id):
    """Get summary of a specific student report."""
    try:
        summary = generate_report_summary(student_id)
        return jsonify({
            'success': True,
            'data': summary
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/download_report/<student_id>')
def download_report(student_id):
    """Download a specific student report."""
    try:
        report_file = get_student_report_file(student_id)
        if report_file and os.path.exists(report_file):
            return send_file(
                report_file,
                as_attachment=True,
                download_name=os.path.basename(report_file)
            )
        else:
            return "Report not found", 404
    except Exception as e:
        return f"Error downloading report: {e}", 500

@app.route('/api/calculate_burnout', methods=['POST'])
def api_calculate_burnout():
    """Calculate burnout risk for student input."""
    try:
        data = request.get_json()
        
        # Extract student data
        student_id = data.get('student_id', f'STD_{datetime.now().strftime("%Y%m%d_%H%M%S")}')
        sleep_hours = float(data.get('sleep_hours'))
        study_hours = float(data.get('study_hours'))
        screen_time = float(data.get('screen_time'))
        stress_level = float(data.get('stress_level'))
        physical_activity = float(data.get('physical_activity'))
        assignment_load = float(data.get('assignment_load'))
        
        # Analyze and save student
        result = analyze_and_save_student(
            student_id=student_id,
            sleep_hours=sleep_hours,
            study_hours=study_hours,
            screen_time=screen_time,
            stress_level=stress_level,
            physical_activity=physical_activity,
            assignment_load=assignment_load
        )
        
        # Return the expected structure for the frontend
        return jsonify({
            'success': True,
            'data': result['student_data']  # Return the student_data directly
        })
    except ValueError as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/predict')
def predict():
    """Burnout prediction page."""
    return render_template('predict.html')

# ============================================================================
# API ENDPOINTS
# ============================================================================

@app.route('/api/statistics', methods=['GET'])
def api_statistics():
    """Get descriptive statistics."""
    try:
        stats = get_statistics_json('data/student_data.csv')
        return jsonify({
            'success': True,
            'data': stats
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/correlation', methods=['GET'])
def api_correlation():
    """Get correlation matrix and burnout indicators."""
    try:
        corr_data = get_correlation_data('data/student_data.csv')
        return jsonify({
            'success': True,
            'data': corr_data
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/regression', methods=['GET'])
def api_regression():
    """Get regression model coefficients."""
    try:
        regression = get_regression_data('data/student_data.csv')
        return jsonify({
            'success': True,
            'data': regression
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/graphs', methods=['GET'])
def api_graphs():
    """Get list of available graphs."""
    try:
        graph_dir = 'static/graphs'
        graphs = {
            'histogram': [
                {'name': 'Sleep Distribution', 'filename': 'sleep_distribution.png'},
                {'name': 'Stress Distribution', 'filename': 'stress_distribution.png'},
                {'name': 'Burnout Distribution', 'filename': 'burnout_distribution.png'}
            ],
            'scatter': [
                {'name': 'Sleep vs Burnout', 'filename': 'sleep_vs_burnout.png'},
                {'name': 'Stress vs Burnout', 'filename': 'stress_vs_burnout.png'},
                {'name': 'Screen Time vs Burnout', 'filename': 'screen_vs_burnout.png'}
            ],
            'heatmap': [
                {'name': 'Correlation Heatmap', 'filename': 'correlation_heatmap.png'}
            ],
            'other': [
                {'name': 'Risk Distribution', 'filename': 'risk_pie_chart.png'},
                {'name': 'Study Hours Analysis', 'filename': 'study_hours_boxplot.png'}
            ]
        }
        return jsonify({
            'success': True,
            'data': graphs
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/burnout_predict', methods=['POST'])
def api_burnout_predict():
    """Predict burnout risk for a student."""
    try:
        data = request.json
        
        # Extract input values
        sleep_hours = float(data.get('sleep_hours', 7))
        study_hours = float(data.get('study_hours', 5))
        screen_time = float(data.get('screen_time', 6))
        stress_level = float(data.get('stress_level', 5))
        physical_activity = float(data.get('physical_activity', 5))
        assignment_load = float(data.get('assignment_load', 5))
        
        # Validate input ranges
        if not (0 <= sleep_hours <= 12):
            raise ValueError("Sleep hours must be between 0-12")
        if not (0 <= study_hours <= 12):
            raise ValueError("Study hours must be between 0-12")
        if not (0 <= screen_time <= 14):
            raise ValueError("Screen time must be between 0-14")
        if not (0 <= stress_level <= 10):
            raise ValueError("Stress level must be between 0-10")
        if not (0 <= physical_activity <= 10):
            raise ValueError("Physical activity must be between 0-10")
        if not (0 <= assignment_load <= 10):
            raise ValueError("Assignment load must be between 0-10")
        
        # Analyze burnout
        result = analyze_student_burnout(
            sleep_hours=sleep_hours,
            study_hours=study_hours,
            screen_time=screen_time,
            stress_level=stress_level,
            physical_activity=physical_activity,
            assignment_load=assignment_load
        )
        
        return jsonify({
            'success': True,
            'data': result
        })
    except ValueError as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/dataset_summary', methods=['GET'])
def api_dataset_summary():
    """Get dataset summary information."""
    try:
        df = clean_data('data/student_data.csv')
        stats = get_statistics_json('data/student_data.csv')
        
        summary = {
            'total_students': len(df),
            'variables': list(df.columns),
            'sleep_hours_avg': stats['sleep_hours']['mean'],
            'study_hours_avg': stats['study_hours']['mean'],
            'screen_time_avg': stats['screen_time']['mean'],
            'stress_level_avg': stats['stress_level']['mean'],
            'physical_activity_avg': stats['physical_activity']['mean'],
            'assignment_load_avg': stats['assignment_load']['mean']
        }
        
        return jsonify({
            'success': True,
            'data': summary
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/report', methods=['GET'])
def api_report():
    """Get the analysis report."""
    try:
        # regenerate or read the latest report text
        report = generate_report()
        return jsonify({
            'success': True,
            'data': report
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/dataset_graphs', methods=['GET'])
def api_dataset_graphs():
    """Get list of all dataset graphs."""
    try:
        graphs = {
            'distributions': [
                {'name': 'Sleep Hours Distribution', 'filename': '01_sleep_distribution.png', 'description': 'Histogram showing sleep patterns'},
                {'name': 'Stress Level Distribution', 'filename': '02_stress_distribution.png', 'description': 'Histogram of stress levels'},
                {'name': 'Screen Time Distribution', 'filename': '04_screen_time_distribution.png', 'description': 'Daily screen time patterns'},
                {'name': 'Burnout Score Distribution', 'filename': '05_burnout_distribution.png', 'description': 'Distribution of predicted burnout scores'},
            ],
            'box_and_analysis': [
                {'name': 'Study Hours Boxplot', 'filename': '03_study_hours_boxplot.png', 'description': 'Study hours by risk category'},
            ],
            'scatter_plots': [
                {'name': 'Sleep vs Burnout', 'filename': '06_sleep_vs_burnout.png', 'description': 'Negative correlation analysis'},
                {'name': 'Stress vs Burnout', 'filename': '07_stress_vs_burnout.png', 'description': 'Strong positive correlation'},
                {'name': 'Screen Time vs Burnout', 'filename': '08_screen_time_vs_burnout.png', 'description': 'Digital exposure impact'},
            ],
            'heatmap': [
                {'name': 'Correlation Heatmap', 'filename': '09_correlation_heatmap.png', 'description': 'All variable relationships'},
            ],
            'pie_chart': [
                {'name': 'Risk Distribution', 'filename': '10_risk_pie_chart.png', 'description': 'Student risk categories'},
            ],
            # additional risk analysis graphs located under risk_analysis subfolder
            'risk_analysis': [
                {'name': 'Risk Bar Chart', 'filename': 'risk_analysis/risk_bar_chart.png', 'description': 'Counts of students by risk level'},
                {'name': 'Risk Pie Chart', 'filename': 'risk_analysis/risk_pie_chart.png', 'description': 'Percentage of each risk level'},
                {'name': 'Burnout Histogram', 'filename': 'risk_analysis/burnout_histogram.png', 'description': 'Histogram of burnout scores'},
            ]
        }
        return jsonify({
            'success': True,
            'data': graphs
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/user_graphs', methods=['POST'])
def api_user_graphs():
    """Generate and return user input-based graphs."""
    try:
        data = request.json
        
        # Extract input values
        sleep_hours = float(data.get('sleep_hours', 7))
        study_hours = float(data.get('study_hours', 5))
        screen_time = float(data.get('screen_time', 6))
        stress_level = float(data.get('stress_level', 5))
        physical_activity = float(data.get('physical_activity', 5))
        assignment_load = float(data.get('assignment_load', 5))
        
        # Validate input ranges
        if not (0 <= sleep_hours <= 12):
            raise ValueError("Sleep hours must be between 0-12")
        if not (0 <= study_hours <= 12):
            raise ValueError("Study hours must be between 0-12")
        if not (0 <= screen_time <= 14):
            raise ValueError("Screen time must be between 0-14")
        if not (0 <= stress_level <= 10):
            raise ValueError("Stress level must be between 0-10")
        if not (0 <= physical_activity <= 10):
            raise ValueError("Physical activity must be between 0-10")
        if not (0 <= assignment_load <= 10):
            raise ValueError("Assignment load must be between 0-10")
        
        # Analyze burnout
        burnout_result = analyze_student_burnout(
            sleep_hours=sleep_hours,
            study_hours=study_hours,
            screen_time=screen_time,
            stress_level=stress_level,
            physical_activity=physical_activity,
            assignment_load=assignment_load
        )
        
        # Generate user graphs
        graph_files = generate_all_user_graphs(
            sleep_hours=sleep_hours,
            study_hours=study_hours,
            screen_time=screen_time,
            stress_level=stress_level,
            physical_activity=physical_activity,
            assignment_load=assignment_load,
            burnout_score=burnout_result['burnout_score']
        )
        
        return jsonify({
            'success': True,
            'data': {
                'burnout_analysis': burnout_result,
                'user_graphs': {
                    'bar_chart': graph_files[0],
                    'radar_chart': graph_files[1],
                    'gauge_chart': graph_files[2]
                }
            }
        })
    except ValueError as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/download-report', methods=['GET'])
def api_download_report():
    """Generate and download burnout report as PDF."""
    try:
        pdf_path = os.path.join('reports', 'burnout_report.pdf')
        
        # Generate PDF
        generated_path = generate_burnout_report_pdf(
            filepath=os.path.join('data', 'student_data.csv'),
            output_path=pdf_path
        )
        
        if generated_path and os.path.exists(generated_path):
            return send_file(
                generated_path,
                mimetype='application/pdf',
                as_attachment=True,
                download_name=f'burnout_report_{pd.Timestamp.now().strftime("%Y%m%d_%H%M%S")}.pdf'
            )
        else:
            return jsonify({
                'success': False,
                'error': 'Failed to generate PDF report'
            }), 500
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/correlation_indicators', methods=['GET'])
def api_correlation_indicators():
    """Get strongest burnout indicators (correlation with burnout)."""
    try:
        corr_data = get_correlation_data('data/student_data.csv')
        indicators = corr_data.get('burnout_indicators', {})
        
        # Sort by absolute correlation value
        sorted_indicators = sorted(
            indicators.items(),
            key=lambda x: abs(x[1]),
            reverse=True
        )
        
        formatted = []
        for factor, corr_value in sorted_indicators:
            direction = "↑" if corr_value > 0 else "↓"
            formatted.append({
                'factor': factor.replace('_', ' ').title(),
                'correlation': round(corr_value, 3),
                'direction': direction,
                'description': f"{'Increases' if corr_value > 0 else 'Decreases'} burnout risk"
            })
        
        return jsonify({
            'success': True,
            'data': formatted
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# ============================================================================
# ERROR HANDLERS
# ============================================================================

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=5000)
