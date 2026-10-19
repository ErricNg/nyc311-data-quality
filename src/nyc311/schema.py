import pandera.pandas as pa
#pandera-> rules clean table must follow 

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