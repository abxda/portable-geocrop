"""Module 0 — Welcome: a real lab in your browser."""

from course.common import md, code

MODULE = dict(
    num=0,
    fname={"en": "00_welcome.ipynb", "es": "00_bienvenida.ipynb"},
    title={"en": "Module 0 — Welcome: a real lab in your browser",
           "es": "Módulo 0 — Bienvenida: un laboratorio real en tu navegador"},
    cards=[
        ("jupyter-notebook", {"en": "What a Jupyter notebook is",
                              "es": "Qué es un cuaderno Jupyter"}),
        ("jupyterlab", {"en": "JupyterLab, the environment around it",
                        "es": "JupyterLab, el entorno que lo rodea"}),
        ("reproducibility", {"en": "Why reproducible analysis matters",
                             "es": "Por qué importa el análisis reproducible"}),
    ],
    cells=[

md(
"""# 🌾 Module 0 — Welcome: a real lab in your browser

By the end of this course you will have built a **real crop map**: you will
classify actual farm parcels of the **Yaqui Valley (Sonora, Mexico)** — wheat,
corn, chickpea and more — from open satellite data, and you will understand
**every step** you took to get there.

No prior experience is assumed. Not in programming, not in maps, not in
machine learning. The course is one straight path:

| Module | You will learn |
|---|---|
| 0 | How this course and your browser-lab work *(you are here)* |
| 1 | Just enough Python |
| 2 | How a satellite sees the world |
| 3 | Clean data: from clouds to the geomedian |
| 4 | Vegetation indices — reading plant health from light |
| 5 | From pixels to parcels: segmentation |
| 6 | Parcels become a table + the ground truth |
| 7 | Machine learning from zero |
| 8 | Capstone: the crop map, end to end |
| 9 | From your browser to production |

Do the modules **in order** — each one uses what the previous one taught,
nothing more.

**Author:** Dr. Abel Coronado ([@abxda](https://github.com/abxda)) ·
built with Claude Fable (Anthropic)
""",
"""# 🌾 Módulo 0 — Bienvenida: un laboratorio real en tu navegador

Al terminar este curso habrás construido un **mapa de cultivos real**:
clasificarás parcelas agrícolas verdaderas del **Valle del Yaqui (Sonora,
México)** — trigo, maíz, garbanzo y más — a partir de datos satelitales
abiertos, y entenderás **cada paso** que diste para lograrlo.

No se asume experiencia previa. Ni en programación, ni en mapas, ni en
aprendizaje automático. El curso es un solo camino recto:

| Módulo | Aprenderás |
|---|---|
| 0 | Cómo funcionan este curso y tu laboratorio en el navegador *(estás aquí)* |
| 1 | El Python justo y necesario |
| 2 | Cómo ve el mundo un satélite |
| 3 | Datos limpios: de las nubes a la geomediana |
| 4 | Índices de vegetación — leer la salud de las plantas en la luz |
| 5 | De píxeles a parcelas: segmentación |
| 6 | Las parcelas se vuelven tabla + la verdad de campo |
| 7 | Aprendizaje automático desde cero |
| 8 | Proyecto final: el mapa de cultivos, de punta a punta |
| 9 | De tu navegador a producción |

Haz los módulos **en orden** — cada uno usa lo que enseñó el anterior,
nada más.

**Autor:** Dr. Abel Coronado ([@abxda](https://github.com/abxda)) ·
construido con Claude Fable (Anthropic)
"""),

md(
"""## What is this page? Your first notebook

This page is a **Jupyter notebook**: a document made of **cells**. Some
cells are text (like this one). Others contain **Python code** — and those
you can **run**, right here.

How to run a code cell:

1. Click on the cell to select it.
2. Press **Shift + Enter** (or the ▶ button in the toolbar).
3. The result appears immediately below the cell.

Two rules that will save you headaches:

- **Run cells from top to bottom.** Later cells often use results from
  earlier ones.
- If things get confused, use the menu **Kernel → Restart Kernel and Run All
  Cells** — it wipes the slate clean and re-runs everything in order.

Try it now with the cell below. 👇
""",
"""## ¿Qué es esta página? Tu primer cuaderno

Esta página es un **cuaderno Jupyter**: un documento hecho de **celdas**.
Algunas celdas son texto (como esta). Otras contienen **código Python** — y
esas las puedes **ejecutar**, aquí mismo.

Cómo ejecutar una celda de código:

1. Haz clic en la celda para seleccionarla.
2. Presiona **Shift + Enter** (o el botón ▶ de la barra).
3. El resultado aparece justo debajo de la celda.

Dos reglas que te ahorrarán dolores de cabeza:

- **Ejecuta las celdas de arriba hacia abajo.** Las celdas de abajo suelen
  usar resultados de las de arriba.
- Si algo se enreda, usa el menú **Kernel → Restart Kernel and Run All
  Cells** — borra todo y vuelve a ejecutar en orden.

Pruébalo ahora con la celda de abajo. 👇
"""),

code(
"""# Your very first cell. Select it and press Shift + Enter.
message = "I just ran Python code!"
print(message)
print("2 + 2 =", 2 + 2)""",
"""# Tu primera celda. Selecciónala y presiona Shift + Enter.
mensaje = "¡Acabo de ejecutar código Python!"
print(mensaje)
print("2 + 2 =", 2 + 2)"""),

md(
"""## Where is this Python running?

Normally Python runs on a server or on a program you install. Here it runs
**inside your browser**, thanks to **WebAssembly** (via a project called
Pyodide): your browser downloaded a complete scientific Python and executes
it locally, in a sandbox. Nothing is installed on your machine, no account
is created, and your data never leaves your computer.

![where does this run](../../anim/en/01_where_it_runs.svg)

Let's ask Python itself where it lives:
""",
"""## ¿Dónde está corriendo este Python?

Normalmente Python corre en un servidor o en un programa que instalas. Aquí
corre **dentro de tu navegador**, gracias a **WebAssembly** (vía un proyecto
llamado Pyodide): tu navegador descargó un Python científico completo y lo
ejecuta localmente, en un espacio aislado. No se instala nada en tu máquina,
no se crea ninguna cuenta, y tus datos nunca salen de tu computadora.

![dónde corre esto](../../anim/es/01_where_it_runs.svg)

Preguntémosle al propio Python dónde vive:
"""),

code(
"""# Where is this Python running?
import sys, platform
print(f"Python   : {sys.version.split()[0]}")
print(f"Platform : {sys.platform!r} / {platform.machine()!r}")
if sys.platform == "emscripten":
    print("Running in WebAssembly, INSIDE your browser. No server. 🚀")
else:
    print("Running locally (regular Python) — everything works the same.")""",
"""# ¿Dónde está corriendo este Python?
import sys, platform
print(f"Python     : {sys.version.split()[0]}")
print(f"Plataforma : {sys.platform!r} / {platform.machine()!r}")
if sys.platform == "emscripten":
    print("Corriendo en WebAssembly, DENTRO de tu navegador. Sin servidor. 🚀")
else:
    print("Corriendo en modo local (Python normal) — todo funciona igual.")"""),

md(
"""## How each module works

Every module repeats the same rhythm, so you always know where you are:

- 🧭 **Objectives** — what you will be able to do at the end.
- 📚 **Theory** — the idea, explained from zero, with an illustration.
- 💻 **Practice** — you run it immediately on the *same real data*: one
  satellite tile of the Yaqui Valley that accompanies you through the whole
  course.
- 🧪 **Check yourself** — a couple of questions (with folded answers).
- 🔭 **Go deeper** — optional links to bilingual *concept cards* with
  prerequisite chains and curated references, when you want more.

One warning about patience: some steps (downloading the tile the first
time, segmenting the image) take from seconds up to a minute. Each cell
tells you what to expect — if a cell shows `[*]` on its left margin, it is
still working.
""",
"""## Cómo funciona cada módulo

Todos los módulos repiten el mismo ritmo, para que siempre sepas dónde
estás:

- 🧭 **Objetivos** — qué sabrás hacer al terminar.
- 📚 **Teoría** — la idea, explicada desde cero, con una ilustración.
- 💻 **Práctica** — lo ejecutas de inmediato sobre los *mismos datos
  reales*: un tile satelital del Valle del Yaqui que te acompaña durante
  todo el curso.
- 🧪 **Ponte a prueba** — un par de preguntas (con respuestas plegadas).
- 🔭 **Profundiza** — enlaces opcionales a *tarjetas de conceptos*
  bilingües con cadenas de prerrequisitos y referencias, para cuando
  quieras más.

Una advertencia sobre paciencia: algunos pasos (descargar el tile la
primera vez, segmentar la imagen) tardan de segundos a un minuto. Cada
celda te dice qué esperar — si una celda muestra `[*]` en su margen
izquierdo, sigue trabajando.
"""),

md(
"""## 🧪 Check yourself

**What happens if you run the cells of a notebook out of order?**

<details><summary>Show answer</summary>

Later cells may fail or use stale values, because they depend on variables
created by earlier cells. If that happens, use *Kernel → Restart Kernel and
Run All Cells* to start clean.

</details>

**Does this course send your data to a server?**

<details><summary>Show answer</summary>

No. The Python you just ran lives inside your browser (WebAssembly). The
satellite tile is downloaded *to* your browser, and everything you compute
stays on your machine.

</details>
""",
"""## 🧪 Ponte a prueba

**¿Qué pasa si ejecutas las celdas de un cuaderno en desorden?**

<details><summary>Ver respuesta</summary>

Las celdas de abajo pueden fallar o usar valores viejos, porque dependen de
variables creadas por celdas anteriores. Si pasa, usa *Kernel → Restart
Kernel and Run All Cells* para empezar limpio.

</details>

**¿Este curso envía tus datos a un servidor?**

<details><summary>Ver respuesta</summary>

No. El Python que acabas de ejecutar vive dentro de tu navegador
(WebAssembly). El tile satelital se descarga *hacia* tu navegador, y todo lo
que calculas se queda en tu máquina.

</details>
"""),

],
)
