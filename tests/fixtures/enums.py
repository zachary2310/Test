from enum import Enum, auto


class BOOK_GENRES(Enum):
    ROMMAN = auto()
    THRILLER = auto()
    HORROR = auto()


class BOOKS(Enum):
    A = auto()
    B = auto()
    C = auto()


class USERS(Enum):
    A = auto()
    B = auto()
    C = auto()
    ADMIN_A = auto()
