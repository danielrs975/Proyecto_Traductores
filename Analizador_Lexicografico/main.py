from analizador import Analizador_Lexicografico
import sys

def main(entrada):
    analizador = Analizador_Lexicografico()
    analizador.build()
    print(analizador.test(entrada))

main(sys.argv[1])