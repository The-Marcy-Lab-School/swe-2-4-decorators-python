# Closures and Decorators

Keep a value alive inside a function, and wrap a method so it refuses to run at the wrong moment.

**Practicing:** closures, decorators, `@` syntax, wrapping a function, reusable refusal, `*args` and `**kwargs`

- [AI Use on This Assignment](#ai-use-on-this-assignment)
- [Setup](#setup)
- [Before You Start](#before-you-start)
  - [Syntax to recognize](#syntax-to-recognize)
  - [Look these up yourself](#look-these-up-yourself)
- [From Scratch](#from-scratch)
  - [Question 1: `announce`](#question-1-announce)
  - [Question 2: `make_surcharge`](#question-2-make_surcharge)
  - [Question 3: `requires_paid`](#question-3-requires_paid)
  - [Question 4: `count_calls`](#question-4-count_calls)
- [Modify](#modify)
  - [Question 5: `Reservation`](#question-5-reservation)
  - [Question 6: `make_ride_numbers`](#question-6-make_ride_numbers)
  - [Question 7: `audit`](#question-7-audit)
- [Debug](#debug)
  - [Question 8: `timed`](#question-8-timed)
  - [Question 9: `require_rentable`](#question-9-require_rentable)
- [Submitting](#submitting)
- [Good luck!](#good-luck)

## AI Use on This Assignment

**Tutor mode, for this whole quarter.** The AI explains, questions, quizzes,
and critiques, and you write every line you submit. Quarter 1 is where you
build the habit of writing code by hand; asking an AI to write it for you
comes later, in Quarter 2, where the job becomes judging code rather than
producing it.

For this assignment that means asking it why a wrapper can still reach a
variable after the function around it has returned, or having it quiz you on
what `@announce` does to the name `announce` is attached to until you can say
it without looking. Ask it a hundred questions — that is the whole point. What
you do not do is ask it for the answer. Paste this at the start of a chat and
it will hold for the rest of the conversation:

> You are acting as a tutor. Your job is to explain what this coding question
> is asking, clarify confusing wording, and highlight the relevant concepts I
> need to know — but do not provide the full solution or code that directly
> answers the question. Instead, rephrase the problem in simpler terms,
> identify what is being tested, and suggest what steps or thought processes
> might help. Ask me guiding questions to make sure I am thinking critically.
> Do not write the final function, algorithm, or code implementation.

You own every line you submit, and you will be asked to explain it.

## Setup

Clone your repository in `development/mod-2` and then `cd` into it. Set up
your virtual environment and make a draft branch before you start.

```sh
git clone [your_repo]
cd [your_repo]
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
git checkout -b draft
```

Run `pytest` to test the entire assignment. To run one question, pass part of
its name: `pytest -k Bike`. Every push runs the tests on GitHub and reports
which ones passed in the **Actions** tab.

Push before it is finished. Your instructor grades this against the rubric,
not against the test count, so treat submitting as a checkpoint rather than a
finish line and come back to improve it.

When you are done working on this assignment, turn off your virtual
environment by running:

```sh
deactivate
```

## Before You Start

Skim this section before you read the lessons, so you know what to look for in
them. Classes, inheritance, properties and higher-order functions are all
assumed here. The new material is the **closure** — a function that remembers —
and the **decorator**, which is a closure wrapped around a function.

This assignment has three sections:

1. From Scratch
2. Modify
3. Debug

<details>
<summary><strong>Ideas to look for</strong> — the ideas behind the questions, if you want them up front</summary>

Each question depends on one or more of these ideas. Part of the work is
deciding which.

| Idea | Lesson |
| --- | --- |
| A function defined inside another function keeps access to the outer function's variables, and keeps it after the outer function has returned. That is a **closure**, and it is why a built function can remember the value it was built with. | 2.7 |
| Each call to the outer function makes a **new** closure with its own copy of those variables, so two functions built the same way never interfere. | 2.7 |
| `nonlocal` is needed to **reassign** an enclosing function's variable from inside the inner one. Reading it needs nothing; assigning to it without `nonlocal` makes a new local and raises `UnboundLocalError`. | 2.7 |
| A **decorator** is a function that takes a function and returns a replacement for it. `@announce` above a definition means `dock = announce(dock)`. | 2.7 |
| The decorator must `return wrapper`. Forgetting it binds the name to `None`, and calling it raises `'NoneType' object is not callable`. | 2.7 |
| The wrapper must `return func(...)`. Forgetting it makes every decorated function return `None`, with no error at all. | 2.7 |
| `*args` and `**kwargs` in the wrapper let one decorator work on functions with different signatures. | 2.7 |
| A decorator on a **method** receives the instance as the wrapper's first argument, so the wrapper can read `self.status` before deciding whether to let the call through. | 2.7 |
| A decorator is a **reusable refusal**. One decorator named for the rule it enforces beats the same `if` copied into every method, where forgetting it once lets an invalid change through silently. | 2.7 |
| Raise **before** calling the method, so a refused call leaves the object exactly as it was. The order of those two lines is the whole guarantee. | 2.7 |
| A **decorator factory** takes an argument and builds a decorator from it, so it is applied with parentheses: `@requires_status("paid")`. Missing them is legal Python that passes your method in as the argument. | 2.7 |

</details>

### Syntax to recognize

```python
def make_surcharge(amount):          # a closure
    def add(price):
        return price + amount        # reads the outer variable
    return add                       # returns the function, does not call it


def announce(func):                  # a decorator
    def wrapper(*args, **kwargs):
        print(f"calling {func.__name__}")
        return func(*args, **kwargs) # return the result
    return wrapper                   # return the wrapper


def requires_status(status):         # a decorator factory
    def decorator(method):
        def wrapper(self, *args, **kwargs):
            if self.status != status:
                raise ValueError(...)   # refuse before running
            return method(self, *args, **kwargs)
        return wrapper
    return decorator


@announce                            # dock = announce(dock)
def dock(serial): ...

@requires_status("paid")             # note the parentheses
def check_in(self): ...

def next_number():
    nonlocal count                   # needed to reassign, not to read
    count += 1
```

### Look these up yourself

- `nonlocal`. Two questions need it and no lesson walks through it. Read about
  it on
  [W3Schools](https://www.w3schools.com/python/ref_keyword_nonlocal.asp).
- Setting an attribute on a function, as in `wrapper.calls = 0`. A function is
  an object, so this works. One question depends on it.

## From Scratch

Write these functions and classes in `src/from_scratch.py`.

### Question 1: `announce`

Boro Bikes wants to see which operations ran, without editing every operation
to print something. A **decorator** adds behavior around a function while
leaving the function alone.

Write `announce`, a decorator that prints a line before the function runs and
then returns whatever the function returned, unchanged.

```python
@announce
def dock(serial):
    return f"{serial} docked"

dock("A1")
# prints: calling dock
# returns: "A1 docked"
```

The printed line is `calling ` followed by the function's name. Every function
knows its own name as `__name__`, so you do not take it as an argument.

A decorator is a function that takes a function and returns a **replacement**
for it. Yours needs three things:

- An inner function, usually called `wrapper`, that does the extra work and then
  calls the original.
- `wrapper` must **return** what the original returned. Forgetting this makes
  every decorated function return `None`.
- `announce` must **return `wrapper`** itself, not call it.

Take `*args` and `**kwargs` in `wrapper` and pass them straight through, so the
decorator works on a function with any arguments. A test uses two functions with
different signatures.

`@announce` above a definition is shorthand. It means `dock = announce(dock)` —
the name `dock` is rebound to whatever `announce` gave back.

### Question 2: `make_surcharge`

Boro Bikes charges a surcharge that differs by borough: 1.50 in Manhattan, 0.75
in Brooklyn. Rather than passing the amount everywhere, build one function per
borough, each already knowing its own amount.

Write `make_surcharge(amount)`, which returns a **function**. The function it
returns takes a price and adds the surcharge.

```python
manhattan = make_surcharge(1.50)
brooklyn = make_surcharge(0.75)

manhattan(10.00)                 # 11.5
brooklyn(10.00)                  # 10.75
manhattan(10.00)                 # 11.5 — still 1.50, it did not change
```

`make_surcharge` has returned long before `manhattan(10.00)` runs. Its local
variable `amount` should be gone, and yet the inner function still reads it.

That is a **closure**: an inner function keeps access to the variables of the
function that built it, for as long as the inner function exists. Python keeps
`amount` alive because something still refers to it.

Each call to `make_surcharge` makes a **new** closure with its own `amount`, so
`manhattan` and `brooklyn` never interfere. A test checks this.

Return the inner function, do not call it. This is the idea every decorator in
this assignment is built from — a decorator is a closure that happens to close
over a function.

### Question 3: `requires_paid`

A rental moves through statuses: `"reserved"`, then `"paid"`, then
`"collected"`. A bike may only be collected once it has been paid for. Right
now nothing stops `collect()` running on an unpaid rental, and the fellow who
wrote it is about to copy the same `if` into three more methods.

Write a decorator `requires_paid` that refuses the call unless the rental's
status is `"paid"`, and a class `Rental` that uses it.

| Write | Does |
| --- | --- |
| `requires_paid` | A decorator. If the rental's status is not `"paid"`, raise `ValueError`. Otherwise run the method |
| `Rental` | `__init__` takes a bike and starts at status `"reserved"`. `pay()` moves it to `"paid"`. `collect()` is decorated, and moves it to `"collected"` |

```python
rental = Rental(Bike("A1", "Grand Army", False))
rental.status                    # "reserved"

rental.collect()                 # raises ValueError — not paid yet
rental.status                    # "reserved" — the method body never ran

rental.pay()
rental.status                    # "paid"
rental.collect()
rental.status                    # "collected"
```

**`Bike` is already written for you.**

The decorator wraps a **method**, so `wrapper`'s first argument is the rental
itself. Call it `self`, read `self.status`, and pass everything through to the
method with `*args` and `**kwargs`.

Raise `ValueError` **before** calling the method, so a refused call leaves the
object exactly as it was. A test checks that the status did not move.

This is the shape your project needs. One decorator per status, named for the
rule it enforces, is the difference between a rule written once and the same
`if` copied into every method that needs it — where forgetting it in one place
lets an invalid change through silently.

### Question 4: `count_calls`

Operations keep running more often than anyone expects, and nobody can say how
often. Write `count_calls`, a decorator that counts how many times the function
it wraps has been called and makes the number readable.

```python
@count_calls
def dock(serial):
    return f"{serial} docked"

dock.calls                       # 0 — before anything runs
dock("A1")
dock("A2")
dock.calls                       # 2
dock("A3")                       # still returns "A3 docked"
dock.calls                       # 3
```

The count lives in the closure, and `wrapper.calls` is how the outside reads it.
Two decorated functions count separately.

Two things to work out:

- **The count has to survive between calls.** A plain `count = count + 1` inside
  `wrapper` raises `UnboundLocalError`, because assigning to a name makes it
  local to `wrapper`. Look up the `nonlocal` keyword, or keep the count
  somewhere that does not need reassigning.
- **`wrapper.calls` has to be readable from outside.** A function is an object,
  so you can set an attribute on it: `wrapper.calls = 0` before you return it,
  and update it as you go.

This is a closure and a decorator at the same time, which is the point — a
decorator *is* a closure, and the thing it closes over is usually the function
it wraps. Here it closes over a number as well.

## Modify

Change the code already in `src/modify.py`.

### Question 5: `Reservation`

`Reservation` has three methods, and each one opens with the same two lines: a
check on the status and a `raise`. The check is correct in all three. The
problem is that it is written three times, so the fourth method someone adds
will be the one that forgets it.

Replace the repeated check with decorators. `requires_status` is waiting in
`src/modify.py` for you to finish.

When you are done:

- `requires_status(status)` returns a decorator that refuses the call unless
  `self.status` matches the status it was given.
- `pay`, `check_in` and `refund` each carry one, and **none of them contains an
  `if` or a `raise` any more**.
- Every answer is what it is now.

```python
booking = Reservation("Ana")
booking.status                   # "reserved"

booking.check_in()               # raises ValueError — must be paid first
booking.status                   # "reserved" — unchanged

booking.pay()
booking.status                   # "paid"
booking.check_in()
booking.status                   # "checked_in"

Reservation("Ben").refund()      # raises ValueError — only a paid one refunds
```

`requires_status` takes an argument, so it is one layer deeper than the
decorators you have written: a function that takes a status and returns a
decorator, which then takes a method and returns a wrapper. It is applied as
`@requires_status("paid")` — with parentheses, because calling it is what builds
the decorator.

That extra call is the whole difference, and missing the parentheses is the
classic mistake: `@requires_status` with no call hands your method in as the
*status*, and nothing raises until much later.

Keep the error messages useful. A refusal should say which status was needed.

### Question 6: `make_ride_numbers`

`next_ride_number` issues ride numbers from a module-level counter. Two stations
both call it, so their numbers interleave, and a test that runs after another
test sees a counter that is already part-used.

Rewrite it as `make_ride_numbers(start)`, which returns a function. Each call to
`make_ride_numbers` gets its own counter.

```python
grand_army = make_ride_numbers(1)
borough_hall = make_ride_numbers(500)

grand_army()                     # 1
grand_army()                     # 2
borough_hall()                   # 500 — its own counter, untouched by the above
grand_army()                     # 3
```

**Delete `next_ride_number` and the module-level `_counter` when you are done.**
A test checks both are gone.

The counter now lives in the closure, which means it is reachable only through
the function that owns it. Nothing else in the program can reach in and change
it, which is the same argument as a non-public attribute behind a property, made
with a function instead of a class.

You will need `nonlocal` to reassign a name from the enclosing function. Without
it, `count = count + 1` makes `count` local to the inner function and raises
`UnboundLocalError` on the read that comes first.

### Question 7: `audit`

Three operations each print the same pair of lines around their real work: one
before, one after. The printing is identical in all three and has nothing to do
with what any of them actually does.

Finish the `audit` decorator in `src/modify.py` and put it on all three.

When you are done each function's body is only its own work, and every answer
is unchanged.

```python
dock("A1")
# prints: start dock
# prints: done dock
# returns: "A1 docked"

release("A1")                    # returns "A1 released"
repair("A1", 2)                  # returns "A1 repaired in 2 days"
```

The printed lines use the function's own name, so `audit` works on a function it
has never seen. The lines are `start ` then the name, and `done ` then the name.

`repair` takes two arguments and the others take one, so `wrapper` needs `*args`
and `**kwargs` rather than a fixed signature.

The "after" line has to print **after** the function runs but the result still
has to come back, so hold the result in a variable, print, then return it.

## Debug

Fix the code in `src/debug.py`.

### Question 8: `timed`

`@timed` prints its line, the function runs, and the caller gets `None`:

```python
rental_cost(3.00, 2)
# prints: timed rental_cost
# returns: None     <- should be 6.00
```

Nothing raises. The function ran, its line printed, and the answer vanished
between the function and the caller. Fix `timed` in `src/debug.py`.

```python
rental_cost(3.00, 2)             # 6.0
rental_cost(4.50, 4)             # 18.0
```

A decorator replaces the function with `wrapper`, so from the caller's side
`wrapper`'s return value **is** the function's return value. A `wrapper` that
calls `func(...)` and does not return the result returns `None`, because every
Python function with no `return` does.

This bug is quiet, which is what makes it worth meeting here. Nothing raises at
the point of the mistake. It surfaces later as a `None` in arithmetic or an
empty report, somewhere that has nothing to do with the decorator.

One word fixes it.

### Question 9: `require_rentable`

`@require_rentable` guards `start()` so a trip cannot begin on a bike needing
repair. The guard is written correctly. Calling the method does not work at all:

```python
Trip("A1", needs_repair=False).start()
# TypeError: 'NoneType' object is not callable
```

Read the message. Something that is `None` is being called. The thing being
called is `start`. So what is `start` now?

Fix `require_rentable` in `src/debug.py`.

```python
Trip("A1", needs_repair=False).start()   # "A1 started"
Trip("B7", needs_repair=True).start()    # raises ValueError
```

`@require_rentable` means `start = require_rentable(start)`. Whatever
`require_rentable` gives back becomes `start`. A decorator that builds a
`wrapper` and then ends without returning it gives back `None`, so `start`
becomes `None`, and calling it fails before any of the guard's logic runs.

This is the second of the two mistakes every decorator author makes. The first
one loses the function's **result**; this one loses the **function**. The error
messages are different enough to tell apart:

- `'NoneType' object is not callable` — the decorator did not return the wrapper.
- No error, but the answer is `None` — the wrapper did not return the result.

Worth knowing both, because the project asks you to write one of these.

## Submitting

```sh
git add -A
git commit -m "your message"
git push
```

Pushing runs the tests on GitHub. Check the **Actions** tab to see which
passed, then open a pull request to your instructor for feedback.

## Good luck!

Every system you build from here is made of classes, so this is the
assignment the rest of the module stands on. You got this!
