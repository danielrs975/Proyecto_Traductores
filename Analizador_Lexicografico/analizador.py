# Autores:
#   Daniel Rodriguez 14-10955
#   Yuni Quintero 14-10880

# Aqui se importa la libreria para el reconocimiento de los tokens 

import ply.lex as lex 

# Diccionario de palabras reservadas

class Analizador_Lexicografico(object):
	# Variables globales
	numero_linea_anterior = 0

	erroresLex = []

	entradaDatos = ""

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
		'TkLlaveAbre',          # "{"
		'TkLlaveCierra',        # "}"
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
	t_TkLlaveAbre      	= r'\{'
	t_TkLlaveCierra    	= r'\}'
	t_TkPuntoYComa		= r'\;'

	#Regla de expresion regular para valores booleanos

	t_TkFalse = r'False'
	t_TkTrue  = r'True'

	# Regla para reconocer errores de tipo "35numero"

	# def t_NumStr(self, t):
	# 	r'\d+[a-zA-Z]+'
	# 	self.print_error_strNum(t)


	# Regla para hacer match con un identificador y buscar 
	# entre las palabras reservadas

	def t_TkId	(self, t):
		r'[a-zA-Z_][a-zA-Z_0-9]*'
		t.type = self.reserved.get(t.value,'TkId')    # Check for reserved words
		return t

	# Regla para hacer match con un caracter

	def t_TkCaracter(self, t):
		r"'[!-z]'"
		return t 

	# Imprimir los Tk_Caracter  

	def print_TkCaracter(self, t):
		return "TkCaracter(" + t.value + ")" + " " + str(t.lineno) + " "

	# Funcion para imprimir un token del tipo nombre variable 

	def print_TkId(self, t):
		return 'TkId("' + t.value + '")' + " " + str(t.lineno) + " "

	# Regla de expresion regular para los numeros

	def t_TkNum(self, t):
		r'\d+'
		t.value = int(t.value)    
		return t

	# Funcion para imprimir un token de tipo numero 

	def print_TkNum(self, t):
		return "TkNum(" + str(t.value) + ")" + " " + str(t.lineno) + " "

	# Regla para definir el numero de la line

	def t_newline(self, t):
		r'\n+'
		t.lexer.lineno += len(t.value)

	# Columnas

	def find_column(self, input, token):
		line_start = input.rfind('\n', 0, token.lexpos) + 1
		return (token.lexpos - line_start) + 1

	# Regla para manejar errores

	def t_error(self, t):
		self.erroresLex.append(self.print_error(t))
		t.lexer.skip(1)

	# Un String que contiene caracteres ignorados: espacios, tabuladores
	# y saltos de lineas

	t_ignore  = ' \t'

	# def print_error_strNum(self, t):
	# 	caracteresError = "" 
	# 	for i in t.value:
	# 		if not (ord(i) > 65 and ord(i) < 90) and not (ord(i) > 97 and ord(i) < 122):
	# 			caracteresError += i 

	# 	self.erroresLex.append('Error: Caracter inesperado "%s" en la fila' % caracteresError + " " + str(t.lineno) + ", columna " + str(self.find_column(self.entradaDatos, t)))
	# 	t.lexer.skip(1)

	def print_error(self, t):
		return 'Error: Caracter inesperado "%s" en la fila' % t.value[0] + " " + str(t.lineno) + ", columna " + str(self.find_column(self.entradaDatos, t))

	# Se construye el lexer

	def build(self, **kwargs):
		self.lexer = lex.lex(module=self, **kwargs)

	# Funcion para leer el archivo de entrada 
	def read_archive(self, archive):
		entrada = open(archive, "r")
		string = entrada.read()
		
		# Se llama a la funcion para testear el lexer 
		return string

	# Funcion que responde a la pregunta. El token esta en la misma linea ?
	def mismaLinea(self, linea_actual):
		if linea_actual != self.numero_linea_anterior:
			self.numero_linea_anterior = linea_actual
			return "\n"
		else:
			return ", "

	# Se prueba el tester
	def test(self, data):
		salida = ""
		
		self.erroresLex = []
		self.numero_linea_anterior = 0	

		data = self.read_archive(data)
		self.lexer.input(data)
		self.entradaDatos = data 
		for tok in self.lexer:
			
			if tok.type == 'TkNum':
				salida = salida + self.mismaLinea(tok.lineno) + self.print_TkNum(tok) +  str(self.find_column(data, tok))
			elif tok.type == 'TkId':
				salida = salida + self.mismaLinea(tok.lineno) + self.print_TkId(tok) + str(self.find_column(data, tok))
			elif tok.type == 'TkCaracter':
				salida = salida + self.mismaLinea(tok.lineno) + self.print_TkCaracter(tok) + str(self.find_column(data, tok))
			else:
				salida = salida + self.mismaLinea(tok.lineno) + tok.type + " " + str(tok.lineno) + " " + str(self.find_column(data, tok))

		# Si existen errores en el archivo de entrada solo se tiene que imprimir tales 
		# errores no los otros tokens 
		if len(self.erroresLex) > 0:
			salida = ""
			for i in self.erroresLex:
				salida = salida + i + "\n"
			salida = salida[:-1]
		else:
			salida = salida[1:] 
		return salida 
