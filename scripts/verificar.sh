#!/usr/bin/env bash
# Verificaciones obligatorias antes de dar un cambio por terminado (REGLAS.md 5).
#
#   bash scripts/verificar.sh
#
# Tiene que terminar en "TODO OK".

set -uo pipefail
cd "$(dirname "$0")/.."
fallas=0

echo "== Datos (data/) =="
if python3 scripts/validar_datos.py >/dev/null; then
    echo "   ok"
else
    echo "   FALLA: python3 scripts/validar_datos.py"
    fallas=$((fallas + 1))
fi

echo "== JavaScript del prototipo =="
if command -v node >/dev/null; then
    tmp=$(mktemp --suffix=.js)
    python3 - "$tmp" <<'PY'
import re, sys
html = open("prototipo/index.html", encoding="utf-8").read()
bloques = re.findall(r"<script>(.*?)</script>", html, re.S)
open(sys.argv[1], "w", encoding="utf-8").write("\n;\n".join(bloques))
PY
    if node --check "$tmp"; then echo "   ok"; else echo "   FALLA: error de sintaxis en prototipo/index.html"; fallas=$((fallas + 1)); fi
    rm -f "$tmp"
else
    echo "   (se omite: no hay node en este entorno)"
fi

echo "== Sin secretos =="
if git grep -nIE "script\.google\.com/macros/s/|AKfyc[A-Za-z0-9_-]{20,}|ghp_[A-Za-z0-9]{20,}|AIza[0-9A-Za-z_-]{30,}" -- . ':!scripts/verificar.sh' >/dev/null; then
    echo "   FALLA: parece haber una URL de Apps Script o una clave versionada"
    fallas=$((fallas + 1))
else
    echo "   ok"
fi

echo
if [ "$fallas" -eq 0 ]; then echo "TODO OK"; else echo "$fallas FALLA(S)"; exit 1; fi
