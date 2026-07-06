# Plan del curso — portable-geocrop v2 (borrador de trabajo)

> Documento de diseño interno (2026-07-05). Guía la expansión del taller actual a un
> curso autocontenido. No se publica en el sitio (el deploy solo empaqueta lo staged).

## Diagnóstico

Lo que existe hoy es un **taller de una sesión** (teoría de 10 secciones + cuaderno de
8 pasos sobre `files/crop_tile_384.tif`) con bilingüismo EN/ES completo y generado
desde `tools/gen_notebooks.py` / `tools/gen_anims.py`. Lo que falta para que sea un
**curso desde cero**:

- Asume Python, estadística básica y nociones de ML (menciona `train_test_split`,
  precision/recall, media/desviación sin enseñarlos).
- No hay módulos introductorios, ejercicios ni auto-evaluación.
- No hay conexión de profundización hacia las 564 tarjetas bilingües de
  [rs-learning-audio](https://github.com/abxda/rs-learning-audio).
- El puente hacia producción (`geocrop_analysis_mx`) es una tabla comparativa, no una
  guía de uso consciente.

## Principios de diseño

1. **Lineal, sin bifurcaciones.** Un solo camino M0 → M9. Cada módulo termina
   enlazando al siguiente.
2. **Autocontenido.** Cero requisitos: Python, estadística y ML se enseñan dentro del
   camino, justo antes de usarse (estilo `portable-satelital`: teoría ilustrada →
   práctica inmediata sobre el mismo caso real).
3. **Un dataset, una historia.** El tile del Valle del Yaqui (13 bandas, marzo 2018)
   atraviesa todos los módulos; el alumno lo conoce cada vez más profundo.
4. **Inglés principal, español conmutables.** Se conserva el mecanismo actual:
   generadores con `{"en":…, "es":…}` → cuadernos gemelos; páginas web con
   `lang-en`/`lang-es` + `localStorage`.
5. **WASM primero, portable después.** Todo corre en JupyterLite/Pyodide con
   `shepherd-wasm`; el módulo final explica cuándo y cómo saltar al entorno de
   escritorio/portable (patrón resuelto en `portable-satelital`).
6. **Profundización = tarjetas.** Cada módulo cierra con "Go deeper": enlaces a
   tarjetas específicas de rs-learning-audio por slug (requiere añadir deep-link
   `?id=<slug>` a esa app; ver Fase B).
7. **Meta final: uso consciente de `geocrop_analysis_mx`** — el alumno termina
   sabiendo qué hace cada fase del pipeline, qué requiere, y qué limitaciones tiene
   cada entorno (navegador wasm32 ~4 GB, sin numba/GDAL vs escritorio conda).

## Temario (módulos lineales)

Estructura fija de cada módulo: **objetivos → teoría ilustrada → práctica en el
cuaderno → "Check yourself" (2-3 preguntas con respuestas plegadas) → "Go deeper"
(tarjetas) → puente al siguiente módulo.**

| # | Módulo (EN) | Contenido | Práctica sobre el tile | Tarjetas "Go deeper" (slugs verificados) |
|---|---|---|---|---|
| M0 | Welcome: a real lab in your browser | Qué lograrás (un mapa de cultivos real); cómo funciona el curso; qué es un cuaderno Jupyter; dónde corre este Python (WASM/Pyodide); cómo pedir ayuda | Ejecutar la primera celda; detectar `emscripten` | `jupyter-notebook`, `jupyterlab`, `reproducibility` |
| M1 | Just enough Python | Variables, listas, funciones, arreglos NumPy, primer gráfico matplotlib — solo lo que el curso usa | Aritmética con mini-arreglos que simulan píxeles; graficar una "firma" inventada | — (módulo instrumental) |
| M2 | How a satellite sees | Radiación EM, reflectancia, bandas, firma espectral, resoluciones (espacial/temporal/espectral), Landsat + Sentinel-2 + HLS | Abrir UNA banda del tile con rasterio; ver que la imagen son números; comparar valores de agua/vegetación/suelo | `remote-sensing`, `electromagnetic-spectrum`, `reflectance`, `spectral-signature`, `spectral-bands`, `resolution`, `landsat`, `sentinel-missions` |
| M3 | Clean data: from clouds to geomedian | Nubes/sombras y máscaras, ARD, compositing temporal, la geomediana, catálogos abiertos (STAC/COG), GEE como opción | Explorar metadata del tile; componer RGB con estiramiento percentil 2–98 | `cloud-masking`, `quality-flags`, `analysis-ready-data`, `temporal-compositing`, `harmonized-landsat-sentinel`, `surface-reflectance` |
| M4 | Vegetation indices | NDVI desde la física (rojo vs NIR); los otros 6 índices del tile (EVI, GCVI, MSAVI2, LSWI, NDSVI, NDTI) y qué aporta cada uno; fenología | Calcular NDVI a mano desde las bandas y verificar contra la capa 7 del tile; mapa NDVI | `ndvi`, `vegetation-indices`, `spectral-indices`, `near-infrared`, `phenology`, `leaf-area-index` |
| M5 | From pixels to parcels | Por qué objetos y no píxeles; k-means intuitivo (familias espectrales); algoritmo Shepherd paso a paso; `shepherd-wasm` | Segmentar el tile; visualizar fronteras; experimentar `numClusters`/`minSegmentSize` | `segmentation`, `image-segmentation`, `object-based-classification`, `clustering`, `pixel-classification` |
| M6 | Parcels become a table + ground truth | Media y desviación desde cero; estadística zonal; qué es verdad de campo; puntos GPS → segmentos; filtro de pureza | Features por segmento (`np.bincount`); unir etiquetas; contar parcelas por clase | `zonal-statistics`, `ground-truth`, `training-samples`, `sample-balancing` |
| M7 | Machine learning from zero | Qué es un modelo; árbol de decisión; bosque aleatorio; entrenar/probar con honestidad (split estratificado); matriz de confusión; accuracy, precision/recall, F1, kappa; errores de omisión/comisión | Entrenar RF; leer `classification_report` línea por línea; dibujar la matriz de confusión | `machine-learning`, `decision-tree`, `random-forest`, `model-training`, `training-dataset`, `validation`, `confusion-matrix`, `overall-accuracy`, `producer-s-accuracy`, `recall`, `f1-score`, `cohen-s-kappa`, `omission`, `commission`, `accuracy-assessment` |
| M8 | Capstone: the crop map, end to end | El pipeline completo de corrido (ahora cada paso se entiende); pintar el mapa; qué salió bien y qué dudar del mapa | Pipeline completo en un cuaderno; mapa final vs color verdadero; celebración | `crop-classification`, `crop-type-mapping`, `land-cover` |
| M9 | From browser to production | `geocrop_analysis_mx` consciente: fases del pipeline real (download GEE opcional / offline, segment, label, extract 846 features multi-mes+radar, TPOT, predict); requisitos (conda, 8 GB RAM, QGIS); límites del navegador (wasm32 ~4 GB, sin numba/GDAL/TPOT) y cuándo saltar a escritorio o al laboratorio portable; correr el tutorial Yaqui offline; llevar TU propia AOI | (lectura + guía; el alumno sale del navegador) | `synthetic-aperture-radar`, `radar-vegetation-index`, `big-data`, `data-cube`, `geospatial-data`, `coordinate-reference-system`, `raster`, `vector`, `gis` |

Notas:
- EVI no tiene tarjeta propia en la ontología → se enlaza `vegetation-indices`.
- El taller actual de 8 pasos se convierte en M8 (capstone); sus celdas se reparten
  como "práctica" de M2–M7 con la teoría enseñada justo antes.
- Las 10 animaciones existentes se reutilizan; se añaden nuevas solo donde un
  concepto nuevo lo pida (árbol de decisión, firma espectral, matriz de confusión).

## Arquitectura de implementación

- `tools/gen_notebooks.py` → refactor a `MODULES = [{"slug", "title": {en,es},
  "cells": […]}]`; genera `notebooks/en/00_welcome.ipynb` … `09_production.ipynb` y
  gemelos `notebooks/es/…` con navegación prev/siguiente al inicio y final de cada
  cuaderno. Se mantienen los dos cuadernos actuales como M8 (renombrados/regenerados).
- `web/index.html` → landing con la ruta lineal de 10 módulos (mismo switch EN/ES).
- `web/theory.html` → se conserva como "the story in 10 steps" (resumen ejecutivo),
  enlazando a los módulos.
- `build/deploy_site.sh` → stage de todos los cuadernos nuevos.
- CI opcional (GitHub Actions → gh-pages) en fase posterior.

## Fases de trabajo

- **Fase A — geocrop_analysis_mx usable (Meta 2, quick wins):** quitar referencia a
  `organize_mosaics.sh` inexistente (INSTRUCTIONS.md §4.2 → fase `setup_test`);
  guard en `full_run` offline para no tocar GEE si los mosaicos existen; limpiar
  `__pycache__` + `.gitignore`; rutas del YAML resueltas relativas al archivo de
  config; prueba end-to-end del tutorial offline.
- **Fase B — deep-link en rs-learning-audio:** handler `?id=<slug>` en la app
  (`src/handbook_rs/stage9_app.py` + `out/index.html`) para que el curso pueda
  enlazar tarjetas.
- **Fase C — contenido M0–M9** en los generadores (EN+ES).
- **Fase D — build local JupyterLite y verificación** de los cuadernos en Pyodide.
- **Fase E — commits, push y deploy** (deploy a gh-pages solo tras verificación).
