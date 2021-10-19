from qiskit import *
Hubert = QuantumCircuit(4)
Hubert.mct([0,1,2],3)
Hubert.ccx(0,1,2)
Hubert.cx(0,1) 
adder = Hubert.to_gate()
type(adder)
PCR = QuantumCircuit(4)
PCR.cx(0,1) 
PCR.ccx(0,1,2)
PCR.mct([0,1,2],3)
decrease = PCR.to_gate()
type(decrease)
q = QuantumRegister(4)
c = ClassicalRegister(2)
qc = QuantumCircuit(q, c)
qc.h(0)
qc.append(p1, [0,1,2,3])
qc.x(0)
qc.append(p2, [0,1,2,3])
qc.draw('mpl')
