#!/usr/bin/env python3
"""Bilingual SVG animation generator for the portable-geocrop workshop.

Every animation is defined once; text comes from a translation table and the
script emits anim/en/*.svg and anim/es/*.svg. Visual language follows
portable-satelital (white cards, slate text, soft SMIL loops) extended for
the crop-classification storyline: open data sources (STAC) with the
optional Google Earth Engine branch, monthly geomedians, spectral indices,
Shepherd segmentation, per-segment features, field labels, training and the
final crop map.

Regenerate with:  python tools/gen_anims.py
"""

import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

FONT = 'font-family="Segoe UI,system-ui,sans-serif"'
INK = "#0f172a"; DIM = "#475569"; FAINT = "#94a3b8"
BLUE = "#0284c7"; GREEN = "#16a34a"; AMBER = "#d97706"; RED = "#e11d48"
WHEAT = "#eab308"; CORN = "#65a30d"; CHICK = "#c2703d"; SOIL = "#a8a29e"

T = {
 "01.title": {"en": "Where is this Python running?",
              "es": "¿Dónde está corriendo este Python?"},
 "01.browser": {"en": "your browser", "es": "tu navegador"},
 "01.inside": {"en": "full Python, right in here", "es": "Python completo, aquí adentro"},
 "01.server": {"en": "server / cloud", "es": "servidor / nube"},
 "01.notused": {"en": "not used", "es": "no se usa"},
 "01.cap": {"en": "The cell asks Python where it lives. Expected answer: 'wasm32' — inside YOUR browser, no server involved.",
            "es": "La celda le pregunta a Python dónde vive. Respuesta esperada: 'wasm32' — dentro de TU navegador, sin servidor."},

 "02.title": {"en": "Where do the images come from? Open catalogs (and optional GEE)",
              "es": "¿De dónde salen las imágenes? Catálogos abiertos (y GEE opcional)"},
 "02.nasa": {"en": "NASA Earthdata", "es": "NASA Earthdata"},
 "02.nasa2": {"en": "HLS: Landsat + Sentinel-2", "es": "HLS: Landsat + Sentinel-2"},
 "02.mpc": {"en": "Planetary Computer", "es": "Planetary Computer"},
 "02.mpc2": {"en": "Sentinel-1 radar (RTC)", "es": "radar Sentinel-1 (RTC)"},
 "02.es": {"en": "Earth Search / AWS", "es": "Earth Search / AWS"},
 "02.es2": {"en": "Sentinel-2 (browser-friendly)", "es": "Sentinel-2 (apto navegador)"},
 "02.you": {"en": "your computer", "es": "tu computadora"},
 "02.gee": {"en": "Google Earth Engine", "es": "Google Earth Engine"},
 "02.gee2": {"en": "OPTIONAL: only if you have an account",
             "es": "OPCIONAL: solo si tienes cuenta"},
 "02.cap": {"en": "Default: anonymous STAC catalogs stream only your area's pixels (HTTP range reads over COGs) — no account needed. GEE is an optional switch, never a requirement.",
            "es": "Por defecto: catálogos STAC anónimos transmiten solo los píxeles de tu zona (lecturas por rango sobre COGs) — sin cuenta. GEE es un interruptor opcional, nunca un requisito."},

 "03.title": {"en": "One month of scenes → one clean geomedian",
              "es": "Un mes de escenas → una geomediana limpia"},
 "03.cloudy": {"en": "clouds, shadows, gaps…", "es": "nubes, sombras, huecos…"},
 "03.gm": {"en": "geomedian", "es": "geomediana"},
 "03.gm2": {"en": "robust multi-band median", "es": "mediana multibanda robusta"},
 "03.cap": {"en": "Every pass sees different clouds. The geometric median keeps, per pixel, the most typical spectral signature of the month — clouds and shadows get voted out.",
            "es": "Cada pasada ve nubes distintas. La mediana geométrica conserva, por píxel, la firma espectral más típica del mes — nubes y sombras quedan fuera por mayoría."},

 "04.title": {"en": "13 layers per pixel: bands + vegetation indices",
              "es": "13 capas por píxel: bandas + índices de vegetación"},
 "04.bands": {"en": "6 spectral bands", "es": "6 bandas espectrales"},
 "04.idx": {"en": "7 indices (NDVI, EVI, …)", "es": "7 índices (NDVI, EVI, …)"},
 "04.healthy": {"en": "vigorous crop", "es": "cultivo vigoroso"},
 "04.bare": {"en": "bare soil", "es": "suelo desnudo"},
 "04.cap": {"en": "NDVI = (NIR − Red) / (NIR + Red). Healthy vegetation reflects near-infrared strongly — invisible to the eye, obvious to the classifier.",
            "es": "NDVI = (NIR − Rojo) / (NIR + Rojo). La vegetación sana refleja mucho infrarrojo cercano — invisible al ojo, obvio para el clasificador."},

 "05.title": {"en": "Shepherd segmentation: pixels become field parcels",
              "es": "Segmentación Shepherd: los píxeles se vuelven parcelas"},
 "05.px": {"en": "raw pixels", "es": "píxeles sueltos"},
 "05.seg": {"en": "segments ≈ parcels", "es": "segmentos ≈ parcelas"},
 "05.cap": {"en": "K-means groups similar spectra, then connected clumps merge until each segment is one homogeneous field. We classify parcels, not pixels.",
            "es": "K-means agrupa espectros parecidos y los grumos conexos se fusionan hasta que cada segmento es un campo homogéneo. Clasificamos parcelas, no píxeles."},

 "06.title": {"en": "Each parcel becomes one row of features",
              "es": "Cada parcela se convierte en una fila de variables"},
 "06.stats": {"en": "mean · stdev · min · max per band", "es": "media · desv · mín · máx por banda"},
 "06.cap": {"en": "Zonal statistics summarise every band and month inside each segment — hundreds of columns describing each parcel's spectral history.",
            "es": "Las estadísticas zonales resumen cada banda y mes dentro de cada segmento — cientos de columnas que describen la historia espectral de cada parcela."},

 "07.title": {"en": "Field labels teach the model (purity filter)",
              "es": "Las etiquetas de campo enseñan al modelo (filtro de pureza)"},
 "07.pure": {"en": "pure: all points agree → train", "es": "pura: todos coinciden → entrena"},
 "07.mixed": {"en": "mixed → discarded", "es": "mixta → se descarta"},
 "07.cap": {"en": "GPS points (wheat, corn, chickpea…) fall inside segments. Only segments where every point agrees on one class are used for training.",
            "es": "Puntos GPS (trigo, maíz, garbanzo…) caen dentro de los segmentos. Solo los segmentos donde todos los puntos coinciden en una clase se usan para entrenar."},

 "08.title": {"en": "Training: features + labels → a crop classifier",
              "es": "Entrenamiento: variables + etiquetas → clasificador de cultivos"},
 "08.model": {"en": "model", "es": "modelo"},
 "08.browser": {"en": "browser: Random Forest · full pipeline: TPOT (AutoML)",
                "es": "navegador: Random Forest · pipeline completo: TPOT (AutoML)"},
 "08.cap": {"en": "The model learns which spectral histories belong to each crop. In this workshop a Random Forest trains in seconds, inside your browser.",
            "es": "El modelo aprende qué historias espectrales corresponden a cada cultivo. En este taller un Random Forest entrena en segundos, dentro de tu navegador."},

 "09.title": {"en": "The final product: a crop map, parcel by parcel",
              "es": "El producto final: un mapa de cultivos, parcela por parcela"},
 "09.legend": {"en": "wheat · corn · chickpea · other", "es": "trigo · maíz · garbanzo · otros"},
 "09.cap": {"en": "Every segment — labeled or not — receives a predicted class. The result is a decision-ready map you can open in QGIS.",
            "es": "Cada segmento — etiquetado o no — recibe una clase predicha. El resultado es un mapa listo para decisiones, que puedes abrir en QGIS."},

 "10.title": {"en": "The full pipeline (geocrop_analysis_mx) — this workshop in production",
              "es": "El pipeline completo (geocrop_analysis_mx) — este taller en producción"},
 "10.s1": {"en": "download", "es": "descarga"},
 "10.s2": {"en": "geomedian", "es": "geomediana"},
 "10.s3": {"en": "segment", "es": "segmenta"},
 "10.s4": {"en": "features", "es": "variables"},
 "10.s5": {"en": "train", "es": "entrena"},
 "10.s6": {"en": "crop map", "es": "mapa"},
 "10.stac": {"en": "STAC (default, no account)", "es": "STAC (default, sin cuenta)"},
 "10.gee": {"en": "GEE (optional)", "es": "GEE (opcional)"},
 "10.cap": {"en": "pip install, one config file, and the same steps you just ran scale to whole municipalities — months of imagery, radar included, plus your own rasters (DEM, climate) as extra features.",
            "es": "pip install, un archivo de configuración, y los mismos pasos que acabas de correr escalan a municipios completos — meses de imágenes, radar incluido, y tus propios rasters (MDE, clima) como variables extra."},
}


