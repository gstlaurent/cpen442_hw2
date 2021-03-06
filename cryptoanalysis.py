from collections import Counter, namedtuple, defaultdict
from itertools import groupby
import pprint
import copy


# everything uses lowercase

ALPHAS = "abcdefghijklmnopqrstuvwxyz"
MAX_LENGTH = 80
MAX_KEY_LENGTH = 10
MIN_WORD_HITS = 30
TOP_CHAR_DEPTH = 10
TOP_CHARS = "aehinorst" # all >6% 
MIN_TOP_CHAR = 5

FREQS = {"a": .082, "b": .015, "c": .028, "d": .043, "e": .127, "f": .022,
         "g": .020, "h": .061, "i": .070, "j": .002, "k": .008, "l": .040,
         "m": .024, "n": .067, "o": .075, "p": .019, "q": .001, "r": .060,
         "s": .063, "t": .091, "u": .028, "v": .010, "w": .024, "x": .002,
         "y": .020, "z": .001}


def load_words():
    with open("./common_words.txt") as f:
        words = f.read()
        return words.splitlines()

COMMON_WORDS = load_words()[:350] # they are in order of usage (500 total)

plaintext1 = "oneofthescholarswasrequiredtoretirecommaandthentoreentertheroomasapolitegentlemanissupposedtoenteradrawingroomdothewasreceivedatthedoorbyanotherscholarandconductedfrombenchtobenchuntilhehadbeenintroducedtoalltheyoungladiesandgentlemenintheroomdotlincolnwentthroughtheordealcountlesstimesdotifhetookaseriousviewoftheperformanceitmusthaveputhimtoexquisitetorturecommaforhewasconsciousthathewasnotaperfecttypeofmanlybeauty"
cipher1    = "entehbitgqiesfkgzfgktlxwktubektbwktqerrffnubitnbekttnbtkbitkeerfgfaeswbtvtnbstrfnwggxaaegtubetnbtkfukfzwnvkeeruebitzfgktqtwctufbbitueekydfnebitkgqiesfkfnuqenuxqbtuhkerytnqibeytnqixnbwsitifuyttnwnbkeuxqtubefssbitdexnvsfuwtgfnuvtnbstrtnwnbitkeeruebswnqesnztnbbikexvibitekutfsqexnbstggbwrtguebwhitbeejfgtkwexgcwtzehbitatkhekrfnqtwbrxgbifctaxbiwrbetplxwgwbtbekbxktqerrfhekitzfgqengqwexgbifbitzfgnebfatkhtqbbdatehrfnsdytfxbd"


# https://en.wikipedia.org/wiki/Frequency_analysis

# permutation substitution cipher
# ALPHAS = "abcdefghijklmnopqrstuvwxyz"
# key      "fequthviw ksrnealkgbxczpd "
# m,o missing



