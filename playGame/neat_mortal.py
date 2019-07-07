import retro
import cv2
import numpy as np
import pickle
import neat

class work:
    def __init__(self):
        self.game = "MortalKombat3-Genesis"
        self.states = ["sub-zero-mid1", "sub-zero-mid2", "sub-zero-hard1"]
        # self.states = ["sub-zero-easy1", "sub-zero-easy2", "sub-zero-mid2",
        #                "sub-zero-hard1"]
        # self.states = ["sub-zero-easy1", "sub-zero-easy2", "sub-zero-mid1", "sub-zero-mid2",
        #                "sub-zero-hard1", "sub-zero-hard2"]
        self.env = retro.make(game=self.game, state=self.states[0])
        self.ww1 = 1
        self.flag = True
        config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                             neat.DefaultSpeciesSet, neat.DefaultStagnation,
                             'config-neat')

        p = neat.Population(config)

        p.add_reporter(neat.StdOutReporter(True))
        stats = neat.StatisticsReporter()
        p.add_reporter(stats)
        # p.add_reporter(neat.Checkpointer(5))

        w = p.run(self.eval_genomes)

        pickle.dump(w, open("sub-zero-winner7.bin", "wb"))
        pickle.dump(stats, open("sub-zero-stats7.bin", "wb"))

    def eval_genomes(self, genomes, config):
        imageArray = []
        gen_count = 0
        print("---------------------------------------------------------------------------------")
        for genome_id, genome in genomes:
            self.ww1 = 0
            genome.fitness = 0
            for curr_state in self.states:
                self.env.close()
                self.env = retro.make(game=self.game, state=curr_state)
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
                start_me_won = 0
                start_en_won = 0
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
                        start_me_won = info["matches_won"]
                        start_en_won = info["enemy_matches_won"]

                    reward += en_hp - info["enemy_health"]
                    reward -= (my_hp - info["health"]) * 2
                    # reward -= my_hp - info["health"]
                    en_hp = info["enemy_health"]
                    my_hp = info["health"]
                    if(info["matches_won"] > start_me_won):
                        reward += 10000 / len(self.states)
                        done = True
                    if (info["enemy_matches_won"] > start_en_won):
                        done = True

                    genome.fitness += reward

            gen_count += 1
            print("-------------------")
            print("genome: ", gen_count)
            print("fitness final: ", genome.fitness)
            print("-------------------")


work()