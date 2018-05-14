import unittest

# Se importa el analizador lexicografico 
from analizador import Analizador_Lexicografico

analizador_lex = Analizador_Lexicografico()

class AnalizadorLexTester(unittest.TestCase):
    analizador_lex.build()

    # Prueba basica. Prueba provista por el enunciado del proyecto 
    def testPrimeraPrueba(self):
        resultadoEsperado = open("salida1.txt", "r")
        resultadoEsperado = resultadoEsperado.read()
        self.assertEquals(resultadoEsperado, analizador_lex.test("prueba1.txt"))


if __name__ == '__main__':
    unittest.main()