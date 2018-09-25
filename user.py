import struct
import os

def packFiles(file_list):
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
	return packed_file_list


def packSaveReq(name, password, mail_list,k):
	global mail_list
	if type(name) is not str:
		return 0	
	packed_mail_list = ''
	for p in mail_list:
		packed_mail_list += struct.pack(">L",len(p))+ struct.pack(">{}s".format(len(p)),p)
	msg = struct.pack(">L", "0") + struct.pack(">L",len(name)) + struct.pack(">L", password) + struct.pack(">{}s".format(len(name)),name) + struct.pack(">L",len(mail_list)) + packed_mail_list + struct.pack(">L",k) + struct.pack(">L", len(file_list)) + ''.join(packFiles(file_list))
	return msg


test_msg = packSaveReq("horhe.zip", 1111, ['poopmckaki@gmail.com', 'tommyka03@gmail.com'],k)


