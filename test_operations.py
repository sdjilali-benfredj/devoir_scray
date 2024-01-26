# test_operations.py

import unittest
from app import envoie

class TestOperations(unittest.TestCase):
    def test_envoie(self):
        # Teste si la fonction envoie() fonctionne correctement
        self.assertEqual(envoie, True)

if __name__ == '__main__':
    unittest.main()
