from cvcb import CovidVaccinationCertificateBuilder
from providers.mac.sha256 import Sha256MP
from providers.mac.crc32 import Crc32MP
from providers.mac.rsa1024 import Rsa1024MP
from providers.mac.dsa512 import Dsa512MP
from providers.mac.aes256_xor import Aes256XorMP
from providers.serialization.concat import ConcatenatorSP
from base64 import b64encode, b64decode
from datetime import datetime
from platform import platform
from time import time
# from server_side_logging import sslog


def read_bytes() -> bytes:
    return b64decode(input())


def print_bytes(s):
    print(b64encode(s).decode('utf-8'))


def main():
    # Here's some platform information
    print(datetime.fromtimestamp(time()))
    print(platform())

    # Please choose a MAC provider (listed in A-Z order):
    # 1 -> Aes256XorMP
    # 2 -> Crc32MP
    # 3 -> Dsa512MP
    # 4 -> Rsa1024MP
    # 5 -> Sha256MP
    # choice = int(input())
    choice = 5
    if choice == 1:
        mp = Aes256XorMP()
    elif choice == 2:
        mp = Crc32MP()
    elif choice == 3:
        mp = Dsa512MP()
    elif choice == 4:
        mp = Rsa1024MP()
    elif choice == 5:
        mp = Sha256MP()
    else:
        assert False, "Unknown algorithm"

    sp = ConcatenatorSP()
    builder = CovidVaccinationCertificateBuilder(mp, sp)
    builder.set_issuer(b"vnsecurity")

    # Please specify your citizen ID and name:
    cid = read_bytes()
    cname = read_bytes()
    # cid = b'a'
    # cname = b'b'
    builder.set_citizen(cid, cname)

    # Here's your certificate
    cert = builder.build()
    print_bytes(cert)

    # If there's something here, you may verify the certificate yourself.
    print_bytes(builder.mp.get_public_info())

    # Give us your certificate
    user_cert = read_bytes()
    # print(builder.debug(b'issuer|vnsecurity|citizen_id|a|citizen_name|b|doses|1|doses|2
    # \x00\x80\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02\xa8|dose|2'))
    # user_cert = ''
    # You have to take at least 2 doses of COVID vaccine to get the flag
    doses = int.from_bytes(builder.parse(user_cert)[b"doses"], "big")
    if doses >= 2:
        # Congrats, here's the flag.
        with open("flag.txt") as f:
            print(f.read())
        # sslog(choice, cid, cname, cert, user_cert)
    else:
        print("Take care of your health, my friend!")


if __name__ == '__main__':
    main()
