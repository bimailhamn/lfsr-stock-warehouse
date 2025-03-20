import pandas as pd
from tabulate import tabulate

class GeneralLFSR:
    def __init__(self, register_size: int, initial_state: str, feedback_positions: list[int]):
        """
        Initialize the General LFSR with configurable parameters.
        """
        if len(initial_state) != register_size:
            raise ValueError("Initial state length must match the register size.")

        self.__register_size = register_size
        self.__default_state = [int(bit) for bit in initial_state]
        self.__state = [int(bit) for bit in initial_state]
        self.__feedback_positions = feedback_positions
        self.__data = []

    @property
    def register_size(self):
        return self.__register_size

    @register_size.setter
    def register_size(self, size: int):
        if not size:
            raise ValueError("size cannot be empty")
        self.__register_size = size

    @property
    def state(self):
        return self.__state

    @state.setter
    def state(self, value: str):
        if not value:
            raise ValueError("size cannot be empty")
        if len(value) != self.__register_size:
            raise ValueError(f"Length of Value Must Be {self.__register_size}")
        self.__state = [int(bit) for bit in value]

    def reset_register(self):
        """Reset the register to a specific state."""
        self.__state = self.__default_state

    def define_tap_sequence(self):
        """
        Define and validate the tap sequence (feedback positions).
        Tap positions determine which bits in the register are XORed for feedback.
        """
        if len(self.__state) != self.__register_size:
            raise ValueError(f"Length of Value Must Be {self.__register_size}")
        if not all(0 <= pos < self.__register_size for pos in self.__feedback_positions):
            return None
        feedback_bit = 0
        for pos in self.__feedback_positions:
            feedback_bit ^= self.__state[pos]
        return feedback_bit

    def get_next_bit(self):
        """
        Retrieve the next bit of the stream and update the state of the register.
        This applies the XOR operation across the defined tap sequence to calculate the feedback bit.
        """
        next_bit = self.define_tap_sequence()
        if next_bit is None:
            raise ValueError("All feedback positions must be valid indices within the register size.")
        return next_bit

    def operate_lfsr(self, operation_count:int):
        if not operation_count:
            raise ValueError("Operation Count must be greater than 0")
        data = []
        for _ in range(operation_count):
            next_bit = self.get_next_bit()
            self.__state.pop()
            self.__state.insert(0, next_bit)
            data.append((''.join(map(str, self.__state)), next_bit))

        # Create a DataFrame to display results
        df = pd.DataFrame(data, columns=["State", "Next Bit"])
        df.index += 1
        # Print the DataFrame with border using tabulate
        print(tabulate(df, headers="keys", tablefmt="grid"))


if __name__ == "__main__":
    # Initialize LFSR with state '0110' and feedback positions [0, 3] (hardwired feedback function)
    lfsr = GeneralLFSR(register_size=4, initial_state='0110', feedback_positions=[0,3])
    lfsr.operate_lfsr(20)
    lfsr.state = '1110'
    lfsr.operate_lfsr(20)
    lfsr.reset_register()
    lfsr.operate_lfsr(20)
