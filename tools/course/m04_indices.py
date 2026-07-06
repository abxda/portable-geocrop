"""Module 4 — Vegetation indices: reading plant health from light."""

from course.common import md, code, LOAD_TILE_EN, LOAD_TILE_ES

MODULE = dict(
    num=4,
    fname={"en": "04_vegetation_indices.ipynb", "es": "04_indices_de_vegetacion.ipynb"},
    title={"en": "Module 4 — Vegetation indices",
           "es": "Módulo 4 — Índices de vegetación"},
    cards=[
        ("ndvi", {"en": "NDVI, in depth", "es": "NDVI, a fondo"}),
        ("vegetation-indices", {"en": "Vegetation indices (the family)",
                                "es": "Índices de vegetación (la familia)"}),
        ("spectral-indices", {"en": "Spectral indices", "es": "Índices espectrales"}),
        ("near-infrared", {"en": "Near-infrared (NIR)", "es": "Infrarrojo cercano (NIR)"}),
        ("phenology", {"en": "Phenology (the crop calendar)",
                       "es": "Fenología (el calendario del cultivo)"}),
        ("leaf-area-index", {"en": "Leaf Area Index", "es": "Índice de Área Foliar"}),
    ],
    cells=[

md(
"""# 🌱 Module 4 — Vegetation indices

🧭 **Objectives** — turn raw bands into meaning. Compute **NDVI** yourself
from the red and NIR bands, verify it against the pre-computed layer in the
tile, and learn what the other 6 indices in the tile add. Understand why a
whole *family* of indices — not just NDVI — helps a classifier tell crops
apart.

📚 **The idea.** In Module 2 you saw a crop's spectral signature leap up in
the near-infrared while red stays low. An **index** distills that contrast
into one number. The most famous is **NDVI**:

$$ NDVI = \\frac{NIR - Red}{NIR + Red} $$

It runs from −1 (water) through ~0 (bare soil) to ~+0.9 (dense healthy
crop). Because it is a *ratio*, it cancels out differences in brightness
(sun angle, slope) and reads plant vigor directly.

📚 **Why more than NDVI?** NDVI saturates over very dense canopies and says
nothing about water or soil residue. So the tile also carries **EVI** and
**GCVI** (chlorophyll), **MSAVI2** (soil-adjusted), **LSWI** (water),
**NDSVI** and **NDTI** (residue / tillage). Together, 6 bands + 7 indices =
**13 layers** describing each pixel — richer clues for the classifier.
""",
"""# 🌱 Módulo 4 — Índices de vegetación

🧭 **Objetivos** — convertir bandas crudas en significado. Calcular tú mismo
el **NDVI** a partir de las bandas roja y NIR, verificarlo contra la capa ya
calculada del tile, y aprender qué aportan los otros 6 índices del tile.
Entender por qué toda una *familia* de índices — no solo NDVI — ayuda a un
clasificador a distinguir cultivos.

📚 **La idea.** En el Módulo 2 viste la firma espectral de un cultivo saltar
en el infrarrojo cercano mientras el rojo se queda bajo. Un **índice**
destila ese contraste en un solo número. El más famoso es el **NDVI**:

$$ NDVI = \\frac{NIR - Rojo}{NIR + Rojo} $$

Va de −1 (agua), pasa por ~0 (suelo desnudo), hasta ~+0.9 (cultivo denso y
sano). Por ser un *cociente*, cancela diferencias de brillo (ángulo solar,
pendiente) y lee el vigor de la planta directamente.

📚 **¿Por qué más que NDVI?** El NDVI se satura en doseles muy densos y no
dice nada del agua ni del residuo del suelo. Por eso el tile también trae
**EVI** y **GCVI** (clorofila), **MSAVI2** (ajustado al suelo), **LSWI**
(agua), **NDSVI** y **NDTI** (residuo / labranza). Juntos, 6 bandas + 7
índices = **13 capas** que describen cada píxel — más pistas para el
clasificador.

![bandas y NDVI](../../anim/es/04_bands_ndvi.svg)
"""),

code(LOAD_TILE_EN, LOAD_TILE_ES),

md(
"""## Compute NDVI yourself, then check it

The tile stores integers scaled by 10000. Red is band index 2, NIR is band
index 3. Compute NDVI with the formula — one vectorized NumPy line, just
like Module 1 — then compare it to layer 6, which the pipeline pre-computed.
They should match.
""",
"""## Calcula el NDVI tú mismo, luego verifícalo

El tile guarda enteros escalados por 10000. El rojo es la banda índice 2, el
NIR es la banda índice 3. Calcula el NDVI con la fórmula — una línea NumPy
vectorizada, como en el Módulo 1 — y luego compáralo con la capa 6, que el
pipeline ya calculó. Deben coincidir.
"""),

code(
"""import numpy as np, rasterio, matplotlib.pyplot as plt

with rasterio.open(TILE) as src:
    img = src.read().astype(np.float64)

red = img[2]
nir = img[3]
ndvi_mine = (nir - red) / (nir + red + 1e-9)   # +tiny to avoid divide-by-zero
ndvi_tile = img[6] / 10000.0                    # pre-computed layer

diff = np.abs(ndvi_mine - ndvi_tile)
print("Max difference between my NDVI and the tile's:", round(float(diff.max()), 4))
print("They match — you just reproduced a real satellite product.")""",
"""import numpy as np, rasterio, matplotlib.pyplot as plt

with rasterio.open(TILE) as src:
    img = src.read().astype(np.float64)

rojo = img[2]
nir = img[3]
ndvi_mio  = (nir - rojo) / (nir + rojo + 1e-9)  # +minúsculo para no dividir entre 0
ndvi_tile = img[6] / 10000.0                     # capa ya calculada

dif = np.abs(ndvi_mio - ndvi_tile)
print("Diferencia máxima entre mi NDVI y el del tile:", round(float(dif.max()), 4))
print("Coinciden — acabas de reproducir un producto satelital real.")"""),

code(
"""# Look at the NDVI map: green = vigorous crop, brown = soil, dark = water
plt.figure(figsize=(7.5, 6))
im = plt.imshow(ndvi_mine, cmap="RdYlGn", vmin=0, vmax=0.9)
plt.title("NDVI — crop vigor across the Yaqui Valley")
plt.axis("off"); plt.colorbar(im, shrink=0.8, label="NDVI"); plt.show()""",
"""# Mira el mapa de NDVI: verde = cultivo vigoroso, café = suelo, oscuro = agua
plt.figure(figsize=(7.5, 6))
im = plt.imshow(ndvi_mio, cmap="RdYlGn", vmin=0, vmax=0.9)
plt.title("NDVI — vigor del cultivo en el Valle del Yaqui")
plt.axis("off"); plt.colorbar(im, shrink=0.8, label="NDVI"); plt.show()"""),

md(
"""## The whole family, side by side

Each index highlights something different. Seeing them together shows why a
classifier benefits from all 13 layers: a wheat field and a chickpea field
might look similar in NDVI but differ in a water or residue index.
""",
"""## Toda la familia, lado a lado

Cada índice resalta algo distinto. Verlos juntos muestra por qué un
clasificador se beneficia de las 13 capas: una parcela de trigo y una de
garbanzo podrían verse similares en NDVI pero diferir en un índice de agua o
de residuo.
"""),

code(
"""# Layers 6..12 are the 7 indices, in this order:
index_names = ["NDVI", "EVI", "GCVI", "MSAVI2", "LSWI", "NDSVI", "NDTI"]

fig, axes = plt.subplots(2, 4, figsize=(14, 7))
for k, ax in enumerate(axes.ravel()):
    if k < len(index_names):
        layer = img[6 + k] / 10000.0
        im = ax.imshow(layer, cmap="RdYlGn")
        ax.set_title(index_names[k]); ax.axis("off")
    else:
        ax.axis("off")
plt.suptitle("6 spectral bands become 7 indices = 13 clues per pixel")
plt.tight_layout(); plt.show()""",
"""# Las capas 6..12 son los 7 índices, en este orden:
nombres_indice = ["NDVI", "EVI", "GCVI", "MSAVI2", "LSWI", "NDSVI", "NDTI"]

fig, axes = plt.subplots(2, 4, figsize=(14, 7))
for k, ax in enumerate(axes.ravel()):
    if k < len(nombres_indice):
        capa = img[6 + k] / 10000.0
        im = ax.imshow(capa, cmap="RdYlGn")
        ax.set_title(nombres_indice[k]); ax.axis("off")
    else:
        ax.axis("off")
plt.suptitle("6 bandas espectrales se vuelven 7 índices = 13 pistas por píxel")
plt.tight_layout(); plt.show()"""),

md(
"""## Phenology: why one month is a snapshot, a season is a story

NDVI on a single date is a snapshot. Follow the same field *through* the
season — planting, greening, peak, harvest — and its NDVI traces a curve
called its **phenology**. That temporal fingerprint is often what separates
two crops that look identical on any single day. Your tile is one month
(March 2018); the production pipeline in Module 9 stacks *many* months
exactly to capture this.
""",
"""## Fenología: por qué un mes es una foto y una temporada es una historia

El NDVI en una sola fecha es una foto. Sigue la misma parcela *a lo largo*
de la temporada — siembra, verdeo, pico, cosecha — y su NDVI traza una curva
llamada su **fenología**. Esa huella temporal suele ser lo que separa dos
cultivos que se ven idénticos cualquier día suelto. Tu tile es un mes (marzo
2018); el pipeline de producción del Módulo 9 apila *muchos* meses justo
para capturar esto.
"""),

md(
"""## 🧪 Check yourself

**NDVI is `(NIR − Red) / (NIR + Red)`. Why divide, instead of just using
`NIR − Red`?**

<details><summary>Show answer</summary>

Dividing makes it a *ratio*, which cancels overall brightness differences
(sun angle, terrain slope, thin haze). `NIR − Red` alone would change with
lighting even for the same healthy plant; the normalized ratio reads vigor
consistently, from −1 to +1.

</details>

**Why carry EVI, LSWI, NDTI... when NDVI already measures greenness?**

<details><summary>Show answer</summary>

NDVI saturates over dense canopies and ignores water and soil residue. Other
indices capture chlorophyll, canopy water, and tillage/residue. Two crops
can share an NDVI but differ in these — so more indices give the classifier
more ways to tell them apart.

</details>
""",
"""## 🧪 Ponte a prueba

**El NDVI es `(NIR − Rojo) / (NIR + Rojo)`. ¿Por qué dividir, en vez de solo
usar `NIR − Rojo`?**

<details><summary>Ver respuesta</summary>

Dividir lo vuelve un *cociente*, que cancela las diferencias de brillo
general (ángulo solar, pendiente del terreno, bruma ligera). `NIR − Rojo`
solo cambiaría con la iluminación aun para la misma planta sana; el cociente
normalizado lee el vigor de forma consistente, de −1 a +1.

</details>

**¿Para qué cargar EVI, LSWI, NDTI... si el NDVI ya mide el verdor?**

<details><summary>Ver respuesta</summary>

El NDVI se satura en doseles densos e ignora el agua y el residuo del suelo.
Otros índices capturan clorofila, agua del dosel y labranza/residuo. Dos
cultivos pueden compartir un NDVI pero diferir en estos — así que más
índices le dan al clasificador más formas de distinguirlos.

</details>
"""),

],
)
