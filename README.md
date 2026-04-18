<<<<<<< HEAD
# Early Statistical Detection of Academic Burnout

A comprehensive full-stack web application that analyzes student lifestyle data and detects early signs of academic burnout using **statistical analysis methods only** (no machine learning).

## 🎯 Project Overview

This system uses statistical modeling techniques to identify burnout risk in students based on their lifestyle patterns including:
- Sleep hours
- Study hours
- Screen time
- Stress level
- Physical activity
- Assignment load

The application provides:
- **Descriptive Statistics**: Mean, median, variance, standard deviation
- **Correlation Analysis**: Identify strongest burnout indicators
- **Linear Regression**: Model burnout based on lifestyle factors
- **Risk Assessment**: Calculate burnout probability and categorize risk levels
- **Visual Analytics**: Graphs and charts showing data distributions and patterns
- **Personalized Recommendations**: Actionable advice based on individual data

## 📋 Features

### Backend (Python Flask)
- ✅ Data cleaning and validation module
- ✅ Descriptive statistical analysis
- ✅ Pearson correlation matrix calculation
- ✅ Multiple linear regression (using mathematical formulas)
- ✅ Burnout score calculation
- ✅ Risk categorization and probability estimation
- ✅ Automatic graph generation
- ✅ **Simplified report generation module** (`src/report_generator.py`)
- ✅ RESTful API endpoints

The report is also produced when running `python main.py` from the project root; this creates `reports/analysis_report.txt` automatically.

### Frontend (HTML, CSS, JavaScript)
- ✅ Responsive dashboard layout
- ✅ Home page with statistics overview
- ✅ Analytics dashboard with graphs
- ✅ Interactive burnout risk calculator
- ✅ Real-time slider inputs
- ✅ Personalized recommendations
- ✅ Statistical insights section
- ✅ Mobile-friendly design

### Statistical Methods Used
- Descriptive Statistics (mean, median, std dev, variance)
- Pearson Correlation Analysis
- Multiple Linear Regression (Normal Equation Method)
- Probability Estimation (Normal Distribution)
- Rule-Based Threshold Classification

## 📁 Project Structure

```
academic_burnout_detection/
backend/
├── app.py                    # Flask application and API endpoints
├── requirements.txt          # Python dependencies
│
├── data/
│   └── student_data.csv     # Dataset with 200+ student records
│
├── src/
│   ├── data_cleaning.py             # Data loading and validation
│   ├── statistical_analysis.py       # Descriptive statistics
│   ├── correlation_analysis.py       # Correlation matrices
│   ├── regression_model.py           # Linear regression
│   ├── burnout_model.py              # Burnout calculation and risk assessment
│   ├── visualization.py              # Graph generation
│   └── report_generator.py           # Analysis report creation
│
├── static/
│   ├── css/
│   │   └── style.css                 # Stylesheet
│   ├── js/
│   │   └── script.js                 # JavaScript functionality
│   └── graphs/                       # Generated graph images
│       ├── sleep_distribution.png
│       ├── stress_distribution.png
│       ├── burnout_distribution.png
│       ├── sleep_vs_burnout.png
│       ├── stress_vs_burnout.png
│       ├── screen_vs_burnout.png
│       ├── correlation_heatmap.png
│       ├── risk_pie_chart.png
│       └── study_hours_boxplot.png
│
├── templates/
│   ├── index.html                    # Home dashboard
│   ├── dashboard.html                # Analytics dashboard
│   └── predict.html                  # Risk calculator
│
└── reports/
    └── analysis_report.txt           # Generated analysis report
```

## ⚙️ Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Steps

1. **Navigate to the backend directory:**
   ```bash
   cd academic_burnout_detection/backend
   ```

2. **Install required packages:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```bash
   python app.py
   ```

4. **Open in browser:**
   ```
   http://localhost:5000
   ```

## 🚀 Usage

### Home Dashboard
- View project overview
- See dataset summary statistics
- Key statistical metrics
- Quick links to calculator and graphs

### Analytics Dashboard
- Explore distribution histograms
- View scatter plots with trend lines
- Analyze correlation heatmap
- See risk category distribution
- Understand key statistical findings

### Risk Calculator
- Enter personal lifestyle data
- Adjust values using sliders
- Get instant burnout score
- View risk category
- See burnout probability
- Receive personalized recommendations

## 📊 Burnout Score Formula

```
BurnoutScore = 0.35 × stress_level 
              + 0.25 × screen_time 
              + 0.20 × study_hours 
              - 0.30 × sleep_hours 
              - 0.05 × physical_activity 
              + 0.05 × assignment_load
```

**Normalized to 0-10 scale** using:
- Min-max normalization
- Low Risk: 0-4
- Moderate Risk: 4-7
- High Risk: 7-10

## 📈 Statistical Methods

### 1. Descriptive Statistics
- Mean: Average value across all students
- Median: Middle value when sorted
- Variance: Measure of data spread
- Standard Deviation: Square root of variance

### 2. Correlation Analysis
- Pearson correlation coefficient
- Identifies relationships between variables
- Range: -1 (negative) to +1 (positive)
- Quantifies strength of burnout indicators

