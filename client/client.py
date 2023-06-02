import socket
import json


def cloak_state(state):
	key = json.load(open('client/key.json'))
	a = key['app_cats']
	u = key['ufs']
	c = key['contexts']

	cloaked_state = [a[state[0]], u[state[1]], c[state[2]]]
	
	return cloaked_state

def uncloak_action(action):
	key = json.load(open('client/key.json'))
	k = key['actions']

	return k.index(action)

settings = json.load(open('client/settings.json'))
app_cats = settings['a']
ufs = settings['u']
contexts = settings['c']
actions = settings['k']

host = 'localhost'
port = settings['p']
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))

print(s.recv(1024).decode())


while True:
	print("\nEnter state:")
	ip = input()
	if ip == 'q':
		s.send(ip.encode())
		s.close()
		break
	else:
		state = list(map(int, ip.split()))[:3]
		cloaked_state = cloak_state(state)
		idx = cloaked_state[0] * ufs * contexts + cloaked_state[1] * contexts + cloaked_state[2]
		print("State:", state)
		print("Cloaked state:", cloaked_state)
		print("Index:", idx)
		s.send(str(idx).encode())
		feedbackReq, action = list(map(int, s.recv(1024).decode().split())) 
		uncloaked_action = uncloak_action(action)
		print("Feedback required:", feedbackReq)
		print("Action:", action)
		print("Uncloaked action:", uncloaked_action)
		if feedbackReq:
			print("Feedback required")
			feedback = int(input())
			s.send(str(feedback).encode())