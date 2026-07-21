import pandas as pd
import numpy as np
import sys
import os

#add src to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.data_utils import load_data, validate_schema, get_indicator_summary

def test_import():
    """Test that imports work"""
    assert True

def test_validate_schema():
    """Test schema validation function exists"""
    from src.data_utils import validate_schema
    assert callable(validate_schema)

def test_get_indicator_summary():
    """Test indicator summary function exists"""
    from src.data_utils import get_indicator_summary
    assert callable(get_indicator_summary)

def test_load_data():
    """Test load data function exists"""
    from src.data_utils import load_data
    assert callable(load_data)

def test_pandas_import():
    """Test pandas is installed"""
    import pandas as pd
    assert pd is not None