from dataclasses import dataclass

@dataclass
class Player:
    _value: int

    def __post_init__(self):
        if self._value != -1 and self._value != 1:
            raise ValueError("Player value is incorrect, chose between -1 or 1.")

    def __hash__(self) -> int:
        return self._value

    def __repr__(self):
        return f"Player({self.symbol})"

    @property
    def value(self):
        return self._value
    
    @property
    def symbol(self):
        return 'X' if self._value == -1 else 'O'
    
    @property
    def is_x(self):
        return self._value == -1
    
    @property
    def is_o(self):
        return self._value == 1

    def switch_player(self):
        return Player(self._value * -1)

    @classmethod
    def create_x(cls):
        return cls(-1)
    
    @classmethod
    def create_y(cls):
        return cls(1)