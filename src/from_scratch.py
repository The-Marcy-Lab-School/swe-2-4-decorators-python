class Bike:
    """Already written for you. Do not change it."""

    def __init__(self, serial, station, needs_repair):
        self.serial = serial
        self.station = station
        self.needs_repair = needs_repair

    def is_rentable(self):
        return not self.needs_repair

    def hourly_rate(self):
        return 3.00

    def __repr__(self):
        return f"{type(self).__name__}({self.serial!r})"


def announce(func):
    pass


def make_surcharge(amount):
    pass


def requires_paid(method):
    pass


class Rental:
    pass


def count_calls(func):
    pass
