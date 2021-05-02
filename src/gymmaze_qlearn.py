import sys
import numpy as np
import math
import random
import time

import gym
import gym_maze


def simulate():

    # ogrenme ile ilgili parametreleri init et
    learning_rate = get_learning_rate(0)
    explore_rate = get_explore_rate(0)
    discount_factor = 0.99
    num_streaks = 0

    # labirenti render et
    env.render()

    for episode in range(NUM_EPISODES):

        # envi resetle (gym best practice)
        obv = env.reset()

        # init state'i
        state_0 = state_to_bucket(obv)
        total_reward = 0

        for t in range(MAX_T):

            # action sec
            action = select_action(state_0, explore_rate)

            # action'u yurut
            obv, reward, done, _ = env.step(action)

            # time.sleep(0.1)

            # sonucu gozlemle
            state = state_to_bucket(obv)
            total_reward += reward

            # sonuca gore Q table'i guncelle
            best_q = np.amax(q_table[state])
            q_table[state_0 + (action,)] += learning_rate * (reward +
                                                             discount_factor * (best_q) - q_table[state_0 + (action,)])

            # yeni state'i set et
            state_0 = state

            # Print data
            if DEBUG_MODE == 2:
                print("\nEpisode = %d" % episode)
                print("t = %d" % t)
                print("Action: %d" % action)
                print("State: %s" % str(state))
                print("Reward: %f" % reward)
                print("Best Q: %f" % best_q)
                print("Explore rate: %f" % explore_rate)
                print("Learning rate: %f" % learning_rate)
                print("Streaks: %d" % num_streaks)
                print("")

            # if t % 100 == 0:
            #     print(q_table)
                # sys.exit(0)

            elif DEBUG_MODE == 1:
                if done or t >= MAX_T - 1:
                    print("\nEpisode = %d" % episode)
                    print("t = %d" % t)
                    print("Explore rate: %f" % explore_rate)
                    print("Learning rate: %f" % learning_rate)
                    print("Streaks: %d" % num_streaks)
                    print("Total reward: %f" % total_reward)
                    print("")

            # labirenti render et
            if RENDER_MAZE:
                env.render()

            if env.is_game_over():
                sys.exit()

            if done:
                print("Episode %d finished after %f time steps with total reward = %f (streak %d)."
                      % (episode, t, total_reward, num_streaks))

                if t <= SOLVED_T:
                    num_streaks += 1
                else:
                    num_streaks = 0
                break

            elif t >= MAX_T - 1:
                print("Episode %d timed out at %d with total reward = %f."
                      % (episode, t, total_reward))

        # 120 kere pes pese labirent cozulurse tamamlanmis say
        if num_streaks > STREAK_TO_END:
            break

        # parametreleri episode degiskenine gore guncelle
        explore_rate = get_explore_rate(episode)
        learning_rate = get_learning_rate(episode)


def select_action(state, explore_rate):
    # rastgele action sec
    if random.random() < explore_rate:
        action = env.action_space.sample()
    # q degeri en yuksek action u sec
    else:
        action = int(np.argmax(q_table[state]))
    return action


def get_explore_rate(t):
    return max(MIN_EXPLORE_RATE, min(0.8, 1.0 - math.log10((t+1)/DECAY_FACTOR)))


def get_learning_rate(t):
    return max(MIN_LEARNING_RATE, min(0.8, 1.0 - math.log10((t+1)/DECAY_FACTOR)))


# gym state ini q_table indisine cevirme
def state_to_bucket(state):
    bucket_indice = []
    for i in range(len(state)):
        if state[i] <= STATE_BOUNDS[i][0]:
            bucket_index = 0
        elif state[i] >= STATE_BOUNDS[i][1]:
            bucket_index = NUM_BUCKETS[i] - 1
        else:
            # state sinirlarini bucket arrayine esle
            bound_width = STATE_BOUNDS[i][1] - STATE_BOUNDS[i][0]
            offset = (NUM_BUCKETS[i]-1)*STATE_BOUNDS[i][0]/bound_width
            scaling = (NUM_BUCKETS[i]-1)/bound_width
            bucket_index = int(round(scaling*state[i] - offset))
        bucket_indice.append(bucket_index)
    return tuple(bucket_indice)


if __name__ == "__main__":

    # maze environmentinin init edilmesi
    # env = gym.make("maze-random-10x10-plus-v0")
    env = gym.make("maze-sample-10x10-v0")

    '''
    GYM enviromenti ile ilgili sabitlerin tanimlanmasi
    '''
    # 10, 10 tuple, her bir kare icin ayrik stateler q table olusuturulurken kullanicilacak
    MAZE_SIZE = tuple((env.observation_space.high +
                      np.ones(env.observation_space.shape)).astype(int))
    NUM_BUCKETS = MAZE_SIZE  # her bir kare icin bir bucket

    # ayrik eylemlerin sayisi
    NUM_ACTIONS = env.action_space.n  # ["N", "S", "E", "W"]
    # Bounds for each discrete state
    # [(0, 9), (0, 9)] state sinirlari
    STATE_BOUNDS = list(zip(env.observation_space.low,
                        env.observation_space.high))

    '''
    Ogrenme ile ilgili sabitlerin tanimlanmasi
    '''
    MIN_EXPLORE_RATE = 0.001
    MIN_LEARNING_RATE = 0.2
    DECAY_FACTOR = np.prod(MAZE_SIZE, dtype=float) / 10.0

    '''
    Simulasyon ile ilgili sabitlerin tanimlanmasi
    '''
    NUM_EPISODES = 50000
    
    # episodun surecegi discrete zaman sayisi
    # episode time i bir episode bundan uzun suremez
    MAX_T = np.prod(MAZE_SIZE, dtype=int) * 100

    # simulasyonun bitmesi icin gerekli mukerrer hit sayisi
    STREAK_TO_END = 100  
    SOLVED_T = np.prod(MAZE_SIZE, dtype=int)
    DEBUG_MODE = 2
    RENDER_MAZE = True

    '''
    her bir state-action cifti icin q table olusturulmasi
    '''
    q_table = np.zeros(NUM_BUCKETS + (NUM_ACTIONS,), dtype=float)

    simulate()

    '''
    harita buyuklugune gore reward hesaplanmasi.

    if np.array_equal(self.maze_view.robot, self.maze_view.goal):
        reward = 1
        done = True
    else:
        reward = -0.1/(self.maze_size[0]*self.maze_size[1])
        done = False
    '''