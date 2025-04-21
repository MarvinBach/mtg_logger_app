from enum import Enum

class GameFormat(Enum):
    DRAFT = "Draft"
    CUBE_DRAFT = "Cube Draft"
    SEALED = "Sealed"
    CONSTRUCTED = "Constructed"
    COMMANDER = "Commander"
    ARENA = "Arena"

    @classmethod
    def list(cls) -> list[str]:
        return [format.value for format in cls]

class Color(Enum):
    BLUE = "Blue"
    GREEN = "Green"
    RED = "Red"
    WHITE = "White"
    BLACK = "Black"

    @classmethod
    def list(cls) -> list[str]:
        return [color.value for color in cls]

class Edition(Enum):
    NONE = "None"
    TARKIR = "Tarkir Dragonstorm"
    AETHERDRIFT = "Aetherdrift"
    INNISTRAD = "Innistrad Remastered"
    FOUNDATIONS = "Foundations"
    DUSKMOURN = "Duskmourn"
    OUTLAWS = "Outlaws of Thunder Junction"

    @classmethod
    def list(cls) -> list[str]:
        return [edition.value for edition in cls]
