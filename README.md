# HEDIS Care Gap Closure Dashboard

An interactive Streamlit dashboard for tracking and analyzing HEDIS care gap closure performance across multiple sites, providers, and payer types.

## 🚀 Quick Start

### Local Setup

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Run the dashboard:**
```bash
streamlit run dashboard_app.py
```

3. **View in browser:**
   - Automatically opens at `http://localhost:8501`

## 📁 Files Included

- `dashboard_app.py` - Main Streamlit application
- `requirements.txt` - Python dependencies
- `hedis_care_gaps.csv` - Individual care gap records (80 entries)
- `monthly_trends.csv` - 13 months of trend data
- `site_performance.csv` - 4 clinic locations
- `provider_performance.csv` - 5 provider rankings
- `payer_performance.csv` - 3 payer types breakdown
- `measure_performance.csv` - 8 HEDIS measures

## 📊 Dashboard Features

### Interactive Filters
- **Site Selection** - Filter by clinic location
- **Payer Type** - Medicare Advantage, Commercial, Medicaid
- **Measure Category** - Diabetes, Preventive, Chronic Disease, Medication

### Key Visualizations
1. **KPI Cards** - Real-time metrics (Open Gaps, Closure Rate, Compliance, Monthly Change)
2. **Monthly Trend Chart** - 13-month compliance trajectory with target line
3. **Site Performance** - Horizontal bar chart comparing 4 locations
4. **Provider Rankings** - Performance comparison across 5 providers
5. **Measure Performance** - Bubble chart showing 8 HEDIS measures
6. **Payer Breakdown** - Grouped bar chart by payer type
7. **Gap Status Distribution** - Pie chart of open vs closed gaps
8. **Recent Gap Details** - Searchable/sortable table

### Key Insights Section
- Positive trends identified
- Areas requiring focus
- Actionable recommendations

## 🌐 Deploy to Streamlit Cloud (Free!)

### Option 1: Streamlit Community Cloud

1. **Create GitHub repository:**
   - Upload all CSV files and Python files
   - Make repository public

2. **Deploy to Streamlit Cloud:**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Sign in with GitHub
   - Click "New app"
   - Select your repository
   - Main file: `dashboard_app.py`
   - Click "Deploy"

3. **Share your live link!**
   - You'll get a URL like: `https://yourname-dashboard.streamlit.app`
   - Share this in your interview!

### Option 2: Local Demo

1. Run locally during interview
2. Share screen to show interactivity
3. Walk through filters and visualizations

## 💡 Interview Tips

### Talking Points:

**Technical Skills Demonstrated:**
- Python programming (Pandas, Plotly)
- Data visualization best practices
- Interactive dashboard development
- Healthcare data analysis

**HEDIS Knowledge Shown:**
- Understanding of quality measures
- Compliance tracking
- Gap closure methodology
- Payer performance metrics

**Business Value:**
- Executive-level KPIs
- Actionable insights highlighted
- Performance trending
- Site/provider comparisons for improvement

### Demo Flow:

1. **Start with Overview** - "This dashboard tracks HEDIS care gap closure across 4 sites..."
2. **Show KPIs** - "We're at 89.3% compliance, above our 85% target..."
3. **Highlight Trend** - "We've improved 16.8% year-over-year..."
4. **Use Filters** - "I can drill down by site, payer, or measure..."
5. **Point Out Insights** - "Notice Medicaid is at risk, and Eastside Medical needs support..."
6. **Discuss Actions** - "I'd recommend deploying Downtown Clinic's best practices..."

### Questions You Might Get:

**Q: How would you use this in the field?**
A: "During site visits, I'd use the filters to show providers their specific performance, identify gaps, and provide targeted feedback."

**Q: What would you add to this?**
A: "I'd add drill-through to patient-level details, predictive analytics for gap closure timing, and automated alerts for high-priority cases."

**Q: How do you handle data quality issues?**
A: "I'd implement validation checks for dates, ensure complete measure mappings, and flag outliers for review."

## 📈 Data Summary

- **Total Gaps:** 80 records
- **Time Period:** January 2024 - January 2025
- **Sites:** 4 clinic locations
- **Providers:** 5 physicians
- **Payers:** Medicare Advantage, Commercial, Medicaid
- **Measures:** 8 HEDIS quality measures

## 🎯 Key Performance Indicators

- **Current Compliance:** 89.3% (Target: 85%)
- **Overall Closure Rate:** 63.8%
- **Best Performing Site:** Downtown Clinic (87.5%)
- **Opportunity Area:** Statin Adherence (50% closure)

## 📞 Support

For questions about this dashboard:
- Review the code comments in `dashboard_app.py`
- Check Streamlit documentation: [docs.streamlit.io](https://docs.streamlit.io)
- Plotly charts: [plotly.com/python](https://plotly.com/python)

---

**Good luck with your interview! 🎉**
