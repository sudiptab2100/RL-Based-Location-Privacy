import random
import pickle
import socket
import json


epsilon = 1
gamma = 0.1

settings = json.load(open('server/settings.json'))
app_cats = settings['a']
ufs = settings['u']
contexts = settings['c']
actions = settings['k']

host = 'localhost'
port = settings['p']

q_table = dict()

def create_q_table():
    global q_table, app_cats, ufs, contexts, actions

    for i in range(app_cats):
        for j in range(ufs):
            for k in range(contexts):
                idx = i * ufs * contexts + j * contexts + k
                q_table[idx] = [0] * actions

def reset_q_table():
    global q_table, epsilon, gamma
    create_q_table()
    epsilon = 1
    gamma = 0.1
    save_model()

def save_model():
    global q_table, epsilon, gamma
    with open('server/model.pickle', 'wb') as f:
        pickle.dump([q_table, epsilon, gamma], f)

def load_model():
    global q_table, epsilon, gamma
    with open('server/model.pickle', 'rb') as f:
        q_table, epsilon, gamma = pickle.load(f)

def get_action(state):
    global epsilon, q_table
    
    idx = state[0] * ufs * contexts + state[1] * contexts + state[2]
    feedbackReq = 1
    if random.random() < epsilon:
        return feedbackReq, random.randint(0, actions - 1)
    else:
        return (1 - feedbackReq), q_table[idx].index(max(q_table[idx]))

def getFeedback(state, action, reward):
    global gamma, q_table, epsilon
    if reward == 1:
        epsilon *= 0.9
    elif reward == 0:
        epsilon *= (1 / 0.9)
    if epsilon > 1: epsilon = 1
    idx = state[0] * ufs * contexts + state[1] * contexts + state[2]
    q_table[idx][action] += gamma * (reward - q_table[idx][action])
    save_model()


# reset_q_table()
load_model()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))
s.listen(1)

c, addr = s.accept()
print("CONNECTION FROM:", str(addr))
c.send(b"CONNECTED")

while True:
    print()
    msg = c.recv(1024).decode()
    if msg == 'q':
        break
    elif msg == '':
        continue
    else:
        idx = int(msg)
        print("idx:", idx)
        state = [idx // (ufs * contexts), (idx % (ufs * contexts)) // contexts, idx % contexts]
        print("state:", state)
        feedbackReq, action = get_action(state)

        response = str(feedbackReq) + " " + str(action)
        c.send(response.encode())
        print("feedbackReq:", feedbackReq)
        print("action:", action)

        if feedbackReq:
            feedback = c.recv(1024).decode()
            print("feedback:", feedback)
            getFeedback(state, action, int(feedback))
        
        print("actions:", q_table[idx])
        print("epsilon:", epsilon)

c.close()