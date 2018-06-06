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
            | TkArray TkCorcheteAbre literal TkCorcheteCierra TkOf tipo 
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
    secuenciacion : instruccion secuenciacion
    '''
    if p[2] == None:
        p[0] = p[1]
    else:
        p[0] = Node('SECUENCIACION', [p[1], p[2]])
        

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
    asignacion  : identificador TkAsignacion expresion TkPuntoYComa
    '''
    p[0] = Node('ASIGNACION',[p[1], p[3]])

def p_condicional(p):
    '''
    condicional : TkIf expresion_booleana TkHacer secuenciacion TkEnd
                | TkIf expresion_booleana TkHacer secuenciacion TkOtherwise TkHacer secuenciacion TkEnd
    '''

    if (len(p)>6):
        p[0] = Node('CONDICIONAL',[p[2],p[4],p[7]])
    else:
        p[0] = Node('CONDICIONAL',[p[2],p[4]])

def p_alcance(p):
    '''
    alcance : TkWith lista_declaraciones TkBegin secuenciacion TkEnd
    '''
    p[0] = p[4]

def p_entrada_salida(p):
    '''
    entrada_salida  : TkRead identificador TkPuntoYComa
                    | TkPrint expresion TkPuntoYComa
    '''
    p[0] = Node('ENTRADA-SALIDA',[p[2]], p[1])

def p_indeterminado(p):
    '''
    indeterminado   : TkWhile expresion_relacional TkHacer secuenciacion TkEnd
    '''
    p[0] = Node('ITERACION INDETERMINADA', [p[2], p[4]])

def p_determinado(p):
    '''
    determinado     : TkFor identificador TkFrom expresion_aritmetica TkTo expresion_aritmetica TkStep literal TkHacer secuenciacion TkEnd
                    | TkFor identificador TkFrom expresion_aritmetica TkTo expresion_aritmetica TkHacer secuenciacion TkEnd
    '''
    if(len(p)<12):
        p[0] = Node('ITERACION DETERMINADA', [p[2], p[4], p[6], p[8]])
    else:   
        p[0] = Node('ITERACION DETERMINADA', [p[2], p[4], p[6], p[8], p[10]])

#--------------------------------------------------------------------------------------------#
#----------------------------Literales e identificadores-------------------------------------#

def p_identificador(p):
    '''
    identificador   : TkId
    '''
    p[0] = Node('VARIABLE',leaf=p[1])

def p_literal(p):
    '''
    literal : TkNum 
            | TkTrue 
            | TkFalse 
            | TkCaracter
    '''
    if isinstance(p[1], int):
        p[0] = Node('LITERAL ENTERO',leaf=str(p[1]))
    elif p[1] == 'true':
        p[0] = Node('LITERAL BOOLEANO', leaf=p[1])
    elif p[1] == 'false':
        p[0] = Node('LITERAL BOOLEANO',leaf=p[1])
    else:
        p[0] = Node('LITERAL CARACTER',leaf=p[1])

#--------------------------------------------------------------------------------------------#
#--------------------------Tipos de expresiones----------------------------------------------#

def p_expresion(p):
    '''
    expresion   : literal
                | expresion_aritmetica 
                | expresion_booleana
                | expresion_caracteres
                | expresion_arreglos
                | expresion_relacional
    '''
    p[0] = p[1]


def p_expresion_aritmetica(p):
    '''
    expresion_aritmetica    : expresion_aritmetica TkSuma expresion_aritmetica 
                            | expresion_aritmetica TkResta expresion_aritmetica
                            | expresion_aritmetica TkMult expresion_aritmetica
                            | expresion_aritmetica TkMod expresion_aritmetica
                            | expresion_aritmetica TkDiv expresion_aritmetica
                            | TkResta expresion_aritmetica
    '''
    if len(p) > 3:
        p[0] = Node('EXP_ARITMETICA', [p[1], p[3]], p[2])
    else:
        p[0] = Node('EXP_ARITMETICA', [p[2]], p[1])    


