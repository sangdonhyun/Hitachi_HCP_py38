'''
Created on 2014. 4. 16.

@author: Administrator
'''
import threading, time
import socket
import os
import common
import ast
import glob
import sys
import logging.handlers
import configparser
import random
import json


class SocketSender():
    def __init__(self,**kwargs):
        self.filieName=kwargs['FILENAME']
        self.dir = kwargs['DIR']
        self.com = common.Common()
        self.dec = common.Decode()
        self.cfg = self.get_cfg()
        self.HOST=self.cfg.get('server','ip',fallback='localhsot')
        self.PORT=self.cfg.get('server','port',fallback=54002)
        self.log = self.flog()


    def flog(self):
        LOG_FILENAME = os.path.join('log','file_send.log')
        """
        Creates a rotating log
        """
        logger=logging.getLogger('fleta')
        logger.setLevel(logging.DEBUG)
        handler=logging.handlers.RotatingFileHandler(LOG_FILENAME, maxBytes=10000000, backupCount=3)
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        return logger

    def get_cfg(self):
        cfg = configparser.RawConfigParser()
        cfg_file = os.path.join('config', 'config.cfg')
        cfg.read(cfg_file)
        # print(cfg.options)
        return cfg



    def getReTryCnt(self):
        try:
            cnt= int(self.cfg.get('server','sock_retry_cnt'))
        except:
            cnt = 5
        return cnt

    def send(self):
#         HOST, PORT = "1.217.179.141", 54001
        HOST = self.HOST
        if isinstance(self.PORT,str):
            PORT = int(self.PORT)
        else:
            PORT = self.PORT

        print(HOST,PORT)
        fname = self.filieName
#         print  "send file name :",fname
        info={}
        info['FLETA_PASS']='kes2719!'
        info['FILENAME']=os.path.basename(fname)
        info['DIR']=self.dir
        info['FILESIZE']=os.path.getsize(fname)


        dec=common.Decode()
        json_info=json.dumps(info)

        # print('json_info type :',type(json_info))
        # print(json_info)
        # if isinstance(json_info,str):
        #     data=dec.fenc(json_info.encode('utf-8'))
        # else:
        #     data = dec.fenc(json_info)
        # # print data
        data = json_info
        if isinstance(data,str):
            #data = str.isalum()
            data = data.encode('utf-8')
        # Create a socket (SOCK_STREAM means a TCP socket)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sBit=False
        #print('DATA :',data)
        try:
            # Connect to server and send data
            sock.connect((HOST, PORT))

            sock.sendall(data )

            # Receive data from the server and shut down
            received = sock.recv(1024)
            # print('RECV :',received)
            if isinstance(received,bytes):
                received = received.decode('utf-8')

            if received =='READY':
                try:
                    with open(fname,'rb') as f:
                        data=f.read()
                    print ('size :',len(data))
                    sock.sendall(data)

                except Exception as e:
                    self.log.error(str(e))

            sBit = True
        except socket.error as e:
            sBit = False
            self.log.error(str(e))

        finally:
            sock.close()

        return sBit

    def main(self):
        reCnt=self.getReTryCnt()
        cnt=0
        while 1:
            sBit=self.send()
            if sBit :
                print("FILE TRANSFER SUCC BY SOCKET")
                break
            else:
                print('FLETA SERVER : %s , PORT : %s SEND FILE ERROR RETRY (%d/%d) ' % (
                self.HOST, self.PORT, cnt + 1, reCnt))
            cnt += 1
            if reCnt == cnt:
                break

            time.sleep(random.randint(5,10))

if __name__=='__main__':
    fileName=os.path.join('.','setup.py')

    SocketSender(FILENAME=fileName,DIR='dbinfo.SCH').main()
