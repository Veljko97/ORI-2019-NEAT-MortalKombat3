import retro
import cv2
import neat_mortal
# env = retro.make("MortalKombat3-Genesis")
# ac = env.action_space.sample()
# ob = env.reset()
# done = False
# t= 0
# while not done:

    # ac = env.action_space.sample()
    # t+= 1
    # if(t == 4):
    #     a = input("ac: ")
    #     t = 0
    #     if(a == "1"):
    #         ac = [0, 0, 0, 0, 0, 0, 0, 0, 1]
    #     elif (a == "2"):
    #         ac = [0, 0, 0, 0, 0, 0, 0, 1, 0]
    #     elif (a == "3"):
    #         ac = [0, 0, 0, 0, 0, 0, 1, 0, 0]
    #     elif (a == "4"):
    #         ac = [0, 0, 0, 0, 0, 1, 0, 0, 0]
    #     elif (a == "5"):
    #         ac = [0, 0, 0, 0, 1, 0, 0, 0, 0]
    #     elif (a == "6"):
    #         ac = [0, 0, 0, 1, 0, 0, 0, 0, 0]
    #     elif (a == "7"):
    #         ac = [0, 0, 1, 0, 0, 0, 0, 0, 0]
    #     elif (a == "8"):
    #         ac = [0, 1, 0, 0, 0, 0, 0, 0, 0]
    #     elif (a == "9"):
    #         ac = [1, 0, 0, 0, 0, 0, 0, 0, 0]
    #     else:
    #         ac = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    # ob, rew, done, info = env.step(ac)
    # print("reword", rew)
    # print("Info", info)
    # env.render()