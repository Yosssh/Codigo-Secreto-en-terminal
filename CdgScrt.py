import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import pygame as pg
import random
import numpy as np
from rich import print as rprint
from rich.table import Table
from rich.console import Console
from rich.table import Table
import os
from rich.panel import Panel #ya lo usare
import random
import ajustes

palabrejos = ["perro", "gato", "elefante", "jirafa", "ballena", "águila", "hormiga", "mariposa", "león", "tigre", "caballo", "vaca", "oveja", "cerdo", "pollo", "pez", "serpiente", "rana", "conejo", "ardilla", "España", "Francia", "Alemania", "Italia", "Japón", "China", "Brasil", "Rusia", "Canadá", "Australia", "Estados Unidos", "Reino Unido", "India", "México", "Argentina"
, "Madrid", "París", "Berlín", "Roma", "Tokio", "Pekín", "Río de Janeiro", "Moscú", "Ottawa", "Sídney", "Nueva York", "Londres", "Barcelona", "Los Ángeles", "Chicago", "México DF", "Buenos Aires", "Shanghai", "Delhi", "Cairo", "manzana", "platano", "naranja", "uva", "pera", "cereza", "sandía", "melón", "piña", "mango", "fresa", "kiwi", "limón", "aguacate", "tomate", "zanahoria", "cebolla", "arroz", "pasta", "pan", "carne", "pescado", "huevo", "leche", "queso",
"rojo", "azul", "verde", "amarillo", "negro", "blanco", "rosa", "violeta", "marrón", "naranja", "gris", "plata", "oro", "fútbol", "baloncesto", "tenis", "natación", "voleibol", "atletismo", "ciclismo", "gimnasia", "boxeo", "rugby", "bádminton", "hockey", "golf", "esquí", "patinaje",
"guitarra", "piano", "violín", "batería", "flauta", "saxofón", "trompeta", "arpa", "violonchelo", "oboe", "acordeón", "trombón", "clarinete", "camiseta", "pantalón", "vestido", "falda", "abrigo", "calcetines", "zapatos", "sombrero", "bufanda", "guantes", "chaqueta", "jersey", "pijama", "bañador", "traje",
"libro", "bolígrafo", "mesa", "silla", "coche", "móvil", "ordenador", "llave", "reloj", "ventana", "puerta", "espejo", "cama", "sofá", "lámpara", "cuadro", "maceta", "pelota", "cuerda", "papel", "martillo", "destornillador", "sierra", "clavos", "tornillos", "lija", "llave inglesa", "alicate", "taladro", "broca", "cinta métrica",
"médico", "enfermero", "profesor", "abogado", "ingeniero", "policía", "bombero", "cocinero", "músico", "artista", "científico", "programador", "escritor", "actor", "diseñador", "coche", "moto", "bicicleta", "avión", "barco", "tren", "autobús", "camión", "helicóptero", "submarino",
"pizza", "pasta", "sushi", "hamburguesa", "ensalada", "sopa", "curry", "fajitas", "paella", "ramen", "tacos", "burritos", "falafel", "kebab", "risotto", "lasaña", "tortilla", "Willy wonka", "Jack Sparrow", "Homer", "Doraeom", "kid keo", "porro", "maricon", "zurrapa", "canuto", "nabo", "polla", "montalban", "arViseh", "camello", "perro Sanxe", "mamahuevo", "mariwana"
]

# Función para elegir una palabra aleatoria de una lista
def elegir_palabra(lista=palabrejos):
    return random.choice(lista)

def get_palabras():
    palabras = []
    palabras_usadas = set()

    while len(palabras) < 25:
        palabra = elegir_palabra().upper()
        if palabra not in palabras_usadas and len(palabra) > 1:
            palabras_usadas.add(palabra)
            palabras.append(palabra)
        else:
            # Si la palabra ya está en el conjunto o es demasiado corta, generar otra
            while palabra in palabras_usadas:
                palabra = elegir_palabra().upper()
            palabras_usadas.add(palabra)
            palabras.append(palabra)

    # Convertir la lista plana en una matriz de 5x5
    return [palabras[i:i+5] for i in range(0, 25, 5)]

