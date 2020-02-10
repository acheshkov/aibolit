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

import argparse
import csv
import os
import time
from functools import partial
from multiprocessing import Pool
from pathlib import Path

from aibolit.metrics.entropy.entropy import Entropy
from aibolit.patterns.nested_blocks.nested_blocks import NestedBlocks, BlockType
from aibolit.patterns.var_middle.var_middle import VarMiddle

# You need to download the archive here:
# https://dibt.unimol.it/report/readability/files/readability.zip
# Unzip and put it into the executable's current directory

parser = argparse.ArgumentParser(description='Compute Readability score')
parser.add_argument(
    '--filename',
    help='path for file with a list of Java files',
    required=True)

args = parser.parse_args()
dir_path = os.path.dirname(os.path.realpath(__file__))


def log_result(result, file_to_write):
    """ Save result to csv file. """
    with open(file_to_write, 'a', newline='\n', encoding='utf-8') as csv_file:
        writer = csv.writer(
            csv_file, delimiter=';',
            quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(
            [result[0], len(result[1]), len(result[2]), len(result[3]),
             result[4], result[1], result[2], result[3]]
        )


def execute_python_code_in_parallel_thread(file):
    """ This runs in a separate thread. """
    var_numbers = VarMiddle().value(file)
    nested_for_blocks = NestedBlocks(2, block_type=BlockType.FOR).value(file)
    nested_if_blocks = NestedBlocks(2, block_type=BlockType.IF).value(file)
    entropy = Entropy().value(file)
    return file, var_numbers, nested_for_blocks, nested_if_blocks, entropy


if __name__ == '__main__':
    start = time.time()

    path = '04'
    os.makedirs(path, exist_ok=True)
    filename = '04/04-find-patterns.csv'
    with open(filename, 'w', newline='\n', encoding='utf-8') as csv_file:
        writer = csv.writer(
            csv_file, delimiter=';',
            quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow([
            'filename', 'var_middle_number', 'nested_for_number',
            'nested_if_number', 'entropy', 'lines_for_var_middle',
            'lines_for_cycle', 'lines_for_if']
        )

    pool = Pool(20)
    handled_files = []
    log_func = partial(log_result, file_to_write=filename)
    with open(args.filename, 'r') as f:
        for i in f.readlines():
            java_file = str(Path(dir_path, i)).strip()
            pool.apply_async(
                execute_python_code_in_parallel_thread,
                args=(java_file,),
                callback=log_func)

    pool.close()
    pool.join()

    end = time.time()
    print('It took {} seconds'.format(str(end - start)))
