from qiskit import *
Adder = QuantumCircuit(5)
Adder.mct([0,1,2,3],4)
Adder.mct([0,1,2],3)
Adder.ccx(0,1,2)
Adder.cx(0,1)
A = Adder.to_gate()
type(A)

AdderBlocker = QuantumCircuit(6)
AdderBlocker.mct([0,1,2,3,4],5)
AdderBlocker.cx(5,1)
AB = AdderBlocker.to_gate() 
type(AB)

DecreaserBlocker = QuantumCircuit(6)
DecreaserBlocker.x((1,2,3,4))
DecreaserBlocker.mct([0,2,3,4],5)
DecreaserBlocker.x((1,2,3,4))
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


DoubleAdder = QuantumCircuit(5)
DoubleAdder.mct([0,2,3],4)
DoubleAdder.ccx(0,2,3)
DoubleAdder.cx(0,2)
DA = DoubleAdder.to_gate()
type(DA)
                   
DoubleAdderBlocker = QuantumCircuit(6)
DoubleAdderBlocker.mct([0,2,3,4],5)
DoubleAdderBlocker.cx(5,2)
DAB = DoubleAdderBlocker.to_gate()
type(DAB)
                   
DoubleDecreaser = QuantumCircuit(5)
DoubleDecreaser.cx(0,2)
DoubleDecreaser.ccx(0,2,3)
DoubleDecreaser.mct([0,2,3],4)
DD = DoubleDecreaser.to_gate()
type(DD)
                   
DoubleDecreaserBlocker = QuantumCircuit(7)
DoubleDecreaserBlocker.x((1,3,4))
DoubleDecreaserBlocker.mct([0,1,2,3,4],5)
DoubleDecreaserBlocker.x((1,2))
DoubleDecreaserBlocker.mct([0,1,2,3,4],6)
DoubleDecreaserBlocker.x((2,3,4))
DoubleDecreaserBlocker.cx(5,2)
DoubleDecreaserBlocker.cx(5,3)
DoubleDecreaserBlocker.cx(6,2)
DDB = DoubleDecreaserBlocker.to_gate()
type(DDB)

q = QuantumRegister(16)
c = ClassicalRegister(8)
qc = QuantumCircuit(q, c)
qc.x(4)
qc.x(11)
for i in range(1):
    qc.rx(pi/2,q[0])
    qc.rx(pi/2,q[7])
    qc.rx(pi/2,q[14])
    qc.rx(pi/2,q[15])
    qc.h(14)
    qc.h(15)
    qc.ch(14,0)
    qc.ch(15,0)
    qc.append(AB,[0,1,2,3,4,5])
    qc.reset(5)
    qc.append(A,[0,1,2,3,4])
    qc.cx(14,0)
    qc.append(DB,[0,1,2,3,4,5])
    qc.reset(5)
    qc.append(D,[0,1,2,3,4])
    qc.cx(15,0)
    qc.x(15)
    qc.rx(pi/2,q[0])
    qc.ch(15,0)
    qc.append(DAB,[0,1,2,3,4,5])
    qc.reset(5)
    qc.append(DA,[0,1,2,3,4])
    qc.cx(15,0)
    qc.append(DDB,[0,1,2,3,4,5,6])
    qc.reset(6)
    qc.append(DD,[0,1,2,3,4])
    qc.reset(0)
    qc.barrier()
    qc.x(14)
    qc.reset(15)
    qc.ch(14,7)
    qc.ch(15,7)
    qc.append(AB,[7,8,9,10,11,12])
    qc.reset(12)
    qc.append(A,[7,8,9,10,11])
    qc.cx(14,7)
    qc.append(DB,[7,8,9,10,11,12])
    qc.reset(12)
    qc.append(D,[7,8,9,10,11])
    qc.cx(15,7)
    qc.x(15)
    qc.rx(pi/2,q[7])
    qc.ch(15,7)
    qc.append(DAB,[7,8,9,10,11,12])
    qc.reset(12)
    qc.append(DA,[7,8,9,10,11])
    qc.cx(15,7)
    qc.append(DDB,[7,8,9,10,11,12,13])
    qc.reset(13)
    qc.append(DD,[7,8,9,10,11])
    qc.reset(7)
    qc.barrier()
    
qc.measure(q[1],c[0])
qc.measure(q[2],c[1])
qc.measure(q[3],c[2])
qc.measure(q[4],c[3])
qc.measure(q[8],c[4])
qc.measure(q[9],c[5])
qc.measure(q[10],c[6])
qc.measure(q[11],c[7])
qc.draw('mpl')
