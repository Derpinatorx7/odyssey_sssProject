import socket
import struct
import os

buff = 4096
s = socket.socket()
s.connect(("84.109.209.188",8080))
file_list = ["openreq.pdf", "editreq.pdf"]
print(len(file_list))
packed_file_list = []

for file in file_list:
	siz = int(os.path.getsize(file))
	fi = open(file,'rb')
	fi = fi.read()
	siz = bin(siz)[2:]
	siz = '0'*(40-len(siz)) + siz
	siz = [int(siz[8*k:8*(k+1)]) for k in range(5)]
	print siz
	siz = struct.pack(">QQQQQ",*siz)
	packed_file_list.append(struct.pack(">L", len(file)) + struct.pack(">{}s".format(len(file)),file) + siz + fi)


def packMessage(name, password, mail_list):
	if type(name) is not str:
		return 0	
	packed_mail_list = ''
	for p in mail_list:
		packed_mail_list += struct.pack(">L",len(p))+ struct.pack(">{}s".format(len(p)),p)
	k = input("number of people required in order to access the file: ")
	msg = struct.pack(">L",len(name)) + struct.pack(">L", password) + struct.pack(">{}s".format(len(name)),name) + struct.pack(">L",len(mail_list)) + packed_mail_list + struct.pack(">L",k) + struct.pack(">L", len(file_list)) + ''.join(packed_file_list)
	return msg


msg = packMessage("horhe.zip", 1111, ['poopmckaki@gmail.com', 'tommyka03@gmail.com'])
while (msg):
    s.send(msg[:buff])
    msg = msg[buff:]
s.close()


