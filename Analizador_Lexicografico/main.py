# Autores:
#   Daniel Rodriguez 14-10955
#   Yuni Quintero 14-10880


from analizador import Analizador_Lexicografico
import sys

# Programa que sirve como intermediario entre la linea de comandos
# y el analizador lexicografico 
def main(entrada):
    analizador = Analizador_Lexicografico()
    analizador.build()
    print(analizador.test(entrada))

main(sys.argv[1])