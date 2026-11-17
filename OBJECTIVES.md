# Objective map — assignment 2.4

**Instructor facing.** This file is for auditing the assignment against the
scope and sequence. It is not written for fellows.

Covers **2.7 Closures and Decorators**.

| | Name |
| --- | --- |
| Code | `swe-2-4-decorators-python` |
| Short response | `swe-sr-2-4-decorators-python` |

## Why 2.7 is alone

The 2.6 split made the old three-assignment plan impossible: 2.7 was taught the
same day the old assignment 3 was due. The four-assignment split puts 2.5 and
2.6 together in `swe-2-3` and leaves 2.7 here.

2.7 has only four objectives plus a testing row, and two of them are code-able.
That sounds thin for nine questions and is not, because the question space is
wide: a decorator can be written, applied by hand, stacked, given an argument,
or broken in two distinct ways. Several questions cover the same objective from
a different angle, which is the same thing 2.2 did with its setter.

## Objective map

All five objectives are covered.

| Objective | Covered by |
| --- | --- |
| 2.7 Apply · R7 — a decorator printing before and returning the result unchanged | Q1 `announce`, Q7 `audit`, Q8 `timed` |
| 2.7 Analyze · R7 — which variable the wrapper closes over, and why | Q2 `make_surcharge`, Q6 `make_ride_numbers`, SR 1 |
| 2.7 Apply · R6, R7 — a decorator named for a status, refusing from any other | Q3 `requires_paid`, Q5 `Reservation`, Q9 `require_rentable` |
| 2.7 Understand — the two steps a decorator factory performs | Q5, SR 2 |
| 2.7 Testing · R7, R9 — a wrong-status call left the object unchanged | SR 3 |

40 tests. All 40 pass against the reference solutions, 33 fail against the
stubs, and the 7 that pass are regression guards on the Modify and Debug
questions.

## The two Debug questions are a pair

Q8 and Q9 are the two mistakes every decorator author makes, and their symptoms
are opposite:

- **Q8** — the wrapper does not return the result. No error at all; the answer
  is silently `None` and surfaces later in arithmetic or an empty report.
- **Q9** — the decorator does not return the wrapper. Immediate
  `'NoneType' object is not callable`, before any of the guard's logic runs.

Both question texts name both symptoms, so a fellow can tell them apart by the
message rather than by guessing. The project asks them to write one of these.

## Open question raised in the pull request

**`functools.wraps`.** Nothing in 2.7's objectives mentions it and the Overview
does not either. Without it a decorated function reports the wrapper's name, so
`dock.__name__` is `"wrapper"`. Added to the ideas table as reading only;
whether it should be required is Ben's call.
