from dataclasses import dataclass


@dataclass
class DataArguments:
    """
    This class is used to store all the data arguments
    """
    ip: str
    port: int
    count: int
    interval: float
    timeout: float
