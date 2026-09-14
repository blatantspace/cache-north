#!/bin/bash
# Durable local server for Cache North preview (port 8765)
# Static files + POST /api/faves → shop/ben-faves.json (Ben localhost disk sync)
SITE_DIR="$(cd "$(dirname "$0")" && pwd)"
LOG=/tmp/cache-north-http.log
PIDFILE="$SITE_DIR/.http-server.pid"
SERVER_PY="$SITE_DIR/serve_faves.py"
cd "$SITE_DIR" || exit 1
# Kill stale listener if any
for p in $(lsof -t -iTCP:8765 -sTCP:LISTEN 2>/dev/null); do kill -9 "$p" 2>/dev/null; done
# Fully detach: new session so agent/shell exit cannot kill us
/usr/bin/python3 -c "
import os, subprocess, sys
log = open('$LOG', 'a', buffering=1)
p = subprocess.Popen(
    [sys.executable, '$SERVER_PY', '8765'],
    cwd='$SITE_DIR',
    stdout=log,
    stderr=subprocess.STDOUT,
    stdin=subprocess.DEVNULL,
    start_new_session=True,
)
open('$PIDFILE', 'w').write(str(p.pid) + '\n')
print(p.pid)
"
