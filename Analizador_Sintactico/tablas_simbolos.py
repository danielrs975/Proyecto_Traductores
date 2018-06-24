# En este script se implementa la tabla de simbolos del lenguaje 
# BasicTran

class tabla_simbolo:
    
    # Constructor de la tabla de simbolos
    # El argumento tabla superior contendra un objeto del tipo tabla de simbolo
    # y este sera justamente la tabla del scope inmediatamente superior
    def __init__(self, tabla_superior):
        self.tabla = {}
        self.tabla_anterior = tabla_superior

    # Funcion que anadira nuevos simbolos a la tabla 
    def anadir_tabla(self, id,  tipo):
        if not self.existe_tabla(id):
            self.tabla[id] = tipo
        else:
            return "Error, la variable " + id + " ya ha sido declarada"

    # Funcion que se encargara de verificar si el simbolo ya existe en la tabla
    def existe_tabla(self, id):
        if self.tabla.get(id) == None:
            return False
        else:
            return True