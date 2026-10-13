Syntax and ideas from the exploration phase of the NYC 311 data quality project.

## Check what's in the data

| Syntax            | Does what                                   |
| ----------------- | ------------------------------------------- |
| `df[col].isna()`  | True where a cell is empty                  |
| `.sum()`          | counts the Trues (also adds numbers)        |
| `.notna()`        | True where a cell is NOT empty              |
| `.dropna()`       | removes empty values                        |
| `.nunique()`      | counts distinct values                      |
| `.value_counts()` | counts each value, biggest first            |
| `.head(n)`        | first n rows                                |
| `.describe()`     | count, mean, min, quartiles, max            |
| `.mean()`         | average (on True/False: the share of Trues) |
| `len(x)`          | number of items                             |
| `df.columns`      | list of column names                        |

## Filter rows

| Syntax                      | Does what                                 |
| --------------------------- | ----------------------------------------- |
| `df.loc[condition, [cols]]` | keep rows that match, show chosen columns |
| `series[condition]`         | keep only entries where True              |
| `==`, `!=`, `>`             | compare                                   |
| `~`                         | flip True/False (NOT)                     |
| `&`                         | AND between two True/False columns        |
| `.isin(set)`                | True if the value is in the set           |
| `.between(a, b)`            | True if the value is from a to b          |
| `.all()`                    | True only if every row is True            |

## Clean text

| Syntax                                  | Does what                                   |
| --------------------------------------- | ------------------------------------------- |
| `.str.strip()`                          | remove outer spaces                         |
| `.str.lower()`                          | lowercase                                   |
| `.str.replace(r"\s+", " ", regex=True)` | collapse repeated spaces                    |
| `.str.fullmatch(r"\d{5}")`              | True if the whole value is exactly 5 digits |
| `pd.to_numeric(x, errors="coerce")`     | text to number, bad values become NaN       |

## Compare and group

| Syntax                          | Does what                                        |
| ------------------------------- | ------------------------------------------------ |
| `pd.crosstab(a, b)`             | count table of two columns                       |
| `x.groupby(key).nunique()`      | one group per key, count distinct values in each |
| `.sort_values(ascending=False)` | sort biggest first                               |
| `.round(2)`                     | 2 decimals                                       |
| `.index`                        | the row labels                                   |
| `pd.Series(dict)`               | dictionary to a labeled column                   |

## Python basics

| Syntax                    | Does what                        |
| ------------------------- | -------------------------------- |
| `for col in list:`        | repeat for each item             |
| `if hits:`                | run only if not 0                |
| `{"a", "b"}`              | set (no duplicates, fast lookup) |
| `{}` and `d[key] = value` | dictionary (lookup table)        |
| `list[5:]`                | slice, position 5 to the end     |
| `r"..."`                  | raw string, keeps the backslash  |

## Ideas, not syntax

- **Missing vs wrong:** empty is missing, a bad value is wrong. Placeholders are missing in disguise.
- **Structural vs optional emptiness:** "does not apply" vs "not entered".
- **FIX / FLAG / DROP / LEAVE:** the four ways to handle an issue.
- **Format vs real:** a 5-digit ZIP is well-formed, not proven real.
- **Phase 2 finds and documents issues. It changes nothing.** Deciding is Phase 3, fixing is Phase 4.
