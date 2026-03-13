# 🚀 Quick Start Guide

## **Run the Application**

```bash
cd backend
pip install -r requirements.txt  # Install all dependencies
python app.py                     # Start Flask server
```

## **Access Dashboard**

📍 Open browser: **http://127.0.0.1:5000**

---

## **10 FEATURES AT A GLANCE**

| # | Feature | Location | Status |
|---|---------|----------|--------|
| 1️⃣ | Burnout Score Calculation | `src/burnout_model.py` | ✅ 0.25×stress + 0.20×screen + 0.20×study + 0.15×load - 0.10×sleep - 0.10×activity |
| 2️⃣ | Risk Classification | `src/burnout_model.py` | ✅ Low(0-4) / Moderate(4-7) / High(7-10) |
| 3️⃣ | Risk Graphs | `src/risk_level_analysis.py` | ✅ Bar, Pie, Histogram, Dept charts |
| 4️⃣ | Burnout Indicators | `/api/correlation_indicators` | ✅ Ranked by correlation strength |
| 5️⃣ | Dashboard | `templates/dashboard.html` | ✅ Complete redesign with stats, graphs, cards |
| 6️⃣ | PDF Reports | `src/pdf_generator.py` | ✅ Professional 8-section reports |
| 7️⃣ | Download Button | `/api/download-report` | ✅ Click to download PDF |
| 8️⃣ | Project Structure | `backend/` folder | ✅ Clean, organized, modular |
| 9️⃣ | Graph Auto-Render | `dashboard.html` (JavaScript) | ✅ Cache-busting, error handling |
| 🔟 | Modern Dashboard UI | `static/css/style.css` | ✅ Responsive, animated, professional |

---

## **KEY FILES MODIFIED**

### **Backend**
- ✅ `app.py` - Added PDF download & indicators endpoints
- ✅ `src/burnout_model.py` - Updated formula
- ✅ `src/pdf_generator.py` - **NEW** PDF generation module
- ✅ `requirements.txt` - Added reportlab

### **Frontend**
- ✅ `templates/dashboard.html` - Redesigned with new sections
- ✅ `static/css/style.css` - Added 400+ lines for new components

---

## **NEW API ENDPOINTS**

### 1. Get Burnout Indicators
```
GET /api/correlation_indicators
```
**Returns**: Sorted list of burnout predictors with correlation values

**Example Response**:
```json
{
  "success": true,
  "data": [
    {"factor": "Stress Level", "correlation": 0.87, "direction": "↑", "description": "Increases burnout risk"},
    {"factor": "Sleep Hours", "correlation": -0.62, "direction": "↓", "description": "Decreases burnout risk"}
  ]
}
```

### 2. Download PDF Report
```
GET /api/download-report
```
**Returns**: Professional PDF file with 8 sections

**Contains**:
- Dataset summary
- Risk distribution
- Burnout indicators
- Risk explanations
- Embedded graphs
- Observations
- Recommendations

---

## **DASHBOARD SECTIONS**

### 📊 **Section 1: Statistics Cards**
- Total students
- Average burnout score
- High-risk percentage
- Average stress level

### 🔴 **Section 2: Risk Distribution Graphs**
- Pie chart (percentages)
- Bar chart (counts)
- Burnout histogram
- Correlation heatmap

### 🎯 **Section 3: Strongest Indicators**
- Ranked by correlation
- Color-coded directions (↑↓)
- Descriptions

### 📋 **Section 4: Risk Categories**
- 3 styled cards (Low/Moderate/High)
- Characteristics
- Recommendations

### 📄 **Section 5: Download Button**
- One-click PDF generation
- Status updates
- Auto-download

---

## **SAMPLE WORKFLOWS**

### **Workflow 1: View Dashboard**
1. Start app: `python app.py`
2. Open: `http://127.0.0.1:5000/dashboard`
3. Scroll through all sections
4. View graphs automatically render

### **Workflow 2: Download Report**
1. Scroll to "Download Report" section
2. Click blue "📥 Download Burnout Report (PDF)" button
3. Wait for "Generating PDF..." message
4. File downloads automatically
5. View report in your default PDF reader

### **Workflow 3: Predict Individual Risk**
1. Navigate to: `http://127.0.0.1:5000/predict`
2. Adjust sliders for student:
   - Sleep hours (0-12)
   - Study hours (0-12)
   - Screen time (0-14)
   - Stress level (0-10)
   - Physical activity (0-10)
   - Assignment load (0-10)
3. Get instant burnout score (0-10)
4. View risk category (Low/Moderate/High)
5. See personalized recommendations

---

## **TECHNICAL DETAILS**

