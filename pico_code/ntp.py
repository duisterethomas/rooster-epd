import socket
from machine import RTC
from struct import unpack
from time import gmtime

NTP_DELTA = 2208988800
host = "pool.ntp.org"

def set_time():
    NTP_QUERY = bytearray(48)
    NTP_QUERY[0] = 0x1B
    addr = socket.getaddrinfo(host, 123)[0][-1]
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    try:
        s.settimeout(10)
        res = s.sendto(NTP_QUERY, addr)
        msg = s.recv(48)
    finally:
        s.close()
    
    val = unpack("!I", msg[40:44])[0]
    t = val - NTP_DELTA    
    tm = gmtime(t)
    RTC().datetime((tm[0], tm[1], tm[2], tm[6] + 1, tm[3], tm[4], tm[5], 0))