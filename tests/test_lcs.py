import random, unittest
from lcs import lcs_recursive,lcs_hirschberg,lcs_tabular
def subseq(s,t):
    it=iter(t)
    return all(any(c==x for x in it) for c in s)
class TestLCS(unittest.TestCase):
    def check(self,a,b,n,fs):
        for f in fs:
            with self.subTest(fn=f.__name__,a=a,b=b):
                s=f(a,b); self.assertEqual(len(s),n); self.assertTrue(subseq(s,a) and subseq(s,b))
    def test_examples(self):
        for a,b,n in [('ABCDEF','ACEF',4),('','ABC',0),('','',0),('ABC','XYZ',0),('AAAA','AA',2),('ABCBDAB','BDCABA',4)]:
            self.check(a,b,n,[lcs_recursive,lcs_hirschberg,lcs_tabular])
    def test_random(self):
        r=random.Random(20261114)
        for _ in range(100):
            a=''.join(r.choices('ABCD',k=r.randrange(9))); b=''.join(r.choices('ABCD',k=r.randrange(9)))
            self.check(a,b,len(lcs_tabular(a,b)),[lcs_recursive,lcs_hirschberg,lcs_tabular])
    def test_theme(self):
        a='ACCGGTCGAGTGCGCGGAAGCCGGCCGAA'; b='GTCGTTCGGAATGCCGTTGCTCTGTAAA'; s='GTCGTCGGAAGCCGGCCGAA'
        self.assertTrue(subseq(s,a) and subseq(s,b))
        self.check(a,b,20,[lcs_hirschberg,lcs_tabular])
    def test_asymmetric(self):
        r=random.Random(31); a=''.join(r.choices('ABCD',k=1000)); b=''.join(r.choices('ABCD',k=53))
        self.check(a,b,len(lcs_tabular(a,b)),[lcs_hirschberg,lcs_tabular])
        self.check(b,a,len(lcs_tabular(a,b)),[lcs_hirschberg,lcs_tabular])
    def test_types(self):
        for f in (lcs_recursive,lcs_hirschberg,lcs_tabular):
            with self.assertRaises(TypeError): f(None,'a')
