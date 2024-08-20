import dataclasses
from typing import Union


@dataclasses.dataclass
class User:
    username: Union[str, None] = None
    password: Union[str, None] = None