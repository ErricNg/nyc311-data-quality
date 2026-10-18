from pathlib import Path

import pandas as pd


def load_raw(path):
    "Read the raw 311 CSV. Every column stays text"

    path = Path(path)

    if not path.exists():
        raise FileNotFoundError(f"Raw file not found: {path}")

    return pd.read_csv(path, dtype=str, keep_default_na=False, na_values=[""] )



DATE_COLUMNS = ["created_date", "closed_date",
                "resolution_action_updated_date", "due_date"]
NUMBER_COLUMNS = ["latitude", "longitude",
                  "x_coordinate_state_plane", "y_coordinate_state_plane"]


def convert_types(df):
    "Dates become datetimes, coordinates become numbers. ZIP stays text"

    df = df.copy()

    for col in DATE_COLUMNS:
        df[col] = pd.to_datetime(df[col], errors="coerce")

    for col in NUMBER_COLUMNS:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    return df


PLACEHOLDER_COLUMNS = {
    "borough": "Unspecified",
    "park_borough": "Unspecified",
    "park_facility_name": "Unspecified",
    "police_precinct": "Unspecified",
    "open_data_channel_type": "UNKNOWN",
    "location_type": "Unknown",
    "descriptor_2": "Unknown",
}


def placeholders_to_missing(df):
    "Turn (unknown) placeholder words into real empty values"
    df = df.copy()
    for col, word in PLACEHOLDER_COLUMNS.items():
        df[col] = df[col].mask(df[col] == word)
        
    return df

"add complaint type"
def add_complaint_type_clean(df):
    df = df.copy()
    df["complaint_type_clean"]=(df["complaint_type"].str.strip().str.lower().str.replace(r"\s+", " ", regex=True))
    return df 

