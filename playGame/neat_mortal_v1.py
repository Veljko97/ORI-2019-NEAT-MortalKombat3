import retro
import cv2
import numpy as np
import pickle
import neat

class work:
    def __init__(self):
        self.env = retro.make(game="MortalKombat3-Genesis", state="sub-zero-easy1")
        self.ww1 = 1
        self.flag = True
        config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                             neat.DefaultSpeciesSet, neat.DefaultStagnation,
                             'config-neat')

        p = neat.Population(config)

        w = p.run(self.eval_genomes)
        pickle.dump(w, open("sub-zero-winner3.bin", "wb"))

    def eval_genomes(self, genomes, config):
        imageArray = []
        gen_count = 0
        print("---------------------------------------------------------------------------------")
        if(not self.flag):
            print("Promena seta: 1")
            self.env.close()
            self.env = retro.make(game="MortalKombat3-Genesis", state="sub-zero-easy2")
            self.ww1 += 1
            self.flag = True
        else:
            print("Promena seta: 2")
            self.env.close()
            self.env = retro.make(game="MortalKombat3-Genesis", state="sub-zero-easy1")
            self.ww1 += 1
            self.flag = False
        for genome_id, genome in genomes:
            ob = self.env.reset()
            inx, iny, inc = self.env.observation_space.shape
            inx = int(inx/8)
            iny = int(iny/8)

            net = neat.nn.recurrent.RecurrentNetwork.create(genome,config)

            done = False
            frame = 0
            go = 0
            my_hp = 100
            en_hp = 100
            genome.fitness = 0
            while not done:

                if(frame > 4):
                    frame = 0
                    continue
                frame += 1
                ob = cv2.resize(ob,(inx,iny))
                ob = cv2.cvtColor(ob, cv2.COLOR_BGR2GRAY)
                ob = np.reshape(ob, (inx,iny))
                for x in ob:
                    for y in x:
                        imageArray.append(y)
                nnOut = net.activate(imageArray)

                ob, reward, done, info = self.env.step(nnOut)

                imageArray.clear()
                if(go == 0):
                    go += 1
                    en_hp = info["enemy_health"]
                    my_hp = info["health"]
                reward += en_hp - info["enemy_health"]
                reward -= my_hp - info["health"]
                en_hp = info["enemy_health"]
                my_hp = info["health"]
                if(info["matches_won"] == 1):
                    reward += 2500 * self.ww1
                    done = True
                if (info["enemy_matches_won"] == 1):
                    done = True

                genome.fitness += reward
            gen_count += 1
            print("-------------------")
            print("genome: ", gen_count)
            print("fitness final: ", genome.fitness)
            print("-------------------")

work()