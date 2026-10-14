from pathlib import Path

import pandas as pd


def load_raw(path):
    path = Path(path)

    if not path.exists():
        raise FileNotFoundError(f"Raw file not found: {path}")

    return pd.read_csv(path, dtype=str, keep_default_na=False, na_values=[""] )

DATE_COLUMNS = ["created_date", "closed_date",
                "resolution_action_updated_date", "due_date"]
NUMBER_COLUMNS = ["latitude", "longitude",
                  "x_coordinate_state_plane", "y_coordinate_state_plane"]


def convert_types(df):
    """Dates become datetimes, coordinates become numbers. ZIP stays text."""
    df = df.copy()
    # NEW: .copy() makes a separate copy, so the DataFrame passed in is not changed.
    for col in DATE_COLUMNS:
        df[col] = pd.to_datetime(df[col], errors=___)
        # NEW: to_datetime turns date text into real datetimes. errors says what to do with a value that can't be converted.
    for col in NUMBER_COLUMNS:
        df[col] = pd.to_numeric(df[col], errors=___)
    return df