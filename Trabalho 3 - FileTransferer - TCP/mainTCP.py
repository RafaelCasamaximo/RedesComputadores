# -*- coding: utf-8 -*-

import socket
import os
import time

class FileTransferer:
    def __init__(self, host_ip, host_port, local_ip, local_port):
        # settings of the file
        self.separator = "SEPARATOR"
        self.buffer_size = 1024

        # ip and port settings
        self.host_ip = host_ip
        self.host_port = host_port
        self.local_ip = local_ip
        self.local_ip = local_port

        self.conn_socket = socket.socket()

    def start(self):
        # menu 
        while True:
            print("hi, welcome!".center(50))
            print("before start, we need some infos\n". center(50))
            self.local_ip = input("> your ip: ")
            self.local_port = int(input("> your port: "))
            self.host_ip = input("> your friend's ip: ")
            self.host_port = int(input("> your friend's port: "))
            # self.local_ip = '10.0.0.137'
            # self.local_port = 55555
            # self.host_ip = '10.0.0.137'
            # self.host_port = 55555
            while True:
                self.buffer_size = int(input("> buffer size (500/1000/1500 bytes): "))
                if (self.buffer_size == 500) or (self.buffer_size == 1000) or (self.buffer_size == 1500):
                    break
                print("please, enter a 500, 1000 or 1500 bytes buffer size".center(50))
            os.system('cls||clear')

            while True:
                print("************************************************")
                print("configuration".center(50))
                print("your ip: ", self.local_ip)
                print("your port: ", self.local_port)
                print("friend's ip: ", self.host_ip)
                print("friend's port: ", self.host_port)
                print("buffer size chosen: ", self.buffer_size)
                print("************************************************")
                print("█▄─▀█▀─▄█▄─▄▄─█▄─▀█▄─▄█▄─██─▄█".center(50))
                print("██─█▄█─███─▄█▀██─█▄▀─███─██─██".center(50))
                print("▀▄▄▄▀▄▄▄▀▄▄▄▄▄▀▄▄▄▀▀▄▄▀▀▄▄▄▄▀▀".center(50))
                print(" ██░▀██████████████▀░██".center(50))
                print(" █▌▒▒░████████████░▒▒▐█".center(50))
                print(" █░▒▒▒░██████████░▒▒▒░█".center(50))
                print(" ▌░▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒░▐".center(50))
                print(" ░▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒░".center(50))
                print("███▀▀▀██▄▒▒▒▒▒▒▒▄██▀▀▀██".center(50))
                print("██░░░▐█░▀█▒▒▒▒▒█▀░█▌░░░█".center(50))
                print("▐▌░░░▐▄▌░▐▌▒▒▒▐▌░▐▄▌░░▐▌".center(50))
                print("              █░░░▐█▌░░▌▒▒▒▐░░▐█▌░░█ > 1. send a file".center(50))
                print(" ▒▀▄▄▄█▄▄▄▌░▄░▐▄▄▄█▄▄▀▒".center(50))
                print("              ░░░░░░░░░░└┴┘░░░░░░░░░ > 2. receive a file".center(50))
                print(" ██▄▄░░░░░░░░░░░░░░▄▄██".center(50))
                print("              ████████▒▒▒▒▒▒████████ > 3. back to welcome page".center(50)) 
                print(" █▀░░███▒▒░░▒░░▒▀██████".center(50))
                print("          █▒░███▒▒╖░░╥░░╓▒▐█████ > 4. exit".center(50))
                print(" █▒░▀▀▀░░║░░║░░║░░█████".center(50))
                print(" ██▄▄▄▄▀▀┴┴╚╧╧╝╧╧╝┴┴███".center(50))
                print(" ██████████████████████".center(50))

                while True:
                    op = int(input("\nenter your option: "))
                    if op == 1:
                        # Chamar função pra enviar um arquivo
                        # Essa função conecta em um ip:port e envia o arquivo
                        print("note: file needs to exist in the current directory or you can use an absolute path to that file somewhere on your computer.".center(150))
                        filepath = input("please, enter the path of the file you want to send path: ")
                        self.sendFile(filepath)
                        yn = input("\nDo you want continue? [y/n]: ")
                        if (yn == 'y') or (yn == 'Y'):
                            os.system('cls||clear')
                            break
                        exit()
                    if op == 2:
                        # Chamar função pra receber um arquivo
                        # Essa função permite que conectem no seu ip:port e enviem o arquivo
                        self.receiveFile()
                        yn = input("\nDo you want continue? [y/n]: ")
                        if (yn == 'y') or (yn == 'Y'):
                            os.system('cls||clear')
                            break
                        exit()
                    if op == 3:
                        break
                    if op == 4:
                        print("this is not a goodbye, it's a 'see you soon'!".center(50))
                        time.sleep(3)
                        os.system('cls||clear')
                        exit()
                    else:
                        print("enter a valid option!")
                if op == 3:
                    os.system('cls||clear')
                    break
        
    # this function checks if the file exists. If don't, return
    # it sends the file to the other side
    # tqdm is a aux lib to make a progress bar appear in the terminal
    # the bandwidth is defined in the class attributes (self.buffer_size)
    def sendFile(self, filepath):
        # checks if the file exist
        if not os.path.exists(filepath):
            print('inserted file does not exist!')
            return

        # fets the filesize
        filesize = os.path.getsize(filepath)

        # tries to connect with the sender ip:port
        print(f"connecting to {self.host_ip}:{self.host_port}")
        try:
            self.conn_socket.connect((self.host_ip, self.host_port))
        except:
            print("ERROR! Connection FAILED!")
            print("Check the ip:port and make sure that the reciever is running and listening!")
            return
        print("connected!")

        # sends the file name and the size of the file
        self.conn_socket.send(str(os.path.basename(filepath)).encode('ascii'))
        time.sleep(0.5)
        self.conn_socket.send(str(filesize).encode('ascii'))
        time.sleep(0.5)
        # self.conn_socket.send(f"{filepath}{self.separator}{filesize}".encode('ascii'))
        # sends the selected file
        # progress = tqdm.tqdm(range(filesize), f"Sending {filepath}", unit="B", unit_scale=True, unit_divisor=1024)
        # opens the file as a binary
        with open(filepath, "rb") as f:
            start = time.time()
            while True:
                # read the bytes (size of buffer_size) from the file
                bytes_read = f.read(self.buffer_size)
                # checks if the file is done
                if not bytes_read:
                    # file transmitting is done
                    break
                # we use sendall to assure transmission in busy networks
                self.conn_socket.sendall(bytes_read)
                # update the progress bar
                # progress.update(len(bytes_read))
            # send a send confirmation message
            # self.clientSender_socket.send(b'File was send.').encode()
            print(f"Tempo de Upload: {round(time.time() - start, 6)}s")
            print("Tamanho do arquivo: ", f.tell(), " bytes")
            print("Numero de pacotes: ", f.tell() // self.buffer_size + 1)
        # close the client sender socket
        self.conn_socket.close()
        print("done! file was sent.")

    def receiveFile(self):
        # accept connection if there is any
        print(f"listening as {self.local_ip}:{self.local_port}")
        self.conn_socket.bind(("", self.local_port))
        self.conn_socket.listen()
        client_sender, clientAddress_sender = self.conn_socket.accept() # posso usar clientSender_socket aqui?

        # while True:
        #     print(f"{clientAddress_sender} wants connect to you.")
        #     yn = input(("accept [y], decline [n]: "))
        #     if (yn == 'n') or (yn == 'N'):
        #         self.conn_socket.shutdown(socket.SHUT_RD)
        #         self.conn_socket.close()
        #     else:
        #         break
        print(f"{clientAddress_sender} is connected!")

        # receive the file infos
        # receive using client sender socket, not client receiver socket
        filepath = client_sender.recv(1024).decode('ascii')
        filesize = int(client_sender.recv(5).decode('ascii'))
        # progress = tqdm.tqdm(range(filesize), f"Receiving {filename}", unit="B", unit_scale=True, unit_divisor=1024)
        f = open(filepath, "wb")
        start = time.time()
        while True:
            # read the bytes (size of buffer_size) from the socket (receive)
            bytes_read = client_sender.recv(self.buffer_size)
            if not bytes_read:    
                # file transmitting is done
                break
            # write to the file the bytes we just received
            f.write(bytes_read)
        # update the progress bar
        # progress.update(len(bytes_read))
        # send a receive confirmation message
        # self.clientReceiver_socket.send(b'File was received!').encode() 
        print(f"Tempo de Download: {round(time.time() - start, 6)}s")
        print("Tamanho do arquivo:", f.tell(), "bytes")
        print("Numero de pacotes: ", f.tell() // self.buffer_size + 1)
        f.close()
        # close the client sender socket
        client_sender.close()
        # close the client receiver socket
        self.conn_socket.close()
        print("done! file was received.")


fileTransferer = FileTransferer('192.168.0.1', 5001, '192.168.0.1', 5002)
fileTransferer.start()