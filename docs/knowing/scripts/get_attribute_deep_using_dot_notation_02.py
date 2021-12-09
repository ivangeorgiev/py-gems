import dataclasses

@dataclasses.dataclass
class Address:
    city: str

@dataclasses.dataclass
class User:
    name: str
    address: Address
