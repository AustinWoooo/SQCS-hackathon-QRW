# SQCS-hackathon-Quantum-Random-Walk

## Description
Inspired by the phenomenon of random walk in macroscopic physics, this project attempts to imitate the motion and behavior of a quantum.
## The Issue
Quantum Random Walk (QRW) has been serving as an implementable and multi-used algorithm in quantum computing. While observing the feature of QRW, we are intrigued by the formulation of quantum circuits. This project is aiming to design quantum circuits being able to make qubits conduct QRW.It is expected that the ultimate result construct the fundamental formula of QRW quantum circuits.
## Our Magic Solution
The imitation of QRW started by a module of 1D QRW using 3 qubits with a number line, whose origin set in 4 (100 in binary), ends at 7, 1 while its maximum and minimum respectively. This module was established by circuits named Adder, Decreaser, and Blockers. Adder is a circuit making the value of the number line go right, while Decreaser does the opposite. Blocker stabilizes the change of value.
## How Do We Make It
* Step 1 : Quantum Random Walk on 1D Number Line
	>How does quantum walk on a line of 15 points? Where should it go when it walks to the ends? Will the possibilities of walking to any point be affected?
* Step 2 : Make the Quantum move randomly in 1 step, 2 steps
	>To get closer to the definition of QRW, we've made a way to execute and imitate the "jumping" of a quantum. The action includes both moving one digit and two digits.
* Step 3 ：From 1D Number Line QRW to 2D QRW
	>In inspiration of the Brownian motion, we decided to expand the QRW into two dimensions. The decision of walking on the x or y axis is involved before the main part of QRW.

