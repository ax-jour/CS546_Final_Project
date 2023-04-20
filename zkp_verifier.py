import random
from database import *


'''
Helper functions
'''
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
    

'''
Registering step for user/prover
y = g^x mod N
x = hash(user_secret) mod N
'''
def save_y(invitation_code, y):
    str_y = str(y)
    conn = get_db_connection()
    conn.execute('UPDATE users SET saved_y = ? WHERE invitation_code = ?', (str_y, invitation_code,))
    conn.commit()
    conn.close()


'''
Challenge step for user/verifier
1. Get t from the prover
2. generate random c to send to the prover
3. get r from the prover
4. calculate result = ( (g**r) * (y**c) ) % N
5. compare result with t
'''
def gen_c(N):
    c = random.randint(1,N)
    return c


def verification(y, r, t, c, g, N):
    result = (inverse_of(pow(g,-r,N),N) * pow(y,c,N)) % N if (r<0) else (pow(g,r,N) * pow(y,c,N)) % N
    return True if t==result else False


