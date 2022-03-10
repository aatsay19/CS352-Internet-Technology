import socket, sys

args = sys.argv
listenPort = int(args[1])

try:
    ts = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("[TS2]: Server socket created")
except socket.error as err:
    print('socket open error: {}\n'.format(err))
    exit()

server_binding = ('', listenPort)
ts.bind(server_binding)
ts.listen(1)
host = socket.gethostname()
print("[TS2]: Server host name is {}".format(host))
localhost_ip = (socket.gethostbyname(host))
print("[TS2]: Server IP address is {}".format(localhost_ip))
rsockid, addr = ts.accept()
print ("[TS2]: Got a connection request from a client at {}".format(addr))

# Load DNS dictionary
lines = []
with open('PROJ2-DNSTS2.txt', 'r') as f:
    lines = f.readlines()
f.close()
db = {}
for line in lines:
    line.rstrip("\n\r")
    tkns = line.split()
    db[tkns[0]] = tkns[1]

# Receive message from the client.
while True:
    msg = rsockid.recv(200)
    msg = msg.decode('utf-8').rstrip("\n\r")
    if len(msg) == 0:
        # Close the server socket
        ts.close()
        exit()
    # Check if Domain Name exists on Server
    dn = msg.split()[0]
    contains = False
    for key in db.keys():
        if dn.lower() == key.lower():
            contains = True
            dn = key
    if contains:
        msg = dn + " " + db[dn] + " A IN\n"
        rsockid.sendall(msg.encode('utf-8'))
    