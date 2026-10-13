# Decisions

How the cleaning code (`clean.py`) will handle each issue in `DATA_ISSUES.md`.

## Rules

- The raw file is never edited. Cleaning writes a new file to `data/processed/`.
- FIX: change the value. FLAG: keep the value and add a marker column. DROP: remove it. LEAVE: keep it as is.
- Placeholder text that means "unknown" (like "Unspecified") becomes an empty value, so `isna()` can find it.
- Keep data when in doubt. No column is dropped in this project.

## Table

| Issue                                                         | Decision | Marker or new column             | Why                                                                                                                           |
| ------------------------------------------------------------- | -------- | -------------------------------- | ----------------------------------------------------------------------------------------------------------------------------- |
| 1. Close date but status not Closed (964)                     | FLAG     | `closed_date_suspect`            | We cannot tell a system error from a real close. Keep the value, leave flagged rows out of time-to-close.                     |
| 2, 3, 4. Closed before created (25)                           | FLAG     | `closed_before_created`          | We cannot tell which date is wrong.                                                                                           |
| 5. status "Unspecified" (7)                                   | FLAG     | covered by `closed_date_suspect` | All 7 rows are already inside issue 1. Not sure it is a placeholder, so the word stays.                                       |
| 6. 9 nearly empty columns                                     | LEAVE    | none                             | Their values are valid. Empty means "does not apply" or "not entered".                                                        |
| 7. borough "Unspecified" (80)                                 | FIX      | none                             | The word becomes empty, so a group-by does not show a sixth borough.                                                          |
| 8. Only one state-plane coordinate (16)                       | FLAG     | `coord_pair_incomplete`          | One coordinate alone cannot locate a point. Keep the values.                                                                  |
| 9. complaint_type spelling (1,947)                            | FIX      | `complaint_type_clean`           | Trim and lowercase into a new column. Keep the original and keep `agency`.                                                    |
| 10. Placeholder text in 5 columns                             | FIX      | none                             | The word becomes empty in `park_facility_name`, `police_precinct`, `open_data_channel_type`, `location_type`, `descriptor_2`. |
| Empty closed_date on non-Closed                               | LEAVE    | none                             | Empty is meaningful: not closed yet.                                                                                          |
| Exact-copy columns: `agency_name`, `location`, `park_borough` | LEAVE    | none                             | Nothing is lost by keeping them. The Phase 5 schema can check that each copy still matches its source.                        |

## Types

- Dates become datetimes.
- ZIP stays text.
- latitude and longitude become numbers.

## Drops

None.