def svg(name, lang, width, height, body):
    tr = lambda key: T[f"{name.split('_')[0]}.{key}"][lang]
    content = body(tr)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" '
            f'width="{width}" height="{height}" {FONT}>\n'
            f'<rect width="{width}" height="{height}" fill="#ffffff"/>\n{content}\n</svg>\n')


def title(text, y=26):
    return f'<text x="20" y="{y}" font-size="15" font-weight="700" fill="{INK}">{text}</text>'


def caption(text, y, width=760):
    # naive two-line wrap for long captions
    words, lines, cur = text.split(), [], ""
    for w in words:
        if len(cur) + len(w) > 108: lines.append(cur); cur = w
        else: cur = (cur + " " + w).strip()
    lines.append(cur)
    out = ""
    for i, ln in enumerate(lines[:3]):
        out += f'<text x="20" y="{y + 15*i}" font-size="12.5" fill="{DIM}">{ln}</text>'
    return out


def a01(tr):
    return f'''{title(tr("title"))}
<g transform="translate(120,52)">
  <rect width="270" height="100" rx="8" fill="#f8fafc" stroke="{FAINT}" stroke-width="1.5"/>
  <rect width="270" height="22" rx="8" fill="#e2e8f0"/>
  <circle cx="14" cy="11" r="4" fill="#f87171"/><circle cx="28" cy="11" r="4" fill="#fbbf24"/><circle cx="42" cy="11" r="4" fill="#4ade80"/>
  <text x="135" y="16" text-anchor="middle" font-size="10" fill="#64748b">{tr("browser")}</text>
  <rect x="85" y="42" width="100" height="40" rx="6" fill="#0ea5e9" opacity=".15" stroke="{BLUE}"/>
  <text x="135" y="67" text-anchor="middle" font-size="14" font-weight="700" fill="#0369a1" font-family="Consolas,monospace">wasm32
    <animate attributeName="opacity" values="1;.35;1" dur="1.6s" repeatCount="indefinite"/></text>
  <text x="135" y="96" text-anchor="middle" font-size="10.5" fill="{DIM}">{tr("inside")}</text>
</g>
<g transform="translate(540,60)">
  <rect width="120" height="76" rx="8" fill="#f1f5f9" stroke="#cbd5e1"/>
  <text x="60" y="32" text-anchor="middle" font-size="11" fill="{FAINT}">{tr("server")}</text>
  <line x1="18" y1="48" x2="102" y2="64" stroke="{RED}" stroke-width="4" stroke-linecap="round"/>
  <line x1="102" y1="48" x2="18" y2="64" stroke="{RED}" stroke-width="4" stroke-linecap="round"/>
  <text x="60" y="100" text-anchor="middle" font-size="10.5" fill="{RED}" font-weight="700">{tr("notused")}</text>
</g>
{caption(tr("cap"), 178)}'''


