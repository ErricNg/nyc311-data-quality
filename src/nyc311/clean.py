from pathlib import Path

import pandas as pd


def load_raw(path):
    """Read the raw 311 CSV. Every column stays text."""
    path = Path(path)
    # NEW: Path wraps a file path so we can ask it questions, like .exists().
    if not path.exists():
        raise FileNotFoundError(f"Raw file not found: {path}")
        # NEW: raise stops the function with an error. FileNotFoundError is Python's standard "no such file" error. f"...{path}" puts the value inside the text.
    return pd.read_csv(path, dtype=str, keep_default_na=False, na_values=[""] )
    # NEW: dtype=str reads every column as text, so ZIP codes keep their leading zeros.
    