precedence = (
    ('nonassoc', 'TkMenor','TkMenorIgual','TkMayor', 'TkMayorIgual'),
    ('left', 'TkSuma', 'TkResta', 'TkValorAscii'),
    ('left', 'TkMult', 'TkDiv', 'TkAnteriorChar'),
    ('left', 'TkMod', 'TkSiguienteChar')
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
                        | expresion_relacional TkConjuncion expresion_relacional
                        | expresion_relacional TkDisyuncion expresion_relacional
                        | TkNegacion expresion_booleana
                        | TkNegacion expresion_relacional 
                        | expresion_relacional
    '''
    operadores = {
        '/\\': 'Conjunción',
        '\\/': 'Disyunción',
    }
    if p[1] == 'not':
        p[0] = Node('EXP_BOOLEANA', [p[2]], p[1])
    elif len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = Node('EXP_BOOLEANA',[p[1], p[3]], operadores[p[2]])        

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

def p_expresion_caracteres(p):
    '''
    expresion_caracteres    : expresion_caracteres TkSiguienteChar
                            | expresion_caracteres TkAnteriorChar
                            | TkValorAscii expresion_caracteres

    '''
    operadores = {
        '++': 'Siguiente caracter',
        '--': 'Caracter anterior',
        '#' : 'Código ASCII'
    }
    
    if p[1] == '#':
        p[0] = Node('EXP_CARACTER', [p[2]], operadores[p[1]])
    else:
        p[0] = Node('EXP_CARACTER', [p[1]], p[2])



def p_expresion_caracteres_literal(p):
    '''
    expresion_caracteres    : literal
                            | TkParAbre expresion_caracteres TkParCierra
    '''
    if len(p) > 2:
        p[0] = p[2]
    else:
        p[0] = p[1]


def p_expresion_arreglos(p):
    '''
    expresion_arreglos  : identificador TkConcatenacion expresion_arreglos
                        | TkShift expresion_arreglos
                        | expresion_arreglos TkCorcheteAbre expresion_aritmetica TkCorcheteCierra
    '''
    if len(p) == 4:
        p[0] = Node('EXP_ARREGLOS', [p[1], p[3]], 'Concatenacion')
    elif len(p) == 3:
        p[0] = Node('EXP_ARREGLOS', [p[2]], 'Shift')
    else:
        p[0] = Node('EXP_ARREGLOS', [p[1]])
    

def p_expresion_arreglos_literal(p):
    '''
    expresion_arreglos  : identificador
                        | TkParAbre expresion_arreglos TkParCierra 
    '''
    if len(p) == 4:
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
                            | expresion_aritmetica TkDesigual expresion_aritmetica
    '''
    operadores = {
        '<': "'Menor que'",
        '<=': "'Menor o igual que'",
        '>': "'Mayor que'",
        '>=': "'Mayor o igual que'",
        '=': "'Igual que'",
        '/=': "'Desigual'"
    }
    p[0] = Node('BIN_RELACIONAL', [p[1], p[3]], operadores[p[2]])
    
#------------------------------------ Clase para la construccion del arbol------------------------------#

class Node:
    def __init__(self, type, children=None,leaf=None):
        self.type = type
        if children:
            self.children = children 
        else:
            self.children = []
        self.leaf = leaf
    
    respuesta = ''

    def __str__(self):
        return self.dfs('')


    def dfs(self, tabs):
        self.respuesta += self.type + '\n'
        tabs += '\t'
        if self.leaf != None:
            self.respuesta += tabs + '\t' + self.leaf + '\n'
        for child in self.children:
            self.respuesta += tabs + child.dfs(tabs)

        return self.respuesta
        



#------------------------------------ Se termina las reglas de la gramatica para BasicTran--------------#

if __name__ == "__main__":
    parser = yacc.yacc()
    entrada = read_archive(sys.argv[1])
    if len(entrada) == 0:
        print('Error introduzca un archivo')
    else:
        result = parser.parse(entrada)
        print(result)