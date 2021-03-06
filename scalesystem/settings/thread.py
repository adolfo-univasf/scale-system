import threading
import os


def inicia_programa(nome_arquivo):
    os.system('py -3.7 {}'.format(nome_arquivo))
    # Ex: os.system('py -3.7 x.py')

if __name__ == "__main__":

    arquivos = ['x.py','y.py']

    processos = []
    for arquivo in arquivos:
        processos.append(threading.Thread(target=inicia_programa, args=(arquivo,)))
        # Ex: adicionar o porcesso `threading.Thread(target=inicia_programa, args=('x.py',))`

    for processo in processos:
        processo.start()