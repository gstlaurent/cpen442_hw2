import pycrc

options = ["--model", "crc-32", "--check-string"]

EXP2_32 = 4294967296
def prove_not_strong():
  hashes = {}
  for i in range(EXP2_32):
    opt = pycrc.Options()
    s = str(i)
    opts = options + [s]
    opt.parse(opts)
    h = pycrc.check_string(opt)
    if h in hashes:
      return (h, (s, hashes[h]))
    else:
      hashes[h] = s
  return "ERROR: no collision found"



if __name__ == "__main__":
  print("proving not strong")
  res = prove_not_strong()
  print(res)
