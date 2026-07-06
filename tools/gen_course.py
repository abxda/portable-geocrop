#!/usr/bin/env python3
"""Bilingual course notebook generator (EN default + ES twin per module).

One source of truth: each module lives in tools/course/mNN_*.py as a MODULE
dict (see tools/course/common.py). This script assembles every module into
notebooks/en/NN_*.ipynb and notebooks/es/NN_*.ipynb, adding automatically:

  - a navigation header (module N of M, link to the twin language),
  - the "Go deeper" cell (concept-card deep links), when the module has cards,
  - a navigation footer (previous / next module).

Regenerate with:  python tools/gen_course.py
"""

import importlib
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

from course.common import RAW, go_deeper_cell  # noqa: E402

MODULE_NAMES = [
    "m00_welcome",
    "m01_python",
    "m02_satellite",
    "m03_clean_data",
    "m04_indices",
    "m05_segmentation",
    "m06_features_labels",
    "m07_machine_learning",
    "m08_capstone",
    "m09_production",
]

OTHER = {"en": "es", "es": "en"}
LANG_NOTE = {
    "en": "**¿Prefieres español?** Abre [{name}](../es/{fname}) — es el mismo módulo, en español.",
    "es": "**Prefer English?** Open [{name}](../en/{fname}) — it is the same module, in English.",
}
PREV = {"en": "← Previous", "es": "← Anterior"}
NEXT = {"en": "Next →", "es": "Siguiente →"}
OF = {"en": "Module {n} of {total}", "es": "Módulo {n} de {total}"}


def load_modules():
    mods = [importlib.import_module(f"course.{name}").MODULE for name in MODULE_NAMES]
    mods.sort(key=lambda m: m["num"])
    return mods


def header_cell(mods, i, lang):
    m = mods[i]
    twin = m["fname"][OTHER[lang]]
    note = LANG_NOTE[lang].format(name=f"`{twin}`", fname=twin)
    pos = OF[lang].format(n=m["num"], total=len(mods) - 1)
    return {
        "cell_type": "markdown",
        "metadata": {},
        "source": f"*{pos}*\n\n> {note}\n".splitlines(keepends=True),
    }


def footer_cell(mods, i, lang):
    links = []
    if i > 0:
        p = mods[i - 1]
        links.append(f"[{PREV[lang]} · {p['title'][lang]}]({p['fname'][lang]})")
    if i < len(mods) - 1:
        n = mods[i + 1]
        links.append(f"[{NEXT[lang]} · {n['title'][lang]}]({n['fname'][lang]})")
    return {
        "cell_type": "markdown",
        "metadata": {},
        "source": ("\n---\n\n" + " · ".join(links) + "\n").splitlines(keepends=True),
    }


def body_cells(module, lang):
    cells = list(module["cells"])
    if module.get("cards"):
        cells.append(go_deeper_cell(module["cards"]))
    out = []
    for kind, texts in cells:
        src = texts[lang].replace("__RAW__", RAW)
        if kind == "markdown":
            out.append({"cell_type": "markdown", "metadata": {},
                        "source": src.splitlines(keepends=True)})
        else:
            out.append({"cell_type": "code", "execution_count": None,
                        "metadata": {}, "outputs": [],
                        "source": src.splitlines(keepends=True)})
    return out


def build(mods, i, lang):
    cells = [header_cell(mods, i, lang)]
    cells += body_cells(mods[i], lang)
    cells.append(footer_cell(mods, i, lang))
    return {"cells": cells,
            "metadata": {"kernelspec": {"display_name": "Python 3",
                                        "language": "python", "name": "python3"},
                         "language_info": {"name": "python"}},
            "nbformat": 4, "nbformat_minor": 5}


def main():
    import nbformat
    mods = load_modules()
    for lang in ("en", "es"):
        out_dir = os.path.join(ROOT, "notebooks", lang)
        os.makedirs(out_dir, exist_ok=True)
        for i in range(len(mods)):
            nb = nbformat.from_dict(build(mods, i, lang))
            nbformat.validator.normalize(nb)
            fname = mods[i]["fname"][lang]
            nbformat.write(nb, os.path.join(out_dir, fname))
            print(f"notebooks/{lang}/{fname}")


if __name__ == "__main__":
    main()
