from __future__ import division
import random
import functools
import hashlib

_PRIME = 2**67-1


_rint = functools.partial(random.SystemRandom().randint, 0)

def make_secret(scrt):
	"""if user wants to choose secret then enter -1 as the secret for a random secret
	otherwise enter the secret the user entered"""
	if scrt == -1:
		scrt = random.randrange(1,_PRIME)
	return scrt
	
def _eval_at(poly, x, prime):
	'''evaluates polynomial (coefficient tuple) at x, used to generate a
	shamir pool in make_random_shares below.
	'''
	accum = 0
	for coefficient in reversed(poly):
		accum *= x
		accum += coefficient
		accum %= prime
	return accum


def make_random_shares(minimum, shares, secret, prime=_PRIME):
	'''
	Generates a random shamir pool, returns the sharepoints.
	'''
	if minimum > shares:
		raise ValueError("pool secret would be irrecoverable")
	poly = [_rint(prime) for i in range(1, minimum)]
	poly[0] = secret

	points = [(i, _eval_at(poly, i, prime))
			  for i in range(1, shares + 1)]
	return poly[0], points


def _extended_gcd(a, b):
	'''
	division in integers modulus p means finding the inverse of the
	denominator modulo p and then multiplying the numerator by this
	inverse (Note: inverse of A is B such that A*B % p == 1) this can
	be computed via extended Euclidean algorithm
	http://en.wikipedia.org/wiki/Modular_multiplicative_inverse#Computation
	'''

	x = 0
	last_x = 1
	y = 1
	last_y = 0
	while b != 0:
		quot = a // b
		a, b = b,  a%b
		x, last_x = last_x - quot * x, x
		y, last_y = last_y - quot * y, y
	return last_x


def _divmod(num, den, p):
	'''compute num / den modulo prime p

	To explain what this means, the return value will be such that
	the following is true: den * _divmod(num, den, p) % p == num
	'''
	inv = _extended_gcd(den, p)
	return num * inv


def _lagrange_interpolate(x, x_s, y_s, p):
	'''
	Find the y-value for the given x, given n (x, y) points;
	k points will define a polynomial of up to kth order
	'''
	k = len(x_s)
	assert k == len(set(x_s)), "points must be distinct"
	def PI(vals):  # upper-case PI -- product of inputs
		accum = 1
		for v in vals:
			accum *= v
		return accum
	nums = []  # avoid inexact division
	dens = []
	for i in range(k):
		others = list(x_s)
		cur = others.pop(i)
		nums.append(PI(x - o for o in others))
		dens.append(PI(cur - o for o in others))
	den = PI(dens)
	num = sum([_divmod(nums[i] * den * y_s[i] % p, dens[i], p)
			   for i in range(k)])
	return (_divmod(num, den, p) + p) % p


def recover_secret(shares, prime=_PRIME):
	'''
	Recover the secret from share points
	(x,y points on the polynomial)
	'''
	if len(shares) < 2:
		raise ValueError("need at least two shares")
	x_s, y_s = zip(*shares)
	return _lagrange_interpolate(0, x_s, y_s, prime)

	
def check_secret(secret, prime = _PRIME):
	#print "secret type", type(secret)
	"""secret = str(secret)
	for ch in secret:
		#print ch
		if ch not in {'0','1','2','3','4','5','6','7','8','9'}: 
			#print "invalid"
			return 0 #not an integer
	"""
	if int(secret) < 1 or secret > _PRIME:
		return 0
	return 1
	
'''
def get_secret(scrt):
	#returns 0 if invalid secret and secret if valid secret
	if check_secret(scrt):
		print "valid secret"
		return scrt
	else:
		print "invalid secret, enter another one"
		return 0
	'''


def md5_scrt_and_shares(secret, shares):
	scrt_md5 = md5_func(secret)
	shares_md5 = []
	for share in shares:
		inpt, otpt = share #share is tuple
		inpt_md5 = md5_func(inpt)
		otpt_md5 = md5_func(otpt)
		shares_md5.append((inpt_md5,otpt_md5))

	return scrt_md5, shares_md5


def make_shares(minimum, shares, secret):
	'''if secret=-1 random secret will be made and otherwise enter the user's secret
	enter minimum number of people to open file and number of shares and returns the secret and the shares
	returns 0,0,0,0 if invalid secret and secret and shares if valid'''

	secret = make_secret(secret)
	if check_secret(secret):
		secret, shares = make_random_shares(minimum, shares, secret)
		#md5_secret, md5_shares = md5_scrt_and_shares(secret, shares)
		return secret, shares#, md5_secret, md5_shares
	print("invalid secret")
	return 0,0

def make_all(mails, secret, required):
	'''if secret = -1 then random secret and otherwise secret will be what is given'''
	num_of_people = len(mails)
	if secret == -1:
		secret = make_secret(secret)
	secret, shares = make_shares(required, num_of_people, secret)
	shares_list = []
	for num in range(num_of_people):
		shares_list.append(mails[num], shares[num])
	return secret, shares_list #returnd (mail,(inpt,otpt))


def md5_func(inpt):
	inpt = str(inpt)
	return hashlib.md5(inpt.encode('utf-8')).hexdigest()


def md5_shares(secret, shares):
	'''returns secret, list of tup:(mail, (hash of inpt,hash of otpt))'''
	list = []
	for tup in shares:
		mail, share = tup
		inpt, otpt = share
		list.append((mail, (md5_func(inpt), md5_func((otpt)))))
	return md5_func(secret), list

