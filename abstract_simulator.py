import re
from aux_data_structures import Stack, Queue, Tape, InputTape

class AbstractMachineSimulator:
    def __init__(self, machine_definition) -> None:

        self.aux_data = None
        self.input_tape = None

        self.logic = machine_definition["logic"]
        self.aux_data = machine_definition["aux_data"]

        # Lifecycle
        self.halted = False
        self.current_state = None
        self.input_tapehead_idx = 0
        
        # Memory
        self.memory = {}

        # Initialize aux data to memory
        for key in self.aux_data.keys():
            if(self.aux_data[key]["type"] == "STACK"):
                self.memory[key] = Stack()
            elif(self.aux_data[key]["type"] == "QUEUE"):
                self.memory[key] = Queue()
            elif(self.aux_data[key]["type"] == "TAPE"):
                self.memory[key] = Tape()
            else:
                raise Exception("Unknown aux data type: " + self.aux_data[key]["type"])

        # Build the state map
        self.state_map = {}
        for key in self.logic.keys():
            self.state_map[key] = {
                "instruction": None,
                "associated_data": None,
                "transitions": {}
            }
            # Set the transitions
            for t in self.logic[key]["arguments"]:
                t = t.split(",")
                transition = (t[0][1:], t[1][:-1])
                self.state_map[key]["transitions"][transition[0]] = transition[1]

            # Check the instruction for an aux data
            data = re.findall("\([a-zA-Z0-9_]{1,}\)", self.logic[key]["instruction"])
            if len(data) > 0:
                # Get the aux data
                self.state_map[key]["associated_data"] = data[0][1:-1]
                # Remove the aux data from the instruction
                self.state_map[key]["instruction"] = self.logic[key]["instruction"].replace("(" + data[0][1:-1] + ")", "")
            else:
                self.state_map[key]["instruction"] = self.logic[key]["instruction"]

    def set_input_tape(self, input_tape):
        # Ensure that the input tape is a string with the first and last character as #
        if not isinstance(input_tape, str):
            raise Exception("Input tape must be a string")
        if input_tape[0] != "#" or input_tape[-1] != "#":
            raise Exception("Input tape must start and end with #")
        
        # Turn the input tape into a Tape of type InputTape
        self.input_tape = InputTape(input_tape)

    def step(self, verbose=False) -> bool:
        # If the input tape is not set yet, raise an error
        if self.input_tape == None:
            raise Exception("Input tape not set")
        
        # If the machine is halted
        if self.halted:
            return False
        
        # If the current state is not set, set it to the first state
        if self.current_state == None:
            first_state = list(self.state_map.keys())[0]
            self.current_state = first_state
            if verbose: print("Starting at state " + first_state)
            # Read the first sharp
            if(self.input_tape.read() != "#"):
                raise Exception("Input tape must start with #")
            print("Read first #")

        # Get the current state
        current_state = self.state_map[self.current_state]
        # Get the current instruction
        instruction = current_state["instruction"]
        # Get the current associated data
        associated_data = current_state["associated_data"]
        # Get the current transitions
        transitions = current_state["transitions"]

        symbol_buffer = ""

        # Execute the instruction
        if instruction == "SCAN":
            symbol_buffer = self.input_tape.read()
            self.input_tape.move("R")
            if verbose: print("Read symbol " + symbol_buffer)
