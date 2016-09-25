import cryptoanalysis as crypt
from multiprocessing import Pool

STRING = crypt.cipher1

def find_candidates_par(string):
    worlds = crypt.find_keylen_worlds(STRING)
    with Pool() as pool:
        candidate_lists = pool.map(make_candidates_par, worlds.items())
    return [c for clist in candidate_lists for c in clist]

def make_candidates_par(kb):
    keylen, bypos = kb
    candidates = []
    xlists = [[]]
    for i in range(keylen):
        xlists = crypt.cross_multiply(xlists, bypos[i])
    for sslst in xlists:
        cr = crypt.Cryptext(STRING)
        for ss in sslst:
            cr = cr.shift(*ss)
        if crypt.is_candidate(str(cr)):
            candidates.append((sslst, str(cr)))
    return candidates

def find_vignere_candidates_par(string):
    cands = find_candidates_par(string)
    cands = crypt.narrow_by_words(cands)
    return cands


if __name__ == '__main__':
    cands = find_vignere_candidates_par(STRING)
    crypt.print_candidates(cands)

