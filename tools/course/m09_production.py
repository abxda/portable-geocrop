"""Module 9 — From your browser to production."""

from course.common import md

MODULE = dict(
    num=9,
    fname={"en": "09_from_browser_to_production.ipynb", "es": "09_del_navegador_a_produccion.ipynb"},
    title={"en": "Module 9 — From your browser to production",
           "es": "Módulo 9 — De tu navegador a producción"},
    cards=[
        ("synthetic-aperture-radar", {"en": "Synthetic Aperture Radar (Sentinel-1)",
                                      "es": "Radar de Apertura Sintética (Sentinel-1)"}),
        ("radar-vegetation-index", {"en": "Radar Vegetation Index (RVI)",
                                    "es": "Índice de Vegetación de Radar (RVI)"}),
        ("data-cube", {"en": "The data cube (space × bands × time)",
                       "es": "El cubo de datos (espacio × bandas × tiempo)"}),
        ("big-data", {"en": "Big data in remote sensing",
                      "es": "Big data en percepción remota"}),
        ("geospatial-data", {"en": "Geospatial data & QGIS",
                             "es": "Datos geoespaciales y QGIS"}),
        ("coordinate-reference-system", {"en": "Coordinate reference systems",
                                         "es": "Sistemas de referencia de coordenadas"}),
        ("raster", {"en": "Raster data", "es": "Datos ráster"}),
        ("vector", {"en": "Vector data (GeoPackage)", "es": "Datos vectoriales (GeoPackage)"}),
    ],
    cells=[

md(
"""# 🚀 Module 9 — From your browser to production

🧭 **Objectives** — connect everything you did in the browser to the real
production tool, **[geocrop_analysis_mx](https://github.com/abxda/geocrop_analysis_mx)**.
Understand what changes at scale, what the browser *cannot* do and why, and
exactly how to run the production pipeline yourself on the same Yaqui Valley
data — offline, no Google Earth Engine needed.

You are now equipped to use that tool *consciously*: you know what each phase
does, what it needs, and how to judge its output.

![full pipeline](../../anim/en/10_full_pipeline.svg)
""",
"""# 🚀 Módulo 9 — De tu navegador a producción

🧭 **Objetivos** — conectar todo lo que hiciste en el navegador con la
herramienta de producción real,
**[geocrop_analysis_mx](https://github.com/abxda/geocrop_analysis_mx)**.
Entender qué cambia a escala, qué *no puede* hacer el navegador y por qué, y
exactamente cómo correr tú mismo el pipeline de producción con los mismos
datos del Valle del Yaqui — offline, sin necesidad de Google Earth Engine.

Ahora estás equipado para usar esa herramienta de forma *consciente*: sabes
qué hace cada fase, qué necesita, y cómo juzgar su resultado.

![pipeline completo](../../anim/es/10_full_pipeline.svg)
"""),

md(
"""## Same story, bigger everything

Every step you learned maps one-to-one onto a phase of the production
pipeline — it just runs bigger:

| You did (browser) | `geocrop_analysis_mx` (desktop) | Phase |
|---|---|---|
| 1 tile, 1 month | whole regions, **many months** | `download` |
| geomedian given to you | builds geomedians from open STAC/COG **or** GEE | `download` |
| optical bands only | **+ Sentinel-1 radar (SAR)** and RVI | `download` |
| `shepherd-wasm` (NumPy) | `pyshepseg` (numba-accelerated) | `segment` |
| purity filter, by hand | spatial join + purity filter | `label` |
| mean/std of 13 layers | full zonal stats over **~846 features** | `extract` |
| Random Forest | **TPOT (AutoML)** searches the best pipeline | `train` |
| paint the array | writes a **GeoPackage** for QGIS | `predict` |

📚 **Why radar?** Clouds block optical sensors; **Synthetic Aperture Radar**
(Sentinel-1) sees through them and senses structure and moisture — extra
clues, especially in cloudy seasons. 📚 **Why many months?** That is the
**phenology** (Module 4) — the season-long NDVI story that separates
look-alike crops. Stacked months × bands × indices form a **data cube**.
""",
"""## La misma historia, todo más grande

Cada paso que aprendiste corresponde uno a uno con una fase del pipeline de
producción — solo que corre más grande:

| Tú hiciste (navegador) | `geocrop_analysis_mx` (escritorio) | Fase |
|---|---|---|
| 1 tile, 1 mes | regiones completas, **muchos meses** | `download` |
| geomediana ya dada | construye geomedianas desde STAC/COG abierto **o** GEE | `download` |
| solo bandas ópticas | **+ radar Sentinel-1 (SAR)** y RVI | `download` |
| `shepherd-wasm` (NumPy) | `pyshepseg` (acelerado con numba) | `segment` |
| filtro de pureza, a mano | unión espacial + filtro de pureza | `label` |
| media/desv de 13 capas | estadística zonal completa sobre **~846 variables** | `extract` |
| Random Forest | **TPOT (AutoML)** busca el mejor pipeline | `train` |
| pintar el arreglo | escribe un **GeoPackage** para QGIS | `predict` |

📚 **¿Por qué radar?** Las nubes bloquean los sensores ópticos; el **Radar de
Apertura Sintética** (Sentinel-1) ve a través de ellas y percibe estructura y
humedad — pistas extra, sobre todo en temporadas nubladas. 📚 **¿Por qué
muchos meses?** Esa es la **fenología** (Módulo 4) — la historia del NDVI a
lo largo de la temporada que separa cultivos parecidos. Los meses × bandas ×
índices apilados forman un **cubo de datos**.
"""),

md(
"""## What the browser cannot do — and why

Being honest about limits is part of using the tool well. The browser
(WebAssembly / Pyodide) is wonderful for *learning* and *small* jobs, but:

- **Memory.** Browser Python is **wasm32**: a hard ceiling around **4 GB**.
  A whole state or many-month cube does not fit; you would need tiling and
  streaming. The desktop tool has your machine's full RAM.
- **No numba, no GDAL binaries.** The fast desktop libraries (`pyshepseg`
  with numba, `earthengine-api`, TPOT's parallel search) either do not exist
  in Pyodide or run far slower. That is *why* `shepherd-wasm` exists — a
  pure-NumPy port so at least segmentation runs in the browser.
- **Compute time.** AutoML over hundreds of features across a region is
  minutes-to-hours of CPU — fine on a desktop, painful in a tab.

**The rule of thumb:** learn and prototype in the browser; run real regions
on the desktop (or the portable environment, next). Nothing you learned is
wasted — it is the *same pipeline*, just a bigger engine.
""",
"""## Qué no puede hacer el navegador — y por qué

Ser honesto sobre los límites es parte de usar bien la herramienta. El
navegador (WebAssembly / Pyodide) es maravilloso para *aprender* y trabajos
*pequeños*, pero:

- **Memoria.** El Python del navegador es **wasm32**: un techo duro de unos
  **4 GB**. Un estado completo o un cubo de muchos meses no cabe; necesitarías
  teselado y streaming. La herramienta de escritorio tiene toda la RAM de tu
  máquina.
- **Sin numba, sin binarios GDAL.** Las librerías rápidas de escritorio
  (`pyshepseg` con numba, `earthengine-api`, la búsqueda paralela de TPOT) o
  no existen en Pyodide o corren mucho más lento. Por *eso* existe
  `shepherd-wasm` — un port en NumPy puro para que al menos la segmentación
  corra en el navegador.
- **Tiempo de cómputo.** El AutoML sobre cientos de variables en una región
  son de minutos a horas de CPU — bien en escritorio, doloroso en una pestaña.

**La regla práctica:** aprende y prototipa en el navegador; corre regiones
reales en escritorio (o el entorno portable, a continuación). Nada de lo que
aprendiste se desperdicia — es el *mismo pipeline*, solo un motor más grande.
"""),

md(
"""## Run the production pipeline yourself (offline, no GEE)

`geocrop_analysis_mx` installs with plain `pip` — **no conda, no Google Earth
Engine account** — and ships with the Yaqui Valley test data pre-processed,
so you can reproduce the whole thing offline. In a terminal (not this
browser):

```bash
git clone https://github.com/abxda/geocrop_analysis_mx
cd geocrop_analysis_mx
python -m venv .venv && . .venv/bin/activate      # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt

# Copy the bundled Yaqui test data into place (enables OFFLINE mode)
python src/main.py --config config.test.yaml --phase setup_test

# Run the full pipeline — it detects the offline mosaics and skips any
# download / GEE connection automatically:
python src/main.py --config config.test.yaml --phase full_run
```

You will watch the same seven phases you now understand — segment, label,
extract, train (TPOT), predict — end with a `predicted_map_test.gpkg` and a
`classification_report.txt` reporting about **89% accuracy**. Open the
GeoPackage in **QGIS** to explore your crop map as real, coordinate-aware
**vector** data.

**Optional — with GEE.** If you *do* have a Google Earth Engine account and
want to classify your own area for fresh dates, `config.yaml` shows how to
point at your own AOI and let the `download` phase build geomedians live.
GEE is an option, never a requirement.
""",
"""## Corre tú mismo el pipeline de producción (offline, sin GEE)

`geocrop_analysis_mx` se instala con `pip` a secas — **sin conda, sin cuenta
de Google Earth Engine** — y viene con los datos de prueba del Valle del
Yaqui ya pre-procesados, así que puedes reproducir todo offline. En una
terminal (no en este navegador):

```bash
git clone https://github.com/abxda/geocrop_analysis_mx
cd geocrop_analysis_mx
python -m venv .venv && . .venv/bin/activate      # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt

# Copia los datos de prueba del Yaqui en su lugar (activa el modo OFFLINE)
python src/main.py --config config.test.yaml --phase setup_test

# Corre el pipeline completo — detecta los mosaicos offline y salta cualquier
# descarga / conexión a GEE automáticamente:
python src/main.py --config config.test.yaml --phase full_run
```

Verás las mismas siete fases que ahora entiendes — segment, label, extract,
train (TPOT), predict — terminando con un `predicted_map_test.gpkg` y un
`classification_report.txt` que reporta alrededor de **89% de exactitud**.
Abre el GeoPackage en **QGIS** para explorar tu mapa de cultivos como datos
**vectoriales** reales, con coordenadas.

**Opcional — con GEE.** Si *sí* tienes cuenta de Google Earth Engine y
quieres clasificar tu propia área para fechas nuevas, `config.yaml` muestra
cómo apuntar a tu propia AOI y dejar que la fase `download` construya
geomedianas en vivo. GEE es una opción, nunca un requisito.
"""),

md(
"""## The portable environment (no browser, no install headaches)

There is a third way, between the browser and a full developer setup: a
**portable environment** — a self-contained Python that runs from a folder,
no admin rights, no conda. The sister project
**[portable-satelital](https://abxda.github.io/portable-satelital/)** already
solved this (a signed, relocatable Python plus a one-click launcher). The
same recipe applies here: distribute `geocrop_analysis_mx` with a portable
Python so a non-expert can double-click and run the desktop pipeline without
touching a terminal. Browser for learning, portable for real work on a
laptop, desktop/server for big regions — the same course, three engines.
""",
"""## El entorno portable (sin navegador, sin dolores de instalación)

Hay una tercera vía, entre el navegador y una instalación completa de
desarrollador: un **entorno portable** — un Python autocontenido que corre
desde una carpeta, sin permisos de administrador, sin conda. El proyecto
hermano **[portable-satelital](https://abxda.github.io/portable-satelital/)**
ya resolvió esto (un Python relocalizable y firmado más un lanzador de un
clic). La misma receta aplica aquí: distribuir `geocrop_analysis_mx` con un
Python portable para que una persona no experta pueda dar doble clic y correr
el pipeline de escritorio sin tocar una terminal. Navegador para aprender,
portable para trabajo real en una laptop, escritorio/servidor para regiones
grandes — el mismo curso, tres motores.
"""),

md(
"""## 🎓 You made it

You started not knowing what a pixel's reflectance was. You now understand —
and have *run* — every step from raw satellite light to a validated crop map,
and you know when to trust the browser, when to move to the desktop, and how
to read a classifier honestly. That is the whole point: not to click a
button, but to use `geocrop_analysis_mx` **consciously**, aware of its
concepts, its requirements, and its limits.

🔭 To keep going deeper on any concept, follow the **Go deeper** links in each
module — they open the bilingual concept cards of
**[rs-learning-audio](https://abxda.github.io/rs-learning-audio/)**, where
every idea has its prerequisites, lineage and references.
""",
"""## 🎓 Lo lograste

Empezaste sin saber qué era la reflectancia de un píxel. Ahora entiendes — y
has *corrido* — cada paso desde la luz satelital cruda hasta un mapa de
cultivos validado, y sabes cuándo confiar en el navegador, cuándo pasar al
escritorio, y cómo leer un clasificador con honestidad. Ese es todo el
punto: no apretar un botón, sino usar `geocrop_analysis_mx` de forma
**consciente**, con conciencia de sus conceptos, sus requisitos y sus
límites.

🔭 Para seguir profundizando en cualquier concepto, sigue los enlaces
**Profundiza** de cada módulo — abren las tarjetas de conceptos bilingües de
**[rs-learning-audio](https://abxda.github.io/rs-learning-audio/)**, donde
cada idea tiene sus prerrequisitos, linaje y referencias.
"""),

],
)
