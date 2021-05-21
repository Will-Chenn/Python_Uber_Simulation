"""Dispatcher for the simulation"""

from typing import Optional
from typing import List
from driver import Driver
from rider import Rider


class Dispatcher:
    """A dispatcher fulfills requests from riders and drivers for a
    ride-sharing service.

    When a rider requests a driver, the dispatcher assigns a driver to the
    rider. If no driver is available, the rider is placed on a waiting
    list for the next available driver. A rider that has not yet been
    picked up by a driver may cancel their request.

    When a driver requests a rider, the dispatcher assigns a rider from
    the waiting list to the driver. If there is no rider on the waiting list
    the dispatcher does nothing. Once a driver requests a rider, the driver
    is registered with the dispatcher, and will be used to fulfill future
    rider requests.
    """
    drivers: List[Driver]
    riders_waiting: List[Rider]

    def __init__(self) -> None:
        """Initialize a Dispatcher.

        """
        self.drivers = []
        self.riders_waiting = []

    def __str__(self) -> str:
        """Return a string representation.

        """
        return "riders: {}, drivers:{}".format(self.riders_waiting,
                                               self.drivers)

    def request_driver(self, rider: Rider) -> Optional[Driver]:
        """Return a driver for the rider, or None if no driver is available.

        Add the rider to the waiting list if there is no available driver.

        """
        if self.drivers:
            locate = rider.origin
            time_list = []
            idle_drivers = []
            for driver in self.drivers:
                if driver.is_idle:
                    time = driver.get_travel_time(locate)
                    time_list.append(time)
                    idle_drivers.append(driver)
            if len(idle_drivers) != 0 and len(time_list) != 0:
                i = find_min(time_list)
                return idle_drivers[i]
        self.riders_waiting.append(rider)
        return None

    def request_rider(self, driver: Driver) -> Optional[Rider]:
        """Return a rider for the driver, or None if no rider is available.

        If this is a new driver, register the driver for future rider requests.

        """
        if driver not in self.drivers:
            self.drivers.append(driver)
        if len(self.riders_waiting) == 0:
            return None
        rider = self.riders_waiting.pop(0)
        return rider

    def cancel_ride(self, rider: Rider) -> None:
        """Cancel the ride for rider.

        """
        if rider in self.riders_waiting:
            self.riders_waiting.remove(rider)


def find_min(time_list: List) -> int:
    """
    return the index of the least number in a list
    """
    mini = time_list[0]
    num = 0
    for count, item in enumerate(time_list):
        if item < mini:
            mini = item
            num = count

    return num


if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config={'extra-imports': ['typing', 'driver', 'rider']})
