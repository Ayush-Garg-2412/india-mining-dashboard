import pandas as pd
import numpy as np

def load_and_clean():
    df = pd.read_csv('data/india_mining_production.csv')
    
    # Fix Year column - extract start year as integer
    df['Year_Label'] = df['Year']  # keep original for display
    df['Year'] = df['Year'].str[:4].astype(int)
    
    # Define key minerals we'll focus on for the dashboard
    # Fuels
    fuel_cols_qty = [
        'Fuels - Coal - Quantity (th.tonne)',
        'Fuels - Lignite - Quantity (th.tonne)',
        'Fuels - Natural Gas - Quantity (mcm)',
        'Fuels - Petroleum (Crude) - Quantity (th.tonne)',
    ]
    
    # Metallic - the commercially important ones
    metallic_cols_qty = [
        'Metallic - Bauxite - Quantity (th.tonne)',
        'Metallic - Chromite - Quantity (tonne)',
        'Metallic - Gold - Quantity (Kilogram)',
        'Metallic - Iron Ore - Quantity (th.Tonne)',
        'Metallic - Manganese Ore - Quantity (th.tonne)',
        'Metallic - Zinc Concetrates - Quantity (tonne)',
        'Metallic - Lead Concentrate - Quantity (tonne)',
    ]
    
    # Value columns for revenue analysis
    value_cols = [
        'Fuels - Coal - Value',
        'Fuels - Lignite - Value',
        'Fuels - Natural Gas - Value',
        'Fuels - Petroleum (Crude) - Value',
        'Metallic - Bauxite - Value',
        'Metallic - Iron Ore - Value',
        'Metallic - Gold - Value',
        'Metallic - Zinc Concetrates - Value',
        'Metallic - Lead Concentrate - Value',
    ]
    
    # Compute sector totals
    df['Fuels_Total_Value'] = df['Fuels - Coal - Value'] + df['Fuels - Lignite - Value'] + \
                               df['Fuels - Natural Gas - Value'] + df['Fuels - Petroleum (Crude) - Value']
    
    df['Metallic_Total_Value'] = df['Metallic - Bauxite - Value'] + df['Metallic - Iron Ore - Value'] + \
                                  df['Metallic - Gold - Value'] + df['Metallic - Zinc Concetrates - Value'] + \
                                  df['Metallic - Lead Concentrate - Value']
    
    # Year-over-year growth for total mining value
    df['YoY_Growth_Pct'] = df['All Minerals - Value'].pct_change() * 100
    
    # Coal share of total fuel value
    df['Coal_Share_Pct'] = (df['Fuels - Coal - Value'] / df['Fuels_Total_Value']) * 100
    
    # Iron ore share of metallic value
    df['IronOre_Share_Pct'] = (df['Metallic - Iron Ore - Value'] / df['Metallic_Total_Value']) * 100
    
    return df

if __name__ == "__main__":
    df = load_and_clean()
    print("=== CLEANED DATA SHAPE ===")
    print(df.shape)
    
    print("\n=== YEAR RANGE ===")
    print(f"From {df['Year'].min()} to {df['Year'].max()}")
    
    print("\n=== TOTAL MINING VALUE TREND ===")
    print(df[['Year_Label', 'All Minerals - Value', 'YoY_Growth_Pct']].to_string(index=False))
    
    print("\n=== SECTOR VALUE BREAKDOWN (last year) ===")
    last = df.iloc[-1]
    print(f"Fuels Total Value: {last['Fuels_Total_Value']:,}")
    print(f"Metallic Total Value: {last['Metallic_Total_Value']:,}")
    print(f"Coal share of Fuels: {last['Coal_Share_Pct']:.1f}%")
    print(f"Iron Ore share of Metallics: {last['IronOre_Share_Pct']:.1f}%")