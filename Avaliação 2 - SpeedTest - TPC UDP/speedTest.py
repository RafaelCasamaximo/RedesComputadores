from speedTestTCP import SpeedTesterTCP
from speedTestUDP import SpeedTesterUDP


class SpeedTester:
    def __init__(self) -> None:
        self.menu()
        pass

    def __del__(self) -> None:
        print('Encerrando Programa...')

    def menu(self) -> None:

        onMenu = True

        while onMenu:
            print('Selecione qual teste você deseja:')
            print('   1 - Speed Test TCP')
            print('   2 - Speed Test UDP')
            print('   3 - Sair')

            choice = int(input())

            if choice == 1:
                spdtstTCP = SpeedTesterTCP()
                spdtstTCP.menu()

            elif choice == 2:
                spdtstUDP = SpeedTesterUDP()
                spdtstUDP.menu()

            elif choice == 3:
                onMenu = False
                exit()
            else:
                print('-Insira uma opção válida!')

        pass
