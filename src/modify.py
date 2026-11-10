def requires_status(status):
    """Finish this, then use it on the three methods below."""
    pass


class Reservation:
    def __init__(self, name):
        self.name = name
        self.status = "reserved"

    def pay(self):
        if self.status != "reserved":
            raise ValueError(f"pay needs a reserved booking, not {self.status}.")
        self.status = "paid"
        return f"{self.name} paid"

    def check_in(self):
        if self.status != "paid":
            raise ValueError(f"check_in needs a paid booking, not {self.status}.")
        self.status = "checked_in"
        return f"{self.name} checked in"

    def refund(self):
        if self.status != "paid":
            raise ValueError(f"refund needs a paid booking, not {self.status}.")
        self.status = "refunded"
        return f"{self.name} refunded"


_counter = 0


def next_ride_number():
    global _counter
    _counter += 1
    return _counter


def make_ride_numbers(start):
    """Replace next_ride_number with this."""
    pass


def audit(func):
    """Finish this, then put it on the three functions below."""
    pass


def dock(serial):
    print("start dock")
    result = f"{serial} docked"
    print("done dock")
    return result


def release(serial):
    print("start release")
    result = f"{serial} released"
    print("done release")
    return result


def repair(serial, days):
    print("start repair")
    result = f"{serial} repaired in {days} days"
    print("done repair")
    return result
