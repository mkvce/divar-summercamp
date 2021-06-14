import sys
import os
import unittest
from final import UserInterface

class TestFinal(unittest.TestCase):
    def test_overall(self):
        with open('in', 'r') as my_input, open('ans', 'r') as ans, open('out', 'w') as my_output:
            original_stdin = sys.stdin
            original_stdout = sys.stdout
            sys.stdin = my_input
            sys.stdout = my_output
            UserInterface()
            my_output.close()
            with open('out', 'r') as my_output:
                self.assertEqual(my_output.read(), ans.read())
            sys.stdin = original_stdin
            sys.stdout = original_stdout
        os.remove('out')

if __name__ == '__main__':
    unittest.main()