from pathlib import Path

import pandas as pd

"the dataset"
RAW_PATH = Path("data/raw/311_2026-09-01_to_2026-09-07.csv")

"the clean result"
OUT_PATH = Path("data/processed/311_clean.parquet")


#Reading the file

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

#Converting dates become datetimes, coordinates become numbers. ZIP stays tex
def convert_types(df):

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
        #                make cell empty whenever condition is true 
        df[col] = df[col].mask(df[col] == word)
        
    return df

"add complaint type"
def add_complaint_type_clean(df):
    df = df.copy()
    df["complaint_type_clean"]=(
        df["complaint_type"]
        .str.strip().str.lower().str.replace(r"\s+", " ", regex=True))

    return df 

"add flag "
def add_flags(df):
    df = df.copy()

    df["closed_date_suspect"] = df["closed_date"].notna() & (df["status"] != "Closed")
    df["closed_before_created"] = df["closed_date"] < df["created_date"] 
    df["coord_pair_incomplete"] = ( df["x_coordinate_state_plane"].isna() != df["y_coordinate_state_plane"].isna() )

    return df

#Cleaning 

def clean(df):
    """Run every cleaning step, in order."""
    df = convert_types(df)
    df = placeholders_to_missing(df)
    df = add_complaint_type_clean(df)

    return add_flags(df)


def main():
    raw = load_raw(RAW_PATH)
    df = clean(raw)
    
    print(f"rows: {len(raw)} -> {len(df)}")

    #creates the data/processed/ folder -> mkdir check does nothing if it already exists, so saving the file never fails.
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    #save the clean table to parquet file -> format rmbr format of column types,...
    df.to_parquet(OUT_PATH, index=False)
    #                       stop saving pandas extra row number column

    print(f"saved {OUT_PATH}")


if __name__ == "__main__":
    main()
