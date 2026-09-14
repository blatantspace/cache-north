# cache.north Wear (fake storefront)

Idea bag for northern mashup kit. Not checkout. Not Shopify.

## Open

- Shop: `site/shop/index.html`
- Extras · Faves: `site/shop/faves.html`
- Catalogue: `site/shop/catalog.json`
- Product images: `site/shop/products/`

From the recruitment page, use the **Wear** / **Extras · Faves** links in the top bar.

## Featured by default

Ben’s locked keepers (status `promoted`, homepage teaser on):

| ID | SKU | Name |
|---|---|---|
| v4-021 | CN-021-STRAP | Strap Seal Boot |
| v4-027 | CN-027-GAUNT | Gauntlet Cuff Boot |
| v4-034 | CN-034-POINT | Point Field Shell |

Earlier approvals ship as `idea` (promote anytime): v3-002, v3-004, v3-009, v3-017, v3-028, mash-013, mash-022, mash-025.

**v5 brand-swap gaiter variants** (36 SKUs from `refs/outfit-mashups-v5/`, all `idea`): practical gaiters off keepers 021 / 027 / 034. Filter by Kit (boots / shells / gaiters / …) or Lineage (021 Strap / 027 Gaunt / 034 Point).

**v6 kit extras** (27 SKUs from `refs/outfit-mashups-v6-kit/`, all `idea`, lineage `extras`): hats (9), eyewear (5), masks (4), XC skis (9). Kit filters · Hats / Eyewear / Masks / Skis. Lineage · Extras kit.

**v7 gumsole** (14 SKUs from `refs/outfit-mashups-v7-gumsole/`, all `idea`, kit `gumsole`, lineage `v4-021`): Kit filter · Gumsole (also under Boots). Lineage · 021 Strap.

**v7 kit extras** (32 SKUs from `refs/outfit-mashups-v7-kit/`, all `idea`, lineage `extras`): hats (8), Visor Seal masks (8), leather wind protection (8, kit `protection`), thermal goggles (8, eyewear). Kit filter · Wind leather. Lineage · Extras kit.

### Creative read (Sep 13) — buddy liked cowls / storm collars

Leather used **functionally** for wind + cold (throat / nape / seal) beat
pieces that only look nice. **Modern outdoor silhouettes** that **happen to be
leather** — not medieval / LARP tannery cosplay. See `RUNWAY-DRIVE.md` § Wear kit lock.

**v8 −50 leather** (16 SKUs, lineage `leather50`, kit `protection`): storm
collars, cowls, hood-interface seals, powder cuffs, overboot gaiter, mitt cuff
ring. Shop filter · **−50 leather**.

**Sort** defaults to newest → oldest via `addedAt`. Toggle Oldest in the Sort row. Clear filters resets Status / Kit / Lineage.

## Promote / demote

All local. No backend.

| Key | What it stores |
|---|---|
| `cacheNorth.shop.status` | `{ "<id>": "idea" \| "promoted" \| "archived" }` |
| `cacheNorth.shop.homepageTeasers` | `{ "<id>": true \| false }` |
| `cacheNorth.shop.faves` | `{ "<id>": { "favedAt": ISO, "note": "…" } }` personal likes (≠ promote) |
| `cacheNorth.shop.bag` | idea-bag line items |

**Ben faves on disk (localhost only):** `site/shop/ben-faves.json` — heart/unheart/notes on `localhost:8765` POST to `/api/faves`; other origins stay localStorage-only. Agents read that file. Never sent remote.

- **Fave** (♡ / ♥) → personal shortlist on **Extras · Faves**. Does not promote.
- **Promote** → status `promoted`, appears on the promoted shelf
- **Demote** → back to `idea`
- **Archive** / **Restore idea**
- **Homepage teaser** → flag for the main `index.html` strip (reads the same localStorage key when you open muster from the same origin)

**Export promoted JSON** downloads the current promoted set. **Reset promotes** clears status/teaser localStorage and falls back to `catalog.json` defaults.

On Extras · Faves: sort / filter, per-item notes, export / import JSON, clear with confirm.

## Edit the catalogue

Edit `catalog.json`, drop images in `products/`, refresh. Status defaults in JSON are the seed; browser overrides win until you reset.

## Detail / bag

Click a card (or `?sku=CN-021-STRAP`). Fake sizes + **Add to bag** toast: “Idea bag — not for sale yet.”
