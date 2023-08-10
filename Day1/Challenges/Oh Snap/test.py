from copy import deepcopy
from Crypto.Util.number import *
from Crypto.Cipher import ARC4
import requests
from tqdm import tqdm
import json 

def ksa(key, t=256):
    state = [i for i in range(256)] 
    j = 0
    for i in range(min(t, 256)):
        j = (j + state[i] + key[i % len(key)]) % 256
        state[i], state[j] = state[j], state[i]
    return state, i, j

def prng(state, length):
    st = deepcopy(state)
    i, j = 0, 0
    stream = b''
    for _ in range(length):
        i = (i + 1) % 256
        j = (j + st[i]) % 256
        st[i], st[j] = st[j], st[i]
        stream += bytes([st[(st[i] + st[j]) % 256]])
        print(stream)
    return stream, st

# pt = b'\x00' * 4
secret_key = b'Cai key gi do o day ne'
key = b'crypto{w1R3d_equ1v4l3nt_pr1v4cy?!}'

def get_first_key(ciphertext, nonce):
    url = f'http://aes.cryptohack.org/oh_snap/send_cmd/{ciphertext}/{nonce}/'
    content = requests.get(url).text
    content = json.loads(content)
    x = long_to_bytes(int(content['error'][len('Unknown command: '):], 16))
    return x

# def get_first_key_local(ciphertext, nonce):
#     cipher = ARC4.new(bytes.fromhex(nonce) + secret_key)
#     return cipher.encrypt(bytes.fromhex(ciphertext))
# for pos in range(len(secret_key)):
for pos in range(len(key), 40):
    cnt = {}
    for k in tqdm(range(256)):
        iv = bytes([pos + 3]) + b'\xff' + bytes([k])
        state, i, j = ksa(iv + key, pos + 3)
        if state[:2] == [pos + 3, 0]:
            # cipher = ARC4.new(iv + secret_key)
            ct = get_first_key('00' * 5, hex(bytes_to_long(iv))[2:])
            x = (ct[0] - j - state[i + 1] + 256) % 256
            if x in cnt:
                cnt[x] += 1
            else:
                cnt[x] = 1
    freq = [(v, u) for u, v in cnt.items()]
    freq.sort(reverse=True)
    choice = 0
    while (freq[choice][0] == freq[0][0]):
        if 31 < freq[choice][1] < 128:
            break
        choice += 1
    key += bytes([freq[choice][1]])
    print(f'Current key: {key}')
print(key)
