from from_scratch import Bike, Rental, announce, count_calls, make_surcharge, requires_paid


TEST_SUITE_NAME = "From Scratch Tests"


def test_announce_prints_before_the_function_runs(capsys):
    """announce - it prints 'calling' and the function's own name"""
    @announce
    def dock(serial):
        return f"{serial} docked"

    dock("A1")

    assert "calling dock" in capsys.readouterr().out, \
        "Print 'calling ' followed by func.__name__."


def test_announce_returns_the_original_result():
    """announce - the wrapper hands back what the function returned"""
    @announce
    def dock(serial):
        return f"{serial} docked"

    assert dock("A1") == "A1 docked", \
        "wrapper must return func(...), not just call it."


def test_announce_works_on_any_signature():
    """announce - *args and **kwargs pass straight through"""
    @announce
    def rate(base, hours, discount=0):
        return base * hours - discount

    assert rate(3, 2) == 6
    assert rate(3, 2, discount=1) == 5
    assert rate(base=4, hours=2) == 8


def test_announce_returns_a_function():
    """announce - it returns the wrapper rather than calling it"""
    def plain():
        return "ok"

    decorated = announce(plain)

    assert callable(decorated), "Return wrapper itself, with no parentheses."
    assert decorated() == "ok"


def test_make_surcharge_returns_a_function():
    """make_surcharge - it hands back a function, it does not add anything itself"""
    manhattan = make_surcharge(1.50)

    assert callable(manhattan), "Return the inner function, with no parentheses."


def test_the_returned_function_adds_its_own_amount():
    """make_surcharge - the closure remembers the amount it was built with"""
    assert make_surcharge(1.50)(10.00) == 11.50
    assert make_surcharge(0.75)(10.00) == 10.75


def test_two_closures_do_not_share_an_amount():
    """make_surcharge - each call builds a new closure with its own amount"""
    manhattan = make_surcharge(1.50)
    brooklyn = make_surcharge(0.75)

    assert manhattan(10.00) == 11.50
    assert brooklyn(10.00) == 10.75
    assert manhattan(10.00) == 11.50, "Building the second one must not change the first."


def test_the_amount_survives_after_make_surcharge_returned():
    """make_surcharge - calling it later still works"""
    add = make_surcharge(2.00)
    prices = [1.00, 5.00, 10.00]

    assert [add(price) for price in prices] == [3.00, 7.00, 12.00]


import pytest



def rental():
    return Rental(Bike("A1", "Grand Army", False))


def test_a_rental_starts_reserved():
    """Rental - __init__ holds the bike and the first status"""
    booked = rental()

    assert booked.status == "reserved"
    assert booked.bike.serial == "A1"


def test_paying_moves_the_status():
    """Rental - pay is not guarded, so it runs from reserved"""
    booked = rental()
    booked.pay()

    assert booked.status == "paid"


def test_collecting_an_unpaid_rental_is_refused():
    """requires_paid - collect raises ValueError from the wrong status"""
    with pytest.raises(ValueError):
        rental().collect()


def test_a_refused_collect_changes_nothing():
    """requires_paid - the guard raises before the method body runs"""
    booked = rental()

    with pytest.raises(ValueError):
        booked.collect()

    assert booked.status == "reserved", \
        "Raise before calling the method, so the body never moves the status."


def test_collecting_a_paid_rental_works():
    """requires_paid - the method runs and its result comes back"""
    booked = rental()
    booked.pay()

    assert booked.collect() == "A1 collected"
    assert booked.status == "collected"


def test_the_decorator_can_guard_any_method():
    """requires_paid - it reads self.status, so it is not tied to collect"""
    class Refund:
        def __init__(self):
            self.status = "reserved"

        @requires_paid
        def refund(self):
            return "refunded"

    with pytest.raises(ValueError):
        Refund().refund()


def test_a_decorated_function_starts_at_zero():
    """count_calls - the count is readable before anything has run"""
    @count_calls
    def dock(serial):
        return f"{serial} docked"

    assert dock.calls == 0


def test_the_count_rises_with_each_call():
    """count_calls - the number survives between calls"""
    @count_calls
    def dock(serial):
        return f"{serial} docked"

    dock("A1")
    dock("A2")

    assert dock.calls == 2

    dock("A3")
    assert dock.calls == 3


def test_the_result_still_comes_back():
    """count_calls - counting must not swallow the return value"""
    @count_calls
    def dock(serial):
        return f"{serial} docked"

    assert dock("A1") == "A1 docked"


def test_two_decorated_functions_count_separately():
    """count_calls - each decorated function gets its own closure"""
    @count_calls
    def dock(serial):
        return serial

    @count_calls
    def release(serial):
        return serial

    dock("A1")
    dock("A2")
    release("A1")

    assert dock.calls == 2
    assert release.calls == 1
