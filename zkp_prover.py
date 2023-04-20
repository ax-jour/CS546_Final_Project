import random
import hashlib


'''
Registering step for user/prover
'''
def hashed_secret(info, N):
    return int(hashlib.sha256(info).hexdigest(), 16) % N


def get_y(x, g, N):
    return pow(g, x, N)

'''
Prover proving step
1. generate random v, calculate t and send it to verifier
2. calculate r by using v, c and hashed_secret
3. send r to verifier
'''
def calc_r(hashed_secret, v, c, g, N):
    t = pow(g, v, N)
    print('v: ', v)
    return t, (v - c * hashed_secret) % N
