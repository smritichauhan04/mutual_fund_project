 Bluestock Mutual Fund - Star Schema Definition

1. Dimension Tables
CREATE TABLE dim_fund (
    amfi_code INTEGER PRIMARY KEY,
    fund_name TEXT,
    category TEXT,
    fund_house TEXT
);

CREATE TABLE dim_date (
    date_id TEXT PRIMARY KEY,
    year INTEGER,
    month INTEGER,
    day INTEGER,
    is_weekend BOOLEAN
);

2. Fact Tables
CREATE TABLE fact_nav (
    nav_id INTEGER PRIMARY KEY AUTOINCREMENT,
    amfi_code INTEGER,
    date TEXT,
    nav REAL,
    FOREIGN KEY(amfi_code) REFERENCES dim_fund(amfi_code),
    FOREIGN KEY(date) REFERENCES dim_date(date_id)
);

CREATE TABLE fact_transactions (
    transaction_id INTEGER PRIMARY KEY,
    date TEXT,
    amfi_code INTEGER,
    transaction_type TEXT,
    amount REAL,
    kyc_status TEXT,
    state TEXT,
    FOREIGN KEY(amfi_code) REFERENCES dim_fund(amfi_code),
    FOREIGN KEY(date) REFERENCES dim_date(date_id)
);

CREATE TABLE fact_performance (
    amfi_code INTEGER PRIMARY KEY,
    1yr_return REAL,
    3yr_return REAL,
    5yr_return REAL,
    expense_ratio REAL,
    aum_cr REAL,
    FOREIGN KEY(amfi_code) REFERENCES dim_fund(amfi_code)
);