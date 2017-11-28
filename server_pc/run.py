from trainingNeuralNetwork import TrainingNeuralNetwork

neuralnetwork = TrainingNeuralNetwork()

strMsg = input("Train? [y/n]")

while strMsg == "y":
    model = neuralnetwork.run()
    strMsg = input("Train? [y/n]")
    