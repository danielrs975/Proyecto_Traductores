# Se importar la libreria para hacer el parser 
import ply.yacc as yacc 
import sys

# Se importa los tokens del analizador lexicografico 
from Analizador_Lexicografico.analizador import tokens, read_archive

# ----------------------- Construccion de la gramatica ------------------------- #

# Partimos de lo mas general. Estructura del programa completo

def p_programa(p):
    '''
    programa    : TkWith lista_declaraciones TkBegin lista_instrucciones TkEnd
    '''
    p[0] = p[4]

#------------------------ Este es la definicion del bloque de declaraciones ------------------#
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

def p_lista_instrucciones(p):
    '''
    lista_instrucciones : instruccion TkPuntoYComa lista_instrucciones
    '''
    if p[3] == None:
        p[0] = p[1]
    else:
        p[0] = p[1] + "\n" + p[3]
        

def p_lista_instrucciones_instruccion(p):
    '''
    lista_instrucciones : instruccion
                        | empty
    '''
    p[0] = p[1]

def p_instruccion(p):
    '''
    instruccion : asignacion
    '''
    p[0] = p[1]

def p_asignacion(p):
    '''
    asignacion  : identificador TkAsignacion expresion 
    '''
    p[0] = "ASIGNACION:\n\t-contenedor: " + p[1] + p[3]

def p_identificador(p):
    '''
    identificador   : TkId
    '''
    p[0] = "VARIABLE\n\t\t-identificador: " + p[1]

def p_expresion(p):
    '''
    expresion   : literal
                | expresion_aritmetica 
    '''
    p[0] = p[1]
    

def p_expresion_aritmetica(p):
    '''
    expresion_aritmetica    : expresion_aritmetica TkSuma literal 
                            | expresion_aritmetica TkResta literal
                            | expresion_aritmetica TkMult literal
                            | expresion_aritmetica TkDiv literal
                            | expresion_aritmetica TkMod literal
    '''
    p[0] = (p[2], p[1], p[3])

def p_expresion_aritmetica_literal(p):
    '''
    expresion_aritmetica    : literal
    '''
    p[0] = p[1]

def p_literal(p):
    '''
    literal : TkNum 
            | TkTrue 
            | TkFalse 
            | TkCaracter
    '''
    if isinstance(p[1], int):
        p[0] = "\n\t-expresion: LITERAL ENTERO\n\t\t-valor: " + str(p[1])
    elif p[1] == 'true':
        p[0] = "\n\t-expresion: LITERAL BOOLEANO\n\t\t-valor: " + p[1]
    elif p[1] == 'false':
        p[0] = "\n\t-expresion: LITERAL BOOLEANO\n\t\t-valor: " + p[1]
    else:
        p[0] = "\n\t-expresion: LITERAL CARACTER\n\t\t-valor: " + p[1]
        
        
        

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