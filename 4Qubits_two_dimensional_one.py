from qiskit import *
Adder = QuantumCircuit(5)
Adder.mct([0,1,2,3],4)
Adder.mct([0,1,2],3)
Adder.ccx(0,1,2)
Adder.cx(0,1)
A = Adder.to_gate()
type(A)
AddBlocker = QuantumCircuit(6)
AddBlocker.mct([0,1,2,3,4],5)
AddBlocker.cx(5,1)
AB = AddBlocker.to_gate() 
type(AB)
DecreaserBlocker = QuantumCircuit(6)
DecreaserBlocker.x(1)
DecreaserBlocker.x(2)
DecreaserBlocker.x(3)
DecreaserBlocker.x(4)
DecreaserBlocker.mct([0,2,3,4],5)
DecreaserBlocker.x(1)
DecreaserBlocker.x(2)
DecreaserBlocker.x(3)
DecreaserBlocker.x(4)
DecreaserBlocker.cx(5,1)
DecreaserBlocker.cx(5,2)
DB = DecreaserBlocker.to_gate()
type(DB)
Decreaser = QuantumCircuit(5)
Decreaser.cx(0,1)
Decreaser.ccx(0,1,2)
Decreaser.mct([0,1,2],3)
Decreaser.mct([0,1,2,3],4)
D = Decreaser.to_gate()
type(D)

q = QuantumRegister(13)
c = ClassicalRegister(8)
qc = QuantumCircuit(q, c)
qc.x(4)
qc.x(10)
for i in range(1):
    qc.rx(pi/2,q[0])
    qc.rx(pi/2,q[6])
    qc.rx(pi/2,q[12])
    qc.h(12)
    qc.ch(12,0)
    qc.append(AB,[0,1,2,3,4,5])
    qc.reset(5)
    qc.append(A,[0,1,2,3,4])
    qc.cx(12,0)
    qc.x(12)
    qc.ch(12,6)
    qc.append(DB,[0,1,2,3,4,5])
    qc.reset(5)
    qc.append(D,[0,1,2,3,4])
    qc.reset(0)
    qc.append(AB,[6,7,8,9,10,11])
    qc.reset(11)
    qc.append(A,[6,7,8,9,10])
    qc.cx(12,6)
    qc.append(DB,[6,7,8,9,10,11])
    qc.reset(11)
    qc.append(D,[6,7,8,9,10])
    qc.reset(6)
    qc.barrier()
    
qc.measure(q[1],c[0])
qc.measure(q[2],c[1])
qc.measure(q[3],c[2])
qc.measure(q[4],c[3])
qc.measure(q[7],c[4])
qc.measure(q[8],c[5])
qc.measure(q[9],c[6])
qc.measure(q[10],c[7])
qc.draw('mpl')
