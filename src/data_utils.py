"""
Data utilities for the Ethiopia Financial Inclusion Forecasting project.
"""

import pandas as pd
import numpy as np
from datetime import datetime
import re

def load_data(raw_data_path, reference_path):
    """
    Load the unified dataset and reference codes.
    
    Args:
        raw_data_path: Path to the main dataset
        reference_path: Path to reference codes file
    
    Returns:
        df: Main dataset
        reference_df: Reference codes
    """
    df = pd.read_csv(raw_data_path)
    reference_df = pd.read_csv(reference_path)
    return df, reference_df

def validate_schema(df):
    """
    Validate that the dataset follows the expected schema.
    
    Args:
        df: DataFrame to validate
    
    Returns:
        dict: Validation results
    """
    required_columns = [
        'record_type', 'pillar', 'category', 'indicator_code', 'indicator_name',
        'value_numeric', 'value_text', 'observation_date', 'name', 'description',
        'source_name', 'source_url', 'confidence', 'parent_id', 'related_indicator',
        'impact_direction', 'impact_magnitude', 'lag_months', 'evidence_basis',
        'collected_by', 'collection_date', 'notes'
    ]
    
    missing_columns = [col for col in required_columns if col not in df.columns]
    
    valid_record_types = ['observation', 'event', 'impact_link', 'target']
    invalid_types = df[~df['record_type'].isin(valid_record_types)]
    
    return {
        'missing_columns': missing_columns,
        'invalid_record_types': invalid_types,
        'n_rows': len(df),
        'n_unique_indicators': df['indicator_code'].nunique()
    }

def get_indicator_summary(df):
    """
    Create a summary of all indicators in the dataset.
    
    Args:
        df: DataFrame with observations
    
    Returns:
        DataFrame: Indicator summary
    """
    observations = df[df['record_type'] == 'observation']
    
    summary = observations.groupby(['indicator_code', 'indicator_name', 'pillar']).agg({
        'value_numeric': ['count', 'mean', 'min', 'max'],
        'observation_date': ['min', 'max']
    }).round(2)
    
    summary.columns = ['n_obs', 'mean_value', 'min_value', 'max_value', 'first_date', 'last_date']
    return summary

def validate_record(row):
    """
    Validate a single record based on its type.
    
    Args:
        row: Series representing a record
    
    Returns:
        dict: Validation results with errors and warnings
    """
    errors = []
    warnings = []
    
    record_type = row['record_type']
    
    if record_type == 'observation':
        if pd.isna(row['value_numeric']) and pd.isna(row['value_text']):
            errors.append("Observation must have either numeric or text value")
        if pd.isna(row['indicator_code']):
            errors.append("Observation must have indicator_code")
            
    elif record_type == 'event':
        if pd.isna(row['category']):
            errors.append("Event must have a category")
        if pd.isna(row['name']):
            errors.append("Event must have a name")
            
    elif record_type == 'impact_link':
        if pd.isna(row['parent_id']):
            errors.append("Impact link must have parent_id")
        if pd.isna(row['related_indicator']):
            errors.append("Impact link must have related_indicator")
            
    elif record_type == 'target':
        if pd.isna(row['value_numeric']):
            errors.append("Target must have value_numeric")
    
    return {'errors': errors, 'warnings': warnings}

def create_enrichment_template():
    """
    Create a template for data enrichment records.
    
    Returns:
        dict: Template for new records
    """
    return {
        'observation': {
            'record_type': 'observation',
            'pillar': None,
            'category': None,
            'indicator_code': None,
            'indicator_name': None,
            'value_numeric': None,
            'value_text': None,
            'observation_date': None,
            'name': None,
            'description': None,
            'source_name': None,
            'source_url': None,
            'confidence': None,
            'parent_id': None,
            'related_indicator': None,
            'impact_direction': None,
            'impact_magnitude': None,
            'lag_months': None,
            'evidence_basis': None,
            'collected_by': None,
            'collection_date': None,
            'notes': None
        }
    }