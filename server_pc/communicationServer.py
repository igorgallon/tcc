from receiveDataTraining import ReceiveDataTraining
from trainingNeuralNetwork import TrainingNeuralNetwork
from sendModel import SendModel

print("[SERVER] Creating connection...")
data = ReceiveDataTraining('')

print("[SERVER] Receiving data training...")
data.receive()

print("[SERVER] Training neural network...")
neuralnetwork = TrainingNeuralNetwork()
model = neuralnetwork.run()
neuralnetwork.save(model)

raspberryAddress = '192.168.0.104'
print("[SERVER] Sending Model and Weights to Raspberry in Address {}...".format(raspberryAddress))
send = SendModel(raspberryAddress)
send.send()
