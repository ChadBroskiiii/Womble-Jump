import socket,json,ast,pygame
from pygame import Vector2

localIP = "192.168.4.23"
localPort = 7680
bufferSize = 2048
msgFromServer = "Client Connected"
sentmessage = str.encode(msgFromServer)
UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
UDPServerSocket.bind((localIP, localPort))
print("UDP server on")
positions = {}

while(True):
    bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
    message = bytesAddressPair[0]
    address = bytesAddressPair[1]
    coordinates_ip = json.loads(message.decode())
    coordinates = Vector2(coordinates_ip.get("x"), coordinates_ip.get("y"))
    coordinates_dict = {"x": coordinates.x, "y": coordinates.y}
    print(positions)
    ip = coordinates_ip.get("ip")
    if positions.get(ip) == None:
        positions[ip] = coordinates_dict
    else:
        positions[ip] = coordinates_dict
    other_player_positions = {k: v for k, v in positions.items() if k != ip}
    other_player_messages = json.dumps(other_player_positions)

    UDPServerSocket.sendto(str.encode(other_player_messages), address)
