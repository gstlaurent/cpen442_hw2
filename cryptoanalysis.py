from collections import Counter, namedtuple, defaultdict
from itertools import groupby
import pprint

# everything uses lowercase

ALPHAS = "abcdefghijklmnopqrstuvwxyz"
MAX_LENGTH = 80
MAX_KEY_LENGTH = 12
TOP_DEPTH = 5
MIN_WORD_HITS = 3

COMMON_WORDS = ['the', 'be', 'am', 'is', 'were', 'to', 'of', 'and', 'in', 'that', 'have']

cipher1 = "entehbitgqiesfkgzfgktlxwktubektbwktqerrffnubitnbekttnbtkbitkeerfgfaeswbtvtnbstrfnwggxaaegtubetnbtkfukfzwnvkeeruebitzfgktqtwctufbbitueekydfnebitkgqiesfkfnuqenuxqbtuhkerytnqibeytnqixnbwsitifuyttnwnbkeuxqtubefssbitdexnvsfuwtgfnuvtnbstrtnwnbitkeeruebswnqesnztnbbikexvibitekutfsqexnbstggbwrtguebwhitbeejfgtkwexgcwtzehbitatkhekrfnqtwbrxgbifctaxbiwrbetplxwgwbtbekbxktqerrfhekitzfgqengqwexgbifbitzfgnebfatkhtqbbdatehrfnsdytfxbd"

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

    def map(self, fun):
        cr = Cryptext(str(self))
        cr.chars = [fun(c) for c in cr.chars]
        return cr



class Char():
    def __init__(self, letter=None, num=None):
        if letter:
            letter = letter.lower()
            self.num = ord(letter) - 96
        elif num:
            self.num = num
        else:
            assert(False)

    # def __eq__(self, o):
        # return self.num == o.num
    # def __hash__(self):
        # return self.num

    def __repr__(self):
        return "Char({c}, {n})".format(c=str(self), n=self.num) 
    def __str__(self):
        return str(chr(96 + self.num))

    def shift_left(self, dist):
        num = (self.num + 26 - dist) % 26
        if num == 0:
            num = 26
        return Char(num=num)


def freqlengths(cr, maxkeylen):
    for i in range(1, maxkeylen): 
        print(i)
        cc = Cryptext(str(cr)[::i])
        print(cc)
        cc.print_frequencies()
        print()


class Freqeuncies():
    def __init__(self, string):
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
    freq = Freqeuncies(string)
    top5 = freq.top(TOP_DEPTH)
    return "e" in top5 and ("a" in top5 or "t" in top5)


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
        print("Key: '{}'".format(sss_to_key(sslist)))
        print(string)
        print()

def sss_to_key(sslist):
    return "".join(str(Char(num=ss.shift)) for ss in sslist)

