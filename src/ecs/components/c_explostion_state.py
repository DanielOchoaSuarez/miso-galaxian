from enum import Enum

class CExplosionState:
    def __init__(self) -> None:
        self.state = ExplosionState.EXPLODE

class ExplosionState(Enum):
    EXPLODE = 0