import socket   #TCP/IP Protocol #contém as funções necessárias para implementar sockets
import sys      #System calls and commands #Dados relacionadps ao diretório, funcções e métodos do sistema
import time     #Info about time and date

newSocket = socket.socket()
hostName = socket.gethostname()
serverIp = socket.gethostbyname(hostName)
port = 8080

#print(hostName)
#print(serverIp)

newSocket.bind((hostName, port))
print('Vinculação completa')
print('Seu IP é ', serverIp)

nickname = input('Insira seu nome: ')
newSocket.listen(1)

conn, add = newSocket.accept()
print('Conexão recebida de ', add[0])
print('Conexão estabelecida. Conectado de ', add[0])

client = (conn.recv(1024)).decode()
print(client + ' entrou no chat')
conn.send(nickname.encode())

while True:
    message = input('Me: ')
    conn.send(message.encode())
    message = conn.recv(1024)
    message = message.decode()
    print(client, ': ', message)