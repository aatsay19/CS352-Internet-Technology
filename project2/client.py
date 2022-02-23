import socket, sys

args = sys.argv
hostname = (args[1])
listenPort = int(args[2])

try:
    cs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("[C]: Client socket created")
except socket.error as err:
    print('socket open error: {} \n'.format(err))
    exit()

# Connect to the server on local machine
server_binding = (hostname, listenPort)
cs.connect(server_binding)

# Reading from file and sending to server
lines = []
with open('PROJ2-HNS.txt', 'r') as inf:
    lines = inf.readlines()
inf.close()
outf = open("RESOLVED.txt", "w")
for line in lines:
    cs.sendall(line.encode('utf-8'))
    msg = cs.recv(200)
    msg = msg.decode('utf-8')
    outf.write(msg)

# close the client socket
cs.close()
exit()
