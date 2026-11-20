#!/bin/sh
# Intelligent-AML POSIX Shell Shim for Vercel
# Intercepts 'vite build' or 'vite' calls on Linux containers
DIR="$(cd "$(dirname "$0")" && pwd)"
if [ -f "$DIR/../../frontend/bin/vite-compat.cjs" ]; then
    BRIDGE="$DIR/../../frontend/bin/vite-compat.cjs"
elif [ -f "$DIR/../frontend/bin/vite-compat.cjs" ]; then
    BRIDGE="$DIR/../frontend/bin/vite-compat.cjs"
elif [ -f "./frontend/bin/vite-compat.cjs" ]; then
    BRIDGE="./frontend/bin/vite-compat.cjs"
else
    BRIDGE="$(pwd)/frontend/bin/vite-compat.cjs"
fi

exec node "$BRIDGE" "$@"
