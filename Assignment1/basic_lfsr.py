import pandas as pd
from tabulate import tabulate

class LFSR:
    def __init__(self, initial_state: str, feedback_positions: list[int]):
        """
        Initialize the LFSR.
        """
        self.state = [int(bit) for bit in initial_state]
        self.feedback_positions = feedback_positions

    def get_state(self) -> str:
        """Retrieve the current state of the LFSR."""
        return ''.join(map(str, self.state))

    def next_bit(self) -> int:
        """
        Generate the next bit in the stream and update the state.
        """
        # Generate feedback bit by XORing the specified positions
        feedback = 0
        for pos in self.feedback_positions:
            feedback ^= self.state[pos]

        # Shift the state and insert the feedback at the first of bit list
        self.state.pop()
        self.state.insert(0, feedback)

        return feedback

if __name__ == "__main__":
    # Initialize LFSR with state '0110' and feedback positions [0, 3] (hardwired feedback function)
    lfsr = LFSR(initial_state="0110", feedback_positions=[0, 3])

    # Collect the state and next bit 20 times
    data = []
    for _ in range(20):
        current_state = lfsr.get_state()
        next_stream_bit = lfsr.next_bit()
        data.append((current_state, next_stream_bit))

    # Create a DataFrame to display results
    df = pd.DataFrame(data, columns=["State", "Next Bit"])
    df.index += 1
    # Print the DataFrame with border using tabulate
    print(tabulate(df, headers="keys", tablefmt="grid"))
