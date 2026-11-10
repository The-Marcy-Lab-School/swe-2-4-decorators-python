def timed(func):
    def wrapper(*args, **kwargs):
        print(f"timed {func.__name__}")
        func(*args, **kwargs)
    return wrapper


@timed
def rental_cost(rate, hours):
    return rate * hours


def require_rentable(method):
    def wrapper(self, *args, **kwargs):
        if self.needs_repair:
            raise ValueError(f"{self.serial} needs repair, so it cannot be rented.")
        return method(self, *args, **kwargs)


class Trip:
    def __init__(self, serial, needs_repair):
        self.serial = serial
        self.needs_repair = needs_repair

    @require_rentable
    def start(self):
        return f"{self.serial} started"
