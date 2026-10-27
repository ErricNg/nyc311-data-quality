# NYC 311 Data Quality Pipeline

Checks and cleans one week of NYC 311 data, then proves it is clean with a schema, tests and a report.

## Problem

Raw 311 data looks fine until you check it. In my 71,830 requests I found:

- 964 have a close date but the status is not Closed
- 80 boroughs say "Unspecified", and `isna()` can't see that
- 25 were closed before they were created
- The same complaint is spelled two ways (`PLUMBING` and `Plumbing`)

## Data

NYC Open Data 311 requests (Socrata API), Sept 1 to 7, 2026. 71,830 rows and 44 columns. The source updates daily, so a new download may differ.

## How to run

Python 3.13, Windows. Run from the repo folder.

```
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt

python -m src.nyc311.download     # download raw data
python -m src.nyc311.clean        # clean it, save a Parquet file
python -m src.nyc311.schema       # check raw (fails) and clean (passes)
python -m src.nyc311.report       # write QUALITY_REPORT.md
python -m pytest                  # run the 10 tests
```

The `data/` folder is not on GitHub. These commands make it.

## What it does

1. Reads the CSV as text, so `07302` keeps its zero and `N/A` stays a word
2. Turns dates into dates and coordinates into numbers (ZIP stays text)
3. Turns "Unspecified" and "Unknown" into real empty values
4. Adds a clean complaint type column (the original stays)
5. Adds 3 flag columns for rows that look wrong (the values stay)
6. Saves a Parquet file. The raw file is never changed.

## Results

| Check                         | Before | After |
| ----------------------------- | ------ | ----- |
| rows                          | 71830  | 71830 |
| borough 'Unspecified'         | 80     | 0     |
| police_precinct 'Unspecified' | 1301   | 0     |
| distinct complaint types      | 155    | 153   |
| closed_date_suspect           | -      | 964   |
| closed_before_created         | -      | 25    |
| coord_pair_incomplete         | -      | 16    |

No rows are dropped.

## Decisions and limits

- If I'm not sure a value is wrong, I flag it and keep it. I never guess a missing value.
- I kept every column so no information is lost.
- I don't know why DOB close dates often equal the created date, so I flagged them and left them.
- It's one week of data. Time-to-close is biased low for recent requests.
- The ZIP check only checks the format, not whether the ZIP is real.

More detail: `DATA_ISSUES.md`, `DECISIONS.md`, `CLEANING_RULES.md`.

## Structure

```
notebooks/    exploration notebook
src/nyc311/   download, clean, schema, report
tests/        10 pytest tests
```
