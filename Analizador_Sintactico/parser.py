# Se importar la libreria para hacer el parser 
import ply.yacc as yacc 
import sys

# Se importa los tokens del analizador lexicografico 
from Analizador_Lexicografico.analizador import tokens, read_archive

# ----------------------- Construccion de la gramatica ------------------------- #

# Partimos de lo mas general. Estructura del programa completo

def p_programa(p):
    '''
    programa    : TkWith lista_declaraciones TkBegin secuenciacion TkEnd
    '''
    p[0] = p[4]

#------------------------ Este es la definicion del bloque de declaraciones ------------------#
# Esta parte no hay que reportarla 
def p_lista_declaraciones(p):
    '''
    lista_declaraciones : TkVar lista_identificadores TkDosPuntos tipo 
    '''


def p_lista_identificadores(p):
    '''
    lista_identificadores   : lista_identificadores TkComa identificador
    '''

def p_lista_identificadores_identificador(p):
    '''
    lista_identificadores    : identificador
                             | empty
    '''

def p_tipo(p):
    '''
    tipo    : TkInt
            | TkBool
            | TkChar 
            | TkArray
    '''
# ---------------------------------------------------------------------------------------------#

#--------------------------Funcion importante para manejar recursion--------------------------#
# Caso base cuando se termina de procesar la instruccion
def p_empty(p):
    'empty :'
    pass

# ------------------- Esta es la gramatica para el bloque de instrucciones --------------------#

def p_secuenciacion(p):
    '''
    secuenciacion : instruccion TkPuntoYComa secuenciacion
    '''
    if p[3] == None:
        p[0] = p[1]
    else:
        p[0] = ('SECUENCIACION', p[1],p[3])
        

def p_secuenciacion_instruccion(p):
    '''
    secuenciacion   : instruccion
                    | empty
    '''
    p[0] = p[1]

def p_instruccion(p):
    '''
    instruccion : asignacion
                | condicional
                | entrada_salida
                | alcance
                | indeterminado
                | determinado
    '''
    p[0] = p[1]

#------------------- Tipos de instrucciones --------------------------------------------------#
def p_asignacion(p):
    '''
    asignacion  : identificador TkAsignacion expresion 
    '''
    p[0] = ('ASIGNACION',p[1],p[3])

def p_condicional(p):
    '''
    condicional : TkIf expresion_booleana TkHacer secuenciacion TkEnd
                | TkIf expresion_booleana TkHacer secuenciacion TkOtherwise TkHacer secuenciacion TkEnd
    '''

    if (len(p)>6):
        p[0] = ('CONDICIONAL',p[2],p[4],p[7])
    else:
        p[0] = ('CONDICIONAL',p[2],p[4])

def p_alcance(p):
    '''
    alcance : TkWith lista_declaraciones TkBegin secuenciacion TkEnd
    '''
    p[0] = p[4]

def p_entrada_salida(p):
    '''
    entrada_salida  : TkRead identificador
                    | TkPrint expresion
    '''
    p[0] = ('ENTRADA-SALIDA',p[1],p[2])

def p_indeterminado(p):
    '''
    indeterminado   : TkWhile expresion_relacional TkHacer secuenciacion TkEnd
    '''
    p[0] = ('ITERACION INDETERMINADA', p[2], p[4])

def p_determinado(p):
    '''
    determinado     : TkFor identificador TkFrom expresion_aritmetica TkTo expresion_aritmetica TkStep literal TkHacer secuenciacion TkEnd
                    | TkFor identificador TkFrom expresion_aritmetica TkTo expresion_aritmetica TkHacer secuenciacion TkEnd
    '''
    if(len(p)<12):
        p[0] = ('ITERACION DETERMINADA', p[2], p[4], p[6], p[8])
    else:   
        p[0] = ('ITERACION DETERMINADA', p[2], p[4], p[6], p[8], p[10])

