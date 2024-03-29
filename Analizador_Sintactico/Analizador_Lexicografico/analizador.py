# Autores:
#   Daniel Rodriguez 14-10955
#   Yuni Quintero 14-10880

# Aqui se importa la libreria para el reconocimiento de los tokens 

import ply.lex as lex 
import sys

# Diccionario de palabras reservadas
reserved = {
	'begin' : 'TkBegin',
	'if' : 'TkIf',
	'while' : 'TkWhile',
	'bool' : 'TkBool',
	'var' : 'TkVar',
	'with' : 'TkWith',
	'int' : 'TkInt',
	'end' : 'TkEnd',
	'true': 'TkTrue',
	'false': 'TkFalse',
	'not': 'TkNegacion',
	'of': 'TkOf',
	'array': 'TkArray',
	'char': 'TkChar',
	'otherwise': 'TkOtherwise',
	'read': 'TkRead',
	'print': 'TkPrint',
	'for': 'TkFor',
	'from': 'TkFrom',
	'to': 'TkTo',
	'step': 'TkStep',
}


	# Diccionarios de tokens 

tokens = [
	#--------------------------------------------------------------
	# Token para variables 
	'TkId',

	# Token para numero
	'TkNum',

	# Token para caracteres 
	'TkCaracter',
	#---------------------------------------------------------------

	# Tokens para separadores 
	'TkComa',               # ","
	'TkPunto',              # "."
	'TkDosPuntos',          # ":"
	'TkParAbre',            # "("
	'TkParCierra',          # ")"
	'TkCorcheteAbre',       # "["
	'TkCorcheteCierra',     # "]"
	'TkPuntoYComa',			# ";"
	'TkHacer',              # "->"
	'TkAsignacion',         # "<-"
	'TkDesigual',			# "/="

	# Tokens operadores aritmeticos, booleanos, relacionales, o de otro tipo
	'TkSuma',               # "+"
	'TkResta',              # "-"
	'TkMult',               # "*"
	'TkDiv',                # "/"
	'TkMod',                # "%"
	'TkConjuncion',         # "/\"
	'TkDisyuncion',         # "\/"
	'TkMenor',              # "<"
	'TkMenorIgual',         # "<="
	'TkMayor',              # ">"
	'TkMayorIgual',         # ">="
	'TkIgual',              # "="
	'TkSiguienteChar',      # "++"
	'TkAnteriorChar',       # "--"
	'TkValorAscii',         # "#"
	'TkConcatenacion',      # "::"
	'TkShift',              # "$"
] + list(reserved.values())

# Variables globales
numero_linea_anterior = 0

erroresLex = []

entradaDatos = ""

# Reglas para las expresiones regulares de tokens simples de sepradores,
# aritmeticos, booleanos, relacionales, etc

t_TkHacer 			= r'\-\>'
t_TkAsignacion 		= r'\<\-'
t_TkDesigual		= r'\/\='
t_TkSiguienteChar 	= r'\+\+'
t_TkSuma 			= r'\+'
t_TkAnteriorChar 	= r'\-\-'
t_TkResta 			= r'\-'
t_TkMult 			= r'\*'
t_TkConjuncion 		= r'\/\\'
t_TkDisyuncion 		= r'\\\/'
t_TkDiv 			= r'\/'
t_TkMod 			= r'\%'
t_TkNegacion 		= r'not' 
t_TkMenorIgual 		= r'\<\='
t_TkMenor 			= r'\<'
t_TkMayorIgual 		= r'\>\='
t_TkMayor 			= r'\>'
t_TkIgual 			= r'\='
t_TkValorAscii 		= r'\#'
t_TkConcatenacion 	= r'\:\:'
t_TkShift          	= r'\$'
t_TkComa           	= r'\,'
t_TkPunto          	= r'\.'
t_TkDosPuntos      	= r'\:'
t_TkParAbre        	= r'\('
t_TkParCierra      	= r'\)'
t_TkCorcheteAbre   	= r'\['
t_TkCorcheteCierra 	= r'\]'
t_TkPuntoYComa		= r'\;'

#Regla de expresion regular para valores booleanos

t_TkFalse = r'false'
t_TkTrue  = r'true'

