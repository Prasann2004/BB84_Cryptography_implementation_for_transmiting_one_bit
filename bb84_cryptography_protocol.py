from qiskit import QuantumCircuit, transpile, Aer

simulator = Aer.get_backend("aer_simulator")


#Compute a random bit to send
randomBitCircuit = QuantumCircuit(1,1)
randomBitCircuit.x(0)
randomBitCircuit.barrier()
randomBitCircuit.h(0)
randomBitCircuit.barrier()
randomBitCircuit.measure(0,0)

randomBitCompiledCircuit = transpile(randomBitCircuit, simulator)
job = simulator.run(randomBitCompiledCircuit, shots = 1)
result = job.result()
counts = result.get_counts(randomBitCompiledCircuit)
if("1" in counts.keys()):
    bitToSend = 1
else:
    bitToSend = 0
    
print("Bit to Send = " + str(bitToSend))
    
#Compute a random basis to use for sending
randomSendBasisCircuit = QuantumCircuit(1,1)
randomSendBasisCircuit.x(0)
randomSendBasisCircuit.barrier()
randomSendBasisCircuit.h(0)
randomSendBasisCircuit.barrier()
randomSendBasisCircuit.measure(0,0)

randomSendBasisCompiledCircuit = transpile(randomSendBasisCircuit, simulator)
job = simulator.run(randomSendBasisCompiledCircuit, shots = 1)
result = job.result()
counts = result.get_counts(randomSendBasisCompiledCircuit)
if("1" in counts.keys()):
    sendBasis = 1
else:
    sendBasis = 0
    
print("Send Basis = " + str(sendBasis))

#Compute a random basis to use for receiving
randomRecvBasisCircuit = QuantumCircuit(1,1)
randomRecvBasisCircuit.x(0)
randomRecvBasisCircuit.barrier()
randomRecvBasisCircuit.h(0)
randomRecvBasisCircuit.barrier()
randomRecvBasisCircuit.measure(0,0)

randomRecvBasisCompiledCircuit = transpile(randomRecvBasisCircuit, simulator)
job = simulator.run(randomRecvBasisCompiledCircuit, shots = 1)
result = job.result()
counts = result.get_counts(randomRecvBasisCompiledCircuit)
if("1" in counts.keys()):
    recvBasis = 1
else:
    recvBasis = 0
    
print("Receive Basis = " + str(recvBasis))

#Quantum Send
commCircuit = QuantumCircuit(1,1)
if(bitToSend==1):
    commCircuit.x(0) 
if(sendBasis==1):
    commCircuit.h(0) # Change the basis
    
#Quantum Receive
if(recvBasis==1):
    commCircuit.h(0) # HH = I. So this will reverse the earlier basis change
commCircuit.measure(0,0)


commCompiledCircuit = transpile(commCircuit, simulator)
job = simulator.run(commCompiledCircuit, shots = 1)
result = job.result()
counts = result.get_counts(commCompiledCircuit)

if("1" in counts.keys()):
    recvBit = 1
else:
    recvBit = 0
    
#If the basis are the same, the received bit should be the same as the sent bit
if(sendBasis==recvBasis):
    print("Sent Bit = "+str(bitToSend)+" Received Bit = "+str(recvBit))
else:
    print("Bit was lost because basis didn't match")
