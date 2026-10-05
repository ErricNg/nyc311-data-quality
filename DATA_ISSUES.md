# Data issues found

Data: NYC 311 service requests, 2026-09-01 to 2026-09-07
Downloaded: 2026-10-01
Rows: 71,830 | Columns: 44
Note: the source dataset is updated daily, so a later download may differ.

## Checked and clean

- unique_key: 0 missing, 0 repeated IDs, 0 fully identical rows
- created_date: 0 missing, 0 unparseable, all within Sept 1-7
- closed_date: 0 unparseable values
- status vs closed_date: every Closed request has a closed_date (64,898 of 64,898)
- The 5,968 empty closed_date values (8.3%) all belong to requests that are not Closed (In Progress 4,013, Open 1,839, Assigned 83, Pending 33). Expected missingness, not an error.

## Issues found

| #   | Column               | Issue                                              | Count      | Notes                                                                                                                                                                                                                                          |
| --- | -------------------- | -------------------------------------------------- | ---------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1   | status / closed_date | close date present but status is not Closed        | 964 (1.3%) | By agency: DOB 810, DEP 119, DOT 29, HPD 4, DPR 1, NYPD 1. By status: Open 696, Assigned 146, In Progress 114, Unspecified 7, Pending 1. Top complaint types: Building/Use 363, General Construction/Plumbing 202, Elevator 154. Cause unknown |
| 2   | closed_date          | closed before created, under 1 minute              | 23         | All DEP; closed time equals created time with the seconds dropped (23 of 23)                                                                                                                                                                   |
| 3   | closed_date          | closed before created, about 9h15m                 | 1          | DOT, unique_key 70290962                                                                                                                                                                                                                       |
| 4   | closed_date / status | closed about 2 days before created, status Pending | 1          | DOT, unique_key 70273435. Also one of the 964 in issue 1                                                                                                                                                                                       |
| 5   | status               | value "Unspecified"                                | 7          | Possible placeholder; all 7 have a close date                                                                                                                                                                                                  |

## Observations (not errors)

- DOB: 810 of the 964 status conflicts (84%) come from DOB. DOB has 2,346 requests and 2,346 close times, so every DOB request appears to have a closed_date, and 34.5% of them are not marked Closed. Hypothesis: for DOB, closed_date may not mean the request was closed. NOT YET VERIFIED.
- Close times recorded to the minute: share of close times with 0 seconds is DEP 91.8%, DOB 65.4%, DOT 49.6%. Chance alone would give about 1.7%. So minute-level recording is common across agencies, not unique to DEP. (Remaining agencies still to review.)
- Because of this, many close times may be up to 59 seconds early. Only requests closed within the same minute they were created show up as a contradiction, which is why issue 2 is limited to 23 rows.
- Censoring: requests created late in the week had less time to be closed than requests created early in the week. Any average time-to-close from this data is biased low for recent requests.

## Decisions so far

- Rows with closed_date before created_date (issues 2, 3, 4; 25 rows): FLAG. Do not fix or drop. We cannot tell which date is wrong, and dropping loses otherwise valid data.
- Empty closed_date on non-Closed requests: LEAVE. Missing is meaningful here.
- Issue 1 (964 rows): leaning FLAG, decide after checking the DOB hypothesis.
- Issue 5 (7 rows): not decided yet.

## Still to check

- DOB: does every DOB request have a closed_date? (cell above)
- remaining rows of the per-agency 0-seconds table
- borough, city, complaint_type spelling and consistency
- placeholder values (Unspecified, N/A) hiding in text columns
- ZIP code format and latitude/longitude ranges
