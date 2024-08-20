import dataclasses
from typing import Union


@dataclasses.dataclass
class ReadResponse:
    data: dict[Union[int, float, str, bool], Union[int, float, str, bool]]


@dataclasses.dataclass
class WriteResponse:
    status: str


SUCCESS_WRITE_RESPONSE = WriteResponse(status="success")
FAILURE_WRITE_RESPONSE = WriteResponse(status="failure")