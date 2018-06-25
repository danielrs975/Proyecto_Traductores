import sys
# En este script se implementa la tabla de simbolos del lenguaje 
# BasicTran

class Tabla_simbolo:
    
    # Constructor de la tabla de simbolos
    # El argumento tabla superior contendra un objeto del tipo tabla de simbolo
    # y este sera justamente la tabla del scope inmediatamente superior
    def __init__(self, tabla_superior=None):
        self.tabla = {}
        self.tabla_anterior = tabla_superior

    # Funcion que anadira nuevos simbolos a la tabla 
    def anadir_tabla(self, id,  tipo):
        if not self.existe_tabla(id):
            self.tabla[id] = tipo
        else:
            print("Error, la variable " + id + " ya ha sido declarada")
            sys.exit()

    # Funcion que se encargara de verificar si el simbolo ya existe en la tabla
    def existe_tabla(self, id):
        if self.tabla.get(id) == None:
            return False
        else:
            return self.tabla[id]

class Pila_tablas:

    def __init__(self):
        self.pila = []
        self.head = 0

    def push(self, tabla):
        self.pila.append(tabla)
        self.head = len(self.pila) - 1

    def pop(self):
        return self.pila.pop()
    
    def ver_tope(self):
        return self.pila[len(self.pila) - 1]

    def esta_en_las_tablas(self, id):
        if not self.vacio():
            for i in range(len(self.pila) - 1, 0, -1):
                if self.pila[i].existe_tabla(id) != False:
                    return self.pila[i].existe_tabla(id)
            return False

    def vacio(self):
        return self.pila == []