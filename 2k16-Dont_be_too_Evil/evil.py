from scapy.all import *
import os
from time import sleep

FLAG="NDH2K16_the_flag_goes_here"
NOFLAG="Sorry, only true evil can access this server."

PORT = 3514
HOST = 'SERVER_IP'

def react(p):
    if p[2].flags == 16:
        AckNr=p.seq
        SeqNr=p.ack
        Client=p[1].src
        ClientPort=p.sport
        Server=p[1].dst
        ServerPort=p.dport

        pkt_ip=IP(src=Server, dst=Client, flags=4)
        raw_msg = NOFLAG+"\n"
        print repr(p[1])
        if p[1].flags & 4 == 4:
            raw_msg=FLAG+"\n"
        pkt_tcp=TCP(sport=ServerPort, dport=ClientPort, flags="FPA", seq=SeqNr, ack=AckNr, options=[('NOP', None)])
        pkt = pkt_ip/pkt_tcp/raw_msg
        send(pkt, verbose=0)

if __name__ == '__main__':
    a=sniff(filter="tcp and host %s and port %s" % (HOST, PORT), prn=react)
