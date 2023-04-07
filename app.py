"""
    Abstract Machine Interpreter
    CSC615M - Automata, Computability, and Formal Languages
    Sir Ryan Austin Fernandez

    Project by:
    @author Adriel Isaiah V. Amoguis
"""

# Dependency Imports
import sys, os, time
from PyQt6.QtWidgets import QApplication, QLabel, QWidget, QGridLayout, QPlainTextEdit, QLineEdit, QGroupBox, QFormLayout, QPushButton, QLayout
from PyQt6.QtGui import QPixmap, QFontDatabase
from PyQt6 import QtCore

# Module Imports
from input_parser import InputParser
from abstract_simulator import AbstractMachineSimulator
from abstract_grapher import graph_abstract_machine

# Main App
app = QApplication(sys.argv)

# Components
window = QWidget()
window.setWindowTitle("Abstract Machine Interpreter")
window.setGeometry(100, 100, 640, 480)

# Handler Functions
def log(message):
    output_console.appendPlainText(message)

machine_instance = None

def update_memory_inspector():
    global machine_instance
    global memory_inspector
    try:
        memory_inspector.clear()

        # Input Tape
        memory_inspector.appendPlainText("Input Tape: " + str(machine_instance.input_tape))
        memory_inspector.appendPlainText("Tape Head:  " + str(" " * machine_instance.input_tape.head) + " ^")
        memory_inspector.appendPlainText("")

        if len(machine_instance.memory.keys()) < 1:
            memory_inspector.appendPlainText("No auxiliary memory used.")
        for key in machine_instance.memory.keys():
            memory_inspector.appendPlainText(str(machine_instance.aux_data[key]["type"]) + " " + key + ": " + str(machine_instance.memory[key]))

        memory_inspector.appendPlainText("")

        # Output Tape
        out = "".join(machine_instance.output)
        memory_inspector.appendPlainText("Output Buffer: " + out)
        memory_inspector.appendPlainText("")

        # Machine States
        memory_inspector.appendPlainText("Halted State: " + str(machine_instance.halted))
        memory_inspector.appendPlainText("Accept State: " + str(machine_instance.accepted))
        
    except Exception as e:
        log("Error: " + str(e))

def compile_machine():
    global machine_instance

    # Clear the output log
    output_console.clear()

    try:
        parser = InputParser(machine_description.toPlainText())
        machine_instance = AbstractMachineSimulator(parser.parse())
        graph_abstract_machine(machine_instance.logic)
        machine_graph.setPixmap(QPixmap("./graph_abstract_machine.png").scaled(600, 600, aspectRatioMode=QtCore.Qt.AspectRatioMode.KeepAspectRatio, transformMode=QtCore.Qt.TransformationMode.SmoothTransformation))
        os.remove("./graph_abstract_machine.png")
        btn_step_machine.setDisabled(False)
        btn_slow_run.setDisabled(False)
        btn_run_machine.setDisabled(False)
        log("Machine Compiled Successfully.")

        # Check if aux memory has a tape
        is_turing_machine = False
        for key in machine_instance.aux_data.keys():
            if machine_instance.aux_data[key]["type"] == "TAPE":
                is_turing_machine = True
                break
        machine_instance.set_input_tape(input_tape.text(), is_turing_machine=is_turing_machine)
        log("Turing machine detected. Input tape set to first aux memory tape.")

        log("Using input tape: " + str(machine_instance.input_tape))

        update_memory_inspector()

    except Exception as e:
        log("Error: " + str(e))

def step_machine():
    global machine_instance
    try:
        # Check if machine is halted
        if machine_instance.halted:
            log("Machine is halted.")
            return

        machine_instance.step()
        log("Machine stepped successfully.")
        update_memory_inspector()
    except Exception as e:
        log("Error: " + str(e))

def run_machine():
    global machine_instance
    try:
        # Check if machine is halted
        if machine_instance.halted:
            log("Machine is halted.")
            return
        
        machine_instance.run()
        log("Machine ran successfully.")
        update_memory_inspector()
    except Exception as e:
        log("Error: " + str(e))

