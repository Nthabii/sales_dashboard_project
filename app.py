import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from datetime import datetime

# Login page 
def login_page():
    st.title("🔐 AI Sales Dashboard Login")
    
    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Login")
        
        if submitted:
            # authentication 
            if username == "Nthabiseng Gopolang" and password == "Nthabi@2001":
                st.session_state.logged_in = True
                st.session_state.view_mode = "Team"  
                st.rerun()
            else:
                st.error("Invalid username or password")

def apply_custom_styles():
    st.markdown("""
    <style>
        /* Main styling */
        .main {
            background-color: #f8f9fa;
        }
        .stApp {
            background-color: white;
        }
        
        
        .metric-card {
            background: white;
            border-radius: 8px;
            padding: 8px;  
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            border-left: 4px solid #4e73df;
            height: 80px; 
            margin-bottom: 6px;  
            display: flex;
            flex-direction: column;
            justify-content: space-between;
        }
        .metric-title {
            font-size: 9px;  
            color: #5a5c69;
            font-weight: 600;
            margin-bottom: 2px;  
        }
        .metric-value {
            font-size: 14px;  
            font-weight: 700;
            color: #2e59d9;
        }
        .metric-change {
            font-size: 8px;  
            margin-top: 2px;  
        }
        .positive {
            color: #1cc88a;
        }
        .negative {
            color: #e74a3b;
        }
        .metric-target {
            font-size: 8px;  
            margin-top: 2px;  
            color: #5a5c69;
        }
        
        
        .header {
            color: #2e59d9;
            font-size: 1.1rem;  
            border-bottom: 1px solid #eee;
            padding-bottom: 6px;  
            margin-bottom: 10px;  
        }
        
        
        .stPlotlyChart {
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            background: white;
            padding: 10px;  
            margin-bottom: 12px !important;  
            height: 240px;  
            width: 100% !important;
        }
        
        
        .block-container {
            padding-top: 1rem;  
            padding-bottom: 1rem;  
        }
        
        
        .stSidebar {
            background-color: #f8f9fa;
        }
        .sidebar .sidebar-content {
            background-color: #f8f9fa;
        }
        
        
        .chart-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 18px;  
            margin-bottom: 10px;  
        }
        
        
        .st-emotion-cache-1v0mbdj {
            width: 100% !important;
        }
        
        
        .individual-metrics {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 8px;  
            margin-bottom: 10px;  
        }
        
        
        .sidebar .sidebar-content h1 {
            font-size: 1.3rem !important;  
        }
        
        
        .st-emotion-cache-1y4p8pa {
            padding-left: 1.2rem;
            padding-right: 1.2rem;
        }
    </style>
    """, unsafe_allow_html=True)

# Performance gauge 
def create_performance_gauge(value, title, target=100):
    
    if value >= target * 1.1:
        gauge_color = "#1cc88a"
        performance_text = "Exceeding Target"
    elif value >= target * 0.9:
        gauge_color = "#4e73df"
        performance_text = "Meeting Target"
    else:
        gauge_color = "#e74a3b"
        performance_text = "Below Target"
    
    fig = go.Figure(go.Indicator(
        mode = "gauge+number+delta",
        value = value,
        delta = {'reference': target, 'increasing': {'color': "#1cc88a"}, 'decreasing': {'color': "#e74a3b"}},
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {
            'text': f"{title}<br><span style='font-size:0.6em;color:gray'>{performance_text}</span>",  
            'font': {'size': 12}  
        },
        gauge = {
            'axis': {'range': [None, target * 1.5], 'tickwidth': 1, 'tickcolor': "darkblue"},
            'bar': {'color': gauge_color, 'thickness': 0.25},  
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [0, target*0.7], 'color': "#f8f9fa"},
                {'range': [target*0.7, target*0.9], 'color': "#f6c23e"},
                {'range': [target*0.9, target*1.1], 'color': "#4e73df"},
                {'range': [target*1.1, target*1.5], 'color': "#1cc88a"}
            ],
            'threshold': {
                'line': {'color': "black", 'width': 3},  
                'thickness': 0.7,
                'value': target
            }
        }
    ))
    
    fig.update_layout(
        height=180,  
        margin=dict(l=15, r=15, t=60, b=15),  
        font={'family': "Arial", 'color': "darkblue", 'size': 10}  
    )
    
    return fig


