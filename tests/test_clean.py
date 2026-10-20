import pandas as pd

from src.nyc311.clean import PLACEHOLDER_COLUMNS, placeholders_to_missing, add_complaint_type_clean

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

    out = placeholders_to_missing(df)

    assert out.isna().sum().sum() == 7
    assert df.isna().sum().sum() == 0


#test 2 add_complaint_type_clean
def test_complaint_type_spellings_merge():
    df = pd.DataFrame({"complaint_type": ["PLUMBING", "Plumbing", "  plumbing  "]})

    out = add_complaint_type_clean(df)

    #after trim and lower case there should be only 1 
    assert out["complaint_type_clean"].nunique() == 1

    assert list(out["complaint_type"]) == ["PLUMBING", "Plumbing", "  plumbing  "]
    # turns a column into a plain list, so we can compare it with == to a list we write by hand.