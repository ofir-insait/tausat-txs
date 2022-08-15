#!/usr/bin/env python
import os
import socket

ip = "132.66.193.14"
port = 5005

# Create a UDP socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# Bind the socket to the port
server_address = (ip, port)
s.bind(server_address)
print("Do Ctrl+c to exit the program !!")

PACKET_LEN = 259

if not os.path.exists('packets'):
    os.mkdir('packets')

packet_num = 0
while True:
    print("####### Server is listening #######")
    data, address = s.recvfrom(PACKET_LEN)
    print(f"\n\n Server received: {str(len(data))} bytes\n\n")
    print(data)
    packet_num += 1
    packet_fname = f'packets/packet_{packet_num}.bin'
    with open(packet_fname, 'wb') as f:
        f.write(data)
