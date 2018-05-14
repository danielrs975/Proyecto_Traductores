import unittest

# Se importa el analizador lexicografico 
from analizador import Analizador_Lexicografico



class AnalizadorLexTester(unittest.TestCase):
   

    # Prueba basica. Prueba provista por el enunciado del proyecto 
    def testPrimeraPrueba(self):
        analizador_lex = Analizador_Lexicografico()
        analizador_lex.build()
        resultadoEsperado = open("salida1.txt", "r")
        resultadoEsperado = resultadoEsperado.read()
        self.assertEqual(resultadoEsperado, analizador_lex.test("prueba1.txt"))

    # Prueba para ver si es correcto el formato de salida cuando hay errores en el
    # archivo de entrada.
    def testCaptandoErrores(self):
        analizador_lex = Analizador_Lexicografico()
        analizador_lex.build()
        resultadoEsperado = open("salida2.txt")
        resultadoEsperado = resultadoEsperado.read()
        self.assertEqual(resultadoEsperado, analizador_lex.test("prueba2.txt"))


if __name__ == '__main__':
    unittest.main()