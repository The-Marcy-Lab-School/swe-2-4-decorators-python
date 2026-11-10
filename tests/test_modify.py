from modify import Reservation, audit, dock, make_ride_numbers, release, repair, requires_status


TEST_SUITE_NAME = "Modify Tests"


import pytest



def test_the_happy_path_still_works():
    """Reservation - reserved, then paid, then checked in"""
    booking = Reservation("Ana")

    assert booking.status == "reserved"
    assert booking.pay() == "Ana paid"
    assert booking.status == "paid"
    assert booking.check_in() == "Ana checked in"
    assert booking.status == "checked_in"


def test_each_transition_still_refuses_from_the_wrong_status():
    """Reservation - the three rules did not change"""
    with pytest.raises(ValueError):
        Reservation("Ana").check_in()
    with pytest.raises(ValueError):
        Reservation("Ben").refund()

    paid = Reservation("Cal")
    paid.pay()
    with pytest.raises(ValueError):
        paid.pay()


def test_a_refused_call_leaves_the_status_alone():
    """Reservation - the guard raises before the method body runs"""
    booking = Reservation("Ana")

    with pytest.raises(ValueError):
        booking.check_in()

    assert booking.status == "reserved"


def test_refunding_a_paid_booking_works():
    """Reservation - refund runs from paid"""
    booking = Reservation("Ana")
    booking.pay()

    assert booking.refund() == "Ana refunded"
    assert booking.status == "refunded"


def test_the_three_methods_go_through_a_decorator_now():
    """Reservation - each transition is wrapped rather than checking for itself"""
    for name in ("pay", "check_in", "refund"):
        method = getattr(Reservation, name)
        assert method.__closure__ is not None, \
            f"{name} should be wrapped by @requires_status(...), not test the status itself."

    assert callable(requires_status("paid")), \
        "requires_status(status) returns a decorator, which is then applied to a method."


def test_requires_status_works_on_a_class_it_never_saw():
    """requires_status - it reads self.status, so any status-driven class can use it"""
    class Loan:
        def __init__(self):
            self.status = "open"

        @requires_status("closed")
        def archive(self):
            return "archived"

    with pytest.raises(ValueError):
        Loan().archive()


import modify



def test_the_numbers_start_where_they_were_asked_to():
    """make_ride_numbers - the first call returns start"""
    grand_army = make_ride_numbers(1)

    assert grand_army() == 1
    assert grand_army() == 2
    assert grand_army() == 3


def test_a_different_start_is_honored():
    """make_ride_numbers - start is whatever it was built with"""
    borough_hall = make_ride_numbers(500)

    assert borough_hall() == 500
    assert borough_hall() == 501


def test_two_counters_do_not_share_a_number():
    """make_ride_numbers - each closure owns its own count"""
    grand_army = make_ride_numbers(1)
    borough_hall = make_ride_numbers(500)

    grand_army()
    grand_army()

    assert borough_hall() == 500, "Building a second counter must not see the first's."
    assert grand_army() == 3


def test_the_module_level_counter_is_gone():
    """make_ride_numbers - nothing shared is left at module level"""
    assert not hasattr(modify, "next_ride_number"), \
        "Delete next_ride_number. make_ride_numbers replaces it."
    assert not hasattr(modify, "_counter"), \
        "Delete the module-level counter. The closure holds it now."


def test_every_result_is_unchanged():
    """audit - a refactor, so the three answers must not move"""
    assert dock("A1") == "A1 docked"
    assert release("A1") == "A1 released"
    assert repair("A1", 2) == "A1 repaired in 2 days"


def test_the_lines_still_print_around_the_work(capsys):
    """audit - start before, done after"""
    dock("A1")
    out = capsys.readouterr().out

    assert "start dock" in out
    assert "done dock" in out
    assert out.index("start dock") < out.index("done dock"), \
        "Print start before calling the function and done after it returns."


def test_audit_reads_the_name_off_the_function(capsys):
    """audit - it works on a function it was never told about"""
    @audit
    def inspect_frame(serial):
        return serial

    inspect_frame("A1")
    out = capsys.readouterr().out

    assert "start inspect_frame" in out
    assert "done inspect_frame" in out


def test_the_three_functions_are_decorated_now():
    """audit - the printing left their bodies"""
    for func in (dock, release, repair):
        assert func.__closure__ is not None, \
            f"Put @audit on {func.__name__} and take the printing out of its body."
