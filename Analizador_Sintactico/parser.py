# Autores:
#   - Daniel Rodriguez
#   - Yuni Quintero
# Se importar la libreria para hacer el parser 
import ply.yacc as yacc 
import sys

# Se importa los tokens del analizador lexicografico 
from Analizador_Lexicografico.analizador import tokens, read_archive
from tablas_simbolos import Tabla_simbolo, Pila_tablas

# ----------------------- Construccion de la gramatica ------------------------- #

pila_de_tablas = Pila_tablas()
pila_de_iteradores = Pila_tablas()

# Partimos de lo mas general. Estructura del programa completo

def p_programa(p):
    '''
    programa    : TkWith lista_declaraciones TkBegin secuenciacion TkEnd
                | TkBegin secuenciacion TkEnd
    '''
    if len(p) > 4:
        p[0] = [p[4], p[2]]
    else:
        p[0] = [p[2]]

#------------------------ Este es la definicion del bloque de declaraciones ------------------#
# Esta parte no hay que reportarla 


def p_lista_declaraciones(p): #Nuevo
    '''
    lista_declaraciones : TkVar lista_identificadores TkDosPuntos tipo lista_declaraciones
                        | TkVar lista_identificadores TkDosPuntos tipo 
    '''
    if len(p) == 5:
        p[0] = Tabla_simbolo()
        for i in p[2]:
            if p[0].existe_tabla(i) == False:
                if p[4][0] == 'array':
                    arreglo = []
                    for k in range(0,p[4][2]):
                        arreglo = arreglo + [None]
                p[0].anadir_tabla(i, p[4], arreglo)
            else:
                print('Se esta declarando una variable ya declarada: ' + i)
                sys.exit()
    else:
        p[0] = p[5]
        for i in p[2]:
            if p[0].existe_tabla(i) == False:
                p[0].anadir_tabla(i, p[4])
            else:
                print('Se esta declarando una variable ya declarada: ' + i)
                sys.exit()

    pila_de_tablas.push(p[0])



def p_lista_identificadores(p):
    '''
    lista_identificadores   : identificador TkComa lista_identificadores
                            | identificador TkAsignacion expresion TkComa lista_identificadores
                            | identificador TkAsignacion expresion
                            | identificador
    '''
    if len(p) == 2 or (len(p) == 4 and p[2] == '<-'):
        p[0] = [p[1].nombre] 
    elif len(p) == 6:
        p[0] = p[5] + [p[1].nombre]
    else:
        p[0] = p[3] + [p[1].nombre]

def p_tipo(p):
    '''
    tipo    : TkInt
            | TkBool
            | TkChar 
            | TkArray TkCorcheteAbre expresion_aritmetica TkCorcheteCierra TkOf tipo 
    '''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = [p[1], p[6], p[3].evaluar_arbol()]
# ---------------------------------------------------------------------------------------------#

#--------------------------Funcion importante para manejar recursion--------------------------#
# Caso base cuando se termina de procesar la instruccion
def p_empty(p):
    'empty :'
    pass

# ------------------- Esta es la gramatica para el bloque de instrucciones --------------------#

def p_secuenciacion(p):
    '''
    secuenciacion : instruccion secuenciacion2
    '''
    if p[2] == None:
        p[0] = p[1]
    else:
        p[0] = Node('SECUENCIACION', [p[1], p[2]], tipo_expr='SECUENCIACION')
    

def p_secuenciacion2(p):
    '''
    secuenciacion2  : instruccion secuenciacion2
    '''
    if p[2] == None:
        p[0] = p[1]
    else:
        p[0] = Node('', [p[1], p[2]], tipo_expr='SECUENCIACION')