#--------------------------------------------------------------------------------------------#
#----------------------------Literales e identificadores-------------------------------------#

def p_identificador(p):
    '''
    identificador   : TkId
    '''
    p[0] = ('VARIABLE',p[1])

def p_literal(p):
    '''
    literal : TkNum 
            | TkTrue 
            | TkFalse 
            | TkCaracter
    '''
    if isinstance(p[1], int):
        p[0] = ('LITERAL ENTERO',str(p[1]))
    elif p[1] == 'true':
        p[0] = ('LITERAL BOOLEANO',p[1])
    elif p[1] == 'false':
        p[0] = ('LITERAL BOOLEANO',p[1])
    else:
        p[0] = ('LITERAL CARACTER',p[1])

#--------------------------------------------------------------------------------------------#
#--------------------------Tipos de expresiones----------------------------------------------#

def p_expresion(p):
    '''
    expresion   : literal
                | expresion_aritmetica 
                | expresion_booleana
                | expresion_relacional
    '''
    p[0] = p[1]


def p_expresion_aritmetica(p):
    '''
    expresion_aritmetica    : literal TkSuma expresion_aritmetica 
                            | literal TkResta expresion_aritmetica
                            | literal TkMult expresion_aritmetica
                            | literal TkDiv expresion_aritmetica
                            | literal TkMod expresion_aritmetica
    '''
    p[0] = (p[2], p[1], p[3])


precedence = (
    ('nonassoc', 'TkMenor','TkMenorIgual','TkMayor', 'TkMayorIgual'),
    ('left', 'TkSuma', 'TkResta'),
    ('left', 'TkMult', 'TkDiv'),
    ('left', 'TkMod')
)

def p_expresion_aritmetica_literal_identificador(p):
    '''
    expresion_aritmetica    : literal
                            | identificador
                            | TkParAbre expresion_aritmetica TkParCierra
                            | empty
    '''
    if p[1] == '(':
        p[0] = p[2]
    else:
        p[0] = p[1]

def p_expresion_booleana(p):
    '''
    expresion_booleana  : literal TkConjuncion expresion_booleana 
                        | literal TkDisyuncion expresion_booleana
                        | literal TkConjuncion expresion_relacional
                        | literal TkDisyuncion expresion_relacional
                        | TkNegacion expresion_booleana
                        | TkNegacion expresion_relacional 
                        | expresion_relacional
    '''
    operadores = {
        '/\\': 'Conjunción',
        '\\/': 'Disyunción',
    }
    if p[1] == 'not':
        p[0] = ('EXP_BOOLEANA',(p[1],p[2]))
    elif len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = ('EXP_BOOLEANA',(operadores[p[2]],p[1],p[3]))        

def p_expresion_booleana_literal_identificador(p):
    '''
    expresion_booleana  : literal
                        | identificador
                        | TkParAbre expresion_booleana TkParCierra
                        | empty
    '''
    if p[1] == '(':
        p[0] = p[2]
    else:
        p[0] = p[1]


def p_expresion_relacional(p):
    '''
    expresion_relacional    : expresion_aritmetica TkMenor expresion_aritmetica
                            | expresion_aritmetica TkMenorIgual expresion_aritmetica 
                            | expresion_aritmetica TkMayor expresion_aritmetica 
                            | expresion_aritmetica TkMayorIgual expresion_aritmetica
                            | expresion_aritmetica TkIgual expresion_aritmetica 
    '''
    operadores = {
        '<': 'Menor que',
        '<=': 'Menor o igual que',
        '>': 'Mayor que',
        '>=': 'Mayor o igual que',
        '=': 'Igual que'
    }
    p[0] = ('BIN_RELACIONAL',(operadores[p[2]],p[1],p[3]))
    



if __name__ == "__main__":
    parser = yacc.yacc()
    entrada = read_archive(sys.argv[1])
    if len(entrada) == 0:
        print('Error introduzca un archivo')
    else:
        result = parser.parse(entrada)
        print(result)