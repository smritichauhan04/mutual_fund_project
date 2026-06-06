import pandas as pd
from sqlalchemy import create_engine
from pathlib import Path
import warnings

# Suppress warnings for clean output
warnings.simplefilter(action='ignore', category=FutureWarning)

BASE_DIR = Path.cwd()
RAW_DIR = BASE_DIR / 'data' / 'raw'
PROCESSED_DIR = BASE_DIR / 'data' / 'processed'
DB_DIR = BASE_DIR / 'data' / 'db'

print("\nStarting Day 2 ETL Pipeline...")

# 1. Clean nav_history
print("Cleaning NAV History...")
df_nav = pd.read_csv(RAW_DIR / '02_nav_history.csv')
df_nav.columns = df_nav.columns.str.strip().str.lower()
df_nav['date'] = pd.to_datetime(df_nav['date'])
df_nav = df_nav.sort_values(by=['amfi_code', 'date'])

def fill_nav_gaps(group):
    group = group.set_index('date')
    full_date_range = pd.date_range(start=group.index.min(), end=group.index.max(), freq='D')
    group = group.reindex(full_date_range).ffill()
    group.index.name = 'date'
    return group.reset_index()

df_nav = df_nav.groupby('amfi_code', group_keys=False).apply(fill_nav_gaps, include_groups=False)
df_nav = df_nav.drop_duplicates()
df_nav = df_nav[df_nav['nav'] > 0] 
df_nav.to_csv(PROCESSED_DIR / 'cleaned_nav_history.csv', index=False)

# 2. Clean investor_transactions
print("Cleaning Transactions...")
df_trans = pd.read_csv(RAW_DIR / '08_investor_transactions.csv')
df_trans.columns = df_trans.columns.str.strip().str.lower() 
df_trans = df_trans.rename(columns={'transaction_date': 'date', 'amount_inr': 'amount'})
df_trans['date'] = pd.to_datetime(df_trans['date'])
df_trans['transaction_type'] = df_trans['transaction_type'].str.capitalize()
df_trans = df_trans[df_trans['amount'] > 0]
if 'kyc_status' in df_trans.columns:
    df_trans['kyc_status'] = df_trans['kyc_status'].str.upper()
df_trans.to_csv(PROCESSED_DIR / 'cleaned_transactions.csv', index=False)

# 3. Clean scheme_performance
print("Cleaning Performance...")
df_perf = pd.read_csv(RAW_DIR / '07_scheme_performance.csv')
df_perf.columns = df_perf.columns.str.strip().str.lower() 

# THE FINAL FIX: Rename columns to match the database expectations exactly!
df_perf = df_perf.rename(columns={
    'return_1yr_pct': '1yr_return',
    'expense_ratio_pct': 'expense_ratio',
    'aum_crore': 'aum_cr'
})

df_perf['1yr_return'] = pd.to_numeric(df_perf['1yr_return'], errors='coerce')
df_perf = df_perf[(df_perf['expense_ratio'] >= 0.1) & (df_perf['expense_ratio'] <= 2.5)]
df_perf.to_csv(PROCESSED_DIR / 'cleaned_performance.csv', index=False)

# 4. Load into SQLite Database
print("Loading into SQLite Database...")
db_path = DB_DIR / 'bluestock_mf.db'
engine = create_engine(f'sqlite:///{db_path}')

df_nav.to_sql('fact_nav', engine, if_exists='replace', index=False)
df_trans.to_sql('fact_transactions', engine, if_exists='replace', index=False)
df_perf.to_sql('fact_performance', engine, if_exists='replace', index=False)

print("✅ Pipeline complete! Your local database bluestock_mf.db is created.")
# ---------------------------------------------------------
# 5. Clean Remaining Auxiliary Files
print("\nProcessing remaining auxiliary CSV files...")

aux_files = [
    ('01_fund_master (1).csv', '01_fund_master.csv'), # Fixing the weird name!
    ('03_aum_by_fund_house.csv', '03_aum_by_fund_house.csv'),
    ('04_monthly_sip_inflows.csv', '04_monthly_sip_inflows.csv'),
    ('05_category_inflows.csv', '05_category_inflows.csv'),
    ('06_industry_folio_count.csv', '06_industry_folio_count.csv'),
    ('09_portfolio_holdings.csv', '09_portfolio_holdings.csv'),
    ('10_benchmark_indices.csv', '10_benchmark_indices.csv')
]

for raw_name, clean_name in aux_files:
    try:
        # Read the file
        df_aux = pd.read_csv(RAW_DIR / raw_name)
        # Clean the column names (lowercase, remove hidden spaces)
        df_aux.columns = df_aux.columns.str.strip().str.lower()
        # Save to the processed folder
        df_aux.to_csv(PROCESSED_DIR / clean_name, index=False)
        print(f"  -> Cleaned {clean_name}")
    except FileNotFoundError:
        print(f"  -> ⚠️ Could not find {raw_name} - skipping.")

print("\n✅ All 10 CSV files are now cleaned and in the processed folder!")