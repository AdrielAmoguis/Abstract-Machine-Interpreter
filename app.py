"""
    Abstract Machine Interpreter
    CSC615M - Automata, Computability, and Formal Languages
    Sir Ryan Austin Fernandez

    Project by:
    @author Adriel Isaiah V. Amoguis
"""

# Dependency Imports
import sys
from PyQt6.QtWidgets import QApplication, QLabel, QWidget, QGridLayout, QTextEdit
from PyQt6.QtGui import QPixmap
from PyQt6 import QtCore

# Module Imports
from abstract_simulator import AbstractMachineSimulator
from abstract_grapher import graph_abstract_machine

# Main App
app = QApplication(sys.argv)

# Components
window = QWidget()
window.setWindowTitle("Abstract Machine Interpreter")
window.setGeometry(100, 100, 640, 480)

# Interactable Components
machine_description = QTextEdit()
machine_description.resize(600, 600)
machine_description.setText(""".LOGIC
A] SCAN RIGHT (0,A), (1,B), (#,accept)
B] SCAN LEFT (0,C), (1,reject)
C] SCAN RIGHT (1,A)""")
machine_graph = QLabel()
machine_graph.setPixmap(QPixmap("./sample.png").scaled(600, 600, aspectRatioMode=QtCore.Qt.AspectRatioMode.KeepAspectRatio, transformMode=QtCore.Qt.TransformationMode.SmoothTransformation))

# Layout Manager
layout = QGridLayout()

# Widgets
layout.addWidget(QLabel("Enter Machine Description below:"), 0, 0)
layout.addWidget(machine_description, 1, 0, 16, 8)
layout.addWidget(QLabel("Machine Graph:"), 0, 9)
layout.addWidget(machine_graph, 1, 9, 16, 16)

# Show Window
window.setLayout(layout)
window.show()

# Run Event Loop
sys.exit(app.exec())