cipher2 = "qtseoktfgacuetdukcduumrpulwtdedqmeykwttdxdiddyqtbfaymkyfacbueoxocehucuazgtleovucxocucaytidpoqfcdvdeqeqykftanekmdumrpupmfcamaueyhekcetgofulwtdedqmeykwtceuamfcamauetdxdidtocetgtocydurtdqidditohctkuhanekmdumrpupumtfkrpgktokteuemcelqcbrtdxdidluceoeetedoyofoxgacufzmpzsuesztcdtdqidofocekcetabeecotcnytugkiqkfgoctybrvdgnetptduumulukeofkycrtdqidofamuklhcaytulwttdxdidetuckpfubphimhdqidmeoftoqsulwtdedqmeykwttdxdidqtsaotfvxoetukruqeqfoetotcekeqlxiqhuceoeelrpulwtqftvneekcgdqidtkfgagmrdqidluoeelwtceoeqtyabeecytetdutogttdxdidofocetxofuvdytegdqidceoelufqgttdxdidukrucetekyctrprktyvdulwttotgdqidxmvdceduumukxoekmdumbhtcuyxhdqidofcxoahunaycetflofdtdqidfzceceguuezqwtgecfcuqfhuykaehtftydyuzqxocaidxptklufiyhvuaycnytezagykicyvorykicceqfcvtyotxgdqidulihxttgdqidkpueuhtdxdidgacursdvruouyhettkyhhurhdqideyyxqfcbayxoxmvdceduumulbhaqwtytulwtdedqmeykwtkttdxdidtkfzkqqscetuirmxybofocetstybbrqfxudqcetgtouhbdoedyrtdqidofcrdquifnydqcetyhefbutdxdidofvcdoxoaucgetdetkcecuxudqkiqkagycettkyutgdqidofcrydxvqfytcecaudfzwtyddqtdxdidofkrqeydyfcrdqidkiplzqsdqfezfooymelfoeqaxotycetfekmdumusthqfrktyfgmpmhdqidqtratohqdndanamxretkaekdmeuffotdzqhrtocvtyqtratoctwftgcgdyucgcksudulwtdykdediqiveqtovdyqayvdoyzqxofadiofvdhuafxoaycgdqidpgtfqfcecimakmtaaeotcttdxdidceoeetluytktzeegdqidofcrdqhuvdpxfzceefcuavtyqtratogytyetudyvyeeqicvdyqayvdoyzqxodiofugqfhcnvuvbuqfxutoytneetdetdlxofqztfcgdqidofackuqfebfloyetzqcdkmtaaeiqftytduebufytyefzcecehffefqyhtdxdidofocetpyeoycqfhcetagbuuexuhucktysyyqayvdcffhgccegfdykrvdyqayvdoycffhgcdiofytftagmduciczrcuqducceofceuamuyhceuchiqfhuanceuamuyhagbutgdqidofocdacfhftoucfhoeqfhcetuhyfeqiqeqyhqztcvythqfcetgtkbyrktyqtratoctwftgeoidoyvyucoaanafoyetzqcdkmtaaeiqfttdxdidofkrfqcwhtmrdqidofkroutdxdidqebkcuunyfoqtdxdidsycehuszhueqpetgofceqfadneetucyhanqetdxdidofocetoybrofcxoaufeyfndyellrhixedqidofcrdqideactbxdukrtdxdiduycdacpqrbtgkqihgcqetdxdidpgtfetekbhtyytoftfequcqsamnwauucoyfkycancehutohgdqidofvrucoaanxedqidfzceayeonvmcanfvyxqfhgdqidyttvuvhdofkmtcqtseokufcncetfofocetucvdyqayvdoyfgmpmhdqidzfqiiqyuchzatuayofmaueanekmdumrprhdqmeulwtqfhgdqidofocetoqayedfqrahtanqenabraybuhixatyflgcybteduumlsduumrktyyhofamwtsfqfxutoytnffeotofvocdcmhuulwtcecfcffhgcofcqvyvdeqidxuefamhyokcuqtmkceqfhgdqidqtsaotxvtyfuwftgyqaykiphotfzcgdqidqtsaotxvtysyeqhycetapqqyelwtlaotxvtyqeyhetfivchuykwtayytnfqfeadytfdtdqidmatocquexfqfeadyuficofqtsaotpwpgoeqzueoyettyetycelwttdxdidqtsaotxvtyqtriyueompiqaqfqoyetgedyyutdxdidqtsaotxvtyirmxybykxahizeecofvoxwfuyqytqaqfqfcetgtkbyrktysbqiiqofhncunamxofgtanxshiratctyetfivchuykwtqfcyfezsuqybrsqocukdyufloflucotyqdicoyduumagupdyekmdumyhaqaqfqxotyekmdumyhoahuototeqgtanqevdyocukdyufloflucgdqicxthuxshirataagudevqftdxdidofkcduumrhdqidtdxdicxtqfhbqfezwtoecehuditcqztgdqidvolshuanneetafbucngnkqqfhuanceuamuyhqkmcrpykwtayytnfqfeadycf"



################################################################################

