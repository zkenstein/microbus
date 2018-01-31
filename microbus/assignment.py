import microbus
from microbus.bus import Bus
import logging

logger = logging.getLogger(__name__)


class BusAssignment(object):
    def __init__(self, bus, route, driver = None):
        self.bus = bus
        self.route = route
        self._finished = False
        self.driver = driver

    @property
    def finished(self):
        return self._finished

    def __contains__(self, item):
        if isinstance(item, Bus):
            return self.bus == item

        if isinstance(item, microbus.BusRoute) or isinstance(item, microbus.BusStop):
            if self.finished:
                return False
            if self.bus.current_route is None:
                return item in self.route
            return item in self.bus.current_route
        return False

    def __call__(self, *args, **kwargs):
        if self.driver:
            trip = self.bus.depart(self.route)
            self.driver(trip)
            if self.bus.current_route is not None:
                logger.warn("Route was not completed by driver, cancelling route")
                trip.close()
        else:
            for _ in self.bus.depart(self.route):
                pass
        self._finished = True
