# -*- coding: utf-8 -*-

from email import message
from socket import *
import time
import random
import os


class SpeedTesterUDP:
    def __init__(self) -> None:
        # Definição dos Socketes
        self.socket = socket(AF_INET, SOCK_DGRAM)
        self.socket2 = socket(AF_INET, SOCK_DGRAM)

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

            print('---Speed Test UDP---')
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

        print('-Aguardando por conexão...')
        self.socket.bind('', self.port)

        data, addr = self.socket.recvfrom(1)

        if data.decode('ascii') != 1:
            print('-Ocorreu um erro na conexão!')
            return

        print('-Conexão estabelecida com sucesso!')

        startTime = time.time()

        # Speed Test
        # Enquanto o tempo de testagem for menor que 20 segundos
        while time.time() - startTime < 20:
            # Recebe dados
            data, addr = self.socket.recvfrom(packageSize)

            # Verifica se os dados chegaram
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
        pass

    def uploadTest(self) -> None:

        message = ''

        for i in range(500):
            # Gera ascii aleatorios
            message += chr(random.randint(48, 122))

        print('Informe o IP para o teste de upload: ')
        ip = input()

        packageSize = 500
        packageNumber = 0
        bytesNumber = 0

        addr = (ip, self.port2)

        self.socket2.sendto('1'.encode('ascii'), addr)

        startTime = time.time()

        while time.time() - startTime < 20:
            self.socket2.sendto(message.encode('ascii'), addr)

            # Atualiza os Valores
            packageNumber += 1
            bytesNumber += packageSize

        # Processamento dos valores
        uploadSpeedInBytes = round((bytesNumber / 20) * 8, 2)
        uploadSpeedInPackages = round(packageNumber / 20, 2)

        print('---Resultados do Teste de Velocidade---')
        print(f'-Velocidade de Upload: {uploadSpeedInBytes}bps')
        print(
            f'-Velocidade de Upload: {uploadSpeedInPackages} pacotes por segundo')
        print(f'-Número de Bytes: {bytesNumber}')

        pass
