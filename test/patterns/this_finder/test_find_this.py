# The MIT License (MIT)
#
# Copyright (c) 2020 Aibolit
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NON-INFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import os
from unittest import TestCase
from aibolit.patterns.this_finder.this_finder import ThisFinder


class TestFindThis(TestCase):
    cur_dir = os.path.dirname(os.path.realpath(__file__))
    pattern = ThisFinder()

    def test_several(self):
        lines = self.pattern.value(self.cur_dir + '/several.java')
        self.assertEqual(lines, [4, 10, 20])

    def test_simple1(self):
        lines = self.pattern.value(self.cur_dir + '/double_this.java')
        self.assertEqual(lines, [12])

    def test_simple2(self):
        lines = self.pattern.value(self.cur_dir + '/init_block.java')
        self.assertEqual(lines, [])

    def test_simple22(self):
        lines = self.pattern.value(self.cur_dir + '/init_static_block.java')
        self.assertEqual(lines, [])

    def test_simple3(self):
        lines = self.pattern.value(self.cur_dir + '/autocloseable.java')
        self.assertEqual(lines, [4, 14, 31])

    def test_simple4(self):
        lines = self.pattern.value(self.cur_dir + '/one_line_this.java')
        self.assertEqual(lines, [11])

    def test_simple5(self):
        lines = self.pattern.value(self.cur_dir + '/one_line_usage.java')
        self.assertEqual(lines, [12])

    def test_simple6(self):
        lines = self.pattern.value(self.cur_dir + '/super.java')
        self.assertEqual(lines, [12])

    def test_simple7(self):
        lines = self.pattern.value(self.cur_dir + '/holy_moly_constructor.java')
        self.assertEqual(lines, [47])

    def test_simple9(self):
        lines = self.pattern.value(self.cur_dir + '/super_this.java')
        self.assertEqual(lines, [15, 25, 51, 62, 76, 87, 101])
