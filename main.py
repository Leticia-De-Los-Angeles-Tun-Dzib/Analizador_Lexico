#Proyecto: analizador lexico de Visual basic

# Tema 4: Analísis lexico
# Integrantes:
# -Liliana Isabel Canche Noh
# -Mario Alberto Carvajal Aguilar
# -Junior Jesus Tello Sanchez
# -Leticia de los Angeles Tun Dzib

#Importa las librerias necesarias para el funcionamiento del programa
import sys
import ply.lex as lex
from ply.lex import Lexer

# Se crea la biblioteca para guardar los resultados
resultado_lexema = []

reserved = {#Se enlistan las palabras reservadas que se utilizaran
    'AddHandler':'ADDHANDLER',
    'AndAlso':'ANDALSO',
    'Byte':'BYTE',
    'Boolean':'BOOLEAN',
    'ByVal':'BYVAL',
    'As':'AS',
    'Call':'CALL',
    'Continue':'CONTINUE',
    'Const':'CONST',
    'Decimal':'DECIMAL',
    'Dim':'DIM',
    'Error':'ERROR',
    'Date':'DATE',
    'Do':'DO',
    'Double':'DOUBLE',
    'Else':'ELSE',
    'ElseIf':'ELSE_IF',
    'String':'STRING',
    'End':'END',
    'Exit':'EXIT',
    'False':'FALSE',
    'Finally':'FINALLY',
    'For':'FOR',
    'Get':'GET',
    'Implements':'IMPLEMENTS',
    'In':'IN',
    'Interface':'INTERFACE',
    'Is':'IS',
    'Lib':'LIB',
    'Module':'MODULE',
    'Object':'OBJECT',
    'Of':'OF',
    'Private':'PRIVATE',
    'Public':'PUBLIC',
    'Static':'STATIC',
    'Try':'TRY',
    'True':'TRUE',
    'Then':'THEN',
    'When':'WHEN',
    'Nothing':'NOTHING',
    'While':'WHILE',
    'Sub':'SUB',
    'End Sub':'END_SUB',
    'Text':'Text',
    'If':'IF',
    'Catch ex':'CATCH_EX',
    'Case':'CASE',
    'Class':'CLASS',
    'EventArgs':'EVENTARGS',
    'Handles':'HANDLES',
    'Click':'Click',
}

tokens = list(reserved.values()) + [#Se enlistan los tokens en una lista

    'IDENTIFICADOR',
    'ENTERO',
    'ASIGNAR',
    'VARIABLE',

    'SUMA',
    'RESTA',
    'MULT',
    'DIV',
    'POTENCIA',
    'MODULO',

    'MINUSMINUS',
    'PLUSPLUS',

    # Condiones
    'SI',
    'SINO',
    # Ciclos
    'MIENTRAS',
    'PARA',
    # logica
    'AND',
    'OR',
    'NOT',
    'MENORQUE',
    'MENORIGUAL',
    'MAYORQUE',
    'MAYORIGUAL',
    'IGUAL',
    'DISTINTO',
    # Symbolos
    'NUMERAL',
    'PARIZQ',
    'PARDER',
    'CORIZQ',
    'CORDER',
    'LLAIZQ',
    'LLADER',
    'DOSPUNTOS',

    # Otros
    'PUNTOCOMA',
    'PUNTO',
    'COMA',
    'COMDOB',
    'MAYORDER',  # >>
    'MAYORIZQ',  # <<
    'ESPACIO',
    'COMENTARIO',
    'SALTO_LINEA',
]

#Se definen los tokens que tienen una expresion regular simple
t_SUMA = r'\+'
t_RESTA = r'-'
t_MINUSMINUS = r'\-\-'
t_PUNTO = r'\.'
t_MULT = r'\*'
t_DIV = r'/'
t_MODULO = r'\%'
t_POTENCIA = r'(\*{2} | \^)'

