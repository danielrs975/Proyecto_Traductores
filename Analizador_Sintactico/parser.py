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
    p[0] = "SECUENCIACION\n" + p[4]

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
        p[0] = p[1] + "\n" + p[3]
        

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
    '''
    p[0] = p[1]

#------------------- Tipos de instrucciones --------------------------------------------------#
def p_asignacion(p):
    '''
    asignacion  : identificador TkAsignacion expresion 
    '''
    p[0] = "\tASIGNACION\n\t\t- contenedor: " + p[1] + p[3]

def p_condicional(p):
    '''
    condicional : TkIf expresion_booleana TkHacer secuenciacion TkEnd
                | TkIf expresion_relacional TkHacer secuenciacion TkEnd
    '''
    p[0] = "\tCONDICIONAL:\n\t\t- guardia: " + p[2] + "\n\t\t- exito: " + p[4]

def p_entrada_salida(p):
    '''
    entrada_salida  : TkRead identificador
                    | TkPrint expresion
    '''
    p[0] = "ENTRADA-SALIDA\n\t\t" + p[1] + " " + p[2]

#--------------------------------------------------------------------------------------------#
#----------------------------Literales e identificadores-------------------------------------#

def p_identificador(p):
    '''
    identificador   : TkId
    '''
    p[0] = "VARIABLE\n\t\t\t- identificador: " + p[1]

def p_literal(p):
    '''
    literal : TkNum 
            | TkTrue 
            | TkFalse 
            | TkCaracter
    '''
    if isinstance(p[1], int):
        p[0] = "\n\t\t- expresion: LITERAL ENTERO\n\t\t\t- valor: " + str(p[1])
    elif p[1] == 'true':
        p[0] = "\n\t\t- expresion: LITERAL BOOLEANO\n\t\t\t- valor: " + p[1]
    elif p[1] == 'false':
        p[0] = "\n\t\t- expresion: LITERAL BOOLEANO\n\t\t\t- valor: " + p[1]
    else:
        p[0] = "\n\t\t- expresion: LITERAL CARACTER\n\t\t\t- valor: " + p[1]

#--------------------------------------------------------------------------------------------#
#--------------------------Tipos de expresiones----------------------------------------------#

def p_expresion(p):
    '''
    expresion   : literal
                | expresion_aritmetica 
                | expresion_booleana
    '''
    p[0] = p[1]


def p_expresion_aritmetica(p):
    '''
    expresion_aritmetica    : expresion_aritmetica TkSuma expresion_aritmetica 
                            | expresion_aritmetica TkResta expresion_aritmetica
                            | expresion_aritmetica TkMult expresion_aritmetica
                            | expresion_aritmetica TkDiv expresion_aritmetica
                            | expresion_aritmetica TkMod expresion_aritmetica
    '''
    p[0] = str((p[2], p[1], p[3]))


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
    expresion_booleana  : expresion_booleana TkConjuncion expresion_booleana 
                        | expresion_booleana TkDisyuncion expresion_booleana
                        | TkNegacion expresion_booleana
    '''
    operadores = {
        '/\\': 'Conjunción',
        '\\/': 'Disyunción',
    }
    if p[1] == 'not':
        p[0] = " EXP_BOOLEANA\n\t\t\t- operador: " + p[1] + "\n\t\t\t- operando: " + p[2]
    else:
        p[0] = " EXP_BOOLEANA\n\t\t\t- operador: " + operadores[p[2]] + "\n\t\t\t- operador izquierdo: " + p[1] + "\n\t\t\t- operador derecho: " + p[3]        

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
        'TkMenor': 'Menor que',
        'TkMenorIgual': 'Menor o igual que',
        'TkMayor': 'Mayor que',
        'TkMayorIgual': 'Mayor o igual que',
        'TkIgual': 'Igual que'
    }
    p[0] = " BIN_RELACIONAL\n\t\t\t- operador: " + operadores[p[2]] + "\n\t\t\t- operador izquierdo: " + p[1] + "\n\t\t\t- operador derecho: " + p[3]
    
        

        
        
        

# def p_asignacion(p):
#     '''
#     asignacion  : variable TkAsignacion expresion
#     '''
#     p[0] = "ASIGNACION:\n\t-contenedor: " + p[1] + p[3]

# def p_expresion_num(p):
#     '''
#     expresion   : TkNum
#     '''
#     p[0] = "\n\t-expresion: LITERAL ENTERO\n\t\t-valor: " + str(p[1])  

# def p_expresion_caracter(p):
#     '''
#     expresion : TkCaracter
#     '''
#     p[0] = "\n\t-expresion: LITERAL CARACTER\n\t\t-valor: " + str(p[1])  

# def p_variable(p):
#     '''
#     variable    : TkId
#     ''' 
#     p[0] = "VARIABLE\n\t\t-identificador: " + p[1]

parser = yacc.yacc()

entrada = read_archive(sys.argv[1])
if len(entrada) == 0:
    print('Error introduzca un archivo')
else:
    result = parser.parse(entrada)
    print(result)