#!/usr/bin/env python3
"""Bilingual workshop notebook generator (EN default + ES twin).

One source of truth: every cell is defined once with EN/ES text, and the
script emits workshop/Crop_Classification_Workshop.ipynb (English) and
workshop/Taller_Clasificacion_Cultivos.ipynb (Spanish). Both run unchanged
in JupyterLite/Pyodide (the published site) and in regular Jupyter.

Regenerate with:  python tools/gen_notebooks.py
"""

import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

RAW = "https://raw.githubusercontent.com/abxda/portable-geocrop/main/files"


def md(en, es):
    return ("markdown", {"en": en, "es": es})


def code(en, es=None):
    return ("code", {"en": en, "es": es if es is not None else en})


def anim(lang, name):
    return f"anim/{lang}/{name}.svg"


CELLS = [

md(
"""# 🌾 Crop Classification Workshop — in your browser

Classify real crop fields of the **Yaqui Valley (Sonora, Mexico)** using
open satellite data — every step runs **inside your browser** (WebAssembly),
no installation, no accounts.

> **¿Prefieres español?** Abre
> [`Taller_Clasificacion_Cultivos.ipynb`](Taller_Clasificacion_Cultivos.ipynb) —
> es el mismo taller, en español.

This workshop is the didactic companion of
[**geocrop_analysis_mx**](https://github.com/abxda/geocrop_analysis_mx),
a production pipeline for crop classification with open STAC/COG data.
What you run here on one small tile, that pipeline runs on whole regions.

**Author:** Dr. Abel Coronado ([@abxda](https://github.com/abxda)) ·
built with Claude Fable (Anthropic)

![where does this run](anim/en/01_where_it_runs.svg)
""",
"""# 🌾 Taller de Clasificación de Cultivos — en tu navegador

Clasifica parcelas agrícolas reales del **Valle del Yaqui (Sonora, México)**
con datos satelitales abiertos — cada paso corre **dentro de tu navegador**
(WebAssembly), sin instalar nada y sin cuentas.

> **Prefer English?** Open
> [`Crop_Classification_Workshop.ipynb`](Crop_Classification_Workshop.ipynb) —
> it is the same workshop, in English.

Este taller es el acompañante didáctico de
[**geocrop_analysis_mx**](https://github.com/abxda/geocrop_analysis_mx),
un pipeline de producción para clasificación de cultivos con datos abiertos
STAC/COG. Lo que aquí corres sobre un tile pequeño, ese pipeline lo corre
sobre regiones completas.

**Autor:** Dr. Abel Coronado ([@abxda](https://github.com/abxda)) ·
construido con Claude Fable (Anthropic)

![dónde corre esto](anim/es/01_where_it_runs.svg)
"""),

code(
"""# Step 0 — Where is this Python running?
import sys, platform
print(f"Python   : {sys.version.split()[0]}")
print(f"Platform : {sys.platform!r} / {platform.machine()!r}")
if sys.platform == "emscripten":
    print("Running in WebAssembly, INSIDE your browser. No server. 🚀")
else:
    print("Running locally (regular Python) — everything works the same.")""",
"""# Paso 0 — ¿Dónde está corriendo este Python?
import sys, platform
print(f"Python     : {sys.version.split()[0]}")
print(f"Plataforma : {sys.platform!r} / {platform.machine()!r}")
if sys.platform == "emscripten":
    print("Corriendo en WebAssembly, DENTRO de tu navegador. Sin servidor. 🚀")
else:
    print("Corriendo en modo local (Python normal) — todo funciona igual.")"""),

md(
"""## Where does the data come from?

The tile you are about to load is a **real product**: the **March-2018
geomedian** of the Yaqui Valley, built by `geocrop_analysis_mx` from
**NASA HLS** imagery (Landsat + Sentinel-2 harmonized), streamed from open
**STAC/COG** catalogs. No Google Earth Engine was needed — though the
pipeline can optionally use GEE if you have an account.

![data sources](anim/en/02_data_sources.svg)

![the geomedian](anim/en/03_geomedian.svg)
""",
"""## ¿De dónde salen los datos?

El tile que vas a cargar es un **producto real**: la **geomediana de
marzo-2018** del Valle del Yaqui, construida por `geocrop_analysis_mx` con
imágenes **HLS de la NASA** (Landsat + Sentinel-2 armonizados), transmitidas
desde catálogos abiertos **STAC/COG**. No se necesitó Google Earth Engine —
aunque el pipeline puede usar GEE opcionalmente si tienes cuenta.

![fuentes de datos](anim/es/02_data_sources.svg)

![la geomediana](anim/es/03_geomedian.svg)
"""),

code(
"""# Step 1 — Tools + workshop data (a few MB; cached after the first run)
%pip install -q shepherd-wasm
import os, sys

async def get_file(name):
    for cand in (f"files/{name}", name, f"../files/{name}"):
        if os.path.exists(cand):
            return cand
    dest = f"/tmp/{name}"
    if not os.path.exists(dest):
        url = f"{RAW}/{name}"
        if sys.platform == "emscripten":
            from pyodide.http import pyfetch
            resp = await pyfetch(url)
            open(dest, "wb").write(await resp.bytes())
        else:
            import urllib.request
            urllib.request.urlretrieve(url, dest)
    return dest

RAW = "__RAW__"
TILE   = await get_file("crop_tile_384.tif")
LABELS = await get_file("crop_labels_384.tif")
NAMES  = await get_file("class_names.json")
print("Ready:", TILE, LABELS, NAMES)""",
"""# Paso 1 — Herramientas + datos del taller (pocos MB; queda en caché)
%pip install -q shepherd-wasm
import os, sys

async def trae_archivo(name):
    for cand in (f"files/{name}", name, f"../files/{name}"):
        if os.path.exists(cand):
            return cand
    dest = f"/tmp/{name}"
    if not os.path.exists(dest):
        url = f"{RAW}/{name}"
        if sys.platform == "emscripten":
            from pyodide.http import pyfetch
            resp = await pyfetch(url)
            open(dest, "wb").write(await resp.bytes())
        else:
            import urllib.request
            urllib.request.urlretrieve(url, dest)
    return dest

RAW = "__RAW__"
TILE     = await trae_archivo("crop_tile_384.tif")
LABELS   = await trae_archivo("crop_labels_384.tif")
NOMBRES  = await trae_archivo("class_names.json")
print("Listo:", TILE, LABELS, NOMBRES)"""),

md(
"""## Look at the field: true color and NDVI

13 layers per pixel: 6 spectral bands plus 7 vegetation/soil indices,
already computed in the geomedian.

![bands and NDVI](anim/en/04_bands_ndvi.svg)
""",
"""## Mira el campo: color verdadero y NDVI

13 capas por píxel: 6 bandas espectrales más 7 índices de vegetación/suelo,
ya calculados en la geomediana.

![bandas y NDVI](anim/es/04_bands_ndvi.svg)
"""),

code(
"""# Step 2 — RGB and NDVI
import json
import numpy as np
import rasterio
import matplotlib.pyplot as plt

with rasterio.open(TILE) as src:
    img = src.read()                      # (13, 384, 384) int16
    band_names = list(src.descriptions)
print("Bands:", band_names)

rgb  = np.clip(np.dstack([img[2], img[1], img[0]]) / 3000.0, 0, 1)
ndvi = img[6] / 10000.0

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.6))
ax1.imshow(rgb); ax1.set_title("True color (geomedian, March 2018)"); ax1.axis("off")
im = ax2.imshow(ndvi, cmap="RdYlGn", vmin=0, vmax=0.9)
ax2.set_title("NDVI — crop vigor"); ax2.axis("off")
plt.colorbar(im, ax=ax2, shrink=0.8); plt.tight_layout(); plt.show()""",
"""# Paso 2 — RGB y NDVI
import json
import numpy as np
import rasterio
import matplotlib.pyplot as plt

with rasterio.open(TILE) as src:
    img = src.read()                      # (13, 384, 384) int16
    nombres_banda = list(src.descriptions)
print("Bandas:", nombres_banda)

rgb  = np.clip(np.dstack([img[2], img[1], img[0]]) / 3000.0, 0, 1)
ndvi = img[6] / 10000.0

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.6))
ax1.imshow(rgb); ax1.set_title("Color verdadero (geomediana, marzo 2018)"); ax1.axis("off")
im = ax2.imshow(ndvi, cmap="RdYlGn", vmin=0, vmax=0.9)
ax2.set_title("NDVI — vigor del cultivo"); ax2.axis("off")
plt.colorbar(im, ax=ax2, shrink=0.8); plt.tight_layout(); plt.show()"""),

md(
"""## From pixels to parcels: Shepherd segmentation

![segmentation](anim/en/05_segmentation.svg)
""",
"""## De píxeles a parcelas: segmentación Shepherd

![segmentación](anim/es/05_segmentation.svg)
"""),

code(
"""# Step 3 — Segment the tile into homogeneous parcels (~30-60 s)
import shepherd_wasm, time

t0 = time.time()
result = shepherd_wasm.doShepherdSegmentation(
    img, numClusters=30, minSegmentSize=50, imgNullVal=0,
    fixedKMeansInit=True)
seg = result.segimg.astype(np.int32)
n_seg = int(seg.max())
print(f"{n_seg} parcels in {time.time()-t0:.1f} s")

from scipy import ndimage
edges = (ndimage.maximum_filter(seg, size=2) != ndimage.minimum_filter(seg, size=2))
vis = rgb.copy(); vis[edges] = [1, 1, 0]
plt.figure(figsize=(7.5, 7.5)); plt.imshow(vis)
plt.title(f"{n_seg} parcels (yellow = boundaries)"); plt.axis("off"); plt.show()""",
"""# Paso 3 — Segmentar el tile en parcelas homogéneas (~30-60 s)
import shepherd_wasm, time

t0 = time.time()
resultado = shepherd_wasm.doShepherdSegmentation(
    img, numClusters=30, minSegmentSize=50, imgNullVal=0,
    fixedKMeansInit=True)
seg = resultado.segimg.astype(np.int32)
n_seg = int(seg.max())
print(f"{n_seg} parcelas en {time.time()-t0:.1f} s")

from scipy import ndimage
bordes = (ndimage.maximum_filter(seg, size=2) != ndimage.minimum_filter(seg, size=2))
vis = rgb.copy(); vis[bordes] = [1, 1, 0]
plt.figure(figsize=(7.5, 7.5)); plt.imshow(vis)
plt.title(f"{n_seg} parcelas (amarillo = fronteras)"); plt.axis("off"); plt.show()"""),

md(
"""## Every parcel becomes a row of numbers

![features](anim/en/06_features.svg)
""",
"""## Cada parcela se convierte en una fila de números

![variables](anim/es/06_features.svg)
"""),

code(
"""# Step 4 — Per-parcel features: mean and st.dev of the 13 bands
flat_seg = seg.ravel()
counts = np.bincount(flat_seg, minlength=n_seg + 1).astype(float)
counts[counts == 0] = 1

features = np.zeros((n_seg + 1, len(band_names) * 2), dtype=np.float32)
for b in range(len(band_names)):
    vals = img[b].ravel().astype(np.float64)
    s1 = np.bincount(flat_seg, weights=vals, minlength=n_seg + 1)
    s2 = np.bincount(flat_seg, weights=vals * vals, minlength=n_seg + 1)
    mean = s1 / counts
    var = np.maximum(s2 / counts - mean**2, 0)
    features[:, 2*b], features[:, 2*b+1] = mean, np.sqrt(var)

feature_names = [f"{n}_{s}" for n in band_names for s in ("mean", "std")]
print(f"Feature table: {features.shape[0]-1} parcels x {features.shape[1]} features")""",
"""# Paso 4 — Variables por parcela: media y desviación de las 13 bandas
seg_plano = seg.ravel()
conteos = np.bincount(seg_plano, minlength=n_seg + 1).astype(float)
conteos[conteos == 0] = 1

variables = np.zeros((n_seg + 1, len(nombres_banda) * 2), dtype=np.float32)
for b in range(len(nombres_banda)):
    vals = img[b].ravel().astype(np.float64)
    s1 = np.bincount(seg_plano, weights=vals, minlength=n_seg + 1)
    s2 = np.bincount(seg_plano, weights=vals * vals, minlength=n_seg + 1)
    media = s1 / conteos
    var = np.maximum(s2 / conteos - media**2, 0)
    variables[:, 2*b], variables[:, 2*b+1] = media, np.sqrt(var)

nombres_variables = [f"{n}_{s}" for n in nombres_banda for s in ("media", "desv")]
print(f"Tabla de variables: {variables.shape[0]-1} parcelas x {variables.shape[1]} variables")"""),

md(
"""## Field labels: the ground truth (with a purity filter)

The label raster comes from **1,645 real field points** collected in the
Yaqui Valley: wheat, corn, chickpea and more.

![labels and purity](anim/en/07_labels_purity.svg)
""",
"""## Etiquetas de campo: la verdad en terreno (con filtro de pureza)

El raster de etiquetas viene de **1,645 puntos reales de campo** levantados
en el Valle del Yaqui: trigo, maíz, garbanzo y más.

![etiquetas y pureza](anim/es/07_labels_purity.svg)
"""),

code(
"""# Step 5 — Attach labels to parcels (majority + purity)
with rasterio.open(LABELS) as src:
    lab = src.read(1)
class_names = {int(k): v for k, v in json.load(open(NAMES)).items()}

parcel_label = np.zeros(n_seg + 1, dtype=int)
for sid in np.unique(seg[lab > 0]):
    values = lab[(seg == sid) & (lab > 0)]
    uniq = np.unique(values)
    if len(uniq) == 1:                      # pure parcel -> usable for training
        parcel_label[sid] = uniq[0]

train_ids = np.flatnonzero(parcel_label)
print(f"Pure labeled parcels: {len(train_ids)} of {n_seg}")
for cid, cname in class_names.items():
    print(f"  {cname:12s}: {(parcel_label[train_ids] == cid).sum():3d} parcels")""",
"""# Paso 5 — Asignar etiquetas a parcelas (mayoría + pureza)
with rasterio.open(LABELS) as src:
    lab = src.read(1)
nombres_clase = {int(k): v for k, v in json.load(open(NOMBRES)).items()}

etiqueta_parcela = np.zeros(n_seg + 1, dtype=int)
for sid in np.unique(seg[lab > 0]):
    valores = lab[(seg == sid) & (lab > 0)]
    unicos = np.unique(valores)
    if len(unicos) == 1:                    # parcela pura -> sirve para entrenar
        etiqueta_parcela[sid] = unicos[0]

ids_entrena = np.flatnonzero(etiqueta_parcela)
print(f"Parcelas etiquetadas puras: {len(ids_entrena)} de {n_seg}")
for cid, cname in nombres_clase.items():
    print(f"  {cname:12s}: {(etiqueta_parcela[ids_entrena] == cid).sum():3d} parcelas")"""),

md(
"""## Train the classifier

![training](anim/en/08_training.svg)
""",
"""## Entrenar el clasificador

![entrenamiento](anim/es/08_training.svg)
"""),

code(
"""# Step 6 — Random Forest (in the browser; the full pipeline uses TPOT/AutoML)
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

X = features[train_ids]
y = parcel_label[train_ids]
X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.3,
                                          random_state=42, stratify=y)
model = RandomForestClassifier(n_estimators=300, random_state=42, n_jobs=-1)
model.fit(X_tr, y_tr)
present = sorted(np.unique(y_te))
print(classification_report(
    y_te, model.predict(X_te),
    labels=present, target_names=[class_names[c] for c in present]))""",
"""# Paso 6 — Random Forest (en el navegador; el pipeline completo usa TPOT/AutoML)
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

X = variables[ids_entrena]
y = etiqueta_parcela[ids_entrena]
X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.3,
                                          random_state=42, stratify=y)
modelo = RandomForestClassifier(n_estimators=300, random_state=42, n_jobs=-1)
modelo.fit(X_tr, y_tr)
presentes = sorted(np.unique(y_te))
print(classification_report(
    y_te, modelo.predict(X_te),
    labels=presentes, target_names=[nombres_clase[c] for c in presentes]))"""),

md(
"""## The crop map

![crop map](anim/en/09_crop_map.svg)
""",
"""## El mapa de cultivos

![mapa de cultivos](anim/es/09_crop_map.svg)
"""),

code(
"""# Step 7 — Classify EVERY parcel and paint the map
pred = np.zeros(n_seg + 1, dtype=int)
pred[1:] = model.predict(features[1:])
crop_map = pred[seg]

palette = {1: "#c2703d", 2: "#65a30d", 3: "#a8a29e",
           4: "#86efac", 5: "#7c3aed", 6: "#eab308"}
rgb_map = np.zeros((*crop_map.shape, 3))
for cid, hx in palette.items():
    rgb_map[crop_map == cid] = [int(hx[i:i+2], 16)/255 for i in (1, 3, 5)]

import matplotlib.patches as mpatches
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12.5, 6))
ax1.imshow(rgb); ax1.set_title("Geomedian (true color)"); ax1.axis("off")
ax2.imshow(rgb_map); ax2.set_title("Predicted crop map"); ax2.axis("off")
ax2.legend(handles=[mpatches.Patch(color=palette[c], label=class_names[c])
                    for c in sorted(class_names)],
           loc="lower right", fontsize=8)
plt.tight_layout(); plt.show()
print("Congratulations — you classified real crops in your browser. 🌾")""",
"""# Paso 7 — Clasificar TODAS las parcelas y pintar el mapa
pred = np.zeros(n_seg + 1, dtype=int)
pred[1:] = modelo.predict(variables[1:])
mapa_cultivos = pred[seg]

paleta = {1: "#c2703d", 2: "#65a30d", 3: "#a8a29e",
          4: "#86efac", 5: "#7c3aed", 6: "#eab308"}
rgb_mapa = np.zeros((*mapa_cultivos.shape, 3))
for cid, hx in paleta.items():
    rgb_mapa[mapa_cultivos == cid] = [int(hx[i:i+2], 16)/255 for i in (1, 3, 5)]

import matplotlib.patches as mpatches
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12.5, 6))
ax1.imshow(rgb); ax1.set_title("Geomediana (color verdadero)"); ax1.axis("off")
ax2.imshow(rgb_mapa); ax2.set_title("Mapa de cultivos predicho"); ax2.axis("off")
ax2.legend(handles=[mpatches.Patch(color=paleta[c], label=nombres_clase[c])
                    for c in sorted(nombres_clase)],
           loc="lower right", fontsize=8)
plt.tight_layout(); plt.show()
print("Felicidades — clasificaste cultivos reales en tu navegador. 🌾")"""),

md(
"""## From this workshop to production

![full pipeline](anim/en/10_full_pipeline.svg)

Everything you just did, **[geocrop_analysis_mx](https://github.com/abxda/geocrop_analysis_mx)**
does at scale:

| Here (browser) | Full pipeline |
|---|---|
| 1 tile, 1 month | whole regions, many months + Sentinel-1 radar |
| bundled data | live download from STAC catalogs (NASA / Planetary Computer / Earth Search) — **or optionally Google Earth Engine** |
| Random Forest | TPOT (AutoML) |
| per-band mean/std | full zonal statistics + your own rasters (DEM, climate…) as extra features |

Install it with plain `pip install -r requirements.txt` (Windows, Linux,
macOS — no conda, no compilers) and follow its step-by-step tutorial.
""",
"""## De este taller a producción

![pipeline completo](anim/es/10_full_pipeline.svg)

Todo lo que acabas de hacer, **[geocrop_analysis_mx](https://github.com/abxda/geocrop_analysis_mx)**
lo hace a escala:

| Aquí (navegador) | Pipeline completo |
|---|---|
| 1 tile, 1 mes | regiones completas, muchos meses + radar Sentinel-1 |
| datos incluidos | descarga en vivo de catálogos STAC (NASA / Planetary Computer / Earth Search) — **u opcionalmente Google Earth Engine** |
| Random Forest | TPOT (AutoML) |
| media/desv por banda | estadísticas zonales completas + tus propios rasters (MDE, clima…) como variables extra |

Se instala con `pip install -r requirements.txt` (Windows, Linux, macOS —
sin conda, sin compiladores) y tiene tutorial paso a paso.
"""),
]


def build(lang):
    cells = []
    for kind, texts in CELLS:
        src = texts[lang].replace("__RAW__", RAW)
        if kind == "markdown":
            cells.append({"cell_type": "markdown", "metadata": {},
                          "source": src.splitlines(keepends=True)})
        else:
            cells.append({"cell_type": "code", "execution_count": None,
                          "metadata": {}, "outputs": [],
                          "source": src.splitlines(keepends=True)})
    return {"cells": cells,
            "metadata": {"kernelspec": {"display_name": "Python 3",
                                        "language": "python", "name": "python3"},
                         "language_info": {"name": "python"}},
            "nbformat": 4, "nbformat_minor": 5}


def main():
    import nbformat
    out_dir = ROOT
    os.makedirs(out_dir, exist_ok=True)
    for lang, fname in (("en", "Crop_Classification_Workshop.ipynb"),
                        ("es", "Taller_Clasificacion_Cultivos.ipynb")):
        nb = nbformat.from_dict(build(lang))
        nbformat.validator.normalize(nb)
        nbformat.write(nb, os.path.join(out_dir, fname))
        print(f"{fname}")


if __name__ == "__main__":
    main()
