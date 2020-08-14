from io import StringIO
import textwrap
from unittest import TestCase

from textbisect import text_bisect, text_bisect_left, text_bisect_right


testtext = textwrap.dedent("""\
                           alpha
                           bravo
                           charlie
                           delta
                           echo
                           foxtrot
                           golf
                           hotel
                           india
                           juillet
                           kilo
                           lima
                           mike
                           november
                           oscar
                           papa
                           quebec
                           romeo
                           sierra
                           tango
                           uniform
                           victor
                           whiskey
                           x-ray
                           yankee
                           zulu
                           """)

# These are the positions in which each of the line of the above string start:
#
# alpha    0
# bravo    6
# charlie  12
# delta    20
# echo     26
# foxtrot  31
# golf     39
# hotel    44
# india    50
# juillet  56
# kilo     64
# lima     69
# mike     74
# november 79
# oscar    88
# papa     94
# quebec   99
# romeo    106
# sierra   112
# tango    119
# uniform  125
# victor   133
# whiskey  140
# x-ray    148
# yankee   154
# zulu     161
#          166 (length of file, or position of next character to be appended)


testtext2 = textwrap.dedent("""\
                            1
                            003
                            fivey
                            seven07
                            ninenine9
                            eleven00011
                            """)

# These are the positions in which each of the line of the above string start:
#
# 1           0
# 003         2
# fivey       6
# seven07     12
# ninenine9   20
# eleven00011 30
#             42 (length of file, or position of next character to be appended)


