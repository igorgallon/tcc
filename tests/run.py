from training import TrainingNeuralNetwork


n = 20
acc = 0
ntest = 8

nodes = [1152, 768, 576, 384, 288, 256, 192, 144]

tr = TrainingNeuralNetwork()

for t in range(0,ntest):
    
    with open("result"+ str(t+1) +".txt", "w") as file:
        print("Init")
        for i in range(0,n):
            acc = tr.run(nodes[t])
            file.write(str(acc)+"\n")
            print("RESULT OF RUN {} using size {} --- accuracy {}".format(i+1, nodes[t], acc))
        
        print("End!")