import pandas as pd

from src.nyc311.clean import PLACEHOLDER_COLUMNS, placeholders_to_missing, add_complaint_type_clean , add_flags

"""
pattern for checking :
df =... the input we made 
out= function(df) what the function gives us 
assert  check the function whether the function give us the right answer or not 
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