import pandas as pd
import re

def load_inventory_data(file_path):
    """Load inventory data from CSV file"""
    return pd.read_csv(file_path)

def process_inventory_data(df):
    """Process inventory data"""
    # Create description from fabric composition
    df["Description"] = df.apply(
        lambda row: f"Shell: {row['fabric composition']}, Lining: {row['lining composition']}",
        axis=1
    )
    
    # Drop original columns
    df = df.drop(["fabric composition", "lining composition"], axis=1)
    
    # Clean up description text
    df["Description"] = (df["Description"]
                         .str.replace("%", "% ")
                         .str.replace(",", ", ")
                         .str.replace(r'\s+', ' ', regex=True)
                         .str.strip())
    
    return df 