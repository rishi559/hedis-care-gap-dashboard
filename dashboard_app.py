import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import numpy as np

# Page configuration
st.set_page_config(
    page_title="HEDIS Care Gap Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Force light theme
st.markdown("""
    <style>
    /* Force light background */
    .main {
        background-color: #ffffff;
    }
    [data-testid="stAppViewContainer"] {
        background-color: #ffffff;
    }
    [data-testid="stHeader"] {
        background-color: #ffffff;
    }
    [data-testid="stSidebar"] {
        background-color: #f8f9fa;
    }
    </style>
    """, unsafe_allow_html=True)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main {
        padding: 0rem 1rem;
        background-color: #ffffff !important;
    }
    .stMetric {
        background-color: #f0f4f8;
        padding: 15px;
        border-radius: 10px;
        border-left: 4px solid #3b82f6;
    }
    .stMetric label {
        color: #1f2937 !important;
        font-weight: 600;
    }
    .stMetric [data-testid="stMetricValue"] {
        color: #111827 !important;
        font-size: 2rem !important;
    }
    .stMetric [data-testid="stMetricDelta"] {
        color: #059669 !important;
    }
    h1 {
        color: #1e3a8a !important;
        padding-bottom: 10px;
        border-bottom: 3px solid #3b82f6;
    }
    h2, h3 {
        color: #1f2937 !important;
        margin-top: 20px;
    }
    p, span, div {
        color: #374151 !important;
    }
    .highlight-green {
        color: #10b981;
        font-weight: bold;
    }
    .highlight-red {
        color: #ef4444;
        font-weight: bold;
    }
    .highlight-yellow {
        color: #f59e0b;
        font-weight: bold;
    }
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background-color: #f8f9fa !important;
    }
    [data-testid="stSidebar"] * {
        color: #1f2937 !important;
    }
    /* Make sure text is visible */
    .stMarkdown {
        color: #1f2937 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# Load data
@st.cache_data
def load_data():
    care_gaps = pd.read_csv('hedis_care_gaps.csv')
    monthly_trends = pd.read_csv('monthly_trends.csv')
    site_performance = pd.read_csv('site_performance.csv')
    provider_performance = pd.read_csv('provider_performance.csv')
    payer_performance = pd.read_csv('payer_performance.csv')
    measure_performance = pd.read_csv('measure_performance.csv')
    
    # Convert dates
    care_gaps['Open_Date'] = pd.to_datetime(care_gaps['Open_Date'])
    care_gaps['Closed_Date'] = pd.to_datetime(care_gaps['Closed_Date'])
    
    return care_gaps, monthly_trends, site_performance, provider_performance, payer_performance, measure_performance

# Load all datasets
care_gaps, monthly_trends, site_performance, provider_performance, payer_performance, measure_performance = load_data()

# Title and header
st.title("📊 HEDIS Care Gap Closure Dashboard")
st.markdown("**Q4 2024 Performance Overview** | Last Updated: January 9, 2025")
st.markdown("---")

# Sidebar filters
st.sidebar.header("🔍 Filters")
selected_sites = st.sidebar.multiselect(
    "Select Sites",
    options=care_gaps['Site_Location'].unique(),
    default=care_gaps['Site_Location'].unique()
)

selected_payers = st.sidebar.multiselect(
    "Select Payer Types",
    options=care_gaps['Payer_Type'].unique(),
    default=care_gaps['Payer_Type'].unique()
)

selected_measures = st.sidebar.multiselect(
    "Select Measures",
    options=care_gaps['Measure_Category'].unique(),
    default=care_gaps['Measure_Category'].unique()
)

# Filter data
filtered_gaps = care_gaps[
    (care_gaps['Site_Location'].isin(selected_sites)) &
    (care_gaps['Payer_Type'].isin(selected_payers)) &
    (care_gaps['Measure_Category'].isin(selected_measures))
]

# Calculate KPIs
total_gaps = len(filtered_gaps)
open_gaps = len(filtered_gaps[filtered_gaps['Gap_Status'] == 'Open'])
closed_gaps = len(filtered_gaps[filtered_gaps['Gap_Status'] == 'Closed'])
closure_rate = (closed_gaps / total_gaps * 100) if total_gaps > 0 else 0
current_compliance = monthly_trends.iloc[-1]['Compliance_Rate']
target_rate = 85.0
monthly_change = monthly_trends.iloc[-1]['Compliance_Rate'] - monthly_trends.iloc[-2]['Compliance_Rate']

# KPI Section
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="📋 Open Gaps",
        value=f"{open_gaps}",
        delta=f"{open_gaps - closed_gaps} vs closed",
        delta_color="inverse"
    )

with col2:
    st.metric(
        label="✅ Closure Rate",
        value=f"{closure_rate:.1f}%",
        delta=f"+1.3% vs last month"
    )