def a02(tr):
    def catalog(x, y, name, sub, color):
        return f'''<g transform="translate({x},{y})">
  <rect width="176" height="58" rx="8" fill="#f8fafc" stroke="{color}" stroke-width="1.5"/>
  <text x="88" y="24" text-anchor="middle" font-size="11.5" font-weight="700" fill="{INK}">{name}</text>
  <text x="88" y="42" text-anchor="middle" font-size="9.5" fill="{DIM}">{sub}</text>
</g>'''
    packets = ""
    for i, y0 in enumerate((79, 147, 215)):
        packets += (f'<rect x="216" y="{y0}" width="14" height="9" rx="2" fill="{BLUE}" opacity=".8">'
                    f'<animate attributeName="x" values="216;420" dur="2.2s" begin="{i*0.7}s" repeatCount="indefinite"/>'
                    f'<animate attributeName="y" values="{y0};160" dur="2.2s" begin="{i*0.7}s" repeatCount="indefinite"/>'
                    f'<animate attributeName="opacity" values=".9;.9;0" dur="2.2s" begin="{i*0.7}s" repeatCount="indefinite"/></rect>')
    return f'''{title(tr("title"))}
{catalog(30, 50, tr("nasa"), tr("nasa2"), BLUE)}
{catalog(30, 118, tr("mpc"), tr("mpc2"), BLUE)}
{catalog(30, 186, tr("es"), tr("es2"), BLUE)}
{packets}
<g transform="translate(430,120)">
  <rect width="180" height="86" rx="10" fill="#f8fafc" stroke="{FAINT}" stroke-width="1.5"/>
  <rect x="20" y="14" width="140" height="44" rx="4" fill="#0ea5e9" opacity=".12" stroke="{BLUE}"/>
  <text x="90" y="41" text-anchor="middle" font-size="18">🌾</text>
  <text x="90" y="76" text-anchor="middle" font-size="10.5" fill="{DIM}">{tr("you")}</text>
</g>
<g transform="translate(410,236)">
  <rect width="220" height="52" rx="8" fill="#fefce8" stroke="{AMBER}" stroke-dasharray="5 4"/>
  <text x="92" y="21" text-anchor="middle" font-size="10.5" font-weight="700" fill="{INK}">{tr("gee")}</text>
  <text x="92" y="38" text-anchor="middle" font-size="8.2" fill="{AMBER}">{tr("gee2")}</text>
  <g transform="translate(180,16)">
    <rect width="30" height="16" rx="8" fill="#e2e8f0" stroke="{FAINT}"/>
    <circle cx="8" cy="8" r="6" fill="{FAINT}">
      <animate attributeName="cx" values="8;22;22;8;8" keyTimes="0;.15;.5;.65;1" dur="6s" repeatCount="indefinite"/>
      <animate attributeName="fill" values="{FAINT};{AMBER};{AMBER};{FAINT};{FAINT}" keyTimes="0;.15;.5;.65;1" dur="6s" repeatCount="indefinite"/>
    </circle>
  </g>
</g>
<line x1="520" y1="236" x2="520" y2="208" stroke="{AMBER}" stroke-width="1.5" stroke-dasharray="4 4"/>
{caption(tr("cap"), 314)}'''


