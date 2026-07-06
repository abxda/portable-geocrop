"""Module 8 — Capstone: the crop map, end to end.

Reuses the original workshop cells (tools/gen_notebooks.py) as the capstone,
fixing relative paths (anim/, files/) for the notebooks/<lang>/ location and
replacing the workshop intro with a course-aware one.
"""

import gen_notebooks

from course.common import md


def _fix(cells):
    fixed = []
    for kind, texts in cells:
        t = {}
        for lang, src in texts.items():
            src = src.replace("](anim/", "](../../anim/")
            src = src.replace(', f"../files/{name}")',
                              ', f"../files/{name}", f"../../files/{name}")')
            t[lang] = src
        fixed.append((kind, t))
    return fixed


_INTRO = md(
"""# 🌾 Module 8 — Capstone: the crop map, end to end

This is the moment everything comes together. You will run the **complete
pipeline in one sitting** — load the tile, look at it, segment it, turn
parcels into a table, attach the field labels, train the classifier and
paint the crop map.

Nothing here is new: every step below is one you already understand from
modules 2–7. This time, notice how *short* the whole story is when you
know what each line does.

🧭 **Objectives**
- Run the full crop-classification pipeline without help.
- Read the quality report and the final map critically.
""",
"""# 🌾 Módulo 8 — Proyecto final: el mapa de cultivos, de punta a punta

Este es el momento en que todo se junta. Vas a correr el **pipeline completo
de una sola sentada** — cargar el tile, mirarlo, segmentarlo, convertir las
parcelas en tabla, unir las etiquetas de campo, entrenar el clasificador y
pintar el mapa de cultivos.

Nada de esto es nuevo: cada paso de abajo ya lo entiendes por los módulos
2–7. Esta vez, fíjate qué *corta* es la historia completa cuando sabes qué
hace cada línea.

🧭 **Objetivos**
- Correr el pipeline completo de clasificación de cultivos sin ayuda.
- Leer con ojo crítico el reporte de calidad y el mapa final.
""")


MODULE = dict(
    num=8,
    fname={"en": "08_capstone_crop_map.ipynb", "es": "08_proyecto_mapa_de_cultivos.ipynb"},
    title={"en": "Module 8 — Capstone: the crop map, end to end",
           "es": "Módulo 8 — Proyecto final: el mapa de cultivos"},
    cards=[
        ("crop-classification", {"en": "Crop classification, the whole idea",
                                 "es": "Clasificación de cultivos, la idea completa"}),
        ("crop-type-mapping", {"en": "Crop type mapping in practice",
                               "es": "Mapeo de tipos de cultivo en la práctica"}),
        ("land-cover", {"en": "Land cover, the broader family",
                        "es": "Cobertura del suelo, la familia más amplia"}),
    ],
    # CELLS[0] is the original workshop intro (twin links that don't apply
    # here); replace it with the course-aware intro and reuse the rest.
    cells=[_INTRO] + _fix(gen_notebooks.CELLS[1:]),
)
