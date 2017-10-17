from receiveDataTraining import ReceiveDataTraining
from trainingNeuralNetwork import TrainingNeuralNetwork
from sendModel import SendModel

print("[SERVER] Creating connection...")
data = ReceiveDataTraining('')

print("[SERVER] Receiving data training...")
data.receive()

print("[SERVER] Training neural network...")
#neuralnetwork = TrainingNeuralNetwork()
#model = neuralnetwork.run()
#neuralnetwork.save(model)

print("[SERVER] Sending Model and Weights to Raspberry...")
