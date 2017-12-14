import time
from socket import *

clientSocket = socket(AF_INET, SOCK_DGRAM)
clientSocket.settimeout(10)
clientSocket.bind(('', 11257))

try:
    data, server = clientSocket.recvfrom(1024)
    print("{} {}".format(data, server))
except timeout:
    print('REQUEST TIMED OUT')