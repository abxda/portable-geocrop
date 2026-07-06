"""Module 6 — Parcels become a table + the ground truth."""

from course.common import md, code, LOAD_TILE_EN, LOAD_TILE_ES

MODULE = dict(
    num=6,
    fname={"en": "06_features_and_labels.ipynb", "es": "06_variables_y_etiquetas.ipynb"},
    title={"en": "Module 6 — Parcels become a table + the ground truth",
           "es": "Módulo 6 — Las parcelas se vuelven tabla + la verdad de campo"},
    cards=[
        ("zonal-statistics", {"en": "Zonal statistics", "es": "Estadística zonal"}),
        ("ground-truth", {"en": "Ground truth", "es": "Verdad de campo"}),
        ("training-samples", {"en": "Training samples", "es": "Muestras de entrenamiento"}),
        ("sample-balancing", {"en": "Sample balancing", "es": "Balanceo de muestras"}),
    ],
    cells=[

md(
"""# 📊 Module 6 — Parcels become a table + the ground truth

🧭 **Objectives** — turn each parcel from Module 5 into a **row of numbers**
(features) using **zonal statistics**, then attach **ground-truth** labels
from real field points with a **purity filter**. At the end you have exactly
what a classifier eats: a table of parcels × features, some of them labelled.

📚 **Features = a parcel as numbers.** A model cannot look at a picture; it
needs numbers. For each parcel we summarize the 13 layers under it into
**zonal statistics** — here the **mean** and **standard deviation** of every
band. So each parcel becomes a row of 26 numbers. (The production pipeline
computes far more — min, max, sums, across many months — hundreds of columns;
Module 9.)

📚 **Ground truth = the answer key.** To train a model we need parcels whose
crop we *actually know*. Those come from **field points**: 1,645 GPS
locations in the Yaqui Valley where someone recorded the real crop. We drop
each point onto its parcel. A **purity filter** keeps only parcels where all
the points inside agree — mixed parcels are ambiguous and would teach the
model wrong lessons.

![features](../../anim/en/06_features.svg)

![labels and purity](../../anim/en/07_labels_purity.svg)
""",
"""# 📊 Módulo 6 — Las parcelas se vuelven tabla + la verdad de campo

🧭 **Objetivos** — convertir cada parcela del Módulo 5 en una **fila de
números** (variables) usando **estadística zonal**, y luego pegarle
etiquetas de **verdad de campo** desde puntos reales con un **filtro de
pureza**. Al final tendrás justo lo que come un clasificador: una tabla de
parcelas × variables, algunas etiquetadas.

📚 **Variables = una parcela como números.** Un modelo no puede mirar una
imagen; necesita números. Para cada parcela resumimos las 13 capas debajo de
ella en **estadística zonal** — aquí la **media** y la **desviación
estándar** de cada banda. Así cada parcela se vuelve una fila de 26 números.
(El pipeline de producción calcula muchas más — mín, máx, sumas, en varios
meses — cientos de columnas; Módulo 9.)

📚 **Verdad de campo = la hoja de respuestas.** Para entrenar un modelo
necesitamos parcelas cuyo cultivo *sí conocemos*. Vienen de **puntos de
campo**: 1,645 ubicaciones GPS del Valle del Yaqui donde alguien registró el
cultivo real. Dejamos caer cada punto en su parcela. Un **filtro de pureza**
conserva solo las parcelas donde todos los puntos coinciden — las parcelas
mixtas son ambiguas y le enseñarían lecciones erróneas al modelo.

![variables](../../anim/es/06_features.svg)

![etiquetas y pureza](../../anim/es/07_labels_purity.svg)
"""),

md(
"""## Rebuild the segmentation

Each course module runs on a fresh kernel, so we re-load the tile and
re-segment it (same parameters as Module 5) before extracting features.
""",
"""## Reconstruye la segmentación

Cada módulo del curso corre en un kernel limpio, así que volvemos a cargar el
tile y a segmentarlo (mismos parámetros que el Módulo 5) antes de extraer las
variables.
"""),

code(LOAD_TILE_EN, LOAD_TILE_ES),

code(
"""import numpy as np, rasterio
import scipy.ndimage, sklearn.cluster
import shepherd_wasm

with rasterio.open(TILE) as src:
    img = src.read()
    band_names = list(src.descriptions)

result = shepherd_wasm.doShepherdSegmentation(
    img, numClusters=30, minSegmentSize=50, imgNullVal=0, fixedKMeansInit=True)
seg = result.segimg.astype(np.int32)
n_seg = int(seg.max())
print(f"{n_seg} parcels to describe")""",
"""import numpy as np, rasterio
import scipy.ndimage, sklearn.cluster
import shepherd_wasm

with rasterio.open(TILE) as src:
    img = src.read()
    nombres_banda = list(src.descriptions)

resultado = shepherd_wasm.doShepherdSegmentation(
    img, numClusters=30, minSegmentSize=50, imgNullVal=0, fixedKMeansInit=True)
seg = resultado.segimg.astype(np.int32)
n_seg = int(seg.max())
print(f"{n_seg} parcelas por describir")"""),

md(
"""## Zonal statistics with np.bincount

For every band we want the mean and standard deviation of the pixels inside
each parcel. `np.bincount` does this fast: it sums values grouped by segment
id. From the sum and the sum-of-squares we get the mean and the standard
deviation for all parcels at once — vectorized, no Python loop over parcels.
""",
"""## Estadística zonal con np.bincount

Para cada banda queremos la media y la desviación estándar de los píxeles
dentro de cada parcela. `np.bincount` lo hace rápido: suma valores agrupados
por id de segmento. De la suma y la suma de cuadrados obtenemos la media y la
desviación de todas las parcelas a la vez — vectorizado, sin ciclo de Python
por parcela.
"""),

code(
"""flat_seg = seg.ravel()
counts = np.bincount(flat_seg, minlength=n_seg + 1).astype(float)
counts[counts == 0] = 1     # avoid divide-by-zero for unused ids

features = np.zeros((n_seg + 1, len(band_names) * 2), dtype=np.float32)
for b in range(len(band_names)):
    vals = img[b].ravel().astype(np.float64)
    s1 = np.bincount(flat_seg, weights=vals,       minlength=n_seg + 1)
    s2 = np.bincount(flat_seg, weights=vals * vals, minlength=n_seg + 1)
    mean = s1 / counts
    var  = np.maximum(s2 / counts - mean**2, 0)
    features[:, 2*b], features[:, 2*b+1] = mean, np.sqrt(var)

feature_names = [f"{n}_{s}" for n in band_names for s in ("mean", "std")]
print(f"Feature table: {features.shape[0]-1} parcels x {features.shape[1]} features")
print("First few feature names:", feature_names[:4])""",
"""seg_plano = seg.ravel()
conteos = np.bincount(seg_plano, minlength=n_seg + 1).astype(float)
conteos[conteos == 0] = 1     # evita dividir entre 0 para ids sin uso

variables = np.zeros((n_seg + 1, len(nombres_banda) * 2), dtype=np.float32)
for b in range(len(nombres_banda)):
    vals = img[b].ravel().astype(np.float64)
    s1 = np.bincount(seg_plano, weights=vals,       minlength=n_seg + 1)
    s2 = np.bincount(seg_plano, weights=vals * vals, minlength=n_seg + 1)
    media = s1 / conteos
    var   = np.maximum(s2 / conteos - media**2, 0)
    variables[:, 2*b], variables[:, 2*b+1] = media, np.sqrt(var)

nombres_variables = [f"{n}_{s}" for n in nombres_banda for s in ("media", "desv")]
print(f"Tabla de variables: {variables.shape[0]-1} parcelas x {variables.shape[1]} variables")
print("Primeros nombres de variable:", nombres_variables[:4])"""),

md(
"""## Attach the ground truth (with the purity filter)

The label raster carries the real crop id at the field-point locations. For
each parcel that contains labelled pixels, we keep it for training **only if
every labelled pixel inside agrees** on the same class — that is the purity
filter. Then we count how many pure parcels we have per crop.
""",
"""## Pega la verdad de campo (con el filtro de pureza)

El raster de etiquetas trae el id de cultivo real en las ubicaciones de los
puntos de campo. Para cada parcela que contiene píxeles etiquetados, la
conservamos para entrenar **solo si todos los píxeles etiquetados de adentro
coinciden** en la misma clase — ese es el filtro de pureza. Luego contamos
cuántas parcelas puras tenemos por cultivo.
"""),

code(
"""import json

async def get_file(name):
    import os, sys
    for cand in (f"files/{name}", name, f"../files/{name}", f"../../files/{name}"):
        if os.path.exists(cand):
            return cand
    dest = f"/tmp/{name}"
    if not os.path.exists(dest):
        url = f"__RAW__/{name}"
        if sys.platform == "emscripten":
            from pyodide.http import pyfetch
            resp = await pyfetch(url); open(dest, "wb").write(await resp.bytes())
        else:
            import urllib.request; urllib.request.urlretrieve(url, dest)
    return dest

LABELS = await get_file("crop_labels_384.tif")
NAMES  = await get_file("class_names.json")

with rasterio.open(LABELS) as src:
    lab = src.read(1)
class_names = {int(k): v for k, v in json.load(open(NAMES)).items()}

parcel_label = np.zeros(n_seg + 1, dtype=int)
for sid in np.unique(seg[lab > 0]):
    values = lab[(seg == sid) & (lab > 0)]
    uniq = np.unique(values)
    if len(uniq) == 1:                 # pure parcel -> usable for training
        parcel_label[sid] = uniq[0]

train_ids = np.flatnonzero(parcel_label)
print(f"Pure labelled parcels: {len(train_ids)} of {n_seg}")
for cid, cname in class_names.items():
    print(f"  {cname:12s}: {(parcel_label[train_ids] == cid).sum():3d} parcels")""",
"""import json

async def trae_archivo(name):
    import os, sys
    for cand in (f"files/{name}", name, f"../files/{name}", f"../../files/{name}"):
        if os.path.exists(cand):
            return cand
    dest = f"/tmp/{name}"
    if not os.path.exists(dest):
        url = f"__RAW__/{name}"
        if sys.platform == "emscripten":
            from pyodide.http import pyfetch
            resp = await pyfetch(url); open(dest, "wb").write(await resp.bytes())
        else:
            import urllib.request; urllib.request.urlretrieve(url, dest)
    return dest

LABELS  = await trae_archivo("crop_labels_384.tif")
NOMBRES = await trae_archivo("class_names.json")

with rasterio.open(LABELS) as src:
    lab = src.read(1)
nombres_clase = {int(k): v for k, v in json.load(open(NOMBRES)).items()}

etiqueta_parcela = np.zeros(n_seg + 1, dtype=int)
for sid in np.unique(seg[lab > 0]):
    valores = lab[(seg == sid) & (lab > 0)]
    unicos = np.unique(valores)
    if len(unicos) == 1:               # parcela pura -> sirve para entrenar
        etiqueta_parcela[sid] = unicos[0]

ids_entrena = np.flatnonzero(etiqueta_parcela)
print(f"Parcelas etiquetadas puras: {len(ids_entrena)} de {n_seg}")
for cid, cname in nombres_clase.items():
    print(f"  {cname:12s}: {(etiqueta_parcela[ids_entrena] == cid).sum():3d} parcelas")"""),

md(
"""## 🧪 Check yourself

**Why summarize each parcel to a mean and standard deviation instead of
feeding the model all its pixels?**

<details><summary>Show answer</summary>

The model classifies *parcels*, and it needs a fixed-length row of numbers
per parcel — but parcels have different pixel counts. Zonal statistics
(mean, std, ...) compress any parcel into the same set of features, and they
capture what matters: the parcel's typical value and how uniform it is.

</details>

**What does the purity filter throw away, and why is that a good thing for
training?**

<details><summary>Show answer</summary>

It discards parcels whose field points disagree on the crop (mixed or
mislabelled parcels). Training only on parcels with a single, agreed class
prevents teaching the model contradictory examples, which would blur every
class it learns.

</details>
""",
"""## 🧪 Ponte a prueba

**¿Por qué resumir cada parcela a una media y una desviación en vez de darle
al modelo todos sus píxeles?**

<details><summary>Ver respuesta</summary>

El modelo clasifica *parcelas*, y necesita una fila de números de largo fijo
por parcela — pero las parcelas tienen distinto número de píxeles. La
estadística zonal (media, desv, ...) comprime cualquier parcela en el mismo
conjunto de variables, y captura lo que importa: el valor típico de la
parcela y qué tan uniforme es.

</details>

**¿Qué desecha el filtro de pureza, y por qué eso es bueno para el
entrenamiento?**

<details><summary>Ver respuesta</summary>

Descarta parcelas cuyos puntos de campo no coinciden en el cultivo (parcelas
mixtas o mal etiquetadas). Entrenar solo con parcelas de una única clase
acordada evita enseñarle al modelo ejemplos contradictorios, que
difuminarían cada clase que aprende.

</details>
"""),

],
)
