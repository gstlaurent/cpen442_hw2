import pycrc
from multiprocessing import Pool
import os

options = ["--model", "crc-32", "--check-string"]
EXP2_32 = 4294967296

def hash_string(string):
    opt = pycrc.Options()
    opts = options + [string]
    opt.parse(opts)
    return pycrc.check_string(opt)

BASE = hash_string("graham")

def prove_not_strong():
    with Pool() as pool:
        chunksize = round(EXP2_32/os.cpu_count())
        pool.imap(check_match, range(EXP2_32), chunksize)

def check_match(i):
    s = str(i)
    h = hash_string(s)
    if h == BASE:
        print("Matches found!")
        print("crc32('graham') == crc32('{s}') == 0x{h:x}".format(s=s, h=h))
    return




if __name__ == "__main__":
    print("proving not strong")
    prove_not_strong()
    print("DONE")

