# cache.north

Northern DIY recruitment surface + pretend Wear kit store.

**Live:** https://blatantspace.github.io/cache-north/

| Path | What |
|------|------|
| `/` | Muster / recruitment |
| `/shop/` | Wear · pretend store |
| `/shop/faves.html` | Extras · Faves |

## Local

```bash
./serve-8765.sh
# → http://127.0.0.1:8765/
```

On localhost, faves also POST to `/api/faves` and write `shop/ben-faves.json` (gitignored) for agents.

## Deploy

Pushes to `main` publish via GitHub Pages (root of this repo = `site/`).
