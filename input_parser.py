import re
from aux_data_structures import Stack, Queue, Tape

class InputParser:
    def __init__(self, input_string):
        self.input_string = input_string
        self.input_lines = input_string.strip().splitlines()

        self.contexts = {"GLOBAL": {}, "DATA": {}, "LOGIC": {}}
        self.current_context_space = "GLOBAL"
        self.iterator_line = 0

    def reset_iterator(self):
        self.iterator_line = 0
        self.current_context_space = "GLOBAL"

    def iterate_line(self):
        # Read line until not blank or comment
        while self.input_lines[self.iterator_line] == "" or re.match("\s*//", self.input_lines[self.iterator_line]):
            self.iterator_line += 1

        while True:
            line = self.input_lines[self.iterator_line]
            # print("Iterator read: " + line + " (" + str(self.iterator_line) + ")")

            # Increment iterator
            self.iterator_line += 1

            # Check if we're in a non-global context    
            if self.current_context_space == "GLOBAL":
                # Expect new context
                if not re.match("\.DATA|\.LOGIC", line):
                    raise SyntaxError("Expected new context at line " + str(self.iterator_line))
                else:
                    # Assign new context
                    self.current_context_space = line[1:]
                    # print("Context changed to " + self.current_context_space)
                    continue
            elif self.current_context_space == "DATA":
                # Check for context change
                if re.match("\.LOGIC", line):
                    self.current_context_space = "LOGIC"
                    # print("Context changed to " + self.current_context_space)
                    continue
                return line
            elif self.current_context_space == "LOGIC":
                # Check for context change
                if re.match("\.DATA", line):
                    self.current_context_space = "DATA"
                    # print("Context changed to " + self.current_context_space)
                    continue
                return line
                
    def parse(self):
        # Check syntax
        self.check_syntax()

        # Parse
        aux_data = self.parse_data()
        logic = self.parse_logic()

        return { aux_data, logic }

    def parse_data(self):
        # Parse the data section
        self.reset_iterator()

        data_structures = {}
        
        while self.current_context_space != "DATA":
            self.iterate_line()
        
        while self.current_context_space == "DATA":
            line = self.iterate_line()
            
            # Ignore empty line
            if line == "":
                continue
            
            # Split declaration by spaces
            declarations = line.split(" ")

            # Get data structure type
            data_structure_type = declarations[0]

            # Get data structure name
            data_structure_name = declarations[1]

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

        return data_structures
                

    def parse_logic(self):
        # Parse the logic section
        pass

    def check_syntax(self):
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
            
