"""
File handler utilities for consistent CSV/Excel handling
"""

import pandas as pd
import os

def load_data(file_path):
    """
    Load data from CSV or Excel file with proper error handling.
    
    Args:
        file_path: Path to the file
        
    Returns:
        DataFrame: Loaded data
    
    Raises:
        FileNotFoundError: If file doesn't exist
        ValueError: If file format is not supported
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    
    try:
        if file_path.endswith('.csv'):
            return pd.read_csv(file_path)
        elif file_path.endswith(('.xlsx', '.xls')):
            return pd.read_excel(file_path)
        else:
            raise ValueError(f"Unsupported file format: {file_path}")
    except Exception as e:
        raise Exception(f"Error loading file {file_path}: {str(e)}")

def save_data(df, file_path):
    """
    Save data to CSV or Excel file with proper error handling.
    
    Args:
        df: DataFrame to save
        file_path: Path where to save
        
    Raises:
        ValueError: If file format is not supported
    """
    try:
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        if file_path.endswith('.csv'):
            df.to_csv(file_path, index=False)
        elif file_path.endswith(('.xlsx', '.xls')):
            df.to_excel(file_path, index=False)
        else:
            raise ValueError(f"Unsupported file format: {file_path}")
    except Exception as e:
        raise Exception(f"Error saving file {file_path}: {str(e)}")

def validate_dataframe(df, required_columns=None):
    """
    Validate DataFrame has required columns.
    
    Args:
        df: DataFrame to validate
        required_columns: List of required column names
        
    Returns:
        bool: True if valid
        
    Raises:
        ValueError: If validation fails
    """
    if required_columns:
        missing = [col for col in required_columns if col not in df.columns]
        if missing:
            raise ValueError(f"Missing required columns: {missing}")
    return True