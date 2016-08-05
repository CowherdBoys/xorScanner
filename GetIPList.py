# -*- coding:utf-8 -*-

import os,sys


def GetSegData(Segdata):
    segList = Segdata.split('\r')
    #print(segList)
    segIPList = []
    for seg in segList:
        IP = seg.split('\t')
        IPStar = IP[0].split('.')
        IPEnd = IP[1].split('.')
        segIPList.append((IPStar,IPEnd))

    return segIPList


def GetIPList(SegData):
    segIPList = GetSegData(SegData)
    #print(segIPList)
    List = []
    for segIP in segIPList:
        #print(segIP)
        IPList = []
        if (int(segIP[0][0]) == int(segIP[1][0])):
            if (int(segIP[0][1]) == int(segIP[1][1])):
                if (int(segIP[0][2]) == int(segIP[1][2])):
                    #print(segIP[0][3] , segIP[1][3])
                    if (int(segIP[0][3]) > int(segIP[1][3])) or (int(segIP[1][3]) > 255) or (int(segIP[0][3]) < 0):
                        print "您输入的网段:",segIP,"有错误，请检查！（T_T）"
                    else:
                        for i in range(int(segIP[0][3]),int(segIP[1][3])+1):
                            IP = segIP[0][0] + '.' + segIP[0][1] + '.' + segIP[0][3] + '.' + str(i)
                            IPList.append(IP)

                else:
                    if (int(segIP[0][2]) > int(segIP[1][2])) or (int(segIP[1][2]) > 255) or (int(segIP[0][2]) < 0):
                        print "您输入的网段:",segIP,"有错误，请检查！（T_T）"
                    else:
                        for i in range(int(segIP[0][2]),int(segIP[1][2]) +1):
                            for j in range(1,255):
                                IP = segIP[0][0] + '.' + segIP[0][1] + '.' + str(i) + '.' + str(j)
                                IPList.append(IP)
                    
            else:
                if (int(segIP[0][1]) > int(segIP[1][1])) or (int(segIP[1][1]) > 255) or (int(segIP[0][1]) < 0):
                    print "您输入的网段:",segIP,"有错误，请检查！（T_T）"

                else:
                    for i in range(int(segIP[0][1]),int(segIP[1][1]) + 1):
                        for j in range(0,255 +1):
                            for r in range(0,255):
                                IP = segIP[0][0] + '.' + str(i) + '.' + str(j) + '.' + str(r)
                                IPList.append(IP)

        else:
            print "您要扫描的网段过大，请将其分段扫描,谢谢（*^_^*）"
            
        List.append(IPList)
    return List


def Main(FileName):
    segData = open(FileName,'rb').read()
    
    return GetIPList(segData)


if __name__ == "__main__":
    openFileName = '01.txt'
    segData = open(openFileName,'rb').read()
    #saveFileName = 'New' + openFileName
    #hSaveFile = open(saveFileName, 'w')
    print(GetIPList(segData)[2][0:100])
    print(GetIPList(segData)[2][1000:1100])
    print(GetIPList(segData)[2][10000:11000])
    




"""
for IPSeg in IPSegList:
    print(IPSeg)
"""
