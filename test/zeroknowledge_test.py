import random
import hashlib

# REF: https://asecuritysite.com/encryption/fiat2

N=16238557847571361432079207259416643917456544702863121607771071554190210386009

text="This is my secret statement".encode('utf-8')
g = 7

def extended_euclidean_algorithm(a, b):
    s, old_s = 0, 1
    t, old_t = 1, 0
    r, old_r = b, a

    while r != 0:
        quotient = old_r // r
        old_r, r = r, old_r - quotient * r
        old_s, s = s, old_s - quotient * s
        old_t, t = t, old_t - quotient * t

    return old_r, old_s, old_t


def inverse_of(N, p):
    gcd, x, y = extended_euclidean_algorithm(N, p)
    assert (N * x + p * y) % p == gcd

    if gcd != 1:
        # Either N is 0, or p is not a prime number.
        raise ValueError(
            '{} has no multiplicative inverse '
            'modulo {}'.format(N, p))
    else:
        return x % p

v = random.randint(1,N)
c = random.randint(1,N)

print("Secret TEXT:\t",text)
x = int(hashlib.sha256(text).hexdigest(), 16) % N
y = pow(g,x,N)
t = pow(g,v,N)
r = (v - c * x) 

Result = (inverse_of(pow(g,-r,N),N) * pow(y,c,N)) % N if (r<0) else (pow(g,r,N) * pow(y,c,N)) % N

print('\n======Agreed parameters============')
print('(Prime number) \t P=',N)
print('(Generator) \t G=',g)


print('\n======The secret==================')
print('(Prover\'s secret) x =',x)

print('\n======Random values===============')
print('(Verifier\'s random value) \t c=',c)
print('(Prover\'s random value) \t v=',v)

print('\n======Shared value===============')
print('g^x mod P=\t',y)
print('r=\t\t',r)

print('\n=========Results===================')
print('t=g**v % N =\t\t',t)
print('( (g**r) * (y**c) )=\t',Result)
print('\n')
if (t==Result):
	print('Prover has proven he knows password')
else:
	print('Prover has not proven he knows x')