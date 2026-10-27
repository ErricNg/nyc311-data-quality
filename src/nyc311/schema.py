#pandera-> rules clean table must follow 
import pandas as pd
import pandera.pandas as pa

from src.nyc311.clean import OUT_PATH, RAW_PATH, load_raw

BOROUGHS = ["BROOKLYN", "QUEENS", "MANHATTAN", "BRONX", "STATEN ISLAND"]

schema = pa.DataFrameSchema(
    # DataFrameSchema is the full list of rules for the table
    {
        "unique_key": pa.Column(unique=True),
        #                       fails if any value repeats

        "incident_zip": pa.Column(checks=pa.Check.str_matches(r"^\d{5}$"), nullable=True),
        # tests text against a pattern (^ start, $ end, so exactly 5 digits). and allows empty cells

        "borough": pa.Column(checks=pa.Check.isin(BOROUGHS), nullable=True),

        "latitude": pa.Column(float, checks=pa.Check.in_range(40.4, 41.0), nullable=True),
        #                                                    in this range
        "longitude": pa.Column(float, checks=pa.Check.in_range(-74.3, -73.6), nullable=True),
        
        "closed_date_suspect": pa.Column(bool),
    }
)


def main():
    #   runs the schema check on the raw table and then on the cleaned table, and prints whether each one passes or fails (with a count of failures by column and rule).               
    for name, df in [("raw", load_raw(RAW_PATH)),          ("clean", pd.read_parquet(OUT_PATH))]:
        #           read raw data and return as a table        read the clean file that main() saved 

        try:
            schema.validate(df, lazy=True)
            #                    collects every failure instead of stopping at the first one.

            print(f"{name}: passes")

        except pa.errors.SchemaErrors as e:

            print(f"{name}: FAILS")
            print(e.failure_cases[["column", "check"]].value_counts())
            #     a table of every broken rule, with the column and the check that failed.
"""
the result shows that :
borough isin: 80	->the 80 “Unspecified” rows. This is 80 failing rows.
latitude and longitude dtype: 1 ->	should be number not text
latitude and longitude in_range: 1 each	-> out of range 

"""

if __name__ == "__main__":
    main()