class Cryptext():
    def __init__(self, string=""):
        self.chars = [Char(c) for c in string]

    def __str__(self):
        chars = [str(c) for c in self.chars]
        return "".join(chars)

    def __repr__(self):
        return "Cryptext('{}')".format(str(self))

    def shift(self, dist, keylen=1, keypos=0):
        chars = self.chars[:]
        for i in range(0, len(chars), keylen):
            idx = i + keypos
            if idx < len(chars):
                chars[idx] = chars[idx].shift_left(dist)
        cr = Cryptext()
        cr.chars = chars
        return cr

    def swap(self, l1, l2):
        def newchar(c):
            c = str(c)
            if c == l1:
                return l2
            elif c == l2:
                return l1
            else:
                return c

        newstring = "".join(newchar(c) for c in self.chars)
        return Cryptext(newstring)

    def s(self, l1, l2):
        return self.swap(l1, l2)
    def f(self):
        self.frequencies()

    def uppers(self, *letters):
        nums = [ord(l) - 96 for l in letters]
        for c in self.chars:
            if c.num in nums:
                c.num -= 32 # make uppercase
        return self

    def map(self, fun):
        cr = Cryptext(str(self))
        cr.chars = [fun(c) for c in cr.chars]
        return cr

    def frequencies(self):
        f = Frequencies(str(self))
        f.show()

    def sort(self):
        freqs = sorted(FREQS.items(), key=lambda lf: -lf[1])
        f = Frequencies(str(self))
        act_exp = zip(f.by_count, freqs)
        print(list(act_exp))

        act_exp = zip(f.by_count, freqs)
        cr = Cryptext(str(self))
        for la_le in act_exp:
            cipherletter = la_le[0][0]
            freqletter = la_le[1][0]
            cr = cr.swap(cipherletter, freqletter)
        return cr


class Char():
    def __init__(self, letter=None, num=None):
        if letter:
            self.num = ord(letter) - 96
        elif num:
            self.num = num
        else:
            assert(False)

    def upper(self):
        self.num -= 32

    def __eq__(self, o):
        return self.num == o.num
    def __hash__(self):
        return self.num

    def __repr__(self):
        return "Char({c}, {n})".format(c=str(self), n=self.num) 
    def __str__(self):
        return str(chr(96 + self.num))

    def shift_left(self, dist):
        num = (self.num + 26 - dist) % 26
        if num == 0:
            num = 26
        return Char(num=num)

    def __sub__(self, o):
        return self.shift_left(o.num)


def freqlengths(cr, maxkeylen):
    for i in range(1, maxkeylen): 
        print(i)
        cc = Cryptext(str(cr)[::i])
        print(cc)
        cc.print_frequencies()
        print()


class Frequencies():
    def __init__(self, string):
        string = string.lower()
        self.counts = Counter(string) # {letter: count}
        self.by_count = sorted(self.counts.items(), key=lambda lc: -lc[1])

    def top(self, n):
        top_lcs = self.by_count[:n]
        topn = [l for l,c in top_lcs]
        return topn

    def show(self):
        most = self.by_count[0][1]
        scale = MAX_LENGTH / most
        for l in ALPHAS:
            n = self.counts[l]
            print("{l}{n:4}:{stars}".format(l=l, n=n, stars="*" * int(scale * n)))

def is_candidate(string):
    freq = Frequencies(string)
    topN = freq.top(1) # TOP_CHAR_DEPTH)
    # return "e" in topN and "a" in topN and "t" in topN
    # return "e" in topN and ("a" in topN or "t" in topN)
    return "e" == topN


    # num_top = sum(1 for c in TOP_CHARS if c in topN)
    # return num_top >= MIN_TOP_CHAR


def ceasearcycle(string):
    cr = Cryptext(string)
    candidates = []
    for i in range(1, 27):
        s = str(cr.shift(i))
        if is_candidate(s):
            candidates.append((i,s))
    return candidates


