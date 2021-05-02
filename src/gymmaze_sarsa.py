import gym
import gym_maze # kullanilmasada durmasi lazim envlerin register edilmesi icin

from time import sleep
from numpy import inf 


""" 
gym'in baslatildigi modul env detaylari icin gym_maze environmentina bakin
"""

if __name__ == "__main__":
    # print(gym.envs.registry.all())
    # env = gym.make("maze-random-10x10-plus-v0")
    env = gym.make("maze-sample-10x10-v0")
    # env = gym.make("maze-random-100x100-v0")
    print(env)
    
    # 20 episode, her episode 100 adim
    for i_episode in range(20):
        observation = env.reset()

        for t in range(100):
            env.render()
            print("observation: {}".format(observation))
            action = env.action_space.sample()

            observation, reward, done, info = env.step(action)
            print("reward: {}, ".format(reward))

            sleep(1)
            if done:
                print("Episode finished after {} timesteps".format(t+1))
                break