def p_secuenciacion_instruccion(p):
    '''
    secuenciacion2  : instruccion
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
def p_asignacion(p): #Nuevo
    '''
    asignacion  : identificador TkAsignacion expresion TkPuntoYComa
                | identificador TkPunto expresion_aritmetica TkPuntoYComa
                | expresion_arreglos TkAsignacion expresion TkPuntoYComa
    '''
    if pila_de_iteradores.esta_en_las_tablas(p[1].nombre)==False:
        if p[2] == '<-' and p[1].tipo_expr != 'EXP_ARREGLOS':
            p[1].type = '- contenedor: ' + p[1].type
            p[3].type = '- expresion: ' + p[3].type
            es_valido = p[1].tipo_dato == p[3].tipo_dato and pila_de_tablas.esta_en_las_tablas(p[1].nombre)!=False and len(pila_de_tablas.pila) > 0
            p[0] = Node('ASIGNACION',[p[1], p[3]], valido=es_valido, tipo_expr='ASIGNACION')
        elif p[1].tipo_expr == 'EXP_ARREGLOS':
            p[1].type = '- contenedor: ' + p[1].type
            p[3].type = '- expresion: ' + p[3].type 
            es_valido = len(pila_de_tablas.pila) > 0
            print(es_valido)
            p[0] = Node('ASIGNACION',[p[1], p[3]], valido=es_valido, tipo_expr='ASIGNACION')
        else:
            p[1].type = '- contenedor: ' + p[1].type
            p[3].type = '- expresion: ' + p[3].type
            es_valido = p[1].tipo_dato == 'int' and p[3].valido and pila_de_tablas.esta_en_las_tablas(p[1].nombre)!=False and len(pila_de_tablas.pila) > 0
            p[0] = Node('ASIGNACION',[p[1], p[3]], '- operacion: punto', valido=es_valido, tipo_expr='ASIGNACION')
    else:
        print('Se esta alterando el valor del iterador: ' + p[1].nombre)
        sys.exit()

def p_condicional(p):
    '''
    condicional : TkIf expresion_booleana TkHacer secuenciacion TkEnd
                | TkIf expresion_booleana TkHacer secuenciacion TkOtherwise TkHacer secuenciacion TkEnd
    '''

    if (len(p)>6):
        p[2].type = '- guardia: ' + p[2].type
        p[4].type = '- exito: ' + p[4].type
        p[7].type = '- no exito: ' + p[7].type
        es_valido = p[2].valido or p[2].tipo_dato == 'bool'
        p[0] = Node('CONDICIONAL',[p[2],p[4],p[7]], valido=es_valido, tipo_expr='CONDICIONAL')
    else:
        p[2].type = '- guardia: ' + p[2].type
        p[4].type = '- exito: ' + p[4].type
        es_valido = p[2].valido or p[2].tipo_dato == 'bool'
        p[0] = Node('CONDICIONAL',[p[2],p[4]], valido=es_valido, tipo_expr='CONDICIONAL')

def p_alcance(p):
    '''
    alcance : TkWith lista_declaraciones TkBegin secuenciacion TkEnd
            | TkBegin secuenciacion TkEnd
    '''
    if len(p) > 4:
        p[0] = p[4]
    else:
        p[0] = p[2]
    pila_de_tablas.pop()

def p_entrada_salida(p): #Nuevo
    '''
    entrada_salida  : TkRead identificador TkPuntoYComa
                    | TkPrint expresion TkPuntoYComa
    '''
    if p[1] == 'read':
        p[2].type = '- argumento: ' + p[2].type
        es_valido = pila_de_tablas.esta_en_las_tablas(p[2].nombre)!=False 
        p[0] = Node('ENTRADA-SALIDA',[p[2]], '- operador: ' + p[1], valido=es_valido, tipo_oper=p[1], tipo_expr='ENTRADA-SALIDA')
    else:
        p[2].type = '- argumento: ' + p[2].type
        es_valido = p[2].valido
        p[0] = Node('ENTRADA-SALIDA',[p[2]], '- operador: ' + p[1], valido=es_valido, tipo_oper=p[1], tipo_expr='ENTRADA-SALIDA')

def p_indeterminado(p):
    '''
    indeterminado   : TkWhile expresion_relacional TkHacer secuenciacion TkEnd
                    | TkWhile expresion_booleana TkHacer secuenciacion TkEnd
    '''
    p[2].type = '- guardia: ' + p[2].type
    p[4].type = '- iteracion: ' + p[4].type
    es_valido = p[2].valido and p[2].tipo_dato == 'bool'
    p[0] = Node('ITERACION INDETERMINADA', [p[2], p[4]], valido=es_valido, tipo_expr='ITERACION INDETERMINADA')

def p_determinado(p): #Nuevo
    '''
    determinado     : TkFor identificador ve_identificador TkFrom expresion_aritmetica TkTo expresion_aritmetica TkStep literal TkHacer secuenciacion TkEnd
                    | TkFor identificador ve_identificador TkFrom expresion_aritmetica TkTo expresion_aritmetica TkHacer secuenciacion TkEnd
    '''
    
    if(len(p)<12):
        p[2].type = '- iterador: ' + p[2].type 
        p[5].type = "- inicio: " + p[5].type 
        p[7].type = "- final: " + p[7].type 
        p[9].type = '- iteracion: ' + p[9].type
        es_valido = pila_de_tablas.esta_en_las_tablas(p[2].nombre)!=False and p[2].tipo_dato == 'int'
        p[0] = Node('ITERACION DETERMINADA', [p[2], p[5], p[7], p[9]], valido=es_valido, tipo_expr='ITERACION DETERMINADA')
    else:
        p[2].type = '- iterador: ' + p[2].type 
        p[5].type = "- inicio: " + p[5].type 
        p[7].type = "- final: " + p[7].type
        p[9].type = "- paso: " + p[9].type 
        p[11].type = '- iteracion: ' + p[11].type 
        es_valido = pila_de_tablas.esta_en_las_tablas(p[2].nombre)!=False and p[2].tipo_dato == 'int' and p[9].tipo_dato == 'int'
        p[0] = Node('ITERACION DETERMINADA', [p[2], p[5], p[7], p[9], p[11]], valido=es_valido, tipo_expr='ITERACION DETERMINADA')
    pila_de_iteradores.pop()

# Esta funcion crea una pila donde se guarda el iterador que es usado 
# en el for
def p_ve_identificador(p):
    '''
    ve_identificador    :
    '''
    tabla_auxiliar = Tabla_simbolo()
    tabla_auxiliar.anadir_tabla(p[-1].nombre, 'int')
    pila_de_iteradores.push(tabla_auxiliar)
#--------------------------------------------------------------------------------------------#
#----------------------------Literales e identificadores-------------------------------------#

def p_identificador(p): #Nuevo aqui se deberia poner algo pero no estoy segura
    '''
    identificador   : TkId
                    | TkParAbre identificador TkParCierra
    '''
    if p[1] == '(':
        p[0] = p[2]
    else:
        if len(pila_de_tablas.pila) > 0:
            if pila_de_tablas.esta_en_las_tablas(p[1])==False:
                p[0] = Node('VARIABLE',leaf="- identificador: " + p[1], nombre=p[1], tipo_dato=False, tipo_expr='VARIABLE')
            else:
                tipo_de_dato = pila_de_tablas.esta_en_las_tablas(p[1])[0]
                if type(tipo_de_dato) == list:
                    tipo_de_dato = tipo_de_dato[0] + " " +  tipo_de_dato[1]
                p[0] = Node('VARIABLE',leaf="- identificador: " + p[1], nombre=p[1], tipo_dato=tipo_de_dato, tipo_expr='VARIABLE')
        else:
            p[0] = Node('VARIABLE',leaf="- identificador: " + p[1], nombre=p[1], tipo_expr='VARIABLE')


def p_literal(p):
    '''
    literal : TkNum 
            | TkTrue 
            | TkFalse 
            | TkCaracter
            | TkParAbre literal TkParCierra
    '''
    if isinstance(p[1], int):
        p[0] = Node('LITERAL ENTERO',leaf='- valor: ' + str(p[1]), tipo_dato='int', nodo_valor=p[1], tipo_expr='LITERAL ENTERO')
    elif p[1] == 'true':
        p[0] = Node('LITERAL BOOLEANO', leaf="- valor: " + p[1], tipo_dato='bool', nodo_valor=True, tipo_expr='LITERAL BOOLEANO')
    elif p[1] == 'false':
        p[0] = Node('LITERAL BOOLEANO',leaf='- valor: ' + p[1], tipo_dato='bool', nodo_valor =False, tipo_expr='LITERAL BOOLEANO')
    elif isinstance(p[1], str) and p[1] != '(':
        p[0] = Node('LITERAL CARACTER',leaf='- valor: ' + p[1], tipo_dato='char', nodo_valor=p[1], tipo_expr='LITERAL CARACTER')
    else:
        p[0] = p[2]


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
        p[1].type = '- operador izquierdo: ' + p[1].type
        p[3].type = '- operador derecho: ' + p[3].type
        es_valido_izquierdo = p[1].type == '- operador izquierdo: LITERAL ENTERO' or (p[1].type == '- operador izquierdo: VARIABLE' and p[1].tipo_dato == 'int') or (p[1].type == '- operador izquierdo: EXP_ARITMETICA' and p[1].valido) 
        es_valido_derecho = p[3].type == '- operador derecho: LITERAL ENTERO' or (p[3].type == '- operador derecho: VARIABLE' and p[3].tipo_dato == 'int') or (p[3].type == '- operador derecho: EXP_ARITMETICA' and p[3].valido)
        es_valido = es_valido_izquierdo and es_valido_derecho
      
        p[0] = Node('EXP_ARITMETICA', [p[1], p[3]], '- operacion: ' + p[2], valido=es_valido, tipo_dato='int', tipo_expr="EXP_ARITMETICA", tipo_oper=p[2])
    else:
        izquierdo = p[2]
        izquierdo.type = '- operador: ' + p[2].type 
        es_valido = p[2].type == '- operador: LITERAL ENTERO' or (p[2].type == 'EXP_ARITMETICA' and p[2].valido)
        p[0] = Node('EXP_ARITMETICA', [izquierdo], '- operacion: ' + p[1], valido=es_valido, tipo_dato='int', tipo_expr='EXP_ARITMETICA', tipo_oper='menos_unario')    



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
                        | TkParAbre expresion_booleana TkParCierra
                        | TkNegacion expresion_booleana
                        | expresion_relacional
    '''
    operadores = {
        '/\\': 'Conjunción',
        '\\/': 'Disyunción',
    }
    if p[1] == 'not':
        p[2].type = '- operador: ' + p[2].type 
        es_valido = p[2].type == '- operador: LITERAL BOOLEANO' or (p[2].type == '- operador: VARIABLE' and p[2].tipo_dato == 'bool') or (p[2].type == '- operador: EXP_BOOLEANA' and p[2].valido) or (p[2].type == '- operador: BIN_RELACIONAL' and p[2].valido)
        p[0] = Node('EXP_BOOLEANA', [p[2]], '- operacion: ' + p[1], valido=es_valido, tipo_dato='bool', tipo_expr='EXP_BOOLEANA', tipo_oper=p[1])
    elif len(p) == 2:
        p[0] = p[1]
    elif len(p) == 4 and p[1] == '(':
        p[0] = p[2]
    else:
        p[1].type = '- operador izquierdo: ' + p[1].type
        p[3].type = '- operador derecho: ' + p[3].type
        es_valido_izquierdo = p[1].type == '- operador izquierdo: LITERAL BOOLEANO' or (p[1].type == '- operador izquierdo: VARIABLE' and p[1].tipo_dato == 'bool') or (p[1].type == '- operador izquierdo: EXP_BOOLEANA' and p[1].valido) or (p[1].type == '- operador izquierdo: BIN_RELACIONAL' and p[1].valido)
        es_valido_derecho = p[3].type == '- operador derecho: LITERAL BOOLEANO' or (p[3].type == '- operador derecho: VARIABLE' and p[3].tipo_dato == 'bool') or (p[3].type == '- operador derecho: EXP_BOOLEANA' and p[3].valido) or (p[3].type == '- operador derecho: BIN_RELACIONAL' and p[3].valido)
        es_valido = es_valido_izquierdo and es_valido_derecho
        p[0] = Node('EXP_BOOLEANA',[p[1], p[3]], '- operacion: ' + operadores[p[2]], valido=es_valido, tipo_dato='bool', tipo_expr='EXP_BOOLEANA', tipo_oper=operadores[p[2]])        

