from pathlib import Path

import pandas as pd

from src.nyc311.clean import OUT_PATH, RAW_PATH, load_raw

REPORT_PATH = Path("QUALITY_REPORT.md")


def build_report(raw, cleaned):
    """Return a markdown table of before/after counts."""
    rows = [
        ("rows", len(raw), len(cleaned)),
        ("borough 'Unspecified'", (raw["borough"] == "Unspecified").sum(),
         (cleaned["borough"] == "Unspecified").sum()),
        ("police_precinct 'Unspecified'", (raw["police_precinct"] == "Unspecified").sum(), (cleaned["police_precinct"] == "Unspecified").sum() ),
        ("distinct complaint types", raw["complaint_type"].nunique(),   
         cleaned["complaint_type_clean"].nunique()),
        ("closed_date_suspect", "-", cleaned["closed_date_suspect"].sum()),
        ("closed_before_created", "-", cleaned["closed_before_created"].sum()),
        ("coord_pair_incomplete", "-", cleaned["coord_pair_incomplete"].sum()),
    ]
    lines = ["| Check | Before (raw) | After (clean) |", "|---|---|---|"]
    for name, before, after in rows:
        lines.append(f"| {name} | {before} | {after} |")
    return "\n".join(lines)


def main():
    raw = load_raw(RAW_PATH)
    cleaned = pd.read_parquet(OUT_PATH)
    REPORT_PATH.write_text(build_report(raw, cleaned) + "\n")


if __name__ == "__main__":
    main()