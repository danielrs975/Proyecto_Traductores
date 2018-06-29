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
# Partimos de lo mas general. Estructura del programa completo

def p_programa(p):
    '''
    programa    : TkWith lista_declaraciones TkBegin secuenciacion TkEnd
                | TkBegin secuenciacion TkEnd
    '''
    if len(p) > 4:
        p[0] = p[4]
    else:
        p[0] = p[2]

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
                p[0].anadir_tabla(i, p[4])
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
        p[0] = p[1] + " " + p[6]
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
        p[0] = Node('SECUENCIACION', [p[1], p[2]])
    

def p_secuenciacion2(p):
    '''
    secuenciacion2  : instruccion secuenciacion2
    '''
    if p[2] == None:
        p[0] = p[1]
    else:
        p[0] = Node('', [p[1], p[2]])

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
    '''
    if pila_de_iteradores.esta_en_las_tablas(p[1].nombre)==False:
        if p[2] == '<-':
            p[1].type = '- contenedor: ' + p[1].type
            p[3].type = '- expresion: ' + p[3].type
            es_valido = p[1].tipo_dato == p[3].tipo_dato and pila_de_tablas.esta_en_las_tablas(p[1].nombre)!=False
            p[0] = Node('ASIGNACION',[p[1], p[3]], valido=es_valido)
        else:
            p[1].type = '- contenedor: ' + p[1].type
            p[3].type = '- expresion: ' + p[3].type
            es_valido = p[1].tipo_dato == 'int' and p[3].valido and pila_de_tablas.esta_en_las_tablas(p[1].nombre)!=False
            p[0] = Node('ASIGNACION',[p[1], p[3]], '- operacion: punto', valido=es_valido)
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
        p[0] = Node('CONDICIONAL',[p[2],p[4],p[7]], valido=es_valido)
    else:
        p[2].type = '- guardia: ' + p[2].type
        p[4].type = '- exito: ' + p[4].type
        es_valido = p[2].valido or p[2].tipo_dato == 'bool'
        p[0] = Node('CONDICIONAL',[p[2],p[4]], valido=es_valido)

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
    p[2].type = '- argumento: ' + p[2].type
    es_valido = pila_de_tablas.esta_en_las_tablas(p[2].nombre)!=False
    p[0] = Node('ENTRADA-SALIDA',[p[2]], '- operador: ' + p[1], valido=es_valido)

def p_indeterminado(p):
    '''
    indeterminado   : TkWhile expresion_relacional TkHacer secuenciacion TkEnd
                    | TkWhile expresion_booleana TkHacer secuenciacion TkEnd
    '''
    p[2].type = '- guardia: ' + p[2].type
    p[4].type = '- iteracion: ' + p[4].type
    p[0] = Node('ITERACION INDETERMINADA', [p[2], p[4]])

def p_determinado(p): #Nuevo
    '''
    determinado     : TkFor identificador TkFrom expresion_aritmetica TkTo expresion_aritmetica TkStep literal TkHacer secuenciacion TkEnd
                    | TkFor identificador TkFrom expresion_aritmetica TkTo expresion_aritmetica TkHacer secuenciacion TkEnd
    '''
    p[0] = Tabla_simbolo()
    p[0].anadir_tabla(p[2].nombre, 'int')
    pila_de_iteradores = Pila_tablas()
    pila_de_iteradores.push(p[0])
    if(len(p)<12):
        p[2].type = '- iterador: ' + p[2].type 
        p[4].type = "- inicio: " + p[4].type 
        p[6].type = "- final: " + p[6].type 
        p[8].type = '- iteracion: ' + p[8].type
        es_valido = pila_de_tablas.esta_en_las_tablas(p[2].nombre)!=False
        p[0] = Node('ITERACION DETERMINADA', [p[2], p[4], p[6], p[8]], valido=es_valido)
    else:   
        p[2].type = '- iterador: ' + p[2].type 
        p[4].type = "- inicio: " + p[4].type 
        p[6].type = "- final: " + p[6].type
        p[8].type = "- paso: " + p[8].type 
        p[10].type = '- iteracion: ' + p[10].type 
        es_valido = pila_de_tablas.esta_en_las_tablas(p[2].nombre)!=False
        p[0] = Node('ITERACION DETERMINADA', [p[2], p[4], p[6], p[8], p[10]], valido=es_valido)
    pila_de_iteradores.pop()

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
            p[0] = Node('VARIABLE',leaf="- identificador: " + p[1], nombre=p[1], tipo_dato=pila_de_tablas.esta_en_las_tablas(p[1]))
        else:
            p[0] = Node('VARIABLE',leaf="- identificador: " + p[1], nombre=p[1])


def p_literal(p):
    '''
    literal : TkNum 
            | TkTrue 
            | TkFalse 
            | TkCaracter
            | TkParAbre literal TkParCierra
    '''
    if isinstance(p[1], int):
        p[0] = Node('LITERAL ENTERO',leaf='- valor: ' + str(p[1]), tipo_dato='int')
    elif p[1] == 'true':
        p[0] = Node('LITERAL BOOLEANO', leaf="- valor: " + p[1], tipo_dato='bool')
    elif p[1] == 'false':
        p[0] = Node('LITERAL BOOLEANO',leaf='- valor: ' + p[1], tipo_dato='bool')
    elif isinstance(p[1], str) and p[1] != '(':
        p[0] = Node('LITERAL CARACTER',leaf='- valor: ' + p[1], tipo_dato='char')
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
        es_valido_izquierdo = p[1].type == '- operador izquierdo: LITERAL ENTERO' or (p[1].type == '- operador izquierdo: VARIABLE' and p[1].tipo_dato == 'int') or (p[3].type == '- operador izquierdo: EXP_ARITMETICA' and p[3].valido) 
        es_valido_derecho = p[3].type == '- operador derecho: LITERAL ENTERO' or (p[3].type == '- operador derecho: VARIABLE' and p[3].tipo_dato == 'int') or (p[3].type == '- operador derecho: EXP_ARITMETICA' and p[3].valido)
        es_valido = es_valido_izquierdo and es_valido_derecho
        p[0] = Node('EXP_ARITMETICA', [p[1], p[3]], '- operacion: ' + p[2], valido=es_valido, tipo_dato='int')
    else:
        izquierdo = p[2]
        izquierdo.type = '- operador: ' + p[2].type 
        es_valido = p[2].type == 'LITERAL ENTERO' or (p[2].type == 'EXP_ARITMETICA' and p[2].valido)
        p[0] = Node('EXP_ARITMETICA', [izquierdo], '- operacion: ' + p[1], valido=es_valido, tipo_dato='int')    



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
        p[0] = Node('EXP_BOOLEANA', [p[2]], '- operacion: ' + p[1], valido=es_valido, tipo_dato='bool')
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
        p[0] = Node('EXP_BOOLEANA',[p[1], p[3]], '- operacion: ' + operadores[p[2]], valido=es_valido, tipo_dato='bool')        

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
        es_valido = p[2].type == '- operador: LITERAL CARACTER' or (p[2].type == '- operador: VARIABLE' and p[2].tipo_dato == 'char') or (p[2].type == '- operador: LITERAL CARACTER' and p[2].valido)
        p[0] = Node('EXP_CARACTER', [p[2]], '- operacion: ' + operadores[p[1]], valido=es_valido, tipo_dato= 'int')
    else:
        p[1].type = '- operador: ' + p[1].type
        es_valido = p[1].type == '- operador: LITERAL CARACTER' or (p[2].type == '- operador: VARIABLE' and p[2].tipe_dato == 'char') or (p[1].type == '- operador: LITERAL CARACTER' and p[1].valido)
        p[0] = Node('EXP_CARACTER', [p[1]], '- operacion: ' + operadores[p[2]], valido=es_valido, tipo_dato= 'char')



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
        p[0] = Node('EXP_ARREGLOS', [p[1], p[3]], '- operacion: Concatenacion', valido=es_valido, tipo_dato=p[1].tipo_dato)
    elif len(p) == 3:
        p[2].type = '- operador: ' + p[2].type 
        es_valido = p[2].type == '- operador: VARIABLE' and p[2].tipo_dato[:5] == 'array'
        p[0] = Node('EXP_ARREGLOS', [p[2]], '- operacion: Shift', valido=es_valido, tipo_dato=p[2].tipo_dato)
    else:
        p[1].type = '- contenedor: ' + p[1].type
        p[3].type = '- indexacion: ' + p[3].type
        es_valido = p[1].type == '- contenedor: VARIABLE' and p[1].tipo_dato[:5] == 'array' and ((p[3].type == '- indexacion: EXP_ARITMETICA' and p[3].valido) or (p[3].type == '- indexacion: LITERAL ENTERO') or (p[3].type == '- indexacion: VARIABLE' and p[3].tipo_dato == 'int'))
        p[0] = Node('EXP_ARREGLOS', [p[1],p[3]], valido=es_valido, tipo_dato=p[1].tipo_dato)
    

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
    p[0] = Node('BIN_RELACIONAL', [p[1], p[3]], '- operacion: ' + operadores[p[2]], valido=es_valido, tipo_dato='bool')


precedence = (
    ('nonassoc','TkMenorIgual','TkMayor', 'TkMayorIgual', 'TkIgual', 'TkDesigual'),
    ('left', 'TkSuma', 'TkResta', 'TkDisyuncion', 'TkSiguienteChar', 'TkConcatenacion'),
    ('left', 'TkMod', 'TkMult', 'TkDiv', 'TkAnteriorChar', 'TkConjuncion', 'TkShift'),
    ('left', 'TkValorAscii', 'TkNegacion', 'TkCorcheteAbre', 'TkCorcheteCierra'),
)
#-------------------------------------- Error ----------------------------------------------#

# def p_error(p):
#     print("Ha ocurrido un error de sintaxis. Abortando...")
#     sys.exit()
    
#------------------------------------ Clase para la construccion del arbol------------------------------#
class Node:
    def __init__(self, type, children=None,leaf=None, tabla_s=None, valido=None, nombre=None, tipo_dato=None):
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

    
        



#------------------------------- Se termina las reglas de la gramatica para BasicTran--------------#

if __name__ == "__main__":
    parser = yacc.yacc()
    entrada = read_archive(sys.argv[1])
    if len(entrada) == 0:
        print('Error introduzca un archivo')
    else:
        result = parser.parse(entrada)
        print(result) 


