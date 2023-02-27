import re

class InputParser:
    def __init__(self, input_string):
        self.input_string = input_string
        self.input_lines = input_string.strip().splitlines()

        self.contexts = {"GLOBAL": {}, "DATA": {}, "LOGIC": {}}
        self.current_context_space = "GLOBAL"

    def check_syntax(self):
        # Check for syntax errors
        for i in range(len(self.input_lines)):
            # Check for empty lines
            if self.input_lines[i] == "":
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
                if not re.match("(STACK|QUEUE|TAPE)\s[a-zA-Z0-9]*", self.input_lines[i]):
                    raise SyntaxError("Expected data structure declaration at line " + str(i + 1) + " in context " + self.current_context_space + ". Got " + self.input_lines[i])

            elif self.current_context_space == "LOGIC":
                # Check for context change
                if re.match("\.DATA", self.input_lines[i]):
                    self.current_context_space = "DATA"
                    continue

                # Succeeding lines must be logic instructions
                

            else:
                raise NameError("Unknown context space: " + self.current_context_space)