class TestTextBisect(TestCase):

    def test_text_bisect(self):
        self.f = StringIO(testtext)

        # Beginning of file
        pos = text_bisect(self.f, 'alice')
        self.assertEqual(pos, 0)
        self.assertEqual(pos, self.f.tell())

        # End of file
        pos = text_bisect(self.f, 'zuzu')
        self.assertEqual(pos, 166)
        self.assertEqual(pos, self.f.tell())

        # Somewhere in the file
        pos = text_bisect(self.f, 'somewhere')
        self.assertEqual(pos, 119)
        self.assertEqual(pos, self.f.tell())

        # Bisect left
        pos = text_bisect_left(self.f, 'lima')
        self.assertEqual(pos, 69)
        self.assertEqual(pos, self.f.tell())

        # Bisect right
        pos = text_bisect_right(self.f, 'lima')
        self.assertEqual(pos, 74)
        self.assertEqual(pos, self.f.tell())

        # Beginning of file part
        pos = text_bisect(self.f, 'bob', lo=106)
        self.assertEqual(pos, 106)
        self.assertEqual(pos, self.f.tell())

        # Beginning of file part starting in middle of line
        pos = text_bisect(self.f, 'bob', lo=108)
        self.assertEqual(pos, 108)
        self.assertEqual(pos, self.f.tell())
        pos = text_bisect(self.f, 'nick', lo=108)
        self.assertEqual(pos, 112)
        self.assertEqual(pos, self.f.tell())

        # Beginning of file part starting in end of line
        pos = text_bisect(self.f, 'bob', lo=111)
        self.assertEqual(pos, 112)
        self.assertEqual(pos, self.f.tell())

        # Beginning of file part starting at end of file
        pos = text_bisect(self.f, 'bob', lo=166)
        self.assertEqual(pos, 166)
        self.assertEqual(pos, self.f.tell())
        pos = text_bisect(self.f, 'bob', lo=165)
        self.assertEqual(pos, 166)
        self.assertEqual(pos, self.f.tell())

        # End of file part
        pos = text_bisect(self.f, 'nick', hi=73)
        self.assertEqual(pos, 74)
        self.assertEqual(pos, self.f.tell())

        # End of file part ending in middle of line
        with self.assertRaises(EOFError):
            text_bisect(self.f, 'nick', hi=71)

        # Beginning and end of file
        pos = text_bisect(self.f, 'nick', lo=64, hi=93)
        self.assertEqual(pos, 79)
        self.assertEqual(pos, self.f.tell())
        pos = text_bisect(self.f, 'george', lo=64, hi=93)
        self.assertEqual(pos, 64)
        self.assertEqual(pos, self.f.tell())
        pos = text_bisect(self.f, 'tango', lo=64, hi=93)
        self.assertEqual(pos, 94)
        self.assertEqual(pos, self.f.tell())

        # Beginning and end of file, left/right
        pos = text_bisect_left(self.f, 'kilo', lo=64, hi=93)
        self.assertEqual(pos, 64)
        self.assertEqual(pos, self.f.tell())
        pos = text_bisect_right(self.f, 'kilo', lo=64, hi=93)
        self.assertEqual(pos, 69)
        self.assertEqual(pos, self.f.tell())
        pos = text_bisect_left(self.f, 'oscar', lo=64, hi=93)
        self.assertEqual(pos, 88)
        self.assertEqual(pos, self.f.tell())
        pos = text_bisect_right(self.f, 'oscar', lo=64, hi=93)
        self.assertEqual(pos, 94)
        self.assertEqual(pos, self.f.tell())
        pos = text_bisect_right(self.f, 'papa', lo=64, hi=93)
        self.assertEqual(pos, 94)
        self.assertEqual(pos, self.f.tell())

    def test_text_bisect_with_key(self):
        self.f = StringIO(testtext2)

        # Beginning of file
        pos = text_bisect(self.f, '', key=len)
        self.assertEqual(pos, 0)
        self.assertEqual(pos, self.f.tell())

        # End of file
        pos = text_bisect(self.f, 'twelvetwelve', key=len)
        self.assertEqual(pos, 42)
        self.assertEqual(pos, self.f.tell())

        # Somewhere in the file
        pos = text_bisect(self.f, 'sixsix', key=len)
        self.assertEqual(pos, 12)
        self.assertEqual(pos, self.f.tell())

        # Bisect left
        pos = text_bisect_left(self.f, 'fiver', key=len)
        self.assertEqual(pos, 6)
        self.assertEqual(pos, self.f.tell())

        # Bisect right
        pos = text_bisect_right(self.f, 'fiver', key=len)
        self.assertEqual(pos, 12)
        self.assertEqual(pos, self.f.tell())

        # Beginning of file part
        pos = text_bisect(self.f, '02', lo=12, key=len)
        self.assertEqual(pos, 12)
        self.assertEqual(pos, self.f.tell())

        # Beginning of file part starting in middle of line
        pos = text_bisect(self.f, '02', lo=8, key=len)
        self.assertEqual(pos, 8)
        self.assertEqual(pos, self.f.tell())
        pos = text_bisect(self.f, 'four', lo=8, key=len)
        self.assertEqual(pos, 12)
        self.assertEqual(pos, self.f.tell())

        # Beginning of file part starting in end of line
        pos = text_bisect(self.f, '02', lo=5, key=len)
        self.assertEqual(pos, 6)
        self.assertEqual(pos, self.f.tell())

        # Beginning of file part starting at end of file
        pos = text_bisect(self.f, 'any', lo=41, key=len)
        self.assertEqual(pos, 42)
        self.assertEqual(pos, self.f.tell())
        pos = text_bisect(self.f, 'any', lo=41, key=len)
        self.assertEqual(pos, 42)
        self.assertEqual(pos, self.f.tell())

        # End of file part
        pos = text_bisect(self.f, 'ten=ten=10', hi=11, key=len)
        self.assertEqual(pos, 12)
        self.assertEqual(pos, self.f.tell())

        # End of file part ending in middle of line
        with self.assertRaises(EOFError):
            text_bisect(self.f, 'eleven=0011', hi=32, key=len)

        # Beginning and end of file
        pos = text_bisect(self.f, 'four', lo=6, hi=29, key=len)
        self.assertEqual(pos, 6)
        self.assertEqual(pos, self.f.tell())
        pos = text_bisect(self.f, 'eight008', lo=6, hi=29, key=len)
        self.assertEqual(pos, 20)
        self.assertEqual(pos, self.f.tell())
        pos = text_bisect(self.f, 'twelvetwelve', lo=6, hi=29, key=len)
        self.assertEqual(pos, 30)
        self.assertEqual(pos, self.f.tell())

        # Beginning and end of file, left/right
        pos = text_bisect_left(self.f, 'fiver', lo=6, hi=29, key=len)
        self.assertEqual(pos, 6)
        self.assertEqual(pos, self.f.tell())
        pos = text_bisect_right(self.f, 'fiver', lo=6, hi=29, key=len)
        self.assertEqual(pos, 12)
        self.assertEqual(pos, self.f.tell())
        pos = text_bisect_left(self.f, 'nine=nine', lo=6, hi=29, key=len)
        self.assertEqual(pos, 20)
        self.assertEqual(pos, self.f.tell())
        pos = text_bisect_right(self.f, 'nine=nine', lo=6, hi=29, key=len)
        self.assertEqual(pos, 30)
        self.assertEqual(pos, self.f.tell())
        pos = text_bisect_right(self.f, 'twelvetwelve', lo=6, hi=29, key=len)
        self.assertEqual(pos, 30)
        self.assertEqual(pos, self.f.tell())