def a03(tr):
    scenes = ""
    for i in range(5):
        x = 26 + i * 88
        cloud = f'''<g opacity=".95"><ellipse cx="{30+((i*23)%40)}" cy="{26+((i*17)%26)}" rx="16" ry="9" fill="#cbd5e1">
      <animate attributeName="cx" values="{30+((i*23)%40)};{46+((i*23)%40)};{30+((i*23)%40)}" dur="{3+i*0.4}s" repeatCount="indefinite"/></ellipse></g>''' if i != 2 else ""
        scenes += f'''<g transform="translate({x},58)">
  <rect width="72" height="72" rx="5" fill="#dcfce7" stroke="{FAINT}"/>
  <rect x="8" y="40" width="24" height="18" fill="{CORN}" opacity=".7"/>
  <rect x="40" y="12" width="22" height="24" fill="{WHEAT}" opacity=".7"/>
  <rect x="10" y="10" width="20" height="20" fill="{SOIL}" opacity=".6"/>
  {cloud}
  <text x="36" y="86" text-anchor="middle" font-size="8.5" fill="{FAINT}">t{i+1}</text>
</g>'''
    return f'''{title(tr("title"))}
{scenes}
<text x="250" y="160" font-size="11" fill="{DIM}">{tr("cloudy")}</text>
<path d="M 480 94 C 520 94 520 94 552 94" stroke="{BLUE}" stroke-width="2.5" fill="none" marker-end="url(#arr3)"/>
<defs><marker id="arr3" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6 z" fill="{BLUE}"/></marker></defs>
<g transform="translate(560,44)">
  <rect width="100" height="100" rx="6" fill="#dcfce7" stroke="{GREEN}" stroke-width="2">
    <animate attributeName="stroke-width" values="2;3.5;2" dur="2.6s" repeatCount="indefinite"/></rect>
  <rect x="11" y="55" width="33" height="25" fill="{CORN}"/>
  <rect x="55" y="16" width="31" height="33" fill="{WHEAT}"/>
  <rect x="14" y="14" width="28" height="28" fill="{SOIL}" opacity=".8"/>
  <text x="50" y="118" text-anchor="middle" font-size="11" font-weight="700" fill="{GREEN}">{tr("gm")}</text>
  <text x="50" y="133" text-anchor="middle" font-size="9" fill="{DIM}">{tr("gm2")}</text>
</g>
{caption(tr("cap"), 196)}'''


