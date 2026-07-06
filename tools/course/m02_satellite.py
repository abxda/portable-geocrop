"""Module 2 — How a satellite sees the world."""

from course.common import md, code, LOAD_TILE_EN, LOAD_TILE_ES

MODULE = dict(
    num=2,
    fname={"en": "02_how_a_satellite_sees.ipynb", "es": "02_como_ve_un_satelite.ipynb"},
    title={"en": "Module 2 — How a satellite sees the world",
           "es": "Módulo 2 — Cómo ve el mundo un satélite"},
    cards=[
        ("remote-sensing", {"en": "Remote sensing, the field itself",
                            "es": "Percepción remota, el campo mismo"}),
        ("electromagnetic-spectrum", {"en": "The electromagnetic spectrum",
                                      "es": "El espectro electromagnético"}),
        ("reflectance", {"en": "Reflectance", "es": "Reflectancia"}),
        ("spectral-signature", {"en": "The spectral signature",
                                "es": "La firma espectral"}),
        ("spectral-bands", {"en": "Spectral bands", "es": "Bandas espectrales"}),
        ("resolution", {"en": "Resolution (spatial/spectral/temporal)",
                        "es": "Resolución (espacial/espectral/temporal)"}),
        ("landsat", {"en": "Landsat", "es": "Landsat"}),
        ("sentinel-missions", {"en": "The Sentinel missions",
                               "es": "Las misiones Sentinel"}),
    ],
    cells=[

md(
"""# 🛰️ Module 2 — How a satellite sees the world

🧭 **Objectives** — understand what a satellite actually measures, why an
image has many *bands*, what *reflectance* and a *spectral signature* are,
and the three *resolutions* that describe any sensor. Then open a **real**
tile of the Yaqui Valley and confirm it is exactly what Module 1 promised:
a grid of numbers.

📚 **The idea.** A satellite carries a **sensor** that measures how much
sunlight the ground **reflects** back, in several **bands** — narrow slices
of the electromagnetic spectrum. Our eyes see three bands (red, green,
blue). Satellites like **Landsat** and **Sentinel-2** see those *and* others
we cannot, especially **near-infrared (NIR)** and **short-wave infrared
(SWIR)**, where vegetation, soil and water differ the most.

The value stored for each pixel and band is **reflectance**: a fraction
between 0 and 1 of the light that bounced back (files store it as an integer
to save space, e.g. `4500` = 0.45). Plot reflectance across bands for one
pixel and you get its **spectral signature** — a fingerprint that says
"this is a thriving crop" or "this is bare soil".

![how a satellite sees](../../anim/en/01_where_it_runs.svg)
""",
"""# 🛰️ Módulo 2 — Cómo ve el mundo un satélite

🧭 **Objetivos** — entender qué mide realmente un satélite, por qué una
imagen tiene muchas *bandas*, qué son la *reflectancia* y una *firma
espectral*, y las tres *resoluciones* que describen a cualquier sensor.
Luego abrir un tile **real** del Valle del Yaqui y confirmar que es
exactamente lo que prometió el Módulo 1: una cuadrícula de números.

📚 **La idea.** Un satélite lleva un **sensor** que mide cuánta luz solar
**refleja** el suelo de vuelta, en varias **bandas** — rebanadas angostas
del espectro electromagnético. Nuestros ojos ven tres bandas (rojo, verde,
azul). Satélites como **Landsat** y **Sentinel-2** ven esas *y* otras que no
podemos, en especial el **infrarrojo cercano (NIR)** y el **infrarrojo de
onda corta (SWIR)**, donde vegetación, suelo y agua más se diferencian.

El valor guardado para cada píxel y banda es la **reflectancia**: una
fracción entre 0 y 1 de la luz que rebotó (los archivos la guardan como
entero para ahorrar espacio, p. ej. `4500` = 0.45). Grafica la reflectancia
a lo largo de las bandas de un píxel y obtienes su **firma espectral** — una
huella que dice "esto es un cultivo próspero" o "esto es suelo desnudo".

![cómo ve un satélite](../../anim/es/01_where_it_runs.svg)
"""),

md(
"""## Resolution: three ways to say "how detailed?"

Every sensor is described by three resolutions — remember them, they decide
what you can and cannot map:

- **Spatial**: how big is one pixel on the ground? Our tile is **30 m** per
  pixel (one pixel ≈ a small orchard). Finer = smaller fields visible.
- **Spectral**: how many bands, and how narrow? More bands = more chemistry
  you can read. Our tile has **6 spectral bands** plus derived indices.
- **Temporal**: how often does the satellite revisit? Every few days for
  Sentinel-2. This is what lets us watch a crop **grow** over a season.

📚 The data below is a **geomedian** (Module 3 explains it) of March 2018,
built from **NASA HLS** — Harmonized Landsat + Sentinel-2 — at 30 m.
""",
"""## Resolución: tres formas de decir "¿qué tan detallado?"

Todo sensor se describe con tres resoluciones — recuérdalas, deciden qué
puedes y qué no puedes mapear:

- **Espacial**: ¿qué tan grande es un píxel en el suelo? Nuestro tile es de
  **30 m** por píxel (un píxel ≈ una huerta pequeña). Más fina = parcelas
  más chicas visibles.
- **Espectral**: ¿cuántas bandas, y qué tan angostas? Más bandas = más
  química que puedes leer. Nuestro tile tiene **6 bandas espectrales** más
  índices derivados.
- **Temporal**: ¿cada cuánto revisita el satélite? Cada pocos días para
  Sentinel-2. Esto es lo que nos deja ver **crecer** un cultivo en la
  temporada.

📚 Los datos de abajo son una **geomediana** (el Módulo 3 la explica) de
marzo 2018, construida con **NASA HLS** — Landsat + Sentinel-2 armonizados —
a 30 m.
"""),

code(LOAD_TILE_EN, LOAD_TILE_ES),

md(
"""## Open the tile and read its shape

Just like the invented 8x8 array in Module 1 — but real. `rasterio` opens
GeoTIFF satellite files; `.read()` hands us a NumPy array with shape
`(bands, rows, cols)`.
""",
"""## Abre el tile y lee su forma

Igual que el arreglo inventado de 8x8 del Módulo 1 — pero real. `rasterio`
abre archivos satelitales GeoTIFF; `.read()` nos da un arreglo NumPy con
forma `(bandas, filas, columnas)`.
"""),

code(
"""import numpy as np
import rasterio
import matplotlib.pyplot as plt

with rasterio.open(TILE) as src:
    img = src.read()                     # (13, 384, 384) integer array
    band_names = list(src.descriptions)  # what each layer is

print("Array shape (bands, rows, cols):", img.shape)
print("Data type:", img.dtype)
print("The 13 layers:", band_names)
print("One pixel (row 200, col 200), all bands:", img[:, 200, 200])""",
"""import numpy as np
import rasterio
import matplotlib.pyplot as plt

with rasterio.open(TILE) as src:
    img = src.read()                       # arreglo entero (13, 384, 384)
    nombres_banda = list(src.descriptions) # qué es cada capa

print("Forma del arreglo (bandas, filas, cols):", img.shape)
print("Tipo de dato:", img.dtype)
print("Las 13 capas:", nombres_banda)
print("Un píxel (fila 200, col 200), todas las bandas:", img[:, 200, 200])"""),

md(
"""## See it in true color

The first three spectral bands are blue, green, red. Stack them (red, green,
blue order for display) and scale to 0–1, exactly the divide-by-a-number
trick from Module 1. This is the field as your eyes would see it from space.
""",
"""## Míralo en color verdadero

Las primeras tres bandas espectrales son azul, verde, rojo. Apílalas (en
orden rojo, verde, azul para mostrar) y escala a 0–1, justo el truco de
dividir entre un número del Módulo 1. Este es el campo como lo verían tus
ojos desde el espacio.
"""),

code(
"""# Bands 0,1,2 = blue, green, red. Display wants Red-Green-Blue.
rgb = np.clip(np.dstack([img[2], img[1], img[0]]) / 3000.0, 0, 1)

plt.figure(figsize=(7, 7))
plt.imshow(rgb)
plt.title("Yaqui Valley — true color (geomedian, March 2018)")
plt.axis("off")
plt.show()
print("Every field you see is a patch of ~30 m pixels.")""",
"""# Bandas 0,1,2 = azul, verde, rojo. Para mostrar se quiere Rojo-Verde-Azul.
rgb = np.clip(np.dstack([img[2], img[1], img[0]]) / 3000.0, 0, 1)

plt.figure(figsize=(7, 7))
plt.imshow(rgb)
plt.title("Valle del Yaqui — color verdadero (geomediana, marzo 2018)")
plt.axis("off")
plt.show()
print("Cada parcela que ves es un pedazo de píxeles de ~30 m.")"""),

md(
"""## The spectral signature: light fingerprints

Now the payoff. Pick two pixels — one on a green field, one on bare soil —
and plot their reflectance across the 6 spectral bands. The curves are their
**spectral signatures**. Notice the crop's jump into the NIR band: that gap
is invisible to your eyes but obvious to the satellite, and it is the whole
basis of vegetation indices in Module 4.
""",
"""## La firma espectral: huellas de luz

Ahora el premio. Elige dos píxeles — uno sobre una parcela verde, otro sobre
suelo desnudo — y grafica su reflectancia en las 6 bandas espectrales. Las
curvas son sus **firmas espectrales**. Fíjate en el salto del cultivo hacia
la banda NIR: esa brecha es invisible a tus ojos pero obvia para el satélite,
y es toda la base de los índices de vegetación del Módulo 4.
"""),

code(
"""# The 6 spectral bands are layers 0..5 (blue,green,red,nir,swir1,swir2)
spectral = ["blue", "green", "red", "nir", "swir1", "swir2"]

# NDVI (layer 6) helps us find a green pixel and a bare one automatically
ndvi = img[6] / 10000.0
green_rc = np.unravel_index(np.argmax(ndvi), ndvi.shape)   # most vegetated
soil_rc  = np.unravel_index(np.argmin(np.where(ndvi > 0, ndvi, 9)), ndvi.shape)

crop_sig = img[0:6, green_rc[0], green_rc[1]] / 10000.0
soil_sig = img[0:6, soil_rc[0],  soil_rc[1]]  / 10000.0

plt.figure(figsize=(7, 4))
plt.plot(spectral, crop_sig, marker="o", color="green", label="green field")
plt.plot(spectral, soil_sig, marker="s", color="peru",  label="bare soil")
plt.ylabel("reflectance"); plt.title("Spectral signatures of two real pixels")
plt.legend(); plt.show()
print("See the crop leap up at NIR — that is chlorophyll, not color.")""",
"""# Las 6 bandas espectrales son las capas 0..5 (azul,verde,rojo,nir,swir1,swir2)
espectrales = ["azul", "verde", "rojo", "nir", "swir1", "swir2"]

# El NDVI (capa 6) nos ayuda a hallar un píxel verde y uno desnudo automáticamente
ndvi = img[6] / 10000.0
verde_rc = np.unravel_index(np.argmax(ndvi), ndvi.shape)   # el más vegetado
suelo_rc = np.unravel_index(np.argmin(np.where(ndvi > 0, ndvi, 9)), ndvi.shape)

firma_cultivo = img[0:6, verde_rc[0], verde_rc[1]] / 10000.0
firma_suelo   = img[0:6, suelo_rc[0], suelo_rc[1]]  / 10000.0

plt.figure(figsize=(7, 4))
plt.plot(espectrales, firma_cultivo, marker="o", color="green", label="parcela verde")
plt.plot(espectrales, firma_suelo,  marker="s", color="peru",  label="suelo desnudo")
plt.ylabel("reflectancia"); plt.title("Firmas espectrales de dos píxeles reales")
plt.legend(); plt.show()
print("Ve cómo el cultivo salta en el NIR — eso es clorofila, no color.")"""),

md(
"""## 🧪 Check yourself

**Your eyes see 3 bands. Why does a crop-mapping satellite bother measuring
near-infrared and SWIR, which we cannot see?**

<details><summary>Show answer</summary>

Because that is where surfaces differ most. Healthy vegetation reflects a
lot of NIR (from leaf structure) while absorbing red; soil and water behave
differently again. Those invisible bands carry the information that
separates crops from everything else — the visible colors alone are not
enough.

</details>

**A tile is 30 m spatial resolution. What does that number mean, and which
resolution lets us watch a crop grow through the season?**

<details><summary>Show answer</summary>

30 m spatial resolution means each pixel covers a 30 m × 30 m patch of
ground. Watching growth over time is **temporal** resolution — how often the
satellite revisits the same place (every few days for Sentinel-2).

</details>
""",
"""## 🧪 Ponte a prueba

**Tus ojos ven 3 bandas. ¿Por qué un satélite para mapear cultivos se
molesta en medir infrarrojo cercano y SWIR, que no podemos ver?**

<details><summary>Ver respuesta</summary>

Porque ahí es donde más difieren las superficies. La vegetación sana refleja
mucho NIR (por la estructura de la hoja) mientras absorbe el rojo; el suelo
y el agua se comportan distinto otra vez. Esas bandas invisibles cargan la
información que separa los cultivos de todo lo demás — los colores visibles
por sí solos no bastan.

</details>

**Un tile tiene 30 m de resolución espacial. ¿Qué significa ese número, y
qué resolución nos deja ver crecer un cultivo en la temporada?**

<details><summary>Ver respuesta</summary>

30 m de resolución espacial significa que cada píxel cubre un pedazo de
30 m × 30 m de suelo. Ver el crecimiento en el tiempo es la resolución
**temporal** — cada cuánto el satélite revisita el mismo lugar (cada pocos
días para Sentinel-2).

</details>
"""),

],
)
