import dataclasses
from typing import Union, Optional


@dataclasses.dataclass
class TokenData:
    username: Optional[str] = None
