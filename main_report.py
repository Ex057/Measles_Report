#!/usr/bin/env python3
"""
Disease Report Dashboard - Main Report Template
==============================================

Main template for the Measles surveillance report dashboard
with improved header layout and print-friendly styling.
"""

import streamlit as st
import streamlit.components.v1 as components
from datetime import datetime, timedelta
import os
import base64
import pandas as pd

# Page configuration
st.set_page_config(
    page_title="Measles Surveillance Report - Uganda",
    page_icon="⚕️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS to hide UI elements for production
st.markdown("""
<style>
/* Hide header action elements (link icons) */
[data-testid="stHeaderActionElements"] {
    display: none !important;
}
.st-emotion-cache-gi0tri {
    display: none !important;
}
.st-emotion-cache-yinll1 {
    display: none !important;
}

/* Hide deploy button */
.stDeployButton {
    display: none !important;
}

/* Hide main menu (hamburger menu) */
#MainMenu {
    visibility: hidden !important;
}

/* Hide footer */
footer {
    visibility: hidden !important;
}

/* Hide "Made with Streamlit" */
#stDecoration {
    display: none !important;
}

/* Adjust main container margin */
.reportview-container {
    margin-top: -2em;
}
</style>
""", unsafe_allow_html=True)

def load_css_styles(css_file):
    """Load custom CSS styles from an external file"""
    with open(css_file) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def get_image_base64(image_path):
    """Convert image to base64 string for embedding"""
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except:
        return ""

def get_logo_base64():
    """Get base64 encoded logo for header"""
    logo_paths = ["moh_logo.PNG", "moh_logo.png", "moh_logo.jpg", "moh_logo.jpeg"]
    for path in logo_paths:
        if os.path.exists(path):
            return get_image_base64(path)
    # Return placeholder if no logo found
    return ""

def get_print_chart_config():
    """Get standardized chart configuration for print output"""
    return {
        'displayModeBar': False,
        'staticPlot': True,
        'responsive': True,
        'toImageButtonOptions': {
            'format': 'png',
            'filename': 'chart',
            'height': 400,
            'width': 700,
            'scale': 2
        }
    }

def get_standard_color_palette():
    """Get standardized color palette for consistent chart styling"""
    return [
        '#1e3a5f',  # Primary dark blue
        '#2c5aa0',  # Medium blue  
        '#3498db',  # Light blue
        '#e74c3c',  # Red
        '#f39c12',  # Orange
        '#27ae60',  # Green
        '#9b59b6',  # Purple
        '#34495e',  # Dark gray
        '#16a085',  # Teal
        '#d35400'   # Dark orange
    ]

# SIDEBAR COMMENTED OUT - NOW USING URL PARAMETERS ONLY
def get_dynamic_parameters():
    """Get parameters from URL only - no sidebar"""
    
    # Parse URL parameters (using clean query format)
    year_from_url = st.query_params.get("year") or st.query_params.get("y")
    month_from_url = st.query_params.get("month") or st.query_params.get("m") 
    location_from_url = st.query_params.get("location") or st.query_params.get("l")
    
    # Default values
    current_year = datetime.now().year
    default_location = "National Level (MOH)"
    default_month = f"All Months {current_year}"
    
    # Process location parameter
    if location_from_url:
        location_map = {
            "national": "National Level (MOH)",
            "regional": "Regional Level", 
            "district": "District Level"
        }
        selected_location = location_map.get(location_from_url.lower(), location_from_url)
    else:
        selected_location = default_location
    
    # Process year parameter
    if year_from_url:
        try:
            selected_year = int(year_from_url)
        except (ValueError, TypeError):
            selected_year = current_year
    else:
        selected_year = current_year
    
    # Process month parameter
    if month_from_url:
        if month_from_url.lower() == "all":
            selected_month = f"All Months {selected_year}"
            month_display = "All Months"
        else:
            # Check if it's a digit (1-12)
            try:
                month_num = int(month_from_url)
                if 1 <= month_num <= 12:
                    digit_to_month = {
                        1: "January", 2: "February", 3: "March", 4: "April",
                        5: "May", 6: "June", 7: "July", 8: "August", 
                        9: "September", 10: "October", 11: "November", 12: "December"
                    }
                    month_name = digit_to_month[month_num]
                    selected_month = f"{month_name} {selected_year}"
                    month_display = month_name
                else:
                    selected_month = default_month
                    month_display = "All Months"
            except (ValueError, TypeError):
                # Try name mapping
                month_map = {
                    "january": "January", "jan": "January",
                    "february": "February", "feb": "February", 
                    "march": "March", "mar": "March",
                    "april": "April", "apr": "April",
                    "may": "May",
                    "june": "June", "jun": "June",
                    "july": "July", "jul": "July",
                    "august": "August", "aug": "August",
                    "september": "September", "sep": "September",
                    "october": "October", "oct": "October",
                    "november": "November", "nov": "November",
                    "december": "December", "dec": "December"
                }
                month_name = month_map.get(month_from_url.lower())
                if month_name:
                    selected_month = f"{month_name} {selected_year}"
                    month_display = month_name
                else:
                    selected_month = default_month
                    month_display = "All Months"
    else:
        selected_month = default_month
        month_display = "All Months"
    
    # No URL updating needed since we're reading from URL only
    
    
    # Determine coverage level 
    if "National Level" in selected_location:
        coverage = "National"
    else:
        coverage = selected_location
    
    
    return {
        'disease': 'Measles',
        'location': selected_location,
        'year': selected_year,
        'month': selected_month,
        'month_display': month_display,
        'coverage': coverage
    }

def render_main_header(params):
    """Render the official Uganda Ministry of Health report header."""
    
    # Get parameter values
    year = params.get('year', '2025')
    month = params.get('month_display', 'All Months')
    coverage = params.get('coverage', 'National')
    
    # Handle logo loading
    logo_html = ""
    if os.path.exists("moh_logo.png") or os.path.exists("moh_logo.PNG"):
        logo_path = "moh_logo.PNG" if os.path.exists("moh_logo.PNG") else "moh_logo.png"
        try:
            with open(logo_path, "rb") as img_file:
                logo_base64 = base64.b64encode(img_file.read()).decode()
                logo_html = f'<img src="data:image/png;base64,{logo_base64}" class="national-emblem" alt="Uganda Coat of Arms" />'
        except:
            logo_html = '<div class="logo-placeholder">COAT OF ARMS</div>'
    else:
        logo_html = '<div class="logo-placeholder">COAT OF ARMS</div>'
    
    st.html(f"""
    <div class="official-report-header">
        <div class="emblem-container">
            {logo_html}
        </div>
        
        <div class="ministry-info">
            <div class="republic-title">THE REPUBLIC OF UGANDA</div>
            <div class="ministry-title">MINISTRY OF HEALTH</div>
        </div>
        
        <div class="report-title">MEASLES</div>
        
        <div class="report-subtitle">Weekly Measles Situation Report</div>
        
        <div class="simple-flag">
            <div class="flag-line black-line"></div>
            <div class="flag-line yellow-line"></div>
            <div class="flag-line red-line"></div>
        </div>
        
        <div class="report-metadata">
            Year: {year} | Month: {month} | Coverage: {coverage}
        </div>
        
        <div class="report-introduction">
            <strong>Introduction:</strong><br>
            This report is designed to provide MoH officials, program managers, and stakeholders with a summary of key Measles surveillance indicators, including total measles cases, measles case fatality rate, among others.
        </div>
    </div>
    
    <style>
    /* Print-friendly and A4 optimized styling */
    @media print {{
        .official-report-header {{
            page-break-inside: avoid;
            margin: 0.5in 0.75in;
            padding: 1rem 0;
        }}
        * {{
            -webkit-print-color-adjust: exact !important;
            color-adjust: exact !important;
            print-color-adjust: exact !important;
        }}
    }}
    
    .official-report-header {{
        text-align: center;
        padding: 1.5rem 1rem 2rem 1rem;
        background: #ffffff;
        border-bottom: 2pt solid #1e3a5f;
        margin: 0 auto 1.5rem auto;
        max-width: 8.27in; /* A4 width minus margins */
        font-family: Arial, Helvetica, sans-serif;
        line-height: 1.4;
    }}
    
    .emblem-container {{
        margin-bottom: 1.5rem;
    }}
    
    .national-emblem {{
        width: 100px;
        height: auto;
        max-height: 120px;
        image-rendering: -webkit-optimize-contrast;
        image-rendering: crisp-edges;
    }}
    
    .logo-placeholder {{
        font-size: 12pt;
        color: #1e3a5f;
        font-weight: bold;
        padding: 0.75rem;
        border: 1.5pt solid #1e3a5f;
        border-radius: 6px;
        display: inline-block;
        margin-bottom: 1rem;
        background: #f8f9fa;
    }}
    
    .ministry-info {{
        margin-bottom: 1.5rem;
    }}
    
    .republic-title {{
        font-size: 11pt;
        font-weight: bold;
        color: #1e3a5f;
        text-transform: uppercase;
        letter-spacing: 0.5pt;
        margin-bottom: 0.2rem;
        line-height: 1.2;
    }}

    .ministry-title {{
        font-size: 10pt;
        font-weight: bold;
        color: #1e3a5f;
        text-transform: uppercase;
        letter-spacing: 0.3pt;
        line-height: 1.2;
    }}

    .report-title {{
        font-size: 28pt;
        font-weight: 900;
        color: #1e3a5f;
        text-transform: uppercase;
        letter-spacing: 2.5pt;
        margin: 1rem 0 0.6rem 0;
        line-height: 1.1;
    }}
    
    .report-subtitle {{
        font-size: 16pt;
        font-weight: 600;
        color: #495057;
        margin-bottom: 1.5rem;
        font-style: italic;
        line-height: 1.3;
    }}
    
    .simple-flag {{
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        margin: 1.5rem auto;
        max-width: 5in;
        border: 0.5pt solid #999;
        box-shadow: 0 1pt 2pt rgba(0,0,0,0.1);
    }}
    
    .flag-line {{
        width: 100%;
        height: 8pt;
        border: none;
        margin: 0;
        padding: 0;
    }}
    
    .black-line {{
        background-color: #000000 !important;
    }}
    
    .yellow-line {{
        background-color: #FCDC00 !important;
    }}
    
    .red-line {{
        background-color: #D90000 !important;
    }}
    
    .report-metadata {{
        font-size: 12pt;
        color: #495057;
        margin-top: 1.2rem;
        font-weight: 500;
        padding: 0.5rem 0.75rem;
        background: rgba(108, 117, 125, 0.08);
        border-radius: 3pt;
        display: inline-block;
        line-height: 1.3;
    }}
    
    .report-introduction {{
        font-size: 11pt;
        color: #333;
        margin-top: 1rem;
        padding: 0.75rem 1rem;
        background: rgba(13, 110, 253, 0.05);
        border-left: 4px solid #0d6efd;
        border-radius: 4pt;
        line-height: 1.5;
    }}
    
    .report-introduction strong {{
        color: #0d6efd;
        font-weight: 600;
    }}
    
    @media (max-width: 768px) {{
        .report-title {{
            font-size: 2rem;
            letter-spacing: 2px;
        }}
        
        .republic-title {{
            font-size: 1rem;
        }}
        
        .ministry-title {{
            font-size: 0.85rem;
        }}
        
        .simple-flag {{
            max-width: 300px;
        }}
    }}
    </style>
    """)

        
            
        
        
        



def main():
    """Main function to run the Measles report template"""
    
    
    # Add comprehensive print-friendly styles with optimized spacing
    st.markdown("""
    <style>
    
    
    /* Ensure all charts are responsive */
    .js-plotly-plot, .plotly {
        width: 100% !important;
        height: auto !important;
    }
    
    /* Responsive columns for wide screens */
    [data-testid="column"] {
        padding: 0.5rem;
    }
    
    /* Mobile responsiveness for tables and text */
    @media (max-width: 768px) {
        .stDataFrame {
            font-size: 12px;
        }
        
        .metric-value {
            font-size: 1.5rem;
        }
    }
    
    /* Print Styles - Always Non-Wide Mode Layout */
    @media print {
        /* Hide sidebar and navigation elements */
        .css-1d391kg, .css-1vencpc, .stSidebar, [data-testid="stSidebar"] {
            display: none !important;
        }
        
        /* Enhanced map visibility and sizing for print */
        .js-plotly-plot, .plotly, .plotly-graph-div {
            width: 100% !important;
            height: 450px !important;
            min-height: 450px !important;
            display: block !important;
            visibility: visible !important;
            opacity: 1 !important;
            background: white !important;
            -webkit-print-color-adjust: exact !important;
            color-adjust: exact !important;
            print-color-adjust: exact !important;
            border: 1px solid #ddd !important;
            margin: 0.5rem 0 !important;
        }
        
        /* Ensure map containers are visible with better sizing */
        .stPlotlyChart {
            display: block !important;
            visibility: visible !important;
            height: 450px !important;
            min-height: 450px !important;
            width: 100% !important;
            page-break-inside: avoid;
            background: white !important;
            border: 1px solid #ddd !important;
            border-radius: 4px !important;
            margin: 0.5rem 0 1rem 0 !important;
        }
        
        /* Fix map text and legend visibility */
        .js-plotly-plot .legendtext,
        .js-plotly-plot .colorbar text,
        .js-plotly-plot text {
            font-size: 10pt !important;
            fill: #000 !important;
            color: #000 !important;
        }
        
        /* Ensure choropleth maps are properly rendered */
        .js-plotly-plot .geo path {
            stroke: #333 !important;
            stroke-width: 0.5px !important;
        }
        
        /* Map title styling for print */
        .js-plotly-plot .gtitle {
            font-size: 14pt !important;
            font-weight: bold !important;
            fill: #1e3a5f !important;
        }
        
        /* Force non-wide mode layout regardless of UI setting */
        .main .block-container {
            max-width: 730px !important; /* Standard Streamlit non-wide width */
            margin: 0 auto !important;
            padding: 1rem !important;
        }
        
        .stApp {
            max-width: 730px !important;
            margin: 0 auto;
        }
        
        /* Enhanced page setup for better print quality */
        @page {
            size: A4;
            margin: 0.75in;
            margin-top: 0.5in;
            margin-bottom: 0.75in;
        }
        
        body { 
            margin: 0;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            font-size: 11pt;
            line-height: 1.5;
            color: #000;
            background: white;
        }
        
        .stApp { 
            background-color: white !important;
            color: #000 !important;
        }
        
        /* Ensure all text is black for print */
        * {
            color: #000 !important;
            -webkit-print-color-adjust: exact !important;
            print-color-adjust: exact !important;
        }
        
        /* Enhanced typography hierarchy for print */
        h1, h2, h3, h4, h5, h6 { 
            page-break-after: avoid;
            margin-top: 1.5em;
            margin-bottom: 0.6em;
            line-height: 1.3;
            font-weight: bold;
            color: #000 !important;
        }
        
        h1 { 
            font-size: 22pt; 
            color: #1e3a5f !important; 
            text-align: center;
            margin-bottom: 1em;
            border-bottom: 2pt solid #1e3a5f;
            padding-bottom: 0.3em;
        }
        h2 { 
            font-size: 18pt; 
            color: #1e3a5f !important; 
            border-bottom: 1pt solid #1e3a5f;
            padding-bottom: 0.2em;
        }
        h3 { 
            font-size: 15pt; 
            color: #1e3a5f !important; 
            margin-top: 1.2em;
        }
        h4 { 
            font-size: 13pt; 
            color: #2c3e50 !important; 
            margin-top: 1em;
        }
        h5 { 
            font-size: 11pt; 
            color: #2c3e50 !important; 
            margin-top: 0.8em;
        }
        
        /* Enhanced content spacing and readability */
        p, div { 
            margin: 0.5em 0;
            orphans: 3;
            widows: 3;
            font-size: 11pt;
            line-height: 1.4;
        }
        
        /* Table styling for better print visibility */
        .stDataFrame, .stTable {
            page-break-inside: avoid;
            margin: 0.5em 0;
            border: 1px solid #ddd !important;
            border-radius: 4px !important;
            background: white !important;
        }
        
        .stDataFrame table {
            font-size: 10pt !important;
            border-collapse: collapse !important;
            width: 100% !important;
        }
        
        .stDataFrame th {
            background: #f8f9fa !important;
            color: #000 !important;
            font-weight: bold !important;
            padding: 0.3em !important;
            border-bottom: 1px solid #ddd !important;
        }
        
        .stDataFrame td {
            padding: 0.3em !important;
            border-bottom: 1px solid #eee !important;
            color: #000 !important;
        }
        
        /* Metrics styling */
        .metric-container {
            page-break-inside: avoid;
            margin: 0.5em 0;
            padding: 0.3em;
            border: 1px solid #ddd;
            background: #f8f9fa !important;
            border-radius: 4px;
        }
        
        /* Section breaks */
        .section-divider {
            page-break-before: auto;
            margin: 1.5em 0 1em 0;
            border-top: 2px solid #1e3a5f;
            padding-top: 0.5em;
        }
        
        /* Chart styling - prevent overlapping and fix sizing */
        .stPlotlyChart { 
            margin: 0.6rem 0;
            width: 100%;
            max-width: 100%;
            box-sizing: border-box;
            min-height: 300px; /* Ensure minimum readable size */
        }
        
        /* Standardize chart dimensions for print */
        .stPlotlyChart .js-plotly-plot {
            width: 100% !important;
            height: auto !important;
            min-height: 300px !important;
        }
        
        /* Ensure charts are properly sized in columns */
        .stColumn .stPlotlyChart {
            min-height: 250px;
        }
        
        /* Single full-width charts should be larger */
        .stPlotlyChart:not(.stColumn .stPlotlyChart) {
            min-height: 350px;
        }
        
        .plotly .modebar { 
            display: none !important; 
        }
        
        /* Improve chart text readability for print */
        .js-plotly-plot .gtitle {
            font-size: 12pt !important;
            font-weight: bold !important;
        }
        
        .js-plotly-plot .xtitle, .js-plotly-plot .ytitle {
            font-size: 10pt !important;
            font-weight: 600 !important;
        }
        
        .js-plotly-plot .xtick, .js-plotly-plot .ytick {
            font-size: 8pt !important;
        }
        
        /* Legend styling for print */
        .js-plotly-plot .legend {
            font-size: 8pt !important;
        }
        
        /* Standardized chart styling for print */
        .stPlotlyChart .js-plotly-plot {
            background: white !important;
            border: 1pt solid #dee2e6 !important;
            border-radius: 2pt !important;
        }
        
        /* Chart title styling - professional appearance */
        .chart-section-title {
            font-size: 12pt !important;
            font-weight: bold !important;
            color: #1e3a5f !important;
            margin: 0.2rem 0 0.1rem 0 !important;
            text-align: left !important;
        }
        
        /* Ensure chart containers have consistent styling */
        .stPlotlyChart {
            border-radius: 2pt;
            overflow: hidden;
        }
        
        /* Enhanced section hierarchy styling */
        .section-header h2 {
            background: #1e3a5f !important;
            color: white !important;
            padding: 0.4rem 0.8rem !important;
            margin: 0.6rem 0 0.2rem 0 !important;
            font-size: 14pt !important;
            font-weight: bold !important;
            text-transform: uppercase !important;
            letter-spacing: 0.5pt !important;
            border-radius: 3pt !important;
            text-align: center !important;
        }
        
        .subsection-header h3 {
            background: #f8f9fa !important;
            color: #1e3a5f !important;
            padding: 0.3rem 0.6rem !important;
            margin: 0.3rem 0 0.15rem 0 !important;
            font-size: 12pt !important;
            font-weight: 600 !important;
            border-left: 4pt solid #1e3a5f !important;
            border-radius: 0 3pt 3pt 0 !important;
        }
        
        .subsection-header h4 {
            color: #2c3e50 !important;
            padding: 0.2rem 0.4rem !important;
            margin: 0.2rem 0 0.1rem 0 !important;
            font-size: 11pt !important;
            font-weight: 600 !important;
            border-bottom: 1pt solid #dee2e6 !important;
        }
        
        .plotly .plotly-graph-div {
            width: 100% !important;
            max-width: 100% !important;
            box-sizing: border-box !important;
            margin: 0 !important;
            padding: 0 !important;
        }
        
        /* Fix chart containers */
        .js-plotly-plot {
            width: 100% !important;
            max-width: 100% !important;
        }
        
        /* Table styling */
        table, .dataframe { 
            width: 100%;
            border-collapse: collapse;
            margin: 0.8em 0;
            font-size: 10pt;
        }
        
        table th {
            background-color: #f8f9fa !important;
            font-weight: bold;
            padding: 6pt 8pt;
            border: 1pt solid #dee2e6;
            text-align: left;
        }
        
        table td {
            padding: 6pt 8pt;
            border: 1pt solid #dee2e6;
            vertical-align: top;
        }
        
        /* Column layouts - better space utilization and no overlaps */
        .stColumns { 
            display: flex;
            gap: 0.5rem;
            width: 100%;
            margin: 0.4rem 0;
            box-sizing: border-box;
        }
        
        .stColumn { 
            flex: 1;
            min-width: 0;
            padding: 0 0.2rem;
            box-sizing: border-box;
            overflow: hidden;
        }
        
        div[data-testid="column"] { 
            flex: 1;
            min-width: 0;
            padding: 0 0.2rem;
            box-sizing: border-box;
            overflow: hidden;
        }
        
        /* Strict content sizing to prevent overlaps */
        .stColumn > div,
        div[data-testid="column"] > div {
            width: 100% !important;
            max-width: 100% !important;
            box-sizing: border-box !important;
            overflow: hidden !important;
        }
        
        /* Specific fixes for charts in columns */
        .stColumn .stPlotlyChart,
        div[data-testid="column"] .stPlotlyChart {
            width: 100% !important;
            max-width: 100% !important;
            margin: 0.3rem 0;
        }
        
        .stColumn .plotly,
        div[data-testid="column"] .plotly {
            width: 100% !important;
            max-width: 100% !important;
        }
        
        /* Section dividers */
        hr {
            margin: 1.2em 0;
            border: none;
            border-top: 1pt solid #dee2e6;
        }
        
        /* Compact info boxes */
        .stInfo, .stWarning, .stError, .stSuccess {
            margin: 0.8em 0;
            padding: 0.6em 0.8em;
            border-radius: 4px;
            font-size: 10pt;
        }
        
        /* Element container spacing - optimized */
        .element-container {
            margin-bottom: 0.4rem;
        }
        
        /* Markdown elements - tighter spacing */
        .stMarkdown {
            margin: 0.25rem 0;
        }
        
        /* Additional space optimization */
        .stSelectbox, .stMultiselect {
            margin-bottom: 0.3rem;
        }
        
        /* Table container optimization */
        .print-table-container {
            margin: 0.5rem 0;
        }
        
        /* Fix for specific visual overlaps */
        .stPlotlyChart + .stPlotlyChart {
            margin-top: 0.6rem;
        }
        
        /* Better spacing for headers within sections */
        .stMarkdown h4 + .stPlotlyChart,
        .stMarkdown h5 + .stPlotlyChart {
            margin-top: 0.4rem;
        }
        
        /* Improve page breaking behavior */
        .stMarkdown h3, .stMarkdown h4 {
            page-break-before: auto;
            page-break-after: auto;
        }
        
        /* Allow natural page breaks for better flow */
        .element-container, .stPlotlyChart, table {
            page-break-inside: auto;
        }
        
        /* Print utility classes */
        .print-only {
            display: block !important;
        }
        
        .no-print {
            display: none !important;
        }
    }
    
    /* A4 Layout Optimization - Works for both wide and non-wide mode */
    .main .block-container {
        max-width: min(8.27in, 100%);
        margin: 0 auto;
        font-family: Arial, Helvetica, sans-serif;
        padding: 0.5rem 0.75rem;
    }
    
    /* Non-wide mode optimization */
    @media (max-width: 1200px) {
        .main .block-container {
            max-width: 100%;
            padding: 0.3rem 0.5rem;
        }
        
        /* Adjust column gaps for smaller screens */
        .stColumns { gap: 0.25rem; }
        .stColumn { padding: 0 0.125rem; }
        div[data-testid="column"] { padding: 0 0.125rem; }
        
        /* Reduce font sizes slightly for better fit */
        h1 { font-size: 18pt; }
        h2 { font-size: 16pt; }
        h3 { font-size: 13pt; }
        h4 { font-size: 11pt; }
        h5 { font-size: 10pt; }
        p, div { font-size: 9pt; }
    }
    
    /* Ultra-compact Typography - maximized print density */
    h1 { font-size: 20pt; line-height: 1.0; margin: 0.2rem 0 0.1rem 0; }
    h2 { font-size: 18pt; line-height: 1.0; margin: 0.15rem 0 0.08rem 0; }
    h3 { font-size: 14pt; line-height: 1.0; margin: 0.1rem 0 0.05rem 0; }
    h4 { font-size: 12pt; line-height: 1.0; margin: 0.08rem 0 0.04rem 0; }
    h5 { font-size: 11pt; line-height: 1.0; margin: 0.05rem 0 0.02rem 0; }
    p, div { font-size: 10pt; line-height: 1.1; margin: 0.05rem 0; }
    
    /* Ultra-compact Chart and Visual Containers */
    .stPlotlyChart {
        margin: 0.08rem 0 0.15rem 0;
    }
    
    /* Ultra-compact Table Styling */
    .print-table-container {
        margin: 0.08rem 0 0.15rem 0;
        overflow: visible;
    }
    
    /* Minimal Whitespace and Spacing */
    .section-break { margin: 0.2rem 0; }
    .chart-title { margin-bottom: 0.05rem; color: #1e3a5f; }
    
    /* Column Optimization - Responsive for 3-column layouts */
    .stColumns { 
        gap: 0.5rem; 
    }
    .stColumn { 
        padding: 0 0.25rem; 
        min-width: 0; /* Allow columns to shrink properly */
    }
    
    /* Streamlit Element Spacing - Further reduced for better print */
    .element-container { margin-bottom: 0.3rem; }
    .stMarkdown { margin-bottom: 0.15rem; }
    
    /* Compact sections with tighter spacing */
    div[data-testid="column"] { padding: 0 0.2rem; }
    
    /* Reduce spacing around headers */
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown h4, .stMarkdown h5 {
        margin-top: 0.3rem;
        margin-bottom: 0.15rem;
    }
    
    /* Tighter spacing for charts and plots */
    .stPlotlyChart .js-plotly-plot { margin: 0; }
    .stPlotlyChart .plot-container { margin: 0; }
    
    /* Reduce spacing around tables */
    .print-table-container table {
        margin: 0.2rem 0;
    }
    
    /* Minimize divider spacing */
    .element-container div[role="separator"] {
        margin: 0.4rem 0;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Load additional CSS if available
    try:
        load_css_styles("styles.css")
    except:
        pass
    
    # Get dynamic parameters from sidebar
    params = get_dynamic_parameters()
    
    # Render the main header section
    render_main_header(params)
    
    # Add Executive Summary section (print-optimized)
    st.markdown("""
    <style>
    @media print {
        .executive-summary {
            background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
            border: 2pt solid #1e3a5f;
            padding: 1rem;
            margin: 0.5rem 0 1rem 0;
            border-radius: 8pt;
            page-break-inside: avoid;
            box-shadow: 0 2pt 4pt rgba(0,0,0,0.1);
        }
        .executive-summary h3 {
            color: #1e3a5f;
            margin: 0 0 0.8rem 0;
            font-size: 16pt;
            text-align: center;
            font-weight: bold;
            text-transform: uppercase;
            letter-spacing: 1pt;
        }
        .summary-table {
            width: 100%;
            border-collapse: collapse;
            margin: 0.8rem 0 0 0;
            background: white !important;
            border: 2pt solid #1e3a5f !important;
            border-radius: 6pt;
            overflow: hidden;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1) !important;
        }
        .summary-header {
            background: #1e3a5f !important;
            color: white !important;
            font-weight: 700 !important;
            font-size: 10pt !important;
            padding: 0.8rem 0.5rem !important;
            text-align: center !important;
            text-transform: uppercase !important;
            letter-spacing: 0.5pt !important;
            border-right: 1pt solid #2c5aa0 !important;
        }
        .summary-header:last-child {
            border-right: none !important;
        }
        .summary-data {
            background: white !important;
            color: #495057 !important;
            font-size: 11pt !important;
            padding: 1rem 0.5rem !important;
            text-align: center !important;
            vertical-align: middle !important;
            border-right: 1pt solid #dee2e6 !important;
        }
        .summary-data:last-child {
            border-right: none !important;
        }
        .summary-data strong {
            color: #1e3a5f !important;
            font-weight: 800 !important;
            font-size: 14pt !important;
            display: block !important;
            margin-bottom: 0.2rem !important;
        }
        .summary-detail {
            color: #6c757d !important;
            font-size: 8pt !important;
            font-weight: 500 !important;
            text-transform: lowercase !important;
        }
    }
    
    /* Apply some print styles to main UI for better appearance */
    .executive-summary {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        border: 2pt solid #1e3a5f;
        padding: 1rem;
        margin: 0.5rem 0 1rem 0;
        border-radius: 8pt;
        box-shadow: 0 2pt 4px rgba(0,0,0,0.1);
    }
    .executive-summary h3 {
        color: #1e3a5f;
        margin: 0 0 0.8rem 0;
        font-size: 16pt;
        text-align: center;
        font-weight: bold;
        text-transform: uppercase;
        letter-spacing: 1pt;
    }
    .summary-table {
        width: 100%;
        border-collapse: collapse;
        margin: 0.8rem 0 0 0;
        background: white;
        border: 2pt solid #1e3a5f;
        border-radius: 6pt;
        overflow: hidden;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .summary-header {
        background: #1e3a5f;
        color: white;
        font-weight: 700;
        font-size: 10pt;
        padding: 0.8rem 0.5rem;
        text-align: center;
        text-transform: uppercase;
        letter-spacing: 0.5pt;
        border-right: 1pt solid #2c5aa0;
    }
    .summary-header:last-child {
        border-right: none;
    }
    .summary-data {
        background: white;
        color: #495057;
        font-size: 11pt;
        padding: 1rem 0.5rem;
        text-align: center;
        vertical-align: middle;
        border-right: 1pt solid #dee2e6;
    }
    .summary-data:last-child {
        border-right: none;
    }
    .summary-data strong {
        color: #1e3a5f;
        font-weight: 800;
        font-size: 14pt;
        display: block;
        margin-bottom: 0.2rem;
    }
    .summary-detail {
        color: #6c757d;
        font-size: 8pt;
        font-weight: 500;
        text-transform: lowercase;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Generate Executive Summary Data
    try:
        # Import the functions we know exist
        from data_fetcher import (
            get_measles_weekly_data, 
            get_measles_age_sex_distribution,
            get_measles_top_10_districts,
            get_measles_cases_last_24h,
            get_measles_total_deaths
        )
        
        # Get real data for summary
        weekly_data = get_measles_weekly_data()
        district_data = get_measles_top_10_districts()
        cases_24h = get_measles_cases_last_24h()
        total_deaths = get_measles_total_deaths()  # Get consistent death data
        
        # Calculate summary statistics
        summary_stats = {}
        if not weekly_data.empty:
            summary_stats['total_cases'] = int(weekly_data['Cumulative Confirmed Cases'].iloc[0]) if len(weekly_data) > 0 else 0
            summary_stats['cases_last_24h'] = cases_24h  # Use actual 24h data
        else:
            summary_stats['total_cases'] = 0
            summary_stats['cases_last_24h'] = cases_24h
            
        # Use consistent death data from the same source as cases
        summary_stats['deaths'] = total_deaths
        
        if not district_data.empty:
            summary_stats['affected_districts'] = len(district_data)
            summary_stats['top_district'] = district_data['District'].iloc[0] if len(district_data) > 0 else 'N/A'
            summary_stats['top_district_cases'] = int(district_data['Total Cases'].iloc[0]) if len(district_data) > 0 else 0
        else:
            summary_stats['affected_districts'] = 0
            summary_stats['top_district'] = 'N/A'
            summary_stats['top_district_cases'] = 0
            
        # Determine trend (simple logic)
        if len(weekly_data) >= 2:
            current_week = weekly_data['Weekly Confirmed Cases'].iloc[0]
            prev_week = weekly_data['Weekly Confirmed Cases'].iloc[1] if len(weekly_data) > 1 else current_week
            if current_week > prev_week:
                summary_stats['trend'] = 'Increasing'
            elif current_week < prev_week:
                summary_stats['trend'] = 'Decreasing'
            else:
                summary_stats['trend'] = 'Stable'
        else:
            summary_stats['trend'] = 'Stable'
        
        # Calculate CFR
        total_cases = summary_stats.get('total_cases', 0)
        total_deaths = summary_stats.get('deaths', 0)
        cfr = (total_deaths / total_cases * 100) if total_cases > 0 else 0
        
        # Create executive summary section with horizontal table format
        st.markdown(f"""
        <div class="executive-summary">
            <h3>EXECUTIVE SUMMARY</h3>
            <table class="summary-table">
                <thead>
                    <tr>
                        <th class="summary-header">Total Cases</th>
                        <th class="summary-header">New Last 24h</th>
                        <th class="summary-header">Deaths</th>
                        <th class="summary-header">CFR</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td class="summary-data"><strong>{total_cases:,}</strong><br><span class="summary-detail">confirmed cases</span></td>
                        <td class="summary-data"><strong>{summary_stats.get('cases_last_24h', 0):,}</strong><br><span class="summary-detail">new cases</span></td>
                        <td class="summary-data"><strong>{total_deaths:,}</strong><br><span class="summary-detail">deaths</span></td>
                        <td class="summary-data"><strong>{cfr:.2f}%</strong><br><span class="summary-detail">fatality rate</span></td>
                    </tr>
                </tbody>
            </table>
        </div>
        """, unsafe_allow_html=True)
        
    except Exception as e:
        # Fallback summary with basic info
        st.markdown(f"""
        <div class="executive-summary">
            <h3>EXECUTIVE SUMMARY</h3>
            <div class="key-metrics">
                <div class="metric-box">
                    <div class="metric-number">-</div>
                    <div class="metric-label">Total Cases</div>
                </div>
                <div class="metric-box">
                    <div class="metric-number">-</div>
                    <div class="metric-label">This Week</div>
                </div>
                <div class="metric-box">
                    <div class="metric-number">-</div>
                    <div class="metric-label">Deaths</div>
                </div>
                <div class="metric-box">
                    <div class="metric-number">-</div>
                    <div class="metric-label">Districts</div>
                </div>
            </div>
            <p class="summary-text">
                <strong>Period:</strong> {params['month']} {params['year']} | 
                <strong>Location:</strong> {params['location']} | 
                <strong>Status:</strong> Data loading...
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    
    # Import data fetching functions
    try:
        from data_fetcher import get_measles_weekly_data
        
        # Add print-friendly container for entire table section
        st.markdown('<div class="print-table-container">', unsafe_allow_html=True)
        
        st.markdown('<div class="subsection-header"><h3>Last 10 Epidemiological Weeks - Measles Cases</h3></div>', unsafe_allow_html=True)
        
        # Get and display the weekly epidemiological data (CUMULATIVE - ALL YEARS)
        # This table should show cumulative data from all years, not filtered by parameters
        weekly_data = get_measles_weekly_data()  # No parameters - get all data
        
        if not weekly_data.empty:
            
            # Convert float years/weeks to integers for better display
            display_data = weekly_data.copy()
            display_data['Year'] = display_data['Year'].astype(int)
            display_data['Epi Week'] = display_data['Epi Week'].astype(int)
            
            # Create compact HTML table for better print formatting
            def create_compact_table(df):
                html_rows = []
                # Header row
                headers = ['Year', 'Epi Week', 'Weekly Cases', 'Cumulative Cases', 'Change (%)']
                header_row = ''.join([f'<th style="padding: 6px 10px; border: 1px solid #dee2e6; font-weight: 600; font-size: 12px; text-align: center;">{h}</th>' for h in headers])
                html_rows.append(f'<tr>{header_row}</tr>')

                # Data rows
                for idx, row in df.iterrows():
                    year = int(row['Year'])
                    week = int(row['Epi Week'])
                    weekly = int(row['Weekly Confirmed Cases'])
                    cumulative = int(row['Cumulative Confirmed Cases'])
                    change = row['Percent Change (%)']

                    # Format percent change with proper handling of NULL values
                    if pd.isna(change) or change is None:
                        change_str = '-'
                        change_color = '#000000'
                    else:
                        change_val = float(change)
                        change_str = f'{change_val:+.1f}%' if change_val != 0 else '0.0%'
                        change_color = '#000000'

                    data_row = f'''
                    <td style="padding: 6px 10px; border: 1px solid #dee2e6; text-align: center; font-size: 13px;">{year}</td>
                    <td style="padding: 6px 10px; border: 1px solid #dee2e6; text-align: center; font-size: 13px;">{week}</td>
                    <td style="padding: 6px 10px; border: 1px solid #dee2e6; text-align: center; font-size: 13px; font-weight: 600;">{weekly:,}</td>
                    <td style="padding: 6px 10px; border: 1px solid #dee2e6; text-align: center; font-size: 13px; font-weight: 600;">{cumulative:,}</td>
                    <td style="padding: 6px 10px; border: 1px solid #dee2e6; text-align: center; font-size: 13px; font-weight: 600; color: {change_color};">{change_str}</td>
                    '''
                    html_rows.append(f'<tr>{data_row}</tr>')
                
                return f'''
                <div style="overflow-x: auto; margin: 1rem 0;">
                    <table style="width: 100%; border-collapse: collapse; font-family: 'Inter', sans-serif; font-size: 10px;">
                        {''.join(html_rows)}
                    </table>
                </div>
                '''
            
            # Display the compact table
            st.markdown(create_compact_table(display_data), unsafe_allow_html=True)
            
            # Additional insights with proper NULL handling
            if len(weekly_data) > 0:
                latest_week = weekly_data.iloc[0]
                change_val = latest_week['Percent Change (%)']
                if pd.isna(change_val) or change_val is None:
                    change_text = "no previous week comparison"
                else:
                    change_text = f"{float(change_val):+.1f}% change"
                st.info(f"**Latest Week:** Week {int(latest_week['Epi Week'])} of {int(latest_week['Year'])} with {int(latest_week['Weekly Confirmed Cases'])} cases ({change_text})")
                
        else:
            st.warning("📭 No weekly measles data found for the selected period. Please check your date range or data availability.")
        
        # Close print-friendly container
        st.markdown('</div>', unsafe_allow_html=True)
            
    except ImportError as e:
        st.error(f"Error importing data functions: {str(e)}")
    except Exception as e:
        st.error(f"Error loading measles data: {str(e)}")
    
    # Add demographic analysis section
    st.markdown('<div style="margin: 0.5rem 0; border-top: 1px solid #dee2e6;"></div>', unsafe_allow_html=True)
    try:
        st.markdown('<div class="print-table-container demographic-section">', unsafe_allow_html=True)
        st.markdown('<div class="subsection-header"><h3>Demographics - Measles Cases by Age and Sex</h3></div>', unsafe_allow_html=True)
        
        try:
            # Import the function first
            from data_fetcher import get_measles_age_sex_distribution
            
            # Get the age-sex data for analysis (CUMULATIVE - ALL YEARS)
            # This section should show total accumulated cases from all years, not filtered by parameters
            age_sex_data = get_measles_age_sex_distribution()  # No parameters - get all cumulative data
            
            if not age_sex_data.empty:
                # Calculate total cases and percentages
                age_sex_data['total_cases'] = age_sex_data['male_cases'] + age_sex_data['female_cases'] + age_sex_data['unknown_cases']
                total_all_cases = age_sex_data['total_cases'].sum()
                total_male_cases = age_sex_data['male_cases'].sum()
                total_female_cases = age_sex_data['female_cases'].sum()
                total_unknown_cases = age_sex_data['unknown_cases'].sum()

                age_sex_data['percentage'] = (age_sex_data['total_cases'] / total_all_cases * 100).round(1)
                age_sex_data['male_percentage'] = (age_sex_data['male_cases'] / total_male_cases * 100).round(1) if total_male_cases > 0 else 0
                age_sex_data['female_percentage'] = (age_sex_data['female_cases'] / total_female_cases * 100).round(1) if total_female_cases > 0 else 0
                age_sex_data['unknown_percentage'] = (age_sex_data['unknown_cases'] / total_unknown_cases * 100).round(1) if total_unknown_cases > 0 else 0
                
                # Create comprehensive demographic table with simple HTML styling (like epidemiological weeks table)
                def create_demographic_table(df):
                    html_rows = []
                    
                    # First header row with grouped columns
                    group_header_cells = [
                        f'<th rowspan="2" style="padding: 8px 10px; border: 1px solid #dee2e6; font-weight: 600; font-size: 12px; text-align: center; white-space: nowrap; vertical-align: middle;">Age Group</th>',
                        f'<th rowspan="2" style="padding: 8px 10px; border: 1px solid #dee2e6; font-weight: 600; font-size: 12px; text-align: center; white-space: nowrap; vertical-align: middle;">Total Cases</th>',
                        f'<th rowspan="2" style="padding: 8px 10px; border: 1px solid #dee2e6; font-weight: 600; font-size: 12px; text-align: center; white-space: nowrap; vertical-align: middle;">% of Cases</th>',
                        f'<th colspan="2" style="padding: 8px 10px; border: 1px solid #dee2e6; font-weight: 600; font-size: 12px; text-align: center; white-space: nowrap;">Males</th>',
                        f'<th colspan="2" style="padding: 8px 10px; border: 1px solid #dee2e6; font-weight: 600; font-size: 12px; text-align: center; white-space: nowrap;">Females</th>',
                        f'<th colspan="2" style="padding: 8px 10px; border: 1px solid #dee2e6; font-weight: 600; font-size: 12px; text-align: center; white-space: nowrap;">Unknown</th>'
                    ]
                    html_rows.append(f'<tr>{"".join(group_header_cells)}</tr>')

                    # Second header row with sub-columns
                    sub_header_cells = [
                        f'<th style="padding: 8px 10px; border: 1px solid #dee2e6; font-weight: 600; font-size: 11px; text-align: center; white-space: nowrap;">Number of Cases</th>',
                        f'<th style="padding: 8px 10px; border: 1px solid #dee2e6; font-weight: 600; font-size: 11px; text-align: center; white-space: nowrap;">% of All Males</th>',
                        f'<th style="padding: 8px 10px; border: 1px solid #dee2e6; font-weight: 600; font-size: 11px; text-align: center; white-space: nowrap;">Number of Cases</th>',
                        f'<th style="padding: 8px 10px; border: 1px solid #dee2e6; font-weight: 600; font-size: 11px; text-align: center; white-space: nowrap;">% of All Females</th>',
                        f'<th style="padding: 8px 10px; border: 1px solid #dee2e6; font-weight: 600; font-size: 11px; text-align: center; white-space: nowrap;">Number of Cases</th>',
                        f'<th style="padding: 8px 10px; border: 1px solid #dee2e6; font-weight: 600; font-size: 11px; text-align: center; white-space: nowrap;">% of All Unknown</th>'
                    ]
                    html_rows.append(f'<tr>{"".join(sub_header_cells)}</tr>')
                    
                    # Data rows
                    for _, row in df.iterrows():
                        age_group = row['age_group']
                        total_cases = int(row['total_cases'])
                        pct_cases = float(row['percentage'])
                        males = int(row['male_cases'])
                        pct_males = float(row['male_percentage'])
                        females = int(row['female_cases'])
                        pct_females = float(row['female_percentage'])
                        unknowns = int(row['unknown_cases'])
                        pct_unknowns = float(row['unknown_percentage'])

                        data_cells = [
                            f'<td style="padding: 8px 10px; border: 1px solid #dee2e6; text-align: left; font-size: 13px;">{age_group}</td>',
                            f'<td style="padding: 8px 10px; border: 1px solid #dee2e6; text-align: center; font-size: 13px; font-weight: 600;">{total_cases:,}</td>',
                            f'<td style="padding: 8px 10px; border: 1px solid #dee2e6; text-align: center; font-size: 13px; font-weight: 600;">{pct_cases:.1f}%</td>',
                            f'<td style="padding: 8px 10px; border: 1px solid #dee2e6; text-align: center; font-size: 13px; font-weight: 600;">{males:,}</td>',
                            f'<td style="padding: 8px 10px; border: 1px solid #dee2e6; text-align: center; font-size: 13px; font-weight: 600;">{pct_males:.1f}%</td>',
                            f'<td style="padding: 8px 10px; border: 1px solid #dee2e6; text-align: center; font-size: 13px; font-weight: 600;">{females:,}</td>',
                            f'<td style="padding: 8px 10px; border: 1px solid #dee2e6; text-align: center; font-size: 13px; font-weight: 600;">{pct_females:.1f}%</td>',
                            f'<td style="padding: 8px 10px; border: 1px solid #dee2e6; text-align: center; font-size: 13px; font-weight: 600;">{unknowns:,}</td>',
                            f'<td style="padding: 8px 10px; border: 1px solid #dee2e6; text-align: center; font-size: 13px; font-weight: 600;">{pct_unknowns:.1f}%</td>'
                        ]
                        html_rows.append(f'<tr>{"".join(data_cells)}</tr>')

                    # Totals row
                    total_cells = [
                        f'<td style="padding: 8px 10px; border: 1px solid #dee2e6; text-align: left; font-size: 13px; font-weight: 700;"><strong>TOTAL</strong></td>',
                        f'<td style="padding: 8px 10px; border: 1px solid #dee2e6; text-align: center; font-size: 13px; font-weight: 700;"><strong>{total_all_cases:,}</strong></td>',
                        f'<td style="padding: 8px 10px; border: 1px solid #dee2e6; text-align: center; font-size: 13px; font-weight: 700;"><strong>100.0%</strong></td>',
                        f'<td style="padding: 8px 10px; border: 1px solid #dee2e6; text-align: center; font-size: 13px; font-weight: 700;"><strong>{total_male_cases:,}</strong></td>',
                        f'<td style="padding: 8px 10px; border: 1px solid #dee2e6; text-align: center; font-size: 13px; font-weight: 700;"><strong>100.0%</strong></td>',
                        f'<td style="padding: 8px 10px; border: 1px solid #dee2e6; text-align: center; font-size: 13px; font-weight: 700;"><strong>{total_female_cases:,}</strong></td>',
                        f'<td style="padding: 8px 10px; border: 1px solid #dee2e6; text-align: center; font-size: 13px; font-weight: 700;"><strong>100.0%</strong></td>',
                        f'<td style="padding: 8px 10px; border: 1px solid #dee2e6; text-align: center; font-size: 13px; font-weight: 700;"><strong>{total_unknown_cases:,}</strong></td>',
                        f'<td style="padding: 8px 10px; border: 1px solid #dee2e6; text-align: center; font-size: 13px; font-weight: 700;"><strong>100.0%</strong></td>'
                    ]
                    html_rows.append(f'<tr>{"".join(total_cells)}</tr>')
                    
                    return f'''
                    <div style="overflow-x: auto; margin: 1rem 0;">
                        <table style="width: 100%; border-collapse: collapse; font-family: 'Inter', sans-serif; font-size: 10px;">
                            {''.join(html_rows)}
                        </table>
                    </div>
                    '''
                
                # Display the demographic table
                st.markdown(create_demographic_table(age_sex_data), unsafe_allow_html=True)
                
            else:
                st.warning("📂 No demographic data found for measles cases. This may be due to missing date of birth or age information in the database.")
                
        except Exception as e:
            st.error(f"Error generating demographic analysis: {str(e)}")
            
        st.markdown('</div>', unsafe_allow_html=True)
        
    except Exception as e:
        st.error(f"Error loading demographic data: {str(e)}")
    
    # Add geographic/district analysis section
    st.markdown('<div style="margin: 0.5rem 0; border-top: 1px solid #dee2e6;"></div>', unsafe_allow_html=True)
    try:
        from data_fetcher import get_measles_top_10_districts
        
        st.markdown('<div class="print-table-container geographic-section">', unsafe_allow_html=True)
        st.markdown('<div class="subsection-header"><h3>Geographic Distribution - Top Districts with Measles Cases</h3></div>', unsafe_allow_html=True)
        
        # Get district data (CUMULATIVE - ALL YEARS)
        # This section should show cumulative data from all years, not filtered by parameters
        district_data = get_measles_top_10_districts()  # No parameters - get all cumulative data
        
        if not district_data.empty:
            # Create comprehensive district table with color coding
            def create_district_table(df):
                html_rows = []
                
                # Header row with new structure
                headers = [
                    'District', 'Total Cases', 'Total Deaths', 'Cases Last Epiweek',
                    'Deaths Last Epiweek', '% Change'
                ]
                header_cells = []
                for h in headers:
                    header_cells.append(
                        f'<th style="padding: 8px 10px; border: 1px solid #dee2e6; '
                        f'font-weight: 600; font-size: 12px; text-align: center; white-space: nowrap;">{h}</th>'
                    )
                html_rows.append(f'<tr>{"".join(header_cells)}</tr>')

                # Data rows without color coding
                for idx, row in df.iterrows():
                    district = row['District']
                    total_cases = int(row['Total Cases'])
                    total_deaths = int(row['Total Deaths'])
                    cases_last_epiweek = int(row['Cases Last Epiweek'])
                    deaths_last_epiweek = int(row['Deaths Last Epiweek'])
                    pct_change = row['Percentage Change in Cases']

                    # Percentage change formatting
                    if pd.isna(pct_change) or pct_change is None:
                        change_text = 'N/A'
                    else:
                        change_val = float(pct_change)
                        change_text = f'{change_val:+.1f}%' if change_val != 0 else '0.0%'

                    data_cells = [
                        f'<td style="padding: 8px 10px; border: 1px solid #dee2e6; text-align: left; font-size: 13px; font-weight: 600;">{district}</td>',
                        f'<td style="padding: 8px 10px; border: 1px solid #dee2e6; text-align: center; font-size: 13px; font-weight: 600;">{total_cases:,}</td>',
                        f'<td style="padding: 8px 10px; border: 1px solid #dee2e6; text-align: center; font-size: 13px; font-weight: 600;">{total_deaths:,}</td>',
                        f'<td style="padding: 8px 10px; border: 1px solid #dee2e6; text-align: center; font-size: 13px; font-weight: 600;">{cases_last_epiweek:,}</td>',
                        f'<td style="padding: 8px 10px; border: 1px solid #dee2e6; text-align: center; font-size: 13px; font-weight: 600;">{deaths_last_epiweek:,}</td>',
                        f'<td style="padding: 8px 10px; border: 1px solid #dee2e6; text-align: center; font-size: 13px; font-weight: 700;">{change_text}</td>'
                    ]
                    html_rows.append(f'<tr>{"".join(data_cells)}</tr>')

                # Totals row
                total_all_cases = df['Total Cases'].sum()
                total_all_deaths = df['Total Deaths'].sum()
                total_cases_last_week = df['Cases Last Epiweek'].sum()
                total_deaths_last_week = df['Deaths Last Epiweek'].sum()

                total_cells = [
                    f'<td style="padding: 8px 10px; border: 1px solid #dee2e6; text-align: left; font-size: 13px; font-weight: 700;"><strong>TOTAL (Top 10)</strong></td>',
                    f'<td style="padding: 8px 10px; border: 1px solid #dee2e6; text-align: center; font-size: 13px; font-weight: 700;"><strong>{total_all_cases:,}</strong></td>',
                    f'<td style="padding: 8px 10px; border: 1px solid #dee2e6; text-align: center; font-size: 13px; font-weight: 700;"><strong>{total_all_deaths:,}</strong></td>',
                    f'<td style="padding: 8px 10px; border: 1px solid #dee2e6; text-align: center; font-size: 13px; font-weight: 700;"><strong>{total_cases_last_week:,}</strong></td>',
                    f'<td style="padding: 8px 10px; border: 1px solid #dee2e6; text-align: center; font-size: 13px; font-weight: 700;"><strong>{total_deaths_last_week:,}</strong></td>',
                    f'<td style="padding: 8px 10px; border: 1px solid #dee2e6; text-align: center; font-size: 13px; font-weight: 700;"><strong>-</strong></td>'
                ]
                html_rows.append(f'<tr>{"".join(total_cells)}</tr>')
                
                return f'''
                <div style="overflow-x: auto; margin: 1rem 0;">
                    <table style="width: 100%; border-collapse: collapse; font-family: 'Inter', sans-serif; font-size: 9px;">
                        {''.join(html_rows)}
                    </table>
                </div>
                '''
            
            # Display the district table
            st.markdown(create_district_table(district_data), unsafe_allow_html=True)
            
                
        else:
            st.warning("No district data found for measles cases.")
            
        st.markdown('</div>', unsafe_allow_html=True)
        
    except Exception as e:
        st.error(f"Error loading district data: {str(e)}")
    
    # Add district reporting analysis section
    st.markdown('<div style="margin: 0.3rem 0; border-top: 1px solid #dee2e6;"></div>', unsafe_allow_html=True)
    try:
        import plotly.graph_objects as go
        
        st.markdown('<div class="subsection-header"><h3>District Reporting Analysis</h3></div>', unsafe_allow_html=True)
        
        # Get data from database based on selected parameters
        from data_fetcher import get_district_reporting_metrics
        
        # Get the selected parameters
        params = get_dynamic_parameters() if 'params' not in locals() else params
        
        # Create three pie charts in columns
        col1, col2, col3 = st.columns(3)
        
        # Chart 1: % of Districts that Reported At least 1 Case
        with col1:
            st.markdown('<div class="subsection-header"><h4>% Districts Reporting Cases</h4></div>', unsafe_allow_html=True)
            try:
                reporting_data = get_district_reporting_metrics(
                    location=params['location'],
                    year=params['year'],
                    month=params['month']
                )
                
                if reporting_data and 'districts_with_cases' in reporting_data:
                    districts_with_cases = reporting_data['districts_with_cases']
                    total_districts = reporting_data['total_districts']
                    districts_without_cases = total_districts - districts_with_cases
                    
                    fig1 = go.Figure(data=[go.Pie(
                        labels=['Districts with Cases', 'Districts without Cases'],
                        values=[districts_with_cases, districts_without_cases],
                        hole=.4,
                        marker_colors=['#E74C3C', '#ECF0F1'],
                        marker_line=dict(color='#FFFFFF', width=2)
                    )])
                    
                    fig1.update_layout(
                        height=280,
                        showlegend=True,
                        legend=dict(
                            orientation="h",
                            yanchor="bottom",
                            y=-0.25,
                            xanchor="center",
                            x=0.5,
                            font=dict(size=10)
                        ),
                        margin=dict(t=20, b=60, l=20, r=20),
                        annotations=[dict(
                            text=f'<b>{districts_with_cases}</b><br>of {total_districts}<br><span style="color:#E74C3C; font-size:16px;"><b>{districts_with_cases/total_districts*100:.1f}%</b></span>', 
                            x=0.5, y=0.5, font_size=12, showarrow=False
                        )],
                        font=dict(family="Inter, sans-serif")
                    )
                    fig1.update_traces(
                        textinfo='none',
                        hovertemplate='<b>%{label}</b><br>Count: %{value}<br>Percentage: %{percent}<extra></extra>',
                        textfont_size=11
                    )
                    
                    st.plotly_chart(fig1, use_container_width=True, config={'displayModeBar': False})
                else:
                    st.warning("No reporting data available")
                    
            except Exception as e:
                st.error(f"Error loading district reporting data: {str(e)}")
        
        # Chart 2: Proportion of Districts Reporting Cases in Last 21 Days
        with col2:
            st.markdown("#### Districts Reporting Cases in Last 21 Days")
            try:
                reporting_21_data = get_district_reporting_metrics(
                    location=params['location'],
                    year=params['year'],
                    month=params['month'],
                    days_filter=21
                )
                
                if reporting_21_data and 'districts_reporting_recent' in reporting_21_data:
                    recent_districts = reporting_21_data['districts_reporting_recent']
                    total_districts = reporting_21_data['total_districts']
                    non_recent_districts = total_districts - recent_districts
                    
                    fig2 = go.Figure(data=[go.Pie(
                        labels=['Recent Reports', 'No Recent Reports'],
                        values=[recent_districts, non_recent_districts],
                        hole=.4,
                        marker_colors=['#F39C12', '#ECF0F1'],
                        marker_line=dict(color='#FFFFFF', width=2)
                    )])
                    
                    fig2.update_layout(
                        height=280,
                        showlegend=True,
                        legend=dict(
                            orientation="h",
                            yanchor="bottom",
                            y=-0.25,
                            xanchor="center",
                            x=0.5,
                            font=dict(size=10)
                        ),
                        margin=dict(t=20, b=60, l=20, r=20),
                        annotations=[dict(
                            text=f'<b>{recent_districts}</b><br>of {total_districts}<br><span style="color:#F39C12; font-size:16px;"><b>{recent_districts/total_districts*100:.1f}%</b></span>', 
                            x=0.5, y=0.5, font_size=12, showarrow=False
                        )],
                        font=dict(family="Inter, sans-serif")
                    )
                    fig2.update_traces(
                        textinfo='none',
                        hovertemplate='<b>%{label}</b><br>Count: %{value}<br>Percentage: %{percent}<extra></extra>',
                        textfont_size=11
                    )
                    
                    st.plotly_chart(fig2, use_container_width=True, config={'displayModeBar': False})
                else:
                    st.warning("No recent reporting data available")
                    
            except Exception as e:
                st.error(f"Error loading 21-day reporting data: {str(e)}")
        
        # Chart 3: Districts Reporting Measles Cases in the Last 24 Hours
        with col3:
            st.markdown("#### Reporting Cases in Last 24 Hours")
            try:
                reporting_24h_data = get_district_reporting_metrics(
                    location=params['location'],
                    year=params['year'],
                    month=params['month'],
                    hours_filter=24
                )
                
                if reporting_24h_data and 'districts_reporting_24h' in reporting_24h_data:
                    recent_24h_districts = reporting_24h_data['districts_reporting_24h']
                    total_districts = reporting_24h_data['total_districts']
                    non_recent_24h_districts = total_districts - recent_24h_districts
                    
                    fig3 = go.Figure(data=[go.Pie(
                        labels=['Last 24h Reports', 'No Reports in 24h'],
                        values=[recent_24h_districts, non_recent_24h_districts],
                        hole=.4,
                        marker_colors=['#2ECC71', '#ECF0F1'],
                        marker_line=dict(color='#FFFFFF', width=2)
                    )])
                    
                    fig3.update_layout(
                        height=280,
                        showlegend=True,
                        legend=dict(
                            orientation="h",
                            yanchor="bottom",
                            y=-0.25,
                            xanchor="center",
                            x=0.5,
                            font=dict(size=10)
                        ),
                        margin=dict(t=20, b=60, l=20, r=20),
                        annotations=[dict(
                            text=f'<b>{recent_24h_districts}</b><br>of {total_districts}<br><span style="color:#2ECC71; font-size:16px;"><b>{recent_24h_districts/total_districts*100:.1f}%</b></span>', 
                            x=0.5, y=0.5, font_size=12, showarrow=False
                        )],
                        font=dict(family="Inter, sans-serif")
                    )
                    fig3.update_traces(
                        textinfo='none',
                        hovertemplate='<b>%{label}</b><br>Count: %{value}<br>Percentage: %{percent}<extra></extra>',
                        textfont_size=11
                    )
                    
                    st.plotly_chart(fig3, use_container_width=True, config={'displayModeBar': False})
                else:
                    st.warning("No 24-hour reporting data available")
                    
            except Exception as e:
                st.error(f"Error loading 24-hour reporting data: {str(e)}")
        
    except ImportError as e:
        st.error("Plotly not available for chart generation. Please install plotly: pip install plotly")
    except Exception as e:
        st.error(f"Error creating district reporting charts: {str(e)}")
    
    # Add time distribution analysis section
    st.markdown('<div style="margin: 0.3rem 0; border-top: 1px solid #dee2e6;"></div>', unsafe_allow_html=True)
    try:
        import plotly.graph_objects as go
        
       
        
        # Get weekly time series data from database
        from data_fetcher import get_measles_weekly_time_series, get_measles_weekly_by_sex, get_measles_top_districts_epicurves
        
        # Get the current parameters (ensure params is available)
        if 'params' not in locals():
            params = get_dynamic_parameters()
        
        # Create two side-by-side charts with equal spacing
        col1, col2 = st.columns(2, gap="medium")

        # Left Chart: Weekly incident cases with 7-day moving average
        with col1:
            st.markdown("#### Weekly Cases & 7-Day Average")
            try:
                weekly_data = get_measles_weekly_time_series(
                    location=params['location'],
                    year=params['year'],
                    month=params['month']
                )
                
                if not weekly_data.empty:
                    # Create subplot for weekly cases and moving average
                    fig_weekly = go.Figure()
                    
                    # Add bar chart for weekly cases
                    fig_weekly.add_trace(go.Bar(
                        x=weekly_data['week_starting'],
                        y=weekly_data['weekly_cases'],
                        name='Weekly Cases',
                        marker_color='#3498DB',
                        opacity=0.7,
                        hovertemplate='<b>Week: %{x|%Y-%m-%d}</b><br>Cases: %{y}<extra></extra>'
                    ))

                    # Add 7-day moving average line
                    fig_weekly.add_trace(go.Scatter(
                        x=weekly_data['week_starting'],
                        y=weekly_data['moving_average_7d'],
                        mode='lines+markers',
                        name='7-Day Moving Average',
                        line=dict(color='#E74C3C', width=3),
                        marker=dict(size=5, color='#E74C3C'),
                        hovertemplate='<b>Week: %{x|%Y-%m-%d}</b><br>7-Day Avg: %{y:.1f}<extra></extra>'
                    ))

                    fig_weekly.update_layout(
                        height=450,
                        xaxis_title="Week Starting",
                        yaxis_title="Number of Cases",
                        legend=dict(
                            orientation="h",
                            yanchor="bottom",
                            y=1.02,
                            xanchor="center",
                            x=0.5,
                            bgcolor='rgba(255,255,255,0.9)',
                            font=dict(size=10),
                            bordercolor='rgba(0,0,0,0.1)',
                            borderwidth=1
                        ),
                        font=dict(family="Inter, sans-serif", size=11),
                        margin=dict(t=50, b=70, l=60, r=20),
                        plot_bgcolor='rgba(248,249,250,0.5)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        bargap=0.2,
                        hovermode='x unified'
                    )

                    # Customize axes
                    fig_weekly.update_xaxes(
                        showgrid=True, gridwidth=1, gridcolor='rgba(0,0,0,0.08)',
                        showline=True, linewidth=1.5, linecolor='rgba(0,0,0,0.2)',
                        tickangle=-45
                    )
                    fig_weekly.update_yaxes(
                        showgrid=True, gridwidth=1, gridcolor='rgba(0,0,0,0.08)',
                        showline=True, linewidth=1.5, linecolor='rgba(0,0,0,0.2)',
                        rangemode='tozero'
                    )
                    
                    st.plotly_chart(fig_weekly, use_container_width=True, config={'displayModeBar': False})
                else:
                    st.warning("No weekly time series data available")
                    
            except Exception as e:
                st.error(f"Error loading weekly time series: {str(e)}")
        
        # Right Chart: Weekly incident cases by sex
        with col2:
            st.markdown("#### Weekly Cases by Sex")
            try:
                sex_data = get_measles_weekly_by_sex(
                    location=params['location'],
                    year=params['year'],
                    month=params['month']
                )
                
                if not sex_data.empty:
                    fig_sex = go.Figure()
                    
                    # Add male cases (dark red)
                    fig_sex.add_trace(go.Bar(
                        x=sex_data['week_starting'],
                        y=sex_data['male_cases'],
                        name='Male Cases',
                        marker_color='#C0392B',
                        opacity=0.85,
                        hovertemplate='<b>Week: %{x|%Y-%m-%d}</b><br>Male: %{y}<extra></extra>'
                    ))

                    # Add female cases (blue) - stacked
                    fig_sex.add_trace(go.Bar(
                        x=sex_data['week_starting'],
                        y=sex_data['female_cases'],
                        name='Female Cases',
                        marker_color='#2980B9',
                        opacity=0.85,
                        hovertemplate='<b>Week: %{x|%Y-%m-%d}</b><br>Female: %{y}<extra></extra>'
                    ))

                    fig_sex.update_layout(
                        height=450,
                        barmode='stack',
                        xaxis_title="Week Starting",
                        yaxis_title="Number of Cases",
                        legend=dict(
                            orientation="h",
                            yanchor="bottom",
                            y=1.02,
                            xanchor="center",
                            x=0.5,
                            bgcolor='rgba(255,255,255,0.9)',
                            font=dict(size=10),
                            bordercolor='rgba(0,0,0,0.1)',
                            borderwidth=1
                        ),
                        font=dict(family="Inter, sans-serif", size=11),
                        margin=dict(t=50, b=70, l=60, r=20),
                        plot_bgcolor='rgba(248,249,250,0.5)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        bargap=0.2,
                        hovermode='x unified'
                    )

                    # Customize axes
                    fig_sex.update_xaxes(
                        showgrid=True, gridwidth=1, gridcolor='rgba(0,0,0,0.08)',
                        showline=True, linewidth=1.5, linecolor='rgba(0,0,0,0.2)',
                        tickangle=-45
                    )
                    fig_sex.update_yaxes(
                        showgrid=True, gridwidth=1, gridcolor='rgba(0,0,0,0.08)',
                        showline=True, linewidth=1.5, linecolor='rgba(0,0,0,0.2)',
                        rangemode='tozero'
                    )
                    
                    st.plotly_chart(fig_sex, use_container_width=True, config={'displayModeBar': False})
                else:
                    st.warning("No sex-disaggregated data available")
                    
            except Exception as e:
                st.error(f"Error loading sex-disaggregated data: {str(e)}")
        
        # Epicurves section for top 12 districts
        st.markdown('<div style="margin: 0.5rem 0; border-top: 1px solid #dee2e6;"></div>', unsafe_allow_html=True)
        st.markdown("### Epicurves of the Top 12 Districts")
        st.markdown("Weekly incident cases across epidemiological weeks for the most affected districts.")

        try:
            epicurve_data = get_measles_top_districts_epicurves(
                location=params['location'],
                year=params['year'],
                month=params['month']
            )

            if epicurve_data:
                # Define distinct colors for each district (extended to 12 colors)
                district_colors = [
                    '#E74C3C', '#3498DB', '#2ECC71', '#F39C12', '#9B59B6',
                    '#1ABC9C', '#E67E22', '#34495E', '#E91E63', '#FF5722',
                    '#795548', '#607D8B'
                ]

                # Helper function to create district chart
                def create_district_chart(district_name, district_data, color_idx):
                    fig_district = go.Figure()

                    fig_district.add_trace(go.Bar(
                        x=district_data['epi_week'],
                        y=district_data['weekly_cases'],
                        marker_color=district_colors[color_idx % len(district_colors)],
                        opacity=0.85,
                        name=district_name,
                        hovertemplate='<b>Week %{x}</b><br>Cases: %{y}<extra></extra>'
                    ))

                    # Custom Y-axis scale based on district's max cases
                    max_cases = district_data['weekly_cases'].max()
                    y_max = max_cases + (max_cases * 0.15)  # Add 15% padding

                    fig_district.update_layout(
                        height=250,
                        xaxis_title="Epi Week",
                        yaxis_title="Cases",
                        showlegend=False,
                        font=dict(family="Inter, sans-serif", size=10),
                        margin=dict(t=10, b=45, l=45, r=10),
                        plot_bgcolor='rgba(248,249,250,0.5)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        yaxis=dict(range=[0, y_max]),
                        bargap=0.15,
                        hovermode='x'
                    )

                    fig_district.update_xaxes(
                        showgrid=True, gridwidth=1, gridcolor='rgba(0,0,0,0.08)',
                        showline=True, linewidth=1.5, linecolor='rgba(0,0,0,0.2)'
                    )
                    fig_district.update_yaxes(
                        showgrid=True, gridwidth=1, gridcolor='rgba(0,0,0,0.08)',
                        showline=True, linewidth=1.5, linecolor='rgba(0,0,0,0.2)'
                    )

                    return fig_district

                # Create a grid layout for the district epicurves (3 columns)
                for i in range(0, len(epicurve_data), 3):
                    col1, col2, col3 = st.columns(3, gap="medium")
                    
                    # Process each district in the row
                    columns = [col1, col2, col3]
                    for j in range(3):
                        district_idx = i + j
                        if district_idx < len(epicurve_data):
                            with columns[j]:
                                district_name = epicurve_data[district_idx]['district']
                                district_data = epicurve_data[district_idx]['data']

                                st.markdown(f"**{district_name}**")

                                if not district_data.empty:
                                    fig = create_district_chart(district_name, district_data, district_idx)
                                    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
                                else:
                                    st.info(f"No data for {district_name}")
            else:
                st.warning("No district epicurve data available")
                
        except Exception as e:
            st.error(f"Error loading district epicurves: {str(e)}")
                
    except ImportError as e:
        st.error("Plotly not available for time series charts.")
    except Exception as e:
        st.error(f"Error creating time series charts: {str(e)}")
    
    # Add proportion analysis section
    st.markdown('<div style="margin: 0.3rem 0; border-top: 1px solid #dee2e6;"></div>', unsafe_allow_html=True)
    try:
        import plotly.graph_objects as go
        

        
        # Get proportion data from database
        from data_fetcher import get_district_weekly_proportions, get_district_total_proportions
        
        # Get the current parameters
        if 'params' not in locals():
            params = get_dynamic_parameters()
        
        # Create two side-by-side charts
        col1, col2 = st.columns(2, gap="medium")

        # Left Chart: Total proportion of cases by district (horizontal bar chart)
        with col1:
            st.markdown("#### Total Case Proportions by District")
            try:
                district_prop_data = get_district_total_proportions(
                    location=params['location'],
                    year=params['year'],
                    month=params['month']
                )
                
                if not district_prop_data.empty:
                    # Take top 5 districts for consistency with right chart
                    top_districts = district_prop_data.head(5).sort_values('proportion', ascending=True)

                    # Better color palette for bars
                    colors_map = ['#E74C3C', '#3498DB', '#2ECC71', '#F39C12', '#9B59B6']
                    bar_colors = [colors_map[i] for i in range(len(top_districts))]

                    fig_district_prop = go.Figure()

                    # Create vertical bar chart with percentage values on top
                    fig_district_prop.add_trace(go.Bar(
                        x=top_districts['district'],
                        y=top_districts['proportion'],
                        marker=dict(
                            color=bar_colors,
                            line=dict(color='rgba(255,255,255,0.3)', width=1)
                        ),
                        opacity=0.85,
                        text=top_districts['proportion'].apply(lambda x: f'{x:.1f}%'),
                        textposition='outside',
                        textfont=dict(color='#2C3E50', size=11, family="Inter, sans-serif"),
                        hovertemplate='<b>%{x}</b><br>Proportion: %{y:.1f}%<extra></extra>'
                    ))

                    fig_district_prop.update_layout(
                        height=450,
                        xaxis_title="District",
                        yaxis_title="Proportion of Total Cases (%)",
                        showlegend=False,
                        font=dict(family="Inter, sans-serif", size=11),
                        margin=dict(t=40, b=100, l=60, r=20),
                        plot_bgcolor='rgba(248,249,250,0.5)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        yaxis=dict(ticksuffix='%'),
                        bargap=0.3
                    )

                    # Customize axes
                    fig_district_prop.update_xaxes(
                        showgrid=False,
                        showline=True, linewidth=1.5, linecolor='rgba(0,0,0,0.2)',
                        tickangle=-45,
                        tickfont=dict(size=10)
                    )
                    fig_district_prop.update_yaxes(
                        showgrid=True, gridwidth=1, gridcolor='rgba(0,0,0,0.08)',
                        showline=True, linewidth=1.5, linecolor='rgba(0,0,0,0.2)',
                        rangemode='tozero'
                    )

                    st.plotly_chart(fig_district_prop, use_container_width=True, config={'displayModeBar': False})
                else:
                    st.warning("No district proportion data available")

            except Exception as e:
                st.error(f"Error loading district proportion data: {str(e)}")
        
        # Right Chart: Proportion of weekly cases for top 5 districts over time
        with col2:
            st.markdown("#### Weekly Case Proportions - Top 5 Districts")
            try:
                weekly_prop_data = get_district_weekly_proportions(
                    location=params['location'],
                    year=params['year'],
                    month=params['month']
                )

                if not weekly_prop_data.empty:
                    fig_weekly_prop = go.Figure()

                    # Get unique districts (top 5)
                    districts = weekly_prop_data['district'].unique()[:5]
                    # More distinct, vibrant colors for better clarity
                    colors = ['#E74C3C', '#3498DB', '#27AE60', '#F39C12', '#9B59B6']

                    for i, district in enumerate(districts):
                        district_data = weekly_prop_data[weekly_prop_data['district'] == district]

                        fig_weekly_prop.add_trace(go.Scatter(
                            x=district_data['week_starting'],
                            y=district_data['proportion'],
                            mode='lines+markers',
                            name=district,
                            line=dict(color=colors[i], width=3.5),
                            marker=dict(size=8, color=colors[i], line=dict(color='white', width=1.5)),
                            hovertemplate='<b>%{fullData.name}</b><br>Week: %{x|%Y-%m-%d}<br>Proportion: %{y:.1f}%<extra></extra>'
                        ))

                    fig_weekly_prop.update_layout(
                        height=500,
                        xaxis_title="Week Starting",
                        yaxis_title="Proportion of Total Cases (%)",
                        legend=dict(
                            orientation="h",
                            yanchor="bottom",
                            y=1.0,
                            xanchor="center",
                            x=0.5,
                            bgcolor='rgba(255,255,255,0.95)',
                            bordercolor='rgba(0,0,0,0.2)',
                            borderwidth=1.5,
                            font=dict(size=10, family="Inter, sans-serif")
                        ),
                        font=dict(family="Inter, sans-serif", size=11),
                        margin=dict(t=50, b=80, l=60, r=20),
                        plot_bgcolor='rgba(255,255,255,0.8)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        yaxis=dict(ticksuffix='%'),
                        hovermode='x unified'
                    )

                    # Customize axes
                    fig_weekly_prop.update_xaxes(
                        showgrid=True, gridwidth=1, gridcolor='rgba(0,0,0,0.1)',
                        showline=True, linewidth=1.5, linecolor='rgba(0,0,0,0.3)',
                        tickangle=-45,
                        tickfont=dict(size=10)
                    )
                    fig_weekly_prop.update_yaxes(
                        showgrid=True, gridwidth=1, gridcolor='rgba(0,0,0,0.1)',
                        showline=True, linewidth=1.5, linecolor='rgba(0,0,0,0.3)',
                        rangemode='tozero'
                    )

                    st.plotly_chart(fig_weekly_prop, use_container_width=True, config={'displayModeBar': False})
                else:
                    st.warning("No weekly proportion data available")

            except Exception as e:
                st.error(f"Error loading weekly proportion data: {str(e)}")
                
    except ImportError as e:
        st.error("Plotly not available for proportion charts.")
    except Exception as e:
        st.error(f"Error creating proportion charts: {str(e)}")
    
    # Add demographic and mortality analysis section
    st.markdown('<div style="margin: 0.3rem 0; border-top: 1px solid #dee2e6;"></div>', unsafe_allow_html=True)
    try:
        import plotly.graph_objects as go
        
      
        
        # Get demographic and mortality data from database
        from data_fetcher import (
            get_measles_gender_distribution, 
            get_measles_age_sex_distribution,
            get_measles_deaths_by_district,
            get_measles_attack_rates_by_age_sex
        )
        
        # Get the current parameters
        if 'params' not in locals():
            params = get_dynamic_parameters()
        
        # Debug: Show current parameters for demographic section
        # st.info(f"Demographic Analysis - Using parameters: Year: {params['year']}, Location: {params['location']}")
        
        # Group 1: Overall Distribution of Incident Cases by Age and Sex
       
        col1, col2 = st.columns(2, gap="medium")

        # Group 1 - Chart 1: Gender Distribution Pie Chart
        with col1:
            st.markdown("##### Gender Distribution")
            try:
                gender_data = get_measles_gender_distribution(
                    location=params['location'],
                    year=params['year'],
                    month=params['month']
                )

                if not gender_data.empty:
                    fig_gender = go.Figure(data=[go.Pie(
                        labels=gender_data['gender'],
                        values=gender_data['cases'],
                        hole=.3,
                        marker_colors=['#3498DB', '#E74C3C', '#95A5A6'],
                        marker_line=dict(color='#FFFFFF', width=2),
                        textposition='inside',
                        textinfo='percent+label',
                        hovertemplate='<b>%{label}</b><br>Cases: %{value}<br>Percentage: %{percent}<extra></extra>'
                    )])

                    fig_gender.update_layout(
                        height=300,
                        showlegend=True,
                        legend=dict(orientation="h", yanchor="bottom", y=-0.15, xanchor="center", x=0.5, font=dict(size=9)),
                        margin=dict(t=20, b=50, l=20, r=20),
                        font=dict(family="Inter, sans-serif", size=10),
                        paper_bgcolor='rgba(0,0,0,0)'
                    )
                    fig_gender.update_traces(textfont_size=9, textfont_color='white')
                    
                    st.plotly_chart(fig_gender, use_container_width=True, config={'displayModeBar': False})
                else:
                    st.warning("No gender data available")
            except Exception as e:
                st.error(f"Error loading gender data: {str(e)}")
        
        # Group 1 - Chart 2: Population Pyramid (Bilateral Histogram)
        with col2:
            st.markdown("##### Distribution of Age and Sex")
            try:
                age_sex_data = get_measles_age_sex_distribution(
                    location=params['location'],
                    year=params['year'],
                    month=params['month']
                )
                
                if not age_sex_data.empty:
                    fig_pyramid = go.Figure()

                    # Define custom order with Unknown just above 0-4 at bottom
                    age_order = ['50+', '45-49', '40-44', '35-39', '30-34', '25-29', '20-24', '15-19', '10-14', '5-9', '0-4', 'Unknown']

                    # Create population pyramid - males on left (negative values), females on right (positive)
                    fig_pyramid.add_trace(go.Bar(
                        y=age_sex_data['age_group'],
                        x=[-x for x in age_sex_data['male_cases']],  # Negative for left side
                        orientation='h',
                        name='Male',
                        marker_color='#3498DB',
                        opacity=0.85,
                        text=[str(x) for x in age_sex_data['male_cases']],
                        textposition='auto',
                        textfont=dict(color='white', size=10),
                        hovertemplate='<b>Male</b><br>Age: %{y}<br>Cases: %{text}<extra></extra>'
                    ))

                    fig_pyramid.add_trace(go.Bar(
                        y=age_sex_data['age_group'],
                        x=age_sex_data['female_cases'],  # Positive for right side
                        orientation='h',
                        name='Female',
                        marker_color='#E74C3C',
                        opacity=0.85,
                        text=[str(x) for x in age_sex_data['female_cases']],
                        textposition='auto',
                        textfont=dict(color='white', size=10),
                        hovertemplate='<b>Female</b><br>Age: %{y}<br>Cases: %{text}<extra></extra>'
                    ))

                    # Add unknown cases if they exist
                    if 'unknown_cases' in age_sex_data.columns:
                        fig_pyramid.add_trace(go.Bar(
                            y=age_sex_data['age_group'],
                            x=age_sex_data['unknown_cases'],  # Positive on right side with females
                            orientation='h',
                            name='Unknown',
                            marker_color='#95A5A6',
                            opacity=0.85,
                            text=[str(x) for x in age_sex_data['unknown_cases']],
                            textposition='auto',
                            textfont=dict(color='white', size=10),
                            hovertemplate='<b>Unknown</b><br>Age: %{y}<br>Cases: %{text}<extra></extra>'
                        ))
                        # Calculate max value including unknown
                        max_val = max(max(age_sex_data['male_cases']),
                                    max(age_sex_data['female_cases']),
                                    max(age_sex_data['unknown_cases']))
                    else:
                        # Calculate max value for symmetric axis
                        max_val = max(max(age_sex_data['male_cases']), max(age_sex_data['female_cases']))

                    fig_pyramid.update_layout(
                        height=400,
                        barmode='overlay',
                        xaxis_title="Number of Cases",
                        yaxis_title="",
                        legend=dict(
                            orientation="h",
                            yanchor="top",
                            y=-0.15,
                            xanchor="center",
                            x=0.5,
                            font=dict(size=11)
                        ),
                        font=dict(family="Inter, sans-serif", size=12),
                        margin=dict(t=30, b=80, l=5, r=5),
                        plot_bgcolor='rgba(248,249,250,0.5)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        xaxis=dict(
                            range=[-max_val*1.1, max_val*1.1],
                            tickvals=[-max_val, -max_val//2, 0, max_val//2, max_val],
                            ticktext=[str(max_val), str(max_val//2), '0', str(max_val//2), str(max_val)],
                            tickfont=dict(size=11),
                            title=dict(font=dict(size=12))
                        ),
                        yaxis=dict(
                            tickfont=dict(size=12)
                        )
                    )

                    fig_pyramid.update_xaxes(
                        showgrid=True, gridwidth=1, gridcolor='rgba(0,0,0,0.1)',
                        showline=True, linewidth=1.5, linecolor='rgba(0,0,0,0.2)',
                        zeroline=True, zerolinewidth=2, zerolinecolor='rgba(0,0,0,0.3)'
                    )
                    fig_pyramid.update_yaxes(
                        showgrid=False,
                        showline=True, linewidth=1.5, linecolor='rgba(0,0,0,0.2)',
                        categoryorder='array',
                        categoryarray=age_order
                    )
                    
                    st.plotly_chart(fig_pyramid, use_container_width=True, config={'displayModeBar': False})
                else:
                    st.warning("No age-sex data available")
            except Exception as e:
                st.error(f"Error loading age-sex data: {str(e)}")
        
        
        # Group 2: Overall Distribution of Deaths by Place and Sex - Age
       
        col1, col2 = st.columns(2)
        
        # Group 2 - Chart 1: Deaths per District Bar Chart
        with col1:
            st.markdown("##### Measles Deaths by District")
            try:
                deaths_district_data = get_measles_deaths_by_district()
                
                if not deaths_district_data.empty:
                    fig_deaths_district = go.Figure()
                    
                    fig_deaths_district.add_trace(go.Bar(
                        y=deaths_district_data['District'][:10],  # Top 10 districts
                        x=deaths_district_data['Deaths'][:10],
                        orientation='h',
                        marker_color='#1f77b4',  # Blue bars
                        opacity=0.8,
                        text=deaths_district_data['Deaths'][:10],
                        textposition='outside',
                        textfont=dict(color='#d91a72', size=10, family='Arial Bold')  # Dark pink/magenta labels
                    ))
                    
                    fig_deaths_district.update_layout(
                        height=280,
                        xaxis_title="Number of Deaths",
                        yaxis_title="District",
                        showlegend=False,
                        font=dict(family="Inter, sans-serif", size=9),
                        margin=dict(t=10, b=40, l=100, r=10),
                        plot_bgcolor='rgba(0,0,0,0)',
                        yaxis=dict(categoryorder='total ascending')
                    )
                    
                    fig_deaths_district.update_xaxes(showgrid=True, gridwidth=1, gridcolor='rgba(0,0,0,0.1)')
                    fig_deaths_district.update_yaxes(showgrid=False)
                    
                    st.plotly_chart(fig_deaths_district, use_container_width=True, config={'displayModeBar': False})
                else:
                    st.warning("No district death data available")
            except Exception as e:
                st.error(f"Error loading district death data: {str(e)}")
        
        # Group 2 - Chart 2: Stacked Bar Chart - Deaths by Age and Sex
        with col2:
            st.markdown("##### Measles Deaths by Age and Sex")
            try:
                # Function not yet implemented
                st.info("Deaths by Age and Sex data is not available")
            except Exception as e:
                st.error(f"Error loading age-sex death data: {str(e)}")
                
    except ImportError as e:
        with col3:
            st.markdown("##### Death Analysis Summary")
            try:
                deaths_summary_available = False
                
                if 'deaths_district_data' in locals() and not deaths_district_data.empty:
                    total_deaths = deaths_district_data['Deaths'].sum()
                    top_death_district = deaths_district_data.iloc[0]['District']
                    districts_with_deaths = len(deaths_district_data[deaths_district_data['Deaths'] > 0])
                    deaths_summary_available = True
                
                if deaths_summary_available:
                    # Child death analysis not available yet
                    child_deaths = 0
                    child_death_pct = 0
                    
                    st.markdown(
                        f"""
                        <div style="background: #fff5f5; padding: 15px; border-radius: 8px; margin: 10px 0; font-size: 11px; border: 1px solid #fed7d7;">
                            <h5 style="color: #c53030; margin: 0 0 10px 0; font-size: 13px;">Mortality Analysis</h5>
                            <div style="margin: 8px 0;"><b>Total Deaths:</b> {int(total_deaths):,}</div>
                            <div style="margin: 8px 0;"><b>Top District:</b> {top_death_district if 'top_death_district' in locals() else 'N/A'}</div>
                            <div style="margin: 8px 0;"><b>Districts Affected:</b> {districts_with_deaths if 'districts_with_deaths' in locals() else 'N/A'}</div>
                            <div style="margin: 8px 0; color: #c53030;"><b>Child Deaths (0-9):</b> {int(child_deaths) if 'child_deaths' in locals() else 'N/A'} ({child_death_pct:.1f}%)</div>
                        </div>
                        """, unsafe_allow_html=True
                    )
                else:
                    st.info("No death data available")
                    
            except Exception as e:
                st.error(f"Error loading death analysis: {str(e)}")
                
    except ImportError as e:
        st.error("Plotly not available for demographic charts.")
    except Exception as e:
        st.error(f"Error creating demographic charts: {str(e)}")

    # Overall Attack Rates by Age - Grouped Bar Chart (Separate Section)
    try:
        st.markdown("#### Overall Attack Rates by Age")
        
        # Get the current parameters for attack rates
        if 'params' not in locals():
            params = get_dynamic_parameters()
        
        attack_rates_data = get_measles_attack_rates_by_age_sex(
            location=params['location'],
            year=params['year'],
            month=params['month']
        )
        
        if not attack_rates_data.empty:
            import plotly.graph_objects as go
            fig_attack_rates = go.Figure()
            
            # Add male bars (left side, bars grow from center towards left)
            fig_attack_rates.add_trace(go.Bar(
                y=attack_rates_data['age_group'],
                x=[-rate/100000 for rate in attack_rates_data['male_attack_rate']],  # Negative for left side, scaled per 100k
                orientation='h',
                name='Male',
                marker_color='#E91E63',  # Pink for males
                opacity=0.8,
                text=[f'{rate/100000:.1f}' for rate in attack_rates_data['male_attack_rate']],  # Show positive values
                textposition='auto',
                textfont=dict(size=9, color='white'),
                base=0  # Start from center axis
            ))
            
            # Add female bars (right side, bars grow from center towards right)
            fig_attack_rates.add_trace(go.Bar(
                y=attack_rates_data['age_group'],
                x=[rate/100000 for rate in attack_rates_data['female_attack_rate']],  # Positive for right side, scaled per 100k
                orientation='h',
                name='Female',
                marker_color='#3498DB',  # Blue for females
                opacity=0.8,
                text=[f'{rate/100000:.1f}' for rate in attack_rates_data['female_attack_rate']],
                textposition='auto',
                textfont=dict(size=9, color='white'),
                base=0  # Start from center axis
            ))
            
            fig_attack_rates.update_layout(
                height=450,
                xaxis_title="Cases per 100,000 Population",
                yaxis_title="Age Group",
                barmode='overlay',  # Overlay for population pyramid
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="center",
                    x=0.5,
                    font=dict(size=10)
                ),
                font=dict(family="Inter, sans-serif", size=10),
                margin=dict(t=80, b=60, l=80, r=80),
                plot_bgcolor='rgba(0,0,0,0)',
                showlegend=True,
                xaxis=dict(
                    showgrid=True,
                    gridwidth=1,
                    gridcolor='rgba(0,0,0,0.1)',
                    zeroline=True,
                    zerolinewidth=2,
                    zerolinecolor='rgba(0,0,0,0.3)',
                    tickformat='.1f',
                    tickvals=[-0.6, -0.4, -0.2, 0, 0.2, 0.4, 0.6],
                    ticktext=['0.6', '0.4', '0.2', '0', '0.2', '0.4', '0.6']
                ),
                yaxis=dict(
                    showgrid=False,
                    categoryorder='array',
                    categoryarray=['50+', '45-49', '40-44', '35-39', '30-34', '25-29', '20-24', '15-19', '5-14', '0-4']
                )
            )
            
            st.plotly_chart(fig_attack_rates, use_container_width=True, config={'displayModeBar': False})
        else:
            st.warning("No attack rates data available")
            
    except Exception as e:
        st.error(f"Error loading attack rates data: {str(e)}")
        import traceback
        st.error(f"Traceback: {traceback.format_exc()}")

    # ===== CHOROPLETH MAPS SECTION =====
    try:
        st.markdown("---")

        # Import required modules
        import json
        import plotly.graph_objects as go
        from choropleth_data import (
            get_measles_cumulative_cases_by_district,
            get_measles_districts_reporting_last_21_days,
            get_measles_attack_rates_by_district_cumulative,
            get_measles_current_case_rates_by_district_21_days
        )
        
        # Load GeoJSON data - districts only
        geojson_path = st.secrets.get("GEOJSON_PATH", "districts.geojson")
        with open(geojson_path, 'r', encoding='utf-8') as f:
            districts_data = json.load(f)
        district_features = districts_data['features']
        
        # Create GeoJSON objects
        districts_geojson = {
            'type': 'FeatureCollection',
            'features': district_features
        }
        
        # Color mapping functions
        def get_cumulative_cases_color(value):
            """Map cumulative cases to color ranges"""
            if value is None or value == 0:
                return '#CCCCCC'  # Grey
            elif 1 <= value <= 9:
                return '#FFE0E0'  # Very light red
            elif 10 <= value <= 49:
                return '#FFB3B3'  # Light red
            elif 50 <= value <= 99:
                return '#FF8080'  # Medium red
            elif 100 <= value <= 499:
                return '#FF4D4D'  # Dark red
            else:  # 500+
                return '#CC0000'  # Deep red
        
        def get_reporting_21_days_color(value):
            """Map 21-day reporting to color ranges"""
            if value is None or value == 0:
                return '#CCCCCC'  # Grey
            elif 1 <= value <= 9:
                return '#FFE6D9'  # Light orange
            else:  # 10-49+
                return '#FFB366'  # Medium orange
        
        def get_attack_rates_color(value):
            """Map attack rates to color ranges"""
            if value is None or value == 0:
                return '#F0F0F0'  # Light grey
            elif 0.1 <= value <= 4.9:
                return '#FFE0E0'  # Very light red
            elif 5 <= value <= 10.9:
                return '#FFB3B3'  # Light red
            elif 11 <= value <= 15.9:
                return '#FF8080'  # Medium red
            elif value >= 21:
                return '#CC0000'  # Deep red
            else:
                return '#808080'  # Dark grey for NA
        
        def get_current_rates_color(value):
            """Map current rates to color ranges"""
            if value is None or value == 0:
                return '#CCCCCC'  # Grey
            elif 0.1 <= value <= 4.9:
                return '#FFE6D9'  # Light orange
            elif 5 <= value <= 10.9:
                return '#FFB366'  # Medium orange
            else:  # 11-15.9+
                return '#FF8000'  # Dark orange
        
        # Fetch data
        cumulative_cases = get_measles_cumulative_cases_by_district()
        reporting_21_days = get_measles_districts_reporting_last_21_days()
        attack_rates = get_measles_attack_rates_by_district_cumulative()
        current_rates = get_measles_current_case_rates_by_district_21_days()
        
        # Create 2x2 layout with smaller spacing
        col1, col2 = st.columns([0.45, 0.45], gap="medium")
        col3, col4 = st.columns([0.45, 0.45], gap="medium")
        
        # 1. Top Left: Cumulative Cases by District
        with col1:
            st.markdown("<h4 style='font-size: 18px; margin-bottom: 10px;'>Cumulative Cases by District</h4>", unsafe_allow_html=True)
            
            # Prepare district names for matching
            locations = [feature['properties']['name'] for feature in district_features]
            z_values = [cumulative_cases.get(loc, 0) for loc in locations]
            max_cumulative = max(z_values) if z_values else 0

            fig_cumulative = go.Figure(data=go.Choroplethmapbox(
                geojson=districts_geojson,
                locations=locations,
                featureidkey="properties.name",
                z=z_values,
                zmin=0,
                zmax=max(500, max_cumulative),
                colorscale=[
                    [0, '#E8E8E8'],          # 0: Light Grey
                    [0.02, '#FFF4E6'],       # 1-9: Very Light Orange
                    [0.10, '#FFD699'],       # 10-49: Light Orange
                    [0.20, '#FFB347'],       # 50-99: Medium Orange
                    [0.80, '#FF8C00'],       # 100-499: Dark Orange
                    [1.0, '#CC6600']         # 500+: Very Dark Orange
                ],
                marker_opacity=0.85,
                marker_line_width=1.5,
                marker_line_color='white',
                hovertemplate='<b>%{location}</b><br>Total Cases: %{z:,}<extra></extra>',
                showscale=False
            ))

            # Add custom legend as annotations
            legend_items = [
                {'label': '0', 'color': '#E8E8E8'},
                {'label': '1-9', 'color': '#FFF4E6'},
                {'label': '10-49', 'color': '#FFD699'},
                {'label': '50-99', 'color': '#FFB347'},
                {'label': '100-499', 'color': '#FF8C00'},
                {'label': '500+', 'color': '#CC6600'}
            ]

            annotations = [dict(
                text="<b>Cases</b>",
                x=0.02, y=0.98,
                xref='paper', yref='paper',
                showarrow=False,
                font=dict(size=12, family="Inter, sans-serif", color='#2C3E50'),
                xanchor='left', yanchor='top',
                bgcolor='rgba(255,255,255,0.9)',
                bordercolor='rgba(0,0,0,0.2)',
                borderwidth=1,
                borderpad=4
            )]

            for i, item in enumerate(legend_items):
                # Add color box as a separate annotation
                annotations.append(dict(
                    text="█",
                    x=0.02, y=0.92 - i*0.05,
                    xref='paper', yref='paper',
                    showarrow=False,
                    font=dict(size=16, family="Arial", color=item['color']),
                    xanchor='left', yanchor='top'
                ))
                # Add label text
                annotations.append(dict(
                    text=item['label'],
                    x=0.04, y=0.92 - i*0.05,
                    xref='paper', yref='paper',
                    showarrow=False,
                    font=dict(size=10, family="Inter, sans-serif", color='#2C3E50'),
                    xanchor='left', yanchor='top',
                    bgcolor='rgba(255,255,255,0.9)',
                    borderpad=2
                ))

            fig_cumulative.update_layout(annotations=annotations)
            
            fig_cumulative.update_layout(
                mapbox_style="white-bg",
                mapbox=dict(
                    center=dict(lat=1.274, lon=32.290),
                    zoom=5.0,
                    layers=[]
                ),
                margin=dict(r=0, t=0, l=0, b=0),
                height=380,
                showlegend=False,
                transition_duration=0,
                autosize=True,
            )
            
            st.plotly_chart(fig_cumulative, use_container_width=True, config={'displayModeBar': False, 'staticPlot': False, 'toImageButtonOptions': {'format': 'png', 'filename': 'cumulative_cases_map', 'height': 400, 'width': 600, 'scale': 2}})
        
        # 2. Top Right: District Reporting Last 21 Days
        with col2:
            st.markdown("<h4 style='font-size: 18px; margin-bottom: 10px;'>District Reporting Last 21 Days</h4>", unsafe_allow_html=True)
            
            # Prepare data for reporting map
            z_values_reporting = [reporting_21_days.get(loc, 0) for loc in locations]
            max_reporting = max(z_values_reporting) if z_values_reporting else 0

            fig_reporting = go.Figure(data=go.Choroplethmapbox(
                geojson=districts_geojson,
                locations=locations,
                featureidkey="properties.name",
                z=z_values_reporting,
                zmin=0,
                zmax=max(50, max_reporting),
                colorscale=[
                    [0, '#E8E8E8'],      # 0: Grey
                    [0.02, '#E3F2FD'],   # 1-9: Very Light Blue
                    [0.20, '#90CAF9'],   # 10-49: Light Blue
                    [1.0, '#1976D2']     # 50+: Blue
                ],
                marker_opacity=0.85,
                marker_line_width=1.5,
                marker_line_color='white',
                hovertemplate='<b>%{location}</b><br>Recent Cases: %{z:,}<extra></extra>',
                showscale=False
            ))

            # Add custom legend as annotations
            legend_items_reporting = [
                {'label': '0', 'color': '#E8E8E8'},
                {'label': '1-9', 'color': '#E3F2FD'},
                {'label': '10-49', 'color': '#90CAF9'}
            ]

            annotations_reporting = [dict(
                text="<b>Recent (21 days)</b>",
                x=0.02, y=0.98,
                xref='paper', yref='paper',
                showarrow=False,
                font=dict(size=12, family="Inter, sans-serif", color='#2C3E50'),
                xanchor='left', yanchor='top',
                bgcolor='rgba(255,255,255,0.9)',
                bordercolor='rgba(0,0,0,0.2)',
                borderwidth=1,
                borderpad=4
            )]

            for i, item in enumerate(legend_items_reporting):
                # Add color box as a separate annotation
                annotations_reporting.append(dict(
                    text="█",
                    x=0.02, y=0.92 - i*0.05,
                    xref='paper', yref='paper',
                    showarrow=False,
                    font=dict(size=16, family="Arial", color=item['color']),
                    xanchor='left', yanchor='top'
                ))
                # Add label text
                annotations_reporting.append(dict(
                    text=item['label'],
                    x=0.04, y=0.92 - i*0.05,
                    xref='paper', yref='paper',
                    showarrow=False,
                    font=dict(size=10, family="Inter, sans-serif", color='#2C3E50'),
                    xanchor='left', yanchor='top',
                    bgcolor='rgba(255,255,255,0.9)',
                    borderpad=2
                ))

            fig_reporting.update_layout(annotations=annotations_reporting)
            
            fig_reporting.update_layout(
                mapbox_style="white-bg",
                mapbox=dict(
                    center=dict(lat=1.274, lon=32.290),
                    zoom=5.0,
                    layers=[]
                ),
                margin=dict(r=0, t=0, l=0, b=0),
                height=380,
                showlegend=False,
                transition_duration=0,
                autosize=True,
            )
            
            st.plotly_chart(fig_reporting, use_container_width=True, config={'displayModeBar': False, 'staticPlot': False, 'toImageButtonOptions': {'format': 'png', 'filename': 'reporting_21days_map', 'height': 400, 'width': 600, 'scale': 2}})
        
        # 3. Bottom Left: Attack Rates per 100K Population (Cumulative)
        with col3:
            st.markdown("<h4 style='font-size: 18px; margin-bottom: 10px;'>Attack Rates per 100K Population by Place (Cumulative)</h4>", unsafe_allow_html=True)
            
            # Prepare data for attack rates map
            z_values_attack = [attack_rates.get(loc, 0) for loc in locations]
            max_attack = max(z_values_attack) if z_values_attack else 0

            fig_attack = go.Figure(data=go.Choroplethmapbox(
                geojson=districts_geojson,
                locations=locations,
                featureidkey="properties.name",
                z=z_values_attack,
                zmin=0,
                zmax=max(25, max_attack),
                colorscale=[
                    [0, '#E8E8E8'],          # 0: Grey
                    [0.20, '#F1F8E9'],       # 0.1-4.9: Very Light Green
                    [0.44, '#AED581'],       # 5-10.9: Light Green
                    [0.64, '#7CB342'],       # 11-15.9: Medium Green
                    [0.84, '#558B2F'],       # 16-20.9: Dark Green
                    [1.0, '#33691E']         # 21+: Very Dark Green
                ],
                marker_opacity=0.85,
                marker_line_width=1.5,
                marker_line_color='white',
                hovertemplate='<b>%{location}</b><br>Attack Rate: %{z:.1f} per 100K<extra></extra>',
                showscale=False
            ))

            # Add custom legend as annotations
            legend_items_attack = [
                {'label': '0', 'color': '#E8E8E8'},
                {'label': '0.1-4.9', 'color': '#F1F8E9'},
                {'label': '5-10.9', 'color': '#AED581'},
                {'label': '11-15.9', 'color': '#7CB342'},
                {'label': '16-20.9', 'color': '#558B2F'},
                {'label': '21+', 'color': '#33691E'}
            ]

            annotations_attack = [dict(
                text="<b>Rate (per 100K)</b>",
                x=0.02, y=0.98,
                xref='paper', yref='paper',
                showarrow=False,
                font=dict(size=12, family="Inter, sans-serif", color='#2C3E50'),
                xanchor='left', yanchor='top',
                bgcolor='rgba(255,255,255,0.9)',
                bordercolor='rgba(0,0,0,0.2)',
                borderwidth=1,
                borderpad=4
            )]

            for i, item in enumerate(legend_items_attack):
                # Add color box as a separate annotation
                annotations_attack.append(dict(
                    text="█",
                    x=0.02, y=0.92 - i*0.05,
                    xref='paper', yref='paper',
                    showarrow=False,
                    font=dict(size=16, family="Arial", color=item['color']),
                    xanchor='left', yanchor='top'
                ))
                # Add label text
                annotations_attack.append(dict(
                    text=item['label'],
                    x=0.04, y=0.92 - i*0.05,
                    xref='paper', yref='paper',
                    showarrow=False,
                    font=dict(size=10, family="Inter, sans-serif", color='#2C3E50'),
                    xanchor='left', yanchor='top',
                    bgcolor='rgba(255,255,255,0.9)',
                    borderpad=2
                ))

            fig_attack.update_layout(annotations=annotations_attack)
            
            fig_attack.update_layout(
                mapbox_style="white-bg",
                mapbox=dict(
                    center=dict(lat=1.274, lon=32.290),
                    zoom=5.0,
                    layers=[]
                ),
                margin=dict(r=0, t=0, l=0, b=0),
                height=380,
                showlegend=False,
                transition_duration=0,
                autosize=True,
            )
            
            st.plotly_chart(fig_attack, use_container_width=True, config={'displayModeBar': False, 'staticPlot': False, 'toImageButtonOptions': {'format': 'png', 'filename': 'attack_rates_map', 'height': 400, 'width': 600, 'scale': 2}})
        
        # 4. Bottom Right: Current Case Rate by District (Last 21 Days)
        with col4:
            st.markdown("<h4 style='font-size: 18px; margin-bottom: 10px;'>Current Case Rate by District (Last 21 Days, Per 100K)</h4>", unsafe_allow_html=True)
            
            # Prepare data for current rates map
            z_values_current = [current_rates.get(loc, 0) for loc in locations]
            max_current = max(z_values_current) if z_values_current else 0

            fig_current = go.Figure(data=go.Choroplethmapbox(
                geojson=districts_geojson,
                locations=locations,
                featureidkey="properties.name",
                z=z_values_current,
                zmin=0,
                zmax=max(11, max_current),
                colorscale=[
                    [0, '#E8E8E8'],       # 0: Grey
                    [0.045, '#FCE4EC'],   # 0.1-4.9: Very Light Pink
                    [0.45, '#F48FB1'],    # 5-10.9: Light Pink
                    [1.0, '#EC407A']      # 11+: Pink
                ],
                marker_opacity=0.85,
                marker_line_width=1.5,
                marker_line_color='white',
                hovertemplate='<b>%{location}</b><br>Current Rate: %{z:.1f} per 100K<extra></extra>',
                showscale=False
            ))

            # Add custom legend as annotations
            legend_items_current = [
                {'label': '0', 'color': '#E8E8E8'},
                {'label': '0.1-4.9', 'color': '#FCE4EC'},
                {'label': '5-10.9', 'color': '#F48FB1'}
            ]

            annotations_current = [dict(
                text="<b>Current (per 100K)</b>",
                x=0.02, y=0.98,
                xref='paper', yref='paper',
                showarrow=False,
                font=dict(size=12, family="Inter, sans-serif", color='#2C3E50'),
                xanchor='left', yanchor='top',
                bgcolor='rgba(255,255,255,0.9)',
                bordercolor='rgba(0,0,0,0.2)',
                borderwidth=1,
                borderpad=4
            )]

            for i, item in enumerate(legend_items_current):
                # Add color box as a separate annotation
                annotations_current.append(dict(
                    text="█",
                    x=0.02, y=0.92 - i*0.05,
                    xref='paper', yref='paper',
                    showarrow=False,
                    font=dict(size=16, family="Arial", color=item['color']),
                    xanchor='left', yanchor='top'
                ))
                # Add label text
                annotations_current.append(dict(
                    text=item['label'],
                    x=0.04, y=0.92 - i*0.05,
                    xref='paper', yref='paper',
                    showarrow=False,
                    font=dict(size=10, family="Inter, sans-serif", color='#2C3E50'),
                    xanchor='left', yanchor='top',
                    bgcolor='rgba(255,255,255,0.9)',
                    borderpad=2
                ))

            fig_current.update_layout(annotations=annotations_current)
            
            fig_current.update_layout(
                mapbox_style="white-bg",
                mapbox=dict(
                    center=dict(lat=1.274, lon=32.290),
                    zoom=5.0,
                    layers=[]
                ),
                margin=dict(r=0, t=0, l=0, b=0),
                height=380,
                showlegend=False,
                transition_duration=0,
                autosize=True,
            )
            
            st.plotly_chart(fig_current, use_container_width=True, config={'displayModeBar': False, 'staticPlot': False, 'toImageButtonOptions': {'format': 'png', 'filename': 'current_rates_map', 'height': 400, 'width': 600, 'scale': 2}})
        
    except Exception as e:
        st.error(f"Error creating choropleth maps: {str(e)}")
        import traceback
        st.error(f"Traceback: {traceback.format_exc()}")


if __name__ == "__main__":
    main()