ShiftStat = namedtuple("ShiftStat", ["shift", "keylen", "pos"])
def vignerecycle(string):
    candidates = []

    for keylen in range(1, MAX_KEY_LENGTH): # round(len(string)/5)):
        # print(keylen)
        for pos in range(0, keylen):
            for shift in range(1, 27):
                ss = ShiftStat(shift, keylen, pos)
                # print(ss)
                selectstring = string[pos::keylen]
                cr = Cryptext(selectstring)
                shiftstring = str(cr.shift(shift))
                if is_candidate(shiftstring):
                    candidates.append(ss)
                    # print("     is candidate")

    return candidates

def group_vignere(string):
    candidates = vignerecycle(string)
    keylens = defaultdict(list)
    for ss in candidates:
        keylens[ss.keylen].append(ss)

    # At least all but 1 of the candidates covers all positions
    narrow_candidates = {kl:sss for kl,sss in keylens.items() if num_pos(sss) >= kl - 1}
    return narrow_candidates

def num_pos(sss):
    uniqe_pos = set(ss.pos for ss in sss)
    return len(uniqe_pos)

def find_keylen_worlds(string):
    groups = group_vignere(string)
    worlds = {}
    for keylen, sss in groups.items():
        bypos = {i:[] for i in range(keylen)}
        for ss in sss:
            bypos[ss.pos].append(ss)
        for pos,sss in bypos.items():
            if len(sss) == 0:
                for shift in range(1,27): # Try all the cases for this one
                    sss.append(ShiftStat(shift, keylen, pos))
        worlds[keylen] = bypos
    return worlds

# This is the first one that takes a long time
def find_candidates(string):
    worlds = find_keylen_worlds(string)
    candidates = []

    for keylen, bypos in worlds.items():
        xlists = [[]]
        for i in range(keylen):
            xlists = cross_multiply(xlists, bypos[i])
        for sslst in xlists:
            cr = Cryptext(string)
            for ss in sslst:
                cr = cr.shift(*ss)
            if is_candidate(str(cr)):
                candidates.append((sslst, str(cr)))
    return candidates

def cross_multiply(nested_lst, lst):
    cross_lists = []
    for l in nested_lst:
        for e in lst:
            lnew = l[:]
            lnew.append(e)
            cross_lists.append(lnew)
    return cross_lists


def narrow_by_words(candidates):
    narrowed = []
    for key, string in candidates:
        hits = count_hits(string, COMMON_WORDS)
        if hits > MIN_WORD_HITS:
            narrowed.append((key,string))
    return narrowed

def count_hits(string, words):
    return sum(string.count(w) for w in words)


def find_vignere_candidates(string):
    cands = find_candidates(string)
    cands = narrow_by_words(cands)
    return cands


def print_candidates(candidates):
    for sslist, string in candidates:
        key = sss_to_key(sslist)
        print("Key({n}): '{k}'".format(n=len(key), k=key))
        print(string)
        print()

def sss_to_key(sslist):
    return "".join(str(Char(num=ss.shift)) for ss in sslist)



# Candidate: ([ShiftStat], str)

def vigenere_search(string, maxkeylen):
    """Return {keylen: [ShiftStat]*keylen} where E is highest frequency for each position"""
    e = Char('e')
    candidates = []
    for keylen in range(1, maxkeylen+1):
        shiftstats = []
        for pos in range(0, keylen):
            select = string[pos::keylen]
            freqs = Frequencies(select)
            maxchar = Char(freqs.by_count[0][0])
            ############ what about ties?
            shift = (e - maxchar).num
            shiftstats.append(ShiftStat(shift, keylen, pos))
        candidates.append((shiftstats, apply_shiftstats(string, shiftstats)))
    return candidates

def apply_shiftstats(string, shiftstats):
    cr = Cryptext(string)
    for ss in shiftstats:
        cr = cr.shift(*ss)
    return str(cr)



def triples(string):
    """Return all consecutive three characters, sorted from most comom to least
    ((chars), #occurences))
    """
    iter1 = iter(string)
    iter2 = iter(string)
    iter3 = iter(string)
    next(iter2)
    next(iter3)
    next(iter3)
    trips = zip(iter1, iter2, iter3)
    return list(trips)

