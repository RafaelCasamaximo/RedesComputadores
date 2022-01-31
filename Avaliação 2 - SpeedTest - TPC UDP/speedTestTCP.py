# -*- coding: utf-8 -*-

from email import message
from socket import *
from threading import local
import time
import random
import os


class SpeedTesterTCP:
    def __init__(self) -> None:
        # Definição dos Socketes
        self.socket = socket()
        self.socket2 = socket()

        # Definição das Portas
        self.port = 55555
        self.port2 = 44444

        pass

    def __del__(self) -> None:
        print('Fechando Sockets')
        self.socket.close()
        self.socket2.close()
        print('Sockets Encerrados')
        pass

    def menu(self) -> None:

        onMenu = True

        while(onMenu):

            os.system('clear')

            print('---Speed Test TCP---')
            print('Insira o que você deseja testar:')
            print('   1 - Download')
            print('   2 - Upload')
            print('   3 - Sair')

            choice = int(input())

            if choice == 1:
                self.downloadTest()
            elif choice == 2:
                self.uploadTest()
            elif choice == 3:
                onMenu = False
                exit()
            else:
                print('Insira uma opção válida!')

        pass

    def downloadTest(self) -> None:

        packageSize = 500
        packageNumber = 0
        bytesNumber = 0

        hostname = gethostname()
        localIp = gethostbyname(hostname)

        print(f'Seu HostName é: {hostname}')
        print(f'Seu IP para conexão é: {localIp}')

        print('-Aguardando por conexão...')

        self.socket.bind(("", self.port))
        self.socket.listen()
        conn, addr = self.socket.accept()
        print('-Conexão estabelecida com sucesso!')

        startTime = time.time()
        while time.time() - startTime < 20:
            data = conn.recv(packageSize)
            if not data:
                print('-Ocorreu um erro durante a testagem!')
                print('-Não foi possível receber dados!')
                return

            # Atualiza os valores
            packageNumber += 1
            bytesNumber += len(data.decode('ascii'))

        # Processamento dos valores
        downloadSpeedInBytes = round((bytesNumber / 20) * 8, 2)
        downloadSpeedInPackages = round(packageNumber / 20, 2)

        print('---Resultados do Teste de Velocidade---')
        print(f'-Velocidade de Download: {downloadSpeedInBytes}bps')
        print(
            f'-Velocidade de Download: {downloadSpeedInPackages} pacotes por segundo')
        print(f'-Número de Bytes: {bytesNumber}')

        input()

        conn.close()

        pass

    def uploadTest(self) -> None:

        message = ''
        for i in range(500):
            message += chr(random.randint(48, 122))
        packageSize = 500
        packageNumber = 0
        bytesNumber = 0

        print('Informe o IP para o teste de upload: ')
        ip = input()
        self.socket2.connect((ip, self.port))
        print("Conexão estabelecida")

        startTime = time.time()
        while time.time() - startTime < 20:
            self.socket2.send(message.encode('ascii'))
            packageNumber += 1
            bytesNumber += packageSize

        pass
