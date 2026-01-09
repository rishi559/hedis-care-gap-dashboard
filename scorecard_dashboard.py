import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Page configuration
st.set_page_config(
    page_title="Provider Performance Scorecard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        background-color: #ffffff !important;
    }
    .stMetric {
        background-color: #f0f4f8;
        padding: 15px;
        border-radius: 10px;
    }
    h1 {
        color: #1e3a8a !important;
        border-bottom: 3px solid #3b82f6;
        padding-bottom: 10px;
    }
    h2, h3 {
        color: #1f2937 !important;
    }
    .metric-card {
        background-color: #f8f9fa;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #3b82f6;
        margin: 10px 0;
    }
    </style>
    """, unsafe_allow_html=True)

# Load data
@st.cache_data
def load_data():
    providers = pd.read_csv('provider_scorecard_main.csv')
    metrics = pd.read_csv('scorecard_metrics.csv')
    trends = pd.read_csv('provider_trends.csv')
    return providers, metrics, trends

providers_df, metrics_df, trends_df = load_data()

# Helper functions
def get_status_color(value, target, good_threshold, warning_threshold, lower_is_better=False):
    """Determine status color based on thresholds"""
    if lower_is_better:
        if value <= good_threshold:
            return 'green', '🟢'
        elif value <= warning_threshold:
            return 'yellow', '🟡'
        else:
            return 'red', '🔴'
    else:
        if value >= good_threshold:
            return 'green', '🟢'
        elif value >= warning_threshold:
            return 'yellow', '🟡'
        else:
            return 'red', '🔴'

def get_rank_suffix(rank):
    """Get ordinal suffix for ranking"""
    if 10 <= rank % 100 <= 20:
        suffix = 'th'
    else:
        suffix = {1: 'st', 2: 'nd', 3: 'rd'}.get(rank % 10, 'th')
    return f"{rank}{suffix}"

def calculate_trend(df, provider, metric):
    """Calculate trend direction for a provider and metric"""
    provider_data = df[df['Provider_Name'] == provider].sort_values('Month')
    if len(provider_data) < 2:
        return '→'
    
    recent = provider_data[metric].iloc[-1]
    previous = provider_data[metric].iloc[-2]
    
    if recent > previous * 1.01:  # More than 1% improvement
        return '↑'
    elif recent < previous * 0.99:  # More than 1% decline
        return '↓'
    else:
        return '→'

# Title
st.title("📊 Provider Performance Scorecard")
st.markdown("**Q4 2024 - January 2025** | Comprehensive Quality & Productivity Metrics")
st.markdown("---")

# Sidebar
st.sidebar.header("🔍 Filters & Options")
selected_provider = st.sidebar.selectbox(
    "Select Provider for Detailed View",
    options=['All Providers'] + list(providers_df['Provider_Name'].unique())
)

selected_category = st.sidebar.multiselect(
    "Filter by Metric Category",
    options=['All'] + list(metrics_df['Category'].unique()),
    default=['All']
)

show_trends = st.sidebar.checkbox("Show Trend Indicators", value=True)
show_rankings = st.sidebar.checkbox("Show Provider Rankings", value=True)

# Overview Section
st.header("📈 Executive Summary")

col1, col2, col3, col4 = st.columns(4)

with col1:
    avg_overall = providers_df['Overall_Score'].mean()
    st.metric(
        label="Average Overall Score",
        value=f"{avg_overall:.1f}%",
        delta="+2.3% vs last quarter"
    )

with col2:
    top_performer = providers_df.nlargest(1, 'Overall_Score')['Provider_Name'].values[0]
    top_score = providers_df.nlargest(1, 'Overall_Score')['Overall_Score'].values[0]
    st.metric(
        label="Top Performer",
        value=top_performer.split()[-1],  # Last name only
        delta=f"{top_score:.1f}%"
    )

with col3:
    providers_above_target = len(providers_df[providers_df['Overall_Score'] >= 85])
    st.metric(
        label="Providers Above Target",
        value=f"{providers_above_target}/5",
        delta=f"{providers_above_target/5*100:.0f}%"
    )

with col4:
    avg_satisfaction = providers_df['Patient_Satisfaction'].mean()
    st.metric(
        label="Avg Patient Satisfaction",
        value=f"{avg_satisfaction:.2f}/5.0",
        delta="+0.2 vs last quarter"
    )

st.markdown("---")

# Main Scorecard View
if selected_provider == 'All Providers':
    st.header("🏆 Provider Performance Scorecard - All Providers")
    
    # Create comprehensive scorecard table
    scorecard_data = []
    
    for idx, provider in providers_df.iterrows():
        provider_name = provider['Provider_Name']
        
        # Get rankings
        providers_sorted = providers_df.sort_values('Overall_Score', ascending=False)
        rank = providers_sorted[providers_sorted['Provider_Name'] == provider_name].index[0] + 1
        
        # Get trends
        hedis_trend = calculate_trend(trends_df, provider_name, 'HEDIS_Compliance_Rate')
        closure_trend = calculate_trend(trends_df, provider_name, 'Gap_Closure_Rate')
        
        # Get status for key metrics
        hedis_status = get_status_color(
            provider['HEDIS_Compliance_Rate'], 
            85, 87, 83
        )
        
        scorecard_data.append({
            'Rank': get_rank_suffix(rank),
            'Provider': provider_name,
            'Specialty': provider['Specialty'],
            'Overall Score': f"{provider['Overall_Score']:.1f}%",
            'Status': hedis_status[1],
            'HEDIS': f"{provider['HEDIS_Compliance_Rate']:.1f}% {hedis_trend}",
            'Gap Closure': f"{provider['Gap_Closure_Rate']:.1f}% {closure_trend}",
            'Pat. Sat.': f"{provider['Patient_Satisfaction']:.1f}/5",
            'Patients': int(provider['Patient_Panel_Size'])
        })
    
    scorecard_table = pd.DataFrame(scorecard_data)
    
    # Display as interactive table
    st.dataframe(
        scorecard_table,
        use_container_width=True,
        hide_index=True,
        height=250
    )
    
    st.markdown("---")
    
    # Detailed Metrics Comparison
    st.subheader("📊 Detailed Metrics Comparison")
    
    # Select metrics to display
    metric_cols = ['HEDIS_Compliance_Rate', 'Gap_Closure_Rate', 'Patient_Satisfaction', 
                   'Documentation_Quality', 'Productivity_Score']
    
    # Create tabs for different views
    tab1, tab2, tab3 = st.tabs(["📊 Bar Chart Comparison", "🎯 Radar Chart", "📈 Trend Analysis"])
    
    with tab1:
        col1, col2 = st.columns(2)
        
        with col1:
            # HEDIS Compliance comparison
            fig_hedis = go.Figure()
            
            providers_sorted = providers_df.sort_values('HEDIS_Compliance_Rate', ascending=True)
            colors = ['#10b981' if x >= 87 else '#f59e0b' if x >= 83 else '#ef4444' 
                     for x in providers_sorted['HEDIS_Compliance_Rate']]
            
            fig_hedis.add_trace(go.Bar(
                y=providers_sorted['Provider_Name'],
                x=providers_sorted['HEDIS_Compliance_Rate'],
                orientation='h',
                marker=dict(color=colors),
                text=providers_sorted['HEDIS_Compliance_Rate'].apply(lambda x: f'{x:.1f}%'),
                textposition='outside'
            ))
            
            fig_hedis.add_vline(x=85, line_dash="dash", line_color="#ef4444", 
                               annotation_text="Target", annotation_position="top right")
            
            fig_hedis.update_layout(
                title="HEDIS Compliance Rate by Provider",
                xaxis_title="Compliance Rate (%)",
                height=350,
                showlegend=False
            )
            
            st.plotly_chart(fig_hedis, use_container_width=True)
        
        with col2:
            # Gap Closure Rate comparison
            fig_closure = go.Figure()
            
            providers_sorted = providers_df.sort_values('Gap_Closure_Rate', ascending=True)
            colors = ['#10b981' if x >= 73 else '#f59e0b' if x >= 67 else '#ef4444' 
                     for x in providers_sorted['Gap_Closure_Rate']]
            
            fig_closure.add_trace(go.Bar(
                y=providers_sorted['Provider_Name'],
                x=providers_sorted['Gap_Closure_Rate'],
                orientation='h',
                marker=dict(color=colors),
                text=providers_sorted['Gap_Closure_Rate'].apply(lambda x: f'{x:.1f}%'),
                textposition='outside'
            ))
            
            fig_closure.add_vline(x=70, line_dash="dash", line_color="#ef4444", 
                                 annotation_text="Target", annotation_position="top right")
            
            fig_closure.update_layout(
                title="Gap Closure Rate by Provider",
                xaxis_title="Closure Rate (%)",
                height=350,
                showlegend=False
            )
            
            st.plotly_chart(fig_closure, use_container_width=True)
    
    with tab2:
        # Radar chart for multi-metric comparison
        st.subheader("Multi-Metric Provider Comparison")
        
        categories = ['HEDIS\nCompliance', 'Gap\nClosure', 'Patient\nSatisfaction', 
                     'Documentation', 'Productivity']
        
        fig_radar = go.Figure()
        
        for idx, provider in providers_df.iterrows():
            values = [
                provider['HEDIS_Compliance_Rate'],
                provider['Gap_Closure_Rate'],
                provider['Patient_Satisfaction'] * 20,  # Scale to 100
                provider['Documentation_Quality'],
                provider['Productivity_Score']
            ]
            
            fig_radar.add_trace(go.Scatterpolar(
                r=values,
                theta=categories,
                fill='toself',
                name=provider['Provider_Name']
            ))
        
        fig_radar.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100]
                )
            ),
            showlegend=True,
            height=500
        )
        
        st.plotly_chart(fig_radar, use_container_width=True)
    
    with tab3:
        # Trend analysis over time
        st.subheader("Performance Trends (Last 4 Months)")
        
        fig_trend = go.Figure()
        
        for provider in trends_df['Provider_Name'].unique():
            provider_data = trends_df[trends_df['Provider_Name'] == provider]
            
            fig_trend.add_trace(go.Scatter(
                x=provider_data['Month'],
                y=provider_data['Overall_Score'],
                mode='lines+markers',
                name=provider,
                line=dict(width=2),
                marker=dict(size=8)
            ))
        
        fig_trend.add_hline(y=85, line_dash="dash", line_color="#ef4444",
                           annotation_text="Target: 85%", annotation_position="right")
        
        fig_trend.update_layout(
            title="Overall Score Trend",
            xaxis_title="Month",
            yaxis_title="Overall Score (%)",
            height=400,
            hovermode='x unified'
        )
        
        st.plotly_chart(fig_trend, use_container_width=True)

else:
    # Individual Provider Detailed View
    provider_data = providers_df[providers_df['Provider_Name'] == selected_provider].iloc[0]
    
    st.header(f"📋 Detailed Scorecard: {selected_provider}")
    
    # Provider info
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Specialty", provider_data['Specialty'])
    with col2:
        st.metric("Experience", f"{int(provider_data['Years_Experience'])} years")
    with col3:
        st.metric("Panel Size", f"{int(provider_data['Patient_Panel_Size'])} patients")
    with col4:
        # Calculate rank
        rank = providers_df.sort_values('Overall_Score', ascending=False).index.tolist().index(
            providers_df[providers_df['Provider_Name'] == selected_provider].index[0]
        ) + 1
        st.metric("Overall Rank", get_rank_suffix(rank) + " of 5")
    
    st.markdown("---")
    
    # Overall Score with gauge
    st.subheader("🎯 Overall Performance Score")
    
    fig_gauge = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=provider_data['Overall_Score'],
        delta={'reference': 85, 'relative': False, 'suffix': ' vs target'},
        title={'text': f"{selected_provider}<br>Overall Score"},
        gauge={
            'axis': {'range': [None, 100]},
            'bar': {'color': "#3b82f6"},
            'steps': [
                {'range': [0, 75], 'color': "#fee2e2"},
                {'range': [75, 85], 'color': "#fef3c7"},
                {'range': [85, 100], 'color': "#d1fae5"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 85
            }
        }
    ))
    
    fig_gauge.update_layout(height=300)
    st.plotly_chart(fig_gauge, use_container_width=True)
    
    st.markdown("---")
    
    # Detailed Metrics Table
    st.subheader("📊 Detailed Metrics Breakdown")
    
    detailed_metrics = []
    
    for _, metric in metrics_df.iterrows():
        metric_name = metric['Metric_Name']
        
        if metric_name in provider_data.index:
            value = provider_data[metric_name]
            target = metric['Target_Value']
            
            # Determine if lower is better
            lower_is_better = metric_name == 'Avg_Days_To_Close'
            
            # Get status
            status_color, status_icon = get_status_color(
                value, target, 
                metric['Good_Threshold'], 
                metric['Warning_Threshold'],
                lower_is_better
            )
            
            # Calculate variance
            if lower_is_better:
                variance = target - value
                variance_str = f"{variance:+.1f} days better" if variance > 0 else f"{abs(variance):.1f} days worse"
            else:
                variance = value - target
                variance_str = f"{variance:+.1f}% vs target"
            
            # Get trend
            if metric_name in trends_df.columns:
                trend = calculate_trend(trends_df, selected_provider, metric_name)
            else:
                trend = '→'
            
            detailed_metrics.append({
                'Category': metric['Category'],
                'Metric': metric['Description'],
                'Current': f"{value:.1f}{'%' if not lower_is_better and metric_name != 'Patient_Satisfaction' else (' days' if lower_is_better else '/5' if 'Satisfaction' in metric_name else '')}",
                'Target': f"{target:.1f}{'%' if not lower_is_better and metric_name != 'Patient_Satisfaction' else (' days' if lower_is_better else '/5' if 'Satisfaction' in metric_name else '')}",
                'Variance': variance_str,
                'Status': status_icon,
                'Trend': trend,
                'Weight': f"{metric['Weight']}%"
            })
    
    metrics_table = pd.DataFrame(detailed_metrics)
    st.dataframe(metrics_table, use_container_width=True, hide_index=True, height=400)
    
    st.markdown("---")
    
    # Individual trend
    st.subheader("📈 4-Month Performance Trend")
    
    provider_trends = trends_df[trends_df['Provider_Name'] == selected_provider]
    
    fig_individual = make_subplots(
        rows=2, cols=2,
        subplot_titles=('Overall Score', 'HEDIS Compliance', 
                       'Gap Closure Rate', 'Patient Satisfaction')
    )
    
    # Overall Score
    fig_individual.add_trace(
        go.Scatter(x=provider_trends['Month'], y=provider_trends['Overall_Score'],
                  mode='lines+markers', name='Overall', line=dict(color='#3b82f6', width=3)),
        row=1, col=1
    )
    
    # HEDIS
    fig_individual.add_trace(
        go.Scatter(x=provider_trends['Month'], y=provider_trends['HEDIS_Compliance_Rate'],
                  mode='lines+markers', name='HEDIS', line=dict(color='#10b981', width=3)),
        row=1, col=2
    )
    
    # Gap Closure
    fig_individual.add_trace(
        go.Scatter(x=provider_trends['Month'], y=provider_trends['Gap_Closure_Rate'],
                  mode='lines+markers', name='Gap Closure', line=dict(color='#f59e0b', width=3)),
        row=2, col=1
    )
    
    # Patient Satisfaction
    fig_individual.add_trace(
        go.Scatter(x=provider_trends['Month'], y=provider_trends['Patient_Satisfaction'],
                  mode='lines+markers', name='Satisfaction', line=dict(color='#8b5cf6', width=3)),
        row=2, col=2
    )
    
    fig_individual.update_layout(height=600, showlegend=False)
    fig_individual.update_xaxes(title_text="Month")
    fig_individual.update_yaxes(title_text="Score (%)", row=1, col=1)
    fig_individual.update_yaxes(title_text="Rate (%)", row=1, col=2)
    fig_individual.update_yaxes(title_text="Rate (%)", row=2, col=1)
    fig_individual.update_yaxes(title_text="Rating (1-5)", row=2, col=2)
    
    st.plotly_chart(fig_individual, use_container_width=True)

# Footer with insights
st.markdown("---")
st.subheader("💡 Key Insights & Recommendations")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    **🟢 Strengths:**
    - 100% providers above 83% overall score
    - Strong HEDIS compliance across team
    - Patient satisfaction high (4.4-4.8)
    """)

with col2:
    st.markdown("""
    **🟡 Areas for Improvement:**
    - Gap closure rates vary significantly
    - Documentation quality inconsistent
    - Productivity differences across team
    """)

with col3:
    st.markdown("""
    **🎯 Recommendations:**
    - Peer coaching from top performers
    - Documentation training workshops
    - Standardize gap closure workflows
    """)

# Sidebar info
st.sidebar.markdown("---")
st.sidebar.markdown("### 📊 Scorecard Info")
st.sidebar.info("""
**Scoring Methodology:**
- Weighted average of 8 metrics
- Quality metrics: 55% weight
- Operations: 35% weight
- Financial: 5% weight
- Productivity: 5% weight

**Color Coding:**
- 🟢 Green: Exceeds target
- 🟡 Yellow: Near target
- 🔴 Red: Below target
""")

st.sidebar.markdown("### 📅 Update Frequency")
st.sidebar.markdown("Monthly refresh on the 5th business day")
