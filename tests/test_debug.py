from debug import Trip, rental_cost, require_rentable, timed


TEST_SUITE_NAME = "Debug Tests"


def test_the_result_reaches_the_caller():
    """timed - the wrapper returns what the function returned"""
    assert rental_cost(3.00, 2) == 6.00
    assert rental_cost(4.50, 4) == 18.00


def test_the_line_still_prints(capsys):
    """timed - the printing was never the bug"""
    rental_cost(3.00, 2)

    assert "timed rental_cost" in capsys.readouterr().out


def test_timed_passes_arguments_through():
    """timed - keyword arguments still arrive"""
    assert rental_cost(rate=3.00, hours=3) == 9.00


def test_timed_works_on_another_function():
    """timed - the fix is in the decorator, so anything it wraps returns properly"""
    @timed
    def late_fee(per_hour, hours):
        return per_hour * hours

    assert late_fee(1.50, 2) == 3.00


import pytest



def test_a_good_bike_can_start_a_trip():
    """require_rentable - start is a function again, and it runs"""
    assert Trip("A1", needs_repair=False).start() == "A1 started"


def test_a_broken_bike_is_refused():
    """require_rentable - the guard was correct and still is"""
    with pytest.raises(ValueError):
        Trip("B7", needs_repair=True).start()


def test_the_decorator_hands_back_a_callable():
    """require_rentable - it returns the wrapper rather than None"""
    def plain(self):
        return "ran"

    assert callable(require_rentable(plain)), \
        "require_rentable must return wrapper. Without that, the method becomes None."


def test_the_guard_runs_before_the_method():
    """require_rentable - a refused call never reaches the body"""
    trip = Trip("B7", needs_repair=True)

    with pytest.raises(ValueError):
        trip.start()

    assert trip.needs_repair is True
