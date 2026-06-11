\# Bluestock Mutual Fund - Data Dictionary



\## dim\_fund

\* \*\*amfi\_code\*\* (INTEGER): Unique identifier for the mutual fund (Primary Key).

\* \*\*fund\_name\*\* (TEXT): Official name of the scheme.

\* \*\*category\*\* (TEXT): Equity, Debt, Hybrid, etc.



\## fact\_nav

\* \*\*date\*\* (TEXT): YYYY-MM-DD format. Reindexed and forward-filled to handle weekends/holidays.

\* \*\*nav\*\* (REAL): Net Asset Value. Validated to be > 0.



\## fact\_transactions

\* \*\*transaction\_type\*\* (TEXT): Standardized to 'Sip', 'Lumpsum', or 'Redemption'.

\* \*\*amount\*\* (REAL): Transaction value in INR. Validated > 0.

\* \*\*kyc\_status\*\* (TEXT): Enum representing customer verification state.



\## fact\_performance

\* \*\*1yr\_return\*\* (REAL): Annualized percentage return.

\* \*\*expense\_ratio\*\* (REAL): Management fee percentage. Validated between 0.1 and 2.5.

\* \*\*aum\_cr\*\* (REAL): Assets Under Management in Crores (Standardized unit).

