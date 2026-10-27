Everything I learned in the NYC 311 data quality project.

## Check what's in the data

| Syntax            | What it does                                |
| ----------------- | ------------------------------------------- |
| `df[col].isna()`  | True where a cell is empty                  |
| `.notna()`        | True where a cell is not empty              |
| `.sum()`          | counts the Trues (or adds numbers)          |
| `.sum().sum()`    | count per column, then add them up          |
| `.dropna()`       | remove empty values                         |
| `.nunique()`      | count different values                      |
| `.value_counts()` | count each value, biggest first             |
| `.head(n)`        | first n rows                                |
| `.describe()`     | count, mean, min, max                       |
| `.mean()`         | average (on True/False: the share of Trues) |
| `.dtype`          | the type of a column                        |
| `.iloc[0]`        | the first row of a column                   |
| `len(x)`          | how many items                              |
| `df.columns`      | the column names                            |

## Filter rows

| Syntax                      | What it does                                 |
| --------------------------- | -------------------------------------------- |
| `df.loc[condition, [cols]]` | keep the rows that match, show these columns |
| `series[condition]`         | keep only the True ones                      |
| `==`, `!=`, `<`, `>`        | compare, row by row                          |
| `~`                         | flip True and False (NOT)                    |
| `&`                         | AND between two True/False columns           |
| `.isin(set)`                | True if the value is in the set              |
| `.between(a, b)`            | True if the value is from a to b             |
| `.all()`                    | True only if every row is True               |

## Clean text

| Syntax                                  | What it does                              |
| --------------------------------------- | ----------------------------------------- |
| `.str.strip()`                          | remove spaces on the outside              |
| `.str.lower()`                          | make it lowercase                         |
| `.str.replace(r"\s+", " ", regex=True)` | turn extra spaces into one space          |
| `.str.fullmatch(r"\d{5}")`              | True if it is exactly 5 digits            |
| `.mask(condition)`                      | make it empty where the condition is True |

## Read, convert, save

| Syntax                                | What it does                                                         |
| ------------------------------------- | -------------------------------------------------------------------- |
| `pd.read_csv(path, dtype=str)`        | read everything as text (keeps `07302`)                              |
| `keep_default_na=False`               | words like `N/A` stay as words                                       |
| `na_values=[""]`                      | only a truly empty cell is empty                                     |
| `pd.to_datetime(x, errors="raise")`   | text to dates. `raise` stops on a bad value. `coerce` turns it empty |
| `pd.to_numeric(x, errors="raise")`    | text to numbers, same choice                                         |
| `df.copy()`                           | a separate copy, so the original is safe                             |
| `df.assign(col=values)`               | a copy with one column replaced                                      |
| `df.to_parquet(path, index=False)`    | save as Parquet, no row numbers                                      |
| `pd.read_parquet(path)`               | read a Parquet file                                                  |
| `pd.DataFrame({"col": [..]})`         | make a small table by hand                                           |
| `pd.testing.assert_frame_equal(a, b)` | fails unless two tables are the same                                 |

## Compare and group

| Syntax                          | What it does                                 |
| ------------------------------- | -------------------------------------------- |
| `pd.crosstab(a, b)`             | count table of two columns                   |
| `x.groupby(key).nunique()`      | group by key, count different values in each |
| `.sort_values(ascending=False)` | biggest first                                |
| `.round(2)`                     | 2 decimals                                   |
| `.index`                        | the row labels                               |
| `pd.Series(dict)`               | turn a dictionary into a column              |

## Python basics

| Syntax                           | What it does                                      |
| -------------------------------- | ------------------------------------------------- |
| `def name(x):`                   | make a function. `return` gives back the result   |
| `"""text"""` under `def`         | docstring: says what the function does            |
| `for col in list:`               | repeat for each item                              |
| `for col, word in d.items():`    | loop over a dictionary's keys and values together |
| `if hits:`                       | only run if it's not 0                            |
| `{"a", "b"}`                     | a set (no repeats, fast to check)                 |
| `{"a": 1}` and `d[key] = value`  | a dictionary (a lookup table)                     |
| `{k: [v] for k, v in d.items()}` | build a dictionary in one line                    |
| `list[5:]`                       | from position 5 to the end                        |
| `["x"] * 3`                      | repeat an item 3 times                            |
| `r"..."`                         | raw string, keeps the backslash                   |
| `f"{name}: {n}"`                 | text with values put in                           |
| `"\n".join(lines)`               | glue lines into one text                          |
| `raise FileNotFoundError(msg)`   | stop with an error                                |
| `try: ... except Error as e:`    | catch an error instead of crashing                |
| `if __name__ == "__main__":`     | only run when I run this file directly            |
| `from module import name`        | bring something in from another file              |
| `NAME = [...]` (capitals)        | a constant, kept at the top                       |

## Files and paths

