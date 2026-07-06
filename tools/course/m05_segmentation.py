"""Module 5 — From pixels to parcels: segmentation."""

from course.common import md, code, LOAD_TILE_EN, LOAD_TILE_ES

MODULE = dict(
    num=5,
    fname={"en": "05_pixels_to_parcels.ipynb", "es": "05_de_pixeles_a_parcelas.ipynb"},
    title={"en": "Module 5 — From pixels to parcels: segmentation",
           "es": "Módulo 5 — De píxeles a parcelas: segmentación"},
    cards=[
        ("image-segmentation", {"en": "Image segmentation", "es": "Segmentación de imágenes"}),
        ("segmentation", {"en": "Segmentation (concept)", "es": "Segmentación (concepto)"}),
        ("object-based-classification", {"en": "Object-based classification",
                                         "es": "Clasificación basada en objetos"}),
        ("clustering", {"en": "Clustering / k-means", "es": "Agrupamiento / k-means"}),
        ("pixel-classification", {"en": "Pixel vs object classification",
                                  "es": "Clasificación por píxel vs objeto"}),
    ],
    cells=[

md(
"""# 🧩 Module 5 — From pixels to parcels: segmentation

🧭 **Objectives** — understand why we classify **parcels** instead of
individual pixels, get the intuition behind **k-means** and the **Shepherd**
segmentation algorithm, run it on your tile with `shepherd-wasm`, and see the
field carved into homogeneous objects.

📚 **Why not pixels?** A single field is hundreds of 30 m pixels. Classifying
each pixel alone gives "salt-and-pepper" noise — stray misclassified dots
inside an obviously uniform field. **Object-based** classification first
groups neighboring, spectrally-similar pixels into **segments** (parcels),
then classifies each *parcel* as a whole. Cleaner maps, and it matches how
agriculture actually works: decisions happen per field, not per pixel.

📚 **Shepherd segmentation** (Shepherd et al., 2019) does it in three steps:
1. **k-means** groups pixels into a handful of spectral "families".
2. **Clumping**: connected pixels of the same family become one segment.
3. **Elimination**: segments smaller than a threshold are merged into their
   most similar neighbor, so no sliver is left behind.

We use **`shepherd-wasm`**, a pure NumPy/SciPy port that runs in the browser
(the desktop pipeline uses the numba-accelerated `pyshepseg` — same
algorithm, different engine; you will see this in Module 9).

![segmentation](../../anim/en/05_segmentation.svg)
""",
"""# 🧩 Módulo 5 — De píxeles a parcelas: segmentación

🧭 **Objetivos** — entender por qué clasificamos **parcelas** en vez de
píxeles sueltos, captar la intuición de **k-means** y del algoritmo de
segmentación **Shepherd**, correrlo en tu tile con `shepherd-wasm`, y ver el
campo recortado en objetos homogéneos.

📚 **¿Por qué no píxeles?** Una sola parcela son cientos de píxeles de 30 m.
Clasificar cada píxel por separado da ruido "sal y pimienta" — puntitos mal
clasificados dentro de una parcela obviamente uniforme. La clasificación
**basada en objetos** primero agrupa píxeles vecinos y espectralmente
similares en **segmentos** (parcelas), y luego clasifica cada *parcela*
completa. Mapas más limpios, y coincide con cómo funciona la agricultura de
verdad: las decisiones se toman por parcela, no por píxel.

📚 **La segmentación Shepherd** (Shepherd et al., 2019) lo hace en tres pasos:
1. **k-means** agrupa los píxeles en unas pocas "familias" espectrales.
2. **Agrupamiento (clumping)**: píxeles conexos de la misma familia se
   vuelven un segmento.
3. **Eliminación**: los segmentos menores a un umbral se fusionan con su
   vecino más parecido, para que no quede ninguna astilla suelta.

Usamos **`shepherd-wasm`**, un port en NumPy/SciPy puro que corre en el
navegador (el pipeline de escritorio usa `pyshepseg` acelerado con numba —
el mismo algoritmo, distinto motor; lo verás en el Módulo 9).

![segmentación](../../anim/es/05_segmentation.svg)
"""),

md(
"""## The k-means intuition (tiny demo)

Before segmenting the real tile, feel what k-means does: it sorts points into
`k` groups by similarity. Here we sort a handful of fake pixels (each with an
NDVI and a water index) into 3 spectral families. No geography yet — just
"which pixels resemble which".
""",
"""## La intuición de k-means (demo diminuta)

Antes de segmentar el tile real, siente qué hace k-means: ordena puntos en
`k` grupos por similitud. Aquí ordenamos un puñado de píxeles falsos (cada
uno con un NDVI y un índice de agua) en 3 familias espectrales. Todavía sin
geografía — solo "qué píxeles se parecen a cuáles".
"""),

code(
"""import numpy as np
from sklearn.cluster import KMeans

# 9 fake pixels: [NDVI, water index]. Three natural groups.
pixels = np.array([[0.8, 0.1], [0.82, 0.12], [0.79, 0.09],   # dense crop
                   [0.2, 0.1], [0.18, 0.08], [0.22, 0.11],   # bare soil
                   [-0.3, 0.6], [-0.28, 0.62], [-0.31, 0.58]])# water
labels = KMeans(n_clusters=3, n_init=10, random_state=0).fit_predict(pixels)
print("Pixel -> family:", labels)
print("k-means found the 3 groups without being told what they are.")""",
"""import numpy as np
from sklearn.cluster import KMeans

# 9 píxeles falsos: [NDVI, índice de agua]. Tres grupos naturales.
pixeles = np.array([[0.8, 0.1], [0.82, 0.12], [0.79, 0.09],   # cultivo denso
                    [0.2, 0.1], [0.18, 0.08], [0.22, 0.11],   # suelo desnudo
                    [-0.3, 0.6], [-0.28, 0.62], [-0.31, 0.58]])# agua
familias = KMeans(n_clusters=3, n_init=10, random_state=0).fit_predict(pixeles)
print("Píxel -> familia:", familias)
print("k-means halló los 3 grupos sin que le dijéramos qué son.")"""),

code(LOAD_TILE_EN, LOAD_TILE_ES),

md(
"""## Segment the real tile

`shepherd-wasm` needs `scipy.ndimage` and `sklearn.cluster` imported first
(a Pyodide quirk — its auto-loader cannot see the internal imports).
`numClusters` sets how many spectral families k-means seeds; `minSegmentSize`
is the smallest parcel allowed (smaller ones get merged away). This takes
roughly 30–60 seconds in the browser — watch for the `[*]`.
""",
"""## Segmenta el tile real

`shepherd-wasm` necesita que primero importes `scipy.ndimage` y
`sklearn.cluster` (una peculiaridad de Pyodide — su autocargador no ve los
imports internos). `numClusters` fija cuántas familias espectrales siembra
k-means; `minSegmentSize` es la parcela más pequeña permitida (las menores se
fusionan). Esto tarda unos 30–60 segundos en el navegador — atento al `[*]`.
"""),

code(
"""# Pyodide: import these BEFORE shepherd_wasm so its internals resolve
import scipy.ndimage, sklearn.cluster
import shepherd_wasm, time, rasterio

with rasterio.open(TILE) as src:
    img = src.read()               # (13, 384, 384)

t0 = time.time()
result = shepherd_wasm.doShepherdSegmentation(
    img, numClusters=30, minSegmentSize=50, imgNullVal=0, fixedKMeansInit=True)
seg = result.segimg.astype(np.int32)
n_seg = int(seg.max())
print(f"{n_seg} parcels found in {time.time()-t0:.1f} s")""",
"""# Pyodide: importa estos ANTES de shepherd_wasm para que resuelva sus internos
import scipy.ndimage, sklearn.cluster
import shepherd_wasm, time, rasterio

with rasterio.open(TILE) as src:
    img = src.read()               # (13, 384, 384)

t0 = time.time()
resultado = shepherd_wasm.doShepherdSegmentation(
    img, numClusters=30, minSegmentSize=50, imgNullVal=0, fixedKMeansInit=True)
seg = resultado.segimg.astype(np.int32)
n_seg = int(seg.max())
print(f"{n_seg} parcelas halladas en {time.time()-t0:.1f} s")"""),

code(
"""import matplotlib.pyplot as plt
from scipy import ndimage

rgb = np.clip(np.dstack([img[2], img[1], img[0]]) / 3000.0, 0, 1)
# Draw parcel boundaries in yellow over the true-color image
edges = (ndimage.maximum_filter(seg, size=2) != ndimage.minimum_filter(seg, size=2))
vis = rgb.copy(); vis[edges] = [1, 1, 0]

plt.figure(figsize=(8, 8)); plt.imshow(vis)
plt.title(f"{n_seg} parcels (yellow = boundaries)"); plt.axis("off"); plt.show()
print("Each yellow-bordered patch is one object we will classify.")""",
"""import matplotlib.pyplot as plt
from scipy import ndimage

rgb = np.clip(np.dstack([img[2], img[1], img[0]]) / 3000.0, 0, 1)
# Dibuja las fronteras de parcela en amarillo sobre el color verdadero
bordes = (ndimage.maximum_filter(seg, size=2) != ndimage.minimum_filter(seg, size=2))
vis = rgb.copy(); vis[bordes] = [1, 1, 0]

plt.figure(figsize=(8, 8)); plt.imshow(vis)
plt.title(f"{n_seg} parcelas (amarillo = fronteras)"); plt.axis("off"); plt.show()
print("Cada parche con borde amarillo es un objeto que clasificaremos.")"""),

md(
"""## Experiment

Change `numClusters` (try 15 or 50) and `minSegmentSize` (try 20 or 120) and
re-run the two cells above. Fewer clusters / bigger minimum = larger, coarser
parcels; more clusters / smaller minimum = finer detail but more fragments.
There is no single "right" answer — it depends on the size of the fields you
want to capture.
""",
"""## Experimenta

Cambia `numClusters` (prueba 15 o 50) y `minSegmentSize` (prueba 20 o 120) y
vuelve a correr las dos celdas de arriba. Menos clusters / mínimo más grande
= parcelas más grandes y gruesas; más clusters / mínimo más chico = más
detalle pero más fragmentos. No hay una única respuesta "correcta" — depende
del tamaño de las parcelas que quieras capturar.
"""),

md(
"""## 🧪 Check yourself

**What is "salt-and-pepper" noise, and how does segmentation cure it?**

<details><summary>Show answer</summary>

It is scattered, individually misclassified pixels inside a field that is
really uniform. Segmentation groups the field's pixels into one object and
classifies the object as a whole, so a few odd pixels can't speckle the map.

</details>

**In Shepherd, what does `minSegmentSize` control, and what happens to
parcels below it?**

<details><summary>Show answer</summary>

It is the smallest allowed segment size. Segments smaller than it are merged
into their spectrally most similar neighbor during the elimination step, so
no tiny slivers survive.

</details>
""",
"""## 🧪 Ponte a prueba

**¿Qué es el ruido "sal y pimienta", y cómo lo cura la segmentación?**

<details><summary>Ver respuesta</summary>

Son píxeles dispersos, mal clasificados de forma individual, dentro de una
parcela que en realidad es uniforme. La segmentación agrupa los píxeles de la
parcela en un objeto y clasifica el objeto completo, así unos pocos píxeles
raros no pueden motear el mapa.

</details>

**En Shepherd, ¿qué controla `minSegmentSize`, y qué pasa con las parcelas
por debajo de ese tamaño?**

<details><summary>Ver respuesta</summary>

Es el tamaño mínimo de segmento permitido. Los segmentos menores se fusionan
con su vecino espectralmente más parecido durante el paso de eliminación, así
que no sobreviven astillas diminutas.

</details>
"""),

],
)
