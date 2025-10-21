# ===== CHOROPLETH MAP DATA FUNCTIONS =====

import streamlit as st
import pandas as pd
from sqlalchemy import text
from data_fetcher import engine

@st.cache_data(ttl=300)
def get_measles_cumulative_cases_by_district():
    """
    Get cumulative measles cases by district for choropleth map
    Returns dictionary: {district_name: total_cases}
    """
    try:
        with engine.connect() as conn:
            query = """
            WITH measles_events AS (
                SELECT DISTINCT 
                    e.event_id,
                    e.event_date,
                    e.dim_org_hierarchy_key
                FROM dwh.fact_eidsr_event_data e
                WHERE e.data_element_id = 'qIlO7yEpiVv' AND e.data_value = 'Measles (B05.0_B05.9)'
                  AND e.event_date IS NOT NULL
            )
            SELECT 
                doh.district_name,
                COUNT(DISTINCT me.event_id) as total_cases
            FROM measles_events me
            JOIN dwh.dim_eidsr_org_hierarchy doh ON me.dim_org_hierarchy_key = doh.dim_org_hierarchy_key
            WHERE doh.district_name IS NOT NULL
              AND doh.district_name != 'Unknown'
              AND doh.district_name != '1 Test District'
            GROUP BY doh.district_name
            ORDER BY total_cases DESC
            """
            
            df = pd.read_sql_query(text(query), conn)
            return dict(zip(df['district_name'], df['total_cases']))
            
    except Exception as e:
        st.error(f"Error fetching cumulative cases by district: {str(e)}")
        return {}


@st.cache_data(ttl=300)
def get_measles_districts_reporting_last_21_days():
    """
    Get districts reporting cases in last 21 days for choropleth map
    Returns dictionary: {district_name: case_count_last_21_days}
    """
    try:
        with engine.connect() as conn:
            query = """
            WITH measles_events AS (
                SELECT DISTINCT 
                    e.event_id,
                    e.event_date,
                    e.dim_org_hierarchy_key
                FROM dwh.fact_eidsr_event_data e
                WHERE e.data_element_id = 'qIlO7yEpiVv' AND e.data_value = 'Measles (B05.0_B05.9)'
                  AND e.event_date IS NOT NULL
                  AND e.event_date >= CURRENT_DATE - INTERVAL '21 days'
            )
            SELECT 
                doh.district_name,
                COUNT(DISTINCT me.event_id) as cases_last_21_days
            FROM measles_events me
            JOIN dwh.dim_eidsr_org_hierarchy doh ON me.dim_org_hierarchy_key = doh.dim_org_hierarchy_key
            WHERE doh.district_name IS NOT NULL
              AND doh.district_name != 'Unknown'
              AND doh.district_name != '1 Test District'
            GROUP BY doh.district_name
            ORDER BY cases_last_21_days DESC
            """
            
            df = pd.read_sql_query(text(query), conn)
            return dict(zip(df['district_name'], df['cases_last_21_days']))
            
    except Exception as e:
        st.error(f"Error fetching districts reporting last 21 days: {str(e)}")
        return {}


@st.cache_data(ttl=300)
def get_measles_attack_rates_by_district_cumulative():
    """
    Get cumulative attack rates per 100K population by district for choropleth map
    Returns dictionary: {district_name: attack_rate_per_100k}
    """
    try:
        with engine.connect() as conn:
            query = """
            WITH measles_events AS (
                SELECT DISTINCT 
                    e.event_id,
                    e.event_date,
                    e.dim_org_hierarchy_key
                FROM dwh.fact_eidsr_event_data e
                WHERE e.data_element_id = 'qIlO7yEpiVv' AND e.data_value = 'Measles (B05.0_B05.9)'
                  AND e.event_date IS NOT NULL
            ),
            district_cases AS (
                SELECT 
                    doh.district_name,
                    COUNT(DISTINCT me.event_id) as total_cases
                FROM measles_events me
                JOIN dwh.dim_eidsr_org_hierarchy doh ON me.dim_org_hierarchy_key = doh.dim_org_hierarchy_key
                WHERE doh.district_name IS NOT NULL
                  AND doh.district_name != 'Unknown'
                  AND doh.district_name != '1 Test District'
                GROUP BY doh.district_name
            )
            SELECT 
                district_name,
                total_cases,
                -- Simple attack rate calculation: cases per 100,000 as proportional rate
                ROUND((total_cases * 100000.0 / GREATEST(total_cases, 1000)), 2) as attack_rate_per_100k
            FROM district_cases
            WHERE total_cases > 0
            ORDER BY attack_rate_per_100k DESC
            """
            
            df = pd.read_sql_query(text(query), conn)
            return dict(zip(df['district_name'], df['attack_rate_per_100k']))
            
    except Exception as e:
        st.error(f"Error fetching attack rates by district: {str(e)}")
        return {}


@st.cache_data(ttl=300)
def get_measles_current_case_rates_by_district_21_days():
    """
    Get current case rates per 100K (last 21 days) by district for choropleth map
    Returns dictionary: {district_name: current_rate_per_100k}
    """
    try:
        with engine.connect() as conn:
            query = """
            WITH measles_events AS (
                SELECT DISTINCT 
                    e.event_id,
                    e.event_date,
                    e.dim_org_hierarchy_key
                FROM dwh.fact_eidsr_event_data e
                WHERE e.data_element_id = 'qIlO7yEpiVv' AND e.data_value = 'Measles (B05.0_B05.9)'
                  AND e.event_date IS NOT NULL
                  AND e.event_date >= CURRENT_DATE - INTERVAL '21 days'
            ),
            district_current_cases AS (
                SELECT 
                    doh.district_name,
                    COUNT(DISTINCT me.event_id) as current_cases
                FROM measles_events me
                JOIN dwh.dim_eidsr_org_hierarchy doh ON me.dim_org_hierarchy_key = doh.dim_org_hierarchy_key
                WHERE doh.district_name IS NOT NULL
                  AND doh.district_name != 'Unknown'
                  AND doh.district_name != '1 Test District'
                GROUP BY doh.district_name
            )
            SELECT 
                district_name,
                current_cases,
                -- Simple current rate calculation: cases per 100,000 as proportional rate
                ROUND((current_cases * 100000.0 / GREATEST(current_cases, 500)), 2) as current_rate_per_100k
            FROM district_current_cases
            WHERE current_cases > 0
            ORDER BY current_rate_per_100k DESC
            """
            
            df = pd.read_sql_query(text(query), conn)
            return dict(zip(df['district_name'], df['current_rate_per_100k']))
            
    except Exception as e:
        st.error(f"Error fetching current case rates by district: {str(e)}")
        return {}