import struct
import os
import random

_PRIME = 2**64-59

welcome = '''
 __          __  _                          
 \ \        / / | |                         
  \ \  /\  / /__| | ___ ___  _ __ ___   ___    _____   _____
   \ \/  \/ / _ \ |/ __/ _ \| '_ ` _ \ / _ \     |    |  _  |
    \  /\  /  __/ | (_| (_) | | | | | |  __/     |    | |_| |
     \/  \/ \___|_|\___\___/|_| |_| |_|\___|     |    |_____|
     '''
row1 = '''
 __        ______    ______    __  __    _____     ______    __     __    __   __    
/\ \      /\  __ \  /\  ___\  /\ \/ /   /\  __-.  /\  __ \  /\ \  _ \ \  /\ "-.\ \   
\ \ \____ \ \ \/\ \ \ \ \____ \ \  _"-. \ \ \/\ \ \ \ \/\ \ \ \ \/ ".\ \ \ \ \-.  \
'''
row2 = '''  
 \ \_____\ \ \_____\ \ \_____\ \ \_\ \_\ \ \____-  \ \_____\ \ \__/".~\_\ \ \_\\"\_ \ 
  \/_____/  \/_____/  \/_____/  \/_/\/_/  \/____/   \/_____/  \/_/   \/_/  \/_/ \/_/                                                                                          
'''

def packFiles(file_list):
	packed_file_list = []
	for file in file_list:
		siz = int(os.path.getsize(file))
		fi = open(file,'rb')
		fi = fi.read()
		siz = bin(siz)[2:]
		siz = '0'*(40-len(siz)) + siz
		siz = [int(siz[8*k:8*(k+1)]) for k in range(5)]
		print(siz)
		siz = struct.pack(">QQQQQ",*siz)
		packed_file_list.append(struct.pack(">L", len(file)) + struct.pack(">{}s".format(len(file)),file) + siz + fi)
	return packed_file_list


def packSaveReq(name, password, mail_list,k, file_list):
	if type(name) is not str:
		return 0	
	packed_mail_list = ''
	for p in mail_list:
		packed_mail_list += struct.pack(">L",len(p))+ struct.pack(">{}s".format(len(p)),p)
	msg = struct.pack(">L", "0") + struct.pack(">L",len(name)) + struct.pack(">L", password) + struct.pack(">{}s".format(len(name)),name) + struct.pack(">L",len(mail_list)) + packed_mail_list + struct.pack(">L",k) + struct.pack(">L", len(file_list)) + ''.join(packFiles(file_list))
	return msg

def randomPassword(password = None):
	global _PRIME
	'''if password is not given returns a random password, else does nothing'''
	if not password:
		password = random.randrange(1,_PRIME)
	return password
	
def packOpenReq(name,mail,passtup):
	if type(name) is not str:
		return 0 
	password_x,password_y = passtup 		
	msg = struct.pack(">L","1") + struct.pack(">L",len(name)) + struct.pack(">{}s".format(len(name)),name) + struct.pack(">L",len(mail)) + struct.pack(">{}s".format(len(mail)),mail) + struct.pack(">QQQQ",password_x) + struct.pack(">QQQQQQQQ",password_y)
	return msg

def masterOpen(name,password):
	if type(name) is not str:
		return 0 
	msg = struct.pack(">L","2") + struct.pack(">L",len(name)) + struct.pack(">{}s".format(len(name)),name) + struct.pack(">L", password)
	return msg
import time, os


def loading_screen():
	print(welcome,end = "")
	time.sleep(0.1)
	print(row1, end = "")
	time.sleep(0.1)
	print(row2, end = "")
	time.sleep(0.1)
	time.sleep(0.5)
	input("press ENTER to continue: ")



test_msg = ["horhe.zip", 1111, ['poopmckaki@gmail.com', 'tommyka03@gmail.com'],7, ["a.txt","b.txt"]]

