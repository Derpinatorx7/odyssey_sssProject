import struct
def packPass(password_x,password_y):
	x = str(password_x)
	x = '0'*(32-len(x)) + x
	x = [int(x[8*k:8*(k+1)]) for k in range(4)]
	x = struct.pack(">QQQQ",*x)
	y = str(password_y)
	y = '0'*(64-len(y)) + y
	y = [int(y[8*k:8*(k+1)]) for k in range(8)]
	y = struct.pack(">QQQQQQQQ",*y)
	passlist = [x,y]
	return passlist



print(packPass(eval("2^32-1"),eval("2^64-1")))