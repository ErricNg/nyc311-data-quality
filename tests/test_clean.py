import pandas as pd

from src.nyc311.clean import PLACEHOLDER_COLUMNS, placeholders_to_missing


def test_placeholder_words_become_empty():
    #a small table first row is all placeholder words -> run out (placeholder to missing) on it -> check -> 7 placeholder become empty
    df = pd.DataFrame({col: [word, "real value"] for col, word in PLACEHOLDER_COLUMNS.items()})

    out = placeholders_to_missing(df)
    
    assert out.isna().sum().sum() == 7
    assert df.isna().sum().sum() == 0