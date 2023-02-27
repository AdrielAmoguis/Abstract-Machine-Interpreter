import re

class InputParser:
    def __init__(self, input_string):
        self.input_string = input_string
        self.input_lines = input_string.strip().splitlines()

        self.contexts = {"GLOBAL": {}, "DATA": {}, "LOGIC": {}}
        self.current_context_space = "GLOBAL"

    def parse(self):
        # Check syntax
        self.check_syntax()

        # Parse
        aux_data = self.parse_data()
        logic = self.parse_logic()

        return { aux_data, logic }

    def parse_data(self):
        # Parse the data section
        pass

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
            
