# Ethiopia Financial Inclusion Dashboard
# Streamlit Dashboard for Task 5

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go

# Page config with icon
st.set_page_config(
    page_title="Ethiopia Financial Inclusion Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        padding: 1rem 0;
    }
    .metric-card {
        background-color: #f0f2f6;
        border-radius: 10px;
        padding: 1rem;
        text-align: center;
        border-left: 4px solid #1f77b4;
    }
    .metric-value {
        font-size: 2rem;
        font-weight: bold;
        color: #1f77b4;
    }
    .metric-label {
        font-size: 0.9rem;
        color: #666;
    }
    .section-header {
        font-size: 1.5rem;
        font-weight: bold;
        padding: 0.5rem 0;
        border-bottom: 2px solid #1f77b4;
        margin-bottom: 1rem;
    }
    .info-box {
        background-color: #e8f4f8;
        border-radius: 10px;
        padding: 1rem;
        border-left: 4px solid #1f77b4;
        margin: 1rem 0;
    }
    .footer {
        text-align: center;
        color: #666;
        padding: 2rem 0;
        border-top: 1px solid #ddd;
        margin-top: 2rem;
    }
    div[data-testid="stMetric"] {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    div[data-testid="stMetric"] > div:first-child {
        font-weight: bold;
        color: #1f77b4;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<div class="main-header">🇪🇹 Ethiopia Financial Inclusion Dashboard</div>', unsafe_allow_html=True)
st.markdown("---")

# Load data
@st.cache_data
def load_data():
    try:
        df = pd.read_excel('data/raw/ethiopia_fi_unified_data.xlsx')
        return df
    except:
        st.warning("Data file not found. Please ensure data is in the correct location.")
        return None

@st.cache_data
def load_forecast():
    try:
        forecast = pd.read_csv('reports/forecast_summary.csv')
        return forecast
    except:
        st.warning("Forecast file not found.")
        return None

df = load_data()
forecast = load_forecast()

if df is not None:
    observations = df[df['record_type'] == 'observation']
    events = df[df['record_type'] == 'event']
    targets = df[df['record_type'] == 'target']
    
    # Sidebar with icon
    st.sidebar.markdown("### 🧭 Navigation")
    page = st.sidebar.radio(
        "Select Page",
        ["📊 Overview", "📈 Trends", "🔮 Forecasts", "📅 Events", "🔍 Data Explorer"],
        index=0
    )
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### ℹ️ About")
    st.sidebar.info(
        "**Data Sources:**\n"
        "- Global Findex Database\n"
        "- National Bank of Ethiopia\n"
        "- GSMA Reports\n"
        "- Industry Reports\n\n"
        "**Last Updated:** " + datetime.now().strftime("%B %d, %Y")
    )
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📊 Key Stats")
    st.sidebar.metric("Total Records", len(df))
    st.sidebar.metric("Observations", len(observations))
    st.sidebar.metric("Events Tracked", len(events))
    
    # Page 1: Overview
    if page == "📊 Overview":
        st.markdown('<div class="section-header">📈 Key Metrics Overview</div>', unsafe_allow_html=True)
        
        col1, col2, col3, col4 = st.columns(4)
        
        latest_access = observations[observations['indicator_code'] == 'ACC_OWNERSHIP']
        if len(latest_access) > 0:
            latest_access = latest_access.sort_values('observation_date').iloc[-1]
            with col1:
                st.metric(
                    label="🏦 Account Ownership",
                    value=f"{latest_access['value_numeric']:.1f}%",
                    delta=None,
                    help="Latest available account ownership rate"
                )
        
        latest_usage = observations[observations['indicator_code'] == 'USG_DIGITAL_PAYMENT']
        if len(latest_usage) > 0:
            latest_usage = latest_usage.sort_values('observation_date').iloc[-1]
            with col2:
                st.metric(
                    label="📱 Digital Payment Adoption",
                    value=f"{latest_usage['value_numeric']:.1f}%",
                    delta=None,
                    help="Latest available digital payment adoption rate"
                )
        
        if forecast is not None:
            forecast_2027 = forecast[forecast['Year'] == 2027]
            if len(forecast_2027) > 0:
                access_2027 = forecast_2027[forecast_2027['Indicator'] == 'Access']['Base'].values[0]
                with col3:
                    st.metric(
                        label="🎯 Access Forecast 2027",
                        value=f"{access_2027:.1f}%",
                        delta=f"{access_2027 - 60:.1f}% vs Target 60%",
                        delta_color="inverse"
                    )
        
        with col4:
            st.metric(
                label="📌 Total Events",
                value=len(events),
                delta=None,
                help="Number of financial inclusion events tracked"
            )
        
        st.markdown("---")
        
        # Two column layout
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📊 Account Ownership Trend")
            access_data = observations[observations['indicator_code'] == 'ACC_OWNERSHIP']
            access_data = access_data.sort_values('observation_date')
            
            fig = px.line(
                access_data,
                x='observation_date',
                y='value_numeric',
                title='Ethiopia Account Ownership (2014-2024)',
                labels={'observation_date': 'Year', 'value_numeric': 'Account Ownership (%)'},
                markers=True,
                color_discrete_sequence=['#1f77b4']
            )
            fig.add_hline(y=60, line_dash="dash", line_color="red", annotation_text="🎯 Target 60%")
            fig.update_layout(
                height=400,
                hovermode='x unified',
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)'
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("### 📱 Digital Payment Trend")
            usage_data = observations[observations['indicator_code'] == 'USG_DIGITAL_PAYMENT']
            if len(usage_data) > 0:
                usage_data = usage_data.sort_values('observation_date')
                fig = px.line(
                    usage_data,
                    x='observation_date',
                    y='value_numeric',
                    title='Digital Payment Adoption (2014-2024)',
                    labels={'observation_date': 'Year', 'value_numeric': 'Adoption (%)'},
                    markers=True,
                    color_discrete_sequence=['#ff7f0e']
                )
                fig.update_layout(
                    height=400,
                    hovermode='x unified',
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)'
                )
                st.plotly_chart(fig, use_container_width=True)
        
        # Bottom row
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📊 Pillar Distribution")
            pillar_counts = observations['pillar'].value_counts()
            colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']
            fig = px.pie(
                values=pillar_counts.values,
                names=pillar_counts.index,
                title="Observations by Pillar",
                color_discrete_sequence=colors,
                hole=0.3
            )
            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("### 📚 Data Sources")
            source_counts = observations['source_name'].value_counts().head(8)
            fig = px.bar(
                x=source_counts.values,
                y=source_counts.index,
                orientation='h',
                title="Top 8 Data Sources",
                labels={'x': 'Count', 'y': 'Source'},
                color=source_counts.values,
                color_continuous_scale='Blues'
            )
            fig.update_layout(
                height=350,
                showlegend=False,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)'
            )
            st.plotly_chart(fig, use_container_width=True)
    
    # Page 2: Trends
    elif page == "📈 Trends":
        st.markdown('<div class="section-header">📈 Trend Analysis</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns([3, 1])
        
        with col1:
            indicators = observations['indicator_code'].unique().tolist()
            selected_indicators = st.multiselect(
                "Select Indicators to Display",
                indicators,
                default=indicators[:3] if len(indicators) >= 3 else indicators
            )
        
        with col2:
            st.write("")
            st.write("")
            trend_type = st.selectbox("Chart Type", ["Line", "Area", "Bar"])
        
        if selected_indicators:
            filtered_data = observations[observations['indicator_code'].isin(selected_indicators)]
            
            if trend_type == "Line":
                fig = px.line(
                    filtered_data,
                    x='observation_date',
                    y='value_numeric',
                    color='indicator_code',
                    title='Selected Indicators Over Time',
                    labels={'observation_date': 'Year', 'value_numeric': 'Value (%)'},
                    markers=True
                )
            elif trend_type == "Area":
                fig = px.area(
                    filtered_data,
                    x='observation_date',
                    y='value_numeric',
                    color='indicator_code',
                    title='Selected Indicators Over Time',
                    labels={'observation_date': 'Year', 'value_numeric': 'Value (%)'}
                )
            else:
                fig = px.bar(
                    filtered_data,
                    x='observation_date',
                    y='value_numeric',
                    color='indicator_code',
                    title='Selected Indicators Over Time',
                    labels={'observation_date': 'Year', 'value_numeric': 'Value (%)'},
                    barmode='group'
                )
            
            fig.update_layout(
                height=500,
                hovermode='x unified',
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)'
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Growth rates section
        st.markdown("### 📈 Growth Rates Analysis")
        access_data = observations[observations['indicator_code'] == 'ACC_OWNERSHIP']
        access_data = access_data.sort_values('observation_date')
        
        if len(access_data) > 1:
            growth_data = []
            for i in range(1, len(access_data)):
                prev = access_data.iloc[i-1]['value_numeric']
                curr = access_data.iloc[i]['value_numeric']
                year = access_data.iloc[i]['observation_date'].year
                growth_data.append({
                    'Period': f"{access_data.iloc[i-1]['observation_date'].year}-{year}",
                    'Growth': round(curr - prev, 1),
                    'Growth %': round(((curr - prev) / prev) * 100, 1)
                })
            
            growth_df = pd.DataFrame(growth_data)
            
            col1, col2 = st.columns(2)
            
            with col1:
                fig = px.bar(
                    growth_df,
                    x='Period',
                    y='Growth',
                    title='Access Growth by Period (percentage points)',
                    labels={'Growth': 'Percentage Points'},
                    color='Growth',
                    color_continuous_scale='RdYlGn'
                )
                fig.update_layout(
                    height=350,
                    showlegend=False,
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)'
                )
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                fig = px.bar(
                    growth_df,
                    x='Period',
                    y='Growth %',
                    title='Access Growth by Period (%)',
                    labels={'Growth %': 'Growth %'},
                    color='Growth %',
                    color_continuous_scale='RdYlGn'
                )
                fig.update_layout(
                    height=350,
                    showlegend=False,
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)'
                )
                st.plotly_chart(fig, use_container_width=True)
    
    # Page 3: Forecasts
    elif page == "🔮 Forecasts":
        st.markdown('<div class="section-header">🔮 Forecasts 2025-2027</div>', unsafe_allow_html=True)
        
        if forecast is not None:
            st.markdown("""
            <div class="info-box">
            <b>📌 Forecast Methodology:</b> Linear regression with scenario adjustments based on event impacts.
            Confidence intervals represent 95% prediction intervals.
            </div>
            """, unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("### 🏦 Access Forecast")
                access_forecast = forecast[forecast['Indicator'] == 'Access']
                
                fig = go.Figure()
                fig.add_trace(go.Scatter(
                    x=access_forecast['Year'],
                    y=access_forecast['Optimistic'],
                    mode='lines+markers',
                    name='🚀 Optimistic',
                    line=dict(color='#2ca02c', width=2, dash='dash'),
                    marker=dict(size=10)
                ))
                fig.add_trace(go.Scatter(
                    x=access_forecast['Year'],
                    y=access_forecast['Base'],
                    mode='lines+markers',
                    name='📊 Base Case',
                    line=dict(color='#1f77b4', width=3),
                    marker=dict(size=12, symbol='circle')
                ))
                fig.add_trace(go.Scatter(
                    x=access_forecast['Year'],
                    y=access_forecast['Pessimistic'],
                    mode='lines+markers',
                    name='⚠️ Pessimistic',
                    line=dict(color='#d62728', width=2, dash='dash'),
                    marker=dict(size=10)
                ))
                fig.add_hline(y=60, line_dash="dash", line_color="red", annotation_text="🎯 60% Target")
                fig.update_layout(
                    title='Account Ownership Forecast 2025-2027',
                    xaxis_title='Year',
                    yaxis_title='Access (%)',
                    height=450,
                    hovermode='x unified',
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
                )
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                st.markdown("### 📱 Usage Forecast")
                usage_forecast = forecast[forecast['Indicator'] == 'Usage']
                
                if len(usage_forecast) > 0:
                    fig = go.Figure()
                    fig.add_trace(go.Scatter(
                        x=usage_forecast['Year'],
                        y=usage_forecast['Optimistic'],
                        mode='lines+markers',
                        name='🚀 Optimistic',
                        line=dict(color='#2ca02c', width=2, dash='dash'),
                        marker=dict(size=10)
                    ))
                    fig.add_trace(go.Scatter(
                        x=usage_forecast['Year'],
                        y=usage_forecast['Base'],
                        mode='lines+markers',
                        name='📊 Base Case',
                        line=dict(color='#ff7f0e', width=3),
                        marker=dict(size=12, symbol='diamond')
                    ))
                    fig.add_trace(go.Scatter(
                        x=usage_forecast['Year'],
                        y=usage_forecast['Pessimistic'],
                        mode='lines+markers',
                        name='⚠️ Pessimistic',
                        line=dict(color='#d62728', width=2, dash='dash'),
                        marker=dict(size=10)
                    ))
                    fig.update_layout(
                        title='Digital Payment Adoption Forecast 2025-2027',
                        xaxis_title='Year',
                        yaxis_title='Usage (%)',
                        height=450,
                        hovermode='x unified',
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
                    )
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("📌 No usage forecast data available")
            
            # Forecast table
            st.markdown("### 📊 Forecast Summary Table")
            st.dataframe(forecast, use_container_width=True, hide_index=True)
            
            # Progress toward target
            st.markdown("### 🎯 Progress Toward 60% Target")
            access_2027 = forecast[(forecast['Indicator'] == 'Access') & (forecast['Year'] == 2027)]
            if len(access_2027) > 0:
                target_access = access_2027['Base'].values[0]
                progress = min(100, (target_access / 60) * 100)
                
                col1, col2, col3 = st.columns([2, 1, 2])
                with col1:
                    st.metric(
                        label="🎯 2027 Projection",
                        value=f"{target_access:.1f}%",
                        delta=f"{target_access - 60:.1f}% vs Target"
                    )
                with col3:
                    st.metric(
                        label="📊 Progress",
                        value=f"{progress:.1f}%",
                        delta=None
                    )
                
                st.progress(progress / 100)
                st.markdown(f"<small>📌 Ethiopia is projected to reach {progress:.1f}% of the 60% target by 2027</small>", unsafe_allow_html=True)
        else:
            st.warning("📌 No forecast data available. Please run forecasting notebook first.")
    
    # Page 4: Events
    elif page == "📅 Events":
        st.markdown('<div class="section-header">📅 Events Timeline</div>', unsafe_allow_html=True)
        
        if len(events) > 0:
            # Event table
            st.markdown("### 📋 Cataloged Events")
            event_cols = ['name', 'category', 'observation_date', 'description']
            available_cols = [col for col in event_cols if col in events.columns]
            
            if 'description' not in available_cols:
                available_cols = [col for col in event_cols if col in events.columns]
            
            st.dataframe(events[available_cols], use_container_width=True, hide_index=True)
            
            # Event timeline
            st.markdown("### 📅 Event Timeline Visualization")
            
            col1, col2 = st.columns(2)
            
            with col1:
                fig = px.scatter(
                    events,
                    x='observation_date',
                    y='category',
                    text='name' if 'name' in events.columns else None,
                    title='Financial Inclusion Events Timeline',
                    labels={'observation_date': 'Year', 'category': 'Event Category'},
                    size=[30] * len(events),
                    color='category',
                    color_discrete_sequence=px.colors.qualitative.Set3
                )
                fig.update_traces(textposition='top center', marker=dict(sizemode='diameter'))
                fig.update_layout(
                    height=400,
                    hovermode='closest',
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    showlegend=False
                )
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                st.markdown("### 📊 Events by Category")
                category_counts = events['category'].value_counts()
                fig = px.pie(
                    values=category_counts.values,
                    names=category_counts.index,
                    title='Events by Category',
                    color_discrete_sequence=px.colors.qualitative.Set3,
                    hole=0.3
                )
                fig.update_traces(textposition='inside', textinfo='percent+label')
                fig.update_layout(
                    height=400,
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)'
                )
                st.plotly_chart(fig, use_container_width=True)
            
            # Event count by year
            st.markdown("### 📊 Events by Year")
            events['year'] = pd.to_datetime(events['observation_date']).dt.year
            yearly_events = events['year'].value_counts().sort_index()
            
            fig = px.bar(
                x=yearly_events.index,
                y=yearly_events.values,
                title='Number of Events by Year',
                labels={'x': 'Year', 'y': 'Number of Events'},
                color=yearly_events.values,
                color_continuous_scale='Blues'
            )
            fig.update_layout(
                height=350,
                showlegend=False,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)'
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("📌 No events found in the dataset")
    
    # Page 5: Data Explorer
    elif page == "🔍 Data Explorer":
        st.markdown('<div class="section-header">🔍 Data Explorer</div>', unsafe_allow_html=True)
        
        st.markdown("### 🔎 Filter and Explore Data")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            record_types = df['record_type'].unique().tolist()
            selected_type = st.selectbox("📋 Record Type", record_types)
        
        filtered_df = df[df['record_type'] == selected_type]
        
        with col2:
            if 'pillar' in filtered_df.columns:
                pillars = filtered_df['pillar'].dropna().unique().tolist()
                if pillars:
                    selected_pillar = st.selectbox("🏷️ Pillar", ['All'] + pillars)
                    if selected_pillar != 'All':
                        filtered_df = filtered_df[filtered_df['pillar'] == selected_pillar]
        
        with col3:
            if 'confidence' in filtered_df.columns:
                confidences = filtered_df['confidence'].dropna().unique().tolist()
                if confidences:
                    selected_confidence = st.selectbox("🎯 Confidence", ['All'] + confidences)
                    if selected_confidence != 'All':
                        filtered_df = filtered_df[filtered_df['confidence'] == selected_confidence]
        
        # Display data
        st.markdown("### 📊 Data Preview")
        st.dataframe(filtered_df, use_container_width=True, hide_index=True)
        
        # Summary stats
        st.markdown("### 📈 Summary Statistics")
        if 'value_numeric' in filtered_df.columns and len(filtered_df) > 0:
            numeric_df = filtered_df['value_numeric'].dropna()
            if len(numeric_df) > 0:
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("📊 Count", len(numeric_df))
                with col2:
                    st.metric("📈 Mean", f"{numeric_df.mean():.2f}")
                with col3:
                    st.metric("📉 Min", f"{numeric_df.min():.2f}")
                with col4:
                    st.metric("📈 Max", f"{numeric_df.max():.2f}")
        
        # Download button
        if len(filtered_df) > 0:
            st.markdown("### 💾 Download Data")
            csv = filtered_df.to_csv(index=False)
            st.download_button(
                label="📥 Download as CSV",
                data=csv,
                file_name=f"{selected_type}_data.csv",
                mime="text/csv",
                use_container_width=True
            )
    
    # Footer
    st.markdown("""
    <div class="footer">
        <p>🏛️ Selam Analytics | Ethiopia Financial Inclusion Forecasting</p>
        <p style="font-size: 0.8rem;">Data sourced from Global Findex, NBE, GSMA, and industry reports</p>
        <p style="font-size: 0.8rem;">Last updated: July 2026</p>
    </div>
    """, unsafe_allow_html=True)

else:
    st.error("❌ Unable to load data. Please check file path and format.")