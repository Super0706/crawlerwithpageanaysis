import unittest
from component.metrics_worker import word_counter
import os
from pathlib import Path
Path('C:\Program Files').parent

class WordCounterTest(unittest.TestCase):


    def find_word_count_test(self,source_code):
        print(source_code)


def main():
    unittest.main()
    source_code_file = open(str(Path(os.getcwd()).parent.parent) + os.sep + "data" + os.sep + 'index.html', 'r')
    source_code = source_code_file.readlines()
    print(source_code)
    WordCounterTest().find_word_count(source_code)

if __name__ == '__main__':
    main()
