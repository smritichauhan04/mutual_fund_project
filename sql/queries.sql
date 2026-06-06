1. Top 5 funds by AUM
SELECT amfi_code, aum_cr FROM fact_performance ORDER BY aum_cr DESC LIMIT 5;

 2. Average NAV per month
SELECT strftime('%Y-%m', date) as month, AVG(nav) as avg_nav FROM fact_nav GROUP BY month ORDER BY month;

 3. SIP YoY growth (Total amount per year for SIPs)
SELECT strftime('%Y', date) as year, SUM(amount) as total_sip_amount FROM fact_transactions WHERE transaction_type = 'Sip' GROUP BY year ORDER BY year;

 4. Transactions by state
SELECT state, COUNT(*) as transaction_count, SUM(amount) as total_volume FROM fact_transactions GROUP BY state ORDER BY total_volume DESC;

 5. Funds with expense ratio < 1%
SELECT amfi_code, expense_ratio FROM fact_performance WHERE expense_ratio < 1.0 ORDER BY expense_ratio ASC;

 6. Total Redemption volume vs SIP volume
SELECT transaction_type, SUM(amount) as total_amount FROM fact_transactions GROUP BY transaction_type;

 7. Highest returning funds (1yr)
SELECT amfi_code, 1yr_return FROM fact_performance ORDER BY 1yr_return DESC LIMIT 10;

 8. Daily platform transaction volume
SELECT date, COUNT(transaction_id) as daily_trades, SUM(amount) as daily_volume FROM fact_transactions GROUP BY date ORDER BY date DESC;

 9. Funds requiring KYC attention
SELECT amfi_code, COUNT(*) as non_compliant_trades FROM fact_transactions WHERE kyc_status != 'VERIFIED' GROUP BY amfi_code ORDER BY non_compliant_trades DESC;

 10. Lowest expense ratio funds with positive returns
SELECT amfi_code, expense_ratio, 1yr_return FROM fact_performance WHERE 1yr_return > 0 ORDER BY expense_ratio ASC LIMIT 5;