def enviar_correo_con_imagen(destinatario, asunto, cuerpo, ruta_imagen):
    """Envía un correo electrónico con una imagen adjunta.

    Args:
        destinatario: Dirección de correo del destinatario.
        asunto: Asunto del correo.
        cuerpo: Cuerpo del mensaje.
        ruta_imagen: Ruta completa al archivo de imagen.
    """

    # Datos de Gmail (recomendable una contraseña de aplicación)
    gmail_user = ''
    gmail_password = ''

    # Crear el mensaje principal
    mensaje = MIMEMultipart()
    mensaje['From'] = gmail_user
    mensaje['To'] = destinatario
    mensaje['Subject'] = asunto

    # Crear el cuerpo del mensaje
    cuerpo_mensaje = MIMEText(cuerpo)
    mensaje.attach(cuerpo_mensaje)

    # Abrir la imagen y crear un objeto MIMEImage
    with open(ruta_imagen, 'rb') as img:
        imagen = MIMEImage(img.read())
        imagen.add_header('Content-Disposition', 'attachment', filename=ruta_imagen.split('/')[-1])
        mensaje.attach(imagen)

    # Conectar al servidor SMTP de Gmail y enviar el correo
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(gmail_user, gmail_password)
        server.sendmail(gmail_user, destinatario, mensaje.as_string())

def contar_colores(array):
    return [np.count_nonzero(array == color) for color in range(4)]

def generar_partida():
    azul_n = 8
    rojo_n = 8
    blanco_n = 7
    negro_n = 1
    colores = [0,1,2,3]
    pesos = [0.25,0.25,0.25,0.25]
    empieza = random.choice([2,3])

    if empieza == 2:
        rojo_n += 1
    
    elif empieza == 3:
        azul_n += 1

    casillas = [negro_n, blanco_n, rojo_n, azul_n]


    map = np.full((5,5),-1)

    for f in range(0,5):
        for c in range(0,5):
            colocado = False
            while colocado == False:
                color = random.choices(colores, pesos)[0]
                cuenta = contar_colores(map)

                if cuenta[color] < casillas[color]:
                    map[f,c] = color
                    colocado = True
    n = [rojo_n, azul_n]

    return [empieza, map, n]

def get_color(n):
    colores = [["[bold red]", "[/bold red]"],["[bold blue]", "[/bold blue]"],["[bold purple]", "[/bold purple]"], ["[bold yellow]", "[/bold yellow]"]]

    if n == 2:
        color = colores[0]

    elif n == 3:
        color = colores[1]

    elif n == 1:
        color = colores[3]

    elif n == 0:
        color = colores[2]
    
    return color

def colores_tablero(map):
    colores_tabl = [[get_color(map[f,c]) for c in range(5)] for f in range(5)]

    return colores_tabl

def get_index(palabra, lista_palabras):
    for f in range(5):
        for c in range(5):
            if palabra == lista_palabras[f][c]:
                indice = [f,c]
            
            else:
                continue

    return indice

def poner_color_palabra(palabra, palabrs, colores, index):
    f,c = index
    palabras = palabrs
    palabras[f][c] = colores[f][c][0] + palabra + colores[f][c][1]
    
    return palabras

def comprobar_acierto(palabra, map, lista_palabras, colores, color_to_play):
    fila,columna = get_index(palabra, lista_palabras)

    if map[fila,columna] == color_to_play:
        acierto = True
    
    elif map[fila, columna] == 0:
        acierto = 'Se acabó'

    else:
        acierto = False

    palabras_tabla = poner_color_palabra(palabra, lista_palabras, colores, [fila,columna])

    return [acierto, palabras_tabla, map[fila,columna]]

def cambiar_color(color):
    if color == 2:
        ahora = 3
    else:
        ahora = 2
    return ahora

