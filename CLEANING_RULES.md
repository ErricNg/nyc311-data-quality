# Cleaning rules

How to choose between LEAVE, FIX, FLAG and DROP.

## The four actions

- **LEAVE:** keep the value as it is.
- **FIX:** change the value.
- **FLAG:** keep the value and add a marker column.
- **DROP:** remove the value, row or column.

## Which one to use

|                                                                | Use       | Example                                                               |
| -------------------------------------------------------------- | --------- | --------------------------------------------------------------------- |
| Is the value correct and its meaning clear?                    | **LEAVE** | Empty `closed_date` on a request that is still open                   |
| Am I sure what it means, and is the fix safe?                  | **FIX**   | "Unspecified" borough becomes empty. `PLUMBING` becomes `plumbing`    |
| Am I unsure if it is wrong, or can't tell which part is wrong? | **FLAG**  | 964 rows with a close date but not Closed. Closed-before-created rows |
| Is it an exact copy, or useless for every analysis?            | **DROP**  | `park_borough` (identical to `borough`)                               |

## Quick tests

- **FIX or FLAG?** Ask "could my fix be wrong?" If yes, FLAG. Turning "Unspecified" into empty cannot be wrong, because the word means "unknown". Changing a close date could be wrong, because we don't know which date is the error.
- **FLAG or LEAVE?** Ask "would another person be misled if nobody told them?" If yes, FLAG. If the meaning is obvious, LEAVE.
- **DROP:** only when nothing is lost. A column with valid values, even sparse ones, is not a DROP. An exact copy is the only safe drop.

## Always

- Never edit the raw file. Cleaning writes a new file to `data/processed/`.
- Never guess a missing value. No filling in, no estimating.
- Placeholder text that means "unknown" becomes empty, so `isna()` can find it.
- Keep the original value next to every flag.
- Log every change with a count, like "turned 80 borough values into empty".
- Cleaning must give the same result when run twice (idempotent).
- Write the **why** next to every decision in `DECISIONS.md`.

## How to explain a decision

> I found [problem, with a number]. I couldn't tell [A] from [B], so I [decision]. That costs [X], but keeps [Y].

Three habits:

1. Say the number. "964 rows" beats "some rows".
2. Say what you gave up.
3. Say "I couldn't tell" when it is true. Flagging beats guessing.