def p_expresion_booleana_literal_identificador(p):
    '''
    expresion_booleana  : literal
                        | identificador
    '''
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
        p[2].type = '- operador: ' + p[2].type
        es_valido = p[2].type == '- operador: LITERAL CARACTER' or (p[2].type == '- operador: VARIABLE' and p[2].tipo_dato == 'char') or (p[2].type == '- operador: EXP_CARACTER' and p[2].valido)
        p[0] = Node('EXP_CARACTER', [p[2]], '- operacion: ' + operadores[p[1]], valido=es_valido, tipo_dato= 'int', tipo_expr='EXP_CARACTER', tipo_oper=p[1])
    else:
        p[1].type = '- operador: ' + p[1].type
        es_valido = p[1].type == '- operador: LITERAL CARACTER' or (p[1].type == '- operador: VARIABLE' and p[1].tipo_dato == 'char') or (p[1].type == '- operador: EXP_CARACTER' and p[1].valido)
        p[0] = Node('EXP_CARACTER', [p[1]], '- operacion: ' + operadores[p[2]], valido=es_valido, tipo_dato= 'char', tipo_expr='EXP_CARACTER', tipo_oper=p[2])



def p_expresion_caracteres_literal(p):
    '''
    expresion_caracteres    : literal
                            | identificador
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
        p[1].type = '- operador izquierdo: ' + p[1].type 
        p[3].type = '- operador derecho: ' + p[3].type 
        es_valido = p[1].type == '- operador izquierdo: VARIABLE' and p[3].type == '- operador derecho: VARIABLE' and p[1].tipo_dato == p[3].tipo_dato and p[1].tipo_dato[:5] == 'array' 
        p[0] = Node('EXP_ARREGLOS', [p[1], p[3]], '- operacion: Concatenacion', valido=es_valido, tipo_dato=p[1].tipo_dato, tipo_expr='EXP_ARREGLOS', tipo_oper='Concatenacion')
    elif len(p) == 3:
        p[2].type = '- operador: ' + p[2].type 
        es_valido = p[2].type == '- operador: VARIABLE' and p[2].tipo_dato[:5] == 'array'
        p[0] = Node('EXP_ARREGLOS', [p[2]], '- operacion: Shift', valido=es_valido, tipo_dato=p[2].tipo_dato, tipo_expr='EXP_ARREGLOS', tipo_oper='Shift')
    else:
        p[1].type = '- contenedor: ' + p[1].type
        p[3].type = '- indexacion: ' + p[3].type
        es_valido = p[1].type == '- contenedor: VARIABLE' and p[1].tipo_dato[:5] == 'array' and ((p[3].type == '- indexacion: EXP_ARITMETICA' and p[3].valido) or (p[3].type == '- indexacion: LITERAL ENTERO') or (p[3].type == '- indexacion: VARIABLE' and p[3].tipo_dato == 'int'))
        p[0] = Node('EXP_ARREGLOS', [p[1],p[3]], valido=es_valido, tipo_dato=p[1].tipo_dato, tipo_expr='EXP_ARREGLOS', tipo_oper='indexacion')
    

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
    p[1].type = '- operador izquierdo: ' + p[1].type
    p[3].type = '- operador derecho: ' + p[3].type 
    es_valido_izquierdo = p[1].type == '- operador izquierdo: LITERAL ENTERO' or (p[1].type == '- operador izquierdo: VARIABLE' and p[1].tipo_dato == 'int') or (p[1].type == '- operador izquierdo: EXP_ARITMETICA' and p[1].valido)
    es_valido_derecho = p[3].type == '- operador derecho: LITERAL ENTERO' or (p[3].type == '- operador derecho: VARIABLE' and p[3].tipo_dato == 'int') or (p[3].type == '- operador derecho: EXP_ARITMETICA' and p[3].valido)
    es_valido = es_valido_izquierdo and es_valido_derecho
    p[0] = Node('BIN_RELACIONAL', [p[1], p[3]], '- operacion: ' + operadores[p[2]], valido=es_valido, tipo_dato='bool', tipo_expr="BIN_RELACIONAL", tipo_oper=p[2])


precedence = (
    ('nonassoc','TkMenorIgual','TkMayor', 'TkMayorIgual', 'TkIgual', 'TkDesigual'),
    ('left', 'TkSuma', 'TkResta', 'TkDisyuncion', 'TkSiguienteChar', 'TkConcatenacion'),
    ('left', 'TkMod', 'TkMult', 'TkDiv', 'TkAnteriorChar', 'TkConjuncion', 'TkShift'),
    ('left', 'TkValorAscii', 'TkNegacion', 'TkCorcheteAbre', 'TkCorcheteCierra'),
)
#-------------------------------------- Error ----------------------------------------------#

def p_error(p):
    print("Ha ocurrido un error de sintaxis. Abortando...")
    sys.exit()
    
#------------------------------------ Clase para la construccion del arbol------------------------------#
class Node:
    def __init__(self, type, children=None,leaf=None, tabla_s=None, valido=None, nombre=None, tipo_dato=None, nodo_valor = None, tipo_expr=None, tipo_oper=None):
        self.type = type
        if children:
            self.children = children 
        else:
            self.children = []
        self.leaf = leaf
        self.valido = valido
        self.nombre = nombre
        self.tabla_s = tabla_s
        self.tipo_dato = tipo_dato
        self.nodo_valor = nodo_valor
        self.tipo_expr = tipo_expr
        self.tipo_oper = tipo_oper
    respuesta = ''
    tipo = ''

    def __str__(self):
        return self.dfs('', self.tipo)


    def dfs(self, tabs, tipo):
        if self.valido != None and not self.valido:
            print('Ha ocurrido un error abortando')
            sys.exit()
        if self.type != '':
            self.respuesta += self.type + '\n'
            tabs += '\t'
        if self.leaf != None:
            self.respuesta += tabs + self.leaf + '\n'
        contador = 0
        for child in self.children:
            contador += 1
            if self.type != '':
                self.respuesta += tabs + child.dfs(tabs, '')
            else:
                if contador == 2:
                    self.respuesta += tabs + child.dfs(tabs, '')
                else:
                    self.respuesta += child.dfs(tabs, '')
        return self.respuesta

    # Funcion que evalua arbol sintactico abstracto 
    def evaluar_arbol(self):
        # Ejecucion de las instrucciones 
        if self.tipo_expr == "SECUENCIACION":
            for child in self.children:
                child.evaluar_arbol()
        elif self.tipo_expr == "ASIGNACION":
            # Lado izquierdo de la asignacion 
            variable = self.children[0].nombre
            # Lado derecho de la asignacion es una expresion guardamos el valor de dicha expresion
            valor = self.children[1].evaluar_arbol()
            pila_de_tablas.modificar_valor_pila(variable, valor)
        elif self.tipo_expr == "ENTRADA-SALIDA":
            # Primero se ve que operacion se esta haciendo
            if self.tipo_oper == 'print':
                print(self.children[0].evaluar_arbol())
            if self.tipo_oper == 'read':
                # Aqui hay que verficar que el tipo de la variable y el que esta 
                # ingresando el usuario sean los mismos 
                entrada = input()
                variable = self.children[0].nombre
                pila_de_tablas.modificar_valor_pila(variable,entrada)
        elif self.tipo_expr == "CONDICIONAL":
            # Primero ejecutamos los if que no tienen else 
            if len(self.children) == 2:
                se_cumple_guardia = self.children[0].evaluar_arbol()
                if se_cumple_guardia:
                    self.children[1].evaluar_arbol()
            else:
                se_cumple_guardia = self.children[0].evaluar_arbol()
                if se_cumple_guardia:
                    self.children[1].evaluar_arbol()
                else:
                    self.children[2].evaluar_arbol()    
        elif self.tipo_expr == "ITERACION INDETERMINADA":
            #Guardamos valor de la guardia
            se_cumple_guardia = self.children[0].evaluar_arbol()
            print(se_cumple_guardia)
            while se_cumple_guardia:
                self.children[1].evaluar_arbol()
                se_cumple_guardia = self.children[0].evaluar_arbol()
        elif self.tipo_expr == "ITERACION DETERMINADA":
            #for sin token step
            if len(self.children) == 4:
                iterador = self.children[0].nombre
                from_ = self.children[1].evaluar_arbol()
                to_ = self.children[2].evaluar_arbol()
                for i in range(from_, to_):
                    pila_de_tablas.modificar_valor_pila(iterador,i)
                    self.children[3].evaluar_arbol()
            else:
                iterador = self.children[0].nombre
                from_ = self.children[1].evaluar_arbol()
                to_ = self.children[2].evaluar_arbol()
                step_ = self.children[3].evaluar_arbol()
                for i in range(from_, to_, step_):
                    pila_de_tablas.modificar_valor_pila(iterador,i) 
                    self.children[4].evaluar_arbol()
        
        # -------------------------------------------------------------------------------------------

        # Evaluacion de las expresiones
        es_literal = self.tipo_expr == "LITERAL CARACTER" or self.tipo_expr == "LITERAL ENTERO" or self.tipo_expr == "LITERAL BOOLEANO" 
        es_variable = self.tipo_expr == "VARIABLE"
        if es_literal:
            return self.nodo_valor
        if es_variable:
            # Si es una variable se devuelve es el valor que almacena 
            # dicha variable
            valor_variable = pila_de_tablas.esta_en_las_tablas(self.nombre)[1]
            # En esta parte se puede colocar la verificacion de que la variable este 
            # inicializada

            return valor_variable
        
        if self.tipo_expr == 'EXP_ARITMETICA':
            # Se ve que tipo de operacion es y se realiza dicha operacion
            if self.tipo_oper == '+':
                return self.children[0].evaluar_arbol() + self.children[1].evaluar_arbol()
            if self.tipo_oper == '-':
                return self.children[0].evaluar_arbol() - self.children[1].evaluar_arbol()
            if self.tipo_oper == '*':
                return self.children[0].evaluar_arbol() * self.children[1].evaluar_arbol()
            if self.tipo_oper == '/':
                # Aqui se puede colocar la verificacion de la division por 0
                return int(self.children[0].evaluar_arbol() / self.children[1].evaluar_arbol())
            if self.tipo_oper == 'menos_unario':
                return -self.children[0].evaluar_arbol()

        if self.tipo_expr == 'EXP_BOOLEANA':
            # Se ve que tipo de operacion es y se realiza la operacion
            if self.tipo_oper == 'not':
                return not self.children[0].evaluar_arbol()
            if self.tipo_oper == 'Conjunción':
                # Lado derecho operado con lado izquierdo
                return self.children[0].evaluar_arbol() and self.children[1].evaluar_arbol()
            if self.tipo_oper == 'Disyunción':
                # Lado derecho operado con lado izquierdo
                return self.children[0].evaluar_arbol() or self.children[1].evaluar_arbol()

        if self.tipo_expr == 'BIN_RELACIONAL':
            # Se ve que tipo de operacion es y se realiza la operacion
            if self.tipo_oper == '>':
                return self.children[0].evaluar_arbol() > self.children[1].evaluar_arbol()
            if self.tipo_oper == '<':
                return self.children[0].evaluar_arbol() < self.children[1].evaluar_arbol()
            if self.tipo_oper == '<=':
                return self.children[0].evaluar_arbol() <= self.children[1].evaluar_arbol()
            if self.tipo_oper == '>=':
                return self.children[0].evaluar_arbol() >= self.children[1].evaluar_arbol()
            if self.tipo_oper == '=':
                return self.children[0].evaluar_arbol() == self.children[1].evaluar_arbol()
            if self.tipo_oper == '/=':
                return self.children[0].evaluar_arbol() != self.children[1].evaluar_arbol()

        if self.tipo_expr == 'EXP_CARACTER':
            # Se ve que tipo de operacion es y se ejecuta
            if self.tipo_oper == '++':
                # Se obtiene el caracter 
                caracter = self.children[0].evaluar_arbol()[1]
                return "'" + chr(ord(caracter) + 1) + "'"
            if self.tipo_oper == '--':
                caracter = self.children[0].evaluar_arbol()[1]
                return "'" + chr(ord(caracter) - 1) + "'"
            if self.tipo_oper == '#':
                caracter = self.children[0].evaluar_arbol()[1]
                return ord(caracter)

        if self.tipo_expr == 'EXP_ARREGLOS':
            # Se ve que tipo de operacion es y se ejecuta
            if self.tipo_oper == 'Concatenacion':
                pass
            elif self.tipo_oper == 'indexacion':
                print("hola")
        
#------------------------------- Se termina las reglas de la gramatica para BasicTran--------------#

if __name__ == "__main__":
    parser = yacc.yacc()
    entrada = read_archive(sys.argv[1])
    if len(entrada) == 0:
        print('Error introduzca un archivo')
    else:
        result = parser.parse(entrada)
        print("-------------Arbol sintactico abstracto----------")
        print(result[0])
        print('--------------------------------------------------')
        print("----------------Tablas de simbolos----------------")
        # Ejecucion de las instrucciones del arbol
        result[0].evaluar_arbol()
        for i in pila_de_tablas.pila:
            print(i.tabla) 
