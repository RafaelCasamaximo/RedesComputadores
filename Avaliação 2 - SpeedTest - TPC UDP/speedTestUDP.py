# -*- coding: utf-8 -*-

from socket import *
import time
import random
import os
import select
from typing import Any
from progress.spinner import Spinner
from math import *


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
            ready = select.select([mySocket], [], [], 5)
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

        realPackageNumber = 0
        msg = ''
        while '\n' not in msg:
            ready = select.select([mySocket], [], [], 2)
            if ready[0]:
                msg, addr = mySocket.recvfrom(packageSize)
                msg = msg.decode('ascii')
                realPackageNumber = int(msg[msg.find('\n') + 1:])
        loss = realPackageNumber - packageNumber 
        mySocket.sendto(str(loss).encode('ascii'), addr)

        # Processamento dos valores
        downloadSpeedInBits = round((bytesNumber / 20) * 8, 2)
        downloadSpeedInPackages = round(packageNumber / 20, 2)

        print('\n---Resultados do Teste de Velocidade---')
        print("-Velocidade de Download: {:,}bps".format(downloadSpeedInBits))
        print(
            f'-Velocidade de Download: {downloadSpeedInPackages} pacotes por segundo')
        print(f'-Número de Bits: {bytesNumber}')
        print(f'-Pacotes Perdidos: {abs(loss)}\n')

        input('\nPressione uma tecla para voltar ao menu')

        mySocket.close()

        pass

    def uploadTest(self, mySocket: Any, port: str) -> None:

        message = msg = 'teste de rede *2022*' * 25

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
        
        aux = '\n' + str(packageNumber)
        mySocket.sendto(aux.encode('ascii'), addr)
        data, addr = mySocket.recvfrom(packageSize)
        loss = int(data.decode('ascii'))

        # Processamento dos valores
        uploadSpeedInBits = round((bytesNumber / 20) * 8, 2)
        uploadSpeedInPackages = round(packageNumber / 20, 2)

        print('\n\n---Resultados do Teste de Velocidade---')
        print("-Velocidade de Upload: {:,}bps".format(uploadSpeedInBits))
        print(
            f'-Velocidade de Upload: {uploadSpeedInPackages} pacotes por segundo')
        print(f'-Número de Bits: {bytesNumber}')
        print(f'-Pacotes Perdidos: {abs(loss)}')

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

# UDP:

# Download:
# -Velocidade de Download: 106,954,600.0bps
# -Velocidade de Download: 26738.65 pacotes por segundo
# -Número de Bits: 267386500
# -Pacotes Perdidos: 4322

# -Velocidade de Download: 106,476,200.0bps
# -Velocidade de Download: 26619.05 pacotes por segundo
# -Número de Bits: 266190500
# -Pacotes Perdidos: 3466

# -Velocidade de Download: 108,823,400.0bps
# -Velocidade de Download: 27205.85 pacotes por segundo
# -Número de Bits: 272058500
# -Pacotes Perdidos: 2623

# -Velocidade de Download: 108,066,000.0bps
# -Velocidade de Download: 27016.5 pacotes por segundo
# -Número de Bits: 270165000
# -Pacotes Perdidos: 1950

# Upload:
# -Velocidade de Upload: 107,819,000.0bps
# -Velocidade de Upload: 26954.75 pacotes por segundo
# -Número de Bits: 269547500
# -Pacotes Perdidos: 4322

# -Velocidade de Upload: 107,169,400.0bps
# -Velocidade de Upload: 26792.35 pacotes por segundo
# -Número de Bits: 267923500
# -Pacotes Perdidos: 3466

# -Velocidade de Upload: 109,348,000.0bps
# -Velocidade de Upload: 27337.0 pacotes por segundo
# -Número de Bits: 273370000
# -Pacotes Perdidos: 2623

# -Velocidade de Upload: 108,456,000.0bps
# -Velocidade de Upload: 27114.0 pacotes por segundo
# -Número de Bits: 271140000
# -Pacotes Perdidos: 1950