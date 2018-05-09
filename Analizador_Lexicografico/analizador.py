# Aqui se importa la libreria para el reconocimiento de los tokens 

import ply.lex as lex 

# Diccionarios de tokens 

tokens = (
    #--------------------------------------------------------------
    # Token para variables 
    'TkId',

    # Token para numero
    'TkNum',

    # Token para booleanos                         Esta seccion se tienen
    'TkTrue',                                     # que definir funciones
    'TkFalse',

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
    'TkNegacion',           # "not"
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
)