import socket
import json

localIP = "127.0.0.1"
localPort = 20001
bufferSize = 1024
msgFromServer = "Client Connected"
sentmessage = str.encode(msgFromServer)
UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
UDPServerSocket.bind((localIP, localPort))
print("UDP server up and listening")
positions = {}

while(True):
    bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
    message = bytesAddressPair[0]
    address = bytesAddressPair[1]
    address_str = str(address)
    if address not in positions:
        positions[address] = {"x": 0, "y": 0}

    coordinates = json.loads(message.decode())
    positions[address_str] = coordinates
    other_player_positions = {k: v for k, v in positions.items() if k != address_str}
    other_player_messages = json.dumps(other_player_positions)

    UDPServerSocket.sendto(str.encode(other_player_messages), address)
