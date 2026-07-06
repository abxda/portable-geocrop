# 🌾 portable-geocrop

**A hands-on, bilingual workshop that teaches crop classification from open
satellite data — running entirely in your browser.**

*Un taller práctico y bilingüe que enseña clasificación de cultivos con datos
satelitales abiertos — corriendo completamente en tu navegador.*

**Live site / Sitio en vivo:** <https://abxda.github.io/portable-geocrop/>

---

## English

This is the self-contained, didactic companion of
[**geocrop_analysis_mx**](https://github.com/abxda/geocrop_analysis_mx), the
production pipeline for crop classification with open STAC/COG data. It is a
**linear course of 10 modules** that assumes **no prior knowledge** — not in
programming, GIS or machine learning — and walks from "what is a pixel's
reflectance?" all the way to consciously running the production pipeline. The
course reproduces the full storyline — open data sources, monthly geomedians,
Shepherd segmentation, per-parcel features, field labels, training and the
final crop map — on one real tile of the **Yaqui Valley (Sonora, Mexico)**,
with **no installation and no accounts**: every cell runs in WebAssembly
(Pyodide) inside your browser.

### The 10 modules (in order)

0. Welcome: a real lab in your browser — 1. Just enough Python — 2. How a
   satellite sees the world — 3. Clean data: from clouds to the geomedian —
   4. Vegetation indices — 5. From pixels to parcels: segmentation —
   6. Parcels become a table + the ground truth — 7. Machine learning from
   zero — 8. Capstone: the crop map, end to end — 9. From your browser to
   production.

- **Self-contained and linear.** No branches: do the modules in order, each
  builds on the last. Concepts that would normally be assumed (Python,
  statistics, ML terms) are taught in place, right before they are used.
- **English by default, Spanish on a switch.** Every module is generated as
  twin EN/ES notebooks from a single source; the landing and theory pages
  have an EN/ES toggle.
- **Go deeper on demand.** Each module ends with links to bilingual concept
  cards in [rs-learning-audio](https://github.com/abxda/rs-learning-audio)
  (via `?id=<slug>` deep links) for prerequisite chains and references.
- **Animated theory + real data.** SVG animations explain each concept; the
  tile is the March-2018 geomedian of the Yaqui Valley, built by
  geocrop_analysis_mx from NASA HLS imagery, with labels from 1,645 real
  field points.

### Run it locally

```bash
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install jupyterlab shepherd-wasm rasterio matplotlib scikit-learn scipy
jupyter lab      # open notebooks/en/00_welcome.ipynb
```

### Repository layout

| Path | What it is |
|---|---|
| `notebooks/en/`, `notebooks/es/` | the 10 course modules, per language (generated) |
| `tools/course/mNN_*.py` | one source file per module (EN+ES text in one place) |
| `tools/gen_course.py` | regenerates all 20 module notebooks from `tools/course/` |
| `Crop_Classification_Workshop.ipynb` | the original single-session workshop (English) |
| `Taller_Clasificacion_Cultivos.ipynb` | the original single-session workshop (Spanish) |
| `tools/gen_notebooks.py` | regenerates the single-session workshop (source for module 8) |
| `anim/en/`, `anim/es/` | the SVG animations, per language |
| `files/` | the workshop tile, labels and class names |
| `web/index.html`, `web/theory.html` | bilingual landing + theory pages |
| `tools/gen_anims.py` | regenerates all animations (one source, both languages) |
| `build/deploy_site.sh` | builds the JupyterLite site and deploys to gh-pages |
| `docs/COURSE_PLAN.md` | the course design (syllabus, concept-card mapping, phases) |

Regenerate the course after editing any module source:

```bash
python tools/gen_course.py
```

### Deploy the site

```bash
bash build/deploy_site.sh            # builds + pushes to gh-pages
bash build/deploy_site.sh --no-push  # builds into dist/site only
```

---

## Español

Este es el acompañante didáctico y autocontenido de
[**geocrop_analysis_mx**](https://github.com/abxda/geocrop_analysis_mx), el
pipeline de producción para clasificación de cultivos con datos abiertos
STAC/COG. Es un **curso lineal de 10 módulos** que **no asume conocimientos
previos** — ni en programación, ni en SIG, ni en aprendizaje automático — y
va desde "¿qué es la reflectancia de un píxel?" hasta correr de forma
consciente el pipeline de producción. El curso reproduce toda la historia —
fuentes de datos abiertas, geomedianas mensuales, segmentación Shepherd,
variables por parcela, etiquetas de campo, entrenamiento y el mapa de
cultivos final — sobre un tile real del **Valle del Yaqui (Sonora, México)**,
**sin instalar nada y sin cuentas**: cada celda corre en WebAssembly
(Pyodide) dentro de tu navegador.

### Los 10 módulos (en orden)

0. Bienvenida: un laboratorio real en tu navegador — 1. El Python justo y
   necesario — 2. Cómo ve el mundo un satélite — 3. Datos limpios: de las
   nubes a la geomediana — 4. Índices de vegetación — 5. De píxeles a
   parcelas: segmentación — 6. Las parcelas se vuelven tabla + la verdad de
   campo — 7. Aprendizaje automático desde cero — 8. Proyecto final: el mapa
   de cultivos — 9. De tu navegador a producción.

- **Autocontenido y lineal.** Sin bifurcaciones: haz los módulos en orden,
  cada uno se apoya en el anterior. Los conceptos que normalmente se dan por
  hechos (Python, estadística, términos de ML) se enseñan en su lugar, justo
  antes de usarse.
- **Inglés por defecto, español con un interruptor.** Cada módulo se genera
  como cuadernos gemelos EN/ES desde una sola fuente; la portada y la teoría
  tienen switch EN/ES.
- **Profundiza cuando quieras.** Cada módulo termina con enlaces a tarjetas de
  conceptos bilingües en
  [rs-learning-audio](https://github.com/abxda/rs-learning-audio) (vía deep
  links `?id=<slug>`) con cadenas de prerrequisitos y referencias.
- **Teoría animada + datos reales.** Animaciones SVG explican cada concepto;
  el tile es la geomediana de marzo-2018 del Valle del Yaqui, construida por
  geocrop_analysis_mx con imágenes HLS de la NASA, y las etiquetas derivan de
  1,645 puntos reales de campo.

### Correrlo localmente

```bash
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install jupyterlab shepherd-wasm rasterio matplotlib scikit-learn scipy
jupyter lab      # abre notebooks/es/00_bienvenida.ipynb
```

---

**Author / Autor:** Dr. Abel Coronado ([@abxda](https://github.com/abxda)) ·
built with / construido con **Claude Fable** (Anthropic) · MIT License.

Sibling projects / Proyectos hermanos:
[portable-satelital](https://github.com/abxda/portable-satelital) ·
[shepherd-wasm](https://github.com/abxda/shepherd-wasm) ·
[geocrop_analysis_mx](https://github.com/abxda/geocrop_analysis_mx)
