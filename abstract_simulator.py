class AbstractSimulator:
    def __init__(self, input_tape, parsed=None) -> None:

        self.aux_data = None
        self.instructions = None
        self.input_tape = input_tape

        if parsed is not None:
            self.logic = parsed["logic"]
            self.aux_data = parsed["aux_data"]

        # Lifecycle
        self.running = False
        self.finished = False
        self.current_state = None
        self.input_tapehead = 0

        