def sort_trips(trips):
    trip_counts = Counter(trips)
    trip_counts = sorted(trip_counts.items(), key=lambda tc: tc[1])
    return trip_counts

def digraphs(string):
    iter1 = iter(string)
    iter2 = iter(string)
    next(iter2)
    pairs = zip(iter1, iter2)
    return list(pairs)

def sort_digraphs(dups):
    counts = Counter(dups)
    counts = sorted(counts.items(), key=lambda dc: dc[1])
    return counts

Replacement = namedtuple("Replacement", ["old", "new"])

class Playfair():
    def __init__(self, string):
        digraphs = list(map(''.join, zip(*[iter(string)]*2))) # from http://stackoverflow.com/questions/9475241/
        self.digraphs = [(Char(c1), Char(c2)) for c1,c2 in digraphs]
        self.size = len(string)
        self._replacements = []

    def fours(self):
        fs = digraphs(self.digraphs)
        fs = [str(a1) + str(a2) + " " + str(b1) + str(b2) for ((a1, a2), (b1, b2)) in fs]
        sfs = sort_digraphs(fs)
        return sfs

    def sixes(self):
        ss = triples(self.digraphs)
        ss = [str(a1) + str(a2) + " " + str(b1) + str(b2) + " " + str(c1) + str(c2) for ((a1, a2), (b1, b2), (c1, c2)) in ss]
        sfs = sort_digraphs(ss)
        return sfs


    def frequencies(self): # percents
        ds = sort_digraphs(self.digraphs)
        frequencies = self.digraph_percents(ds)
        return [("{a}{b}".format(a=str(a), b=str(b)), "{:.3}".format(p)) for (a,b), p in frequencies]

    def digraph_percents(self, sorted_digraph_counts):
        return [(x[0], (x[1]/(self.size/2) * 100)) for x in sorted_digraph_counts]

    def __repr__(self):
        pairs = [str(c1) + str(c2) for c1, c2 in self.digraphs]
        return "Playfair({pairs})".format(pairs=" ".join(pairs))

    def __str__(self):
        return "".join(str(c1) + str(c2) for c1, c2 in self.digraphs)

    def copy(self):
        return copy.deepcopy(self)

    def uppers(self, pair):
        pf = self.copy()

        d = digraph(pair)
        for c1, c2 in pf.digraphs:
            if (c1,c2) == d:
                c1.upper()
                c2.upper()
        return pf

    def r(self, po, pn):

        por = list(po)
        por.reverse()
        por = "".join(por)

        pnr = list(pn)
        pnr.reverse()
        pnr = "".join(pnr)

        return self.replace(po, pn).replace(por, pnr)

    def replace(self, pair_old, pair_new):
        pf = self.copy()
        dold = digraph(pair_old)
        dOLD = digraph(pair_old.upper())
        dnew = digraph(pair_new)
        dNEW = digraph(pair_new.upper())

        ds = []
        for d in self.digraphs:
            if d == dold or d == dOLD:
                ds.append(dnew)
            elif d == dnew or d == dNEW:
                ds.append(dold)
            else:
                ds.append(d)

        pf.digraphs = ds
        pf._replacements.append(Replacement(dold, dnew))
        pf = pf.uppers(pair_new).uppers(pair_old)
        return pf

    def replacements(self):
        for r in self._replacements:
            old = str(r.old[0]) + str(r.old[1])
            new = str(r.new[0]) + str(r.new[1])
            print(old, "->", new)

    def doubles(self):
        pairs = digraphs(self.digraphs)
        return [((a1,a2), (b1,b2)) for ((a1,a2), (b1,b2)) in pairs if a1 == b2 and a2 == b1]





def digraph(pair):
    return (Char(pair[0]), Char(pair[1]))



def clean(string):
    for c in string:
        if c == "\n":
            yield " "
        elif c.isalpha() or c == "." or c == "," or c == " ":
            yield c.lower()



def commadot(string):
    res = []
    for c in string:
        if c == ".":
            res += ["d", "o", "t"]
        elif c == ",":
            res += ["c", "o", "m", "m", "a"]
        else:
            res.append(c)
    return "".join(res)

