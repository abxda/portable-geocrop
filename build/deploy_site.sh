#!/usr/bin/env bash
# Builds the workshop site (JupyterLite) + bilingual landing/theory pages and
# publishes it to the gh-pages branch.
#
#   USAGE:  bash build/deploy_site.sh [--no-push]
#
# Steps (mirrors portable-satelital's deploy_taller.ps1):
#   1. stage contents (notebooks + anim/ + files/) into _contents
#   2. jupyter lite build with overrides (windowingMode=none = full cells, so
#      long outputs are never virtualised/clipped)
#   3. overlay landing + theory, INJECTING the jupyter-config-data block from
#      the generated index.html (JupyterLite inherits its config by reading
#      parent index pages; a landing page without that block breaks /lab)
#   4. force-push the built site to the gh-pages branch
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SITE="$ROOT/dist/site"
CONTENTS="$ROOT/dist/_contents"
JUPYTER="${JUPYTER:-jupyter}"
NO_PUSH="${1:-}"

echo "==> [1/4] staging contents"
rm -rf "$CONTENTS"; mkdir -p "$CONTENTS"
cp "$ROOT/Crop_Classification_Workshop.ipynb" "$CONTENTS/"
cp "$ROOT/Taller_Clasificacion_Cultivos.ipynb" "$CONTENTS/"
cp -r "$ROOT/anim" "$CONTENTS/anim"
cp -r "$ROOT/files" "$CONTENTS/files"

echo "==> [2/4] jupyter lite build"
rm -rf "$SITE" "$ROOT/.jupyterlite.doit.db"
( cd "$ROOT" && "$JUPYTER" lite build \
    --contents "$CONTENTS" \
    --settings-overrides "$ROOT/overrides.json" \
    --output-dir "$SITE" )

echo "==> [3/4] overlay landing + theory (injecting jupyter-config-data)"
python3 - "$SITE" "$ROOT/web" <<'PY'
import re, sys, pathlib
site, web = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
built = (site / "index.html").read_text(encoding="utf-8")
m = re.search(r'(?s)<script id="jupyter-config-data"[^>]*>.*?</script>', built)
if not m:
    raise SystemExit("jupyter-config-data block not found in generated index.html")
landing = (web / "index.html").read_text(encoding="utf-8")
if "<!--JUPYTER_CONFIG-->" not in landing:
    raise SystemExit("landing page missing <!--JUPYTER_CONFIG--> placeholder")
(site / "index.html").write_text(
    landing.replace("<!--JUPYTER_CONFIG-->", m.group(0)), encoding="utf-8")
(site / "theory.html").write_text((web / "theory.html").read_text(encoding="utf-8"),
                                  encoding="utf-8")
# animations are referenced by the landing/theory pages with relative paths too
import shutil
if (site / "anim").exists():
    shutil.rmtree(site / "anim")
shutil.copytree(web.parent / "anim", site / "anim")
print("   landing + theory overlaid, config injected")
PY

# JupyterLite needs .nojekyll so GitHub Pages serves the _-prefixed dirs
touch "$SITE/.nojekyll"

echo "==> [4/4] publish to gh-pages"
if [ "$NO_PUSH" = "--no-push" ]; then
    echo "   --no-push: built at $SITE, not pushing."
    exit 0
fi
cd "$SITE"
git init -q
git checkout -q -b gh-pages
git add -A
git -c user.name="Claude Fable" -c user.email="noreply@anthropic.com" \
    commit -q -m "Deploy workshop site (JupyterLite + bilingual landing)"
git push -f -q "git@github.com-portable-geocrop:abxda/portable-geocrop.git" gh-pages
echo "   pushed to gh-pages."
