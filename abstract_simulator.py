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

    def set_input_tape(self, input_tape, is_turing_machine=False):
        # Ensure that the input tape is a string with the first and last character as #
        if not isinstance(input_tape, str):
            raise Exception("Input tape must be a string")
        if input_tape[0] != "#" or input_tape[-1] != "#":
            raise Exception("Input tape must start and end with #")
        
        # Turn the input tape into a Tape of type InputTape
        self.input_tape = InputTape(input_tape)

        # If this is a Turing machine, set the input tape to the first declared tape aux data
        if is_turing_machine:
            for key in self.aux_data.keys():
                if self.aux_data[key]["type"] == "TAPE":
                    self.memory[key] = self.input_tape
                    break

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

        # Check if accepting or rejecting state
        if self.current_state.lower() == "accept":
            self.accepted = True
            self.halted = True
            if verbose: print("Accepted and halted.")
            return False
        elif self.current_state.lower() == "reject":
            self.halted = True
            if verbose: print("Rejected and halted.")
            return False

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

            # Transition to the next state
            if symbol_buffer in transitions.keys():
                self.current_state = transitions[symbol_buffer]
                if verbose: print("Transitioned to state " + self.current_state)
            else:
                self.halted = True
                if verbose: print("No transitions found for this symbol. Halted.")
        elif instruction == "WRITE":
            if associated_data == None:
                raise Exception("WRITE instruction requires associated data")
            
            # Grab the value to write from the transitions
            keys = transitions.keys()
            if len(keys) > 1:
                raise Exception("WRITE instruction can only have one transition.")
            symbol_buffer = list(keys)[0]

            # Get the data type and write accordingly
            if isinstance(self.memory[associated_data], Stack):
                self.memory[associated_data].push(symbol_buffer)
            elif isinstance(self.memory[associated_data], Queue):
                self.memory[associated_data].enqueue(symbol_buffer)
            elif isinstance(self.memory[associated_data], Tape):
                raise Exception("Tape is not a valid data type for WRITE instruction")
            if verbose: print("Wrote symbol " + symbol_buffer + " to " + associated_data)

            # Transition to the next state
            self.current_state = transitions[symbol_buffer]
            if verbose: print("Transitioned to state " + self.current_state)

        elif instruction == "READ":
            if associated_data == None:
                raise Exception("READ instruction requires associated data")
            # Get the data type and read accordingly
            if isinstance(self.memory[associated_data], Stack):
                symbol_buffer = self.memory[associated_data].pop()
            elif isinstance(self.memory[associated_data], Queue):
                symbol_buffer = self.memory[associated_data].dequeue()
            elif isinstance(self.memory[associated_data], Tape):
                raise Exception("Tape is not a valid data type for READ instruction")
            if verbose: print("Read symbol " + symbol_buffer + " from " + associated_data)

            # Transition to the next state based on the sybmol buffer
            if symbol_buffer in transitions.keys():
                self.current_state = transitions[symbol_buffer]
                if verbose: print("Transitioned to state " + self.current_state)
            else:
                self.halted = True
                if verbose: print("No transitions found for this symbol. Halted.")

        elif instruction == "PRINT":
            # Get the value to print from the transitions
            keys = transitions.keys()
            if len(keys) > 1:
                raise Exception("PRINT instruction can only have one transition.")
            symbol_buffer = list(keys)[0]

            # Print the symbol buffer
            print(symbol_buffer)
            if verbose: print("Printed symbol " + symbol_buffer)

            # Transition to the next state
            self.current_state = transitions[symbol_buffer]
            if verbose: print("Transitioned to state " + self.current_state)

        elif instruction == "SCAN RIGHT":
            # Move the tape head right
            self.input_tape.move("R")
            symbol_buffer = self.input_tape.read()
            if verbose: print("Read symbol " + symbol_buffer + " from the right")

            # Transition to the next state based on symbol read
            if symbol_buffer in transitions.keys():
                self.current_state = transitions[symbol_buffer]
                if verbose: print("Transitioned to state " + self.current_state)
            else:
                self.halted = True
                if verbose: print("No transitions found for this symbol. Halted.")

        elif instruction == "SCAN LEFT":
            # Move the tape head left
            self.input_tape.move("L")
            symbol_buffer = self.input_tape.read()
            if verbose: print("Read symbol " + symbol_buffer + " from the left")

            # Transition to the next state based on symbol read
            if symbol_buffer in transitions.keys():
                self.current_state = transitions[symbol_buffer]
                if verbose: print("Transitioned to state " + self.current_state)
            else:
                self.halted = True
                if verbose: print("No transitions found for this symbol. Halted.")
                
        elif instruction == "RIGHT":
            # Assert that the symbol buffer is not empty and associated data is a tape
            if not isinstance(self.memory[associated_data], Tape):
                raise Exception("Associated data must be a tape")
            # Move the tape head right
            self.memory[associated_data].move("R")
            # Read
            symbol_buffer = self.memory[associated_data].read()
            if verbose: print("Read symbol " + symbol_buffer + " from the right")
            # Find this symbol in the available transitions
            keys = list(map(lambda x: (x.split("/")[0], x.split("/")[1]), transitions.keys()))
            keys = list(filter(lambda x: x[0] == symbol_buffer, keys))
            if len(keys) > 1:
                raise Exception("More than one transition for a symbol. Non-determinism is not supported.")
            
            # Replace the symbol in the tape with the symbol in the transition
            if len(keys[0]) > 1:
                # Get the transition and go to next state
                self.current_state = transitions[str(keys[0][0]) + "/" + str(keys[0][1])]
                self.memory[associated_data].write(keys[0][1])
                if verbose: print("Replaced symbol " + symbol_buffer + " with " + keys[0][1])
                if verbose: print("Transitioning to state " + self.current_state)
            else:
                # Get the transition and go to next state
                self.current_state = transitions[keys[0][0]]
                if verbose: print("Transitioning to state " + self.current_state)

        elif instruction == "LEFT":
            # Assert that the symbol buffer is not empty and associated data is a tape
            if not isinstance(self.memory[associated_data], Tape):
                raise Exception("Associated data must be a tape")
            # Move the tape head left
            self.memory[associated_data].move("L")
            # Read
            symbol_buffer = self.memory[associated_data].read()
            if verbose: print("Read symbol " + symbol_buffer + " from the left")
            # Find this symbol in the available transitions
            keys = list(map(lambda x: (x.split("/")[0], x.split("/")[1]), transitions.keys()))
            keys = list(filter(lambda x: x[0] == symbol_buffer, keys))
            if len(keys) > 1:
                raise Exception("More than one transition for a symbol. Non-determinism is not supported.")
            
            # Replace the symbol in the tape with the symbol in the transition
            if len(keys[0]) > 1:
                # Get the transition and go to next state
                self.current_state = transitions[str(keys[0][0]) + "/" + str(keys[0][1])]
                self.memory[associated_data].write(keys[0][1])
                if verbose: print("Replaced symbol " + symbol_buffer + " with " + keys[0][1])
                if verbose: print("Transitioning to state " + self.current_state)
            else:
                # Get the transition and go to next state
                self.current_state = transitions[keys[0][0]]
                if verbose: print("Transitioning to state " + self.current_state)

        else:
            raise Exception("Instruction not supported.")
        
    def run(self, verbose=False):
        """Runs the machine until it halts"""
        while not self.halted:
            self.step(verbose=verbose)