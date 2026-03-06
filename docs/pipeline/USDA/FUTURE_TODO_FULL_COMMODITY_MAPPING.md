# Full USDA API Commodity Mapping — COMPLETED ✅

_Resolved March 5, 2026 on branch `usda_more_mapping`._

## What was built

`reviewed_api_mappings.py` (in `utils/`) is the single source of truth for NASS
commodity name → QuickStats `commodity_desc` mappings. It now contains:

- **356 `OFFICIAL_API_MAPPINGS` entries** covering all NASS crops, livestock,
  dairy, grains, specialty, and field commodities relevant to California ETL.
- **~100 `DISABLED_API_MAPPINGS` entries** for aggregates, livestock
  subcategories, and codes that have no QuickStats counterpart — these produce
  `api_name = NULL` in the DB and are intentionally excluded from API queries.
- `get_api_name(name)` — returns the QuickStats name, or `None` for DISABLED.
- `guess_api_name(name)` — heuristic fallback (strips subcategory suffixes).
- `--list-quickstats [FILE]` CLI flag — dumps the live QuickStats name list.
- `--output FILE` CLI flag — writes a draft additions block for copy-paste
  review.

Non-obvious mappings resolved: `PISTACHIO NUTS→PISTACHIOS`,
`SWEETPOTATOES→SWEET POTATOES`, `CANTALOUPES→MELONS`, `WATERMELONS→MELONS`,
`HONEYDEW MELONS→MELONS`, `PEPPERMINT→MINT`, `SPEARMINT→MINT`,
`SWEET CHERRIES→CHERRIES`, `TART CHERRIES→CHERRIES`, `PEPPERS-BELL→PEPPERS`,
`LETTUCE-HEAD→LETTUCE`, `SUNFLOWER SEED ALL→SUNFLOWER`,
`TOMATOES FOR PROCESSING→TOMATOES`, `WALNUTS (ENGLISH)→WALNUTS`, etc.

## How it integrates

`seed_commodity_mappings.py` imports `get_api_name` from this file and uses it
as the authoritative source when seeding/backfilling `usda_commodity.api_name`.
The CSV (`commodity_mappings.csv`) and the DB are always kept consistent through
the `--export-csv` / `--save-to-db` workflow.

## Still open (future)

- TODO 3: ON CONFLICT upsert with `UNIQUE (name)` on `usda_commodity` — deferred
  until AMS integration design is confirmed.

---

_Original task added: 2026-02-05. Completed: 2026-03-05._
