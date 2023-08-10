# Gzip = LZ77 + Huffman encoding 
# LZ77 -> compress partial match string using index and length 
import gzip

flag = 'picoctf{this is the flag}'
alphabet = 'abcdefghijklmnopqrstuvwxyz {}'
known = 'picoctf{'

# for ch in alphabet:
#     data = known + ch + flag
#     compress = gzip.compress(data.encode())
#     print(f'Compress for char {ch}: {len(compress)}')
#     print(data, compress)

# Case flag + input -> same
while len(known) < len(flag):
    di = {}
    for ch in alphabet:
        data = flag + known + ch
        compress = gzip.compress(data.encode())
        di[ch] = len(compress)
    known += min(di, key=di.get)
    print(known)