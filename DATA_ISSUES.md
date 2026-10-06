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
- Columns with 0.0% missing (rounded to one decimal): unique_key, created_date, agency, agency_name, complaint_type, status, community_board, police_precinct, park_borough, borough, open_data_channel_type
- agency and agency_name: 14 distinct values each and 14 distinct pairs, so one-to-one (agency_name is redundant)
- latitude and location: empty on exactly the same 1,301 rows (70,529 have both, 1,301 have neither, 0 have only one)

## Issues found

| #   | Column               | Issue                                              | Count      | Notes                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| --- | -------------------- | -------------------------------------------------- | ---------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1   | status / closed_date | close date present but status is not Closed        | 964 (1.3%) | By agency and status: DOB Open 692, DOB Assigned 118, DEP In Progress 114, DOT Assigned 28, DEP Unspecified 5, HPD Open 4, DOT Pending 1, DPR Unspecified 1, NYPD Unspecified 1. DOB Open: closed_date equals created_date in 692 of 692 rows and never equals resolution_action_updated_date (0 of 692). DOB Assigned: closed_date equals created_date in 3 of 118 and equals resolution_action_updated_date in 115 of 118. All other groups: closed_date never equals created_date. Meaning of the field is unknown                                                                                                                                                                                                                                                                                             |
| 2   | closed_date          | closed before created, under 1 minute              | 23         | All DEP; closed time equals created time with the seconds dropped (23 of 23)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| 3   | closed_date          | closed before created, about 9h15m                 | 1          | DOT, unique_key 70290962                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| 4   | closed_date / status | closed about 2 days before created, status Pending | 1          | DOT, unique_key 70273435. Also one of the 964 in issue 1                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| 5   | status               | value "Unspecified"                                | 7          | DEP 5, DPR 1, NYPD 1. All 7 have a closed_date (none equal to created_date). Possible placeholder                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| 6   | 9 columns            | nearly empty                                       | 9 columns  | taxi_company_borough 99.9%, due_date 99.7%, facility_type 99.7%, road_ramp 99.7%, bridge_highway_direction 99.7%, bridge_highway_name 99.5%, bridge_highway_segment 99.5%, taxi_pick_up_location 99.1%, vehicle_type 94.9%. Five tested: filled values come from specific complaint types (taxi_company_borough only For Hire Vehicle Complaint 56 and Report 2; facility_type only Derelict Vehicles, 196 of 196, value "DSNY Garage"; vehicle_type mostly Abandoned Vehicle, Noise - Vehicle, Illegal Parking; road_ramp and bridge_highway_name mostly Highway Condition, Encampment, Homeless Person Assistance, Panhandling). Looks structural. Not tested: whether those types always fill the column. Not tested at all: due_date, bridge_highway_direction, bridge_highway_segment, taxi_pick_up_location |

## Observations (not errors)

- DOB: all 2,346 DOB requests have a closed_date, but only 1,536 are marked Closed (Open 692, Assigned 118). Median closed_date minus created_date by status: Closed about 2 days, Assigned about 12.5 days, Open exactly 0. closed_date equals resolution_action_updated_date in 1,402 of 1,536 Closed (91.3%), 115 of 118 Assigned (97.5%), 0 of 692 Open. Hypothesis: for Assigned DOB requests, closed_date may record the last action date, not a closure. NOT VERIFIED.
- Close times recorded to the minute: share of close times with 0 seconds is DEP 91.8%, DOB 65.4%, DOT 49.6%. These are the three highest agencies in the table. Chance alone would give about 1.7%. So minute-level recording is common across agencies, not unique to DEP.
- Because of this, many close times may be up to 59 seconds early. Only requests closed within the same minute they were created show up as a contradiction, which is why issue 2 is limited to 23 rows.
- closed_date has 41,038 distinct values among 65,862 non-empty rows, so many requests share an identical close timestamp. Cause unknown.
- longitude, x_coordinate_state_plane and y_coordinate_state_plane are also 1.8% missing (same rows not yet confirmed). Whether location is a combined copy of latitude/longitude is not yet verified.
- borough: 0% missing but 6 distinct values; New York City has 5 boroughs, so check the sixth value. park_borough also has 6 distinct values.
- city has 50 distinct values and 6.9% missing, and mixes borough and neighborhood names (seen in the first rows). landmark is 29.7% missing and often repeated the street name in the first 10 rows (to verify).
- created_date has 61,337 distinct values among 71,830 rows; about 10,500 requests share a timestamp with another request.
- Censoring: requests created late in the week had less time to be closed than requests created early in the week. Any average time-to-close from this data is biased low for recent requests.

## Decisions so far

- Rows with closed_date before created_date (issues 2, 3, 4; 25 rows): FLAG. Do not fix or drop. We cannot tell which date is wrong, and dropping loses otherwise valid data.
- Empty closed_date on non-Closed requests: LEAVE. Missing is meaningful here.
- Issue 1: candidate rule for Phase 3: compute time-to-close only where status is Closed. For the 692 DOB Open rows, fix vs flag vs leave is not decided yet.
- Issues 5 and 6: not decided yet.
- agency_name is redundant with agency: decide in Phase 3 which to keep.

## Still to check

- borough and park_borough values (the sixth value)
- whether longitude and the state-plane coordinates are empty on the same 1,301 rows, and what a location value contains
- sparse columns: reverse test (does each complaint type always fill its column), and the four untested columns
- city, complaint_type spelling and consistency
- placeholder values (Unspecified, N/A) hiding in text columns
- ZIP code format and latitude/longitude ranges
