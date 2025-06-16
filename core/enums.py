from enum import Enum

class GameFormat(Enum):
    """Available game formats"""
    DRAFT = "Draft"
    SEALED = "Sealed"
    CONSTRUCTED = "Constructed"
    COMMANDER = "Commander"
    WINSTON_DRAFT = "Winston Draft"
    JUMP_IN = "Jump In"
    BOOSTER_WAR = "Booster War"

    @classmethod
    def list(cls) -> list[str]:
        return [format.value for format in cls]

class Color(Enum):
    """Magic card colors"""
    BLUE = "Blue"
    GREEN = "Green"
    RED = "Red"
    WHITE = "White"
    BLACK = "Black"

    @classmethod
    def list(cls) -> list[str]:
        return [color.value for color in cls]

class Edition(Enum):
    """Available card editions"""
    NONE = "None"
    FINAL_FANTASY = "Final Fantasy"
    TARKIR = "Tarkir Dragonstorm"
    AETHERDRIFT = "Aetherdrift"
    INNISTRAD = "Innistrad Remastered"
    FOUNDATIONS = "Foundations"
    DUSKMOURN = "Duskmourn"
    OUTLAWS = "Outlaws of Thunder Junction"
    LOTR = "Lord of the Rings"
    DOMINARIA = "Dominaria Remastered"
    KAMIGAWA = "Kamigawa"
    OLLIS_CUBE = "Ollis Cube"

    @classmethod
    def list(cls) -> list[str]:
        return [edition.value for edition in cls]
