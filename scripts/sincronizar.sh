#!/usr/bin/env bash
# Trae main al día en la rama actual y muestra qué llegó y de quién.
# Se corre al empezar cada sesión y antes del primer cambio (REGLAS.md 3).
#
#   bash scripts/sincronizar.sh

set -uo pipefail
cd "$(dirname "$0")/.."
BASE="${1:-main}"

git fetch origin "$BASE" || { echo "No se pudo hacer fetch de $BASE. Avísale al usuario antes de seguir."; exit 1; }

rama=$(git rev-parse --abbrev-ref HEAD)
nuevos=$(git log --format='%h  %an  %ad  %s' --date=short "HEAD..FETCH_HEAD")
if [ -z "$nuevos" ]; then
    echo "Al día con $BASE."
else
    echo "Llegó desde $BASE:"
    echo "$nuevos"
    echo
    if [ "$rama" = "$BASE" ]; then
        git merge --ff-only FETCH_HEAD
    else
        git merge --no-edit FETCH_HEAD
    fi
fi
echo
echo "Ahora lee BITACORA.md (Pendientes abiertos y En curso) antes de tocar nada."
