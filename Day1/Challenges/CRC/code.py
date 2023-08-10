from zlib import crc32

def crc32_manual(msg, initial_state = 0xffffffff, expand = False):
    crc = initial_state
    if expand:
        crc ^= 0xffffffff

    for b in msg:
        crc ^= b
        for _ in range(8):
            crc = (crc >> 1) ^ 0xedb88320 if crc & 1 else crc >> 1
    return crc ^ 0xffffffff


secret = b'some text here'
message = b'123456789'
mac = crc32(secret + message)
print(mac)

appended_data = b' and 987654321'
new_mac = crc32(secret + message + appended_data)
print(new_mac)

print(crc32_manual(appended_data, mac, True))

# Patch -> crc(message + secret)
