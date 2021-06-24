import os
from winAPI import *
import colorset as winAPI

if __name__ == '__main__':
    for colr in winAPI.colorset.values():
        gotoXY(colr, colr+1)
        changeTxtColor(colr)
        print("%d, %d" % (wrIsX(), wrIsY()))
    hideConsoleCursor(1)
    os.system("pause")
