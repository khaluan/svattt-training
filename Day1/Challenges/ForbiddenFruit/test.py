F.<a> = GF(2^128, modulus=x^128 + x^7 + x^2 + x + 1)
P.<x> = PolynomialRing(F)

def int_to_poly(val):
    val = int(f"{val:0128b}"[::-1], 2)
    return F.fetch_int(val)

def poly_to_int(poly):
    val = poly.integer_representation()
    val = int(f"{val:0128b}"[::-1], 2)
    return val

def bytes_to_poly(b):
    return int_to_poly(bytes_to_long(b))

def poly_to_bytes(poly):
    return long_to_bytes(poly_to_int(poly))

def pad(b):
    return b + b'\x00' * (16 - len(b))


pt_1 = '61' * 16
ct_1 ={"associated_data":"43727970746f4861636b","ciphertext":"ce4ec34ea6f0481e6eac76d71f3dbfdc","nonce":"090c70a740f4930059c66028","tag":"b1ce2024c569bc698605e39779aed881"}
pt_2 = '62' * 16
ct_2 = {"associated_data":"43727970746f4861636b","ciphertext":"cd4dc04da5f34b1d6daf75d41c3ebcdf","nonce":"090c70a740f4930059c66028","tag":"415c1848b3138581f423275cec1451c1"}
ad_data = b'CryptoHack'
ad = bytes_to_poly(pad(ad_data))

tag_1 = bytes_to_poly(bytes.fromhex(ct_1['tag']))
ct1_data = ct_1['ciphertext']
ct_1 = bytes_to_poly(bytes.fromhex(ct_1['ciphertext']))

tag_2 = bytes_to_poly(bytes.fromhex(ct_2['tag']))
ct_2 = bytes_to_poly(bytes.fromhex(ct_2['ciphertext']))
length = bytes_to_poly(b'\x00' * 7 + b'\x0a' + b'\x00' * 7 + b'\x10')


# tag_1 = ad * X ^ 3 + ct_1 * X ^ 2 + length * X + mask
# tag_fake = ad * X ^ 3 + ct_fake * X ^ 2 + length * X + mask
f_1 = ad * X ^ 3 + ct_1 * X ^ 2 + length * X  - tag_1
f_2 = ad * X ^ 3 + ct_2 * X ^ 2 + length * X  - tag_2
p = f_1 - f_2

root = p.roots()[0][0]

pt_data = b'give me the flag'
ct_data = bytes.fromhex('c846d44ae7fc4c5f7ba572961830bfda')
ct_fake = bytes_to_poly(ct_data)
length_fake = len(ad_data).to_bytes(8, byteorder='big') + len(pt_data).to_bytes(8, byteorder='big')
tag_fake = (ct_fake - ct_1) * root ^ 2 + tag_1
poly_to_bytes(tag_fake).hex()