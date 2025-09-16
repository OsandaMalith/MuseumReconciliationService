import re
import pandas as pd

def normalize_text(text: str) -> str:
    """Normalize text for better matching"""
    if not text:
        return ""
    # Convert to lowercase and remove extra spaces
    text = str(text).lower().strip()
    # Remove articles
    text = re.sub(r'\b(the|a|an)\b', '', text)
    # Remove punctuation
    text = re.sub(r'[^\w\s]', ' ', text)
    # Collapse multiple spaces
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def clean_float_value(value):
    """Clean and convert a value to float, return None if invalid"""
    if value is None or value == '' or pd.isna(value):
        return None
    try:
        return float(value)
    except (ValueError, TypeError):
        return None

def clean_numeric_value(value):
    """Clean and convert a value to integer, return None if invalid"""
    if value is None or value == '' or pd.isna(value):
        return None
    try:
        # Handle string values that might have commas or other formatting
        if isinstance(value, str):
            value = value.replace(',', '').strip()
        return int(float(value))  # Convert to float first to handle decimals, then to int
    except (ValueError, TypeError):
        return None