def a04(tr):
    layers = ""
    cols = ["#3b82f6", "#22c55e", "#ef4444", "#7c3aed", "#b45309", "#78350f"]
    for i, c in enumerate(cols):
        layers += (f'<rect x="{40+i*7}" y="{56+i*11}" width="120" height="14" rx="2" fill="{c}" opacity=".75" '
                   f'stroke="#fff" stroke-width=".8"/>')
    for i in range(7):
        layers += (f'<rect x="{40+(6+i)*7}" y="{56+(6+i)*11}" width="120" height="14" rx="2" fill="{GREEN}" '
                   f'opacity="{0.35+i*0.06:.2f}" stroke="#fff" stroke-width=".8"/>')
    return f'''{title(tr("title"))}
{layers}
<text x="100" y="48" text-anchor="middle" font-size="10" fill="{DIM}">{tr("bands")}</text>
<text x="148" y="220" text-anchor="middle" font-size="10" fill="{GREEN}">{tr("idx")}</text>
<g transform="translate(300,68)">
  <text x="0" y="0" font-size="16" font-family="Consolas,monospace" fill="{INK}">NDVI = <tspan fill="#7c3aed">(NIR</tspan> − <tspan fill="#ef4444">Red)</tspan> / <tspan fill="#7c3aed">(NIR</tspan> + <tspan fill="#ef4444">Red)</tspan></text>
</g>
<g transform="translate(320,100)">
  <rect width="130" height="80" rx="6" fill="#16a34a">
    <animate attributeName="fill" values="#16a34a;#4ade80;#16a34a" dur="3s" repeatCount="indefinite"/></rect>
  <text x="65" y="46" text-anchor="middle" font-size="13" font-weight="700" fill="#fff">NDVI 0.8</text>
  <text x="65" y="98" text-anchor="middle" font-size="10" fill="{DIM}">{tr("healthy")}</text>
</g>
<g transform="translate(490,100)">
  <rect width="130" height="80" rx="6" fill="#d6c4a3"/>
  <text x="65" y="46" text-anchor="middle" font-size="13" font-weight="700" fill="#6b5d43">NDVI 0.1</text>
  <text x="65" y="98" text-anchor="middle" font-size="10" fill="{DIM}">{tr("bare")}</text>
</g>
{caption(tr("cap"), 232)}'''


