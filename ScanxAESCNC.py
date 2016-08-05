#-*-coding:utf-8-*-
#!/usr/bin/env python2

"""=============================================================================
=Autor:Smallboy                                                                =
=func:主要实现网段IP端口协议探活扫描                                           =
=push:主要是存放扫描IP网段的文件IPSeg.bin，用于生成IP列表;存放要扫描端口的文件 =
=PortList.bin,用于获取扫描端口列表                                             =
=pop:探测出存活的IP端口存放在IPSeg.bin文件中,探测出存活的CNC存放在AliveCNC.bin =
=文件中                                                                        =
============================================================================="""
import os
import sys
import string
#import optparse
#import Queue
import time
import socket
#import threadpool
from threading import Thread


def hexdump(src, length=16):
    FILTER = ''.join([(len(repr(chr(x))) == 3) and chr(x) or '.' for x in range(256)])
    lines = []
    for c in xrange(0, len(src), length):
        chars = src[c:c+length]
        hex = ' '.join(["%02x" % ord(x) for x in chars])
        printable = ''.join(["%s" % ((ord(x) <= 127 and FILTER[ord(x)]) or '.') for x in chars])
        lines.append("%04x  %-*s  %s\n" % (c, length*3, hex, printable))
    return ''.join(lines)


def EnumIP(IPSeg):
    IPList = []
    IP_Seg = IPSeg.split('/')
    DataList = IP_Seg[0].split('.')
    #print(IP_Seg)
    if (len(DataList) == 2):
        for i in range(int(DataList[1]),int(IP_Seg[1].split('.')[0]) + 1):
            for j in range(1,255):
                for r in range(2,255):
                    IP = DataList[0] + '.' + str(i) + '.'  + str(j) + '.'  + str(r)
                    IPList.append(IP)
        return IPList
        
    elif (len(DataList) == 3):
        for i in range(int(DataList[2]),int(IP_Seg[1].split('.')[0]) + 1):
            IP_Addr = DataList[0] + '.' + DataList[1] + '.' + str(i) 
            for j in range(2,255):
                IP = IP_Addr +  '.' + str(j)
                IPList.append(IP)
                #print(IP)
        return IPList
    
    elif (len(DataList) == 4):
        IP_Addr = DataList[0] + '.' + DataList[1] + '.' + DataList[2]
        for i in range(int(DataList[3]),int(IP_Seg[1]) + 1):
            IP = IP_Addr + '.' + str(i)
            IPList.append(IP)
            #print(IP)
        return IPList

    return 

        
def ScanPort(AddressList,Port):
    #for AddressList_1 in AddressList:
    for Address in AddressList:
        #print "IP_Addr:",Address,"Port:",Port
        global g_hAliveIP
        if AES_ConnScan(Address,Port):
            print("Get ", Address, Port, 'is Open')
            break
        





def AES_ConnScan(TarHost,TarPort):
    try:
        socket.setdefaulttimeout(1)
        conn = socket.create_connection((TarHost, string.atoi(TarPort)))
        global g_OpenTheHeartData
        if conn.send(g_OpenTheHeartData):
            print(TarHost,TarPort,"Send Open Heart Data")
        
        result = conn.recv(1024)    
        print('recver length:',len(result))
        Output_Data = TarHost + '\t' + TarPort + "\r"
        time.sleep(0.25)
        hFile = open('AliveIP.bin','a')
        WriteDataToFile(hFile,str(Output_Data))
        hFile.close()
        
        #print(hexdump(result))
        hCommandFile = open('unkowncommand.bin','a')
        WriteDataToFile(hCommandFile,hexdump(result))
        WriteDataToFile(hCommandFile,Output_Data)
        hCommandFile.close()

        
        if (result[0] == "\x07") & (len(result) == 413):
            hAliveCNC = open('AliveCNC.bin','a')
            WriteDataToFile(hAliveCNC,Output_Data)
            hAliveCNC.close()
            print (TarHost + '\t',TarPort + '\t','connect successful……')
            return True
    except Exception,e:
        #print(e)
        #print TarHost + '\t',TarPort + '\t',"connect fail……"
        return False
    

    
def WriteDataToFile(Filename,WriteData):
    Filename.write(WriteData)
    return 


'''
def Main():
    parser =optparse.OptionParser("usage%prog " + "-H <HostAddressSegment> -S <SaveAliveIPtoFile>")
    parser.add_option("-H", dest = 'Host_IP',   type = 'string',    help = 'Scaner Destination IP Segment' )
    parser.add_option("-S", dest = "SaveFile",  type = 'string',    help = 'Save Alive IP to File' )
    (options, args) = parser.parse_args()
    if (options.Host_IP == None) | (options.SaveFile == None):
        print(parser.usage)
        exit(0)
    else:
        Host_IP = options.Host_IP
        SaveFile = options.SaveFile
'''



g_OpenTheHeartData = open('OpenHeart.bin', 'rb').read()
g_IPSeg = open('IPSeg.bin','rb').read().split('\r')
g_ScanPortList = open('PortList.bin','rb').read().split('\r')

if __name__ == "__main__":

    
    IPlist = []
    print(g_IPSeg)
    #print(g_ScanPortList)
    for i in g_IPSeg:
        IPlist.append(EnumIP(i))
    print(IPlist[1])
    #print(len(IPlist))
    for i in range(0,len(IPlist)):
        #print(IPlist[i]) 
        for port in g_ScanPortList:
            t = Thread(target = ScanPort,args = (IPlist[i], port) )
            t.start()
            time.sleep(2)
    """
    #for Thread in Threadlist:
    g_OpenTheHeartData.close()
    g_IPSeg.close()
    g_ScanPortList.close()
    
    
    pool = threadpool.ThreadPool(20)
    
    for IPlist_1 in IPlist:
        for IP in IPlist_1:
            ScanPort(IP)
            requests = threadpool.makeRequests(ScanPort,IP)

        for req in requests:
            pool.putRequest(req)
    pool.wait()
    """
    
    
    
        

    
