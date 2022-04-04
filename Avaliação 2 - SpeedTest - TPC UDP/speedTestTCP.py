# -*- coding: utf-8 -*-

from socket import *
import time
import random
import os
from typing import Any
from progress.spinner import Spinner


class SpeedTesterTCP:
    def __init__(self) -> None:
        # Definição dos Socketes
        self.mySocket = None
        self.mySocket2 = None

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

            print('---Speed Test TCP---')
            print('Insira o que você deseja testar:')
            print('   1 - Download')
            print('   2 - Upload')
            print('   3 - Âmbos')
            print('   4 - Sair')

            choice = int(input())

            self.mySocket = socket()
            self.mySocket2 = socket()

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

        hostname = gethostname()
        localIp = gethostbyname(hostname)

        print(f'Seu HostName é: {hostname}')

        s = socket(AF_INET, SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        print(f'Seu IP para conexão é: {s.getsockname()[0]}')
        s.close()

        print('-Aguardando por conexão...')

        mySocket.bind(("", port))
        mySocket.listen()
        conn, addr = mySocket.accept()
        print('-Conexão estabelecida com sucesso!')
        print('-Iniciando teste de rede. ')

        startTime = time.time()
        spinner = Spinner('Testando... ')
        while time.time() - startTime < 20:
            data = conn.recv(packageSize)
            if not data:
                print('-Ocorreu um erro durante a testagem!')
                print('-Não foi possível receber dados!')
                return

            # Atualiza os valores
            packageNumber += 1
            bytesNumber += len(data.decode('ascii'))
            spinner.next()

        # Responsável por receber o número real de pacotes transmitidos
        msg = ''
        while '\n' not in msg:
            data = conn.recv(20)
            msg = data.decode('ascii')
        realPackageNumber = int(msg[msg.find('\n') + 1:])
        loss = realPackageNumber - packageNumber

        lossNumberString = str(loss)

        # Envia de volta o valor da perda de pacotes que foi recebido e calculado
        conn.send(lossNumberString.encode('ascii'))
        
        # Processamento dos valores
        downloadSpeedInBits = round((bytesNumber / 20) * 8, 2)
        downloadSpeedInPackages = round(packageNumber / 20, 2)

        print('\n\n---Resultados do Teste de Velocidade---')
        print("-Velocidade de Download: {:,}bps".format(downloadSpeedInBits))
        print(
            f'-Velocidade de Download: {downloadSpeedInPackages} pacotes por segundo')
        print(f'-Número de Bits: {bytesNumber}')
        print(f'-Pacotes Perdidos: {abs(loss)}\n')

        input('\nPressione uma tecla para voltar ao menu')

        conn.close()

        pass

    def uploadTest(self, mySocket: Any, port: str) -> None:

        message = 'teste de rede *2022*' * 25
        packageSize = 500
        packageNumber = 0
        bytesNumber = 0

        print('Informe o IP para o teste de upload: ')
        ip = input()
        mySocket.connect((ip, port))
        print("-Conexão estabelecida com sucesso!")
        print("-Iniciando Teste de Rede. ")

        startTime = time.time()
        spinner = Spinner('Testando... ')
        while time.time() - startTime < 20:
            mySocket.send(message.encode('ascii'))
            packageNumber += 1
            bytesNumber += packageSize
            spinner.next()

        # Após o teste da internet o upload envia para o download
        # a quantidade de pacortes que foi enviado para ele poder
        # comparar com a quantidade de pacotes que chegou
        packageNumberString = '\n' + str(packageNumber)
        mySocket.send(packageNumberString.encode('ascii'))

        loss = int(mySocket.recv(20).decode('ascii'))

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


# TCP:

# Download:
# -Velocidade de Download: 167,552,200.0bps
# -Velocidade de Download: 41888.05 pacotes por segundo
# -Número de Bits: 418880500
# -Pacotes Perdidos: 8765

# -Velocidade de Download: 171,744,600.0bps
# -Velocidade de Download: 42936.15 pacotes por segundo
# -Número de Bits: 429361500
# -Pacotes Perdidos: 165

# -Velocidade de Download: 164,479,004.8bps
# -Velocidade de Download: 41201.2 pacotes por segundo
# -Número de Bits: 411197512
# -Pacotes Perdidos: 2427

# -Velocidade de Download: 163,199,200.0bps
# -Velocidade de Download: 40799.8 pacotes por segundo
# -Número de Bits: 407998000
# -Pacotes Perdidos: 899

# Upload:
# -Velocidade de Upload: 171,777,600.0bps
# -Velocidade de Upload: 42944.4 pacotes por segundo
# -Número de Bits: 429444000
# -Pacotes Perdidos: 165

# -Velocidade de Upload: 169,305,200.0bps
# -Velocidade de Upload: 42326.3 pacotes por segundo
# -Número de Bits: 423263000
# -Pacotes Perdidos: 8765

# -Velocidade de Upload: 165,290,200.0bps
# -Velocidade de Upload: 41322.55 pacotes por segundo
# -Número de Bits: 413225500
# -Pacotes Perdidos: 2427

# -Velocidade de Upload: 163,379,000.0bps
# -Velocidade de Upload: 40844.75 pacotes por segundo
# -Número de Bits: 408447500
# -Pacotes Perdidos: 899