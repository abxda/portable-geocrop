# 🌾 portable-geocrop

**A hands-on, bilingual workshop that teaches crop classification from open
satellite data — running entirely in your browser.**

*Un taller práctico y bilingüe que enseña clasificación de cultivos con datos
satelitales abiertos — corriendo completamente en tu navegador.*

**Live site / Sitio en vivo:** <https://abxda.github.io/portable-geocrop/>

---

## English

This is the didactic companion of
[**geocrop_analysis_mx**](https://github.com/abxda/geocrop_analysis_mx), the
production pipeline for crop classification with open STAC/COG data. The
workshop reproduces the full storyline — open data sources, monthly
geomedians, Shepherd segmentation, per-parcel features, field labels,
training and the final crop map — on one real tile of the **Yaqui Valley
(Sonora, Mexico)**, with **no installation and no accounts**: every cell runs
in WebAssembly (Pyodide) inside your browser.

- **English by default, Spanish on a switch.** The landing page and theory
  page have an EN/ES toggle; the workshop ships as two twin notebooks.
- **Animated theory.** Ten SVG animations explain each concept, including
  where the imagery comes from and how the optional Google Earth Engine
  backend fits in.
- **Real data.** The tile is the March-2018 geomedian of the Yaqui Valley,
  built by geocrop_analysis_mx from NASA HLS imagery, with labels derived
  from 1,645 real field points.

### Run it locally

```bash
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install jupyterlab shepherd-wasm rasterio matplotlib scikit-learn scipy geopandas
jupyter lab      # open Crop_Classification_Workshop.ipynb
```

### Repository layout

| Path | What it is |
|---|---|
| `Crop_Classification_Workshop.ipynb` | the workshop (English) |
| `Taller_Clasificacion_Cultivos.ipynb` | the workshop (Spanish) |
| `anim/en/`, `anim/es/` | the SVG animations, per language |
| `files/` | the workshop tile, labels and class names |
| `web/index.html`, `web/theory.html` | bilingual landing + theory pages |
| `tools/gen_anims.py` | regenerates all animations (one source, both languages) |
| `tools/gen_notebooks.py` | regenerates both notebooks (one source, both languages) |
| `build/deploy_site.sh` | builds the JupyterLite site and deploys to gh-pages |

### Deploy the site

```bash
bash build/deploy_site.sh            # builds + pushes to gh-pages
bash build/deploy_site.sh --no-push  # builds into dist/site only
```

---

## Español

Este es el acompañante didáctico de
[**geocrop_analysis_mx**](https://github.com/abxda/geocrop_analysis_mx), el
pipeline de producción para clasificación de cultivos con datos abiertos
STAC/COG. El taller reproduce toda la historia — fuentes de datos abiertas,
geomedianas mensuales, segmentación Shepherd, variables por parcela, etiquetas
de campo, entrenamiento y el mapa de cultivos final — sobre un tile real del
**Valle del Yaqui (Sonora, México)**, **sin instalar nada y sin cuentas**:
cada celda corre en WebAssembly (Pyodide) dentro de tu navegador.

- **Inglés por defecto, español con un interruptor.** La portada y la página
  de teoría tienen un switch EN/ES; el taller viene como dos cuadernos gemelos.
- **Teoría animada.** Diez animaciones SVG explican cada concepto, incluyendo
  de dónde salen las imágenes y cómo encaja el backend opcional de Google
  Earth Engine.
- **Datos reales.** El tile es la geomediana de marzo-2018 del Valle del
  Yaqui, construida por geocrop_analysis_mx con imágenes HLS de la NASA, y las
  etiquetas derivan de 1,645 puntos reales de campo.

### Correrlo localmente

```bash
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install jupyterlab shepherd-wasm rasterio matplotlib scikit-learn scipy geopandas
jupyter lab      # abre Taller_Clasificacion_Cultivos.ipynb
```

---

**Author / Autor:** Dr. Abel Coronado ([@abxda](https://github.com/abxda)) ·
built with / construido con **Claude Fable** (Anthropic) · MIT License.

Sibling projects / Proyectos hermanos:
[portable-satelital](https://github.com/abxda/portable-satelital) ·
[shepherd-wasm](https://github.com/abxda/shepherd-wasm) ·
[geocrop_analysis_mx](https://github.com/abxda/geocrop_analysis_mx)
