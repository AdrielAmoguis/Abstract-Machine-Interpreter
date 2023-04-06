import re
from aux_data_structures import Stack, Queue, Tape, InputTape

class AbstractMachineSimulator:
    def __init__(self, machine_definition) -> None:

        self.aux_data = None
        self.input_tape = None

        self.logic = machine_definition["logic"]
        self.aux_data = machine_definition["aux_data"]

        # Lifecycle
        self.accepted = False
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
            # if(self.input_tape.read() != "#"):
            #     raise Exception("Input tape must start with #")
            # print("Read first #")

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
            self.input_tape.move("R")
            symbol_buffer = self.input_tape.read()
            if verbose: print("Read symbol " + symbol_buffer)
        elif instruction == "WRITE":
            if associated_data == None:
                raise Exception("WRITE instruction requires associated data")
            # Get the data type and write accordingly
            if isinstance(self.aux_data[associated_data], Stack):
                self.aux_data[associated_data].push(symbol_buffer)
            elif isinstance(self.aux_data[associated_data], Queue):
                self.aux_data[associated_data].enqueue(symbol_buffer)
            elif isinstance(self.aux_data[associated_data], Tape):
                self.aux_data[associated_data].write(symbol_buffer)
            if verbose: print("Wrote symbol " + symbol_buffer + " to " + associated_data)
        elif instruction == "READ":
            if associated_data == None:
                raise Exception("READ instruction requires associated data")
            # Get the data type and read accordingly
            if isinstance(self.aux_data[associated_data], Stack):
                symbol_buffer = self.aux_data[associated_data].pop()
            elif isinstance(self.aux_data[associated_data], Queue):
                symbol_buffer = self.aux_data[associated_data].dequeue()
            elif isinstance(self.aux_data[associated_data], Tape):
                symbol_buffer = self.aux_data[associated_data].read()
            if verbose: print("Read symbol " + symbol_buffer + " from " + associated_data)
        elif instruction == "PRINT":
            # Print the symbol buffer
            print(symbol_buffer)
            if verbose: print("Printed symbol " + symbol_buffer)
        elif instruction == "SCAN RIGHT":
            # Move the tape head right
            self.input_tape.move("R")
            symbol_buffer = self.input_tape.read()
            if verbose: print("Read symbol " + symbol_buffer + " from the right")
        elif instruction == "SCAN LEFT":
            # Move the tape head left
            self.input_tape.move("L")
            symbol_buffer = self.input_tape.read()
            if verbose: print("Read symbol " + symbol_buffer + " from the left")
        elif instruction == "RIGHT":
            # Move the associated data head right
            if associated_data == None:
                raise Exception("RIGHT instruction requires associated data")
            self.aux_data[associated_data].move("R")
            symbol_buffer = self.aux_data[associated_data].read()
            if verbose: print("Moved " + associated_data + " head right")
        elif instruction == "LEFT":
            # Move the associated data head left
            if associated_data == None:
                raise Exception("LEFT instruction requires associated data")
            self.aux_data[associated_data].move("L")
            symbol_buffer = self.aux_data[associated_data].read()
            if verbose: print("Moved " + associated_data + " head left")
        
        # Check the available transitions for the symbol buffer
        if symbol_buffer in transitions.keys():
            
            # If accepting state, halt the machine
            if transitions[symbol_buffer].lower() == "accept":
                self.halted = True
                self.accepted = True
                if verbose: print("Accepting state reached. Machine halted.")
                return False
            
            # If rejecting state, halt the machine
            if transitions[symbol_buffer].lower() == "reject":
                self.halted = True
                self.accepted = False
                if verbose: print("Rejecting state reached. Machine halted.")
                return False

            # Get the transition and go to next state
            self.current_state = transitions[symbol_buffer]
            if verbose: print("Transitioning to state " + self.current_state)
            
            return False
        else:
            # If there is no transition, halt
            self.halted = True
            if verbose: print("No transition found for this symbol. Machine halted.")
            return False