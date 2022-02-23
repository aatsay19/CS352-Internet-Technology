import socket, select

# Client Socket
try:
    ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("[S]: Server socket created")
except socket.error as err:
    print('socket open error: {}\n'.format(err))
    exit()
server_binding = ('', 50003)
ss.bind(server_binding)
ss.listen(1)
print("[S]: Server host name is {}".format(socket.gethostname()))
localhost_ip = (socket.gethostbyname(socket.gethostname()))
print("[S]: Server IP address is {}".format(localhost_ip))
csockid, addr = ss.accept()
print ("[S]: Got a connection request from a client at {}".format(addr))

# TS1 Socket
try:
    ts1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("[S]: TS1 socket created")
except socket.error as err:
    print('socket open error: {}\n'.format(err))
    exit()
server_binding = ('', 50009)
ts1.connect(server_binding)
# ts.settimeout(5)
print("[S]: TS1 host name is {}".format(socket.gethostname()))
localhost_ip = (socket.gethostbyname(socket.gethostname()))
print("[S]: TS1 IP address is {}".format(localhost_ip))

# TS2 Socket
try:
    ts2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("[S]: TS2 socket created")
except socket.error as err:
    print('socket open error: {}\n'.format(err))
    exit()
server_binding = ('', 50010)
ts2.connect(server_binding)
# ts.settimeout(5)
print("[S]: TS2 host name is {}".format(socket.gethostname()))
localhost_ip = (socket.gethostbyname(socket.gethostname()))
print("[S]: TS2 IP address is {}".format(localhost_ip))

# Receive message from the client + Send to TS1 and TS2
while True:
    msg = csockid.recv(200)
    if len(msg) == 0:
        # Close the server socket
        ss.close()
        exit()
    ts1.sendall(msg)
    ts2.sendall(msg)
    readers, _, _ = select.select([ts1, ts2], [], [], 5)
    for reader in readers:
        if reader is ts1:
            msg = ts1.recv(200)
            csockid.sendall(msg)
        elif reader is ts2:            
            msg = ts2.recv(200)
            csockid.sendall(msg)
    if not (readers):
        msg = msg.decode('utf8').rstrip("\n\r")
        msg += " - TIMED OUT\n"
        csockid.sendall(msg)