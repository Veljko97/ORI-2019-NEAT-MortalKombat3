import retro
import cv2
import numpy as np
import pickle
import neat

env = retro.make(game="MortalKombat3-Genesis", state="sub-zero-hard1", record='.')
# env = retro.make(game="MortalKombat3-Genesis")

w = pickle.load(open("sub-zero-winner6.bin", "rb"))
ob = env.reset()
inx, iny, inc = env.observation_space.shape
inx = int(inx/8)
iny = int(iny/8)
imageArray = []
frame = 0
done = False
config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                    neat.DefaultSpeciesSet, neat.DefaultStagnation,
                    'config-neat')
net = neat.nn.recurrent.RecurrentNetwork.create(w,config)
while not done:
    if (frame >= 5):
        # env.render()
        frame = 0
    frame += 1
    ob = cv2.resize(ob, (inx, iny))
    ob = cv2.cvtColor(ob, cv2.COLOR_BGR2GRAY)
    ob = np.reshape(ob, (inx, iny))

    # for x in ob:
    #     for y in x:
    #         imageArray.append(y)
    imageArray = ob.flatten()
    nnOut = net.activate(imageArray)

    ob, reword, done, info = env.step(nnOut)