### 3. Linear Regression
- Multiple linear regression model
- Formula: `Burnout = a + b₁×sleep + b₂×study + b₃×screen + b₄×stress`
- Uses Normal Equation method: `β = (X^T X)^-1 X^T y`
- Provides R² value (model quality)

### 4. Risk Assessment
- Burnout probability using normal distribution
- Threshold-based categorization
- Rule-based recommendation engine

## 🔗 API Endpoints

All endpoints return JSON responses with `success` flag and `data` object.

### GET /api/statistics
Returns descriptive statistics for all variables.

**Response:**
```json
{
  "success": true,
  "data": {
    "sleep_hours": {
      "mean": 6.5,
      "median": 6.5,
      "variance": 1.2,
      "std_dev": 1.1,
      ...
    }
  }
}
```

### GET /api/correlation
Returns correlation matrix and burnout indicators.

**Response:**
```json
{
  "success": true,
  "data": {
    "correlation_matrix": {...},
    "burnout_indicators": {
      "stress_level": 0.8,
      "screen_time": 0.65,
      ...
    }
  }
}
```

### GET /api/regression
Returns regression coefficients and equation.

**Response:**
```json
{
  "success": true,
  "data": {
    "intercept": 2.5,
    "sleep_hours_coeff": -0.3,
    "study_hours_coeff": 0.2,
    "screen_time_coeff": 0.25,
    "stress_level_coeff": 0.35,
    "r_squared": 0.78,
    "equation": "Burnout = 2.5 + (-0.3)*sleep + ..."
  }
}
```

### GET /api/graphs
Returns list of available graph filenames.

**Response:**
```json
{
  "success": true,
  "data": {
    "histogram": [...],
    "scatter": [...],
    "heatmap": [...],
    "other": [...]
  }
}
```

### POST /api/burnout_predict
Predicts burnout risk for individual student.

**Request Body:**
```json
{
  "sleep_hours": 6.5,
  "study_hours": 5.5,
  "screen_time": 7.0,
  "stress_level": 6.0,
  "physical_activity": 4.0,
  "assignment_load": 6.0
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "burnout_score": 5.2,
    "risk_category": "Moderate Risk",
    "burnout_probability": 32.5,
    "recommendations": [
      {
        "category": "Sleep",
        "message": "Increase sleep to 7-8 hours",
        "impact": "Improving sleep quality is crucial..."
      }
    ]
  }
}
```

### GET /api/dataset_summary
Returns overview of the dataset.

### GET /api/report
Returns complete analysis report.

## 📊 Dataset Information

The dataset contains 200+ student records with:
- **sleep_hours**: 4.3 - 7.6 hours
- **study_hours**: 3.5 - 8.9 hours
- **screen_time**: 4.8 - 9.8 hours
- **stress_level**: 2.5 - 8.7 / 10
- **physical_activity**: 1.2 - 6.5 / 10
- **assignment_load**: 2 - 9 / 10

## 🔍 Key Insights

1. **Sleep Impact**: Students with <5 hours sleep have 60% higher burnout risk
2. **Stress Correlation**: Stress level is the strongest burnout predictor
3. **Screen Time Effect**: >8 hours daily increases burnout significantly
4. **Physical Activity**: Protective factor with negative correlation to burnout
5. **Assignment Load**: Direct relationship with burnout scores

## 📝 Generated Outputs

- **Analysis Report**: Comprehensive statistical analysis saved to `reports/analysis_report.txt`, now with an expanded "Burnout Risk Analysis" section including risk counts and observations.
- **Graphs**: Over a dozen visualizations saved to `static/graphs/` and `static/graphs/risk_analysis/`. New risk-level charts include:
  - Risk distribution bar chart (`risk_bar_chart.png`)
  - Risk distribution pie chart (`risk_pie_chart.png`)
  - Burnout score histogram (`burnout_histogram.png`)
  - Optional advanced charts (trend, department comparison, lifestyle impact) when data is available.
- **Statistics**: JSON data available via API endpoints

## 🛠️ Technologies Used

**Backend:**
- Flask 2.3.3 - Web framework
- Pandas 2.0.3 - Data manipulation
- NumPy 1.24.3 - Numerical computing
- Matplotlib 3.7.2 - Graph generation
- Seaborn 0.12.2 - Statistical visualization
- SciPy 1.11.2 - Scientific computing

**Frontend:**
- HTML5 - Structure
- CSS3 - Styling
- JavaScript (Vanilla) - Interactivity

## ⚠️ Important Notes

- **No Machine Learning**: This system uses ONLY statistical methods
- **Educational Purpose**: For research and educational analysis
- **Data Privacy**: Handle student data responsibly
- **Limitations**: Statistical models have inherent limitations

## 🤝 Contributing

This is an educational project. For improvements or extensions, please ensure:
- No ML algorithms are used
- Only statistical methods are implemented
- Code is well-documented
- Statistical methods are properly explained

## 📄 License

This project is provided as-is for educational purposes.


