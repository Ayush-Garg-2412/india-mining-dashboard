import pandas as pd
import numpy as np

# Load data
df = pd.read_csv('data/india_mining_production.csv')

# Basic structure
print("=== SHAPE ===")
print(df.shape)

print("\n=== COLUMNS ===")
for col in df.columns.tolist():
    print(col)

print("\n=== FIRST 3 ROWS ===")
print(df.head(3).to_string())

print("\n=== DATA TYPES ===")
print(df.dtypes)

print("\n=== NULL VALUES ===")
print(df.isnull().sum())