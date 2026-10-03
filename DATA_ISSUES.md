# Data issues found

Data: NYC 311 service requests, 2026-09-01 to 2026-09-07
Downloaded: 2026-10-01
Rows: 71,830 | Columns: 44

## Checked and clean

- unique_key: 0 missing, 0 repeated IDs, 0 fully identical rows
- created_date: 0 missing, 0 unparseable, all within Sept 1-7
- closed_date: 0 unparseable values

## Issues found

| #   | Column               | Issue                                              | Count        | Notes                                                        |
| --- | -------------------- | -------------------------------------------------- | ------------ | ------------------------------------------------------------ |
| 1   | closed_date          | empty at download time                             | 5,968 (8.3%) | Likely still open; verify against status                     |
| 2   | closed_date          | closed before created, under 1 minute              | 23           | All DEP; closed time looks truncated to the minute (to test) |
| 3   | closed_date          | closed before created, about 9h15m                 | 1            | DOT, unique_key 70290962                                     |
| 4   | closed_date / status | closed about 2 days before created, status Pending | 1            | DOT, unique_key 70273435                                     |

## Decision so far

- Rows with closed_date before created_date: FLAG, do not fix or drop (we can't tell which date is wrong, and dropping loses valid data).

## Still to check

- status vs closed_date across all rows
- borough, city, complaint_type spelling and consistency
- placeholder values (Unspecified, N/A) hiding in text columns
- ZIP code format and latitude/longitude ranges