with col3:
    st.metric(
        label="🎯 Compliance Rate",
        value=f"{current_compliance:.1f}%",
        delta=f"{current_compliance - target_rate:+.1f}% vs target"
    )

with col4:
    st.metric(
        label="📈 Monthly Change",
        value=f"{monthly_change:+.1f}%",
        delta="Above trajectory" if monthly_change > 0 else "Below trajectory"
    )

st.markdown("---")

# Row 1: Monthly Trend (full width)
st.subheader("📈 Monthly Compliance Trend (2024-2025)")

fig_trend = go.Figure()

# Add compliance rate line
fig_trend.add_trace(go.Scatter(
    x=monthly_trends['Month_Year'],
    y=monthly_trends['Compliance_Rate'],
    mode='lines+markers',
    name='Compliance Rate',
    line=dict(color='#3b82f6', width=3),
    marker=dict(size=8),
    fill='tozeroy',
    fillcolor='rgba(59, 130, 246, 0.1)'
))

# Add target line
fig_trend.add_trace(go.Scatter(
    x=monthly_trends['Month_Year'],
    y=[target_rate] * len(monthly_trends),
    mode='lines',
    name='Target (85%)',
    line=dict(color='#ef4444', width=2, dash='dash')
))

fig_trend.update_layout(
    height=400,
    xaxis_title="Month",
    yaxis_title="Compliance Rate (%)",
    hovermode='x unified',
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    plot_bgcolor='white',
    yaxis=dict(gridcolor='#e5e7eb', range=[70, 95])
)

st.plotly_chart(fig_trend, use_container_width=True)

st.markdown("---")

# Row 2: Site Performance and Provider Performance
col1, col2 = st.columns(2)

with col1:
    st.subheader("🏥 Site Performance Comparison")
    
    # Sort by compliance rate
    site_sorted = site_performance.sort_values('Compliance_Rate', ascending=True)
    
    # Color coding
    colors = ['#10b981' if x >= target_rate else '#ef4444' if x < 83 else '#f59e0b' 
              for x in site_sorted['Compliance_Rate']]
    
    fig_site = go.Figure(go.Bar(
        x=site_sorted['Compliance_Rate'],
        y=site_sorted['Site_Location'],
        orientation='h',
        marker=dict(color=colors),
        text=site_sorted['Compliance_Rate'].apply(lambda x: f'{x:.1f}%'),
        textposition='outside',
        hovertemplate='<b>%{y}</b><br>Compliance: %{x:.1f}%<br>Open Gaps: %{customdata[0]}<extra></extra>',
        customdata=site_sorted[['Open_Gaps']]
    ))
    
    fig_site.add_vline(x=target_rate, line_dash="dash", line_color="#ef4444", 
                       annotation_text="Target", annotation_position="top right")
    
    fig_site.update_layout(
        height=350,
        xaxis_title="Compliance Rate (%)",
        yaxis_title="",
        showlegend=False,
        plot_bgcolor='white',
        xaxis=dict(gridcolor='#e5e7eb', range=[80, 90])
    )
    
    st.plotly_chart(fig_site, use_container_width=True)

with col2:
    st.subheader("👨‍⚕️ Provider Performance Rankings")
    
    # Sort by closure rate
    provider_sorted = provider_performance.sort_values('Closure_Rate', ascending=True)
    
    # Color coding
    colors_provider = ['#10b981' if x >= 70 else '#ef4444' if x < 65 else '#f59e0b' 
                       for x in provider_sorted['Closure_Rate']]
    
    fig_provider = go.Figure(go.Bar(
        x=provider_sorted['Closure_Rate'],
        y=provider_sorted['Provider_Name'],
        orientation='h',
        marker=dict(color=colors_provider),
        text=provider_sorted['Closure_Rate'].apply(lambda x: f'{x:.1f}%'),
        textposition='outside',
        hovertemplate='<b>%{y}</b><br>Closure Rate: %{x:.1f}%<br>Avg Days: %{customdata[0]:.0f}<extra></extra>',
        customdata=provider_sorted[['Avg_Days_to_Close']]
    ))
    
    fig_provider.update_layout(
        height=350,
        xaxis_title="Closure Rate (%)",
        yaxis_title="",
        showlegend=False,
        plot_bgcolor='white',
        xaxis=dict(gridcolor='#e5e7eb', range=[55, 80])
    )
    
    st.plotly_chart(fig_provider, use_container_width=True)

st.markdown("---")

# Row 3: Measure Performance and Payer Breakdown
col1, col2 = st.columns(2)