def array_to_png(partida):
    color_primero = partida[0]
    map = partida[1]
    colores = {
        0: (0, 0, 0),  # Negro
        1: (255, 255, 255),  # Blanco
        2: (255, 0, 0),  # Rojo
        3: (0, 0, 255)  # Azul
    }
    negro = (64,64,64)

    # Inicializar Pygame
    pg.init()

    # Crear una superficie de 50x50 píxeles
    sheet = pg.Surface((150, 200))
    sheet.fill((64,64,64))

    # Rellenar la superficie con los colores del array
    for f in range(5):
        for c in range(5):
            color = colores[map[f, c]]  # Obtener el color del diccionario
            pg.draw.rect(sheet, color, (c * 30, f * 30, 30, 30))  # Dibujar un rectángulo

    for f in range(5):
            for c in range(5):
                pg.draw.rect(sheet, negro, (c * 30, f * 30, 30, 30), 2)

    pg.draw.circle(sheet, colores[color_primero], (75,175), 15)

    # Guardar la imagen como PNG
    pg.image.save(sheet, "tablero.png")

    # Salir de Pygame
    pg.quit()

def print_tablero(palabras):
    console = Console()
    table = Table(show_header=False)
    for f in palabras:
        table.add_row(f[0], f[1], f[2], f[3], f[4])
    rprint(table)

def print_tablero_2(palabras):
    console = Console()
    table = Table(show_header=False, style="bold", show_lines=True, expand=True)  # Fuente en negrita

    table.add_column(justify="center")
    table.add_column(justify="center")
    table.add_column(justify="center")
    table.add_column(justify="center")
    table.add_column(justify="center")

    # Ajustar el ancho de las columnas
    table.column_widths = (40, 40, 40, 40, 40)

    for fila in palabras:
        table.add_row(*fila)

    console.print(table)

def actualizar_contador(n, color):
    color_to_ind = {
        2 : 0,
        3 : 1
    }
    copy = n
    if color != 1:
        copy[color_to_ind[color]] = n[color_to_ind[color]] - 1

    return copy

console = Console()

def main():
    juega, tablero, n = generar_partida()
    words_to_guess = get_palabras()
    colores = colores_tablero(tablero)
    
    array_to_png([juega,tablero])

    informadores = input("Quienes dirán las palabras: ").split(' ')

    ruta_imagen = "C:/Users/Josh/Desktop/Codigo Secreto/tablero.png"

    enviar = input("y/n")
    if enviar == 'y':
        enviar_correo_con_imagen(ajustes.jugadores[informadores[0]], 'Objetivos', "", ruta_imagen)
        enviar_correo_con_imagen(ajustes.jugadores[informadores[1]], 'Objetivos', "", ruta_imagen)
    

    #enviar_correo_con_imagen('fisicajosh@gmail.com', 'Correo con imagen', f"Empieza el {color_primero}", ruta_imagen)

    #enviar_correo_con_imagen('josemarijunior2@gmail.com', 'Correo con imagen', f"", ruta_imagen)


    game = True

    translate = {
        2 : '[bold red]rojo[/bold red]',
        3 : '[bold blue]azul[/bold blue]'
    }

    while game:
        os.system('cls')
        print(n)
        print_tablero_2(words_to_guess)
        rprint(f"\nJuega el {translate[juega]}")
        entrada = input('\nPalabra: ').upper()

        if entrada == "PASO":
            juega = cambiar_color(juega)
        else:
            try:
                control = comprobar_acierto(entrada, tablero, words_to_guess, colores, juega)
                n = actualizar_contador(n, control[2])

                if control[0] == 'Se acabó':
                    os.system('cls')
                    print_tablero_2(words_to_guess)
                    rprint(f"\n{entrada} es la [bold purple]negra[/bold purple], [strikethrough]puto gilipollas[/strikethrough]")
                    game = False
            
                elif control[0] == False:
                    juega = cambiar_color(juega)

                else: 
                    continue

            except:
                n = actualizar_contador(n, 1)
                continue

main()
'''
entrada = None
palabras = []

while entrada != 'adios':
    entrada = input("palabra:")
    if entrada != 'adios':
        palabras.append(entrada)

print(palabras)

'''
