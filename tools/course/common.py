"""Shared helpers for the course module sources (tools/course/mNN_*.py).

Every module file defines a MODULE dict:

    MODULE = dict(
        num=3,
        fname={"en": "03_clean_data.ipynb", "es": "03_datos_limpios.ipynb"},
        title={"en": "Module 3 - ...", "es": "Módulo 3 - ..."},
        cells=[md(...), code(...), ...],   # module body, in order
        cards=[(slug, {"en": label, "es": label}), ...],  # "Go deeper" links
    )

The generator (tools/gen_course.py) adds the navigation header/footer and the
"Go deeper" cell automatically, so module files only write the body.
"""

RAW = "https://raw.githubusercontent.com/abxda/portable-geocrop/main/files"

# Concept cards of the companion knowledge base (rs-learning-audio).
# ?id=<slug> deep-links straight to one bilingual concept card.
CARDS_BASE = "https://abxda.github.io/rs-learning-audio/?id="


def md(en, es):
    return ("markdown", {"en": en, "es": es})


def code(en, es=None):
    return ("code", {"en": en, "es": es if es is not None else en})


def anim(lang, name):
    return f"../../anim/{lang}/{name}.svg"


def check(items):
    """Self-check cell: list of ((q_en, q_es), (a_en, a_es)); answers folded."""
    def block(lang, header):
        parts = [f"## {header}\n"]
        for (q, a) in items:
            parts.append(
                f"**{q[lang]}**\n\n<details><summary>"
                + ("Show answer" if lang == "en" else "Ver respuesta")
                + f"</summary>\n\n{a[lang]}\n\n</details>\n"
            )
        return "\n".join(parts)
    return md(block("en", "🧪 Check yourself"), block("es", "🧪 Ponte a prueba"))


def go_deeper_cell(cards):
    """Build the 'Go deeper' markdown cell from [(slug, {en,es}), ...]."""
    en = ["## 🔭 Go deeper\n",
          "Optional: these bilingual concept cards expand what you just learned",
          "(prerequisite chains, lineage to fundamentals, curated references):\n"]
    es = ["## 🔭 Profundiza\n",
          "Opcional: estas tarjetas bilingües de conceptos amplían lo que acabas",
          "de aprender (prerrequisitos, linaje a fundamentos, referencias):\n"]
    for slug, label in cards:
        en.append(f"- [{label['en']}]({CARDS_BASE}{slug})")
        es.append(f"- [{label['es']}]({CARDS_BASE}{slug}&lang=es)")
    return md("\n".join(en) + "\n", "\n".join(es) + "\n")


# Standard "load the workshop data" code cell, reused by several modules so
# each notebook runs on a fresh kernel. Variable names follow each language
# (the ES twins translate identifiers, matching the original workshop style).
LOAD_TILE_EN = '''# Get the workshop tile (a few MB; cached after the first download)
import os, sys

async def get_file(name):
    for cand in (f"files/{name}", name, f"../files/{name}", f"../../files/{name}"):
        if os.path.exists(cand):
            return cand
    dest = f"/tmp/{name}"
    if not os.path.exists(dest):
        url = f"__RAW__/{name}"
        if sys.platform == "emscripten":
            from pyodide.http import pyfetch
            resp = await pyfetch(url)
            open(dest, "wb").write(await resp.bytes())
        else:
            import urllib.request
            urllib.request.urlretrieve(url, dest)
    return dest

TILE = await get_file("crop_tile_384.tif")
print("Tile ready:", TILE)'''

LOAD_TILE_ES = '''# Trae el tile del taller (pocos MB; queda en caché tras la primera descarga)
import os, sys

async def trae_archivo(name):
    for cand in (f"files/{name}", name, f"../files/{name}", f"../../files/{name}"):
        if os.path.exists(cand):
            return cand
    dest = f"/tmp/{name}"
    if not os.path.exists(dest):
        url = f"__RAW__/{name}"
        if sys.platform == "emscripten":
            from pyodide.http import pyfetch
            resp = await pyfetch(url)
            open(dest, "wb").write(await resp.bytes())
        else:
            import urllib.request
            urllib.request.urlretrieve(url, dest)
    return dest

TILE = await trae_archivo("crop_tile_384.tif")
print("Tile listo:", TILE)'''
