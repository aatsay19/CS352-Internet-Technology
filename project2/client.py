import time
import socket

try:
    cs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("[C]: Client socket created")
except socket.error as err:
    print('socket open error: {} \n'.format(err))
    exit()
    
# Define the port on which you want to connect to the server
port = 50007
localhost_addr = socket.gethostbyname(socket.gethostname())

# connect to the server on local machine
server_binding = (localhost_addr, port)
cs.connect(server_binding)

# Reading from file and sending to server
lines = []
with open('PROJ2-HNS.txt', 'r') as inf:
    lines = inf.readlines()
inf.close()
outf = open("RESOLVED.txt", "w")
for line in lines:
    cs.sendall(line.encode('utf-8'))
    time.sleep(1)
    msg = cs.recv(200)
    msg = msg.decode('utf-8') 
    outf.write(msg)

# close the client socket
cs.close()
exit()
