from scapy.all import *
import os

PORT = 3514
HOST = 'SERVER_IP'

if __name__ == '__main__':
    print ""
  #  ip=IP(dst=HOST)
    ip=IP(dst=HOST, flags=4)

    syn=TCP(dport=PORT, flags="S", seq=100)
#    print repr(ip/syn)
    synack=sr1(ip/syn, verbose=0)
#    print repr(synack)
    ack=TCP(dport=3514, flags="A", seq=101, ack=synack.seq)
#    print repr(ip/ack)
    ans,unans=sr(ip/ack, verbose=0)
    print ans[0][-1].load

