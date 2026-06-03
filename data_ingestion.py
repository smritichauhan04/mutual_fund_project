import os
import pandas as pd

data_dir = "data/raw/"

# List of the 10 files
csv_files = [
    "01_fund_master (1).csv",
    "02_nav_history.csv",
    "03_aum_by_fund_house.csv",
    "04_monthly_sip_inflows.csv",
    "05_category_inflows.csv",
    "06_industry_folio_count.csv",
    "07_scheme_performance.csv",
    "08_investor_transactions.csv",
    "09_portfolio_holdings.csv",
    "10_benchmark_indices.csv"
]

print("LOADING AND INSPECTING DATASETS")
print("-" * 60)

for file_name in csv_files:
    file_path = os.path.join(data_dir, file_name)
    try:
        df = pd.read_csv(file_path)
        print(f"File: {file_name} | Rows: {df.shape}, Columns: {df.shape}")
    except Exception as e:
        print(f"Error reading {file_name}: {e}")

# Load master and history files for validation
fund_master = pd.read_csv(os.path.join(data_dir, "01_fund_master (1).csv"))
nav_history = pd.read_csv(os.path.join(data_dir, "02_nav_history.csv"))

print("\nFUND MASTER METADATA SUMMARY")
print("-" * 60)
print(f"Total Unique Fund Houses: {fund_master['fund_house'].nunique()}")
print(f"Total Categories: {fund_master['category'].nunique()}")

print("\nREFERENTIAL INTEGRITY CHECK")
print("-" * 60)
master_codes = set(fund_master['amfi_code'].unique())
nav_codes = set(nav_history['amfi_code'].unique())
missing_count = len(master_codes - nav_codes)

if missing_count == 0:
    print("STATUS: PASS - All AMFI codes in Master have historical data.")
else:
    print(f"STATUS: WARNING - {missing_count} funds missing historical data.")