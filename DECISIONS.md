# Data issues

- Data: NYC 311 requests, 2026-09-01 to 2026-09-07 (downloaded 2026-10-01)
- Size: 71,830 rows, 44 columns

## Clean

- unique_key: no missing, no repeats
- created_date: no missing, all within Sept 1-7
- closed_date: all parse. Empty only on non-Closed requests (5,968), which is expected
- Every Closed request has a closed_date (64,898)
- incident_zip: all 5 digits (602 empty)
- latitude, longitude: all numeric, all inside NYC
- city, complaint_type: no stray spaces. city has no spelling variants

## Issues

| #   | Column                       | Problem                                   | Rows      | Notes                                                                                                                                                                                                                                                                                                                                                                            |
| --- | ---------------------------- | ----------------------------------------- | --------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1   | status, closed_date          | has a close date but status is not Closed | 964       | DOB Open 692 (close date = created date, looks fake), DOB Assigned 118, DEP In Progress 114, DOT Assigned 28, other 12                                                                                                                                                                                                                                                           |
| 2   | closed_date                  | closed before created, under 1 minute     | 23        | All DEP. The seconds were dropped                                                                                                                                                                                                                                                                                                                                                |
| 3   | closed_date                  | closed before created, about 9 hours      | 1         | DOT, key 70290962                                                                                                                                                                                                                                                                                                                                                                |
| 4   | closed_date                  | closed about 2 days before created        | 1         | DOT, key 70273435 (also in #1)                                                                                                                                                                                                                                                                                                                                                   |
| 5   | status                       | "Unspecified"                             | 7         | DEP 5, DPR 1, NYPD 1                                                                                                                                                                                                                                                                                                                                                             |
| 6   | 9 columns                    | nearly empty (95% to 99.9%)               | 9         | taxi_company_borough, due_date, facility_type, road_ramp, bridge_highway_direction, bridge_highway_name, bridge_highway_segment, taxi_pick_up_location, vehicle_type. Always filled for their complaint type: the 4 highway columns (Highway Condition), vehicle_type (Abandoned Vehicle, Noise - Vehicle). Only sometimes filled: due_date, facility_type, taxi_company_borough |
| 7   | borough, park_borough        | "Unspecified"                             | 80        | Same 80 rows in both. 76 also have no coordinates                                                                                                                                                                                                                                                                                                                                |
| 8   | x, y state-plane coordinates | only one of the pair is filled            | 16        | 11 are DOT Street Condition, which is only 2.4% of all rows                                                                                                                                                                                                                                                                                                                      |
| 9   | complaint_type               | same complaint, two spellings             | 1,947     | PLUMBING (HPD) vs Plumbing (DOB). ELEVATOR (HPD) vs Elevator (DOB)                                                                                                                                                                                                                                                                                                               |
| 10  | 5 columns                    | placeholder text                          | see notes | park_facility_name "Unspecified" 71,745. open_data_channel_type "UNKNOWN" 5,164. police_precinct "Unspecified" 1,301. location_type "Unknown" 25. descriptor_2 "Unknown" 1                                                                                                                                                                                                       |

`isna()` cannot see the placeholders in #5, #7 and #10.

## Redundant columns

- agency_name = agency
- location = latitude + longitude
- park_borough = borough (identical on all rows)

## Good to know

- 1,301 rows have no coordinates. latitude, longitude and location are always empty together.
- city mixes boroughs, neighborhoods and "NEW YORK". It is not a borough column, so use borough.
- Close times are often recorded to the minute: DEP 92%, DOB 65%, DOT 50%.
- DOB: all 2,346 requests have a close date, but only 1,536 are Closed. On Assigned rows the close date often equals the last update (not verified).
- Time-to-close is biased low for recent requests, because they had less time to close.

## Decisions

See `DECISIONS.md`.

## Not pursued

- 0-seconds table for the remaining agencies. DEP, DOB and DOT already show the pattern.

Status: Phases 2:finding and documenting issue and 3:decision done.