def a05(tr):
    import random
    rng = random.Random(7)
    px = ""
    palette = [WHEAT, CORN, SOIL, "#86efac"]
    for r in range(8):
        for c in range(8):
            col = palette[(r // 3 + c // 3 + (1 if rng.random() < .18 else 0)) % 4]
            px += f'<rect x="{40+c*17}" y="{52+r*17}" width="16" height="16" fill="{col}" opacity=".85"/>'
    return f'''{title(tr("title"))}
{px}
<text x="108" y="204" text-anchor="middle" font-size="10" fill="{DIM}">{tr("px")}</text>
<path d="M 200 116 C 250 116 250 116 288 116" stroke="{BLUE}" stroke-width="2.5" fill="none" marker-end="url(#arr5)"/>
<defs><marker id="arr5" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6 z" fill="{BLUE}"/></marker></defs>
<g transform="translate(300,52)">
  <rect width="136" height="136" fill="#f8fafc" stroke="{FAINT}"/>
  <path d="M0,0 h70 v52 h66 M70,0 v52 M0,52 h70 M0,90 h136 M64,90 v46" stroke="{INK}" stroke-width="2.5" fill="none">
    <animate attributeName="stroke-dasharray" values="0 600;600 0" dur="3.2s" repeatCount="indefinite"/></path>
  <rect x="2" y="2" width="66" height="48" fill="{WHEAT}" opacity=".55"/>
  <rect x="72" y="2" width="62" height="48" fill="{CORN}" opacity=".55"/>
  <rect x="2" y="54" width="132" height="34" fill="#86efac" opacity=".5"/>
  <rect x="2" y="92" width="60" height="42" fill="{SOIL}" opacity=".55"/>
  <rect x="66" y="92" width="68" height="42" fill="{WHEAT}" opacity=".45"/>
</g>
<text x="368" y="204" text-anchor="middle" font-size="10" fill="{DIM}">{tr("seg")}</text>
<g transform="translate(490,70)" font-size="11" fill="{DIM}">
  <text y="0">1. k-means</text>
  <text y="26">2. clumps</text>
  <text y="52">3. merge</text>
  <circle cx="-10" cy="-4" r="3" fill="{BLUE}"><animate attributeName="cy" values="-4;22;48;-4" keyTimes="0;.33;.66;1" dur="4s" repeatCount="indefinite"/></circle>
</g>
{caption(tr("cap"), 232)}'''


def a06(tr):
    rows = ""
    for i in range(4):
        y = 72 + i * 26
        rows += (f'<g opacity="0"><animate attributeName="opacity" values="0;1;1" keyTimes="0;.2;1" dur="4s" begin="{i*0.8}s" repeatCount="indefinite"/>'
                 f'<rect x="330" y="{y}" width="300" height="20" rx="3" fill="{"#f8fafc" if i%2 else "#f1f5f9"}" stroke="#e2e8f0"/>'
                 f'<text x="342" y="{y+14}" font-size="10" font-family="Consolas,monospace" fill="{INK}">seg_{101+i}</text>'
                 f'<text x="420" y="{y+14}" font-size="10" font-family="Consolas,monospace" fill="{DIM}">0.{72-i*9} 0.0{3+i} 21{i}0 …</text></g>')
    return f'''{title(tr("title"))}
<g transform="translate(40,58)">
  <rect width="180" height="120" fill="#f8fafc" stroke="{FAINT}"/>
  <path d="M0,44 h84 M84,0 v44 M84,44 v76 M0,44 h180 M120,44 v76" stroke="{INK}" stroke-width="2" fill="none"/>
  <rect x="2" y="2" width="80" height="40" fill="{WHEAT}" opacity=".6"/>
  <rect x="88" y="2" width="90" height="40" fill="{CORN}" opacity=".6"/>
  <rect x="2" y="48" width="80" height="70" fill="#86efac" opacity=".55"/>
  <rect x="88" y="48" width="30" height="70" fill="{SOIL}" opacity=".6"/>
  <rect x="122" y="48" width="56" height="70" fill="{WHEAT}" opacity=".5"/>
  <rect x="2" y="2" width="80" height="40" fill="none" stroke="{RED}" stroke-width="2.5">
    <animate attributeName="opacity" values="1;0;0;1" keyTimes="0;.25;.9;1" dur="4s" repeatCount="indefinite"/></rect>
</g>
<path d="M 240 118 C 280 118 280 90 322 84" stroke="{BLUE}" stroke-width="2.5" fill="none" marker-end="url(#arr6)"/>
<defs><marker id="arr6" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6 z" fill="{BLUE}"/></marker></defs>
<rect x="330" y="46" width="300" height="20" rx="3" fill="#e2e8f0"/>
<text x="342" y="60" font-size="10" font-weight="700" fill="{INK}">id</text>
<text x="420" y="60" font-size="10" font-weight="700" fill="{INK}">{tr("stats")}</text>
{rows}
{caption(tr("cap"), 208)}'''


def a07(tr):
    return f'''{title(tr("title"))}
<g transform="translate(60,54)">
  <rect width="150" height="110" fill="{WHEAT}" opacity=".5" stroke="{INK}" stroke-width="2"/>
  <g>
    <circle cx="40" cy="40" r="7" fill="{WHEAT}" stroke="#78350f" stroke-width="2"><animate attributeName="r" values="7;9;7" dur="2s" repeatCount="indefinite"/></circle>
    <circle cx="86" cy="66" r="7" fill="{WHEAT}" stroke="#78350f" stroke-width="2"/>
    <circle cx="112" cy="34" r="7" fill="{WHEAT}" stroke="#78350f" stroke-width="2"/>
  </g>
  <text x="75" y="134" text-anchor="middle" font-size="10.5" fill="{GREEN}" font-weight="700">✓ {tr("pure")}</text>
</g>
<g transform="translate(420,54)">
  <rect width="150" height="110" fill="{CORN}" opacity=".45" stroke="{INK}" stroke-width="2"/>
  <circle cx="42" cy="44" r="7" fill="{CORN}" stroke="#365314" stroke-width="2"/>
  <circle cx="96" cy="64" r="7" fill="{WHEAT}" stroke="#78350f" stroke-width="2"><animate attributeName="r" values="7;9;7" dur="2s" repeatCount="indefinite"/></circle>
  <line x1="8" y1="8" x2="142" y2="102" stroke="{RED}" stroke-width="4" stroke-linecap="round" opacity=".9">
    <animate attributeName="opacity" values="0;0;.9;.9" keyTimes="0;.4;.55;1" dur="3.5s" repeatCount="indefinite"/></line>
  <text x="75" y="134" text-anchor="middle" font-size="10.5" fill="{RED}" font-weight="700">✗ {tr("mixed")}</text>
</g>
{caption(tr("cap"), 204)}'''


def a08(tr):
    trees = ""
    for i in range(3):
        x = 348 + i * 40
        trees += (f'<g transform="translate({x},92)" stroke="{GREEN}" stroke-width="2" fill="none">'
                  f'<path d="M0,36 v-14 M0,22 l-12,-12 M0,22 l12,-12 M-12,10 l-6,-8 M-12,10 l4,-9 M12,10 l-4,-9 M12,10 l6,-8"/>'
                  f'<animate attributeName="opacity" values=".3;1;1" keyTimes="0;.3;1" dur="3s" begin="{i*0.5}s" repeatCount="indefinite"/></g>')
    return f'''{title(tr("title"))}
<g transform="translate(40,64)">
  <rect width="130" height="60" rx="6" fill="#f1f5f9" stroke="{FAINT}"/>
  <text x="65" y="26" text-anchor="middle" font-size="10.5" fill="{INK}">features</text>
  <text x="65" y="44" text-anchor="middle" font-size="9" font-family="Consolas,monospace" fill="{DIM}">ndvi… sar… dem…</text>
</g>
<g transform="translate(40,138)">
  <rect width="130" height="46" rx="6" fill="#fef9c3" stroke="{WHEAT}"/>
  <text x="65" y="28" text-anchor="middle" font-size="10.5" fill="#713f12">labels 🌾🌽</text>
</g>
<path d="M 178 94 C 240 94 240 118 300 118 M 178 160 C 240 160 240 130 300 124" stroke="{BLUE}" stroke-width="2.5" fill="none" marker-end="url(#arr8)"/>
<defs><marker id="arr8" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6 z" fill="{BLUE}"/></marker></defs>
<g transform="translate(310,64)">
  <rect width="180" height="110" rx="10" fill="#f0fdf4" stroke="{GREEN}" stroke-width="2"/>
  <text x="90" y="24" text-anchor="middle" font-size="11.5" font-weight="700" fill="{GREEN}">{tr("model")}</text>
  {trees}
</g>
<path d="M 498 118 C 540 118 540 118 570 118" stroke="{BLUE}" stroke-width="2.5" fill="none" marker-end="url(#arr8)"/>
<g transform="translate(578,88)">
  <rect width="70" height="60" rx="6" fill="{WHEAT}" opacity=".25" stroke="{INK}"/>
  <text x="35" y="36" text-anchor="middle" font-size="20">🗺️</text>
</g>
<text x="380" y="204" text-anchor="middle" font-size="10.5" fill="{DIM}">{tr("browser")}</text>
{caption(tr("cap"), 228)}'''


def a09(tr):
    cells = ""
    import random
    rng = random.Random(3)
    palette = [WHEAT, CORN, CHICK, "#86efac", SOIL]
    for r in range(6):
        for c in range(10):
            col = palette[(r * 10 + c + rng.randrange(2)) % 5]
            delay = (c * 0.18 + r * 0.05)
            cells += (f'<rect x="{140+c*40}" y="{58+r*20}" width="39" height="19" fill="{col}" opacity="0">'
                      f'<animate attributeName="opacity" values="0;0;.85;.85" keyTimes="0;{min(delay/5,.9):.2f};{min(delay/5+.08,.98):.2f};1" dur="5s" repeatCount="indefinite"/></rect>')
    return f'''{title(tr("title"))}
<rect x="139" y="57" width="401" height="121" fill="#f8fafc" stroke="{FAINT}"/>
{cells}
<g transform="translate(566,66)" font-size="10.5" fill="{DIM}">
  <rect x="0" y="-9" width="12" height="12" fill="{WHEAT}"/><text x="18" y="1">wheat/trigo</text>
  <rect x="0" y="15" width="12" height="12" fill="{CORN}"/><text x="18" y="25">corn/maíz</text>
  <rect x="0" y="39" width="12" height="12" fill="{CHICK}"/><text x="18" y="49">chickpea</text>
  <rect x="0" y="63" width="12" height="12" fill="{SOIL}"/><text x="18" y="73">no_crop</text>
</g>
{caption(tr("cap"), 208)}'''


def a10(tr):
    steps = [tr("s1"), tr("s2"), tr("s3"), tr("s4"), tr("s5"), tr("s6")]
    icons = ["📥", "🧮", "🧩", "📊", "🤖", "🗺️"]
    belt = ""
    for i, (s, ic) in enumerate(zip(steps, icons)):
        x = 26 + i * 120
        belt += f'''<g transform="translate({x},96)">
  <rect width="104" height="62" rx="8" fill="#f8fafc" stroke="{BLUE}" stroke-width="1.5"/>
  <text x="52" y="28" text-anchor="middle" font-size="17">{ic}</text>
  <text x="52" y="50" text-anchor="middle" font-size="10" font-weight="700" fill="{INK}">{s}</text>
</g>'''
        if i < 5:
            belt += (f'<path d="M {x+106} 127 h 10" stroke="{BLUE}" stroke-width="2.5" marker-end="url(#arrA)"/>')
    return f'''{title(tr("title"))}
<defs><marker id="arrA" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6 z" fill="{BLUE}"/></marker></defs>
<g transform="translate(26,44)">
  <rect width="230" height="34" rx="8" fill="#eff6ff" stroke="{BLUE}"/>
  <text x="115" y="21" text-anchor="middle" font-size="10.5" font-weight="700" fill="{BLUE}">{tr("stac")}</text>
</g>
<g transform="translate(270,44)">
  <rect width="180" height="34" rx="8" fill="#fefce8" stroke="{AMBER}" stroke-dasharray="5 4"/>
  <text x="90" y="21" text-anchor="middle" font-size="10.5" fill="{AMBER}">{tr("gee")}</text>
</g>
<path d="M 140 78 v 14 M 360 78 C 360 90 200 84 150 92" stroke="{FAINT}" stroke-width="1.5" fill="none" stroke-dasharray="4 4"/>
{belt}
<circle r="5" fill="{GREEN}">
  <animateMotion path="M 78 127 H 682" dur="5s" repeatCount="indefinite"/>
  <animate attributeName="opacity" values="1;1;0" keyTimes="0;.94;1" dur="5s" repeatCount="indefinite"/>
</circle>
{caption(tr("cap"), 190)}'''


ANIMS = [
    ("01_where_it_runs", 760, 195, a01),
    ("02_data_sources", 760, 352, a02),
    ("03_geomedian", 760, 222, a03),
    ("04_bands_ndvi", 760, 250, a04),
    ("05_segmentation", 760, 250, a05),
    ("06_features", 760, 225, a06),
    ("07_labels_purity", 760, 220, a07),
    ("08_training", 760, 245, a08),
    ("09_crop_map", 760, 225, a09),
    ("10_full_pipeline", 760, 210, a10),
]


def main():
    for lang in ("en", "es"):
        out_dir = os.path.join(ROOT, "anim", lang)
        os.makedirs(out_dir, exist_ok=True)
        for name, w, h, builder in ANIMS:
            path = os.path.join(out_dir, f"{name}.svg")
            with open(path, "w", encoding="utf-8") as fh:
                fh.write(svg(name, lang, w, h, builder))
            print(f"{lang}/{name}.svg")


if __name__ == "__main__":
    main()