# Regla para reconocer errores de tipo "35numero"

# def t_NumStr(self, t):
# 	r'\d+[a-zA-Z]+'
# 	self.print_error_strNum(t)


# Regla para hacer match con un identificador y buscar 
# entre las palabras reservadas

def t_TkId	( t):
	r'[a-zA-Z_][a-zA-Z_0-9]*'
	t.type = reserved.get(t.value,'TkId')    # Check for reserved words
	return t

# Regla para hacer match con un caracter

def t_TkCaracter( t):
	r"'[!-z]'"
	return t 

# Imprimir los Tk_Caracter  

def print_TkCaracter( t):
	return "TkCaracter(" + t.value + ")" + " " + str(t.lineno) + " "

# Funcion para imprimir un token del tipo nombre variable 

def print_TkId( t):
	return 'TkId("' + t.value + '")' + " " + str(t.lineno) + " "

# Regla de expresion regular para los numeros

def t_TkNum( t):
	r'\d+'
	t.value = int(t.value)    
	return t

# Funcion para imprimir un token de tipo numero 

def print_TkNum( t):
	return "TkNum(" + str(t.value) + ")" + " " + str(t.lineno) + " "

# Regla para definir el numero de la line

def t_newline( t):
	r'\n+'
	t.lexer.lineno += len(t.value)

# Columnas

def find_column( input, token):
	line_start = input.rfind('\n', 0, token.lexpos) + 1
	return (token.lexpos - line_start) + 1

# Regla para manejar errores

def t_error( t):
	erroresLex.append(print_error(t))
	t.lexer.skip(1)

# Un String que contiene caracteres ignorados: espacios, tabuladores
# y saltos de lineas

t_ignore  = ' \t'

# def print_error_strNum( t):
# 	caracteresError = "" 
# 	for i in t.value:
# 		if not (ord(i) > 65 and ord(i) < 90) and not (ord(i) > 97 and ord(i) < 122):
# 			caracteresError += i 

# 	erroresLex.append('Error: Caracter inesperado "%s" en la fila' % caracteresError + " " + str(t.lineno) + ", columna " + str(find_column(entradaDatos, t)))
# 	t.lexer.skip(1)

def print_error( t):
	return 'Error: Caracter inesperado "%s" en la fila' % t.value[0] + " " + str(t.lineno) + ", columna " + str(find_column(entradaDatos, t))

# Se construye el lexer


# Funcion para leer el archivo de entrada 
def read_archive(archive):
	entrada = open(archive, "r")
	string = entrada.read()
	
	# Se llama a la funcion para testear el lexer 
	return string

# Funcion que responde a la pregunta. El token esta en la misma linea ?
def mismaLinea(linea_actual):
	global numero_linea_anterior
	if linea_actual != numero_linea_anterior:
		numero_linea_anterior = linea_actual
		return "\n"
	else:
		return ", "


lexer = lex.lex()
# Se prueba el tester
def test( data):
	salida = ""
	salidaBuena = ""
	
	global erroresLex
	erroresLex = []
	numero_linea_anterior = 0	

	data = read_archive(data)
	lexer.input(data)
	entradaDatos = data 
	for tok in lexer:
		
		if tok.type == 'TkNum':
			salidaBuena = salidaBuena + mismaLinea(tok.lineno) + print_TkNum(tok) +  str(find_column(data, tok))
		elif tok.type == 'TkId':
			salidaBuena = salidaBuena + mismaLinea(tok.lineno) + print_TkId(tok) + str(find_column(data, tok))
		elif tok.type == 'TkCaracter':
			salidaBuena = salidaBuena + mismaLinea(tok.lineno) + print_TkCaracter(tok) + str(find_column(data, tok))
		else:
			salidaBuena = salidaBuena + mismaLinea(tok.lineno) + tok.type + " " + str(tok.lineno) + " " + str(find_column(data, tok))

	# Si existen errores en el archivo de entrada solo se tiene que imprimir tales 
	# errores no los otros tokens 
	if len(erroresLex) > 0:
		salida = ""
		for i in erroresLex:
			salida = salida + i + "\n"
		salida = salida[:-1]

	return salida 

if __name__ == "__main__":
        print(test(sys.argv[1]))
