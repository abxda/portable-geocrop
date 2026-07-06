"""Module 7 — Machine learning from zero."""

from course.common import md, code, LOAD_TILE_EN, LOAD_TILE_ES

MODULE = dict(
    num=7,
    fname={"en": "07_machine_learning_from_zero.ipynb", "es": "07_machine_learning_desde_cero.ipynb"},
    title={"en": "Module 7 — Machine learning from zero",
           "es": "Módulo 7 — Aprendizaje automático desde cero"},
    cards=[
        ("machine-learning", {"en": "Machine learning", "es": "Aprendizaje automático"}),
        ("decision-tree", {"en": "Decision tree", "es": "Árbol de decisión"}),
        ("random-forest", {"en": "Random forest", "es": "Bosque aleatorio"}),
        ("model-training", {"en": "Model training", "es": "Entrenamiento de modelos"}),
        ("training-dataset", {"en": "Training vs test data",
                              "es": "Datos de entrenamiento vs prueba"}),
        ("validation", {"en": "Validation", "es": "Validación"}),
        ("confusion-matrix", {"en": "Confusion matrix", "es": "Matriz de confusión"}),
        ("overall-accuracy", {"en": "Overall accuracy", "es": "Exactitud global"}),
        ("producer-s-accuracy", {"en": "Producer's accuracy", "es": "Exactitud del productor"}),
        ("recall", {"en": "Recall", "es": "Exhaustividad (recall)"}),
        ("f1-score", {"en": "F1-score", "es": "Puntaje F1"}),
        ("cohen-s-kappa", {"en": "Cohen's kappa", "es": "Kappa de Cohen"}),
        ("omission", {"en": "Omission error", "es": "Error de omisión"}),
        ("commission", {"en": "Commission error", "es": "Error de comisión"}),
    ],
    cells=[

md(
"""# 🤖 Module 7 — Machine learning from zero

🧭 **Objectives** — understand what a **model** is, meet the **decision tree**
and the **random forest**, learn the golden rule of honest evaluation
(**train/test split**), train a classifier on your labelled parcels, and
*read* the quality report: **accuracy**, **precision/recall**, **F1**,
**kappa**, and the **confusion matrix** — plus **omission** vs **commission**
errors.

📚 **What is a model?** A model is a function learned from examples. We show
it parcels whose crop we know (features → label), and it learns rules to
predict the crop of parcels it has never seen. This is **supervised
learning**.

📚 **Decision tree → random forest.** A **decision tree** asks yes/no
questions about the features ("is NIR mean > 3000?") down to a leaf that
names a crop. One tree overfits — it memorizes quirks. A **random forest**
grows hundreds of trees, each on a random slice of the data and features,
and lets them **vote**. The crowd is far more accurate and stable than any
single tree.

📚 **The golden rule.** Never judge a model on the data it trained on — of
course it aced those. Split the labelled parcels into a **training set** (it
learns from) and a **test set** (held back, used only to grade). Accuracy on
the *test* set estimates how it will do on the real, unseen map.

![training](../../anim/en/08_training.svg)
""",
"""# 🤖 Módulo 7 — Aprendizaje automático desde cero

🧭 **Objetivos** — entender qué es un **modelo**, conocer el **árbol de
decisión** y el **bosque aleatorio**, aprender la regla de oro de la
evaluación honesta (**división entrenamiento/prueba**), entrenar un
clasificador con tus parcelas etiquetadas, y *leer* el reporte de calidad:
**exactitud**, **precisión/exhaustividad**, **F1**, **kappa**, y la **matriz
de confusión** — más los errores de **omisión** vs **comisión**.

📚 **¿Qué es un modelo?** Un modelo es una función aprendida de ejemplos. Le
mostramos parcelas cuyo cultivo conocemos (variables → etiqueta), y aprende
reglas para predecir el cultivo de parcelas que nunca vio. Esto es
**aprendizaje supervisado**.

📚 **Árbol de decisión → bosque aleatorio.** Un **árbol de decisión** hace
preguntas sí/no sobre las variables ("¿la media de NIR > 3000?") hasta una
hoja que nombra un cultivo. Un solo árbol se sobreajusta — memoriza rarezas.
Un **bosque aleatorio** hace crecer cientos de árboles, cada uno sobre una
rebanada aleatoria de los datos y variables, y los deja **votar**. La
multitud es mucho más exacta y estable que cualquier árbol solo.

📚 **La regla de oro.** Nunca juzgues un modelo con los datos con que se
entrenó — por supuesto que salió perfecto en esos. Divide las parcelas
etiquetadas en un **conjunto de entrenamiento** (del que aprende) y un
**conjunto de prueba** (apartado, usado solo para calificar). La exactitud
en el conjunto de *prueba* estima cómo le irá en el mapa real, no visto.

![entrenamiento](../../anim/es/08_training.svg)
"""),

md(
"""## Rebuild features and labels

As in Module 6, a fresh kernel means we re-create the parcels, their
features, and the pure labels before training.
""",
"""## Reconstruye variables y etiquetas

Como en el Módulo 6, un kernel limpio significa que volvemos a crear las
parcelas, sus variables, y las etiquetas puras antes de entrenar.
"""),

code(LOAD_TILE_EN, LOAD_TILE_ES),

code(
"""import numpy as np, rasterio, json
import scipy.ndimage, sklearn.cluster
import shepherd_wasm

async def get_file(name):
    import os, sys
    for cand in (f"files/{name}", name, f"../files/{name}", f"../../files/{name}"):
        if os.path.exists(cand):
            return cand
    dest = f"/tmp/{name}"
    if not os.path.exists(dest):
        url = f"__RAW__/{name}"
        if sys.platform == "emscripten":
            from pyodide.http import pyfetch
            resp = await pyfetch(url); open(dest, "wb").write(await resp.bytes())
        else:
            import urllib.request; urllib.request.urlretrieve(url, dest)
    return dest

with rasterio.open(TILE) as src:
    img = src.read(); band_names = list(src.descriptions)
LABELS = await get_file("crop_labels_384.tif")
NAMES  = await get_file("class_names.json")

result = shepherd_wasm.doShepherdSegmentation(
    img, numClusters=30, minSegmentSize=50, imgNullVal=0, fixedKMeansInit=True)
seg = result.segimg.astype(np.int32); n_seg = int(seg.max())

flat = seg.ravel(); counts = np.bincount(flat, minlength=n_seg+1).astype(float)
counts[counts == 0] = 1
features = np.zeros((n_seg+1, len(band_names)*2), dtype=np.float32)
for b in range(len(band_names)):
    v = img[b].ravel().astype(np.float64)
    s1 = np.bincount(flat, weights=v, minlength=n_seg+1)
    s2 = np.bincount(flat, weights=v*v, minlength=n_seg+1)
    m = s1/counts; var = np.maximum(s2/counts - m*m, 0)
    features[:, 2*b], features[:, 2*b+1] = m, np.sqrt(var)

with rasterio.open(LABELS) as src:
    lab = src.read(1)
class_names = {int(k): v for k, v in json.load(open(NAMES)).items()}
parcel_label = np.zeros(n_seg+1, dtype=int)
for sid in np.unique(seg[lab > 0]):
    u = np.unique(lab[(seg == sid) & (lab > 0)])
    if len(u) == 1: parcel_label[sid] = u[0]
train_ids = np.flatnonzero(parcel_label)
print(f"Ready: {len(train_ids)} labelled parcels, {features.shape[1]} features each")""",
"""import numpy as np, rasterio, json
import scipy.ndimage, sklearn.cluster
import shepherd_wasm

async def trae_archivo(name):
    import os, sys
    for cand in (f"files/{name}", name, f"../files/{name}", f"../../files/{name}"):
        if os.path.exists(cand):
            return cand
    dest = f"/tmp/{name}"
    if not os.path.exists(dest):
        url = f"__RAW__/{name}"
        if sys.platform == "emscripten":
            from pyodide.http import pyfetch
            resp = await pyfetch(url); open(dest, "wb").write(await resp.bytes())
        else:
            import urllib.request; urllib.request.urlretrieve(url, dest)
    return dest

with rasterio.open(TILE) as src:
    img = src.read(); nombres_banda = list(src.descriptions)
LABELS  = await trae_archivo("crop_labels_384.tif")
NOMBRES = await trae_archivo("class_names.json")

resultado = shepherd_wasm.doShepherdSegmentation(
    img, numClusters=30, minSegmentSize=50, imgNullVal=0, fixedKMeansInit=True)
seg = resultado.segimg.astype(np.int32); n_seg = int(seg.max())

plano = seg.ravel(); conteos = np.bincount(plano, minlength=n_seg+1).astype(float)
conteos[conteos == 0] = 1
variables = np.zeros((n_seg+1, len(nombres_banda)*2), dtype=np.float32)
for b in range(len(nombres_banda)):
    v = img[b].ravel().astype(np.float64)
    s1 = np.bincount(plano, weights=v, minlength=n_seg+1)
    s2 = np.bincount(plano, weights=v*v, minlength=n_seg+1)
    m = s1/conteos; var = np.maximum(s2/conteos - m*m, 0)
    variables[:, 2*b], variables[:, 2*b+1] = m, np.sqrt(var)

with rasterio.open(LABELS) as src:
    lab = src.read(1)
nombres_clase = {int(k): v for k, v in json.load(open(NOMBRES)).items()}
etiqueta_parcela = np.zeros(n_seg+1, dtype=int)
for sid in np.unique(seg[lab > 0]):
    u = np.unique(lab[(seg == sid) & (lab > 0)])
    if len(u) == 1: etiqueta_parcela[sid] = u[0]
ids_entrena = np.flatnonzero(etiqueta_parcela)
print(f"Listo: {len(ids_entrena)} parcelas etiquetadas, {variables.shape[1]} variables c/u")"""),

md(
"""## Split, train, and grade honestly

`train_test_split` holds back 30% of the parcels for testing, **stratified**
so every crop is represented in both parts. We fit a `RandomForestClassifier`
on the training 70%, then grade it on the untouched 30% with a
`classification_report`.
""",
"""## Divide, entrena, y califica con honestidad

`train_test_split` aparta el 30% de las parcelas para prueba,
**estratificado** para que cada cultivo esté en ambas partes. Ajustamos un
`RandomForestClassifier` con el 70% de entrenamiento, y lo calificamos con el
30% intacto usando un `classification_report`.
"""),

code(
"""from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

X = features[train_ids]
y = parcel_label[train_ids]
X_tr, X_te, y_tr, y_te = train_test_split(
    X, y, test_size=0.3, random_state=42, stratify=y)

model = RandomForestClassifier(n_estimators=300, random_state=42, n_jobs=-1)
model.fit(X_tr, y_tr)

present = sorted(np.unique(y_te))
print(classification_report(
    y_te, model.predict(X_te),
    labels=present, target_names=[class_names[c] for c in present]))""",
"""from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

X = variables[ids_entrena]
y = etiqueta_parcela[ids_entrena]
X_tr, X_te, y_tr, y_te = train_test_split(
    X, y, test_size=0.3, random_state=42, stratify=y)

modelo = RandomForestClassifier(n_estimators=300, random_state=42, n_jobs=-1)
modelo.fit(X_tr, y_tr)

presentes = sorted(np.unique(y_te))
print(classification_report(
    y_te, modelo.predict(X_te),
    labels=presentes, target_names=[nombres_clase[c] for c in presentes]))"""),

md(
"""## Read the report

- **precision** of a crop = of the parcels the model *called* this crop, how
  many really were? Low precision = **commission** error (false alarms).
- **recall** of a crop = of the parcels that *truly* were this crop, how many
  did the model catch? Low recall = **omission** error (misses).
- **f1-score** = the balance of precision and recall in one number.
- **accuracy** (bottom) = overall fraction correct across all crops.

Now visualize the **confusion matrix**: rows = true crop, columns =
predicted. The diagonal is correct; off-diagonal cells show *which* crops get
confused for which — far more informative than a single accuracy number.
""",
"""## Lee el reporte

- **precision** de un cultivo = de las parcelas que el modelo *llamó* así,
  ¿cuántas lo eran de verdad? Precisión baja = error de **comisión** (falsas
  alarmas).
- **recall** de un cultivo = de las parcelas que *en verdad* eran ese
  cultivo, ¿cuántas atrapó el modelo? Recall bajo = error de **omisión**
  (se le escaparon).
- **f1-score** = el balance de precisión y recall en un solo número.
- **accuracy** (abajo) = fracción global correcta entre todos los cultivos.

Ahora visualiza la **matriz de confusión**: filas = cultivo real, columnas =
predicho. La diagonal es lo correcto; las celdas fuera de la diagonal
muestran *qué* cultivos se confunden con cuáles — mucho más informativo que
un solo número de exactitud.
"""),

code(
"""from sklearn.metrics import confusion_matrix, cohen_kappa_score
import matplotlib.pyplot as plt

y_pred = model.predict(X_te)
cm = confusion_matrix(y_te, y_pred, labels=present)
print("Cohen's kappa (agreement beyond chance):", round(cohen_kappa_score(y_te, y_pred), 3))

fig, ax = plt.subplots(figsize=(6.5, 6))
im = ax.imshow(cm, cmap="Blues")
ax.set_xticks(range(len(present))); ax.set_yticks(range(len(present)))
ax.set_xticklabels([class_names[c] for c in present], rotation=45, ha="right")
ax.set_yticklabels([class_names[c] for c in present])
ax.set_xlabel("predicted"); ax.set_ylabel("true")
for i in range(len(present)):
    for j in range(len(present)):
        ax.text(j, i, cm[i, j], ha="center",
                color="white" if cm[i, j] > cm.max()/2 else "black")
ax.set_title("Confusion matrix (diagonal = correct)")
plt.tight_layout(); plt.show()""",
"""from sklearn.metrics import confusion_matrix, cohen_kappa_score
import matplotlib.pyplot as plt

y_pred = modelo.predict(X_te)
cm = confusion_matrix(y_te, y_pred, labels=presentes)
print("Kappa de Cohen (acuerdo más allá del azar):", round(cohen_kappa_score(y_te, y_pred), 3))

fig, ax = plt.subplots(figsize=(6.5, 6))
im = ax.imshow(cm, cmap="Blues")
ax.set_xticks(range(len(presentes))); ax.set_yticks(range(len(presentes)))
ax.set_xticklabels([nombres_clase[c] for c in presentes], rotation=45, ha="right")
ax.set_yticklabels([nombres_clase[c] for c in presentes])
ax.set_xlabel("predicho"); ax.set_ylabel("real")
for i in range(len(presentes)):
    for j in range(len(presentes)):
        ax.text(j, i, cm[i, j], ha="center",
                color="white" if cm[i, j] > cm.max()/2 else "black")
ax.set_title("Matriz de confusión (diagonal = correcto)")
plt.tight_layout(); plt.show()"""),

md(
"""## 🧪 Check yourself

**Why is accuracy measured on the test set, not the training set?**

<details><summary>Show answer</summary>

A model can memorize its training data and score near-perfectly on it while
failing on new parcels (overfitting). The held-back test set was never seen
during training, so its accuracy honestly estimates performance on the real,
unseen map.

</details>

**A crop has high precision but low recall. In plain terms, what is the
model doing — and is that omission or commission?**

<details><summary>Show answer</summary>

When it says "this crop" it is usually right (high precision), but it misses
many true parcels of that crop (low recall). Missing true positives is
**omission** error.

</details>

**Why prefer a random forest over a single decision tree?**

<details><summary>Show answer</summary>

One tree overfits — it latches onto quirks of the training data. A forest
averages hundreds of varied trees, canceling out individual mistakes, giving
more accurate and more stable predictions.

</details>
""",
"""## 🧪 Ponte a prueba

**¿Por qué la exactitud se mide en el conjunto de prueba y no en el de
entrenamiento?**

<details><summary>Ver respuesta</summary>

Un modelo puede memorizar sus datos de entrenamiento y salir casi perfecto en
ellos mientras falla en parcelas nuevas (sobreajuste). El conjunto de prueba
apartado nunca se vio durante el entrenamiento, así que su exactitud estima
con honestidad el desempeño en el mapa real, no visto.

</details>

**Un cultivo tiene precisión alta pero recall bajo. En palabras simples,
¿qué hace el modelo — y eso es omisión o comisión?**

<details><summary>Ver respuesta</summary>

Cuando dice "este cultivo" suele acertar (precisión alta), pero se le escapan
muchas parcelas verdaderas de ese cultivo (recall bajo). Perder positivos
verdaderos es error de **omisión**.

</details>

**¿Por qué preferir un bosque aleatorio sobre un solo árbol de decisión?**

<details><summary>Ver respuesta</summary>

Un árbol se sobreajusta — se aferra a rarezas de los datos de entrenamiento.
Un bosque promedia cientos de árboles variados, cancelando errores
individuales, dando predicciones más exactas y estables.

</details>
"""),

],
)
