import random
import string
import uuid


def randomNumber(length):
    return ''.join(str(random.choice(range(10))) for _ in range(length))


def randomMac():
    mac = [0x10, 0x2a, 0xb3,
           random.randint(0x00, 0x7f),
           random.randint(0x00, 0xff),
           random.randint(0x00, 0xff)]
    return ':'.join(map(lambda x: "%02x" % x, mac))


def randomString(length):
    return ''.join(random.sample(string.ascii_letters + string.digits, length))


def randomHex(length):
    return "".join([random.choice("0123456789abcdef") for _ in range(length)])


def randomIMEI(digits14):
    digit15 = 0
    for num in range(14):
        if num % 2 == 0:
            digit15 = digit15 + int(digits14[num])
        else:
            digit15 = digit15 + (int(digits14[num]) * 2) % 10 + (int(digits14[num]) * 2) / 10
    digit15 = int(digit15) % 10
    if digit15 == 0:
        digits14 = digits14 + str(digit15)
    else:
        digits14 = digits14 + str(10 - digit15)
    return digits14


def randomUUID():
    return uuid.uuid4()