def display_metric(title, current_value, prev_value=None, target=None, format_str=None, reverse_trend=False):
    
    current_value = float(current_value) if current_value is not None else 0
    prev_value = float(prev_value) if prev_value is not None else None
    target = float(target) if target is not None else None
    
    
    if format_str is None:
        if "REVENUE" in title.upper() or "$" in title.upper():
            if abs(current_value) >= 1000000:
                format_str = "${:,.1f}M"
                current_value_display = current_value / 1000000
                if prev_value is not None:
                    prev_value_display = prev_value / 1000000
                if target is not None:
                    target_display = target / 1000000
            elif abs(current_value) >= 1000:
                format_str = "${:,.0f}K"
                current_value_display = current_value / 1000
                if prev_value is not None:
                    prev_value_display = prev_value / 1000
                if target is not None:
                    target_display = target / 1000
            else:
                format_str = "${:,.0f}"
                current_value_display = current_value
                if prev_value is not None:
                    prev_value_display = prev_value
                if target is not None:
                    target_display = target
        else:
            format_str = "{:,.0f}"
            current_value_display = current_value
            if prev_value is not None:
                prev_value_display = prev_value
            if target is not None:
                target_display = target
    else:
        current_value_display = current_value
        if prev_value is not None:
            prev_value_display = prev_value
        if target is not None:
            target_display = target
    
    if prev_value is not None:
        change = ((current_value - prev_value) / prev_value * 100) if prev_value != 0 else 0
        symbol = "▲" if change >= 0 else "▼"
        color_class = "positive" if change >= 0 else "negative"
        if reverse_trend:
            color_class = "negative" if change >= 0 else "positive"
            symbol = "▼" if change >= 0 else "▲"
        
        change_text = f"{symbol} {abs(change):.1f}% vs PY"
    else:
        change_text = ""
        color_class = ""
        symbol = ""
    
    if target is not None:
        target_status = (current_value / target * 100) if target != 0 else 0
        target_icon = "✅" if target_status >= 100 else "⚠️" if target_status >= 90 else "❌"
        target_text = f"<div class='metric-target'>{target_icon} {target_status:.0f}% of target</div>"
    else:
        target_text = ""
    
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">{title}</div>
        <div class="metric-value">{format_str.format(current_value_display)}</div>
        {f"<div class='metric-change {color_class}'>{change_text}</div>" if prev_value is not None else ""}
        {target_text if target is not None else ""}
    </div>
    """, unsafe_allow_html=True)

# Team revenue trend chart 
def plot_team_revenue_trend(current_year, last_year, title):
    
    monthly_current = current_year.groupby('Month')['Total_Revenue'].sum().reset_index()
    monthly_last = last_year.groupby('Month')['Total_Revenue'].sum().reset_index()
    
    
    month_order = ['January', 'February', 'March', 'April', 'May', 'June', 
                   'July', 'August', 'September', 'October', 'November', 'December']
    
    monthly_current['Month'] = pd.Categorical(monthly_current['Month'], categories=month_order, ordered=True)
    monthly_last['Month'] = pd.Categorical(monthly_last['Month'], categories=month_order, ordered=True)
    
    monthly_current = monthly_current.sort_values('Month')
    monthly_last = monthly_last.sort_values('Month')
    
    # Calculate YoY change
    merged = monthly_current.merge(monthly_last, on='Month', suffixes=('_current', '_last'))
    merged['YoY_Change'] = ((merged['Total_Revenue_current'] - merged['Total_Revenue_last']) / 
                           merged['Total_Revenue_last']) * 100
    
    
    fig = go.Figure()
    
    
    fig.add_trace(go.Bar(
        x=merged['Month'],
        y=merged['Total_Revenue_current'],
        name='Current Year',
        marker_color='#4e73df',
        hoverinfo='y+name',
        hovertemplate='%{x}<br>Revenue: $%{y:,.0f}<extra></extra>'
    ))
    
    
    fig.add_trace(go.Scatter(
        x=merged['Month'],
        y=merged['Total_Revenue_last'],
        name='Last Year',
        line=dict(color='#858796', width=2, dash='dot'),
        mode='lines+markers',
        hoverinfo='y+name',
        hovertemplate='%{x}<br>Revenue: $%{y:,.0f}<extra></extra>'
    ))
    
    
    target_value = 10000000  
    fig.add_hline(y=target_value, line_dash="dash", line_color="#f6c23e",
                 annotation_text=f"Monthly Target: ${target_value/1e6:.1f}M", 
                 annotation_position="bottom right")
    
    
    for i, row in merged.iterrows():
        if abs(row['YoY_Change']) > 5:  
            fig.add_annotation(
                x=row['Month'],
                y=row['Total_Revenue_current'],
                text=f"{'▲' if row['YoY_Change'] >=0 else '▼'} {abs(row['YoY_Change']):.0f}%",
                showarrow=False,
                yshift=10,
                font=dict(size=10, color='#1cc88a' if row['YoY_Change'] >=0 else '#e74a3b')
            )
    
    fig.update_layout(
        title=dict(text=title, font=dict(size=14)),
        xaxis_title="Month",
        yaxis_title="Revenue ($)",
        hovermode="x unified",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        plot_bgcolor='white',
        height=240,
        margin=dict(l=40, r=40, t=60, b=40)
    )
    
    return fig

# Team leaderboard comparison 
def plot_team_leaderboard(current_year, last_year, title):
    
    current = current_year.groupby('Team_Member')['Total_Revenue'].sum().reset_index()
    last = last_year.groupby('Team_Member')['Total_Revenue'].sum().reset_index()
    
    merged = current.merge(last, on='Team_Member', suffixes=('_current', '_last'), how='left').fillna(0)
    merged['YoY_Change'] = ((merged['Total_Revenue_current'] - merged['Total_Revenue_last']) / 
                          (merged['Total_Revenue_last'] + 1e-6)) * 100  
    
    
    merged = merged.sort_values('Total_Revenue_current', ascending=False)
    
    
    selected_member = st.selectbox(
        "Select Team Member",
        merged['Team_Member'].unique(),
        key="team_member_select"
    )
    
    
    member_data = merged[merged['Team_Member'] == selected_member].iloc[0]
    
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        
        st.markdown(f"**{member_data['Team_Member']}**")
        
    with col2:
        
        revenue_millions = member_data['Total_Revenue_current'] / 1000000
        st.markdown(f"**${revenue_millions:,.1f}M**")
    
    # Display YoY change
    change_color = "#1cc88a" if member_data['YoY_Change'] >= 0 else "#e74a3b"
    change_symbol = "▲" if member_data['YoY_Change'] >= 0 else "▼"
    st.markdown(
        f"<div style='color:{change_color}; font-size:0.8em;'>"
        f"{change_symbol} {abs(member_data['YoY_Change']):.1f}% vs Last Year"
        f"</div>",
        unsafe_allow_html=True
    )
    
    st.markdown("---")
    
    
    fig = go.Figure()
    
    
    fig.add_trace(go.Bar(
        y=merged['Team_Member'],
        x=merged['Total_Revenue_current'],
        name='Current Year',
        marker_color='#4e73df',
        orientation='h',
        text=[f"${x/1e6:.1f}M" for x in merged['Total_Revenue_current']],
        textposition='auto',
        hoverinfo='text'
    ))
    
    
    fig.add_trace(go.Bar(
        y=merged['Team_Member'],
        x=merged['Total_Revenue_last'],
        name='Last Year',
        marker_color='#858796',
        opacity=0.6,
        orientation='h',
        hoverinfo='x'
    ))
    
    
    for i, row in merged.iterrows():
        fig.add_annotation(
            x=max(row['Total_Revenue_current'], row['Total_Revenue_last']),
            y=row['Team_Member'],
            text=f"{'▲' if row['YoY_Change'] >=0 else '▼'} {abs(row['YoY_Change']):.1f}%",
            showarrow=False,
            xshift=10,
            font=dict(color='#1cc88a' if row['YoY_Change'] >=0 else '#e74a3b')
        )
    
    fig.update_layout(
        title=title,
        yaxis_title="Team Member",
        xaxis_title="Revenue ($)",
        barmode='group',
        hovermode="y unified",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        plot_bgcolor='white',
        height=400  
    )
    
    return fig

# Top products comparison with YoY indicators
def plot_top_products_comparison(current_year, last_year, title, n=5):
    
    top_products = current_year.groupby('Product_Name')['Total_Revenue'].sum().nlargest(n).index
    
    
    current = current_year[current_year['Product_Name'].isin(top_products)]
    last = last_year[last_year['Product_Name'].isin(top_products)]
    
    current_grouped = current.groupby('Product_Name')['Total_Revenue'].sum().reset_index()
    last_grouped = last.groupby('Product_Name')['Total_Revenue'].sum().reset_index()
    
    merged = current_grouped.merge(last_grouped, on='Product_Name', suffixes=('_current', '_last'))
    merged['YoY_Change'] = ((merged['Total_Revenue_current'] - merged['Total_Revenue_last']) / 
                           merged['Total_Revenue_last']) * 100
    
    
    merged = merged.sort_values('Total_Revenue_current', ascending=False)
    
    
    fig = go.Figure()
    
    
    fig.add_trace(go.Bar(
        x=merged['Product_Name'],
        y=merged['Total_Revenue_current'],
        name='Current Year',
        marker_color='#4e73df',
        text=[f"${x/1e6:.1f}M" for x in merged['Total_Revenue_current']],
        textposition='auto',
        hoverinfo='text'
    ))
    
    
    fig.add_trace(go.Bar(
        x=merged['Product_Name'],
        y=merged['Total_Revenue_last'],
        name='Last Year',
        marker_color='#858796',
        opacity=0.6,
        hoverinfo='y'
    ))
    
    
    for i, row in merged.iterrows():
        fig.add_annotation(
            x=row['Product_Name'],
            y=max(row['Total_Revenue_current'], row['Total_Revenue_last']),
            text=f"{'▲' if row['YoY_Change'] >=0 else '▼'} {abs(row['YoY_Change']):.1f}%",
            showarrow=False,
            yshift=10,
            font=dict(color='#1cc88a' if row['YoY_Change'] >=0 else '#e74a3b')
        )
    
    fig.update_layout(
        title=title,
        xaxis_title="Product",
        yaxis_title="Revenue ($)",
        barmode='group',
        hovermode="x unified",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        plot_bgcolor='white',
        height=240  
    )
    
    return fig

# Channel revenue breakdown with YoY comparison
def plot_channel_revenue(current_year, last_year, title):
    
    current = current_year.groupby('Sales_Channel')['Total_Revenue'].sum().reset_index()
    last = last_year.groupby('Sales_Channel')['Total_Revenue'].sum().reset_index()
    
    merged = current.merge(last, on='Sales_Channel', suffixes=('_current', '_last'))
    merged['YoY_Change'] = ((merged['Total_Revenue_current'] - merged['Total_Revenue_last']) / 
                          merged['Total_Revenue_last']) * 100
    
    
    merged = merged.sort_values('Total_Revenue_current', ascending=False)
    
    
    fig = go.Figure()
    
    
    fig.add_trace(go.Bar(
        x=merged['Sales_Channel'],
        y=merged['Total_Revenue_current'],
        name='Current Year',
        marker_color='#4e73df',
        text=[f"${x/1e6:.1f}M" for x in merged['Total_Revenue_current']],
        textposition='auto',
        hoverinfo='text'
    ))
    
    
    fig.add_trace(go.Bar(
        x=merged['Sales_Channel'],
        y=merged['Total_Revenue_last'],
        name='Last Year',
        marker_color='#858796',
        opacity=0.6,
        hoverinfo='y'
    ))
    
    
    for i, row in merged.iterrows():
        fig.add_annotation(
            x=row['Sales_Channel'],
            y=max(row['Total_Revenue_current'], row['Total_Revenue_last']),
            text=f"{'▲' if row['YoY_Change'] >=0 else '▼'} {abs(row['YoY_Change']):.1f}%",
            showarrow=False,
            yshift=10,
            font=dict(color='#1cc88a' if row['YoY_Change'] >=0 else '#e74a3b')
        )
    
    fig.update_layout(
        title=title,
        xaxis_title="Sales Channel",
        yaxis_title="Revenue ($)",
        barmode='group',
        hovermode="x unified",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        plot_bgcolor='white',
        height=240  
    )
    
    return fig

# Individual revenue trend vs target 
def plot_individual_trend(current_year, last_year, title, target=5000000):
    
    monthly_current = current_year.groupby('Month')['Total_Revenue'].sum().reset_index()
    monthly_last = last_year.groupby('Month')['Total_Revenue'].sum().reset_index()
    
    
    month_order = ['January', 'February', 'March', 'April', 'May', 'June', 
                   'July', 'August', 'September', 'October', 'November', 'December']
    
    monthly_current['Month'] = pd.Categorical(monthly_current['Month'], categories=month_order, ordered=True)
    monthly_last['Month'] = pd.Categorical(monthly_last['Month'], categories=month_order, ordered=True)
    
    monthly_current = monthly_current.sort_values('Month')
    monthly_last = monthly_last.sort_values('Month')
    
    
    merged = monthly_current.merge(monthly_last, on='Month', suffixes=('_current', '_last'))
    merged['YoY_Change'] = ((merged['Total_Revenue_current'] - merged['Total_Revenue_last']) / 
                           merged['Total_Revenue_last']) * 100
    
    
    fig = go.Figure()
    
    
    fig.add_trace(go.Bar(
        x=merged['Month'],
        y=merged['Total_Revenue_current'],
        name='Current Year',
        marker_color='#4e73df',
        hoverinfo='y+name',
        hovertemplate='%{x}<br>Revenue: $%{y:,.0f}<extra></extra>'
    ))
    
    
    fig.add_trace(go.Scatter(
        x=merged['Month'],
        y=merged['Total_Revenue_last'],
        name='Last Year',
        line=dict(color='#858796', width=2, dash='dot'),
        mode='lines+markers',
        hoverinfo='y+name',
        hovertemplate='%{x}<br>Revenue: $%{y:,.0f}<extra></extra>'
    ))
    
    
    fig.add_hline(y=target, line_dash="dash", line_color="#f6c23e",
                 annotation_text=f"Monthly Target: ${target/1e6:.1f}M", 
                 annotation_position="bottom right")
    
    
    for i, row in merged.iterrows():
        if abs(row['YoY_Change']) > 5:  
            fig.add_annotation(
                x=row['Month'],
                y=row['Total_Revenue_current'],
                text=f"{'▲' if row['YoY_Change'] >=0 else '▼'} {abs(row['YoY_Change']):.0f}%",
                showarrow=False,
                yshift=10,
                font=dict(size=10, color='#1cc88a' if row['YoY_Change'] >=0 else '#e74a3b')
            )
    
    fig.update_layout(
        title=dict(text=title, font=dict(size=14)),
        xaxis_title="Month",
        yaxis_title="Revenue ($)",
        hovermode="x unified",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        plot_bgcolor='white',
        height=240,
        margin=dict(l=40, r=40, t=60, b=40)
    )
    
    return fig

# Individual top products
def plot_individual_products(current_year, last_year, title):
    
    current = current_year.groupby('Product_Name')['Total_Revenue'].sum().reset_index()
    last = last_year.groupby('Product_Name')['Total_Revenue'].sum().reset_index()
    
    merged = current.merge(last, on='Product_Name', suffixes=('_current', '_last'), how='outer').fillna(0)
    merged['YoY_Change'] = ((merged['Total_Revenue_current'] - merged['Total_Revenue_last']) / 
                          (merged['Total_Revenue_last'] + 1e-6)) * 100  
    
    
    merged = merged.sort_values('Total_Revenue_current', ascending=False).head(5)
    
    
    fig = go.Figure()
    
    
    fig.add_trace(go.Bar(
        x=merged['Product_Name'],
        y=merged['Total_Revenue_current'],
        name='Current Year',
        marker_color='#4e73df',
        text=[f"${x/1e6:.1f}M" for x in merged['Total_Revenue_current']],  
        textposition='auto',
        hoverinfo='text'
    ))
    
    
    fig.add_trace(go.Bar(
        x=merged['Product_Name'],
        y=merged['Total_Revenue_last'],
        name='Last Year',
        marker_color='#858796',
        opacity=0.6,
        hoverinfo='y'
    ))
    
    
    for i, row in merged.iterrows():
        fig.add_annotation(
            x=row['Product_Name'],
            y=max(row['Total_Revenue_current'], row['Total_Revenue_last']),
            text=f"{'▲' if row['YoY_Change'] >=0 else '▼'} {abs(row['YoY_Change']):.1f}%",
            showarrow=False,
            yshift=10,
            font=dict(color='#1cc88a' if row['YoY_Change'] >=0 else '#e74a3b')
        )
    
    fig.update_layout(
        title=title,
        xaxis_title="Product",
        yaxis_title="Revenue ($)",
        barmode='group',
        hovermode="x unified",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        plot_bgcolor='white',
        height=240  
    )
    
    return fig

# Individual channel performance
def plot_individual_channels(current_year, last_year, title):
    
    current = current_year.groupby('Sales_Channel')['Total_Revenue'].sum().reset_index()
    last = last_year.groupby('Sales_Channel')['Total_Revenue'].sum().reset_index()
    
    merged = current.merge(last, on='Sales_Channel', suffixes=('_current', '_last'), how='outer').fillna(0)
    merged['YoY_Change'] = ((merged['Total_Revenue_current'] - merged['Total_Revenue_last']) / 
                          (merged['Total_Revenue_last'] + 1e-6)) * 100  
    
    
    merged = merged.sort_values('Total_Revenue_current', ascending=False)
    
    
    fig = go.Figure()
    
    
    fig.add_trace(go.Bar(
        x=merged['Sales_Channel'],
        y=merged['Total_Revenue_current'],
        name='Current Year',
        marker_color='#4e73df',
        text=[f"${x/1e6:.1f}M" for x in merged['Total_Revenue_current']],  
        textposition='auto',
        hoverinfo='text'
    ))
    
    
    fig.add_trace(go.Bar(
        x=merged['Sales_Channel'],
        y=merged['Total_Revenue_last'],
        name='Last Year',
        marker_color='#858796',
        opacity=0.6,
        hoverinfo='y'
    ))
    
    
    for i, row in merged.iterrows():
        fig.add_annotation(
            x=row['Sales_Channel'],
            y=max(row['Total_Revenue_current'], row['Total_Revenue_last']),
            text=f"{'▲' if row['YoY_Change'] >=0 else '▼'} {abs(row['YoY_Change']):.1f}%",
            showarrow=False,
            yshift=10,
            font=dict(color='#1cc88a' if row['YoY_Change'] >=0 else '#e74a3b')
        )
    
    fig.update_layout(
        title=title,
        xaxis_title="Sales Channel",
        yaxis_title="Revenue ($)",
        barmode='group',
        hovermode="x unified",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        plot_bgcolor='white',
        height=240  
    )
    
    return fig

# Sales by location geo chart
def plot_sales_by_location(current_year, title):
    
    location_data = current_year.groupby('Country')['Total_Revenue'].sum().reset_index()
    
    fig = px.choropleth(
        location_data,
        locations="Country",
        locationmode="country names",
        color="Total_Revenue",
        hover_name="Country",
        hover_data=["Total_Revenue"],
        color_continuous_scale=px.colors.sequential.Blues,
        title=title
    )
    
    fig.update_layout(
        height=240,  
        margin=dict(l=15, r=15, t=35, b=15),
        geo=dict(
            showframe=False,
            showcoastlines=False,
            projection_type='equirectangular'
        )
    )
    
    return fig

# Individual performance comparison chart
def plot_individual_comparison(current_year, last_year, title):
    
    rev_c = current_year["Total_Revenue"].sum() if not current_year.empty else 0
    rev_l = last_year["Total_Revenue"].sum() if not last_year.empty else 0
    
    
    yoy_change = ((rev_c - rev_l) / rev_l * 100) if rev_l != 0 else 0
    
    
    fig = go.Figure()
    
    
    fig.add_trace(go.Bar(
        x=['Current Year'],
        y=[rev_c],
        name='Current Year',
        marker_color='#4e73df',
        text=[f"${rev_c/1e6:.1f}M"],  
        textposition='auto'
    ))
    
    
    fig.add_trace(go.Bar(
        x=['Last Year'],
        y=[rev_l],
        name='Last Year',
        marker_color='#858796',
        text=[f"${rev_l/1e6:.1f}M"],  
        textposition='auto'
    ))
    
    
    fig.add_annotation(
        x=0.5,
        y=max(rev_c, rev_l),
        text=f"{'▲' if yoy_change >=0 else '▼'} {abs(yoy_change):.1f}% YoY",
        showarrow=False,
        yshift=20,
        font=dict(size=12, color='#1cc88a' if yoy_change >=0 else '#e74a3b')  
    )
    
    fig.update_layout(
        title=title,
        yaxis_title="Revenue ($)",
        plot_bgcolor='white',
        height=240,  
        showlegend=True
    )
    
    return fig

# Load data from CSV file
@st.cache_data(ttl=3600)  
def load_data(file_path):
    try:
        
        df = pd.read_csv(file_path)
        
        
        df['Date'] = pd.to_datetime(df['Date'], format='%d/%m/%Y')
        
        
        df['Year'] = df['Date'].dt.year
        df['Month'] = df['Date'].dt.month_name()
        df['Month_Num'] = df['Date'].dt.month
        
        
        df.columns = [col.strip().replace(' ', '_') for col in df.columns]
        
        
        numeric_cols = ['Quantity_Sold', 'Unit_Price', 'Total_Revenue', 'CSAT', 'NPS']
        for col in numeric_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
        
        
        if 'Team' in df.columns:
            df['Team'] = df['Team'].str.replace('Team ', '')
        
        
        if 'Sales_Channel' in df.columns:
            df['Sales_Channel'] = df['Sales_Channel'].str.strip()
        
        return df
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return pd.DataFrame()  

# Check login state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.view_mode = "Team"

if not st.session_state.logged_in:
    login_page()
    st.stop()


apply_custom_styles()


df = load_data("final_cleaned_dataset.csv")


if df.empty:
    st.error("No data available. Please check your data file.")
    st.stop()

# Sidebar configuration
with st.sidebar:
    st.title("📊 AI SALES DASHBOARD")
    st.markdown("---")
    
    
    st.markdown("**DASHBOARD VIEW**")
    view_mode = st.radio(
        "Select view mode:",
        ["Team", "Individual"],
        index=0 if st.session_state.view_mode == "Team" else 1,
        key="view_mode_selector"
    )
    st.session_state.view_mode = view_mode
    
    st.markdown("---")
    
    # Date range filter
    st.markdown("**DATE RANGE**")
    min_date, max_date = df["Date"].min(), df["Date"].max()
    date_range = st.date_input(
        "Select date range:",
        [min_date, max_date],
        min_value=min_date,
        max_value=max_date
    )
    
    st.markdown("---")
    
    # Team/Individual selection
    if st.session_state.view_mode == "Team":
        if 'Team' in df.columns:
            selected_team = st.selectbox(
                "SELECT TEAM",
                sorted(df['Team'].dropna().unique()),
                key="team_selector"
            )
        else:
            st.error("No 'Team' column found in data")
            st.stop()
    else:
        if 'Team_Member' in df.columns:
            selected_member = st.selectbox(
                "SELECT TEAM MEMBER",
                sorted(df["Team_Member"].dropna().unique()),
                key="member_selector"
            )
        else:
            st.error("No 'Team_Member' column found in data")
            st.stop()
    
    st.markdown("---")
    
    
    with st.expander("🔍 FILTER OPTIONS", expanded=False):
        if 'Country' in df.columns:
            countries = st.multiselect(
                "Filter by Country", 
                options=sorted(df["Country"].unique()), 
                default=sorted(df["Country"].unique())
            )
        else:
            countries = []
            st.warning("No 'Country' column found in data")
        
        if 'Product_Name' in df.columns:
            products = st.multiselect(
                "Filter by Products", 
                options=sorted(df["Product_Name"].unique()), 
                default=sorted(df["Product_Name"].unique())
            )
        else:
            products = []
            st.warning("No 'Product_Name' column found in data")
        
        if 'Sales_Channel' in df.columns:
            channels = st.multiselect(
                "Filter by Sales Channels", 
                options=sorted(df["Sales_Channel"].unique()), 
                default=sorted(df["Sales_Channel"].unique())
            )
        else:
            channels = []
            st.warning("No 'Sales_Channel' column found in data")
    
    st.markdown("---")
    
    # Data uploader
    st.markdown("**DATA MANAGEMENT**")
    uploaded = st.file_uploader("Upload new dataset", type=["csv"])
    if uploaded:
        try:
            df = pd.read_csv(uploaded)
            st.success("Dataset updated successfully!")
            st.rerun()
        except Exception as e:
            st.error(f"Error loading uploaded file: {str(e)}")
    
    st.markdown("---")
    if st.button("🚪 LOG OUT"):
        st.session_state.logged_in = False
        st.rerun()

# Filter data based on selections
try:
    if len(date_range) == 2:
        if st.session_state.view_mode == "Team":
            filtered_df = df[
                (df['Date'] >= pd.to_datetime(date_range[0])) & 
                (df['Date'] <= pd.to_datetime(date_range[1])) &
                (df["Country"].isin(countries if countries else df["Country"].unique())) &
                (df["Product_Name"].isin(products if products else df["Product_Name"].unique())) &
                (df["Sales_Channel"].isin(channels if channels else df["Sales_Channel"].unique())) &
                (df["Team"] == selected_team)
            ].copy()
        else:
            filtered_df = df[
                (df['Date'] >= pd.to_datetime(date_range[0])) & 
                (df['Date'] <= pd.to_datetime(date_range[1])) &
                (df["Country"].isin(countries if countries else df["Country"].unique())) &
                (df["Product_Name"].isin(products if products else df["Product_Name"].unique())) &
                (df["Sales_Channel"].isin(channels if channels else df["Sales_Channel"].unique())) &
                (df["Team_Member"] == selected_member)
            ].copy()
    else:
        st.warning("Please select a valid date range")
        filtered_df = df.copy()
except Exception as e:
    st.error(f"Error filtering data: {str(e)}")
    filtered_df = df.copy()

# Year separation for comparisons
current_year = filtered_df[filtered_df["Year"] == filtered_df["Year"].max()]
last_year = filtered_df[filtered_df["Year"] == (filtered_df["Year"].max() - 1)]

# TEAM VIEW
if st.session_state.view_mode == "Team":
    st.markdown(f"## <span class='header'>🏆 TEAM PERFORMANCE: {selected_team}</span>", unsafe_allow_html=True)
    
    # Key Metrics Row 
    cols = st.columns(4)
    
    with cols[0]:
        # Team size metric
        team_size = df[df["Team"] == selected_team]["Team_Member"].nunique()
        display_metric("TEAM SIZE", team_size, format_str="{:,.0f}")
    
    with cols[1]:
        # Units sold metric
        qty_c = current_year["Quantity_Sold"].sum() if not current_year.empty else 0
        qty_l = last_year["Quantity_Sold"].sum() if not last_year.empty else 0
        display_metric("UNITS SOLD", qty_c, qty_l, format_str="{:,.0f}")
    
    with cols[2]:
        # Revenue metric 
        rev_c = current_year["Total_Revenue"].sum() if not current_year.empty else 0
        rev_l = last_year["Total_Revenue"].sum() if not last_year.empty else 0
        display_metric("TOTAL REVENUE", rev_c, rev_l, None, "${:,.1f}M")
    
    with cols[3]:
        # CSAT metric
        csat_c = current_year["CSAT"].mean() if not current_year.empty and not current_year["CSAT"].isnull().all() else 0
        csat_l = last_year["CSAT"].mean() if not last_year.empty and not last_year["CSAT"].isnull().all() else 0
        display_metric("AVG CUSTOMER SATISFACTION", csat_c, csat_l, None, "{:.1f}/10", True)
    
    # Team Leaderboard 
    with st.expander("📊 View Team Leaderboard", expanded=False):
        st.plotly_chart(
            plot_team_leaderboard(current_year, last_year, "TEAM MEMBER PERFORMANCE (YoY)"),
            use_container_width=True
        )
    
    # Second row 
    cols = st.columns(2)
    
    with cols[0]:
        if not current_year.empty and not last_year.empty:
            st.plotly_chart(
                plot_team_revenue_trend(current_year, last_year, "TEAM REVENUE TREND VS TARGET (YoY)"),
                use_container_width=True
            )
    
    with cols[1]:
        if not current_year.empty and not last_year.empty:
            st.plotly_chart(
                plot_top_products_comparison(current_year, last_year, "TOP PRODUCTS PERFORMANCE (YoY)"),
                use_container_width=True
            )
    
    # Third row 
    cols = st.columns([2, 2, 1])
    
    with cols[0]:
        if not current_year.empty and not last_year.empty:
            st.plotly_chart(
                plot_channel_revenue(current_year, last_year, "REVENUE BY SALES CHANNEL (YoY)"),
                use_container_width=True
            )
    
    with cols[1]:
        if not current_year.empty and 'Country' in current_year.columns:
            st.plotly_chart(
                plot_sales_by_location(current_year, "SALES BY LOCATION"),
                use_container_width=True
            )
    
    with cols[2]:
        
        performance_score = min(150, rev_c / 10000000) if rev_c else 0  
        st.plotly_chart(
            create_performance_gauge(performance_score, "TEAM PERFORMANCE", 100),
            use_container_width=True
        )

# INDIVIDUAL VIEW
else:
    st.markdown(f"## <span class='header'>👤 INDIVIDUAL PERFORMANCE: {selected_member}</span>", unsafe_allow_html=True)
    
    
    rev_c = current_year["Total_Revenue"].sum() if not current_year.empty else 0
    rev_l = last_year["Total_Revenue"].sum() if not last_year.empty else 0
    csat_c = current_year["CSAT"].mean() if not current_year.empty and not current_year["CSAT"].isnull().all() else 0
    csat_l = last_year["CSAT"].mean() if not last_year.empty and not last_year["CSAT"].isnull().all() else 0
    cust_c = current_year["Customer_ID"].nunique() if not current_year.empty else 0
    cust_l = last_year["Customer_ID"].nunique() if not last_year.empty else 0
    qty_c = current_year["Quantity_Sold"].sum() if not current_year.empty else 0
    qty_l = last_year["Quantity_Sold"].sum() if not last_year.empty else 0
    
    # Key Metrics Row 
    cols = st.columns(4)
    
    with cols[0]:
        # Revenue metric 
        display_metric("TOTAL REVENUE", rev_c, rev_l, None, "${:,.1f}M")  

    with cols[1]:
        # New customers metric
        display_metric("NEW CUSTOMERS", cust_c, cust_l, format_str="{:,.0f}")

    with cols[2]:
        # Units sold metric
        display_metric("UNITS SOLD", qty_c, qty_l, format_str="{:,.0f}")

    with cols[3]:
        # CSAT metric
        display_metric("AVG CUSTOMER SATISFACTION", csat_c, csat_l, None, "{:.1f}/10", True)
    
    # Second row 
    cols = st.columns(2)
    
    with cols[0]:
        if not current_year.empty and not last_year.empty:
            st.plotly_chart(
                plot_individual_trend(current_year, last_year, "MONTHLY REVENUE TREND VS TARGET (YoY)", target=5000000),
                use_container_width=True
            )
    
    with cols[1]:
        if not current_year.empty and not last_year.empty:
            st.plotly_chart(
                plot_individual_products(current_year, last_year, "TOP PRODUCTS PERFORMANCE (YoY)"),
                use_container_width=True
            )
    
    # Third row 
    cols = st.columns([2, 2, 1])
    
    with cols[0]:
        if not current_year.empty and not last_year.empty:
            st.plotly_chart(
                plot_individual_channels(current_year, last_year, "SALES CHANNEL PERFORMANCE (YoY)"),
                use_container_width=True
            )
    
    with cols[1]:
        if not current_year.empty and not last_year.empty:
            st.plotly_chart(
                plot_individual_comparison(current_year, last_year, "ANNUAL PERFORMANCE COMPARISON"),
                use_container_width=True
            )
    
    with cols[2]:
        # Performance gauge 
        yoy_change = ((rev_c - rev_l) / rev_l) * 100 if rev_l != 0 else 0
        performance_score = min(150, 100 + yoy_change)  
        st.plotly_chart(
            create_performance_gauge(performance_score, "PERSONAL PERFORMANCE", 100),
            use_container_width=True
        )