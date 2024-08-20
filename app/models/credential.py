import dataclasses
from typing import Union


@dataclasses.dataclass
class UserCredential:
    username: Union[str, None] = None
    password: Union[str, None] = None