| Syntax                                           | What it does                                    |
| ------------------------------------------------ | ----------------------------------------------- |
| `Path(p)`                                        | turn text into a file path                      |
| `path.exists()`                                  | True if the file is there                       |
| `path / "file.csv"`                              | join a folder and a file name                   |
| `path.parent`                                    | the folder the file is in                       |
| `path.parent.mkdir(parents=True, exist_ok=True)` | make the folder, no error if it's already there |
| `path.write_text("...")`                         | write text into a file                          |

## pandera (the schema)

| Syntax                                        | What it does                                      |
| --------------------------------------------- | ------------------------------------------------- |
| `pa.DataFrameSchema({...})`                   | all the rules for a table                         |
| `pa.Column(float, checks=..., nullable=True)` | rules for one column, empty is allowed            |
| `pa.Column(unique=True)`                      | no repeats                                        |
| `pa.Check.isin([...])`                        | value must be in the list                         |
| `pa.Check.in_range(a, b)`                     | value must be from a to b                         |
| `pa.Check.str_matches(r"^\d{5}$")`            | text must fit the pattern                         |
| `schema.validate(df)`                         | check the table. Quiet if it passes, error if not |
| `schema.validate(df, lazy=True)`              | collect every failure, not only the first         |
| `pa.errors.SchemaError` / `SchemaErrors`      | one failure / all failures                        |
| `e.failure_cases`                             | table of every broken rule                        |

A wrong type is 1 failure for the whole column. A bad value is 1 failure per value.

## pytest (the tests)

| Syntax                               | What it does                                        |
| ------------------------------------ | --------------------------------------------------- |
| `def test_something():`              | pytest runs every function that starts with `test_` |
| `assert x == 7`                      | this has to be true, or the test fails              |
| `with pytest.raises(Error):`         | passes only if the code inside raises that error    |
| `def test_x(tmp_path):`              | pytest gives the test a temporary folder            |
| `python -m pytest`                   | run all the tests                                   |
| `python -m pytest -s -k name`        | show prints, run only tests with that name          |
| `python -m pytest --collect-only -q` | list the tests it found                             |
| `pytest.ini` with `pythonpath = .`   | lets plain `pytest` find `src`                      |

A test has 3 steps: make a tiny input, run the function, assert the answer I already know.

## ruff

| Command              | What it does                            |
| -------------------- | --------------------------------------- |
| `ruff check .`       | find style problems                     |
| `ruff check --fix .` | fix the ones it can (like import order) |

## Git

| Command                       | What it does                                   |
| ----------------------------- | ---------------------------------------------- |
| `git status`                  | what changed                                   |
| `git add file` / `git add -A` | stage one file / everything                    |
| `git commit -m "msg"`         | save a snapshot on my computer                 |
| `git push`                    | upload to GitHub                               |
| `git log --oneline -3`        | last 3 commits                                 |
| `git ls-remote origin main`   | GitHub's real latest commit                    |
| `git rev-parse HEAD`          | my latest commit (should match the line above) |
| `git ls-files`                | every file git tracks                          |
| `git check-ignore -v path`    | which `.gitignore` rule covers a path          |
| `git rm --cached file`        | stop tracking a file, keep it on my computer   |
| `git mv old new`              | move or rename a tracked file                  |
| `git restore file`            | throw away my changes (can't undo)             |

Commit after one finished piece of work. Push at the end of the day.

## Terminal

| Command                           | What it does                              |
| --------------------------------- | ----------------------------------------- |
| `python -m src.nyc311.clean`      | run a module from the repo folder         |
| `python -c "code"`                | run one line of Python                    |
| `.venv\Scripts\activate`          | turn on the virtual environment (Windows) |
| `pip install name`                | install a library                         |
| `pip install -r requirements.txt` | install everything the project needs      |
| `ls folder`                       | list the files in a folder                |

## Ideas, not syntax

- **Missing vs wrong:** empty is missing, a bad value is wrong. "Unspecified" is missing in disguise, and `isna()` can't see it.
- **Structural vs optional emptiness:** "doesn't apply" vs "not entered".
- **LEAVE / FIX / FLAG / DROP:** LEAVE if the meaning is clear. FIX if I'm sure and the fix is safe. FLAG if I'm not sure. DROP only if nothing is lost.
- **I never change the raw file.** Cleaning saves a new file.
- **I never guess a missing value.**
- **Idempotent:** cleaning twice gives the same result, so re-running after a crash is safe.
- **Parquet vs CSV:** Parquet remembers types (dates stay dates). CSV turns everything into text.
- **ZIP is a label, not a number.** `07302` keeps its zero.
- **Format vs real:** a 5-digit ZIP looks right, but that doesn't prove it's real.
- **A schema that never fails proves nothing.** Mine fails on the raw data and passes on the clean data.
- **A good test uses the value that breaks when the code is wrong** (`N/A`, `07302`), and tests both the good case and the bad case.
- **Phase order:** Phase 2 finds the issues, 3 decides, 4 fixes, 5 checks, 6 tests.
