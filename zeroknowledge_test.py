# setup zero knowledge proof

import random
import math

def setup(p,q):
    # compute n = p*q
    n = p*q
    # compute phi(n) = (p-1)*(q-1)
    phi = (p-1)*(q-1)
    # choose an integer e such that 1 < e < phi(n) and gcd(e, phi(n)) = 1
    e = 7
    # compute d as the multiplicative inverse of e mod phi
    d = pow(e, -1, phi)
    # return public and private keys
    return ((e, n), (d, n))

def encrypt(pk, plaintext):
    # unpack the key into it's components
    key, n = pk
    # convert each letter in the plaintext to numbers based on the character using a^b mod m
    cipher = [(ord(char) ** key) % n for char in plaintext]
    # return the array of bytes
    return cipher

def decrypt(pk, ciphertext):
    # unpack the key into its components
    key, n = pk
    # generate the plaintext based on the ciphertext and key using a^b mod m
    plain = [chr((char ** key) % n) for char in ciphertext]
    # return the array of bytes as a string
    return ''.join(plain)

if __name__ == '__main__':
    print("RSA Encrypter/ Decrypter")
    p = int(input("Enter a prime number (17, 19, 23, etc): "))
    q = int(input("Enter another prime number (Not one you entered above): "))
    print("Generating your public/private keypairs now . . .")
    public, private = setup(p,q)
    print("Your public key is ", public ," and your private key is ", private)
    message = input("Enter a message to encrypt with your private key: ")
    encrypted_msg = encrypt(private, message)
    print("Your encrypted message is: ")
    print(encrypted_msg)
    print(''.join(map(lambda x: str(x), encrypted_msg)))
    print("Decrypting message with public key ", public ," . . .")
    print("Your message is:")
    print(decrypt(public, encrypted_msg))