def remove_doubles_and_js(string):
    """insert x's and replace j's with i's"""
    string = string.replace("j", "i")
    string = string.replace(" ", "")

    res = []
    iter1 = iter(string)
    iter2 = iter(string)
    next(iter2)
    for c1, c2 in zip(iter1, iter2):
        if c1 != c2:
            res.append(c1)
        else:
            res += [c1, "x"]
    return "".join(res)

with open("dickens.txt") as f:
    dickens = list(clean(f.read()))

with open("holmes.txt") as f:
    holmes = list(clean(f.read()))

with open("eyre.txt") as f:
    eyre = list(clean(f.read()))

dickenscode = remove_doubles_and_js(commadot(dickens))
holmescode = remove_doubles_and_js(commadot(holmes))
eyrecode = remove_doubles_and_js(commadot(eyre))

dickens_playfair = Playfair(dickenscode)
holmes_playfair = Playfair(holmescode)
eyre_playfair = Playfair(eyrecode)

pf = Playfair(cipher2)

def justletters(string):
    res = []
    for c in string:
        if c.isalpha():
            res.append(c)
    return "".join(res)



# cr.s("t", "e").s("b", "a").s("o", "f").s("n", "i").s("k", "n").s("k", "s").s("g", "h").s("f", "z").s("m", "q").s("p", "x")
# cr.s("t", "e").s("b", "a").s("o", "f").s("n", "i").s("k", "n").s("k", "s").s("g", "h").s("f", "z").s("m", "q").s("p", "x").s("e", "o").s("o", "m").s("i", "y").f()
# cr.s("t", "e").s("b", "a").s("o", "f").s("n", "i").s("k", "n").s("k", "s").s("g", "h").s("f", "z").s("m", "q").s("p", "x").s("r", "w").s("m", "d")
# cr.s("t", "e").s("b", "a").s("o", "f").s("n", "i").s("k", "n").s("k", "s").s("g", "h").s("f", "z").s("m", "q").s("p", "x").s("r", "w").s("m", "d").s("l", "p").s("c", "w").s("k", "w")


# cr.s("t", "e").s("b", "a").s("o", "f").s("n", "i").s("k", "n").s("k", "s").s("g", "h").s("f", "z").s("m", "q").s("p", "x").s("r", "w").s("m", "d").s("l", "p").s("c", "w").s("k", "w").s("u", "d").s("u", "l").s("m", "f").s("f", "b").s("m", "g").s("p", "b").s("b", "v").s("v", "k").f()


#cr.swap("b", "t").swap("b", "e").swap("i", "h").swap("n", "a").swap("k", "o")

# PROGRESS, 'A' might be wrong
# cr.swap("b", "t").swap("b", "e").swap("i", "h").uppers("t", "e", "h").swap("b", "o").uppers('o').uppers('n').swap("i", "f").uppers("f").swap("k", "r").swap("k", "m").uppers("r", "m").swap("i", "a").uppers("a")

# cr.swap("b", "t").swap("b", "e").swap("i", "h").uppers("t", "e", "h").swap("b", "o").uppers('o').uppers('n').swap("i", "f").uppers("f").swap("k", "r").swap("k", "m").uppers("r", "m").swap("i", "a").uppers("a").swap("w", "i").uppers("i").swap("u", "d").uppers("d").swap("x", "u").swap("q", "c").uppers("c", "u").swap("l", "q").uppers("q").swap("l", "v").uppers("v").swap("y", "b").swap("s", "l").uppers("b", "l").swap("g", "s").uppers("s").swap("z", "w").uppers("w").swap("x", "y").uppers("y", "g").swap("z", "p").uppers("p").swap("j", "k").swap("z", "x").uppers("k", "x")



################################################################################
#********************************************************************************

#crypt.pf.replace("id", "th").replace("dq", "he").replace("of", "ma").replace("ce", "om").replace("qf", "co").replace("et", "mx").replace("wt", "xm")
# crypt.pf.r("dq", "co").r("id", "mx").r("of", "ma")
