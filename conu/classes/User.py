from dataclasses import dataclass


@dataclass
class User:
    id: int
    first_name: str
    last_name: str
    job_title: str
    email_address: str
    username: str
    password: str
    permission_level: int
    available: bool