### **Burnout Formula** (0-10 scale)
```python
burnout_raw = (
    0.25 * stress_level +
    0.20 * screen_time +
    0.20 * study_hours +
    0.15 * assignment_load -
    0.10 * sleep_hours -
    0.10 * physical_activity
)
# Normalized to 0-10 range
burnout_score = normalize(burnout_raw)
```

### **Risk Classification**
```python
if burnout_score < 4:
    return "Low Risk"           # 🟢
elif burnout_score < 7:
    return "Moderate Risk"      # 🟡
else:
    return "High Risk"          # 🔴
```

### **Generated Files**
- **Graphs**: `static/graphs/risk_analysis/*.png`
- **PDF Reports**: `reports/burnout_report.pdf`
- **Text Reports**: `reports/analysis_report.txt`

---

## **DEPENDENCIES**

**Required** (all installed):
- Flask >= 2.3.0
- pandas >= 2.0.0
- numpy >= 1.24.0
- matplotlib >= 3.7.0
- seaborn >= 0.12.0
- scipy >= 1.11.0
- **reportlab >= 4.0.0** (for PDF) ✨ **NEW**

---

## **TROUBLESHOOTING**

### App won't start?
```bash
cd backend
pip install -r requirements.txt --upgrade
python app.py
```

### PDF button not working?
- Check if reportlab is installed: `pip list | grep reportlab`
- Install if missing: `pip install reportlab`
- Check browser console for errors (F12)

### Graphs not showing?
- Refresh page (Ctrl+F5)
- Check if `static/graphs/` folder exists
- Verify graphs were generated in startup output

### API endpoints return errors?
- Check Flask server logs for error messages
- Ensure all modules are in `src/` folder
- Verify Python paths are correct

---

## **PERFORMANCE NOTES**

✅ **Startup Time**: ~15-20 seconds (generating all graphs)
✅ **Dashboard Load**: <1 second
✅ **PDF Generation**: ~5-10 seconds
✅ **Predictor Response**: <100ms

---

## **FILE STRUCTURE**

```
backend/
├── app.py                          # Main Flask app
├── requirements.txt                # Dependencies
├── data/
│   └── student_data.csv (156 students)
├── src/
│   ├── burnout_model.py           # ✅ UPDATED
│   ├── pdf_generator.py           # ✅ NEW
│   ├── risk_level_analysis.py
│   ├── data_cleaning.py
│   ├── statistical_analysis.py
│   ├── correlation_analysis.py
│   ├── regression_model.py
│   ├── data_visualization.py
│   ├── report_generator.py
│   └── input_graph_generator.py
├── static/
│   ├── css/style.css              # ✅ ENHANCED
│   ├── js/script.js
│   └── graphs/ (generated)
├── templates/
│   ├── dashboard.html             # ✅ REDESIGNED
│   ├── index.html
│   └── predict.html
└── reports/ (generated)
```

---

## **TESTING THE SYSTEM**

### Quick Test:
```bash
# Terminal 1: Start server
cd backend && python app.py

# Terminal 2: Test endpoints
curl http://localhost:5000/api/correlation_indicators
curl http://localhost:5000/api/download-report -o test_report.pdf
```

### Browser Test:
1. Visit: `http://127.0.0.1:5000`
2. Click "Dashboard" tab
3. Scroll through all sections
4. Click "Download Report" button
5. Verify PDF downloads

---

## **KEY IMPROVEMENTS SUMMARY**

| Before | After |
|--------|-------|
| Simple formula | ✅ Weighted statistical formula |
| Basic graphs | ✅ 4+ professional risk graphs |
| No indicators | ✅ Ranked correlation indicators |
| Old dashboard | ✅ Modern, responsive dashboard |
| No PDF | ✅ Professional 8-section PDFs |
| Manual setup | ✅ Auto-generate on startup |
| Basic styling | ✅ Modern CSS animations & gradients |

---

## **SUPPORT & DOCUMENTATION**

📖 **Full Details**: See `IMPROVEMENT_REPORT.md` for comprehensive feature documentation

🎯 **Questions?** Check error messages or verify:
- All files in correct directories
- All dependencies installed
- Flask server running on port 5000
- Browser cache cleared (Ctrl+F5)

---

## **SUCCESS CHECKLIST**

✅ Python 3.8+
✅ Flask installed
✅ ReportLab installed (`pip install reportlab`)
✅ All files in backend/src/
✅ Data file exists (backend/data/student_data.csv)
✅ Port 5000 available
✅ Graphs directory exists (backend/static/graphs/)

---

**🚀 Ready to go!** Start with:
```bash
cd backend && python app.py
```

Then visit: **http://127.0.0.1:5000** 🎓

