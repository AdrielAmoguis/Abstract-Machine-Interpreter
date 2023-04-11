# Abstract Machine Interpreter

Adriel Isaiah V. Amoguis | CSC615M - Automata, Formal Languages, Computability

Feature list:

-   Deterministic Finite Automata (DFA)
-   Implements DFA and Generalized Sequential Transducers
-   Implements Finite State Accepters
-   Implements Deterministic Pushdown Automata (PDA) with Stacks & Queues
-   Implements 1-D Tape Turing Machine (TM)

This implementation does not support non-determinism and 2-D Turing tapes.

## Installation

```bash
# Optionally, create a virtual environment with Conda
conda create -n abstract-machine-interpreter python=3.9
conda activate abstract-machine-interpreter

# Clone the repository
git clone https://github.com/AdrielAmoguis/Abstract-Machine-Interpreter.git

# Install the requirements
pip install -r requirements.txt
```

## Usage

1. Run the program

```bash
python app.py
```

### Machine Definition Language

As defined in the CSC615M Machine Project specifications.

```
<SOURCE_STATE_NAME>] COMMAND (<SYMBOL_1>,<DESTINATION_STATE_NAME_1>),
    (<SYMBOL_2>,<DESTINATION_STATE_NAME_2>),
    ...,
    (<SYMBOL_N>,<DESTINATION_STATE_NAME_N>)
```

### Sample Machines in the Supported Machine Definition Language (MDL)

```
.LOGIC

A] SCAN (a,B), (b,C)
B] SCAN (a,B), (b,accept)
C] SCAN (b,C), (a,accept)
```

```
.DATA

QUEUE Q1

.LOGIC

A] WRITE(Q1) (X,B)
B] SCAN (a,C), (b,D)
C] WRITE(Q1) (#,E)
D] WRITE(Q1) (#,H)
E] READ(Q1) (#,B), (X,F)
F] WRITE(Q1) (X,G)
G] WRITE(Q1) (X,E)
H] READ(Q1) (X,I)
I] SCAN (b,H), (#,J)
J] READ(Q1) (#,accept)
```

```
.DATA
STACK S1
STACK S2

.LOGIC
A] WRITE(S1) (#,B)
B] WRITE(S2) (#,C)
C] WRITE(S1) (X,D)
D] SCAN (a,E), (b,L)
E] READ(S1) (X,F), (#,H)
F] WRITE(S2) (X,G)
G] WRITE(S2) (X,E)
H] WRITE(S1) (#,I)
I] READ(S2) (X,J), (#,K)
J] WRITE(S1) (X,I)
K] WRITE(S2) (#,D)
L] READ(S1) (X,M)
M] SCAN (b,L), (#,N)
N] READ(S1) (#,O)
O] READ(S2) (#,accept)
```

```
.LOGIC

A] SCAN RIGHT (a,B), (b,A), (#,reject)
B] SCAN RIGHT (a,A), (b,B), (#,C)
C] SCAN LEFT (a,C), (#,accept), (b,D)
D] SCAN LEFT (a,D), (b,C), (#,reject)
```
