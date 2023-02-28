class Stack:
    def __init__(self):
        self.stack = []
        self.top = -1

    def push(self, value):
        self.stack.append(value)
        self.top += 1

    def pop(self):
        if self.top == -1:
            return None
        else:
            self.top -= 1
            return self.stack.pop()

    def peek(self):
        if self.top == -1:
            return None
        else:
            return self.stack[self.top]

    def get_stack(self):
        return self.stack

    def get_top(self):
        return self.top

    def is_empty(self):
        return self.top == -1

    def __str__(self):
        return str(self.stack)
    
class Queue:
    def __init__(self):
        self.queue = []
        self.front = 0
        self.back = -1

    def enqueue(self, value):
        self.queue.append(value)
        self.back += 1

    def dequeue(self):
        if self.front > self.back:
            return None
        else:
            self.front += 1
            return self.queue.pop(0)

    def peek(self):
        if self.front > self.back:
            return None
        else:
            return self.queue[self.front]

    def get_queue(self):
        return self.queue

    def get_front(self):
        return self.front

    def get_back(self):
        return self.back

    def is_empty(self):
        return self.front > self.back

    def __str__(self):
        return str(self.queue)
    
class Tape:
    def __init__(self):
        self.tape = {}
        self.head = 0

    def write(self, value):
        self.tape[self.head] = value

    def read(self):
        if self.head in self.tape:
            return self.tape[self.head]
        else:
            return None

    def move(self, direction):
        if direction == "R":
            self.head += 1
        elif direction == "L":
            self.head -= 1
        else:
            raise ValueError("Invalid direction: " + direction)

    def get_tape(self):
        return self.tape

    def get_head(self):
        return self.head

    def __str__(self):
        return str(self.tape)