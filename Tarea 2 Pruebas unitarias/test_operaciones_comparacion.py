# test_operaciones_comparacion.py

import unittest
from operaciones_comparacion import (
    es_mayor_que,
    es_menor_que,
    es_mayor_o_igual_que,
    es_menor_o_igual_que,
    son_iguales
)

class TestOperacionesComparacion(unittest.TestCase):

    def test_es_mayor_que(self):
        self.assertTrue(es_mayor_que(5, 3))
        self.assertFalse(es_mayor_que(3, 5))
        self.assertFalse(es_mayor_que(5, 5))

    def test_es_menor_que(self):
        self.assertTrue(es_menor_que(2, 4))
        self.assertFalse(es_menor_que(4, 2))
        self.assertFalse(es_menor_que(4, 4))

    def test_es_mayor_o_igual_que(self):
        self.assertTrue(es_mayor_o_igual_que(6, 3))
        self.assertTrue(es_mayor_o_igual_que(5, 5))
        self.assertFalse(es_mayor_o_igual_que(2, 4))

    def test_es_menor_o_igual_que(self):
        self.assertTrue(es_menor_o_igual_que(2, 5))
        self.assertTrue(es_menor_o_igual_que(4, 4))
        self.assertFalse(es_menor_o_igual_que(6, 4))

    def test_son_iguales(self):
        self.assertTrue(son_iguales(7, 7))
        self.assertFalse(son_iguales(1, 2))

#Casos aparte con decimales, cero, negativos y error intencional

    def test_casos_decimal_y_negativos(self):
        # Decimales
        self.assertTrue(es_mayor_que(5.5, 2.3))
        self.assertFalse(es_menor_que(3.3, 3.3))  

        # Negativos
        self.assertTrue(es_menor_que(-5, -1))
        self.assertFalse(es_mayor_que(-3, 0))

        # Cero
        self.assertTrue(es_menor_o_igual_que(0, 0))
        self.assertFalse(es_mayor_que(0, 10))

def es_mayor_que(a, b):
    return a < b  

if __name__ == '__main__':
    unittest.main()