with col1:
    st.subheader("🎯 HEDIS Measure Performance")
    
    # Create bubble chart
    fig_measure = px.scatter(
        measure_performance,
        x='Compliance_Rate',
        y='Closure_Rate',
        size='Total_Gaps',
        color='Closure_Rate',
        hover_name='Measure_Name',
        hover_data={'Compliance_Rate': ':.1f', 'Closure_Rate': ':.1f', 'Total_Gaps': True},
        color_continuous_scale=['#ef4444', '#f59e0b', '#10b981'],
        size_max=60
    )
    
    fig_measure.update_layout(
        height=350,
        xaxis_title="Compliance Rate (%)",
        yaxis_title="Closure Rate (%)",
        coloraxis_colorbar=dict(title="Closure<br>Rate (%)"),
        plot_bgcolor='white',
        xaxis=dict(gridcolor='#e5e7eb'),
        yaxis=dict(gridcolor='#e5e7eb')
    )
    
    st.plotly_chart(fig_measure, use_container_width=True)

with col2:
    st.subheader("💳 Payer Performance Breakdown")
    
    # Create grouped bar chart
    fig_payer = go.Figure()
    
    fig_payer.add_trace(go.Bar(
        name='Compliance Rate',
        x=payer_performance['Payer_Type'],
        y=payer_performance['Compliance_Rate'],
        marker_color='#3b82f6',
        text=payer_performance['Compliance_Rate'].apply(lambda x: f'{x:.1f}%'),
        textposition='outside'
    ))
    
    fig_payer.add_trace(go.Bar(
        name='Closure Rate',
        x=payer_performance['Payer_Type'],
        y=payer_performance['Closure_Rate'],
        marker_color='#10b981',
        text=payer_performance['Closure_Rate'].apply(lambda x: f'{x:.1f}%'),
        textposition='outside'
    ))
    
    fig_payer.add_hline(y=target_rate, line_dash="dash", line_color="#ef4444",
                        annotation_text="Target", annotation_position="right")
    
    fig_payer.update_layout(
        height=350,
        barmode='group',
        yaxis_title="Rate (%)",
        xaxis_title="",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        plot_bgcolor='white',
        yaxis=dict(gridcolor='#e5e7eb', range=[0, 100])
    )
    
    st.plotly_chart(fig_payer, use_container_width=True)

st.markdown("---")

# Row 4: Gap Status Distribution and Detailed Table
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("📊 Gap Status Distribution")
    
    status_counts = filtered_gaps['Gap_Status'].value_counts()
    
    fig_pie = go.Figure(data=[go.Pie(
        labels=status_counts.index,
        values=status_counts.values,
        hole=0.4,
        marker=dict(colors=['#10b981', '#ef4444']),
        textinfo='label+percent',
        textfont_size=14
    )])
    
    fig_pie.update_layout(
        height=300,
        showlegend=True,
        legend=dict(orientation="v", yanchor="middle", y=0.5)
    )
    
    st.plotly_chart(fig_pie, use_container_width=True)
    
    # Summary stats
    st.markdown(f"""
    **Summary:**
    - Total Gaps: **{total_gaps}**
    - Closed: **{closed_gaps}** ({closed_gaps/total_gaps*100:.1f}%)
    - Open: **{open_gaps}** ({open_gaps/total_gaps*100:.1f}%)
    """)

with col2:
    st.subheader("📋 Recent Gap Details")
    
    # Show recent gaps
    display_gaps = filtered_gaps.sort_values('Open_Date', ascending=False).head(10)
    
    display_df = display_gaps[[
        'Gap_ID', 'Measure_Name', 'Gap_Status', 
        'Site_Location', 'Provider_Name', 'Days_Open'
    ]].copy()
    
    st.dataframe(
        display_df,
        use_container_width=True,
        height=300,
        hide_index=True
    )

st.markdown("---")

# Footer with insights
st.subheader("💡 Key Insights")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    **📈 Positive Trends:**
    - Compliance improved 16.8% YoY
    - Above 85% target for 2 months
    - 4 of 8 measures >80% closure
    """)

with col2:
    st.markdown("""
    **⚠️ Areas of Focus:**
    - Eastside Medical below target
    - Medicaid payer at risk
    - Statin adherence only 50%
    """)

with col3:
    st.markdown("""
    **🎯 Recommendations:**
    - Deploy best practices to Eastside
    - Medicaid outreach campaign
    - Medication adherence program
    """)

# Sidebar additional info
st.sidebar.markdown("---")
st.sidebar.markdown("### 📊 Dashboard Info")
st.sidebar.info("""
**Data Sources:**
- HEDIS Quality Measures
- EHR System Integration
- Payer Quality Reports

**Refresh Frequency:**
- Daily updates
- Real-time gap tracking
""")

st.sidebar.markdown("### 👤 Created By")
st.sidebar.markdown("Clinical Data Analyst Candidate")
st.sidebar.markdown("Interview Demonstration")
