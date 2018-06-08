**Fase II**
**Análisis Sintáctico**
**Yuni Quintero**
**Daniel Rodríguez**

Esta fase incluye la definición de la gramática del lenguaje y se tiene como salida el Árbol Sintáctico Abstracto.

Nuestra gramática genera un analizador que es capaz de reconocer cualquier cadena válida en el lenguaje. Como input se tiene la cadena mencionada anteriormente y el programa realiza una representación legible del árbol sintáctico abstracto correspondiente.

La gramática es ambigua y de izquierda, tratamos los conflictos de ambigüedad con precedencia y asociatividad.

La gramática y el parser fueron escritos utilizando la librería Yacc de Python.

La formulación/implementación del analizador sintáctico fue la siguiente:

Con `p_programa` se define la gramática de la estructura del programa completo, comenzando con el bloque de declaraciones demarcado por el token `with` seguido por el bloque de secuencias de instrucción con `begin`.

Para la gramática del bloque de declaraciones se definieron las siguientes reglas: `p_lista_declaraciones`, `p_lista_identificadores`, `p_lista_identificadores_identificador` y `p_tipo`. Respectivamente haciendo referencia a la estructura típica de una declaración de variables en el lenguaje `with var a : int`. Para esta fase las declaraciones de variables no son reportadas en el árbol sintáctico abstracto.

Se tiene una función muy importante, `p_empty` que sirve de caso base para las recursiones presentes en las gramáticas cuando se termina de procesar la instrucción.

Para el bloque de instrucciones se tienen las siguientes gramáticas:

+ `p_secuenciacion`
+ `p_secuenciacion2`
+ `p_secuenciacion_instruccion`
+ `p_instruccion`

Luego, las funciones definidas anteriormente hacen llamadas a las funciones respectivas dependiendo del tipo de instrucción:

+ `p_asignacion` para a<-2 o a.2
+ `p_condicional` para if [expresión booleana] -> [instrucción] otherwise -> [instrucción]
+ `p_alcance` para bloques de with begin anidados
+ `p_entrada_salida` para instrucciones de tipo `read` y `print`
+ `p_indeterminado` para ciclos While
+ `p_derminado` para ciclos for

Se procede a definir los tipos de literales e identificadores:

+ `p_identificador` determinado por el token TkId
+ `p_literal` el cual puede ser un entero, booleano o un caracter

La gramática de los tipos de expresiones son las siguientes:

+ `p_expresion`
+ `p_expresion_aritmetica`
+ `p_expr_minus`
+ `p_expresion_aritmetica_literal_identificador`
+ `p_expresion_booleana`
+ `p_expresion_booleana_literal_identificador`
+ `p_expresion_caracteres`
+ `p_expresion_caracteres_literal`
+ `p_expresion_arreglos`
+ `p_expresion_arreglos_literal`
+ `p_expresion_relacional`

Para reportar errores se utiliza la función `p_error`


Se define la variable `precedence` el cual nos ayuda a solventar ambigüedades. Yacc le permite a los tokens asignarles un nivel de precedencia y asociatividad.

Finalmente, para la impresión de Árbol Sintáctico Abstracto se creó la clase `Node` que tiene como atributos el tipo de instrucción, su hijo que representa la sub instrucción y las hojas. Sobre el string `respuesta` se va concatenando la construcción del árbol para ser mostrada como salida del programa.

Para poder mostrar de manera exitosa el árbol, la solución tuvo un alcance sobre el algoritmo DFS para ir recorriendo cada instrucción analizando las subexpresiones que contiene y así recursivamente hasta llegar a las hojas, que hasta los momentos son tokens TkId y Literales.

