import dataclasses
from typing import Union


@dataclasses.dataclass
class ReadRequest:
    keys: list[Union[int, float, str, bool]]


@dataclasses.dataclass
class WriteRequest:
    data: dict[Union[int, float, str, bool], Union[int, float, str, bool]]
