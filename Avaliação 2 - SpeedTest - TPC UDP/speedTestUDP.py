# -*- coding: utf-8 -*-

from socket import *
import time
import random
import os
import select
from typing import Any
from progress.spinner import Spinner


class SpeedTesterUDP:
    def __init__(self) -> None:
        # Definição dos Socketes
        self.mySocket = None
        self.mySocket2 = None
        # mySocket.setblocking(False)
        # mySocket.setblocking(False)

        # Definição das Portas
        self.port = 55555
        self.port2 = 44444

        pass

    def __del__(self) -> None:
        print('Fechando Sockets')
        self.mySocket.close()
        self.mySocket2.close()
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
            print('   3 - Âmbos')
            print('   4 - Sair')

            choice = int(input())

            self.mySocket = socket(AF_INET, SOCK_DGRAM)
            self.mySocket2 = socket(AF_INET, SOCK_DGRAM)

            if choice == 1:
                self.downloadTest(self.mySocket, self.port)
            elif choice == 2:
                self.uploadTest(self.mySocket, self.port)
            elif choice == 3:
                self.both()
            elif choice == 4:
                onMenu = False
                exit()
            else:
                print('Insira uma opção válida!')

        pass

    def downloadTest(self, mySocket: Any, port: str) -> None:

        packageSize = 500
        packageNumber = 0
        bytesNumber = 0

        print('-Aguardando por conexão...')
        mySocket.bind(("", port))

        data, addr = mySocket.recvfrom(1)

        if data.decode('ascii') != '1':
            print('-Ocorreu um erro na conexão!')
            input()
            return

        print('-Conexão estabelecida com sucesso!')

        startTime = time.time()

        # Speed Test
        # Enquanto o tempo de testagem for menor que 20 segundos
        # with tqdm(total=20) as pbar:
        mySocket.setblocking(False)
        spinner = Spinner('Testando... ')
        while (time.time() - startTime) < 20:
            # Recebe dados
            ready = select.select([mySocket], [], [], 2)
            if ready[0]:
                data, addr = mySocket.recvfrom(packageSize)

            # Verifica se os dados chegaram
            if not data:
                print('-Ocorreu um erro durante a testagem!')
                print('-Não foi possível receber dados!')
                return

            # Atualiza os valores
            packageNumber += 1
            bytesNumber += len(data.decode('ascii'))
            spinner.next()

            # pbar.update(time.time() - startTime)

        # Processamento dos valores
        downloadSpeedInBytes = round((bytesNumber / 20) * 8, 2)
        downloadSpeedInPackages = round(packageNumber / 20, 2)
        lost = (packageSize * packageNumber - bytesNumber) / \
            (packageSize * packageNumber) * 100

        print('\n---Resultados do Teste de Velocidade---')
        print(f'-Velocidade de Download: {downloadSpeedInBytes}bps')
        print(
            f'-Velocidade de Download: {downloadSpeedInPackages} pacotes por segundo')
        print(f'-Número de Bytes: {bytesNumber}')
        print(f'-Taxa de perda: {lost}%\n')

        input('\nPressione uma tecla para voltar ao menu')

        mySocket.close()

        pass

    def uploadTest(self, mySocket: Any, port: str) -> None:

        message = ''

        for i in range(500):
            # Gera ascii aleatorios
            message += chr(random.randint(48, 122))

        print('Informe o IP para o teste de upload: ')
        ip = input()

        packageSize = 500
        packageNumber = 0
        bytesNumber = 0

        addr = (ip, port)

        mySocket.sendto('1'.encode('ascii'), addr)

        startTime = time.time()
        spinner = Spinner('Testando... ')
        while time.time() - startTime < 20:
            mySocket.sendto(message.encode('ascii'), addr)

            # Atualiza os Valores
            packageNumber += 1
            bytesNumber += packageSize
            spinner.next()

        # Processamento dos valores
        uploadSpeedInBytes = round((bytesNumber / 20) * 8, 2)
        uploadSpeedInPackages = round(packageNumber / 20, 2)

        print('\n\n---Resultados do Teste de Velocidade---')
        print(f'-Velocidade de Upload: {uploadSpeedInBytes}bps')
        print(
            f'-Velocidade de Upload: {uploadSpeedInPackages} pacotes por segundo')
        print(f'-Número de Bytes: {bytesNumber}')

        input('\nPressione uma tecla para voltar ao menu')

        mySocket.close()

        pass

    def both(self) -> None:

        print('\nVocê gostaria de começar pelo...')
        print('   1 - Download')
        print('   2 - Upload')
        print('   Outros - Sair')

        choice = int(input())

        if choice == 1:
            self.downloadTest(self.mySocket, self.port)
            self.uploadTest(self.mySocket2, self.port2)
            pass
        elif choice == 2:
            self.uploadTest(self.mySocket, self.port)
            self.downloadTest(self.mySocket2, self.port2)
            pass
        else:
            exit()
            pass

        pass