def slow_run_machine():
    global machine_instance
    try:
        while True:
            # Check if machine is halted
            if machine_instance.halted:
                log("Machine is halted.")
                return

            machine_instance.step()
            log("Machine step successfully.")
            update_memory_inspector()
            time.sleep(1)
    except Exception as e:
        log("Error: " + str(e))

# Interactable Components
machine_description = QPlainTextEdit()
machine_description.resize(600, 1000)
machine_description.setPlainText("""// This is a comment.
.LOGIC
A] SCAN RIGHT (0,A), (1,B), (#,accept)
B] SCAN LEFT (0,C), (1,reject)
C] SCAN RIGHT (1,A)""")
monospaced_font = QFontDatabase.systemFont(QFontDatabase.SystemFont.FixedFont)
monospaced_font.setPointSize(12)
machine_description.setFont(monospaced_font)
machine_description.setLineWrapMode(QPlainTextEdit.LineWrapMode.NoWrap)
execution_panel = QGroupBox("Execution Panel")
input_tape = QLineEdit()
input_tape.setPlaceholderText("#aaabbbccc12344321#")
input_tape.setText("##")
monospaced_font2 = QFontDatabase.systemFont(QFontDatabase.SystemFont.FixedFont)
monospaced_font2.setPointSize(18)
input_tape.setFont(monospaced_font2)
btn_compile_machine = QPushButton("Compile / Reset Machine")
btn_compile_machine.clicked.connect(compile_machine)
btn_step_machine = QPushButton("Step Machine")
btn_step_machine.clicked.connect(step_machine)
btn_slow_run = QPushButton("Slowly Run Machine")
btn_slow_run.clicked.connect(slow_run_machine)
btn_run_machine = QPushButton("Run Machine")
btn_run_machine.clicked.connect(run_machine)
btn_step_machine.setDisabled(True)
btn_slow_run.setDisabled(True)
btn_run_machine.setDisabled(True)
execution_panel_layout = QFormLayout()
execution_panel_layout.addRow(QLabel("Input Tape:"), input_tape)
execution_panel_layout.addRow(btn_compile_machine)
execution_panel_layout.addRow(btn_step_machine)
execution_panel_layout.addRow(btn_slow_run)
execution_panel_layout.addRow(btn_run_machine)
execution_panel_layout.setSizeConstraint(QLayout.SizeConstraint.SetNoConstraint)
execution_panel.setLayout(execution_panel_layout)
machine_graph = QLabel()
machine_graph.setPixmap(QPixmap("./sample.png").scaled(600, 600, aspectRatioMode=QtCore.Qt.AspectRatioMode.KeepAspectRatio, transformMode=QtCore.Qt.TransformationMode.SmoothTransformation))
output_console = QPlainTextEdit()
output_console.setReadOnly(True)
output_console.setLineWrapMode(QPlainTextEdit.LineWrapMode.NoWrap)
output_console.setFont(monospaced_font)
output_console.setPlainText("""Abstract Machine Interpreter by Adriel Isaiah Amoguis (v1)
Compile a machine to get started.""")
memory_inspector = QPlainTextEdit()
memory_inspector.setReadOnly(True)
memory_inspector.setLineWrapMode(QPlainTextEdit.LineWrapMode.NoWrap)
memory_inspector.setFont(monospaced_font)

# Layout Manager
layout = QGridLayout()

# Widgets
layout.addWidget(QLabel("Enter Machine Description below:"), 0, 0)
layout.addWidget(machine_description, 1, 0, 7, 12)
layout.addWidget(execution_panel, 8, 0, 8, 12)
layout.addWidget(QLabel("Machine Graph:"), 0, 13)
layout.addWidget(machine_graph, 1, 13, 15, 16)
layout.addWidget(QLabel("Output Console:"), 17, 0)
layout.addWidget(output_console, 18, 0, 20, 16)
layout.addWidget(QLabel("Memory Inspector:"), 17, 17)
layout.addWidget(memory_inspector, 18, 17, 20, 20)

# Show Window
window.setLayout(layout)
window.show()

# Run Event Loop
sys.exit(app.exec())