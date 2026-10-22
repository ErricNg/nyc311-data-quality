import pandas as pd

import pandera.pandas as pa

from src.nyc311.schema import schema

import pytest 
from src.nyc311.clean import PLACEHOLDER_COLUMNS, placeholders_to_missing, add_complaint_type_clean , add_flags , load_raw , DATE_COLUMNS, NUMBER_COLUMNS, convert_types, clean
"""
pattern for checking :
df =... the input we made 
out= function(df) what the function gives us 
assert  check the function whether the function give us the right answer or not 
"""


"""
Test the clean.py
"""


#test 1 placeholder missing 
def test_placeholder_words_become_empty():
    #a small table first row is all placeholder words -> run out (placeholder to missing) on it -> check -> 7 placeholder become empty
    df = pd.DataFrame({col: [word, "real value"] for col, word in PLACEHOLDER_COLUMNS.items()})

    #clean table
    out = placeholders_to_missing(df)

    #7 placeholder words turn into empty cell 
    assert out.isna().sum().sum() == 7

    #Org table placeholder should be all in words no empty
    assert df.isna().sum().sum() == 0


#test 2 add_complaint_type_clean
def test_complaint_type_spellings_merge():
    df = pd.DataFrame({"complaint_type": ["PLUMBING", "Plumbing", "  plumbing  "]})

    out = add_complaint_type_clean(df)

    #after trim and lower case there should be only 1 is "plumbing"
    assert out["complaint_type_clean"].nunique() == 1

    assert list(out["complaint_type"]) == ["PLUMBING", "Plumbing", "  plumbing  "]
    # turns a column into a plain list, so we can compare it with == to a list we write by hand.


#test 3 add flags 
def test_flags_mark_the_right_rows():
    # a table show 3 cases 
    """
    Row	   created	closed	  status	x	    y	   closed_date_suspect	closed_before_created	coord_pair_incomplete
    0	   10:00	09:00	  Closed	1.0	    1.0	       False  	           True	                   False
    1	   10:00	empty	  Open	    empty	2.0	       False  	           False	               True
    2	   10:00	next day  Open	    3.0	    empty      True	               False	               True
    """
    df = pd.DataFrame({
        "created_date": pd.to_datetime(["2026-09-01 10:00"] * 3),
        "closed_date": pd.to_datetime(["2026-09-01 09:00", None, "2026-09-02 10:00"]),
        "status": ["Closed", "Open", "Open"],
        "x_coordinate_state_plane": [1.0, None, 3.0],
        "y_coordinate_state_plane": [1.0, 2.0, None],
    })


    out = add_flags(df)
    #does it have no closed date and status is not closed
    assert out["closed_date_suspect"].sum() == 1

    #closed < created
    assert out["closed_before_created"].sum() == 1

    #does 1 of them empty
    assert out["coord_pair_incomplete"].sum() == 2

    #test 4 load raw

def test_load_raw_missing_file_raises():
        #check if load raw raise the right error (when i give a file that doesnt exist)
    with pytest.raises(FileNotFoundError):

        load_raw("data/raw/does_not_exist.csv")

def test_convert_types_keeps_zip_as_text():
    #A table conver everything to text like the raw file
    df = pd.DataFrame({col: ["2026-09-01 10:00:00"] for col in DATE_COLUMNS})
                                                     
    for col in NUMBER_COLUMNS:
        df[col] = ["40.7"]
    df["incident_zip"] = ["07302"]
    """
    Column	                            Value (all text)
    created_date	                    2026-09-01 10:00:00
    closed_date	                        2026-09-01 10:00:00
    resolution_action_updated_date	    2026-09-01 10:00:00
    due_date	                        2026-09-01 10:00:00
    latitude	                        40.7
    longitude	                        40.7
    x_coordinate_state_plane	        40.7
    y_coordinate_state_plane	        40.7
    incident_zip	                    07302
    """

    out = convert_types(df)

    #must be a real number
    assert out["latitude"].dtype == "float64"

    #check the first row still have to be text "07302"
    assert out["incident_zip"].iloc[0] == "07302"

    #chek if it converted to real datetime or not 
    assert str(out["created_date"].dtype).startswith("datetime")



#test 6  clean -> never drop rows
def make_raw():
    """Two fake raw rows with every column the pipeline touches, all text."""
    df = pd.DataFrame({col: ["2026-09-01 10:00:00", "2026-09-01 11:00:00"] for col in DATE_COLUMNS})

    for col in NUMBER_COLUMNS:
        df[col] = ["40.7", "40.8"]

    for col, word in PLACEHOLDER_COLUMNS.items():
        df[col] = [word, "real"]

    df["complaint_type"] = ["Plumbing", "PLUMBING"]
    df["status"] = ["Closed", "Open"]
    df["incident_zip"] = ["07302", "10001"]

    return df


def test_clean_keeps_every_row():
    raw = make_raw()
    out = clean(raw)

    assert len(out) == 2

    # new collumn has :complaint_type_clean,closed_date_suspect, closed_before_created, coord_pair_incomplete
    # added :add_complaint_type_clean, add_flags, add_flags, add_flags -> add 4
    assert len(out.columns) == len(raw.columns) + 4


#test 7 running clean twice gives the same result

def test_clean_is_idempotent():
    #clean fake raw table
    once = clean(make_raw())

    #clean again
    twice = clean(once)

    #compare if 2 of them are identical 
    pd.testing.assert_frame_equal(once, twice)


"""
test the schema
"""

def make_good():
    """A tiny table that follows every schema rule."""
    return pd.DataFrame({
        "unique_key": ["1", "2"],
        "incident_zip": ["10001", None],
        "borough": ["QUEENS", None],
        "latitude": [40.7, 40.8],
        "longitude": [-73.9, -73.8],
        "closed_date_suspect": [False, True],
    })


def test_schema_catches_bad_zip():
    good = make_good()
    schema.validate(good)
    # NEW: if validate finds no problem, it returns quietly. A problem raises an error, which would fail this test.
    bad = good.copy()
    bad["incident_zip"] = ["1000", None]
    with pytest.raises(pa.errors.SchemaError):
        schema.validate(bad)