t_ASIGNAR = r'='
# Expresiones Logicas
t_AND = r'\&'
t_OR = r'\|{2}'
t_NOT = r'\!'
t_MENORQUE = r'<'
t_MAYORQUE = r'>'
t_PUNTOCOMA = ';'
t_COMA = r','
t_PARIZQ = r'\('
t_PARDER = r'\)'
t_CORIZQ = r'\['
t_CORDER = r'\]'
t_LLAIZQ = r'{'
t_LLADER = r'}'
t_COMDOB = r'\"'
t_DOSPUNTOS = r'\:'

#Se definen los tokens que necesitan una expresion regular mas compleja
def t_SI(t):
    r'If'
    return t


def t_SINO(t):
    r'Elseif'
    return t


def t_MIENTRAS(t):
    r'while'
    return t


def t_PARA(t):
    r'for'
    return t


def t_ENTERO(t):
    r'\d+(\.\d+)?'
    t.value = float(t.value)
    return t


def t_VARIABLE(t): #Definimos el token para las variables, el cual verifica si el valor del token se encuentra entre las palabras reservadas y procede a imprimirlo
    r'[a-z]([\w])*'
    if t.value in reserved:
        t.type = reserved[t.value]
        return t
    else:
        return t


def t_IDENTIFICADOR(t): #Definimos el token para los IDs el cual verifica si el valor del token se encuentra en las palabras reservadas y procede a imprimirlo o de lo contrario procede a t_error
    r'[a-zA-Z_][a-zA-Z_0-9_]*'
    if t.value in reserved:
        t.type = reserved[t.value]
        return t
    else:
        t_error(t)


def t_COMENTARIO(t):
    r'\'(.)*?\n+'
    t.lexer.lineno += 1
    return t


def t_SALTO_LINEA(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


def t_NUMERAL(t):
    r'\#'
    return t


def t_PLUSPLUS(t):
    r'\+\+'
    return t


def t_MENORIGUAL(t):
    r'<='
    return t


def t_MAYORIGUAL(t):
    r'>='
    return t


def t_IGUAL(t):
    r'=='
    return t


def t_MAYORDER(t):
    r'<<'
    return t


def t_MAYORIZQ(t):
    r'>>'
    return t


def t_DISTINTO(t):
    r'!='
    return t


def t_ESPACIO(t):
    r'\s+'
    t.lexer.lineno += len(t.value)


t_ignore = ' \t' #Definimos el token para \t el cual es muy importante para el funcionamiento de los demas


def t_error(t):   #Definimos el token de error para que este indique cual ha sido el error, lo ignore y proceda con la ejecución
    print("Error: "+str(t.value))
    t.lexer.skip(1)


def test(data, lexer): #Creamos el metodo test para vincular los datos del archivo con la libreria lexer
    lexer.input(data)  #Aqui ingresamos los datos a la libreria
    i = 1 # Representa la linea del documento
    while True: #indicamos al lexer que indentifique los tokens o de otro modo proceder con la ejecucion.
        tok = lexer.token()
        if not tok:
            break
        import texttable #Importamos la libreria texttable para facilitar la creacion de la tabla

        #Definimos las dimensiones de la tabla y los titulos de las columnas
        tableObj = texttable.Texttable()
        tableObj.set_cols_align(["l","r","c","v"])
        tableObj.set_cols_valign(["t","n","b","r"])
        tableObj.add_rows([
            ["Numero", "Linea de codigo", "Token", "Parte de codigo"],
            [str(i), str(tok.lineno), str(tok.type), str(tok.value)]
        ])

        #Dibujamos la tabla y aumentamos uno a la variable que recorre las filas del documento
        print(tableObj.draw())
        i += 1


# INICIALIZACION DEL ANALIZADOR LEXICO
# En esta parte del codigo procedemos a inicializar el analizador lexico llamando al metodo correspondiente (test)

lexer: Lexer = lex.lex()

if __name__ == '__main__':
    if len(sys.argv) > 1:
        fin = sys.argv[1]
    else:
        fin = 'Prueba.sln'
    f = open(fin,'r')#Abre el documento de texto
    data = f.read()#Lee el documento de texto
    test(data,lexer)