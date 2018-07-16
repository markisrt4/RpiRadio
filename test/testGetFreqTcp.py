import socket

# create an ipv4 (AF_INET) socket object using the tcp protocol (SOCK_STREAM)
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# connect the client
client.connect(('192.168.29.115', 7356))

# send some data (in this case a HTTP GET request)
client.send('f\n')

# receive the response data (4096 is recommended buffer size)
response = client.recv(128)

print response
