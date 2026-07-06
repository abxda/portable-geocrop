"""Module 1 — Just enough Python."""

from course.common import md, code

MODULE = dict(
    num=1,
    fname={"en": "01_just_enough_python.ipynb", "es": "01_python_justo.ipynb"},
    title={"en": "Module 1 — Just enough Python",
           "es": "Módulo 1 — El Python justo y necesario"},
    cards=[],
    cells=[

md(
"""# 🐍 Module 1 — Just enough Python

This module teaches **only** the Python that the rest of the course uses —
nothing more. Every example is already about satellites: pixel values,
reflectance, bands. By the end you will speak just enough Python to open a
real satellite image in Module 2 and understand what you are looking at.

One idea carries the whole module: **a satellite image is just a grid of
numbers**. Learn to store numbers, group them, transform them and draw
them — and you can do remote sensing.
""",
"""# 🐍 Módulo 1 — El Python justo y necesario

Este módulo enseña **solo** el Python que usa el resto del curso — nada
más. Cada ejemplo trata ya de satélites: valores de píxel, reflectancia,
bandas. Al terminar hablarás el Python suficiente para abrir una imagen
satelital real en el Módulo 2 y entender qué estás viendo.

Una sola idea sostiene todo el módulo: **una imagen satelital es solo una
cuadrícula de números**. Aprende a guardar números, agruparlos,
transformarlos y dibujarlos — y ya puedes hacer percepción remota.
"""),

md(
"""## 🧭 Objectives

By the end of this module you will be able to:

- Store values in **variables** and show them with `print`.
- Keep several values together in a **list** and pick them by position
  (counting **from 0**!).
- Package a small calculation as a **function** with `def`.
- Create **NumPy arrays**, check their `shape`, and operate on *all* their
  numbers at once — the way we will treat images.
- Draw your first two plots with **matplotlib**: a curve and a tiny
  8x8 "image" made of numbers you invented.
""",
"""## 🧭 Objetivos

Al terminar este módulo sabrás:

- Guardar valores en **variables** y mostrarlos con `print`.
- Mantener varios valores juntos en una **lista** y tomarlos por posición
  (¡contando **desde 0**!).
- Empaquetar un cálculo pequeño como **función** con `def`.
- Crear **arreglos NumPy**, revisar su `shape`, y operar sobre *todos* sus
  números a la vez — que es como trataremos las imágenes.
- Dibujar tus primeras dos gráficas con **matplotlib**: una curva y una
  "imagen" diminuta de 8x8 hecha de números que tú inventaste.
"""),

md(
"""## 📚 Variables: giving numbers a name

A satellite measures **how much light** each patch of ground reflects.
That measurement — the **reflectance** — is a number between 0 (reflects
nothing) and 1 (reflects everything). Healthy vegetation reflects little
red light (it absorbs it to photosynthesize) and a *lot* of near-infrared.

In Python you store a value by giving it a name with `=`. That named value
is a **variable**, and `print` shows it. Names should say what the value
*means* — `red_reflectance` tells a story; `x` does not.
""",
"""## 📚 Variables: darle nombre a los números

Un satélite mide **cuánta luz** refleja cada pedacito de terreno. Esa
medición — la **reflectancia** — es un número entre 0 (no refleja nada) y
1 (lo refleja todo). La vegetación sana refleja poca luz roja (la absorbe
para hacer fotosíntesis) y *muchísimo* infrarrojo cercano.

En Python guardas un valor dándole un nombre con `=`. Ese valor con nombre
es una **variable**, y `print` lo muestra. Los nombres deben decir qué
*significa* el valor — `reflectancia_rojo` cuenta una historia; `x` no.
"""),

code(
"""# Reflectance of one healthy-crop pixel, in two colors of light
red_reflectance = 0.05    # plants absorb red light -> low value
nir_reflectance = 0.45    # plants bounce back near-infrared -> high value

print("Red reflectance :", red_reflectance)
print("NIR reflectance :", nir_reflectance)

# Variables combine with ordinary arithmetic: + - * /
difference = nir_reflectance - red_reflectance
print("NIR minus red   :", difference)   # big gap = healthy plant!""",
"""# Reflectancia de un píxel de cultivo sano, en dos colores de luz
reflectancia_rojo = 0.05   # las plantas absorben la luz roja -> valor bajo
reflectancia_nir  = 0.45   # las plantas rebotan el infrarrojo cercano -> valor alto

print("Reflectancia rojo :", reflectancia_rojo)
print("Reflectancia NIR  :", reflectancia_nir)

# Las variables se combinan con aritmética normal: + - * /
diferencia = reflectancia_nir - reflectancia_rojo
print("NIR menos rojo    :", diferencia)   # brecha grande = ¡planta sana!"""),

md(
"""## 📚 Lists: several values, one name — and counting from 0

A satellite does not measure one color: it measures many **bands** (blue,
green, red, near-infrared...). A **list** keeps those values together, in
order, under one name: `[0.03, 0.05, 0.05, 0.45]`.

You pick an element by its **position in square brackets** — and here comes
the surprise that trips up every beginner: **Python counts from 0**. The
first element is `values[0]`, the second is `values[1]`. Negative positions
count from the end: `values[-1]` is the last one. Remember this — image
band numbers will follow the same rule for the whole course.
""",
"""## 📚 Listas: varios valores, un nombre — y contar desde 0

Un satélite no mide un color: mide muchas **bandas** (azul, verde, rojo,
infrarrojo cercano...). Una **lista** mantiene esos valores juntos, en
orden, bajo un solo nombre: `[0.03, 0.05, 0.05, 0.45]`.

Un elemento se toma por su **posición entre corchetes** — y aquí viene la
sorpresa que tropieza a todo principiante: **Python cuenta desde 0**. El
primer elemento es `valores[0]`, el segundo es `valores[1]`. Las posiciones
negativas cuentan desde el final: `valores[-1]` es el último. Recuérdalo —
los números de banda de las imágenes seguirán esta regla todo el curso.
"""),

code(
"""# One pixel seen in 4 bands: blue, green, red, near-infrared (NIR)
band_names  = ["blue", "green", "red", "nir"]
reflectance = [0.03, 0.05, 0.05, 0.45]

print("First band  (position 0):", band_names[0], "=", reflectance[0])
print("Third band  (position 2):", band_names[2], "=", reflectance[2])
print("Last band   (position -1):", band_names[-1], "=", reflectance[-1])
print("How many bands?", len(reflectance))""",
"""# Un píxel visto en 4 bandas: azul, verde, rojo, infrarrojo cercano (NIR)
nombres_banda = ["azul", "verde", "rojo", "nir"]
reflectancia  = [0.03, 0.05, 0.05, 0.45]

print("Primera banda (posición 0):", nombres_banda[0], "=", reflectancia[0])
print("Tercera banda (posición 2):", nombres_banda[2], "=", reflectancia[2])
print("Última banda  (posición -1):", nombres_banda[-1], "=", reflectancia[-1])
print("¿Cuántas bandas?", len(reflectancia))"""),

md(
"""## 📚 Functions: name a calculation, reuse it forever

You will compute "NIR minus red, divided by their sum" thousands of times
in this course (it has a famous name — you will meet it properly in
Module 4). Instead of retyping it, Python lets you **define a function**
with `def`: give the recipe a name, list its ingredients (parameters), and
`return` the result. Indentation (the spaces at the start of the line)
marks which lines belong to the function.
""",
"""## 📚 Funciones: dale nombre a un cálculo y reúsalo por siempre

En este curso calcularás "NIR menos rojo, dividido entre su suma" miles de
veces (tiene un nombre famoso — lo conocerás formalmente en el Módulo 4).
En vez de reescribirlo, Python te deja **definir una función** con `def`:
le das nombre a la receta, listas sus ingredientes (parámetros), y con
`return` devuelves el resultado. La sangría (los espacios al inicio de la
línea) marca qué líneas pertenecen a la función.
"""),

code(
"""# A function: takes red and NIR reflectance, returns a 'greenness' score
def greenness(red, nir):
    return (nir - red) / (nir + red)

# Call it on three different pixels:
print("Healthy crop :", greenness(0.05, 0.45))   # near +1
print("Bare soil    :", greenness(0.20, 0.25))   # near 0
print("Water        :", greenness(0.06, 0.02))   # negative!""",
"""# Una función: recibe reflectancia roja y NIR, devuelve un puntaje de 'verdor'
def verdor(rojo, nir):
    return (nir - rojo) / (nir + rojo)

# Llámala con tres píxeles distintos:
print("Cultivo sano :", verdor(0.05, 0.45))   # cerca de +1
print("Suelo desnudo:", verdor(0.20, 0.25))   # cerca de 0
print("Agua         :", verdor(0.06, 0.02))   # ¡negativo!"""),

md(
"""## 📚 NumPy: because an image is a 2D array of numbers

A single satellite image of our Yaqui Valley tile has 384 x 384 =
**147,456 pixels per band**. Lists are too slow and clumsy for that.
**NumPy** gives us the **array**: a grid of numbers that Python can
transform *all at once* — no loops needed. That is called a
**vectorized** operation, and it is the daily bread of remote sensing:

- `arr.shape` tells you the grid's size, e.g. `(8, 8)` = 8 rows x 8 columns.
- `arr / 10000` divides **every** number in the array in one stroke.
- `arr.mean()`, `arr.max()` summarize the whole grid.

Satellite files usually store reflectance as whole numbers (e.g. `4500`
means 0.45) to save space — so "divide the whole image by 10000" is
literally the first thing we will do to real data in Module 2.
""",
"""## 📚 NumPy: porque una imagen es un arreglo 2D de números

Una sola imagen satelital de nuestro tile del Valle del Yaqui tiene
384 x 384 = **147,456 píxeles por banda**. Las listas son demasiado lentas
y torpes para eso. **NumPy** nos da el **arreglo**: una cuadrícula de
números que Python transforma *toda a la vez* — sin bucles. Eso se llama
operación **vectorizada**, y es el pan de cada día de la percepción remota:

- `arr.shape` te dice el tamaño de la cuadrícula, p. ej. `(8, 8)` = 8
  filas x 8 columnas.
- `arr / 10000` divide **cada** número del arreglo de un solo golpe.
- `arr.mean()`, `arr.max()` resumen toda la cuadrícula.

Los archivos satelitales suelen guardar la reflectancia como enteros
(p. ej. `4500` significa 0.45) para ahorrar espacio — así que "divide toda
la imagen entre 10000" es literalmente lo primero que haremos con datos
reales en el Módulo 2.
"""),

code(
"""# From list to array: now math applies to ALL values at once
import numpy as np

# Raw pixel values as a satellite file stores them (scaled by 10000)
raw_values = np.array([300, 500, 500, 4500])
print("Raw values :", raw_values)
print("Shape      :", raw_values.shape)     # (4,) -> 4 values in a row

reflectance = raw_values / 10000            # one line converts them ALL
print("Reflectance:", reflectance)
print("Mean       :", reflectance.mean())
print("Maximum    :", reflectance.max())""",
"""# De lista a arreglo: ahora la matemática aplica a TODOS los valores a la vez
import numpy as np

# Valores crudos de píxel tal como los guarda un archivo satelital (escalados x 10000)
valores_crudos = np.array([300, 500, 500, 4500])
print("Valores crudos:", valores_crudos)
print("Shape         :", valores_crudos.shape)   # (4,) -> 4 valores en fila

reflectancia = valores_crudos / 10000            # una línea los convierte TODOS
print("Reflectancia  :", reflectancia)
print("Media         :", reflectancia.mean())
print("Máximo        :", reflectancia.max())"""),

code(
"""# A 2D array IS a mini-image: 8x8 'pixels' of NIR reflectance we invent
mini_image = np.full((8, 8), 0.20)     # start: bare soil everywhere (0.20)
mini_image[2:6, 2:6] = 0.45            # rows 2-5, cols 2-5: a healthy field
mini_image[:, 0] = 0.02                # entire column 0: an irrigation canal

print("Shape:", mini_image.shape)      # (8, 8) -> 8 rows x 8 columns
print("Pixel at row 3, col 3:", mini_image[3, 3])   # inside the field
print("Pixel at row 0, col 0:", mini_image[0, 0])   # in the canal

# Slicing reads whole regions: row 3, all its columns
print("Row 3 :", mini_image[3, :])""",
"""# Un arreglo 2D ES una mini-imagen: 8x8 'píxeles' de reflectancia NIR inventada
mini_imagen = np.full((8, 8), 0.20)    # inicio: puro suelo desnudo (0.20)
mini_imagen[2:6, 2:6] = 0.45           # filas 2-5, cols 2-5: una parcela sana
mini_imagen[:, 0] = 0.02               # toda la columna 0: un canal de riego

print("Shape:", mini_imagen.shape)     # (8, 8) -> 8 filas x 8 columnas
print("Píxel en fila 3, col 3:", mini_imagen[3, 3])   # dentro de la parcela
print("Píxel en fila 0, col 0:", mini_imagen[0, 0])   # en el canal

# El slicing lee regiones completas: la fila 3, todas sus columnas
print("Fila 3:", mini_imagen[3, :])"""),

md(
"""## 📚 matplotlib: numbers you can *see*

Staring at grids of numbers gets old fast. **matplotlib** turns them into
pictures with two commands you will use constantly:

- `plt.plot(x, y)` draws a **curve** — perfect for how reflectance changes
  from band to band (a *spectral signature*, the fingerprint of a surface).
- `plt.imshow(array_2d)` paints a **2D array as an image**, coloring each
  number — which is exactly how every satellite image in this course will
  reach your eyes.
""",
"""## 📚 matplotlib: números que puedes *ver*

Mirar cuadrículas de números cansa rápido. **matplotlib** las convierte en
imágenes con dos comandos que usarás constantemente:

- `plt.plot(x, y)` dibuja una **curva** — perfecta para ver cómo cambia la
  reflectancia de banda en banda (una *firma espectral*, la huella digital
  de una superficie).
- `plt.imshow(arreglo_2d)` pinta un **arreglo 2D como imagen**, dándole
  color a cada número — que es exactamente como llegará a tus ojos cada
  imagen satelital de este curso.
"""),

code(
"""# Your first plot: two invented spectral 'signatures'
import matplotlib.pyplot as plt

bands = ["blue", "green", "red", "nir"]
crop  = np.array([0.03, 0.05, 0.05, 0.45])   # healthy crop pixel
soil  = np.array([0.10, 0.15, 0.20, 0.25])   # bare soil pixel

plt.figure(figsize=(6, 4))
plt.plot(bands, crop, marker="o", color="green", label="healthy crop")
plt.plot(bands, soil, marker="s", color="peru",  label="bare soil")
plt.ylabel("reflectance")
plt.title("Two surfaces, two light fingerprints")
plt.legend()
plt.show()""",
"""# Tu primera gráfica: dos 'firmas' espectrales inventadas
import matplotlib.pyplot as plt

bandas  = ["azul", "verde", "rojo", "nir"]
cultivo = np.array([0.03, 0.05, 0.05, 0.45])   # píxel de cultivo sano
suelo   = np.array([0.10, 0.15, 0.20, 0.25])   # píxel de suelo desnudo

plt.figure(figsize=(6, 4))
plt.plot(bandas, cultivo, marker="o", color="green", label="cultivo sano")
plt.plot(bandas, suelo,  marker="s", color="peru",  label="suelo desnudo")
plt.ylabel("reflectancia")
plt.title("Dos superficies, dos huellas de luz")
plt.legend()
plt.show()""" ),

code(
"""# And now SEE your 8x8 mini-image: imshow paints the array
plt.figure(figsize=(5, 4))
plt.imshow(mini_image, cmap="RdYlGn", vmin=0, vmax=0.5)
plt.title("My first 'satellite image' (8x8 invented pixels)")
plt.colorbar(label="NIR reflectance")
plt.show()
print("Green field, brown soil, dark canal — all from a grid of numbers.")""",
"""# Y ahora VE tu mini-imagen de 8x8: imshow pinta el arreglo
plt.figure(figsize=(5, 4))
plt.imshow(mini_imagen, cmap="RdYlGn", vmin=0, vmax=0.5)
plt.title("Mi primera 'imagen satelital' (8x8 píxeles inventados)")
plt.colorbar(label="reflectancia NIR")
plt.show()
print("Parcela verde, suelo café, canal oscuro — todo desde una cuadrícula de números.")"""),

md(
"""## You are ready for real data

Look at what you just did: you stored reflectance in variables, grouped
bands in lists, wrapped a calculation in a function, transformed a whole
grid of pixels in one NumPy stroke, and *painted numbers as an image*.

That 8x8 grid was invented. In **Module 2** you will do the exact same
moves — `shape`, slicing, `imshow` — on a **real satellite image** of the
Yaqui Valley, and learn *how* the satellite produced those numbers in the
first place.
""",
"""## Ya estás listo para datos reales

Mira lo que acabas de hacer: guardaste reflectancia en variables,
agrupaste bandas en listas, envolviste un cálculo en una función,
transformaste toda una cuadrícula de píxeles de un solo golpe de NumPy, y
*pintaste números como imagen*.

Esa cuadrícula de 8x8 era inventada. En el **Módulo 2** harás exactamente
los mismos movimientos — `shape`, slicing, `imshow` — sobre una **imagen
satelital real** del Valle del Yaqui, y aprenderás *cómo* produjo el
satélite esos números en primer lugar.
"""),

md(
"""## 🧪 Check yourself

**In the list `reflectance = [0.03, 0.05, 0.05, 0.45]`, what does
`reflectance[1]` give you — and why not 0.03?**

<details><summary>Show answer</summary>

It gives `0.05`, the *second* element. Python counts positions from **0**,
so `reflectance[0]` is the first element (0.03) and `reflectance[1]` is
the second. Band numbering in images will follow the same from-0 rule.

</details>

**An array has `shape` equal to `(384, 384)`. What is it, in image terms,
and what does `arr / 10000` do to it?**

<details><summary>Show answer</summary>

It is a 2D grid of 384 rows by 384 columns — one band of a 384x384-pixel
image. `arr / 10000` divides *every one* of its 147,456 numbers at once
(a vectorized operation), e.g. converting stored integers like 4500 into
reflectance values like 0.45.

</details>

**You want to *look at* a 2D array of pixel values. Which matplotlib
command do you reach for: `plt.plot` or `plt.imshow`?**

<details><summary>Show answer</summary>

`plt.imshow` — it paints a 2D array as an image, one colored square per
number. `plt.plot` draws curves, like a spectral signature across bands.

</details>
""",
"""## 🧪 Ponte a prueba

**En la lista `reflectancia = [0.03, 0.05, 0.05, 0.45]`, ¿qué te da
`reflectancia[1]` — y por qué no 0.03?**

<details><summary>Ver respuesta</summary>

Da `0.05`, el *segundo* elemento. Python cuenta posiciones desde **0**,
así que `reflectancia[0]` es el primer elemento (0.03) y `reflectancia[1]`
es el segundo. La numeración de bandas en las imágenes seguirá la misma
regla desde 0.

</details>

**Un arreglo tiene `shape` igual a `(384, 384)`. ¿Qué es, en términos de
imagen, y qué le hace `arr / 10000`?**

<details><summary>Ver respuesta</summary>

Es una cuadrícula 2D de 384 filas por 384 columnas — una banda de una
imagen de 384x384 píxeles. `arr / 10000` divide *cada uno* de sus 147,456
números a la vez (operación vectorizada), p. ej. convirtiendo enteros
guardados como 4500 en reflectancias como 0.45.

</details>

**Quieres *mirar* un arreglo 2D de valores de píxel. ¿Qué comando de
matplotlib usas: `plt.plot` o `plt.imshow`?**

<details><summary>Ver respuesta</summary>

`plt.imshow` — pinta un arreglo 2D como imagen, un cuadrito de color por
número. `plt.plot` dibuja curvas, como una firma espectral a lo largo de
las bandas.

</details>
"""),

],
)
