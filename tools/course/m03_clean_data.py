"""Module 3 — Clean data: from clouds to the geomedian."""

from course.common import md, code, LOAD_TILE_EN, LOAD_TILE_ES

MODULE = dict(
    num=3,
    fname={"en": "03_clean_data_geomedian.ipynb", "es": "03_datos_limpios_geomediana.ipynb"},
    title={"en": "Module 3 — Clean data: from clouds to the geomedian",
           "es": "Módulo 3 — Datos limpios: de las nubes a la geomediana"},
    cards=[
        ("cloud-masking", {"en": "Cloud masking", "es": "Enmascarado de nubes"}),
        ("quality-flags", {"en": "Quality flags", "es": "Banderas de calidad"}),
        ("analysis-ready-data", {"en": "Analysis Ready Data (ARD)",
                                 "es": "Datos Listos para Análisis (ARD)"}),
        ("temporal-compositing", {"en": "Temporal compositing",
                                  "es": "Composición temporal"}),
        ("harmonized-landsat-sentinel", {"en": "Harmonized Landsat-Sentinel (HLS)",
                                         "es": "Landsat-Sentinel Armonizado (HLS)"}),
        ("surface-reflectance", {"en": "Surface reflectance",
                                 "es": "Reflectancia de superficie"}),
    ],
    cells=[

md(
"""# ☁️ Module 3 — Clean data: from clouds to the geomedian

🧭 **Objectives** — understand why raw satellite images are messy (clouds,
shadows, gaps), what a **cloud mask** and **quality flags** do, and how a
**geomedian** turns a whole month of imperfect images into one clean,
gap-free image — the tile you have been using.

📚 **The problem.** A single satellite pass is often ruined by clouds and
their shadows. One image of your field might be 40% cloud. The fix is
**temporal compositing**: take *many* images over a period and combine them
per pixel, keeping only good observations.

📚 **The geomedian.** A plain per-band median would pick, say, the median red
from one date and the median NIR from another — breaking the pixel's true
color. The **geomedian** (geometric median) instead finds the single
multi-band value closest to all cloud-free observations *at once*, so band
ratios like NDVI stay physically consistent. Clouds are outliers, so they
get voted out. The result is **Analysis Ready Data**: surface reflectance,
cloud-free, ready to use.

![the geomedian](../../anim/en/03_geomedian.svg)
""",
"""# ☁️ Módulo 3 — Datos limpios: de las nubes a la geomediana

🧭 **Objetivos** — entender por qué las imágenes satelitales crudas son un
desorden (nubes, sombras, huecos), qué hacen una **máscara de nubes** y las
**banderas de calidad**, y cómo una **geomediana** convierte todo un mes de
imágenes imperfectas en una sola imagen limpia y sin huecos — el tile que
has estado usando.

📚 **El problema.** Un solo paso del satélite suele arruinarse por nubes y
sus sombras. Una imagen de tu parcela podría ser 40% nube. La solución es la
**composición temporal**: tomar *muchas* imágenes en un periodo y
combinarlas por píxel, quedándose solo con las observaciones buenas.

📚 **La geomediana.** Una mediana simple por banda tomaría, digamos, el rojo
mediano de una fecha y el NIR mediano de otra — rompiendo el color real del
píxel. La **geomediana** (mediana geométrica) en cambio encuentra el único
valor multibanda más cercano a todas las observaciones sin nube *a la vez*,
así los cocientes como el NDVI se mantienen físicamente consistentes. Las
nubes son atípicas, así que quedan descartadas. El resultado son **Datos
Listos para Análisis**: reflectancia de superficie, sin nubes, lista.

![la geomediana](../../anim/es/03_geomedian.svg)
"""),

md(
"""## Where the data comes from (and the optional GEE)

The tile is built from **NASA HLS** (Harmonized Landsat + Sentinel-2),
streamed from open **STAC/COG** catalogs — no account needed. The production
pipeline (`geocrop_analysis_mx`) can *optionally* use Google Earth Engine
too, but it is not required: the same geomedian can be built from open
catalogs. You will meet this choice again in Module 9.
""",
"""## De dónde salen los datos (y el GEE opcional)

El tile se construye con **NASA HLS** (Landsat + Sentinel-2 armonizados),
transmitido desde catálogos abiertos **STAC/COG** — sin cuenta. El pipeline
de producción (`geocrop_analysis_mx`) puede *opcionalmente* usar también
Google Earth Engine, pero no es obligatorio: la misma geomediana se puede
construir desde catálogos abiertos. Verás esta elección de nuevo en el
Módulo 9.
"""),

md(
"""## Simulate the problem, then the fix

You do not have the raw cloudy stack in the browser, but you can *feel* why
the geomedian works with a tiny experiment: take one clean pixel value,
scatter fake "cloudy" observations on top (clouds are bright — high values),
and watch how the **median** ignores them while the **mean** is fooled.
""",
"""## Simula el problema, luego la solución

No tienes la pila cruda con nubes en el navegador, pero puedes *sentir* por
qué funciona la geomediana con un experimento diminuto: toma un valor limpio
de píxel, salpica encima observaciones "nubladas" falsas (las nubes son
brillantes — valores altos), y observa cómo la **mediana** las ignora
mientras la **media** se deja engañar.
"""),

code(
"""import numpy as np

# 10 observations of one pixel's red reflectance over a month.
# 7 are clear (~0.06); 3 are cloud-contaminated (bright, ~0.8).
observations = np.array([0.06, 0.05, 0.80, 0.07, 0.06, 0.78, 0.05, 0.82, 0.06, 0.07])

print("Mean   (fooled by clouds):", round(observations.mean(), 3))
print("Median (votes clouds out):", round(np.median(observations), 3))
print("True clear value is about 0.06 — the median recovers it.")""",
"""import numpy as np

# 10 observaciones de la reflectancia roja de un píxel durante un mes.
# 7 están despejadas (~0.06); 3 tienen nube (brillantes, ~0.8).
observaciones = np.array([0.06, 0.05, 0.80, 0.07, 0.06, 0.78, 0.05, 0.82, 0.06, 0.07])

print("Media    (engañada por nubes):", round(observaciones.mean(), 3))
print("Mediana  (descarta las nubes):", round(np.median(observaciones), 3))
print("El valor limpio real es ~0.06 — la mediana lo recupera.")"""),

md(
"""## The geomedian is already in your tile

Every pixel of your tile is the *result* of this process applied across a
month of HLS images, for all bands together. That is why it looks seamless —
no cloud holes, consistent color. Load it and confirm it is complete
(no missing pixels in the valid area).
""",
"""## La geomediana ya está en tu tile

Cada píxel de tu tile es el *resultado* de este proceso aplicado a lo largo
de un mes de imágenes HLS, para todas las bandas juntas. Por eso se ve sin
costuras — sin huecos de nube, color consistente. Cárgalo y confirma que
está completo (sin píxeles faltantes en el área válida).
"""),

code(LOAD_TILE_EN, LOAD_TILE_ES),

code(
"""import rasterio, matplotlib.pyplot as plt

with rasterio.open(TILE) as src:
    img = src.read()

# A geomedian has no cloud gaps: count pixels that are exactly 0 (nodata)
valid = np.count_nonzero(img[3] != 0)         # NIR band
total = img[3].size
print(f"Valid pixels: {valid:,} of {total:,} ({100*valid/total:.1f}%)")

rgb = np.clip(np.dstack([img[2], img[1], img[0]]) / 3000.0, 0, 1)
plt.figure(figsize=(7, 7)); plt.imshow(rgb)
plt.title("Clean geomedian — no clouds, no gaps"); plt.axis("off"); plt.show()""",
"""import rasterio, matplotlib.pyplot as plt

with rasterio.open(TILE) as src:
    img = src.read()

# Una geomediana no tiene huecos de nube: cuenta píxeles exactamente 0 (nodata)
validos = np.count_nonzero(img[3] != 0)       # banda NIR
total = img[3].size
print(f"Píxeles válidos: {validos:,} de {total:,} ({100*validos/total:.1f}%)")

rgb = np.clip(np.dstack([img[2], img[1], img[0]]) / 3000.0, 0, 1)
plt.figure(figsize=(7, 7)); plt.imshow(rgb)
plt.title("Geomediana limpia — sin nubes, sin huecos"); plt.axis("off"); plt.show()"""),

md(
"""## 🧪 Check yourself

**Why not just average all the images of a month to remove clouds?**

<details><summary>Show answer</summary>

Clouds are bright outliers; the **mean** gets dragged upward by them. The
**median** (and the multi-band geomedian) ignores outliers, so cloudy
observations are effectively voted out. Averaging would leave a hazy,
cloud-tinted image.

</details>

**What does the "geo" in geomedian buy you over a per-band median?**

<details><summary>Show answer</summary>

It keeps the bands *consistent per pixel*: instead of mixing the red from
one date with the NIR from another, it picks one multi-band observation
closest to all clear ones at once. That keeps band ratios like NDVI
physically meaningful.

</details>
""",
"""## 🧪 Ponte a prueba

**¿Por qué no simplemente promediar todas las imágenes de un mes para quitar
las nubes?**

<details><summary>Ver respuesta</summary>

Las nubes son atípicos brillantes; la **media** se jala hacia arriba por
ellas. La **mediana** (y la geomediana multibanda) ignora los atípicos, así
que las observaciones con nube quedan descartadas. Promediar dejaría una
imagen brumosa y teñida de nube.

</details>

**¿Qué te da el "geo" de geomediana frente a una mediana por banda?**

<details><summary>Ver respuesta</summary>

Mantiene las bandas *consistentes por píxel*: en vez de mezclar el rojo de
una fecha con el NIR de otra, elige una observación multibanda cercana a
todas las despejadas a la vez. Eso mantiene los cocientes como el NDVI
físicamente con sentido.

</details>
"""),

],
)
