import random
from dataclasses import dataclass
from typing import List, Optional


@dataclass
class CustomerRecord:
    arrival: float
    start_service: float
    departure: float

    @property
    def wait_time(self) -> float:
        return self.start_service - self.arrival

    @property
    def system_time(self) -> float:
        return self.departure - self.arrival

    @property
    def service_time(self) -> float:
        return self.departure - self.start_service


def uniform_time(mean: float, half_range: float) -> float:
    """Uniform(mean-half_range, mean+half_range)."""
    return random.uniform(mean - half_range, mean + half_range)


def simulate_barber_shop(
    day_minutes: float = 420.0,           # 9am to 4pm
    interarrival_mean: float = 10.0,
    interarrival_half_range: float = 2.0, # ±2
    service_mean: float = 13.0,
    service_half_range: float = 2.0,      # ±2
    seed: Optional[int] = None
) -> dict:
    """
    Discrete-event simulation of a single-server (1 barber) FIFO queue.
    Arrivals occur until day_minutes; service continues until system empties.
    """
    if seed is not None:
        random.seed(seed)

    # ---------- Generate arrival times until closing ----------
    arrivals: List[float] = []
    t = 0.0
    while True:
        t += uniform_time(interarrival_mean, interarrival_half_range)  # Uniform(8,12)
        if t > day_minutes:
            break
        arrivals.append(t)

    # ---------- Process customers in FIFO order ----------
    records: List[CustomerRecord] = []
    barber_free_time = 0.0  # when barber becomes available next
    busy_time = 0.0
    max_queue_len = 0

    # For queue length estimation at arrival instants:
    # queue_len = number of customers who arrived but haven't started service yet.
    # At each arrival, those with start_service <= arrival are no longer waiting.
    waiting_starts: List[float] = []  # store start_service times of customers processed so far

    for arrival in arrivals:
        # compute queue length at this arrival time (waiting only, not in service)
        # customers already started service by 'arrival' are not in queue.
        while waiting_starts and waiting_starts[0] <= arrival:
            waiting_starts.pop(0)

        # If barber is busy, and next free time is after arrival, customer waits.
        start_service = max(arrival, barber_free_time)
        service_time = uniform_time(service_mean, service_half_range)  # Uniform(11,15)
        departure = start_service + service_time

        barber_free_time = departure
        busy_time += service_time

        rec = CustomerRecord(arrival=arrival, start_service=start_service, departure=departure)
        records.a
