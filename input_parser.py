import re
from aux_data_structures import Stack, Queue, Tape

class InputParser:
    def __init__(self, input_string):
        self.input_string = input_string
        self.input_lines = input_string.strip().splitlines()

        self.contexts = {"GLOBAL": {}, "DATA": {}, "LOGIC": {}}
        self.current_context_space = "GLOBAL"
        self.iterator_line = 0

        self.data_keywords = [
            "STACK",
            "QUEUE",
            "TAPE"
        ]
        self.data_keywords = re.compile("^" + "|".join(self.data_keywords))

        self.command_keywords = [
            "SCAN LEFT",
            "SCAN RIGHT",
            "SCAN",
            "PRINT",
            "READ",
            "WRITE",
            "RIGHT",
            "LEFT",
            "UP",
            "DOWN"
        ]
        self.command_keywords = re.compile("^\s*(" + "|".join(self.command_keywords) + ")")

    def reset_iterator(self):
        self.iterator_line = 0
        self.current_context_space = "GLOBAL"

    def iterate_line(self, verbose=False):
        # Read line until not blank or comment
        while self.iterator_line < len(self.input_lines) and (self.input_lines[self.iterator_line] == "" or re.match("\s*//", self.input_lines[self.iterator_line])):
            self.iterator_line += 1

        while self.iterator_line < len(self.input_lines):
            line = self.input_lines[self.iterator_line]
            if verbose: print("Iterator read: " + line + " (" + str(self.iterator_line) + ")")

            # Increment iterator
            self.iterator_line += 1

            # If blank line, continue
            if line == "":
                continue

            # If comment, continue
            if re.match("\s*//", line):
                continue

            # Check if we're in a non-global context    
            if self.current_context_space == "GLOBAL":
                # Expect new context
                if not re.match("\.DATA|\.LOGIC", line):
                    raise SyntaxError("Expected new context at line " + str(self.iterator_line))
                else:
                    # Assign new context
                    self.current_context_space = line[1:]
                    if verbose: print("Context changed to " + self.current_context_space)
                return line
            elif self.current_context_space == "DATA":
                # Check for context change
                if re.match("\.LOGIC", line):
                    self.current_context_space = "LOGIC"
                    if verbose: print("Context changed to " + self.current_context_space)
                return line
            elif self.current_context_space == "LOGIC":
                # Check for context change
                if re.match("\.DATA", line):
                    self.current_context_space = "DATA"
                    if verbose: print("Context changed to " + self.current_context_space)
                return line
                
    def parse(self):
        # Check syntax
        self.check_syntax()

        # Parse
        aux_data = self.parse_data()
        logic = self.parse_logic()

        return { "aux_data": aux_data, "logic": logic }

    def parse_data(self):
        # Parse the data section
        self.reset_iterator()

        data_structures = {}
        
        while self.current_context_space != "DATA":
            self.iterate_line()
        
        while self.current_context_space == "DATA":
            line = self.iterate_line()

            # Break if end of context
            if line == None or self.current_context_space != "DATA":
                break
            
            # Ignore empty line
            if line == "":
                continue
            
            # Split declaration by spaces
            declarations = line.split(" ")

            # If more than 2 arguments, raise error
            if len(declarations) > 2:
                raise SyntaxError("Too many arguments for declaration at line " + str(self.iterator_line))

            # Get data structure type
            data_structure_type = declarations[0]

            # Get data structure name
            data_structure_name = declarations[1]

            # Raise error if data structure already exists
            if data_structure_name in data_structures:
                raise SyntaxError("Data structure " + data_structure_name + " already exists at line " + str(self.iterator_line))

            # Create data structure
            if data_structure_type == "STACK":
                data_structures[data_structure_name] = {
                    "type": "STACK",
                    "data": Stack()
                }
            elif data_structure_type == "QUEUE":
                data_structures[data_structure_name] = {
                    "type": "QUEUE",
                    "data": Queue()
                }
            elif data_structure_type == "TAPE":
                data_structures[data_structure_name] = {
                    "type": "TAPE",
                    "data": Tape()
                }
            else:
                raise SyntaxError("Invalid data structure type at line " + str(self.iterator_line))

        return data_structures
                

    def parse_logic(self):
        # Parse the logic section
        self.reset_iterator()

        logic = {}

        while self.current_context_space != "LOGIC":
            self.iterate_line()

        while self.current_context_space == "LOGIC":
            line = self.iterate_line()

            # Break if end of context
            if line == None or self.current_context_space != "LOGIC":
                break
            
            # Ignore empty line
            if line == "":
                continue

            # Read the states
            # State format: <state_name>] <instruction> <arguments>

            # Find the first ] in the line
            state_end = line.find("]")
            if state_end == -1:
                raise SyntaxError("Expected ] at line " + str(self.iterator_line))
            state_name = line[:state_end]
            line = line[state_end + 1:]

            # RegEx matching to look for command
            command_matches = self.command_keywords.findall(line.upper())
            if len(command_matches) == 0:
                raise SyntaxError("Expected command at line " + str(self.iterator_line))
            instruction = command_matches[0]

            # Get arguments
            arguments_idx = re.findall("\([^\s]*,[^\s]*\)", line)

            # Raise error if state already exists
            if state_name in logic:
                raise SyntaxError("State " + state_name + " already exists at line " + str(self.iterator_line))
            
            # Create instruction object
            logic[state_name] = {
                "instruction": instruction,
                "arguments": arguments_idx
            }

        return logic

    def check_syntax(self):
        # Reset iterator
        self.reset_iterator()

        # Check for syntax errors
        for i in range(len(self.input_lines)):
            # Check for empty lines
            if self.input_lines[i] == "":
                continue

            # Ignore if comment
            if re.match("\s*//", self.input_lines[i]):
                continue

            # Check if we're in a non-global context
            if self.current_context_space == "GLOBAL":
                # Expect new context
                if not re.match("\.DATA|\.LOGIC", self.input_lines[i]):
                    raise SyntaxError("Expected new context at line " + str(i + 1))
                else:
                    # Assign new context
                    self.current_context_space = self.input_lines[i][1:]
            elif self.current_context_space == "DATA":
                # Check for context change
                if re.match("\.LOGIC", self.input_lines[i]):
                    self.current_context_space = "LOGIC"
                    continue

                # Succeeding lines must be data structure declarations
                if not re.match("(STACK|QUEUE|TAPE)\s[a-zA-Z0-9_]*", self.input_lines[i]):
                    raise SyntaxError("Expected data structure declaration at line " + str(i + 1) + " in context " + self.current_context_space + ". Got " + self.input_lines[i])

            elif self.current_context_space == "LOGIC":
                # Check for context change
                if re.match("\.DATA", self.input_lines[i]):
                    self.current_context_space = "DATA"
                    continue

                # Succeeding lines must be logic instructions
                if not re.match("[a-zA-Z0-9_]*] (SCAN|PRINT|SCAN RIGHT|SCAN LEFT|READ|WRITE|RIGHT|LEFT|UP|DOWN)", self.input_lines[i]):
                    raise SyntaxError("Expected logic instruction at line " + str(i + 1) + " in context " + self.current_context_space + ". Got " + self.input_lines[i])

            else:
                raise NameError("Unknown context space: " + self.current_context_space)
            
