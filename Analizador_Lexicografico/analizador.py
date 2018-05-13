# Aqui se importa la libreria para el reconocimiento de los tokens 

import ply.lex as lex 

# Diccionario de palabras reservadas

reserved = {
	'begin' : 'TkBegin',
	'if' : 'TkIf',
	'while' : 'TkWhile',
	'bool' : 'TkBool',
	'var' : 'TkVar',
	'with' : 'TkWith',
	'int' : 'TkInt',
	'End' : 'TkEnd',
	'True': 'TkTrue',
	'False': 'TkFalse',
	'not': 'TkNegacion',
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
	'TkHacer',              # "->"
	'TkAsignacion',         # "<-"

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
t_TkSiguienteChar 	= r'\+\+'
t_TkSuma 			= r'\+'
TkAnteriorChar 		= r'\-\-'
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

#Regla de expresion regular para valores booleanos

t_TkFalse = r'False'
t_TkTrue  = r'True'


# Regla para hacer match con un identificador y buscar 
# entre las palabras reservadas

def t_TkId(t):
	r'[a-zA-Z_][a-zA-Z_0-9]*'
	t.type = reserved.get(t.value,'TkId')    # Check for reserved words
	return t

# Regla para hacer match con un caracter

def t_TkCaracter(t):
    r"'[!-z]'"
    return t 

# Imprimir los Tk_Caracter  

def print_TkCaracter(t):
    return "TkCaracter(" + t.value + ")" + " " + str(t.lineno) + " " + str(t.lexpos)

# Funcion para imprimir un token del tipo nombre variable 

def print_TkId(t):
    return 'TkId("' + t.value + '")' + " " + str(t.lineno) + " " + str(t.lexpos)

# Regla de expresion regular para los numeros

def t_TkNum(t):
	r'\d+'
	t.value = int(t.value)    
	return t

# Funcion para imprimir un token de tipo numero 

def print_TkNum(t):
    return "TkNum(" + str(t.value) + ")" + " " + str(t.lineno) + " " + str(t.lexpos)

# Regla para definir el numero de la line

def t_newline(t):
	r'\n+'
	t.lexer.lineno += len(t.value)

# Columnas

def find_column(input, token):
	line_start = input.rfind('\n', 0, token.lexpos) + 1
	return (token.lexpos - line_start) + 1

# Regla para manejar errores

def t_error(t):
	print("Caracter ilegal '%s'" % t.value[0])
	t.lexer.skip(1)

# Regla de expresion regular de literales para caracteres

# literals = r'[(-=^\]+|,.)*"{}a-zA-Z_0-9'

# Un String que contiene caracteres ignorados: espacios, tabuladores
# y saltos de lineas

t_ignore  = ' \t\n'

# Se construye el lexer

lexer = lex.lex()

data = '''
with\nvar 7contador : char\nbegin\ncontador <- True .\nend\n
'''

lexer.input(data)

# Variable que va a almacenar la salida del analizador 
salida = ""

for tok in lexer:
    if tok.type == 'TkNum':
        salida = salida + " " + print_TkNum(tok)
    elif tok.type == 'TkId':
        salida = salida + " " + print_TkId(tok)
    elif tok.type == 'TkCaracter':
        salida = salida + " " + print_TkCaracter(tok)
    else:
        salida = salida + " " + tok.type + " " + str(tok.lineno) + " " + str(tok.lexpos)

print(salida) 