import socket
import sys
import time

socketServer = socket.socket()
serverHost = socket.gethostname()
ip = socket.gethostbyname(serverHost)
serverPort = 8080

print('Seu IP é ', ip)
serverHost = input('IP do servidor: ')
nickname = input('Insira seu nome: ')
socketServer.connect((serverHost, serverPort))

socketServer.send(nickname.encode())
serverName = socketServer.recv(1024)
serverName = serverName.decode()

print(serverName + ' entrou no chat')
while True:
    message = (socketServer.recv(1024)).decode()
    print(serverName, ': ', message)
    message = input('Me: ')
    socketServer.send(message.encode())